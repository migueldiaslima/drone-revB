# V2 - G6 mesh for model revB_v04B (C3D10, free tet). Set LEVEL first:
#   'debug' : TUB 2.5 mm, LID 1.5 mm, ARM 1.5 mm; tie-face edges (fin bosses, lid bosses, lid pads) 1.5 mm
#   'prod'  : everything 1.0 mm (local seeds removed)
# G6 pass: 0 errors and warnings below 1 % in every part. Prints the counts for the build log.
from __future__ import print_function
from abaqus import *
from abaqusConstants import *
import mesh

LEVEL = 'debug'                     # <-- 'debug' or 'prod'
m = mdb.models['revB_v04B']
SIZES = {'debug': {'TUB': 2.5, 'LID': 1.5, 'ARM': 1.5, 'TIE': 1.5},
         'prod': {'TUB': 1.0, 'LID': 1.0, 'ARM': 1.0, 'TIE': None}}[LEVEL]
TIE_SURF = {'TUB': ('S_FIN_BOSS_', 'S_TUB_BOSS_'), 'LID': ('S_LID_PAD_1', 'S_LID_PAD_2', 'S_LID_PAD_3', 'S_LID_PAD_4')}
et = (mesh.ElemType(elemCode=C3D10, elemLibrary=STANDARD),)
tot, bad = 0, []
for n in ('TUB', 'LID', 'ARM'):
    p = m.parts[n]
    p.deleteMesh()
    try:
        p.deleteSeeds(regions=p.edges)
    except Exception:
        pass
    p.setMeshControls(regions=p.cells, elemShape=TET, technique=FREE)
    p.setElementType(regions=(p.cells,), elemTypes=et)
    p.seedPart(size=SIZES[n], deviationFactor=0.1, minSizeFactor=0.1)
    if SIZES['TIE'] and n in TIE_SURF:
        ed = set()
        for k in p.surfaces.keys():
            if any(k.startswith(t) for t in TIE_SURF[n]):
                for f in p.surfaces[k].faces:
                    ed.update(f.getEdges())
        ed = sorted(ed)
        if ed:
            es = p.edges[ed[0]:ed[0] + 1]
            for i in ed[1:]:
                es = es + p.edges[i:i + 1]
            p.seedEdgeBySize(edges=es, size=SIZES['TIE'], deviationFactor=0.1, constraint=FINER)
            print('%s: %d tie-face edges seeded at %.1f mm' % (n, len(ed), SIZES['TIE']))
    p.generateMesh()
    unmeshed = [c.index for c in p.cells if not p.getMeshStats(regions=p.cells[c.index:c.index + 1]).numTetElems]
    q = p.verifyMeshQuality(criterion=ANALYSIS_CHECKS)
    ne = len(p.elements)
    mult = 4 if n == 'ARM' else 1
    tot += ne * mult
    nf, nw = len(q['failedElements']), len(q['warningElements'])
    pct = 100.0 * nw / max(ne, 1)
    ok = not unmeshed and nf == 0 and pct < 1.0
    if not ok:
        bad.append(n)
    print('%-4s %8d elements, %8d nodes | design %8d, fixed %8d | errors %d, warnings %d (%.2f %%) | unmeshed cells %s  %s%s' % (
        n, ne, len(p.nodes), len(p.sets['DESIGN_' + n].elements), len(p.sets['FIXED_' + n].elements),
        nf, nw, pct, unmeshed or 'none', 'G6 PASS' if ok else 'G6 FAIL', '  (x4 instances)' if mult == 4 else ''))
    if nw:
        xs = []
        for e in q['warningElements'][:2000]:
            c = [p.nodes[i].coordinates for i in e.connectivity[:4]]
            xs.append(((c[0][0] + c[1][0] + c[2][0] + c[3][0]) / 4.0,
                       (c[0][1] + c[1][1] + c[2][1] + c[3][1]) / 4.0,
                       (c[0][2] + c[1][2] + c[2][2] + c[3][2]) / 4.0))
        print('     warning element centres (first 10): %s' % ', '.join('(%.1f, %.1f, %.1f)' % x for x in xs[:10]))
m.rootAssembly.regenerate()
print('TOTAL %d elements (%s mesh)' % (tot, LEVEL))
print('=== V2 %s: %s ===' % (LEVEL, 'G6 PASS, save the model' if not bad else 'G6 FAIL in %s: stop and report' % bad))
