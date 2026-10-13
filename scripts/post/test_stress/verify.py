# independent check of stress_th.py on the mock (item 67): centroid stresses, volume-weighted P99.9, exclusion,
# clusters (scipy connected components on shared edges), free faces (dictionary count), pass / fail
import numpy as np, pickle, re, sys
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
D=pickle.load(open('mock.pkl','rb')); out=open(sys.argv[1]).read()
nodes,conn=D['nodes'],D['conn']; P=nodes[conn-1]; cen=P.mean(1)
vol=np.abs(np.linalg.det(np.stack([P[:,1]-P[:,0],P[:,2]-P[:,0],P[:,3]-P[:,0]],1)))/6
on=np.zeros(len(nodes)+1,bool); on[D['tie_nodes']]=True
for i,f in D['cp_faces']:
    k=int(f[-1])-1; FA=((0,1,2),(0,3,1),(1,3,2),(2,3,0)); on[[conn[i-1][q] for q in FA[k]]]=True
excl=on[conn].any(1)
sol=D['solid']
cnt={}
for e in np.nonzero(sol)[0]:
    for a,b,c in ((0,1,2),(0,3,1),(1,3,2),(2,3,0)):
        k=tuple(sorted((conn[e][a],conn[e][b],conn[e][c]))); cnt[k]=cnt.get(k,0)+1
surf=np.array([sol[e] and any(cnt[tuple(sorted((conn[e][a],conn[e][b],conn[e][c])))]==1 for a,b,c in ((0,1,2),(0,3,1),(1,3,2),(2,3,0))) for e in range(len(conn))])
LIM={'VM':36.3,'S33':15.9,'TSH':15.9}; names={'VM':'von Mises','S33':'S33 tension \\(across layers\\)','TSH':'sqrt\\(S13\\^2 \\+ S23\\^2\\)'}
ok=True; n=0; seen_fail=set(); seen_pass=set()
for st,S in D['steps'].items():
    m=S.mean(1); a,b,c,d,e,f=m.T
    val={'VM':np.sqrt(((a-b)**2+(b-c)**2+(c-a)**2)/2+3*(d*d+e*e+f*f)),'S33':c,'TSH':np.hypot(e,f)}
    for pn in ('TUB','LID','ARM_pp','ARM_pm','ARM_mp','ARM_mm'):
        chk=sol&(D['part']==pn)&~excl; ex=sol&(D['part']==pn)&excl
        for q in ('VM','S33','TSH'):
            x=val[q]; lim=LIM[q]
            xs=x[chk]; ws=vol[chk]; o=np.argsort(xs); cw=np.cumsum(ws[o]); p999=xs[o][np.searchsorted(cw,0.999*cw[-1])]
            over=np.nonzero(chk&(x>lim))[0]; nbad=0; ncl=0
            if len(over):
                E=[]
                for i_,r in enumerate(over):
                    for j_,s_ in enumerate(over[:i_]):
                        if len(set(conn[r])&set(conn[s_]))>=2: E.append((i_,j_))
                E=np.array(E).reshape(-1,2)
                ncl,lab=connected_components(coo_matrix((np.ones(len(E)),(E[:,0],E[:,1])),shape=(len(over),)*2),directed=False)
                for L in range(ncl):
                    g=over[lab==L]
                    if not (vol[g].sum()<1.0 and surf[g].any()): nbad+=1
            res='PASS' if (p999<=lim and nbad==0) else 'FAIL'
            exm=x[ex].max() if ex.any() else 0.0
            pat=r'%s\s+%s\s+%s\s+P99.9\s+([-0-9.]+) / [0-9.]+ MPa \(util [0-9.]+\) \| max\s+([-0-9.]+) \| above: (\d+) el. in (\d+) clusters \((\d+) failing\) \| excluded \(tie/coupling\) max\s+([-0-9.]+) \| (PASS|FAIL)'%(re.escape(pn),st,names[q])
            g_=re.search(pat,out)
            if not g_: print('NOT FOUND',pn,st,q); ok=False; continue
            got=g_.groups(); n+=1
            exp=(p999,x[chk].max(),len(over),ncl,nbad,exm,res)
            good=abs(float(got[0])-exp[0])<0.006 and abs(float(got[1])-exp[1])<0.006 and int(got[2])==exp[2] and int(got[3])==exp[3] and int(got[4])==exp[4] and abs(float(got[5])-exp[5])<0.006 and got[6]==exp[6]
            if not good: print('MISMATCH',pn,st,q,got,exp); ok=False
            (seen_fail if res=='FAIL' else seen_pass).add((pn,st,q))
print('cases with failing result: %d, passing: %d'%(len(seen_fail),len(seen_pass)))
print('expected features: TUB LC3a VM fails (big cluster):', ('TUB','LC3a','VM') in seen_fail, '; LID LC2b VM excluded peak does not fail:', ('LID','LC2b','VM') in seen_pass)
print('checked %d rows:'%n,'ALL CHECKS PASS' if ok else 'FAIL')
