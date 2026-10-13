# independent check of th04_build.py TH_KEELS / TH_CLEAN / TH_ISO on the mock (build log item 64)
# inside test: generalized winding number (solid angles, Van Oosterom and Strackee 1983), all triangles, no binning
import numpy as np, pickle, struct
D=pickle.load(open('mesh.pkl','rb')); nodes,conn,rho,fixed=D['nodes'],D['conn'],D['rho'],D['fixed']
P=nodes[conn-1]; cen=P.mean(1); x,y,z=cen.T
vol=np.abs(np.einsum('ij,ij->i',P[:,1]-P[:,0],np.cross(P[:,2]-P[:,0],P[:,3]-P[:,0])))/6
def stl(fn):
    d=open(fn,'rb').read(); n=struct.unpack('<I',d[80:84])[0]
    return np.frombuffer(d[84:84+50*n],dtype=[('n','<f4',3),('v','<f4',(3,3)),('a','<u2')])['v'].astype(float)
def winding(T,Q):
    w=np.zeros(len(Q))
    for i in range(0,len(Q),64):
        A=T[None,:,0]-Q[i:i+64,None];B=T[None,:,1]-Q[i:i+64,None];C=T[None,:,2]-Q[i:i+64,None]
        a,b,c=[np.linalg.norm(V,axis=2) for V in (A,B,C)]
        num=np.einsum('pij,pij->pi',A,np.cross(B,C))
        den=a*b*c+np.einsum('pij,pij->pi',A,B)*c+np.einsum('pij,pij->pi',B,C)*a+np.einsum('pij,pij->pi',C,A)*b
        w[i:i+64]=2*np.arctan2(num,den).sum(1)/(4*np.pi)
    return w
keel=np.zeros(len(cen),bool); amb=0
for fn in ('../keels/KEEL_A_r4.stl','../keels/KEEL_B_r4.stl'):
    T=stl(fn); lo,hi=T.reshape(-1,3).min(0),T.reshape(-1,3).max(0)
    c=np.nonzero(np.all((cen>=lo-1e-6)&(cen<=hi+1e-6),1))[0]
    w=winding(T,cen[c]); keel[c[w>0.5]]=True; amb+=int(((w>0.1)&(w<0.9)).sum())
print('independent keel selection: %d elements, %.1f mm3; ambiguous winding numbers (0.1 to 0.9): %d'%(keel.sum(),vol[keel].sum(),amb))
def read(fn):
    S,Mm,cur={},{},None
    for ln in open(fn):
        if ln.startswith('*DISTRIBUTION TABLE'): cur=S if 'Stiffness' in ln else Mm; continue
        if ln.startswith('*') or ln.startswith(' ') or not ln.strip(): continue
        p=ln.split(','); cur[int(p[0])]=float(p[1])
    n=len(conn); return np.array([S[i] for i in range(1,n+1)]),np.array([Mm[i] for i in range(1,n+1)])
CLEAN=(-54,-23,-11,11,-2,21.5)
inbox=(x>=CLEAN[0])&(x<=CLEAN[1])&(y>=CLEAN[2])&(y<=CLEAN[3])&(z>=CLEAN[4])&(z<=CLEAN[5])
cases={'_i30_F':(0.3,keel,True),'_i30_K':(0.3,keel,False),'_i30_C':(0.3,np.zeros_like(keel),True),'_F40':(0.4,keel,True)}
ok_all=True
for tag,(iso,shp,clean) in cases.items():
    s,m=read('dist_TH_r4%s.inp'%tag)
    exp=rho>=iso
    if clean: exp=exp&~(inbox&~fixed&~shp)
    exp=exp|shp
    got=s>0.5
    checks={
     'solid pattern equals the independent rule':np.array_equal(got,exp),
     'stiffness only 1 or 1e-6':set(np.round(np.log10(s)).astype(int).tolist())<={0,-6},
     'mass only 1 or 1e-9 and same pattern':np.array_equal(m>0.5,got) and set(np.round(np.log10(m)).astype(int).tolist())<={0,-9},
     'all fixed solid':bool(got[fixed].all()),
     'all keel elements solid':bool(got[shp].all()),
     'outside box unchanged except keels':np.array_equal(got[~inbox&~shp],(rho>=iso)[~inbox&~shp]),
     'no design element solid in the box outside keels (if clean)':(not clean) or (not got[inbox&~fixed&~shp].any()),
    }
    bad=int((got!=exp).sum())
    print('%s: solid %d, %.1f mm3, mismatches %d | '%(tag,got.sum(),vol[got].sum(),bad)+'; '.join('%s %s'%(k,'OK' if v else 'FAIL') for k,v in checks.items()))
    ok_all&=all(checks.values())
print('ALL CHECKS','PASS' if ok_all else 'FAIL')
