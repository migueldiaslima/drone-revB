# R7 - step 1 of handover 2 (D-056 BODY, D-059 identical arms).
# Replaces BODY with the keel export; keeps ARM_pp as the single arm part ARM (renamed, generic surface names)
# and instances it four times, rotated about z. Checks every result and stops on a mismatch.
# Run in a saved copy (revB_v03B_D056.cae). Set STEP_DIR first (folder of the new zip).
from __future__ import print_function
from abaqus import *
from abaqusConstants import *
import math

STEP_DIR = r'C:\path\to\new_zip_folder'      # <-- folder with the D-056 BODY.step
MODEL = 'revB_v03B'
m = mdb.models[MODEL]
a = m.rootAssembly
CORNERS = {'pp': (1, 1), 'pm': (1, -1), 'mp': (-1, 1), 'mm': (-1, -1)}
ROT = {'pp': 0.0, 'pm': -90.0, 'mp': 90.0, 'mm': 180.0}
R2 = 1.0 / math.sqrt(2.0)

def stop(msg):
    raise Exception('R7 STOPPED: ' + msg)

def fa(p, idx):                       # FaceArray from a list of face indices
    idx = sorted(set(idx))
    s = p.faces[idx[0]:idx[0] + 1]
    for i in idx[1:]:
        s = s + p.faces[i:i + 1]
    return s

def area(p, idx):
    return p.getArea(fa(p, idx))

def check(label, got, exp, tol):
    ok = abs(got - exp) <= tol
    print('%-28s %10.2f   expected %10.2f   %s' % (label, got, exp, 'OK' if ok else '<<< MISMATCH'))
    if not ok:
        stop(label)

def check_n(label, got, exp):
    print('%-28s %10d   expected %10d   %s' % (label, got, exp, 'OK' if got == exp else '<<< MISMATCH'))
    if got != exp:
        stop(label)

# ---------- helpers for face selection ----------
def fixed_ext(p, tag):
    """indices of external faces (one cell) that bound a fixed cell"""
    fc = set([c.index for c in p.sets['FIXED_' + tag].cells])
    out = []
    for f in p.faces:
        cl = f.getCells()
        if len(cl) == 1 and cl[0] in fc:
            out.append(f.index)
    return out

def in_box(p, x0, y0, z0, x1, y1, z1):
    return set([f.index for f in p.faces.getByBoundingBox(x0, y0, z0, x1, y1, z1)])

def straddle(p, box, axis, val):
    """faces fully inside box that cross the plane axis = val"""
    x0, y0, z0, x1, y1, z1 = box
    inside = in_box(p, *box)
    lo = list(box); hi = list(box)
    lo[3 + axis] = val + 1e-3            # fully on the low side
    hi[axis] = val - 1e-3                # fully on the high side
    return sorted(inside - in_box(p, *lo) - in_box(p, *hi))

def zface(p, idx, z, nz):
    out = []
    for i in idx:
        f = p.faces[i]
        pt = f.pointOn[0]; nr = f.getNormal()
        if abs(pt[2] - z) < 1e-4 and abs(abs(nr[2]) - 1.0) < 1e-6:
            out.append(i)
    return out

def diag_face(p, idx, sx, sy, toff, smin):
    """planar faces normal to the corner's (-sy, sx) direction at |t| = toff, s > smin; returns {'L': [...], 'R': [...]}"""
    res = {'L': [], 'R': []}
    for i in idx:
        f = p.faces[i]
        x, y, z = f.pointOn[0]; nr = f.getNormal()
        s = (sx * x + sy * y) * R2
        t = (-sy * x + sx * y) * R2
        nt = (-sy * nr[0] + sx * nr[1]) * R2
        if s > smin and abs(abs(t) - toff) < 1e-3 and abs(abs(nt) - 1.0) < 1e-5:
            res['L' if t > 0 else 'R'].append(i)
    return res


# ---------- 1. remove constraints, LC3a_P, instances, BODY and three arm parts ----------
for n in [k for k in m.constraints.keys() if k.startswith('CP_') or k.startswith('TIE_')]:
    del m.constraints[n]
if 'LC3a_P' in m.loads.keys():
    del m.loads['LC3a_P']
for n in list(a.instances.keys()):
    del a.instances[n]
for n in ('BODY', 'ARM_pm', 'ARM_mp', 'ARM_mm'):
    if n in m.parts.keys():
        del m.parts[n]
if 'ARM_pp' in m.parts.keys():
    m.parts.changeKey(fromName='ARM_pp', toName='ARM')
pa = m.parts['ARM']
for old, new in (('S_PRONG_BOSS_pp_L', 'S_PRONG_BOSS_L'), ('S_PRONG_BOSS_pp_R', 'S_PRONG_BOSS_R'),
                 ('S_JNT_pp', 'S_JNT'), ('S_MOT_SEAT_pp', 'S_MOT_SEAT')):
    if old in pa.surfaces.keys():
        pa.surfaces.changeKey(fromName=old, toName=new)
print('arm part ARM, surfaces: %s' % sorted(pa.surfaces.keys()))
print('--- ARM checks ---')
check_n('ARM cells', len(pa.cells), 6)
check('ARM fixed volume', pa.getVolume(cells=pa.sets['FIXED_ARM'].cells), 2933.5, 1.0)
check('ARM design volume', pa.getVolume(cells=pa.sets['DESIGN_ARM'].cells), 8036.9, 1.0)
for nm, idx_exp, aexp in (('S_PRONG_BOSS_L', 2, 134.58), ('S_PRONG_BOSS_R', 2, 134.58),
                          ('S_JNT', 4, 431.31), ('S_MOT_SEAT', 1, 214.15)):
    fs = pa.surfaces[nm].faces
    check_n(nm + ' faces', len(fs), idx_exp)
    check(nm + ' area', pa.getArea(fs), aexp, 0.5)

# ---------- 2. import BODY, section, orientation, cell sets ----------
g = mdb.openStep(STEP_DIR + '\\BODY.step', scaleFromFile=OFF)
m.PartFromGeometryFile(name='BODY', geometryFile=g, combine=True, retainBoundary=True,
                       mergeSolidRegions=True, dimensionality=THREE_D, type=DEFORMABLE_BODY)
p = m.parts['BODY']
allset = p.Set(name='ALL_BODY', cells=p.cells)
p.SectionAssignment(region=allset, sectionName='SEC_PETCF', offset=0.0,
                    offsetType=MIDDLE_SURFACE, offsetField='', thicknessAssignment=FROM_SECTION)
p.MaterialOrientation(region=allset, orientationType=GLOBAL, axis=AXIS_3,
                      additionalRotationType=ROTATION_NONE, localCsys=None, fieldName='',
                      stackDirection=STACK_3)
FIXED_VOLS = (3050.0, 1094.4, 198.2)
des, fix = [], []
for c in p.cells:
    v = p.getVolume(cells=p.cells[c.index:c.index + 1])
    if min([abs(v - fv) for fv in FIXED_VOLS]) < 0.5:
        fix.append(c.index)
    else:
        des.append(c.index)
cf = p.cells[fix[0]:fix[0] + 1]
for i in fix[1:]:
    cf = cf + p.cells[i:i + 1]
cd = p.cells[des[0]:des[0] + 1]
for i in des[1:]:
    cd = cd + p.cells[i:i + 1]
p.Set(name='FIXED_BODY', cells=cf)
p.Set(name='DESIGN_BODY', cells=cd)
print('--- BODY ---')
check_n('BODY fixed cells', len(fix), 13)
check('BODY fixed volume', p.getVolume(cells=cf), 12597.9, 1.0)
check_n('BODY design cells', len(des), 1)
check('BODY design volume', p.getVolume(cells=cd), 42206.2, 1.0)

# ---------- 3-4. BODY partitions and surfaces ----------
p = m.parts['BODY']
print('--- BODY surfaces ---')
for axis, val in ((0, 20.0), (0, -20.0), (1, 20.0), (1, -20.0)):
    d = p.DatumPlaneByPrincipalPlane(principalPlane=(YZPLANE if axis == 0 else XZPLANE), offset=val)
    st = straddle(p, (-23.0, -23.0, -15.01, 23.0, 23.0, -14.99), axis, val)
    if len(st) != 1:
        stop('floor partition %s=%g: %d faces cross the plane, expected 1' % ('xy'[axis], val, len(st)))
    p.PartitionFaceByDatumPlane(datumPlane=p.datums[d.id], faces=fa(p, st))
d = p.DatumPlaneByPrincipalPlane(principalPlane=YZPLANE, offset=-32.0)
st = straddle(p, (-60.0, -30.0, 23.99, 40.0, 30.0, 24.01), 0, -32.0)
if len(st) != 1:
    stop('top partition x=-32: %d faces cross the plane, expected 1' % len(st))
p.PartitionFaceByDatumPlane(datumPlane=p.datums[d.id], faces=fa(p, st))

fx = fixed_ext(p, 'BODY')
top = zface(p, fx, 24.0, 1)
batt = [i for i in top if p.faces[i].pointOn[0][0] > -32.0]
gps = [i for i in top if p.faces[i].pointOn[0][0] < -32.0]
fcs = zface(p, fx, -6.0, 1)
floor = [i for i in in_box(p, -20.01, -20.01, -15.01, 20.01, 20.01, -14.99)]
floor = zface(p, floor, -15.0, -1)
for nm, idx, nexp, aexp in (('S_BATT_SEAT', batt, 1, 1056.0), ('S_GPS_SEAT', gps, 1, 164.0),
                            ('S_FC_SEAT', fcs, 4, 80.92), ('S_FLOOR', floor, 5, 1600.0)):
    check_n(nm + ' faces', len(idx), nexp)
    check(nm + ' area', area(p, idx), aexp, 0.5)
    p.Surface(name=nm, side1Faces=fa(p, idx))
for c, (sx, sy) in sorted(CORNERS.items()):
    r = diag_face(p, fx, sx, sy, 5.0, 10.0)
    for side in ('L', 'R'):
        nm = 'S_FIN_BOSS_%s_%s' % (c, side)
        check_n(nm + ' faces', len(r[side]), 2)
        check(nm + ' area', area(p, r[side]), 138.50, 0.5)
        p.Surface(name=nm, side1Faces=fa(p, r[side]))


# ---------- 5. instances: BODY and four rotated arms ----------
a.Instance(name='BODY-1', part=m.parts['BODY'], dependent=ON)
for c in ('pp', 'pm', 'mp', 'mm'):
    n = 'ARM_%s-1' % c
    a.Instance(name=n, part=pa, dependent=ON)
    if ROT[c] != 0.0:
        a.rotate(instanceList=(n,), axisPoint=(0.0, 0.0, 0.0), axisDirection=(0.0, 0.0, 1.0), angle=ROT[c])
a.regenerate()

# ---------- 6. position checks: prong faces at |t| = 5.15 on the right side, fin faces at |t| = 5 ----------
print('--- arm positions (t across the arm, s along it; gap = |t_prong| - |t_fin|) ---')
B = a.instances['BODY-1']
for c, (sx, sy) in sorted(CORNERS.items()):
    I = a.instances['ARM_%s-1' % c]
    for side, sgn in (('L', 1.0), ('R', -1.0)):
        ts = []
        for f in I.surfaces['S_PRONG_BOSS_' + side].faces:
            x, y, z = f.pointOn[0]
            ts.append(((-sy * x + sx * y) * R2, (sx * x + sy * y) * R2))
        tf = []
        for f in B.surfaces['S_FIN_BOSS_%s_%s' % (c, side)].faces:
            x, y, z = f.pointOn[0]
            tf.append((-sy * x + sx * y) * R2)
        ok = all(abs(t - sgn * 5.15) < 1e-3 and s > 10 for t, s in ts) and all(abs(t - sgn * 5.0) < 1e-3 for t in tf)
        print('ARM_%s %s: prong t %s, fin t %s, gap %.3f mm  %s' % (c, side,
              ['%.3f' % t for t, s in ts], ['%.3f' % t for t in tf],
              abs(ts[0][0]) - abs(tf[0]), 'OK' if ok else '<<< MISMATCH'))
        if not ok:
            stop('arm %s side %s not in place' % (c, side))
    x, y, z = I.surfaces['S_MOT_SEAT'].faces[0].pointOn[0]
    ok = sx * x > 39 and sy * y > 39 and abs(z) < 1e-4
    print('ARM_%s motor seat point (%.1f, %.1f, %.1f)  %s' % (c, x, y, z, 'OK' if ok else '<<< MISMATCH'))
    if not ok:
        stop('motor seat of %s not in its corner' % c)

# ---------- 7. assembly sets for Tosca ----------
a.SetByBoolean(name='DESIGN_ALL', operation=UNION,
               sets=[B.sets['DESIGN_BODY']] + [a.instances['ARM_%s-1' % c].sets['DESIGN_ARM'] for c in ('pp', 'pm', 'mp', 'mm')])
a.SetByBoolean(name='FIXED_ALL', operation=UNION,
               sets=[B.sets['FIXED_BODY']] + [a.instances['ARM_%s-1' % c].sets['FIXED_ARM'] for c in ('pp', 'pm', 'mp', 'mm')])
print('assembly sets DESIGN_ALL (%d cells), FIXED_ALL (%d cells)' % (len(a.sets['DESIGN_ALL'].cells), len(a.sets['FIXED_ALL'].cells)))
check_n('DESIGN_ALL cells', len(a.sets['DESIGN_ALL'].cells), 5)
check_n('FIXED_ALL cells', len(a.sets['FIXED_ALL'].cells), 33)
print('=== R7 done: all checks OK. Save the model, then run R8_connect.py. ===')
