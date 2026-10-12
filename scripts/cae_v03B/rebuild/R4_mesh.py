# R4 - mesh per set-up sheet section 9 (laptop debug): BODY global 2.5 mm, arms 1.5 mm,
# fin-boss tie faces seeded 1.5 mm so both sides of each tie match. C3D10, free tet.
from __future__ import print_function
from abaqus import *
from abaqusConstants import *
import mesh
m = mdb.models['revB_v03B']
GLOBAL_BODY, ARM, JOINT = 2.5, 1.5, 1.5
et = (mesh.ElemType(elemCode=C3D10, elemLibrary=STANDARD),)
tot = 0
for n in ['BODY', 'ARM_pp', 'ARM_pm', 'ARM_mp', 'ARM_mm']:
    p = m.parts[n]
    p.deleteMesh()
    p.setMeshControls(regions=p.cells, elemShape=TET, technique=FREE)
    p.setElementType(regions=(p.cells,), elemTypes=et)
    if n == 'BODY':
        p.seedPart(size=GLOBAL_BODY, deviationFactor=0.1, minSizeFactor=0.1)
        ed = set()
        for k in p.surfaces.keys():
            if k.startswith('S_FIN_BOSS_'):
                for f in p.surfaces[k].faces:
                    ed.update(f.getEdges())
        ed = sorted(ed)
        es = p.edges[ed[0]:ed[0] + 1]
        for i in ed[1:]:
            es = es + p.edges[i:i + 1]
        p.seedEdgeBySize(edges=es, size=JOINT, deviationFactor=0.1, constraint=FINER)
        print('BODY: %d tie-face edges seeded at %.1f mm' % (len(ed), JOINT))
    else:
        p.seedPart(size=ARM, deviationFactor=0.1, minSizeFactor=0.1)
    p.generateMesh()
    q = p.verifyMeshQuality(criterion=ANALYSIS_CHECKS)
    tag = 'BODY' if n == 'BODY' else 'ARM'
    ne = len(p.elements)
    tot += ne
    print('%-7s %7d elements, %7d nodes | design %7d, fixed %7d | errors %d, warnings %d (%.2f %%)' % (
        n, ne, len(p.nodes), len(p.sets['DESIGN_' + tag].elements), len(p.sets['FIXED_' + tag].elements),
        len(q['failedElements']), len(q['warningElements']), 100.0 * len(q['warningElements']) / max(ne, 1)))
m.rootAssembly.regenerate()
print('TOTAL %d elements. Save the model.' % tot)
