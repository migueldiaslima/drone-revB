# capacity_r4.py - Stage 7 geometric capacity checks on the iso 0.3 print set (build log item 66):
#   D-050: arm section modulus for up-down bending at the fork exit (u about 50 mm) at most 260 mm^3
#   D-051: TUB fin-root section modulus (up-down) at least 390 mm^3 (1.5 x the arm limit)
# u = distance from the frame centre along the corner diagonal (x = y = u / sqrt 2 for pp); sections normal to the
# diagonal. Up-down bending: about the horizontal axis w (normal to the diagonal, in plane), so
#   I = integral (z - z_c)^2 dA,  Z = I / max |z - z_c|
# Section properties from the exact polygons of a manifold3d slice (Green's theorem), all pieces of the cut.
# For the TUB only the part of the cut with abs(w) <= W_FIN is taken (the fin; the body lies further out in w).
# Run in the set-up workspace (python3, numpy, manifold3d):
#   python3 capacity_r4.py <print_ARM_pp_r4_iso030.stl> <print_TUB_r4_iso030.stl>
# ASCII only.
from __future__ import print_function
import sys, struct
import numpy as np
from manifold3d import Manifold, Mesh

W_FIN = 8.0       # mm, half width of the strip around the diagonal taken as the fin in the TUB cut
ARM_LIMIT, FIN_LIMIT = 260.0, 390.0


def read_stl(fn):
    d = open(fn, 'rb').read()
    n = struct.unpack('<I', d[80:84])[0]
    return np.frombuffer(d[84:84 + 50 * n], dtype=[('n', '<f4', 3), ('v', '<f4', (3, 3)), ('a', '<u2')])['v'].astype(float)


def to_manifold(T):
    P = T.reshape(-1, 3)
    _, idx, inv = np.unique(np.round(P / 1e-5).astype(np.int64), axis=0, return_index=True, return_inverse=True)
    F = inv.reshape(-1, 3)
    m = Manifold(Mesh(vert_properties=P[idx].astype(np.float32), tri_verts=F.astype(np.uint32)))
    st = str(m.status())
    if 'NoError' not in st:
        raise SystemExit('not a closed manifold (%s)' % st)
    return m


def props(polys, wlim=None):
    """area, centroid z, I about the centroidal horizontal axis, max fibre distance; polygons in (w, z)"""
    A = Sz = Szz = 0.0
    zs = []
    for P in polys:
        P = np.asarray(P, dtype=float)
        if wlim is not None:
            if np.abs(P[:, 0]).max() > wlim:          # piece reaching beyond the strip: not the fin
                continue
        w, z = P[:, 0], P[:, 1]
        w2, z2 = np.roll(w, -1), np.roll(z, -1)
        c = w * z2 - w2 * z
        A += c.sum() / 2.0
        Sz += ((z + z2) * c).sum() / 6.0
        Szz += ((z * z + z * z2 + z2 * z2) * c).sum() / 12.0
        zs.append(z)
    if abs(A) < 1e-9:
        return None
    zc = Sz / A
    I = Szz - A * zc * zc
    c = np.abs(np.concatenate(zs) - zc).max()
    return abs(A), zc, abs(I), c


if __name__ == '__main__':
    arm_fn, tub_fn = sys.argv[1], sys.argv[2]
    res = {}
    for name, fn, us, wlim in (('ARM_pp', arm_fn, np.arange(45.0, 55.01, 1.0), None),
                               ('TUB fin', tub_fn, np.arange(20.0, 40.01, 1.0), W_FIN)):
        m = to_manifold(read_stl(fn))
        r = m.rotate((0.0, 0.0, -45.0))         # pp diagonal onto +x; w = y
        b = r.bounding_box()
        print('%s: volume %.1f mm^3, rotated bbox x %.1f..%.1f (u), y %.1f..%.1f (w), z %.1f..%.1f' % (
            name, r.volume() if hasattr(r, 'volume') else r.get_volume(), b[0], b[3], b[1], b[4], b[2], b[5]))
        # slice planes x = u: rotate so x becomes the slicing axis z'
        rr = r.rotate((0.0, 90.0, 0.0))         # about y by +90: x -> -z', z -> x'
        rows = []
        for u in us:
            cs = rr.slice(-u)
            polys = cs.to_polygons()
            # in rr: x' = z (up), y' = w; take (w, z) = (y', x')
            pw = [np.c_[np.asarray(P)[:, 1], np.asarray(P)[:, 0]] for P in polys]
            p = props(pw, wlim)
            if p is None:
                rows.append((u, 0, 0, 0, 0, 0))
                continue
            A, zc, I, c = p
            rows.append((u, A, zc, I, c, I / c))
        res[name] = rows
        print('  u (mm)   area mm^2   z_c mm   I mm^4      c mm   Z mm^3')
        for u, A, zc, I, c, Z in rows:
            print('  %5.1f  %9.2f  %7.2f  %9.1f  %6.2f  %7.1f' % (u, A, zc, I, c, Z))
    a = dict((round(r[0], 1), r[5]) for r in res['ARM_pp'])
    z50 = a.get(50.0)
    print('D-050 arm at the fork exit (u 50): Z = %.1f mm^3, limit <= %.0f -> %s' % (z50, ARM_LIMIT, 'PASS' if z50 <= ARM_LIMIT else 'CHECK'))
    near = [r[5] for r in res['ARM_pp'] if 45.0 <= r[0] <= 55.0 and r[5] > 0]
    print('   u 45 to 55: Z %.1f to %.1f mm^3' % (min(near), max(near)))
