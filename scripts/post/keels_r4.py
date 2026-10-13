# keels_r4.py - rev 4 keel proposals under the GPS deck (build log item 55, note docs/stage6_v04B_r4_keel_note.md).
# One definition used for the preview STLs (python3) and for the TH element selection (abaqus python, py2):
#   A : twin tapered keels hanging from the deck underside (Miguel's sketch, 2026-10-13)
#   B : web under the antenna tunnel, down to the keel underside z 0 (the part inside the design space; the
#       extension down the rear wall face below z 0 is print geometry only, see the note)
# All in model coordinates (mm). Clipped by the prop sweep + 3 mm (z 10 to 21.5), K8, K9 and the keel envelope.
# Preview:  python3 keels_r4.py [outdir]   -> keel_A_preview.stl, keel_B_preview.stl (0.25 mm voxels)
from __future__ import print_function
import sys, struct
import numpy as np

M, RK = 52.5, 47.45                      # rear motor axes (+-52.5, -52.5 ... ), prop radius + 3 mm


def keep_y(x):
    d = RK * RK - (x + M) ** 2
    return M - np.sqrt(np.maximum(d, 0.0))


def _a_outline():
    xo = np.linspace(-50.0, -22.0, 57)
    outer = [(x, min(9.0, keep_y(x)) if x < -24.5 else 9.0) for x in xo] + [(-23.0, 11.0), (-22.0, 12.5)]
    inner = [(-22.0, 0.0), (-23.0, 2.6), (-24.5, 4.0), (-26.0, 4.8), (-27.0, 5.0), (-50.0, 5.0)]
    return np.asarray(outer + inner, dtype=float)


A_OUT = _a_outline()


def in_poly(x, y, poly):
    # even-odd ray casting, vectorised over x, y (arrays of equal shape)
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    ins = np.zeros(x.shape, dtype=bool)
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        if y1 == y2:
            continue
        c = ((y1 > y) != (y2 > y)) & (x < (x2 - x1) * (y - y1) / (y2 - y1) + x1)
        ins ^= c
    return ins


def a_zbot(x):
    # keel bottom: deck underside (z 21.5) at x -50, z 10 at the rear wall x -22, slightly concave
    t = np.clip((np.asarray(x, dtype=float) + 50.0) / 28.0, 0.0, 1.0)
    return 21.5 - 11.5 * (0.6 * t + 0.4 * t * t)


def voids(x, y, z):
    x, y, z = [np.asarray(v, dtype=float) for v in (x, y, z)]
    ok = np.ones(x.shape, dtype=bool)
    ok &= ~((z >= 3.0) & (np.hypot(x + 38.2, y + 3.0) <= 2.0))                                   # K9 vertical
    r = np.sqrt(np.maximum(0.0, 4.0 - (z - 5.0) ** 2))
    ok &= ~((z >= 3.0) & (z <= 7.0) & (x > -38.2) & (np.abs(y + 3.0) <= r))                      # K9 leg
    r = np.sqrt(np.maximum(0.0, 1.75 ** 2 - (z - 6.5) ** 2))
    ok &= ~((z >= 4.75) & (z <= 8.25) & (x > -42.0) & (np.abs(y - 3.5) <= r))                    # K8
    prop = (z >= 10.0) & (z <= 21.5) & ((np.hypot(x + M, y - M) < RK) | (np.hypot(x + M, y + M) < RK))
    ok &= ~prop
    return ok


def in_A(x, y, z):
    x, y, z = [np.asarray(v, dtype=float) for v in (x, y, z)]
    env = (z <= 21.5) & (z >= a_zbot(x)) & ((np.abs(y) <= 9.0) | (x > -24.5)) & (x >= -50.0) & (x <= -22.0)
    plan = in_poly(x, np.abs(y), A_OUT)
    return env & plan & voids(x, y, z)


B_Y, B_X, B_ZTOP = (2.5, 4.5), (-40.0, -22.0), 3.25


def b_zbot(x):
    t = np.clip((np.asarray(x, dtype=float) + 40.0) / 14.0, 0.0, 1.0)
    return 3.25 * (1.0 - t) ** 1.5


def in_B(x, y, z):
    x, y, z = [np.asarray(v, dtype=float) for v in (x, y, z)]
    m = (y >= B_Y[0]) & (y <= B_Y[1]) & (x >= B_X[0]) & (x <= B_X[1]) & (z <= B_ZTOP) & (z >= b_zbot(x)) & (z >= 0.0)
    return m & voids(x, y, z)


SHAPES = {'A': in_A, 'B': in_B}


def voxel_stl(fn, mask, x0, y0, z0, h):
    nx, ny, nz = mask.shape
    pad = np.zeros((nx + 2, ny + 2, nz + 2), dtype=bool)
    pad[1:-1, 1:-1, 1:-1] = mask
    tris = []
    for ax in range(3):
        for sgn in (-1, 1):
            nb = np.roll(pad, -sgn, axis=ax)
            face = pad & ~nb
            idx = np.argwhere(face[1:-1, 1:-1, 1:-1])
            if not len(idx):
                continue
            p = np.c_[x0 + idx[:, 0] * h, y0 + idx[:, 1] * h, z0 + idx[:, 2] * h]
            off = np.zeros(3)
            off[ax] = h if sgn > 0 else 0.0
            u, v = [k for k in range(3) if k != ax]
            du = np.zeros(3); du[u] = h
            dv = np.zeros(3); dv[v] = h
            a = p + off
            b, c, d = a + du, a + du + dv, a + dv
            if (sgn > 0) == ((u, v) in ((0, 1), (1, 2), (2, 0))):
                tris += [np.stack([a, b, c], 1), np.stack([a, c, d], 1)]
            else:
                tris += [np.stack([a, c, b], 1), np.stack([a, d, c], 1)]
    t = np.concatenate(tris, 0)
    n = np.cross(t[:, 1] - t[:, 0], t[:, 2] - t[:, 0])
    n /= np.maximum(np.linalg.norm(n, axis=1)[:, None], 1e-12)
    rec = np.zeros(len(t), dtype=[('n', '<f4', 3), ('v', '<f4', (3, 3)), ('a', '<u2')])
    rec['n'] = n
    rec['v'] = t
    with open(fn, 'wb') as f:
        f.write(b'keels_r4 preview (voxels)'.ljust(80, b' '))
        f.write(struct.pack('<I', len(t)))
        f.write(rec.tobytes())
    return len(t)


if __name__ == '__main__':
    out = sys.argv[1] if len(sys.argv) > 1 else '.'
    h = 0.25
    x0, y0, z0 = -56.0, -16.0, 0.0
    xs = x0 + h / 2 + np.arange(int(36 / h)) * h
    ys = y0 + h / 2 + np.arange(int(32 / h)) * h
    zs = z0 + h / 2 + np.arange(int(21.5 / h)) * h
    X, Y, Z = np.meshgrid(xs, ys, zs, indexing='ij')
    for k, fn in SHAPES.items():
        m = fn(X, Y, Z)
        v = m.sum() * h ** 3
        nt = voxel_stl('%s/keel_%s_preview.stl' % (out, k), m, x0, y0, z0, h)
        print('%s: %.0f mm^3 = %.2f g (1.30e-3 g/mm^3), %d triangles -> keel_%s_preview.stl' % (k, v, v * 1.30e-3, nt, k))
