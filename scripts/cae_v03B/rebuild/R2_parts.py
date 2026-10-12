# R2 - replaces the five parts with the D-054/D-055 export and rebuilds everything that lives on the parts:
# section, orientation, cell sets, face partitions, surfaces, instances. Checks every result and stops on a mismatch.
# Run in revB_v03B_D055.cae (NOT the original file). Set STEP_DIR first.
from __future__ import print_function
from abaqus import *
from abaqusConstants import *
import regionToolset, math

STEP_DIR = r'C:\path\to\abaqus_v03B'      # <-- folder with BODY.step and ARM_xx.step (new zip)
MODEL = 'revB_v03B'
m = mdb.models[MODEL]
a = m.rootAssembly
CORNERS = {'pp': (1, 1), 'pm': (1, -1), 'mp': (-1, 1), 'mm': (-1, -1)}
R2 = 1.0 / math.sqrt(2.0)

def stop(msg):
    raise Exception('R2 STOPPED: ' + msg)

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

# ---------- 1. remove what references the old parts ----------
for n in [k for k in m.constraints.keys() if k.startswith('CP_') or k.startswith('TIE_')]:
    del m.constraints[n]
if 'LC3a_P' in m.loads.keys():
    del m.loads['LC3a_P']
names = ['BODY', 'ARM_pp', 'ARM_pm', 'ARM_mp', 'ARM_mm']
for n in names:
    if n + '-1' in a.instances.keys():
        del a.instances[n + '-1']
for n in names:
    if n in m.parts.keys():
        del m.parts[n]
print('old couplings, ties, LC3a_P, instances and parts deleted')

# ---------- 2. import, section, orientation, cell sets ----------
FIX_EXP = {'BODY': (13, 12597.9, 2, 33353.9), 'ARM': (5, 2933.5, 1, 8036.9)}
DESIGN_VOLS = {'BODY': (32863.9, 490.0), 'ARM': (8036.9,)}
for n in names:
    g = mdb.openStep(STEP_DIR + '\\' + n + '.step', scaleFromFile=OFF)
    m.PartFromGeometryFile(name=n, geometryFile=g, combine=True, retainBoundary=True,
                           mergeSolidRegions=True, dimensionality=THREE_D, type=DEFORMABLE_BODY)
    p = m.parts[n]
    kind = 'BODY' if n == 'BODY' else 'ARM'
    tag = 'BODY' if kind == 'BODY' else 'ARM'
    allset = p.Set(name='ALL_' + tag, cells=p.cells)
    p.SectionAssignment(region=allset, sectionName='SEC_PETCF', offset=0.0,
                        offsetType=MIDDLE_SURFACE, offsetField='', thicknessAssignment=FROM_SECTION)
    p.MaterialOrientation(region=allset, orientationType=GLOBAL, axis=AXIS_3,
                          additionalRotationType=ROTATION_NONE, localCsys=None, fieldName='',
                          stackDirection=STACK_3)
    des, fix = [], []
    for c in p.cells:
        v = p.getVolume(cells=p.cells[c.index:c.index + 1])
        if min([abs(v - dv) for dv in DESIGN_VOLS[kind]]) < 1.0:
            des.append(c.index)
        else:
            fix.append(c.index)
    cf = p.cells[fix[0]:fix[0] + 1]
    for i in fix[1:]:
        cf = cf + p.cells[i:i + 1]
    cd = p.cells[des[0]:des[0] + 1]
    for i in des[1:]:
        cd = cd + p.cells[i:i + 1]
    p.Set(name='FIXED_' + tag, cells=cf)
    p.Set(name='DESIGN_' + tag, cells=cd)
    ne = FIX_EXP[kind]
    print('--- %s ---' % n)
    check_n(n + ' fixed cells', len(fix), ne[0])
    check(n + ' fixed volume', p.getVolume(cells=cf), ne[1], 1.0)
    check_n(n + ' design cells', len(des), ne[2])
    check(n + ' design volume', p.getVolume(cells=cd), ne[3], 1.0)

# ---------- 3. helpers for face selection ----------
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

# ---------- 4. BODY partitions and surfaces ----------
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

# ---------- 5. ARM surfaces ----------
for c, (sx, sy) in sorted(CORNERS.items()):
    p = m.parts['ARM_' + c]
    print('--- ARM_%s surfaces ---' % c)
    fx = fixed_ext(p, 'ARM')
    r = diag_face(p, fx, sx, sy, 5.15, 10.0)
    for side in ('L', 'R'):
        nm = 'S_PRONG_BOSS_%s_%s' % (c, side)
        check_n(nm + ' faces', len(r[side]), 2)
        check(nm + ' area', area(p, r[side]), 134.58, 0.5)
        p.Surface(name=nm, side1Faces=fa(p, r[side]))
    r = diag_face(p, fx, sx, sy, 10.15, 10.0)
    j = r['L'] + r['R']
    check_n('S_JNT_%s faces' % c, len(j), 4)
    check('S_JNT_%s area' % c, area(p, j), 431.31, 0.5)
    p.Surface(name='S_JNT_' + c, side1Faces=fa(p, j))
    mot = zface(p, fx, 0.0, 1)
    mot = [i for i in mot if p.faces[i].getNormal()[2] > 0]
    check_n('S_MOT_SEAT_%s faces' % c, len(mot), 1)
    check('S_MOT_SEAT_%s area' % c, area(p, mot), 214.15, 0.5)
    p.Surface(name='S_MOT_SEAT_' + c, side1Faces=fa(p, mot))

# ---------- 6. instances (dependent, no offset) ----------
for n in names:
    a.Instance(name=n + '-1', part=m.parts[n], dependent=ON)
a.regenerate()
print('instances: %s' % sorted(a.instances.keys()))
print('=== R2 done: all checks OK. Save the model (Ctrl+S). ===')
