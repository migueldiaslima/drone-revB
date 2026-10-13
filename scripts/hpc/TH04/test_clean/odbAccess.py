import numpy as np, pickle
class O:
    def __init__(s,**k): s.__dict__.update(k)
D=pickle.load(open('mesh.pkl','rb'))
nodes=[O(label=i+1,coordinates=tuple(c)) for i,c in enumerate(D['nodes'])]
els=[O(label=i+1,type='C3D10',connectivity=tuple(int(v) for v in c)) for i,c in enumerate(D['conn'])]
des=[e for e,f in zip(els,D['fixed']) if not f]
inst=O(name='PART-1-1',nodes=nodes,elements=els,nodeSets={},elementSets={'TUB-1_ALL_TUB':O(elements=els),'TUB-1_DESIGN_TUB':O(elements=des)})
fr=O(description='',fieldOutputs={'MAT_PROP_NORMALIZED':O(bulkDataBlocks=[O(instance=inst,elementLabels=np.arange(1,len(els)+1),data=D['rho'][:,None])])})
def openOdb(p,readOnly=True):
    return O(steps={'FREQ':O(frames=[fr])},rootAssembly=O(instances={'PART-1-1':inst}),close=lambda:None)
