import numpy as np, pickle, sys
sys.path.insert(0,'.'); import keels_r4 as K
D=pickle.load(open('mesh.pkl','rb')); nodes,conn,rho,fixed=D['nodes'],D['conn'],D['rho'],D['fixed']
P=nodes[conn-1]; cen=P.mean(1); x,y,z=cen.T
vol=np.abs(np.einsum('ij,ij->i',P[:,1]-P[:,0],np.cross(P[:,2]-P[:,0],P[:,3]-P[:,0])))/6
def read(fn):
    S,Mm,cur={},{},None
    for ln in open(fn):
        if ln.startswith('*DISTRIBUTION TABLE'): cur=S if 'Stiffness' in ln else Mm; continue
        if ln.startswith('*') or ln.startswith(' ') or not ln.strip(): continue
        p=ln.split(','); cur[int(p[0])]=float(p[1])
    n=len(conn); s=np.array([S[i] for i in range(1,n+1)]); m=np.array([Mm[i] for i in range(1,n+1)]); return s,m
inbox=(x>=-54)&(x<=-22)&(y>=-9)&(y<=9)&(z>=0)&(z<=21.5)
A=K.in_A(x,y,z); B=K.in_B(x,y,z)
cases={'_AB':(A|B,True),'_A':(A,True),'_N':(np.zeros_like(A),True),'_X':(A|B,False)}
ok_all=True
for tag,(shp,clean) in cases.items():
    s,m=read('dist_TH_r4%s.inp'%tag)
    exp=rho>=0.4
    if clean: exp=exp&~(inbox&~fixed&~shp)
    exp=exp|shp
    got=s>0.5
    checks={
     'solid pattern equals the independent rule': np.array_equal(got,exp),
     'stiffness values only 1 or 1e-6': set(np.round(np.log10(s)).astype(int).tolist())<= {0,-6},
     'mass column matches (1 / 1e-9)': np.array_equal(m>0.5,got) and set(np.round(np.log10(m)).astype(int).tolist())<={0,-9},
     'all fixed elements solid': bool(got[fixed].all()),
     'outside the clean box unchanged except shapes': np.array_equal(got[~inbox&~shp],(rho>=0.4)[~inbox&~shp]),
     'all shape elements solid': bool(got[shp].all()),
     'no design element solid in the box outside shapes (if clean)': (not clean) or (not got[inbox&~fixed&~shp].any()),
    }
    print('%s: solid %d elements, %.1f mm3 | '%(tag,got.sum(),vol[got].sum())+'; '.join('%s %s'%(k,'OK' if v else 'FAIL') for k,v in checks.items()))
    ok_all&=all(checks.values())
print('ALL CHECKS', 'PASS' if ok_all else 'FAIL')
