import numpy as np, pickle
h=1.0
xs=np.arange(-56,-15.9,h); ys=np.arange(-14,14.1,h); zs=np.arange(-4,26.1,h)
nx,ny,nz=len(xs),len(ys),len(zs)
nid=lambda i,j,k: (i*ny+j)*nz+k+1
X,Y,Z=np.meshgrid(xs,ys,zs,indexing='ij')
nodes=np.c_[X.ravel(),Y.ravel(),Z.ravel()]
# 6-tet split of each cube (Kuhn)
cube=[(0,0,0),(1,0,0),(1,1,0),(0,1,0),(0,0,1),(1,0,1),(1,1,1),(0,1,1)]
TETS=[(0,1,2,6),(0,2,3,6),(0,3,7,6),(0,7,4,6),(0,4,5,6),(0,5,1,6)]
conn=[]
for i in range(nx-1):
  for j in range(ny-1):
    for k in range(nz-1):
      c=[nid(i+a,j+b,k+d) for a,b,d in cube]
      for t in TETS: conn.append([c[q] for q in t])
conn=np.asarray(conn)
cen=nodes[conn-1].mean(1)
x,y,z=cen.T
rng=np.random.default_rng(1)
fixed=((x<-32.5)&(np.abs(y)<9)&(z>21.5)&(z<24))|((x>-53)&(x<-40)&(np.abs(y)<8)&(z>0)&(z<2))
rho=np.where(fixed,1.0,rng.uniform(0.02,0.3,len(x)))
blob=(~fixed)&(np.hypot(x+40,y-6)<2.5)&(z>12)&(z<20)          # leftover inside the clean box (to be cleaned)
rho[blob]=0.85
wall=(~fixed)&(x>-22)
rho[wall]=0.9                                                     # outside the clean box: kept by the threshold
pickle.dump(dict(nodes=nodes,conn=conn,rho=rho,fixed=fixed),open('mesh.pkl','wb'))
print(len(nodes),'nodes',len(conn),'tets, fixed',fixed.sum(),'blob',blob.sum())
# distribution file and model deck
with open('tosca_distribution.inp','w') as f:
  for nm in ('Stiffness','Mass'):
    f.write('*DISTRIBUTION TABLE, NAME=__SMATso_Distribution_%s_1_FMT_\n  RATIO,RATIO\n*DISTRIBUTION, DESIGN VARIABLE, LOCATION=ELEMENT, NAME=__SMATso_Distribution_%s_1, TABLE=__SMATso_Distribution_%s_1_FMT_\n , 1., 1.\n'%(nm,nm,nm))
    for l in range(1,len(conn)+1): f.write('%d, %.6e, %.6e\n'%(l,1.0,998.5))
open('TO_v04B_r4_H4-Job.inp','w').write('*Include, input=tosca_distribution.inp\n*Tie, name=TIE_LIDRIM, adjust=no\nTUB-1_S_RIM, LID-1_S_LID\n*Step\n*Frequency\n20, , , , ,\n*DESIGN RESPONSE, name=R1\n*GLOBALRESPONSE\nALLSE\n*End Step\n')
