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


U_M = 52.5 * 2 ** 0.5        # motor axis (52.5, 52.5) on the diagonal (D-079; motor pad centroid in ARM_pp.step u 74.24)
U_J = 33.0 + 3.0 * 2 ** 0.5  # J3 bolt line: 33 mm in v03 (F-9) moved out 3 mm in x and y by D-079 (prong boss centroids u 37.4 to 37.5)
U_SLOT = 34.35 + 3.0 * 2 ** 0.5 + 5.15   # slot-end semicircle: centre 34.35 (v03, F-9) + D-079, radius 5.15 (D-048); checked on the STL
S_XY, M_JOINT = 54.4, 21216.0             # MPa (N-05-03), joint vertical moment capacity N mm (N-06-04)


def profile(rr, us, wlim):
    rows = []
    for u in us:
        polys = rr.slice(-u).to_polygons()
        pw = [np.c_[np.asarray(P)[:, 1], np.asarray(P)[:, 0]] for P in polys]
        p = props(pw, wlim)
        if p is None:
            rows.append((u, 0.0, 0.0, 0.0, 0.0, 0.0))
            continue
        A, zc, I, c = p
        rows.append((u, A, zc, I, c, I / c))
    return rows


def show(rows, extra=None):
    print('  u (mm)   area mm^2   z_c mm   I mm^4      c mm   Z mm^3' + ('   Z / (u_m - u) mm^2' if extra else ''))
    for r in rows:
        u, A, zc, I, c, Z = r
        print('  %5.2f  %9.2f  %7.2f  %9.1f  %6.2f  %7.1f' % (u, A, zc, I, c, Z) + ('   %8.2f' % (Z / (U_M - u)) if extra else ''))


if __name__ == '__main__':
    arm_fn, tub_fn = sys.argv[1], sys.argv[2]
    arm = to_manifold(read_stl(arm_fn)).rotate((0.0, 0.0, -45.0)).rotate((0.0, 90.0, 0.0))
    tub = to_manifold(read_stl(tub_fn)).rotate((0.0, 0.0, -45.0)).rotate((0.0, 90.0, 0.0))
    print('u from the frame centre along the pp diagonal; motor axis u_m %.2f, bolt line u_j %.2f, slot end u %.2f' % (U_M, U_J, U_SLOT))
    print('ARM_pp, D-050 (Z <= %.0f mm^3), u 45 to 55:' % ARM_LIMIT)
    r1 = profile(arm, np.arange(45.0, 55.01, 1.0), None)
    show(r1)
    rs = profile(arm, [U_SLOT, 54.0], None)
    print('ARM_pp at the slot end (fork exit) and at u 54:')
    show(rs)
    print('D-050 at the fork exit u %.2f: Z = %.1f mm^3 -> %s' % (U_SLOT, rs[0][5], 'PASS' if rs[0][5] <= ARM_LIMIT else 'NOT MET'))
    print('ARM_pp, lever-corrected Z / (u_m - u), u 45 to 72:')
    r2 = profile(arm, np.arange(45.0, 72.01, 1.0), None)
    show(r2, extra=True)
    k = min(range(len(r2)), key=lambda i: r2[i][5] / (U_M - r2[i][0]))
    q = r2[k][5] / (U_M - r2[k][0])
    ratio = S_XY * q * (U_M - U_J) / M_JOINT
    print('minimum Z / (u_m - u) = %.2f mm^2 at u %.1f (Z %.1f mm^3, lever %.2f mm)' % (q, r2[k][0], r2[k][5], U_M - r2[k][0]))
    print('arm-to-joint failure force ratio = S_xy x min[Z / (u_m - u)] x (u_m - u_j) / M_joint = %.1f x %.2f x %.2f / %.0f = %.2f' % (
        S_XY, q, U_M - U_J, M_JOINT, ratio))
    print('  (tip force to fail the arm / tip force to fail the joint; above 1: the joint fails first)')
    print('TUB fin, D-051 (Z >= %.0f mm^3), cut restricted to abs(w) <= %.0f mm, u 25 to 33:' % (FIN_LIMIT, W_FIN))
    r3 = profile(tub, np.arange(25.0, 33.01, 0.5), W_FIN)
    show(r3)
