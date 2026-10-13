# analytic check: a bar 8 mm wide (w) x 20 mm deep (z) along the pp diagonal from u 25 to 75, z -12..8
# plus a 'fin' bar 6 x 16 (z -10..6) from u 15 to 45 for the TUB; Z = b d^2 / 6 (rectangle)
import numpy as np, struct
from manifold3d import Manifold
def bar(b,d,u0,u1,z0):
    m=Manifold.cube((u1-u0,b,d)).translate((u0,-b/2,z0)).rotate((0,0,45))
    return m
def wr(fn,m):
    me=m.to_mesh(); V=np.asarray(me.vert_properties)[:,:3]; F=np.asarray(me.tri_verts); T=V[F]
    with open(fn,'wb') as f:
        f.write(b'box'.ljust(80)); f.write(struct.pack('<I',len(T)))
        for t in T: f.write(struct.pack('<12fH',0,0,0,*t.ravel(),0))
wr('arm.stl',bar(8,20,25,75,-12)); wr('tub.stl',bar(6,16,15,45,-10))
print('expected Z arm 8*20^2/6 = %.1f, area 160, z_c -2.0; fin 6*16^2/6 = %.1f, area 96, z_c -2.0'%(8*400/6,6*256/6))
