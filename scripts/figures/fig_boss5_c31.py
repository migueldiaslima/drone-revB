# fig_boss5_c31.py - build log item 47: shells of the smoothed TUB iso surface (iso_mt.py ... TUB) of H4 cycle 31,
# gap from the keel lid boss shell to the main tub, and the rear views. Usage: python3 fig_boss5_c31.py mt_c31_TUB_040.stl mt_c31_TUB_030.stl
import numpy as np, sys
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
from scipy.spatial import cKDTree

F=dict((a.rsplit('_', 1)[-1].replace('.stl', ''), a) for a in sys.argv[1:])
def load(fn):
    d=open(fn,'rb').read(); n=np.frombuffer(d[80:84],'<u4')[0]
    rec=np.frombuffer(d[84:84+50*n],dtype=[('n','<f4',3),('v','<f4',(3,3)),('a','<u2')])
    return rec['v'].astype(float)
for tag,fn in F.items():
    T=load(fn); P=T.reshape(-1,3)
    key=np.round(P*1e4).astype(np.int64)
    u,inv=np.unique(key,axis=0,return_inverse=True); inv=inv.ravel()
    V=u/1e4; tri=inv.reshape(-1,3)
    e=np.vstack([tri[:,[0,1]],tri[:,[1,2]],tri[:,[2,0]]])
    g=coo_matrix((np.ones(len(e)),(e[:,0],e[:,1])),shape=(len(V),)*2)
    nc,lab=connected_components(g,directed=False)
    tl=lab[tri[:,0]]
    def vol(m):
        t=V[tri[m]]; return np.einsum('ij,ij->i',t[:,0],np.cross(t[:,1],t[:,2])).sum()/6
    comps=[]
    for c in range(nc):
        m=tl==c; comps.append((abs(vol(m)),c,m.sum()))
    comps.sort(reverse=True)
    print('== iso',tag,'triangles',len(tri),'shells',nc)
    for v,c,nt in comps[:6]:
        vv=V[np.unique(tri[tl==c])]
        print('  shell %d: %8.1f mm3, %6d tris, bbox x %.1f..%.1f y %.1f..%.1f z %.1f..%.1f'%(c,v,nt,*[x for p in zip(vv.min(0),vv.max(0)) for x in p]))
    # boss shell
    d=np.linalg.norm(V-np.array([-30,0,21.5]),axis=1); bc=lab[np.argmin(d)]
    main=comps[0][1]
    print('  boss 5 vertex nearest (-30,0,21.5) in shell',bc,'(main shell %d)'%main)
    if bc!=main:
        A=V[lab==bc]; B=V[lab==main]; t=cKDTree(B); dd,ii=t.query(A)
        k=np.argmin(dd); print('  min gap boss shell to main shell %.3f mm, at boss point (%.2f, %.2f, %.2f) / main (%.2f, %.2f, %.2f)'%(dd[k],*A[k],*B[ii[k]]))
    np.savez('sh_%s.npz'%tag,V=V,tri=tri,lab=lab,bc=bc,main=main)
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
fig=plt.figure(figsize=(15,10))
for r,tag in enumerate(['040','030']):
    d=np.load('sh_%s.npz'%tag); V,tri,lab,bc,main=d['V'],d['tri'],d['lab'],int(d['bc']),int(d['main'])
    T=V[tri]; c=T.mean(1); tl=lab[tri[:,0]]
    box=(c[:,0]<-14)&(c[:,0]>-50)&(np.abs(c[:,1])<14)
    for k,(el,az,ttl) in enumerate([(25,-60,'iso view from rear left'),(0,-90,'side view (x-z), from -y'),(90,-90,'top view (x-y)')]):
        ax=fig.add_subplot(2,3,r*3+k+1,projection='3d')
        for m,col in [(box&(tl==main),'#9aa7b4'),(box&(tl==bc),'#d9534f'),(box&(tl!=main)&(tl!=bc),'#f0ad4e')]:
            pc=Poly3DCollection(T[m],facecolor=col,edgecolor='none',alpha=1.0 if col!='#9aa7b4' else 0.55); ax.add_collection3d(pc)
        ax.set_xlim(-50,-14);ax.set_ylim(-18,18);ax.set_zlim(-16,22);ax.set_box_aspect((36,36,38))
        ax.view_init(el,az);ax.set_xlabel('x');ax.set_ylabel('y');ax.set_zlabel('z')
        ax.set_title('iso 0.%s: %s'%(tag[1:],ttl),fontsize=10)
fig.suptitle('H4 cycle 31, TUB only, smoothed iso surface, rear part (x -50 to -14). Red: keel lid boss 5 shell; orange: other loose shells (antenna boss); grey: main tub',fontsize=11)
plt.tight_layout(); plt.savefig('fig_boss5_c31.png',dpi=110)
