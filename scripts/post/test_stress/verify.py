# independent statistics for the mock (np.linalg.eig on full matrices, per element loops avoided differently)
import numpy as np, pickle, re, sys
D=pickle.load(open('mock.pkl','rb')); out=open(sys.argv[1]).read()
nodes,conn=D['nodes'],D['conn']; P=nodes[conn-1]; cen=P.mean(1)
vol=np.abs(np.linalg.det(np.stack([P[:,1]-P[:,0],P[:,2]-P[:,0],P[:,3]-P[:,0]],1)))/6
FS=1.5; ALLOW={'vm':60.0,'p1':40.0,'p3':70.0,'s33':20.0}
ok=True; nchk=0
for st,S in D['steps'].items():
    T=np.zeros(S.shape[:2]+(3,3)); idx=[(0,0),(1,1),(2,2),(0,1),(0,2),(1,2)]
    for c,(i,j) in enumerate(idx): T[...,i,j]=S[...,c]; T[...,j,i]=S[...,c]
    ev=np.sort(np.real(np.linalg.eig(T)[0]),-1)
    dev=T-np.trace(T,axis1=-2,axis2=-1)[...,None,None]*np.eye(3)/3
    vm=np.sqrt(1.5*np.einsum('...ij,...ij->...',dev,dev))
    q={'vm':vm.max(1),'p1':ev[...,2].max(1),'p3':-ev[...,0].min(1),'s33':S[...,2].max(1)}
    for pn in ('TUB','LID','ARM'):
        m=D['solid']&(D['part']==pn)
        for k,lab in (('vm','von Mises'),('p1','max principal'),('p3','min principal'),('s33','S33 \\(z\\)')):
            x=q[k][m]; v=vol[m]
            pat=r'={20} %s .*?\n(?:.*\n)*?%-4s %s\s+max\s+([-0-9.]+)\s+p99.9\s+([-0-9.]+)\s+p99\s+([-0-9.]+) MPa \| allowable/FS ([0-9.]+): util max ([0-9.]+) p99.9 ([0-9.]+), volume above ([0-9.]+) mm\^3 \((\d+) el.\)'%(st,pn,lab)
            g=re.search(pat,out)
            if not g: print('NOT FOUND',st,pn,k); ok=False; continue
            lim=ALLOW[k]/FS
            exp=[x.max(),np.percentile(x,99.9),np.percentile(x,99),lim,x.max()/lim,np.percentile(x,99.9)/lim,v[x>lim].sum(),(x>lim).sum()]
            got=[float(t) for t in g.groups()]
            tol=[0.006,0.006,0.006,0.006,0.006,0.006,0.0006+1e-3*exp[6],0.5]
            good=all(abs(a-b)<=t for a,b,t in zip(got,exp,tol)); nchk+=1
            if not good: print('MISMATCH',st,pn,k,got,[round(e,3) for e in exp]); ok=False
print('checked %d step x part x quantity rows against the independent computation:'%nchk,'ALL CHECKS PASS' if ok else 'FAIL')
