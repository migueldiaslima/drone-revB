# mock for stress_th.py: 3 parts on a tet grid, 4 integration points per element, analytic stress field
import numpy as np, pickle
h=1.0
xs=np.arange(0,30.1,h)+0.11; ys=np.arange(0,20.1,h)+0.07; zs=np.arange(0,10.1,h)+0.05
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
conn=np.asarray(conn); cen=nodes[conn-1].mean(1)
part=np.where(cen[:,0]<10,'TUB',np.where(cen[:,0]<20,'LID','ARM'))
rng=np.random.default_rng(3)
solid=rng.random(len(conn))<0.6
# 4 IPs per element: stress = analytic field at points between centroid and the corners
steps={}
for s,sc in (('LC1',1.0),('LC2a',0.7),('LC2b',1.3),('LC3a',2.0)):
  ip=[]
  for q in range(4):
    p=0.6*cen+0.4*nodes[conn[:,q]-1]
    x,y,z=p.T
    S=np.c_[sc*(x-5*np.sin(y)), sc*0.5*y, sc*(z-3+0.1*x), sc*0.3*x*np.cos(z), sc*0.2*y, sc*0.1*(x+y)]
    ip.append(S)
  steps[s]=np.stack(ip,1)          # n x 4 x 6
# a hot spot (outlier) in one TUB element
steps['LC3a'][5,:,0]+=400.0
pickle.dump(dict(nodes=nodes,conn=conn,part=part,solid=solid,steps=steps),open('mock.pkl','wb'))
with open('dist_mock.inp','w') as f:
  for nm,lo in (('Stiffness',1e-6),('Mass',1e-9)):
    f.write('*DISTRIBUTION TABLE, NAME=__SMATso_Distribution_%s_1_FMT_\n  RATIO,RATIO\n*DISTRIBUTION, DESIGN VARIABLE, LOCATION=ELEMENT, NAME=__SMATso_Distribution_%s_1, TABLE=__SMATso_Distribution_%s_1_FMT_\n , 1., 1.\n'%(nm,nm,nm))
    for l in range(1,len(conn)+1): f.write('%d, %.6e, %.6e\n'%(l,1.0 if solid[l-1] else lo,998.5))
print(len(conn),'elements,',solid.sum(),'solid')
