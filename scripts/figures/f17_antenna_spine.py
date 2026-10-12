# -*- coding: ascii -*-
"""
f17_antenna_spine.py - concept geometry for the F-17 fix, under-keel option (2026-10-12):
one smooth fixed feature ("antenna spine") made of
  - a pad in the keel underside that takes the TPU antenna holder (M2 insert, locating hole),
  - a sleeve of 1.5 mm wall around the antenna channel K8, from its exit back to the rear wall,
  - a web up the rear wall into the rear lid boss (-21, +5), which carries the lid tie,
blended with smooth unions (blend radius K_BLEND) so the transitions are filleted, then cut by
K8, the insert hole and the locating hole, and clipped to the keel envelope and the bay face.
K9 (GPS channel) gets no fixed material; it is moved 1.5 mm towards -y so the sleeve keeps
>= 1.0 mm from it (geometry change for the generator, proposed).

Signed distance field on a grid, surface by marching tetrahedra with shared vertices, written as
figures/f17_spine_mesh.json (for docs/f17_antenna_viewer.html). Prints volume, mass and
clearances. Concept geometry from the generator parameters, not the generator itself. ASCII only.
"""
import json
import math
import os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
src = open(os.path.join(HERE, "f17_antenna_link.py")).read().split("if __name__")[0]
NS = {"__file__": os.path.join(HERE, "f17_antenna_link.py")}
exec(src, NS)
K8, R8, K9_0, R9, keel_half_width = NS["K8"], NS["R8"], NS["K9"], NS["R9"], NS["keel_half_width"]

H = 0.30               # grid step (mm)
K_BLEND = 1.6          # smooth-union radius (mm)
WALL = 1.5             # sleeve wall
K9_DY = -1.5           # proposed shift of the GPS channel
K9 = K9_0 + np.array([0.0, K9_DY, 0.0])
PAD = dict(c=(-45.75, 3.0, 2.25), half=(6.75, 5.0, 2.25), r=1.5)      # x -52.5..-39, y -2..8, z 0..4.5
INSERT = dict(xy=(-50.0, 5.0), r=1.6, z=(-1.0, 4.5))                     # M2 heat-set insert, dia 3.2 x 4.5
PEG = dict(xy=(-50.0, 0.5), r=1.0, z=(-1.0, 2.0))                         # locating hole dia 2 x 2
WEB = dict(a=(-22.3, 4.6, 8.0), b=(-21.6, 5.0, 17.0), r=1.75)
LIDB = dict(xy=(-21.0, 5.0), r=3.0, z=(15.5, 21.5))


def seg_dist(P, A, B):
    AB = B - A
    t = np.clip(((P - A) @ AB) / max(AB @ AB, 1e-12), 0.0, 1.0)
    return np.linalg.norm(P - (A + t[:, None] * AB), axis=1)


def poly_dist(P, pts):
    d = np.full(len(P), 1e9)
    for a, b in zip(pts[:-1], pts[1:]):
        d = np.minimum(d, seg_dist(P, a, b))
    return d


def smin(a, b, k):
    h = np.clip(0.5 + 0.5 * (b - a) / k, 0.0, 1.0)
    return b * (1 - h) + a * h - k * h * (1 - h)


def sd_box_round(P, c, half, r):
    q = np.abs(P - np.array(c)) - (np.array(half) - r)
    return np.linalg.norm(np.maximum(q, 0.0), axis=1) + np.minimum(q.max(axis=1), 0.0) - r


def sd_zcyl(P, xy, r, z0, z1):
    dr = np.hypot(P[:, 0] - xy[0], P[:, 1] - xy[1]) - r
    dz = np.maximum(z0 - P[:, 2], P[:, 2] - z1)
    return np.minimum(np.maximum(dr, dz), 0.0) + np.hypot(np.maximum(dr, 0.0), np.maximum(dz, 0.0))


K8_SLEEVE = K8[(K8[:, 0] <= -19.0)]


def sdf(P):
    d8 = poly_dist(P, K8_SLEEVE)
    sleeve = d8 - (R8 + WALL)
    pad = sd_box_round(P, PAD["c"], PAD["half"], PAD["r"])
    web = seg_dist(P, np.array(WEB["a"]), np.array(WEB["b"])) - WEB["r"]
    boss = sd_zcyl(P, LIDB["xy"], LIDB["r"], *LIDB["z"])
    s = smin(smin(smin(sleeve, pad, K_BLEND), web, K_BLEND), boss, K_BLEND)
    # hard clips: keel underside z >= 0, bay face x <= -20.5, keel sides, lid seat z <= 21.5
    hw = np.where(P[:, 2] < 10.0, 9.0,
                  np.minimum(9.0, NS["M"] - np.sqrt(np.maximum(NS["R_KEEP"] ** 2 - (np.abs(P[:, 0]) - NS["M"]) ** 2, 0.0))))
    s = np.maximum.reduce([s, -P[:, 2], np.minimum(P[:, 0] + 20.5, boss), np.abs(P[:, 1]) - hw, P[:, 2] - 21.5])
    # cuts: K8 channel, insert hole, locating hole
    s = np.maximum(s, -(poly_dist(P, K8) - R8))
    s = np.maximum(s, -sd_zcyl(P, INSERT["xy"], INSERT["r"], *INSERT["z"]))
    s = np.maximum(s, -sd_zcyl(P, PEG["xy"], PEG["r"], *PEG["z"]))
    return s


# ---------------- marching tetrahedra with shared vertices ----------------
TETS = np.array([[0, 5, 1, 6], [0, 1, 2, 6], [0, 2, 3, 6], [0, 3, 7, 6], [0, 7, 4, 6], [0, 4, 5, 6]])
CUBE = np.array([[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0], [0, 0, 1], [1, 0, 1], [1, 1, 1], [0, 1, 1]])


def march(F, origin, h):
    nx, ny, nz = F.shape
    gid = lambda i, j, k: (i * ny + j) * nz + k
    I, J, Kk = np.meshgrid(np.arange(nx - 1), np.arange(ny - 1), np.arange(nz - 1), indexing="ij")
    I, J, Kk = I.ravel(), J.ravel(), Kk.ravel()
    corner_ids = np.stack([gid(I + c[0], J + c[1], Kk + c[2]) for c in CUBE], axis=1)
    Ff = F.ravel()
    corner_vals = Ff[corner_ids]
    keep = (corner_vals.min(axis=1) < 0) & (corner_vals.max(axis=1) > 0)
    corner_ids = corner_ids[keep]
    tris = []
    for t in TETS:
        v = corner_ids[:, t]
        f = Ff[v]
        inside = f < 0
        n_in = inside.sum(axis=1)
        for case_n in (1, 3):
            sel = n_in == case_n
            if not sel.any():
                continue
            vv, ii = v[sel], inside[sel]
            lone = ii if case_n == 1 else ~ii
            a = vv[lone].reshape(-1)
            others = vv[~lone].reshape(-1, 3)
            tri = np.stack([np.stack([a, others[:, k]], axis=1) for k in range(3)], axis=1)
            if case_n == 3:
                tri = tri[:, ::-1]
            tris.append(tri)
        sel = n_in == 2
        if sel.any():
            vv, ii = v[sel], inside[sel]
            ins = vv[ii].reshape(-1, 2)
            out = vv[~ii].reshape(-1, 2)
            e00 = np.stack([ins[:, 0], out[:, 0]], 1); e01 = np.stack([ins[:, 0], out[:, 1]], 1)
            e10 = np.stack([ins[:, 1], out[:, 0]], 1); e11 = np.stack([ins[:, 1], out[:, 1]], 1)
            tris.append(np.stack([e00, e01, e11], 1)); tris.append(np.stack([e00, e11, e10], 1))
    E = np.concatenate(tris, axis=0)                     # (ntri, 3, 2) grid-point pairs
    pairs = np.sort(E.reshape(-1, 2), axis=1)
    key = pairs[:, 0].astype(np.int64) * (nx * ny * nz) + pairs[:, 1]
    uk, inv = np.unique(key, return_inverse=True)
    p0, p1 = uk // (nx * ny * nz), uk % (nx * ny * nz)
    f0, f1 = Ff[p0], Ff[p1]
    t = (f0 / (f0 - f1))[:, None]
    def xyz(g):
        k = g % nz; j = (g // nz) % ny; i = g // (ny * nz)
        return np.stack([i, j, k], 1) * h + origin
    V = xyz(p0) + t * (xyz(p1) - xyz(p0))
    Tri = inv.reshape(-1, 3)
    # orient triangles outward (normal along +grad f)
    c = V[Tri].mean(axis=1)
    n = np.cross(V[Tri[:, 1]] - V[Tri[:, 0]], V[Tri[:, 2]] - V[Tri[:, 0]])
    eps = 0.05
    g = np.stack([(sdf(c + eps * np.eye(3)[k]) - sdf(c - eps * np.eye(3)[k])) for k in range(3)], 1)
    flip = (n * g).sum(axis=1) < 0
    Tri[flip] = Tri[flip][:, ::-1]
    good = np.linalg.norm(n, axis=1) > 1e-10
    return V, Tri[good]


def main():
    lo = np.array([-53.5, -7.5, -0.6]); hi = np.array([-17.4, 9.5, 22.0])
    nx, ny, nz = [int(math.ceil((hi[i] - lo[i]) / H)) + 1 for i in range(3)]
    X, Y, Z = np.meshgrid(lo[0] + H * np.arange(nx), lo[1] + H * np.arange(ny), lo[2] + H * np.arange(nz), indexing="ij")
    P = np.c_[X.ravel(), Y.ravel(), Z.ravel()]
    F = np.empty(len(P))
    for i in range(0, len(P), 400000):
        F[i:i + 400000] = sdf(P[i:i + 400000])
    inside = F < 0
    vol = inside.sum() * H ** 3
    Pin = P[inside]
    boss_part = (np.hypot(Pin[:, 0] - LIDB["xy"][0], Pin[:, 1] - LIDB["xy"][1]) <= LIDB["r"]) & (Pin[:, 2] >= LIDB["z"][0])
    v_new = (~boss_part).sum() * H ** 3
    print("grid %d x %d x %d, step %.2f mm" % (nx, ny, nz, H))
    print("spine solid incl. rear lid boss %.0f mm^3; new fixed material %.0f mm^3 = %.2f g (PET-CF 1.30)" % (vol, v_new, v_new * 1.30e-3))
    d9 = poly_dist(Pin, K9) - R9
    print("clearance spine to K9 (moved %.1f mm in y): %.2f mm (rule >= 1.0)" % (K9_DY, d9.min()))
    d9o = poly_dist(Pin, K9_0) - R9
    print("clearance spine to K9 at its current position: %.2f mm" % d9o.min())
    d8 = poly_dist(Pin, K8) - R8
    print("min wall to K8 inside the solid: %.2f mm" % d8.min())
    dK = np.array([keel_half_width(x, z) for x, z in Pin[::50][:, [0, 2]]]) - np.abs(Pin[::50][:, 1])
    print("min margin to the keel side: %.2f mm" % dK.min())
    # K9 moved: its distance to the keel side and to the K8 channel
    k9d = NS["densify"](K9)
    hw9 = np.array([keel_half_width(x, z) for x, y, z in k9d]) - (np.abs(k9d[:, 1]) + R9)
    print("moved K9 to keel side (z >= 0 part inside the keel): %.2f mm" % hw9[(k9d[:, 0] < -23) & (k9d[:, 2] <= 21.5)].min())
    print("moved K9 to K8 surface gap: %.2f mm" % (poly_dist(k9d, K8).min() - R8 - R9))
    V, T = march(F.reshape(nx, ny, nz), lo, H)
    print("mesh %d vertices, %d triangles" % (len(V), len(T)))
    col = ((np.hypot(V[:, 0] - LIDB["xy"][0], V[:, 1] - LIDB["xy"][1]) <= LIDB["r"] + 0.05) & (V[:, 2] >= LIDB["z"][0] - 0.05)).astype(int)
    out = {"v": np.round(V, 3).ravel().tolist(), "t": T.ravel().astype(int).tolist(), "boss": col.tolist(),
           "k9": np.round(K9, 2).tolist(), "volume_mm3": round(v_new, 0)}
    with open(os.path.join(ROOT, "figures", "f17_spine_mesh.json"), "w") as f:
        json.dump(out, f, separators=(",", ":"))
    print("written figures/f17_spine_mesh.json")


if __name__ == "__main__":
    main()
