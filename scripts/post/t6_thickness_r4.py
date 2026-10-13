# T-6 wall thickness of the restored rev 4 print set: (1) sphere method (local thickness, Hildebrand and
# Rueegsegger 1997): a point is thinner than t if no ball of diameter t inside the solid contains it, evaluated
# by morphological opening on a voxel grid; (2) ray method: from each surface triangle centroid along the inward
# normal to the opposite surface. Also: connected shells (fragments dropped) and cleaned STLs.
import sys, struct, json, numpy as np
from scipy import ndimage
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
TH = (0.8, 1.2, 2.0, 2.5)
def read_stl(fn):
    d=open(fn,'rb').read(); n=struct.unpack('<I',d[80:84])[0]
    return np.frombuffer(d[84:84+50*n],dtype=[('n','<f4',3),('v','<f4',(3,3)),('a','<u2')])['v'].astype(float)
def write_stl(fn,T):
    n=np.cross(T[:,1]-T[:,0],T[:,2]-T[:,0]); n/=np.maximum(np.linalg.norm(n,axis=1)[:,None],1e-12)
    rec=np.zeros(len(T),dtype=[('n','<f4',3),('v','<f4',(3,3)),('a','<u2')]); rec['n']=n; rec['v']=T
    with open(fn,'wb') as f: f.write(b'rev 4 print set, fragments removed'.ljust(80,b' ')); f.write(struct.pack('<I',len(T))); f.write(rec.tobytes())
def shells(T):
    P=T.reshape(-1,3); key=np.round(P*1e5).astype(np.int64)
    _,inv=np.unique(key,axis=0,return_inverse=True); F=inv.reshape(-1,3)
    e=np.vstack([F[:,[0,1]],F[:,[1,2]]]); g=coo_matrix((np.ones(len(e)),(e[:,0],e[:,1])),shape=(inv.max()+1,)*2)
    nc,lab=connected_components(g,directed=False); tl=lab[F[:,0]]
    v=np.bincount(tl,weights=np.einsum('ij,ij->i',T[:,0],np.cross(T[:,1],T[:,2]))/6,minlength=nc)
    return tl,v
def voxelize(T,h):
    lo=T.reshape(-1,3).min(0)-2*h; hi=T.reshape(-1,3).max(0)+2*h
    n=np.ceil((hi-lo)/h).astype(int)
    xs=lo[0]+(np.arange(n[0])+0.5)*h+1.3e-7; ys=lo[1]+(np.arange(n[1])+0.5)*h+1.7e-7
    zc=lo[2]+(np.arange(n[2])+0.5)*h
    # z crossings of the column (x, y) through each triangle (parity fill)
    a,b,c=T[:,0],T[:,1],T[:,2]
    i0=np.clip(np.floor((T[:,:,0].min(1)-xs[0])/h).astype(int),0,n[0]-1); i1=np.clip(np.ceil((T[:,:,0].max(1)-xs[0])/h).astype(int),0,n[0]-1)
    j0=np.clip(np.floor((T[:,:,1].min(1)-ys[0])/h).astype(int),0,n[1]-1); j1=np.clip(np.ceil((T[:,:,1].max(1)-ys[0])/h).astype(int),0,n[1]-1)
    di=(i1-i0).max()+1; dj=(j1-j0).max()+1
    cols=[]; zs=[]
    den=(b[:,1]-c[:,1])*(a[:,0]-c[:,0])+(c[:,0]-b[:,0])*(a[:,1]-c[:,1])
    ok=np.abs(den)>1e-14
    for oi in range(di):
        for oj in range(dj):
            ii=i0+oi; jj=j0+oj; m=ok&(ii<=i1)&(jj<=j1)
            if not m.any(): continue
            x=xs[ii[m]]; y=ys[jj[m]]; A,B,C,D=a[m],b[m],c[m],den[m]
            l1=((B[:,1]-C[:,1])*(x-C[:,0])+(C[:,0]-B[:,0])*(y-C[:,1]))/D
            l2=((C[:,1]-A[:,1])*(x-C[:,0])+(A[:,0]-C[:,0])*(y-C[:,1]))/D
            l3=1-l1-l2; inside=(l1>=0)&(l2>=0)&(l3>=0)
            z=l1*A[:,2]+l2*B[:,2]+l3*C[:,2]
            cols.append((ii[m][inside]*n[1]+jj[m][inside])); zs.append(z[inside])
    cols=np.concatenate(cols); zs=np.concatenate(zs)
    o=np.lexsort((zs,cols)); cols,zs=cols[o],zs[o]
    vox=np.zeros(n,dtype=bool)
    st=np.r_[0,np.nonzero(np.diff(cols))[0]+1,len(cols)]
    odd=0
    for s,e in zip(st[:-1],st[1:]):
        cz=zs[s:e]
        if len(cz)%2: odd+=1; cz=cz[:-1]
        i,j=divmod(int(cols[s]),n[1])
        for k in range(0,len(cz),2):
            k0=int(np.ceil((cz[k]-zc[0])/h)); k1=int(np.floor((cz[k+1]-zc[0])/h))
            if k1>=k0: vox[i,j,max(k0,0):min(k1,n[2]-1)+1]=True
    return vox,lo,h,odd
def sphere_method(vox,h):
    d=ndimage.distance_transform_edt(vox)*h               # distance to the outside, mm
    surf=vox&~ndimage.binary_erosion(vox)
    res={}; thinmask={}
    for t in TH:
        r=t/2.0
        core=d>=r
        cov=ndimage.distance_transform_edt(~core)*h<=r     # within r of a centre deep enough: inside a ball of diameter t
        thin=vox&~cov
        res[t]=(float(thin[surf].mean()),float(thin.sum()/vox.sum()))
        thinmask[t]=thin
    return res,surf,thinmask
def ray_method(T,vox,lo,h,maxd=12.0):
    c=T.mean(1); nrm=np.cross(T[:,1]-T[:,0],T[:,2]-T[:,0]); ar=np.linalg.norm(nrm,axis=1)/2; nrm/=np.maximum(2*ar[:,None],1e-12)
    p=c-nrm*0.5*h; th=np.full(len(c),np.nan); alive=np.ones(len(c),bool); step=0.25*h; s=0.0
    nmax=int(maxd/step)
    for k in range(nmax):
        s+=step; q=p-nrm*s; idx=np.floor((q-lo)/h).astype(int)
        inb=np.all((idx>=0)&(idx<np.array(vox.shape)),axis=1)
        val=np.zeros(len(c),bool); val[inb]=vox[idx[inb,0],idx[inb,1],idx[inb,2]]
        hit=alive&~val; th[hit]=s+0.5*h; alive&=val
        if not alive.any(): break
    th[np.isnan(th)]=maxd
    return th,ar
if __name__=='__main__':
    out={}
    for name,fn,h in [(a.split('=')[0],a.split('=')[1],float(a.split('=')[2])) for a in sys.argv[1:]]:
        T=read_stl(fn); tl,v=shells(T); keep=np.nonzero(v>0.01)[0]
        Tk=T[np.isin(tl,keep)]
        write_stl('print_%s_r4.stl'%name,Tk)
        vox,lo,hh,odd=voxelize(Tk,h)
        sp,surf,thin=sphere_method(vox,h)
        th,ar=ray_method(Tk,vox,lo,h)
        rr={t:float(ar[th<t].sum()/ar.sum()) for t in TH}
        out[name]=dict(shells=len(v),kept=len(keep),dropped_vol=float(v[v<=0.01].sum()),volume=float(v[keep].sum()),voxel=h,
                       vox_volume=float(vox.sum()*h**3),odd_columns=odd,sphere_surface={str(t):sp[t][0] for t in TH},
                       sphere_volume={str(t):sp[t][1] for t in TH},ray_surface={str(t):rr[t] for t in TH},
                       ray_median=float(np.median(th)))
        np.savez_compressed('t6_%s.npz'%name,vox=vox,lo=lo,h=h,thin08=thin[0.8],thin12=thin[1.2],surf=surf,th=th,ar=ar)
        o=out[name]
        print('%s: %d shells, kept %d (dropped %.4f mm^3), volume %.1f mm^3 (voxels %.1f, h %.2f, odd columns %d)'%(name,o['shells'],o['kept'],o['dropped_vol'],o['volume'],o['vox_volume'],h,odd))
        print('   sphere method, surface share below 0.8 / 1.2 / 2.0 / 2.5 mm: %s %%; volume share: %s %%'%(' / '.join('%.2f'%(100*sp[t][0]) for t in TH),' / '.join('%.2f'%(100*sp[t][1]) for t in TH)))
        print('   ray method,    surface share below 0.8 / 1.2 / 2.0 / 2.5 mm: %s %%; median %.2f mm'%(' / '.join('%.2f'%(100*rr[t]) for t in TH),o['ray_median']))
    json.dump(out,open('t6.json','w'),indent=1)
