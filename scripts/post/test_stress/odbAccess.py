import numpy as np, pickle
class O:
    def __init__(s,**k): s.__dict__.update(k)
class K(dict):
    pass
D=pickle.load(open('mock.pkl','rb'))
nodes=[O(label=i+1,coordinates=tuple(c)) for i,c in enumerate(D['nodes'])]
els=[O(label=i+1,type='C3D10',connectivity=tuple(int(v) for v in c)) for i,c in enumerate(D['conn'])]
sets=K()
for pn,nm in (('TUB','TUB-1_ALL_TUB'),('LID','LID-1_ALL_LID'),('ARM_pp','ARM_PP-1_ALL_ARM'),('ARM_pm','ARM_PM-1_ALL_ARM'),('ARM_mp','ARM_MP-1_ALL_ARM'),('ARM_mm','ARM_MM-1_ALL_ARM')):
    sets[nm]=O(elements=[e for e,p in zip(els,D['part']) if p==pn])
sets['TUB-1_DESIGN_TUB']=O(elements=[e for e,p,d in zip(els,D['part'],D['design']) if d and p=='TUB'])
sets['LID-1_DESIGN_LID']=O(elements=[e for e,p,d in zip(els,D['part'],D['design']) if d and p=='LID'])
nodesurf=O(nodes=[[nodes[i-1] for i in D['tie_nodes']]],elements=[],faces=[])
empty=O(nodes=[[]],elements=[[]],faces=[[]])
facesurf=O(nodes=[[]],elements=[[els[i-1] for i,f in D['cp_faces']]],faces=[[f for i,f in D['cp_faces']]])
surfs=K({'TUB-1_S_RIM_UNDER_LID':nodesurf,'LID-1_S_LID_BOTTOM':nodesurf,'ARM_MM-1_S_PAD':facesurf})
inst=O(name='PART-1-1',nodes=nodes,elements=els,elementSets=sets,surfaces=K())
def frame(S):
    n=S.shape[0]; labs=np.repeat(np.arange(1,n+1),4)
    return O(fieldOutputs=K({'S':O(bulkDataBlocks=[O(instance=inst,elementLabels=labs,data=S.reshape(-1,6))]),'U':None}))
steps=K({k:O(frames=[frame(v)]) for k,v in D['steps'].items()})
def openOdb(p,readOnly=True):
    return O(steps=steps,rootAssembly=O(instances=K({'PART-1-1':inst}),surfaces=surfs),close=lambda:None)
