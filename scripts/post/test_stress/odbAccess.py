import numpy as np, pickle
class O:
    def __init__(s,**k): s.__dict__.update(k)
    def keys(s): return list(s.__dict__.keys())
D=pickle.load(open('mock.pkl','rb'))
nodes=[O(label=i+1,coordinates=tuple(c)) for i,c in enumerate(D['nodes'])]
els=[O(label=i+1,type='C3D10',connectivity=tuple(int(v) for v in c)) for i,c in enumerate(D['conn'])]
sets={}
for pn,nm in (('TUB','TUB-1_ALL_TUB'),('LID','LID-1_ALL_LID'),('ARM','ARM_pp-1_ALL_ARM')):
    sets[nm]=O(elements=[e for e,p in zip(els,D['part']) if p==pn])
inst=O(name='PART-1-1',nodes=nodes,elements=els,elementSets=sets)
def frame(S):
    n=S.shape[0]; labs=np.repeat(np.arange(1,n+1),4)
    return O(fieldOutputs={'S':O(bulkDataBlocks=[O(instance=inst,elementLabels=labs,data=S.reshape(-1,6))]),'U':None})
steps={k:O(frames=[frame(v)]) for k,v in D['steps'].items()}
class Steps(dict): pass
def openOdb(p,readOnly=True):
    st=Steps(steps)
    return O(steps=st,rootAssembly=O(instances={'PART-1-1':inst}),close=lambda:None)
