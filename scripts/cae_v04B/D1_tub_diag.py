# D1 - read-only diagnosis of the TUB design cell volume (V1 stop: 32852.4 mm3 in CAE, 40676.1 in the STEP).
# Run in the same CAE session after the V1 stop (model revB_v04B, part TUB exists). Set STEP_DIR as in V1.
# Prints: validity check of TUB, the design cell's face count, bounding box and centroid, the location of
# the missing volume, and the volumes of the STEP solids imported separately (no merge).
from __future__ import print_function
from abaqus import *
from abaqusConstants import *

STEP_DIR = r'C:\path\to\stage6_abaqus_v04B'      # <-- same as V1
m = mdb.models['revB_v04B']
p = m.parts['TUB']
FULL_V, FULL_C = 40676.10, (-9.2351, 0.1625, -0.4178)       # STEP design solid (OCC)

print('=== D1: TUB part ===')
try:
    p.checkGeometry(detailed=ON, reportFacetErrors=ON, level=20)
except Exception as e:
    print('checkGeometry: %s' % e)
des = [c.index for c in p.sets['DESIGN_TUB'].cells]
c = p.cells[des[0]]
print('design cell %d: faces %d (STEP solid: 187)' % (des[0], len(c.getFaces())))
mp = p.getMassProperties(regions=p.cells[des[0]:des[0] + 1], relativeAccuracy=HIGH)
v, cg = mp['volume'], mp['volumeCentroid']
print('CAE design cell: volume %.1f, centroid (%.2f, %.2f, %.2f)' % (v, cg[0], cg[1], cg[2]))
dv = FULL_V - v
if dv > 1.0:
    mc = [(FULL_V * FULL_C[k] - v * cg[k]) / dv for k in range(3)]
    print('missing volume %.1f mm3, its centroid about (%.1f, %.1f, %.1f)' % (dv, mc[0], mc[1], mc[2]))
bb = p.cells[des[0]:des[0] + 1].getBoundingBox()
print('design cell bounding box: %s' % (bb,))
tot = p.getMassProperties(regions=p.cells, relativeAccuracy=HIGH)['volume']
print('TUB all cells %.1f (STEP 51172.2)' % tot)
try:
    print('invalid entities / imprecise: %s' % (p.getInvalidEntities() if hasattr(p, 'getInvalidEntities') else 'n/a'))
except Exception as e:
    print('invalid entities: %s' % e)

print('=== D1: separate import (no combine, no merge) ===')
g = mdb.openStep(STEP_DIR + '\\TUB.step', scaleFromFile=OFF)
m.PartFromGeometryFile(name='TUBRAW', geometryFile=g, combine=False, dimensionality=THREE_D, type=DEFORMABLE_BODY)
raw = sorted([k for k in m.parts.keys() if k.startswith('TUBRAW')])
vols = []
for k in raw:
    q = m.parts[k]
    try:
        vv = q.getMassProperties(regions=q.cells, relativeAccuracy=HIGH)['volume']
    except Exception as e:
        vv = -1.0
    vols.append((vv, k, len(q.cells), len(q.faces)))
vols.sort(reverse=True)
for vv, k, nc, nf in vols[:3]:
    print('%-12s volume %10.1f  cells %d  faces %d' % (k, vv, nc, nf))
print('%d raw parts imported (STEP: 19 solids). Delete the TUBRAW parts after reading.' % len(raw))
print('=== D1 done ===')
