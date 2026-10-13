# fig_r4_keel_variants.py - build log item 54: rear of the rev 4 TUB, optimised iso 0.4 against the TH geometries of
# variants S and L (iso_mt.py with ISO_DIST). Usage: python3 fig_r4_keel_variants.py <opt_040.stl> <S_050.stl> <L_050.stl>
import sys
import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components


def load(fn):
    d=open(fn,'rb').read(); n=np.frombuffer(d[80:84],'<u4')[0]
    return np.frombuffer(d[84:84+50*n],dtype=[('n','<f4',3),('v','<f4',(3,3)),('a','<u2')])['v'].astype(float)
def section(T, axis, c):
    # oriented section segments of a closed outward-oriented mesh by plane coord[axis]=c
    d=T[:,:,axis]-c; s=np.sign(d); s[s==0]=1e-9
    m=(s.min(1)<0)&(s.max(1)>0); T=T[m]; d=d[m]
    segs=[]
    for t,dd in zip(T,d):
        pts=[]
        for i in range(3):
            j=(i+1)%3
            if (dd[i]<0)!=(dd[j]<0):
                a=dd[i]/(dd[i]-dd[j]); pts.append(t[i]+a*(t[j]-t[i]))
        if len(pts)==2:
            n=np.cross(t[1]-t[0],t[2]-t[0]); e=np.zeros(3); e[axis]=1
            p,q=pts
            if np.dot(np.cross(e,q-p),n)<0: p,q=q,p
            segs.append((p,q))
    return segs
def area(segs, axis):
    o=[k for k in range(3) if k!=axis]
    A=0.0
    for p,q in segs: A+=p[o[0]]*q[o[1]]-q[o[0]]*p[o[1]]
    return A/2
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

M=dict(zip(['optimised, iso 0.4', 'S: side webs (TH pass)', 'L: local iso 0.15 (TH fail)'], sys.argv[1:4]))
G={k:load(v) for k,v in M.items()}
col=['#888888','#2e7d32','#c62828']
cuts=[(1,0.0,'side section y = 0'),(1,8.0,'side section y = +8'),(0,-47.0,'cross section x = -47'),(0,-38.0,'cross section x = -38'),(2,12.0,'plan section z = 12')]
fig,ax=plt.subplots(3,5,figsize=(22,13))
for r,(name,T) in enumerate(G.items()):
    for c,(axis,v,lab) in enumerate(cuts):
        a=ax[r,c]; o=[i for i in range(3) if i!=axis]
        sg=section(T,axis,v)
        if sg: a.add_collection(LineCollection([[(p[o[0]],p[o[1]]),(q[o[0]],q[o[1]])] for p,q in sg],colors=col[r],linewidths=1.0))
        if axis==1: a.set_xlim(-58,-15); a.set_ylim(-16,28); a.axhline(21.5,color='k',lw=.4,ls=':')
        elif axis==0: a.set_xlim(-14,14); a.set_ylim(-16,28); a.axhline(21.5,color='k',lw=.4,ls=':')
        else: a.set_xlim(-58,-15); a.set_ylim(-16,16)
        a.set_aspect('equal'); a.grid(alpha=.3); a.set_title('%s | %s'%(name,lab),fontsize=9)
plt.tight_layout(); plt.savefig('fig_r4_keel_variants_sections.png',dpi=95)
fig=plt.figure(figsize=(20,7))
for k,(name,T) in enumerate(G.items()):
    c=T.mean(1); m=(c[:,0]<-20)&(c[:,0]>-56)&(np.abs(c[:,1])<15)
    a=fig.add_subplot(1,3,k+1,projection='3d')
    a.add_collection3d(Poly3DCollection(T[m],facecolors=col[k],linewidths=0,alpha=.9,shade=True,lightsource=matplotlib.colors.LightSource(315,35)))
    a.set_xlim(-56,-20);a.set_ylim(-18,18);a.set_zlim(-16,28);a.set_box_aspect((36,36,44));a.view_init(12,-125)
    a.set_title(name,fontsize=11); a.set_xlabel('x');a.set_ylabel('y');a.set_zlabel('z')
fig.suptitle('Rear of the TUB (x -56 to -20), view from below-rear-left: GPS deck on top, antenna spine at the bottom',fontsize=12)
plt.tight_layout(); plt.savefig('fig_r4_keel_variants_3d.png',dpi=95)
