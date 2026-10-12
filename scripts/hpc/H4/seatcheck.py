# seatcheck.py - D-082 (b): density of the tub elements under the lid seat, and of the lid design
# elements, on one saved Tosca cycle (flattened odb). Run:  abaqus python seatcheck.py <cycle odb>
# Tub seat zone: element centroid z between 19.5 and 21.5 (2 mm under the seat), inside the lid
# footprint (|x| <= 32 and |y| <= 17, or x < -32 and |y| <= 10). Lid design: centroid z above 21.5.
from __future__ import print_function
import sys
import numpy as np
from odbAccess import openOdb
path = [a for a in sys.argv[1:] if a.lower().endswith('.odb')][0]
o = openOdb(path, readOnly=True)
st = o.steps['FREQ']
fr = [f for f in st.frames if any('MAT_PROP_NORMALIZED' in k.upper() for k in f.fieldOutputs.keys())][-1]
key = [k for k in fr.fieldOutputs.keys() if 'MAT_PROP_NORMALIZED' in k.upper()][0]
rho = {}
for b in fr.fieldOutputs[key].bulkDataBlocks:
    iname = b.instance.name if b.instance is not None else ''
    d = np.asarray(b.data).reshape(len(b.elementLabels), -1)[:, 0]
    for l, v in zip(np.asarray(b.elementLabels).tolist(), d.tolist()):
        rho[(iname, l)] = v
seat, lid = [], []
for iname, inst in o.rootAssembly.instances.items():
    xyz = dict((n.label, n.coordinates) for n in inst.nodes)
    for e in inst.elements:
        k = (iname, e.label)
        if k not in rho or not e.type.startswith('C3D'):
            continue
        c = np.mean([xyz[n] for n in e.connectivity[:4]], axis=0)
        x, y, z = c
        foot = (abs(x) <= 32 and abs(y) <= 17) or (x < -32 and abs(y) <= 10)
        if 19.5 <= z <= 21.5 and foot:
            seat.append(rho[k])
        elif z > 21.5:
            lid.append(rho[k])
for name, v in (('tub seat zone (design elements)', seat), ('lid design elements', lid)):
    v = np.asarray(v)
    if len(v):
        print('%-32s %6d elements | mean density %.3f | share below 0.3 %.2f | below 0.5 %.2f' % (
            name, len(v), v.mean(), (v < 0.3).mean(), (v < 0.5).mean()))
    else:
        print('%-32s none found' % name)
o.close()
