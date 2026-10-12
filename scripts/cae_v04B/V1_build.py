# V1 - v04-B revision 2 model (export note claude/stage6_v04B_export_note.md, brief section 10).
# Builds model 'revB_v04B' as a copy of 'revB_v03B' (keeps material, section, steps, inertia relief,
# outputs, RP loads, point masses, the arm part ARM and the Tosca task), then:
#   - imports TUB.step and LID.step (combine, merge, retain boundaries), sets, partitions, surfaces;
#   - instances TUB-1, LID-1 and the arm part at the moved corners (rotation, then (3 sx, 3 sy, 0));
#   - moves RP_MOT, RP_JNT, RP_GPS to the revision 2 positions, GPS mass 2.6 g;
#   - recreates couplings, joint ties, lid ties (G7a: 5 bosses), supports (D-064) and LC3a.
# Every count, area and position is checked against values computed from the STEP files; any
# mismatch stops the script. Run in revB_v04B.cae (File > Save As of revB_v03B_D056.cae), with
# File > Run Script. Set STEP_DIR first. ASCII only.
from __future__ import print_function
from abaqus import *
from abaqusConstants import *
import math

import os
STEP_DIR = None
for _d in ([os.path.dirname(os.path.abspath(__file__))] if '__file__' in globals() else []) + [os.getcwd()]:
    if os.path.exists(os.path.join(_d, 'v04B_paths.txt')):
        STEP_DIR = open(os.path.join(_d, 'v04B_paths.txt')).read().strip()
        break
if not STEP_DIR:
    STEP_DIR = r'C:\path\to\stage6_abaqus_v04B'      # <-- or put the folder in v04B_paths.txt next to this script
print('STEP_DIR = %s' % STEP_DIR)
SRC, MODEL = 'revB_v03B', 'revB_v04B'
CORNERS = {'pp': (1, 1), 'pm': (1, -1), 'mp': (-1, 1), 'mm': (-1, -1)}
ROT = {'pp': 0.0, 'pm': -90.0, 'mp': 90.0, 'mm': 180.0}
SHIFT = 3.0
R2 = 1.0 / math.sqrt(2.0)
LIDBOSS = [(21.0, 9.5), (21.0, -9.5), (-21.0, 5.0), (-21.0, -5.0), (-30.0, 0.0)]
NEW_RP = {'MOT_pp': (52.5, 52.5, 8.5), 'MOT_pm': (52.5, -52.5, 8.5),
          'MOT_mp': (-52.5, 52.5, 8.5), 'MOT_mm': (-52.5, -52.5, 8.5),
          'JNT_pp': (26.335, 26.335, -2.5), 'JNT_pm': (26.335, -26.335, -2.5),
          'JNT_mp': (-26.335, 26.335, -2.5), 'JNT_mm': (-26.335, -26.335, -2.5),
          'GPS': (-44.0, 0.0, 26.5)}
GPS_MASS = 2.6e-6
GROUPS = {'SET_MOT_ALL': ('pp', 'pm', 'mp', 'mm'), 'SET_MOT_DIAG_A': ('pp', 'mm'),
          'SET_MOT_DIAG_B': ('pm', 'mp'), 'SET_MOT_FRONT': ('pp', 'pm')}


def stop(msg):
    raise Exception('V1 STOPPED: ' + msg)


def check(label, got, exp, tol):
    ok = abs(got - exp) <= tol
    print('%-34s %10.2f   expected %10.2f   %s' % (label, got, exp, 'OK' if ok else '<<< MISMATCH'))
    if not ok:
        stop(label)


def check_n(label, got, exp):
    print('%-34s %10d   expected %10d   %s' % (label, got, exp, 'OK' if got == exp else '<<< MISMATCH'))
    if got != exp:
        stop(label)


def fa(p, idx):
    idx = sorted(set(idx))
    s = p.faces[idx[0]:idx[0] + 1]
    for i in idx[1:]:
        s = s + p.faces[i:i + 1]
    return s


def ca(p, idx):
    idx = sorted(set(idx))
    s = p.cells[idx[0]:idx[0] + 1]
    for i in idx[1:]:
        s = s + p.cells[i:i + 1]
    return s


def area(p, idx):
    return p.getArea(fa(p, idx))


def zfaces(p, z, nz, cells=None):
    """planar faces at height z with normal nz (+1 / -1); optionally only faces bounding the given cells"""
    out = []
    for f in p.faces:
        pt = f.pointOn[0]
        if abs(pt[2] - z) > 1e-4:
            continue
        try:
            nr = f.getNormal()
        except Exception:
            continue
        if abs(nr[2] - nz) > 1e-6:
            continue
        if cells is not None and not (set(f.getCells()) & cells):
            continue
        out.append(f.index)
    return out


def bbox_of(p, i):
    return p.faces[i].getBoundingBox() if hasattr(p.faces[i], 'getBoundingBox') else None


def crosses(p, i, axis, val):
    vs = [p.vertices[v].pointOn[0][axis] for v in p.faces[i].getVertices()]
    if not vs:
        return False
    return min(vs) < val - 1e-3 and max(vs) > val + 1e-3


def partition_plane(p, idx, axis, val):
    """partition the faces in idx that cross the plane (axis = val); returns the number cut"""
    cut = [i for i in idx if crosses(p, i, axis, val)]
    if cut:
        d = p.DatumPlaneByPrincipalPlane(principalPlane=(YZPLANE if axis == 0 else XZPLANE), offset=val)
        p.PartitionFaceByDatumPlane(datumPlane=p.datums[d.id], faces=fa(p, cut))
    return len(cut)


def cells_by_volume(p, table):
    """table: {volume: expected count}; returns (fixed list, design list, report)"""
    groups = {}
    for c in p.cells:
        v = p.getVolume(cells=p.cells[c.index:c.index + 1])
        groups.setdefault(round(v, 1), []).append(c.index)
    return groups


def diag_face(p, idx, sx, sy, toff, smin):
    res = {'L': [], 'R': []}
    for i in idx:
        f = p.faces[i]
        x, y, z = f.pointOn[0]
        try:
            nr = f.getNormal()
        except Exception:
            continue
        s = (sx * x + sy * y) * R2
        t = (-sy * x + sx * y) * R2
        nt = (-sy * nr[0] + sx * nr[1]) * R2
        if s > smin and abs(abs(t) - toff) < 1e-3 and abs(abs(nt) - 1.0) < 1e-5:
            res['L' if t > 0 else 'R'].append(i)
    return res


def fixed_ext(p, fixed_cells):
    out = []
    for f in p.faces:
        cl = f.getCells()
        if len(cl) == 1 and cl[0] in fixed_cells:
            out.append(f.index)
    return out


def import_part(name, fn):
    g = mdb.openStep(STEP_DIR + '\\' + fn, scaleFromFile=OFF)
    m.PartFromGeometryFile(name=name, geometryFile=g, combine=True, retainBoundary=True,
                           mergeSolidRegions=True, dimensionality=THREE_D, type=DEFORMABLE_BODY)
    p = m.parts[name]
    allset = p.Set(name='ALL_' + name, cells=p.cells)
    p.SectionAssignment(region=allset, sectionName='SEC_PETCF', offset=0.0, offsetType=MIDDLE_SURFACE,
                        offsetField='', thicknessAssignment=FROM_SECTION)
    p.MaterialOrientation(region=allset, orientationType=GLOBAL, axis=AXIS_3,
                          additionalRotationType=ROTATION_NONE, localCsys=None, fieldName='',
                          stackDirection=STACK_3)
    return p


# ---------- 0. model copy ----------
if not mdb.pathName.lower().endswith('revb_v04b.cae'):
    stop('open revB_v03B_D056.cae, File > Save As revB_v04B.cae, then run V1 (current: %s)' % mdb.pathName)
if MODEL in mdb.models.keys():
    del mdb.models[MODEL]
    print('old model %s from a previous run deleted' % MODEL)
mdb.Model(name=MODEL, objectToCopy=mdb.models[SRC])
m = mdb.models[MODEL]
a = m.rootAssembly
print('model %s copied from %s' % (MODEL, SRC))

# ---------- 1. remove old connections, supports, LC3a pressure, instances, BODY ----------
for n in [k for k in m.constraints.keys() if k.startswith('CP_') or k.startswith('TIE_')]:
    del m.constraints[n]
for n in [k for k in m.boundaryConditions.keys() if k.startswith('BC_')]:
    del m.boundaryConditions[n]
if 'LC3a_P' in m.loads.keys():
    del m.loads['LC3a_P']
for n in list(a.instances.keys()):
    del a.instances[n]
if 'BODY' in m.parts.keys():
    del m.parts['BODY']
pa = m.parts['ARM']
print('--- ARM part (unchanged v03-B) ---')
check_n('ARM cells', len(pa.cells), 6)
check('ARM fixed volume', pa.getVolume(cells=pa.sets['FIXED_ARM'].cells), 2933.5, 1.0)
check('ARM design volume', pa.getVolume(cells=pa.sets['DESIGN_ARM'].cells), 8036.9, 1.0)

# ---------- 2. TUB ----------
pt = import_part('TUB', 'TUB.step')
g = cells_by_volume(pt, None)
print('TUB cell volumes: %s' % ', '.join('%.1f x %d' % (v, len(g[v])) for v in sorted(g)))
TUB_FIX = {133.5: 5, 240.2: 4, 112.7: 1, 1094.4: 8}
fix_t, des_t = [], []
for v, ids in g.items():
    if v in TUB_FIX:
        check_n('TUB cells of %.1f mm3' % v, len(ids), TUB_FIX[v])
        fix_t += ids
    else:
        des_t += ids
pt.Set(name='FIXED_TUB', cells=ca(pt, fix_t))
pt.Set(name='DESIGN_TUB', cells=ca(pt, des_t))
check_n('TUB fixed cells', len(fix_t), 18)
check_n('TUB design cells', len(des_t), 1)
check('TUB fixed volume', pt.getVolume(cells=ca(pt, fix_t)), 10496.1, 1.0)
check('TUB design volume', pt.getVolume(cells=ca(pt, des_t)), 40676.1, 1.0)
fixset_t = set(fix_t)
desset_t = set(des_t)

# floor: partition the design floor face at x, y = +-23, then the 46 x 46 square (incl. FC boss rings)
for axis in (0, 1):
    for val in (23.0, -23.0):
        n = partition_plane(pt, zfaces(pt, -15.0, -1.0, desset_t), axis, val)
        print('floor partition %s = %+.0f: %d face(s) cut' % ('xy'[axis], val, n))
# rim: partition the tub top faces at y = +-17 (lid footprint, G7b)
for val in (17.0, -17.0):
    n = partition_plane(pt, zfaces(pt, 21.5, 1.0), 1, val)
    print('rim partition y = %+.0f: %d face(s) cut' % (val, n))

allfl = zfaces(pt, -15.0, -1.0)
print('floor faces at z = -15 after the cuts:')
for i in allfl:
    b = pt.faces[i:i + 1].getBoundingBox()
    print('  face %4d  area %8.2f  x %.2f..%.2f  y %.2f..%.2f  cells %s' % (
        i, area(pt, [i]), b['low'][0], b['high'][0], b['low'][1], b['high'][1], pt.faces[i].getCells()))
floor = [f.index for f in pt.faces.getByBoundingBox(-23.01, -23.01, -15.01, 23.01, 23.01, -14.99) if f.index in allfl]
fx = fixed_ext(pt, fixset_t)
fcs = [i for i in zfaces(pt, -6.0, 1.0) if i in fx]
print('--- TUB surfaces ---')
for nm, idx, nexp, aexp in (('S_FLOOR', floor, 5, 2060.58), ('S_FC_SEAT', fcs, 4, 113.47)):
    check_n(nm + ' faces', len(idx), nexp)
    check(nm + ' area', area(pt, idx), aexp, 0.5)
    pt.Surface(name=nm, side1Faces=fa(pt, idx))
for c, (sx, sy) in sorted(CORNERS.items()):
    r = diag_face(pt, fx, sx, sy, 5.0, 10.0)
    for side in ('L', 'R'):
        nm = 'S_FIN_BOSS_%s_%s' % (c, side)
        check_n(nm + ' faces', len(r[side]), 2)
        check(nm + ' area', area(pt, r[side]), 138.50, 0.5)
        pt.Surface(name=nm, side1Faces=fa(pt, r[side]))
top_t = zfaces(pt, 21.5, 1.0)
for k, (bx, by) in enumerate(LIDBOSS):
    idx = [i for i in top_t if i in fx and math.hypot(pt.faces[i].pointOn[0][0] - bx, pt.faces[i].pointOn[0][1] - by) < 3.01]
    nm = 'S_TUB_BOSS_%d' % (k + 1)
    check_n(nm + ' faces', len(idx), 1)
    check(nm + ' area (dia 6 / 3.2)', area(pt, idx), 20.23, 0.2)
    pt.Surface(name=nm, side1Faces=fa(pt, idx))
rim = [i for i in top_t if abs(pt.faces[i].pointOn[0][1]) < 17.0]
check_n('S_RIM_UNDER_LID faces', len(rim), 9)
check('S_RIM_UNDER_LID area', area(pt, rim), 625.98, 0.5)
pt.Surface(name='S_RIM_UNDER_LID', side1Faces=fa(pt, rim))

# ---------- 3. LID ----------
pl = import_part('LID', 'LID.step')
g = cells_by_volume(pl, None)
print('LID cell volumes: %s' % ', '.join('%.1f x %d' % (v, len(g[v])) for v in sorted(g)))
fix_l, des_l, pads = [], [], []
for v, ids in g.items():
    if v in (4365.4, 58.4):
        fix_l += ids
        if v == 58.4:
            pads += ids
    else:
        des_l += ids
pl.Set(name='FIXED_LID', cells=ca(pl, fix_l))
pl.Set(name='DESIGN_LID', cells=ca(pl, des_l))
check_n('LID fixed cells', len(fix_l), 5)
check_n('LID screw pad cells', len(pads), 4)
check_n('LID design cells', len(des_l), 2)
check('LID fixed volume', pl.getVolume(cells=ca(pl, fix_l)), 4599.1, 1.0)
check('LID design volume', pl.getVolume(cells=ca(pl, des_l)), 2496.6, 1.0)
fixset_l = set(fix_l)
padset = set(pads)
for val in (32.0, -32.0):
    n = partition_plane(pl, zfaces(pl, 24.0, 1.0, fixset_l - padset), 0, val)
    print('lid top partition x = %+.0f: %d face(s) cut' % (val, n))
fxl = fixed_ext(pl, fixset_l)
top_l = [i for i in zfaces(pl, 24.0, 1.0) if i in fxl]
batt = [i for i in top_l if abs(pl.faces[i].pointOn[0][0]) < 32.0 and not (set(pl.faces[i].getCells()) & padset)]
gps = [i for i in top_l if -52.81 < pl.faces[i].pointOn[0][0] < -35.19 and abs(pl.faces[i].pointOn[0][1]) < 6.31]
bot_l = zfaces(pl, 21.5, -1.0)
print('--- LID surfaces ---')
for nm, idx, nexp, aexp in (('S_BATT_SEAT', batt, 1, 1052.91), ('S_GPS_SEAT', gps, 1, 209.19),
                            ('S_LID_BOTTOM', bot_l, 7, 2740.84)):
    check_n(nm + ' faces', len(idx), nexp)
    check(nm + ' area', area(pl, idx), aexp, 0.5)
    pl.Surface(name=nm, side1Faces=fa(pl, idx))
big = [i for i in bot_l if i in fxl and area(pl, [i]) > 1000.0]
check_n('LID fixed bottom face', len(big), 1)
for k, (bx, by) in enumerate(LIDBOSS):
    if k < 4:
        idx = [i for i in bot_l if (set(pl.faces[i].getCells()) & padset)
               and math.hypot(pl.faces[i].pointOn[0][0] - bx, pl.faces[i].pointOn[0][1] - by) < 3.01]
        check_n('S_LID_PAD_%d faces' % (k + 1), len(idx), 1)
        check('S_LID_PAD_%d area (dia 6 / 2.2)' % (k + 1), area(pl, idx), 24.47, 0.2)
    else:
        idx = big     # keel pad: part of the fixed bottom face (DV-22)
    pl.Surface(name='S_LID_PAD_%d' % (k + 1), side1Faces=fa(pl, idx))

# ---------- 4. instances ----------
a.Instance(name='TUB-1', part=pt, dependent=ON)
a.Instance(name='LID-1', part=pl, dependent=ON)
for c, (sx, sy) in sorted(CORNERS.items()):
    n = 'ARM_%s-1' % c
    a.Instance(name=n, part=pa, dependent=ON)
    if ROT[c] != 0.0:
        a.rotate(instanceList=(n,), axisPoint=(0.0, 0.0, 0.0), axisDirection=(0.0, 0.0, 1.0), angle=ROT[c])
    a.translate(instanceList=(n,), vector=(SHIFT * sx, SHIFT * sy, 0.0))
a.regenerate()
print('--- arm positions (t across the arm; gap = |t_prong| - |t_fin|) ---')
B = a.instances['TUB-1']
for c, (sx, sy) in sorted(CORNERS.items()):
    I = a.instances['ARM_%s-1' % c]
    for side, sgn in (('L', 1.0), ('R', -1.0)):
        ts = [((-sy * f.pointOn[0][0] + sx * f.pointOn[0][1]) * R2, (sx * f.pointOn[0][0] + sy * f.pointOn[0][1]) * R2)
              for f in I.surfaces['S_PRONG_BOSS_' + side].faces]
        tf = [(-sy * f.pointOn[0][0] + sx * f.pointOn[0][1]) * R2 for f in B.surfaces['S_FIN_BOSS_%s_%s' % (c, side)].faces]
        ok = all(abs(t - sgn * 5.15) < 1e-3 and s > 14 for t, s in ts) and all(abs(t - sgn * 5.0) < 1e-3 for t in tf)
        print('ARM_%s %s: prong t %s, fin t %s, gap %.3f mm  %s' % (c, side, ['%.3f' % t for t, s in ts],
              ['%.3f' % t for t in tf], abs(ts[0][0]) - abs(tf[0]), 'OK' if ok else '<<< MISMATCH'))
        if not ok:
            stop('arm %s side %s not in place' % (c, side))
    x, y, z = I.surfaces['S_MOT_SEAT'].faces[0].pointOn[0]
    ok = sx * x > 42 and sy * y > 42 and abs(z) < 1e-4
    print('ARM_%s motor seat point (%.1f, %.1f, %.1f)  %s' % (c, x, y, z, 'OK' if ok else '<<< MISMATCH'))
    if not ok:
        stop('motor seat of %s not in its corner' % c)

# ---------- 5. assembly sets for Tosca ----------
arms = [a.instances['ARM_%s-1' % c] for c in ('pp', 'pm', 'mp', 'mm')]
L = a.instances['LID-1']
a.SetByBoolean(name='DESIGN_ARMS', operation=UNION, sets=[i.sets['DESIGN_ARM'] for i in arms])
a.SetByBoolean(name='DESIGN_ALL', operation=UNION,
               sets=[B.sets['DESIGN_TUB'], L.sets['DESIGN_LID']] + [i.sets['DESIGN_ARM'] for i in arms])
a.SetByBoolean(name='FIXED_ALL', operation=UNION,
               sets=[B.sets['FIXED_TUB'], L.sets['FIXED_LID']] + [i.sets['FIXED_ARM'] for i in arms])
check_n('DESIGN_ALL cells', len(a.sets['DESIGN_ALL'].cells), 7)
check_n('FIXED_ALL cells', len(a.sets['FIXED_ALL'].cells), 43)
check_n('DESIGN_ARMS cells', len(a.sets['DESIGN_ARMS'].cells), 4)

# ---------- 6. reference points ----------
print('--- reference points ---')
for key in sorted(NEW_RP.keys()):
    xyz = NEW_RP[key]
    sname, fname = 'SET_RP_' + key, 'RP_' + key
    if sname not in a.sets.keys():
        stop('set %s not found' % sname)
    f = a.ReferencePoint(point=xyz)
    a.Set(name=sname, referencePoints=(a.referencePoints[f.id],))
    if fname in a.features.keys():
        a.deleteFeatures((fname,))
    else:
        print('old feature %s not found (old RP left in place, unused)' % fname)
    a.features.changeKey(fromName=f.name, toName=fname)
rpobj = lambda key: a.sets['SET_RP_' + key].referencePoints[0]
for gname, cs in GROUPS.items():
    a.Set(name=gname, referencePoints=tuple(rpobj('MOT_' + c) for c in cs))
for key in sorted(NEW_RP.keys()) + ['BATT', 'FC']:
    xyz = a.getCoordinates(rpobj(key))
    exp = NEW_RP.get(key, {'BATT': (0.0, 0.0, 40.0), 'FC': (0.0, 0.0, 0.0)}.get(key))
    ok = max(abs(xyz[i] - exp[i]) for i in range(3)) < 1e-4
    print('RP_%-7s (%9.3f, %9.3f, %7.3f)  %s' % (key, xyz[0], xyz[1], xyz[2], 'OK' if ok else '<<< MISMATCH'))
    if not ok:
        stop('RP_' + key)
changed = set(['SET_RP_' + k for k in NEW_RP] + list(GROUPS.keys()))


def region_name(obj):
    try:
        r = obj.region
    except Exception:
        return None
    if isinstance(r, (tuple, list)) and r:
        return r[0] if isinstance(r[0], str) else None
    return getattr(r, 'name', None)


nl = 0
for k, ld in m.loads.items():
    rn = region_name(ld)
    if rn in changed:
        ld.setValues(region=a.sets[rn])
        nl += 1
ni = 0
inert = a.engineeringFeatures.inertias
for k in inert.keys():
    rn = region_name(inert[k])
    if rn in changed:
        inert[k].setValues(region=a.sets[rn])
        ni += 1
    if rn == 'SET_RP_GPS':
        inert[k].setValues(mass=GPS_MASS)
        print('point mass %s on SET_RP_GPS set to %.2e t' % (k, GPS_MASS))
print('loads re-linked: %d (expected 8), point masses re-linked: %d (expected 9)' % (nl, ni))
for k in sorted(inert.keys()):
    print('  point mass %-10s on %s' % (k, region_name(inert[k])))
tot = 0.0
for k in inert.keys():
    tot += inert[k].mass if hasattr(inert[k], 'mass') and inert[k].mass else 0.0
check('point masses total (g)', tot * 1e6, 200.0, 0.01)

# ---------- 7. couplings, ties, supports, LC3a ----------
cp = [('CP_BATT', 'SET_RP_BATT', L, 'S_BATT_SEAT'), ('CP_FC', 'SET_RP_FC', B, 'S_FC_SEAT'),
      ('CP_GPS', 'SET_RP_GPS', L, 'S_GPS_SEAT')]
for c in ('pp', 'pm', 'mp', 'mm'):
    arm = a.instances['ARM_%s-1' % c]
    cp.append(('CP_MOT_' + c, 'SET_RP_MOT_' + c, arm, 'S_MOT_SEAT'))
    cp.append(('CP_JNT_' + c, 'SET_RP_JNT_' + c, arm, 'S_JNT'))
for n, rpset, inst, surf in cp:
    m.Coupling(name=n, controlPoint=a.sets[rpset], surface=inst.surfaces[surf], influenceRadius=WHOLE_SURFACE,
               couplingType=DISTRIBUTING, adjust=False, weightingMethod=UNIFORM, localCsys=None,
               u1=ON, u2=ON, u3=ON, ur1=ON, ur2=ON, ur3=ON)
for c in ('pp', 'pm', 'mp', 'mm'):
    arm = a.instances['ARM_%s-1' % c]
    for s in ('L', 'R'):
        m.Tie(name='TIE_%s_%s' % (c, s), main=arm.surfaces['S_PRONG_BOSS_%s' % s],
              secondary=B.surfaces['S_FIN_BOSS_%s_%s' % (c, s)], positionToleranceMethod=SPECIFIED,
              positionTolerance=0.3, adjust=OFF, tieRotations=OFF, constraintEnforcement=SURFACE_TO_SURFACE,
              thickness=ON)
for k in range(5):
    m.Tie(name='TIE_LID_%d' % (k + 1), main=L.surfaces['S_LID_PAD_%d' % (k + 1)],
          secondary=B.surfaces['S_TUB_BOSS_%d' % (k + 1)], positionToleranceMethod=SPECIFIED,
          positionTolerance=0.1, adjust=OFF, tieRotations=OFF, constraintEnforcement=SURFACE_TO_SURFACE,
          thickness=ON)
for s in ('LC1', 'LC2a', 'LC2b', 'LC3a'):
    m.DisplacementBC(name='BC_A_' + s, createStepName=s, region=a.sets['SET_RP_JNT_pp'], u1=0.0, u2=0.0, u3=0.0)
    m.DisplacementBC(name='BC_B_' + s, createStepName=s, region=a.sets['SET_RP_JNT_pm'], u1=0.0, u3=0.0)
    m.DisplacementBC(name='BC_C_' + s, createStepName=s, region=a.sets['SET_RP_JNT_mp'], u3=0.0)
A = B.surfaces['S_FLOOR']
afl = pt.getArea(pt.surfaces['S_FLOOR'].faces)
pmag = 56.4 / afl
m.Pressure(name='LC3a_P', createStepName='LC3a', region=A, distributionType=UNIFORM, field='', magnitude=pmag)
print('LC3a_P = 56.4 / %.2f = %.6f MPa (note: 0.027371)' % (afl, pmag))
check('LC3a pressure x 1e6', pmag * 1e6, 27371.0, 5.0)

# ---------- 8. summary ----------
print('--- summary ---')
print('couplings %d, joint ties %d, lid ties %d, BCs %d' % (
    len([k for k in m.constraints.keys() if k.startswith('CP_')]),
    len([k for k in m.constraints.keys() if k.startswith('TIE_') and not k.startswith('TIE_LID')]),
    len([k for k in m.constraints.keys() if k.startswith('TIE_LID')]),
    len([k for k in m.boundaryConditions.keys() if k.startswith('BC_')])))
for k, ld in sorted(m.loads.items()):
    try:
        print('load %-10s region %s' % (k, region_name(ld)))
    except Exception:
        print('load %-10s (no region)' % k)
try:
    for tn, t in m.optimizationTasks.items():
        print('Tosca task %s kept (regions are checked again before H4)' % tn)
except Exception as e:
    print('Tosca task check: %s' % e)
print('=== V1 done: all checks OK. Save the model, then run V2_mesh.py. ===')
