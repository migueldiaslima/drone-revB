# mock for stress_th.py (item 67): one flattened instance, parts TUB / LID / 4 arms, DESIGN sets, tie and coupling
# surfaces (node-based and face-based), 4 integration points per element with an analytic field and hot spots
import numpy as np, pickle
h=1.0
xs=np.arange(0,36.1,h)+0.11; ys=np.arange(0,12.1,h)+0.07; zs=np.arange(0,8.1,h)+0.05
nx,ny,nz=len(xs),len(ys),len(zs)
nid=lambda i,j,k:(i*ny+j)*nz+k+1
X,Y,Z=np.meshgrid(xs,ys,zs,indexing='ij'); nodes=np.c_[X.ravel(),Y.ravel(),Z.ravel()]
cube=[(0,0,0),(1,0,0),(1,1,0),(0,1,0),(0,0,1),(1,0,1),(1,1,1),(0,1,1)]
TETS=[(0,1,2,6),(0,2,3,6),(0,3,7,6),(0,7,4,6),(0,4,5,6),(0,5,1,6)]
conn=[]
for i in range(nx-1):
  for j in range(ny-1):
    for k in range(nz-1):
      c=[nid(i+a,j+b,d+k) for a,b,d in cube]
      for t in TETS: conn.append([c[q] for q in t])
conn=np.asarray(conn); cen=nodes[conn-1].mean(1); x,y,z=cen.T
part=np.select([x<12,x<18,x<22,x<26,x<30],['TUB','LID','ARM_pp','ARM_pm','ARM_mp'],'ARM_mm')
rng=np.random.default_rng(5)
solid=(rng.random(len(conn))<0.85)|(z<2)
design=(y>2)&(y<10)
steps={}
for s,sc in (('LC1',1.0),('LC2a',0.6),('LC2b',1.2),('LC3a',1.6)):
  ip=[]
  for q in range(4):
    p=0.6*cen+0.4*nodes[conn[:,q]-1]; px,py,pz=p.T
    ip.append(0.25*np.c_[sc*2*px, sc*py, sc*(pz-4)*2, sc*0.5*px*np.cos(pz), sc*0.3*py*pz, sc*0.4*(px-py)])
  steps[s]=np.stack(ip,1)
# hot spots: a small surface cluster (passes), a larger through-thickness block (fails), one on a tie face (excluded)
small=(np.abs(x-8.6)<0.6)&(np.abs(y-0.6)<0.6)&(z<1.2)
big=(np.abs(x-4.6)<1.6)&(np.abs(y-6.6)<1.6)&(np.abs(z-4.0)<1.6)
steps['LC3a'][small,:,0]+=300; steps['LC3a'][big,:,0]+=300; steps['LC3a'][big,:,2]+=60
tie_nodes=np.nonzero(np.abs(nodes[:,0]-16.11)<1e-6)[0]+1         # plane x = 16.11 (inside the LID)
steps['LC2b'][(np.abs(x-16.11)<1.0)&(y<3),:,0]+=500                # peak at the tie, must be excluded
cp_faces=[(i+1,'FACE1') for i in np.nonzero((z<1.0)&(x>30))[0]][:400]   # face-based coupling surface on ARM_mm floor
pickle.dump(dict(nodes=nodes,conn=conn,part=part,solid=solid,design=design,steps=steps,tie_nodes=tie_nodes,cp_faces=cp_faces),open('mock.pkl','wb'))
with open('dist_mock.inp','w') as f:
  for nm,lo in (('Stiffness',1e-6),('Mass',1e-9)):
    f.write('*DISTRIBUTION TABLE, NAME=__SMATso_Distribution_%s_1_FMT_\n  RATIO,RATIO\n*DISTRIBUTION, DESIGN VARIABLE, LOCATION=ELEMENT, NAME=__SMATso_Distribution_%s_1, TABLE=__SMATso_Distribution_%s_1_FMT_\n , 1., 1.\n'%(nm,nm,nm))
    for l in range(1,len(conn)+1): f.write('%d, %.6e, %.6e\n'%(l,1.0 if solid[l-1] else lo,998.5))
open('TH_mock.inp','w').write('*Tie, name=TIE_LIDRIM, adjust=no, position tolerance=0.1, no rotation, type=SURFACE TO SURFACE\n     TUB-1_S_RIM_UNDER_LID, LID-1_S_LID_BOTTOM\n*Coupling, constraint name=CP_PAD, ref node=RP_PAD, surface=ARM_mm-1_S_PAD\n*Distributing, weighting method=UNIFORM\n')
print(len(conn),'elements,',solid.sum(),'solid, small',small.sum(),'big',big.sum())
