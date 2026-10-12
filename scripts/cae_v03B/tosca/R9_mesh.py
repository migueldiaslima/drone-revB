# R9 - mesh for the first Tosca run (D-058 target): BODY 2.0 mm with the fin-boss tie faces at 1.2 mm,
# arm part 1.2 mm (one part, meshed once, shared by the four instances). C3D10, free tet.
# If the data check memory estimate is above about 10 GB, set the fallback below and re-run.
from __future__ import print_function
from abaqus import *
from abaqusConstants import *
import mesh
m = mdb.models['revB_v03B']
BODY_GLOBAL, JOINT, ARM = 2.0, 1.2, 1.2          # fallback (Phase 8 mesh): 2.5, 1.5, 1.5
et = (mesh.ElemType(elemCode=C3D10, elemLibrary=STANDARD),)
tot = 0
for n in ['BODY', 'ARM']:
    p = m.parts[n]
    p.deleteMesh()
    p.setMeshControls(regions=p.cells, elemShape=TET, technique=FREE)
    p.setElementType(regions=(p.cells,), elemTypes=et)
    if n == 'BODY':
        p.seedPart(size=BODY_GLOBAL, deviationFactor=0.1, minSizeFactor=0.1)
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
        tag, mult = 'BODY', 1
    else:
        p.seedPart(size=ARM, deviationFactor=0.1, minSizeFactor=0.1)
        tag, mult = 'ARM', 4
    p.generateMesh()
    q = p.verifyMeshQuality(criterion=ANALYSIS_CHECKS)
    ne = len(p.elements)
    tot += ne * mult
    print('%-5s %7d elements, %7d nodes | design %7d, fixed %7d | errors %d, warnings %d (%.2f %%)%s' % (
        n, ne, len(p.nodes), len(p.sets['DESIGN_' + tag].elements), len(p.sets['FIXED_' + tag].elements),
        len(q['failedElements']), len(q['warningElements']), 100.0 * len(q['warningElements']) / max(ne, 1),
        '  (x4 instances)' if mult == 4 else ''))
m.rootAssembly.regenerate()
print('TOTAL %d elements in the model. Save the model.' % tot)
