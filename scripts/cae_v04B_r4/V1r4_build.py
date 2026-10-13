# V1r4 - v04-B revision 4 model (D-086, export note docs/stage6_v04B_r4_export_note.md), derived from V1r3.
# Changes against V1r3: TUB 18 cells (17 fixed: 3 lid bosses, 4 FC bosses, 8 fin bosses, spine + boss 3,
# GPS deck 1218.56), design / fixed 39,538.5 / 12,796.3 mm3; boss 5 gone; TUB partition x = -32;
# S_RIM_UNDER_LID = TUB top at z 21.5 with x >= -32 and |y| <= 17, 363.23 mm2; S_GPS_SEAT on the TUB
# (deck pocket floor, 209.19); LID 3 cells (1 fixed 3417.1, 2 design 2357.0), partitions x = +-29, +-32 and
# y = +-14, S_BATT_SEAT 1056.00 (frame + band, pad and link faces excluded), S_LID_BOTTOM 3 faces 2314.02;
# CP_GPS on the TUB; no lid ties in this model (the seat tie TIE_LIDRIM is added by V3r4 / W2r4, G7b);
# FIXED_ALL 38 cells. The lid pad circles for the five-boss sensitivity tie (G7a) are not made here
# (Stage 7, D-082 item 3). Run in revB_v04B_r4.cae. STEP folder in v04B_r4_paths.txt.
#
# Header of V1r3 (revision 3) (D-084, export note docs/stage6_v04B_r3_export_note.md), derived from V1
# (revision 2). Changes against V1: TUB 18 cells (17 fixed: the antenna spine fused with the rear-left lid
# boss, 1461.2 mm3, replaces that boss and the antenna boss), design / fixed 39,368.8 / 11,711.1 mm3;
# surface S_ANT_PAD (spine underside at z = 0, 175.93 mm2); RP_ANT at (-48.6, 3.5, -4.0) with CP_ANT and
# point mass PM_ANT 2.24 g; RP_FC 22.91 g, RP_GPS 4.23 g; point masses 199.58 g; FIXED_ALL 42 cells.
# Run in revB_v04B_r3.cae (File > Save As of revB_v03B_D056.cae). STEP folder in v04B_r3_paths.txt.
#
# Original V1 header:
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
    if os.path.exists(os.path.join(_d, 'v04B_r4_paths.txt')):
        STEP_DIR = open(os.path.join(_d, 'v04B_r4_paths.txt')).read().strip()
        break
if not STEP_DIR:
    STEP_DIR = r'C:\path\to\geometry\v04B_r4'      # <-- or put the folder in v04B_r3_paths.txt next to this script
print('STEP_DIR = %s' % STEP_DIR)
SRC, MODEL = 'revB_v03B', 'revB_v04B'
CORNERS = {'pp': (1, 1), 'pm': (1, -1), 'mp': (-1, 1), 'mm': (-1, -1)}
ROT = {'pp': 0.0, 'pm': -90.0, 'mp': 90.0, 'mm': 180.0}
SHIFT = 3.0
R2 = 1.0 / math.sqrt(2.0)
LIDBOSS = [(21.0, 9.5), (21.0, -9.5), (-21.0, 5.0), (-21.0, -5.0)]     # rev 4: boss 5 deleted (D-086)
NEW_RP = {'MOT_pp': (52.5, 52.5, 8.5), 'MOT_pm': (52.5, -52.5, 8.5),
          'MOT_mp': (-52.5, 52.5, 8.5), 'MOT_mm': (-52.5, -52.5, 8.5),
          'JNT_pp': (26.335, 26.335, -2.5), 'JNT_pm': (26.335, -26.335, -2.5),
          'JNT_mp': (-26.335, 26.335, -2.5), 'JNT_mm': (-26.335, -26.335, -2.5),
          'GPS': (-44.0, 0.0, 26.5)}
GPS_MASS = 4.23e-6                 # rev 3 (D-084 item 5): GPS 2.6 + cap, 2 screws, 2 inserts
FC_MASS = 22.91e-6                  # rev 3: antenna, holder, screw, insert moved out of the RP_FC lump
ANT_MASS = 2.24e-6                  # rev 3: new RP_ANT (antenna 0.9, holder 0.94, screw 0.23, insert 0.17)
ANT_RP = (-48.6, 3.5, -4.0)
SPINE_BOSS = 2                      # index in LIDBOSS of the boss fused with the spine: (-21, +5)
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


def vol_match(v, table, tol=0.15):
    for k in table:
        if abs(v - k) <= tol:
            return k
    return None


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
if not mdb.pathName.lower().endswith('revb_v04b_r4.cae'):
    stop('open revB_v03B_D056.cae, File > Save As revB_v04B_r4.cae, then run V1r4 (current: %s)' % mdb.pathName)
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
TUB_FIX = {133.45: 3, 240.24: 4, 1461.19: 1, 1094.4: 8, 1218.56: 1}
fix_t, des_t, spine, deck = [], [], [], []
byk = {}
for v, ids in g.items():
    k = vol_match(v, TUB_FIX)
    if k is not None:
        byk.setdefault(k, []).extend(ids)
        fix_t += ids
        if k == 1461.19:
            spine += ids
        if k == 1218.56:
            deck += ids
    else:
        des_t += ids
for k in sorted(TUB_FIX):
    check_n('TUB cells of %.1f mm3' % k, len(byk.get(k, [])), TUB_FIX[k])
pt.Set(name='FIXED_TUB', cells=ca(pt, fix_t))
pt.Set(name='DESIGN_TUB', cells=ca(pt, des_t))
check_n('TUB fixed cells', len(fix_t), 17)
check_n('TUB design cells', len(des_t), 1)
check('TUB fixed volume', pt.getVolume(cells=ca(pt, fix_t)), 12796.3, 1.0)
check('TUB design volume', pt.getVolume(cells=ca(pt, des_t)), 39538.5, 1.0)
spineset = set(spine)
deckset = set(deck)
bb = pt.cells[deck[0]:deck[0] + 1].getBoundingBox()
print('GPS deck cell bbox x %.2f..%.2f y %.2f..%.2f z %.2f..%.2f (expected -54..-32.5, -12..12, 21.5..26.5)' % (
    bb['low'][0], bb['high'][0], bb['low'][1], bb['high'][1], bb['low'][2], bb['high'][2]))
if abs(bb['low'][0] + 54.0) > 0.01 or abs(bb['high'][0] + 32.5) > 0.01 or abs(bb['high'][2] - 26.5) > 0.01:
    stop('GPS deck cell not where the export note puts it')
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
n = partition_plane(pt, zfaces(pt, 21.5, 1.0), 0, -32.0)
print('rim partition x = -32 (lid end, rev 4): %d face(s) cut' % n)

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
    if k == SPINE_BOSS:
        on_spine = set(pt.faces[idx[0]].getCells()) <= spineset
        print('%s on the spine cell: %s' % (nm, 'OK' if on_spine else '<<< MISMATCH'))
        if not on_spine:
            stop('boss %d top face is not on the spine cell' % (k + 1))
    pt.Surface(name=nm, side1Faces=fa(pt, idx))
ant = [i for i in zfaces(pt, 0.0, -1.0) if set(pt.faces[i].getCells()) & spineset]
for i in ant:
    print('  spine face at z = 0: %4d  area %8.2f  cells %s' % (i, area(pt, [i]), pt.faces[i].getCells()))
check_n('S_ANT_PAD faces', len(ant), 1)
check_n('S_ANT_PAD cells (external face)', len(pt.faces[ant[0]].getCells()), 1)
check('S_ANT_PAD area', area(pt, ant), 175.93, 0.5)
pt.Surface(name='S_ANT_PAD', side1Faces=fa(pt, ant))
rim = [i for i in top_t if abs(pt.faces[i].pointOn[0][1]) < 17.0 and pt.faces[i].pointOn[0][0] > -32.0
       and len(pt.faces[i].getCells()) == 1]
print('S_RIM_UNDER_LID: %d faces' % len(rim))
check('S_RIM_UNDER_LID area', area(pt, rim), 363.23, 0.5)
strip = [i for i in top_t if -32.5 < pt.faces[i].pointOn[0][0] < -32.0 and len(pt.faces[i].getCells()) == 1]
check('keel strip x -32.5..-32 (left free)', area(pt, strip), 9.0, 0.1)
gps = [i for i in zfaces(pt, 24.0, 1.0) if i in fx and set(pt.faces[i].getCells()) <= deckset
       and -52.81 < pt.faces[i].pointOn[0][0] < -35.19 and abs(pt.faces[i].pointOn[0][1]) < 6.31]
check_n('S_GPS_SEAT faces (TUB)', len(gps), 1)
check('S_GPS_SEAT area (TUB)', area(pt, gps), 209.19, 0.5)
pt.Surface(name='S_GPS_SEAT', side1Faces=fa(pt, gps))
pt.Surface(name='S_RIM_UNDER_LID', side1Faces=fa(pt, rim))

# ---------- 3. LID ----------
pl = import_part('LID', 'LID.step')
g = cells_by_volume(pl, None)
print('LID cell volumes: %s' % ', '.join('%.1f x %d' % (v, len(g[v])) for v in sorted(g)))
LID_FIX = {3417.1: 1}
fix_l, des_l = [], []
for v, ids in g.items():
    if vol_match(v, LID_FIX, 0.2) is not None:
        fix_l += ids
    else:
        des_l += ids
pl.Set(name='FIXED_LID', cells=ca(pl, fix_l))
pl.Set(name='DESIGN_LID', cells=ca(pl, des_l))
check_n('LID fixed cells', len(fix_l), 1)
check_n('LID design cells', len(des_l), 2)
check('LID fixed volume', pl.getVolume(cells=ca(pl, fix_l)), 3417.1, 1.0)
check('LID design volume', pl.getVolume(cells=ca(pl, des_l)), 2357.0, 1.0)
fixset_l = set(fix_l)
# top of the fixed cell: frame, band, tab, pads and links are one face; cut at the frame inner edges and x = +-32
for axis, val in ((0, 32.0), (0, -32.0), (0, 29.0), (0, -29.0), (1, 14.0), (1, -14.0)):
    n = partition_plane(pl, zfaces(pl, 24.0, 1.0, fixset_l), axis, val)
    print('lid top partition %s = %+.0f: %d face(s) cut' % ('xy'[axis], val, n))
fxl = fixed_ext(pl, fixset_l)
top_l = [i for i in zfaces(pl, 24.0, 1.0) if i in fxl]


def in_opening(p, i):
    # pad and link faces lie in the two frame openings (9 < |x| < 29, |y| < 14); frame and band do not
    x, y = p.faces[i].pointOn[0][0], p.faces[i].pointOn[0][1]
    return 9.0 < abs(x) < 29.0 and abs(y) < 14.0


inx = [i for i in top_l if abs(pl.faces[i].pointOn[0][0]) < 32.0]
batt = [i for i in inx if not in_opening(pl, i)]
padlink = [i for i in inx if in_opening(pl, i)]
bot_l = zfaces(pl, 21.5, -1.0)
print('--- LID surfaces ---')
check('LID fixed top within |x| < 32', area(pl, inx), 1187.84, 0.5)
check('pad + link top faces (excluded)', area(pl, padlink), 131.84, 0.5)
for nm, idx, nexp, aexp in (('S_BATT_SEAT', batt, None, 1056.00), ('S_LID_BOTTOM', bot_l, 3, 2314.02)):
    print('%s: %d faces' % (nm, len(idx)))
    if nexp is not None:
        check_n(nm + ' faces', len(idx), nexp)
    check(nm + ' area', area(pl, idx), aexp, 0.5)
    pl.Surface(name=nm, side1Faces=fa(pl, idx))

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
check_n('FIXED_ALL cells', len(a.sets['FIXED_ALL'].cells), 38)
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
if 'SET_RP_ANT' in a.sets.keys():
    stop('SET_RP_ANT already exists in the source model')
f = a.ReferencePoint(point=ANT_RP)
a.Set(name='SET_RP_ANT', referencePoints=(a.referencePoints[f.id],))
a.features.changeKey(fromName=f.name, toName='RP_ANT')
rpobj = lambda key: a.sets['SET_RP_' + key].referencePoints[0]
for gname, cs in GROUPS.items():
    a.Set(name=gname, referencePoints=tuple(rpobj('MOT_' + c) for c in cs))
for key in sorted(NEW_RP.keys()) + ['BATT', 'FC', 'ANT']:
    xyz = a.getCoordinates(rpobj(key))
    exp = NEW_RP.get(key, {'BATT': (0.0, 0.0, 40.0), 'FC': (0.0, 0.0, 0.0), 'ANT': ANT_RP}.get(key))
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
nfc = 0
for k in inert.keys():
    if region_name(inert[k]) == 'SET_RP_FC':
        inert[k].setValues(mass=FC_MASS)
        nfc += 1
        print('point mass %s on SET_RP_FC set to %.2e t' % (k, FC_MASS))
check_n('point masses on SET_RP_FC', nfc, 1)
a.engineeringFeatures.PointMassInertia(name='PM_ANT', region=a.sets['SET_RP_ANT'], mass=ANT_MASS, alpha=0.0, composite=0.0)
print('point mass PM_ANT %.2e t on SET_RP_ANT created' % ANT_MASS)
print('loads re-linked: %d (expected 8), point masses re-linked: %d (expected 9)' % (nl, ni))
for k in sorted(inert.keys()):
    print('  point mass %-10s on %s' % (k, region_name(inert[k])))
tot = 0.0
for k in inert.keys():
    tot += inert[k].mass if hasattr(inert[k], 'mass') and inert[k].mass else 0.0
check('point masses total (g)', tot * 1e6, 199.58, 0.01)

# ---------- 7. couplings, ties, supports, LC3a ----------
cp = [('CP_BATT', 'SET_RP_BATT', L, 'S_BATT_SEAT'), ('CP_FC', 'SET_RP_FC', B, 'S_FC_SEAT'),
      ('CP_GPS', 'SET_RP_GPS', B, 'S_GPS_SEAT'), ('CP_ANT', 'SET_RP_ANT', B, 'S_ANT_PAD')]
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
# rev 4: no lid ties here; the seat tie TIE_LIDRIM (G7b, D-082) is added by V3r4 and W2r4
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
print('=== V1r4 done: all checks OK. Save the model, then run V2_mesh.py (cae_v04B, LEVEL debug). ===')
