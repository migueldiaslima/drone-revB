# fig_r4_deck.py - build log item 52: sections of the rev 4 H4 cycle 28 TUB iso surfaces (iso_mt.py ... TUB) at 0.3 / 0.4 / 0.5
# through the keel under the GPS deck. Usage: python3 fig_r4_deck.py mt_c28_TUB_030.stl mt_c28_TUB_040.stl mt_c28_TUB_050.stl
import sys
import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components

F=dict((a.rsplit('_', 1)[-1].replace('.stl', ''), a) for a in sys.argv[1:])
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
iso={k:load(v) for k,v in F.items()}
col={'030':'#f0ad4e','040':'#d9534f','050':'#337ab7'}
# fig 1: y-z sections at x
xs=(-53,-50,-47,-44,-41,-38,-35,-33,-30)
fig,ax=plt.subplots(2,5,figsize=(19,8)); ax=ax.ravel()
for k,x in enumerate(xs):
    a=ax[k]
    for tag in ('030','040','050'):
        sg=section(iso[tag],0,x)
        if sg: a.add_collection(LineCollection([[(p[1],p[2]),(q[1],q[2])] for p,q in sg],colors=col[tag],linewidths=1.2 if tag=='040' else 0.8))
    a.axhline(21.5,color='k',lw=0.5,ls=':'); a.set_xlim(-14,14); a.set_ylim(-16,28); a.set_aspect('equal'); a.set_title('section x = %d'%x,fontsize=10); a.grid(alpha=.3)
    a.set_xlabel('y'); a.set_ylabel('z')
a=ax[9]
for tag in ('030','040','050'): a.plot([],[],color=col[tag],label='iso 0.%s'%tag[1])
a.legend(loc='center'); a.axis('off')
a.text(0.5,0.15,'dotted: z 21.5 (keel top / deck underside)\nkeel envelope |y|<9, z 0..21.5;\ndeck x -54..-32.5, z 21.5..26.5',ha='center',transform=a.transAxes,fontsize=9)
fig.suptitle('H4 rev 4 cycle 28, TUB smoothed iso surfaces: sections through the keel under the GPS deck',fontsize=12)
plt.tight_layout(); plt.savefig('fig_r4_deck_sections.png',dpi=100)
# fig 2: x-z sections at y and x-y at z
fig,ax=plt.subplots(2,3,figsize=(19,9)); ax=ax.ravel()
for k,(axis,c,lab) in enumerate([(1,0.0,'y = 0'),(1,6.0,'y = +6'),(1,-6.0,'y = -6'),(2,5.0,'z = 5'),(2,12.0,'z = 12'),(2,19.0,'z = 19')]):
    a=ax[k]; o=[i for i in range(3) if i!=axis]
    for tag in ('030','040','050'):
        sg=section(iso[tag],axis,c)
        if sg: a.add_collection(LineCollection([[(p[o[0]],p[o[1]]),(q[o[0]],q[o[1]])] for p,q in sg],colors=col[tag],linewidths=1.2 if tag=='040' else 0.8))
    a.set_xlim(-58,-15); a.set_ylim((-16,28) if axis==1 else (-16,16)); a.set_aspect('equal'); a.grid(alpha=.3)
    a.set_title('section '+lab,fontsize=10); a.set_xlabel('x'); a.set_ylabel('z' if axis==1 else 'y')
    if axis==1: a.axhline(21.5,color='k',lw=0.5,ls=':'); a.axvline(-32.5,color='k',lw=0.5,ls=':')
for tag in ('030','040','050'): ax[0].plot([],[],color=col[tag],label='iso 0.%s'%tag[1])
ax[0].legend(loc='lower left',fontsize=8)
fig.suptitle('H4 rev 4 cycle 28, TUB: longitudinal sections (top) and plan sections (bottom), rear part; dotted: deck underside z 21.5 and deck front x -32.5',fontsize=12)
plt.tight_layout(); plt.savefig('fig_r4_deck_long.png',dpi=100)
