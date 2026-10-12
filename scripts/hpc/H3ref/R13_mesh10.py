# R13 - H3 reference mesh (D-062): BODY and ARM at 1.0 mm, C3D10 free tet, then writes the H3
# reference job input H3_ref.inp (D-063 caps). Run in revB_v03B_m10.cae (a Save As copy of
# revB_v03B_D056.cae), work directory = project folder. Model revB_v03B keeps DV-18.
from __future__ import print_function
from abaqus import *
from abaqusConstants import *
import mesh
m = mdb.models['revB_v03B']
SIZE = 1.0
et = (mesh.ElemType(elemCode=C3D10, elemLibrary=STANDARD),)
tot = 0
for n in ['BODY', 'ARM']:
    p = m.parts[n]
    p.deleteMesh()
    try:
        p.deleteSeeds(regions=p.edges)
        print('%s: local edge seeds deleted' % n)
    except Exception as e:
        print('%s: deleteSeeds: %s' % (n, e))
    p.setMeshControls(regions=p.cells, elemShape=TET, technique=FREE)
    p.setElementType(regions=(p.cells,), elemTypes=et)
    p.seedPart(size=SIZE, deviationFactor=0.1, minSizeFactor=0.1)
    p.generateMesh()
    tag, mult = ('BODY', 1) if n == 'BODY' else ('ARM', 4)
    ne = len(p.elements)
    tot += ne * mult
    q = p.verifyMeshQuality(criterion=ANALYSIS_CHECKS)
    print('%-5s %8d elements, %8d nodes | design %8d, fixed %8d | errors %d, warnings %d%s' % (
        n, ne, len(p.nodes), len(p.sets['DESIGN_' + tag].elements), len(p.sets['FIXED_' + tag].elements),
        len(q['failedElements']), len(q['warningElements']), '  (x4 instances)' if mult == 4 else ''))
m.rootAssembly.regenerate()
print('TOTAL %d elements (2.5 / 1.5 mesh: 149,305)' % tot)
if 'H3_ref' in mdb.jobs.keys():
    del mdb.jobs['H3_ref']
mdb.Job(name='H3_ref', model='revB_v03B', type=ANALYSIS)
mdb.jobs['H3_ref'].writeInput(consistencyChecking=OFF)
print('=== R13 done: H3_ref.inp written. Save the model (File > Save). ===')
