# T-6 thickness maps of the rev 4 print set (build log item 61). Usage: python3 fig_t6_r4.py <TUB|LID|ARM_pp> x (after t6_thickness_r4.py)
import numpy as np, sys, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
sys.argv=[sys.argv[0]]+sys.argv[1:]
exec(open('t6_thickness_r4.py').read().split("if __name__")[0])
name,fn=sys.argv[1],sys.argv[2]
T=read_stl('print_%s_r4.stl'%name); D=np.load('t6_%s.npz'%name); th=D['th']; ar=D['ar']
c=T.mean(1)
fig,ax=plt.subplots(1,3,figsize=(21,7))
for a,(i,j,lab) in zip(ax,[(0,1,'plan (x-y)'),(0,2,'side (x-z)'),(1,2,'front (y-z)')]):
    a.scatter(c[:,i],c[:,j],s=0.2,c='#cccccc',rasterized=True)
    m2=(th<1.2)&(th>=0.8); m1=th<0.8
    a.scatter(c[m2,i],c[m2,j],s=2,c='#f0ad4e',label='ray thickness 0.8 to 1.2 mm',rasterized=True)
    a.scatter(c[m1,i],c[m1,j],s=3,c='#d9534f',label='ray thickness below 0.8 mm',rasterized=True)
    a.set_aspect('equal'); a.grid(alpha=.3); a.set_title('%s, %s'%(name,lab)); a.legend(markerscale=6,fontsize=8,loc='upper right')
plt.tight_layout(); plt.savefig('fig_t6_%s.png'%name,dpi=80)
# cluster report: thin area by region (2 mm grid)
m=th<0.8; g=np.floor(c[m]/4.0).astype(int); keys,inv=np.unique(g,axis=0,return_inverse=True)
a=np.bincount(inv.ravel(),weights=ar[m]); o=np.argsort(-a)[:12]
print(name,'thin (<0.8 mm, ray) area %.1f of %.1f mm2; largest 4 mm cells:'%(ar[m].sum(),ar.sum()))
for k in o: print('   cell centre (%.0f, %.0f, %.0f): %.2f mm2'%(*(keys[k]*4+2),a[k]))
