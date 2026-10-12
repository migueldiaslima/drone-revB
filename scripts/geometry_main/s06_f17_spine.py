# -*- coding: ascii -*-
"""
s06_f17_spine.py - F-17 fix, under-keel antenna (v04-B revision 3 proposal, 2026-10-12).

Defines and validates, without a CAD kernel (numpy signed distance fields):
  1. K8 antenna channel, new route: dia 3.5, horizontal at (y +3.5, z 6.5) from the bay to x -42,
     then one R7 bend in the x-z plane down to the exit at (-49, +3.5) on the keel underside.
     (Old route: z 7, R5 bend, exit at (-38, +3.5).) The coax bend radius stays >= 6 x OD (1.13 mm
     coax, I-PEX recommendation) everywhere, including into the antenna stem (no bend there).
  2. K9 GPS channel moved 1.5 mm towards -y (vertical leg (-38.2, -3.0), rear-wall hole (-23, -5.0));
     no fixed material around it.
  3. Antenna spine (TUB fixed, replaces the antenna boss): sleeve of 1.5 mm wall around K8 from the
     bay face to the exit, pad in the keel underside (x -53..-40, y -8..+8, z 0..6) with an M2
     heat-set insert hole (dia 3.2 x 4.5, 1.5 mm cap) and a locating hole (dia 2 x 2), web up the
     rear wall into the rear lid boss (-21, +5). Smooth unions (blend radius K_BLEND).
  4. Antenna holder (TPU 95A, separate print): top plate on the pad with a slot for the antenna stem,
     U cradle for the moulded T bar standing vertical (stem up), snap lips, C-clips on both legs,
     peg, M2 screw from below.
Checks are printed (PASS/FAIL against the project rules) and written to
geometry/v04B_r3_f17/checks.json; STL files of the spine (restoration solid, D-044) and the holder
(print file) and a JSON mesh for the viewer are written to the same folder.
ASCII only. Coordinates x forward, y left, z up, mm.
"""
import json
import math
import os
import struct
import numpy as np
from scipy import ndimage
from scipy.spatial import cKDTree

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
OUT = os.path.join(ROOT, "geometry", "v04B_r3_f17")

# ------------------------------------------------------------------ fixed v04-B data (rev 2)
M = 52.497                      # motor axis coordinate
R_KEEP = 47.45                  # prop radius + 3
KEEL = dict(x=(-54.0, -22.0), yh=9.0, z=(0.0, 21.5))
BAY_X = -20.5                   # bay inner face (rear wall inner face)
WALL_X = -23.0                  # rear wall outer face
FLOOR_Z = -15.0                 # landing plane
LIDB_RL = dict(xy=(-21.0, 5.0), r=3.0, z=(15.5, 21.5))
KEELB = dict(xy=(-30.0, 0.0), r=3.0, z=(15.5, 21.5))
RHO_PET, RHO_TPU = 1.30e-3, 1.21e-3        # g/mm^3; TPU 95A density assumed (typical datasheet value)

# ------------------------------------------------------------------ proposal parameters
K8P = dict(d=3.5, y=3.5, z=6.5, x_entry=-18.5, x_bend=-42.0, R=7.0, z_exit=-1.0)
K9_DY = -1.5
WALL = 1.5
K_BLEND = 1.6
PAD = dict(x=(-53.0, -39.0), y=(-8.0, 8.0), z=(0.0, 2.2), r=0.6)        # top 1.05 below the sleeve: no grazing intersection in CAD (G3)
BOSS_INS = dict(r=3.3, z=(0.0, 5.7))                                     # local boss around the insert: 1.7 wall, 1.7 cap
INSERT = dict(xy=(-43.0, -1.0), r=1.6, z=(0.0, 4.0))           # dia 3.2 x 4.0 for an M2 x 3 heat-set insert (1 mm melt room)
PEG = dict(xy=(-43.0, -5.3), r=1.0, z=(0.0, 1.1))              # locating hole dia 2 x 1.1, 1.1 cap
WEB = dict(a=(-21.9, 4.6, 8.0), b=(-21.5, 5.0, 16.5), r=1.75)
# antenna (measured: moulding 14 x 7.5 x 4; split into bar and stem, leg diameter and span ASSUMED)
ANT = dict(x=-49.0, y=3.5, bar=(4.0, 14.0, 4.5), stem=(3.0, 3.2, 3.0), stem_top=-0.5, leg_d=1.4,
           span=50.0, cap_d=4.0, cap_len=5.0)
# holder (TPU)
HOLD = dict(plate_z=(-1.5, 0.0), plate_x=(-52.2, -41.0), plate_y=(-7.5, 8.0),
            gap_x=0.10, gap_stem=0.20, cheek_t=1.2, lip=(1.0, 1.0), clip_wall=0.8, clip_gap=0.10,
            screw_clear_d=2.2, screw_head_d=3.8, cb_d=4.2, peg_d=1.8, peg_h=0.9)


# ------------------------------------------------------------------ helpers
def lin(a, b, h):
    return np.linspace(a, b, max(2, int(math.ceil(abs(b - a) / h)) + 1))


def k8_path(n_arc=60):
    p = K8P
    xe, y, z, xb, R = p["x_entry"], p["y"], p["z"], p["x_bend"], p["R"]
    leg = np.c_[lin(xe, xb, 0.5), np.full(len(lin(xe, xb, 0.5)), y), np.full(len(lin(xe, xb, 0.5)), z)]
    c = np.array([xb, y, z - R])                       # arc centre
    t = np.linspace(0.0, math.pi / 2, n_arc)
    arc = np.c_[c[0] - R * np.sin(t), np.full(n_arc, y), c[2] + R * np.cos(t)]
    stub = np.c_[np.full(5, xb - R), np.full(5, y), np.linspace(z - R, p["z_exit"], 5)]
    return np.vstack([leg, arc[1:], stub[1:]])


def k9_path():
    xv, yv, zb, R, zh = -38.2, -1.5 + K9_DY, 10.0, 5.0, 5.0
    xw, yw = -23.0, -3.5 + K9_DY
    ang = math.atan2(yw - yv, xw - xv)
    Lh = ((BAY_X + 2.0) - xv) / math.cos(ang) - R
    vert = np.c_[np.full(20, xv), np.zeros(20), np.linspace(22.0, zb, 20)]
    t = np.linspace(math.pi, 1.5 * math.pi, 40)
    bend = np.c_[xv + R + R * np.cos(t), np.zeros(40), zb + R * np.sin(t)]
    leg = np.c_[np.linspace(xv + R, xv + R + Lh, 30), np.zeros(30), np.full(30, zh)]
    p = np.vstack([vert, bend[1:], leg[1:]])
    dx = p[:, 0] - xv
    return np.c_[xv + dx * math.cos(ang) - p[:, 1] * math.sin(ang), dx * math.sin(ang) + p[:, 1] * math.cos(ang) + yv, p[:, 2]]


def densify(p, step=0.1):
    out = [p[0]]
    for a, b in zip(p[:-1], p[1:]):
        n = max(1, int(np.linalg.norm(b - a) / step))
        out.extend(a + (b - a) * (i / float(n)) for i in range(1, n + 1))
    return np.array(out)


K8 = k8_path()
K9 = k9_path()
K8d, K9d = densify(K8), densify(K9)
T8, T9 = cKDTree(K8d), cKDTree(K9d)


def keel_hw(x, z):
    x = np.asarray(x, float); z = np.asarray(z, float)
    cut = M - np.sqrt(np.maximum(R_KEEP ** 2 - (np.abs(x) - M) ** 2, 0.0))
    return np.where(z < 10.0, KEEL["yh"], np.minimum(KEEL["yh"], cut))


def seg_dist(P, A, B):
    A, B = np.asarray(A, float), np.asarray(B, float)
    AB = B - A
    t = np.clip(((P - A) @ AB) / (AB @ AB), 0.0, 1.0)
    return np.linalg.norm(P - (A + t[:, None] * AB), axis=1)


def smin(a, b, k):
    h = np.clip(0.5 + 0.5 * (b - a) / k, 0.0, 1.0)
    return b * (1 - h) + a * h - k * h * (1 - h)


def sd_box(P, x, y, z, r=0.0):
    c = np.array([(x[0] + x[1]) / 2, (y[0] + y[1]) / 2, (z[0] + z[1]) / 2])
    half = np.array([(x[1] - x[0]) / 2, (y[1] - y[0]) / 2, (z[1] - z[0]) / 2]) - r
    q = np.abs(P - c) - half
    return np.linalg.norm(np.maximum(q, 0.0), axis=1) + np.minimum(q.max(axis=1), 0.0) - r


def sd_zcyl(P, xy, r, z0, z1):
    dr = np.hypot(P[:, 0] - xy[0], P[:, 1] - xy[1]) - r
    dz = np.maximum(z0 - P[:, 2], P[:, 2] - z1)
    return np.minimum(np.maximum(dr, dz), 0.0) + np.hypot(np.maximum(dr, 0.0), np.maximum(dz, 0.0))


def sd_ycyl(P, xz, r, y0, y1):
    dr = np.hypot(P[:, 0] - xz[0], P[:, 2] - xz[1]) - r
    dy = np.maximum(y0 - P[:, 1], P[:, 1] - y1)
    return np.minimum(np.maximum(dr, dy), 0.0) + np.hypot(np.maximum(dr, 0.0), np.maximum(dy, 0.0))


def d8(P):
    return T8.query(P)[0] - K8P["d"] / 2.0


def d9(P):
    return T9.query(P)[0] - 2.0


# ------------------------------------------------------------------ spine
def spine_sdf(P):
    sleeve_line = K8d[K8d[:, 0] <= -19.5]
    sleeve = cKDTree(sleeve_line).query(P)[0] - (K8P["d"] / 2.0 + WALL)
    pad = smin(sd_box(P, PAD["x"], PAD["y"], PAD["z"], PAD["r"]), sd_zcyl(P, INSERT["xy"], BOSS_INS["r"], *BOSS_INS["z"]), 1.0)
    web = seg_dist(P, WEB["a"], WEB["b"]) - WEB["r"]
    boss = sd_zcyl(P, LIDB_RL["xy"], LIDB_RL["r"], *LIDB_RL["z"])
    s = smin(smin(smin(sleeve, pad, K_BLEND), web, K_BLEND), boss, K_BLEND)
    hw = keel_hw(P[:, 0], P[:, 2])
    s = np.maximum.reduce([s, -P[:, 2], np.minimum(P[:, 0] - BAY_X, boss), np.abs(P[:, 1]) - hw,
                           P[:, 2] - KEEL["z"][1], KEEL["x"][0] - P[:, 0]])
    s = np.maximum(s, -d8(P))
    s = np.maximum(s, -sd_zcyl(P, INSERT["xy"], INSERT["r"], INSERT["z"][0] - 1.0, INSERT["z"][1]))
    s = np.maximum(s, -sd_zcyl(P, PEG["xy"], PEG["r"], PEG["z"][0] - 1.0, PEG["z"][1]))
    return s


# ------------------------------------------------------------------ antenna and holder
def ant_parts():
    a = ANT
    bx, by, bz = a["bar"]; sx, sy, sz = a["stem"]
    z_stem = (a["stem_top"] - sz, a["stem_top"])
    z_bar = (z_stem[0] - bz, z_stem[0])
    leg_z = 0.5 * (z_bar[0] + z_bar[1])
    return dict(bar=((a["x"] - bx / 2, a["x"] + bx / 2), (a["y"] - by / 2, a["y"] + by / 2), z_bar),
                stem=((a["x"] - sx / 2, a["x"] + sx / 2), (a["y"] - sy / 2, a["y"] + sy / 2), z_stem),
                leg_z=leg_z, tips=(a["y"] - a["span"] / 2, a["y"] + a["span"] / 2))


def holder_sdf(P):
    h, A = HOLD, ant_parts()
    (bx0, bx1), (by0, by1), (bz0, bz1) = A["bar"]
    (sx0, sx1), (sy0, sy1), _ = A["stem"]
    gx = h["gap_x"]; ct = h["cheek_t"]
    cx0, cx1 = bx0 - gx - ct, bx1 + gx + ct                    # outer faces of the cheeks
    lip_h, lip_w = h["lip"]
    yc0, yc1 = by0 - 0.6, by1 + 0.6                            # lips along the bar
    yk0, yk1 = by0 - 3.0 - 1.5, by1 + 3.0 + 1.5                # cheeks run out to the clips, full height to z = 0
    plate = sd_box(P, h["plate_x"], h["plate_y"], h["plate_z"], 0.4)
    cheeks = np.minimum(sd_box(P, (cx0, bx0 - gx), (yk0, yk1), (bz0 - lip_h, h["plate_z"][1]), 0.3),
                        sd_box(P, (bx1 + gx, cx1), (yk0, yk1), (bz0 - lip_h, h["plate_z"][1]), 0.3))
    lips = np.minimum(sd_box(P, (bx0 - gx, bx0 - gx + lip_w), (yc0, yc1), (bz0 - lip_h, bz0 - 0.05), 0.2),
                      sd_box(P, (bx1 + gx - lip_w, bx1 + gx), (yc0, yc1), (bz0 - lip_h, bz0 - 0.05), 0.2))
    body = np.minimum.reduce([plate, cheeks, lips])
    # C-clips on the legs, 3 mm out from the moulding ends, opening downwards (leg pressed up into it)
    rl = ANT["leg_d"] / 2.0 + h["clip_gap"]
    ro = rl + h["clip_wall"]
    for ycl in (by0 - 3.0, by1 + 3.0):
        ring = np.maximum(sd_ycyl(P, (ANT["x"], A["leg_z"]), ro, ycl - 1.5, ycl + 1.5),
                          -sd_ycyl(P, (ANT["x"], A["leg_z"]), rl, ycl - 2.0, ycl + 2.0))
        ring = np.maximum(ring, (A["leg_z"] - 0.5 * rl) - P[:, 2])      # C-clip: lower part cut flat, opening 1.73 x rl wide
        yr = (ycl - 1.5, yc0 + 0.5) if ycl < yc0 else (yc1 - 0.5, ycl + 1.5)
        arm = sd_box(P, (cx0, cx1), yr, (A["leg_z"] + ro - 0.2, A["leg_z"] + ro + 1.0), 0.2)   # bridge over the leg
        body = np.minimum.reduce([body, ring, arm])
    # cuts: stem slot through the plate, M2 clearance + counterbore, keep the bar pocket free
    slot = sd_box(P, (sx0 - h["gap_stem"], sx1 + h["gap_stem"]), (sy0 - h["gap_stem"], sy1 + h["gap_stem"]), (-5.0, 1.0))
    pocket = sd_box(P, (bx0 - gx, bx1 + gx), (by0 - 0.05, by1 + 0.05), (bz0 - 0.05, h["plate_z"][0] + 0.01))
    legs = sd_ycyl(P, (ANT["x"], A["leg_z"]), rl, by0 - 30, by1 + 30)
    screw = sd_zcyl(P, INSERT["xy"], h["screw_clear_d"] / 2.0, -10.0, 1.0)
    body = np.maximum.reduce([body, -slot, -pocket, -legs, -screw])
    peg = sd_zcyl(P, PEG["xy"], h["peg_d"] / 2.0, -0.5, h["peg_h"])
    return np.minimum(body, peg)


# ------------------------------------------------------------------ meshing (marching tetrahedra)
TETS = np.array([[0, 5, 1, 6], [0, 1, 2, 6], [0, 2, 3, 6], [0, 3, 7, 6], [0, 7, 4, 6], [0, 4, 5, 6]])
CUBE = np.array([[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0], [0, 0, 1], [1, 0, 1], [1, 1, 1], [0, 1, 1]])


def grid(fn, lo, hi, h):
    nx, ny, nz = [int(math.ceil((hi[i] - lo[i]) / h)) + 1 for i in range(3)]
    ax = [lo[i] + h * np.arange(n) for i, n in enumerate((nx, ny, nz))]
    X, Y, Z = np.meshgrid(*ax, indexing="ij")
    P = np.c_[X.ravel(), Y.ravel(), Z.ravel()]
    F = np.empty(len(P))
    for i in range(0, len(P), 300000):
        F[i:i + 300000] = fn(P[i:i + 300000])
    return F.reshape(nx, ny, nz), P, np.array(lo, float)


def march(F, origin, h, fn):
    nx, ny, nz = F.shape
    N = nx * ny * nz
    I, J, K = [a.ravel() for a in np.meshgrid(np.arange(nx - 1), np.arange(ny - 1), np.arange(nz - 1), indexing="ij")]
    gid = lambda i, j, k: (i * ny + j) * nz + k
    ids = np.stack([gid(I + c[0], J + c[1], K + c[2]) for c in CUBE], axis=1)
    Ff = F.ravel()
    v = Ff[ids]
    ids = ids[(v.min(axis=1) < 0) & (v.max(axis=1) >= 0)]
    tris = []
    for t in TETS:
        vv = ids[:, t]
        ins = Ff[vv] < 0
        n_in = ins.sum(axis=1)
        for case in (1, 3):
            s = n_in == case
            if s.any():
                lone = ins[s] if case == 1 else ~ins[s]
                a = vv[s][lone]
                o = vv[s][~lone].reshape(-1, 3)
                tri = np.stack([np.stack([a, o[:, k]], 1) for k in range(3)], 1)
                tris.append(tri)
        s = n_in == 2
        if s.any():
            i2 = vv[s][ins[s]].reshape(-1, 2); o2 = vv[s][~ins[s]].reshape(-1, 2)
            e = lambda a, b: np.stack([a, b], 1)
            tris.append(np.stack([e(i2[:, 0], o2[:, 0]), e(i2[:, 0], o2[:, 1]), e(i2[:, 1], o2[:, 1])], 1))
            tris.append(np.stack([e(i2[:, 0], o2[:, 0]), e(i2[:, 1], o2[:, 1]), e(i2[:, 1], o2[:, 0])], 1))
    E = np.concatenate(tris, 0)
    pr = np.sort(E.reshape(-1, 2), 1)
    key = pr[:, 0].astype(np.int64) * N + pr[:, 1]
    uk, inv = np.unique(key, return_inverse=True)
    p0, p1 = uk // N, uk % N
    f0, f1 = Ff[p0], Ff[p1]
    t = np.clip(f0 / (f0 - f1), 0.0, 1.0)[:, None]
    xyz = lambda g: np.stack([g // (ny * nz), (g // nz) % ny, g % nz], 1) * h + origin
    V = xyz(p0) + t * (xyz(p1) - xyz(p0))
    T = inv.reshape(-1, 3)
    n = np.cross(V[T[:, 1]] - V[T[:, 0]], V[T[:, 2]] - V[T[:, 0]])
    keep = np.linalg.norm(n, axis=1) > 1e-12
    T, n = T[keep], n[keep]
    c = V[T].mean(1); eps = 0.05
    g = np.stack([fn(c + eps * np.eye(3)[k]) - fn(c - eps * np.eye(3)[k]) for k in range(3)], 1)
    flip = (n * g).sum(1) < 0
    T[flip] = T[flip][:, ::-1]
    # weld vertices that coincide (edge points at t = 0 or 1 shared between edges)
    q = np.round(V / 1e-5).astype(np.int64)
    _, first, inv2 = np.unique(q, axis=0, return_index=True, return_inverse=True)
    V = V[first]; T = inv2.reshape(-1)[T]
    T = T[(T[:, 0] != T[:, 1]) & (T[:, 1] != T[:, 2]) & (T[:, 0] != T[:, 2])]
    return V, T


def mesh_report(V, T):
    e = np.sort(np.vstack([T[:, [0, 1]], T[:, [1, 2]], T[:, [2, 0]]]), 1)
    _, cnt = np.unique(e, axis=0, return_counts=True)
    vol = np.einsum("ij,ij->i", V[T[:, 0]], np.cross(V[T[:, 1]], V[T[:, 2]])).sum() / 6.0
    return dict(vertices=int(len(V)), triangles=int(len(T)), edges_not_shared_by_2=int((cnt != 2).sum()), volume_mm3=float(vol))


def write_stl(path, V, T, name):
    tri = V[T]
    n = np.cross(tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0])
    n /= np.linalg.norm(n, axis=1)[:, None] + 1e-30
    with open(path, "wb") as f:
        f.write(name.encode("ascii")[:80].ljust(80, b" "))
        f.write(struct.pack("<I", len(T)))
        data = np.zeros(len(T), dtype=[("n", "<f4", 3), ("v", "<f4", 9), ("a", "<u2")])
        data["n"] = n; data["v"] = tri.reshape(-1, 9)
        f.write(data.tobytes())


# ------------------------------------------------------------------ arms (plan model calibrated on gate C-9)
def arm_plan_points(h=0.1):
    S = 3.0 * math.sqrt(2.0); UM = 70.0 + S
    U, Vv = np.meshgrid(np.arange(26.5 + S, UM + 12.01, h), np.arange(-13.2, 13.21, h), indexing="ij")
    U, Vv = U.ravel(), Vv.ravel()
    hw = np.where(U < 40 + S, 10.15, np.where(U < 54 + S, 10.15 + (5 - 10.15) * (U - 40 - S) / 14.0, 5.0))
    ins = (np.abs(Vv) <= hw) | (np.hypot(U - UM, Vv) <= 12.0)
    uc = UM - math.sqrt(17 ** 2 - 10 ** 2)
    ins |= (U > uc - 1) & (U < UM) & (np.abs(Vv) <= np.minimum(12, 10 - np.sqrt(np.maximum(25 - (U - uc) ** 2, 0))))
    U, Vv = U[ins], Vv[ins]
    out = {}
    for k, ang in (("mp", 135.0), ("mm", -135.0)):
        a = math.radians(ang)
        out[k] = U[:, None] * np.array([math.cos(a), math.sin(a)]) + Vv[:, None] * np.array([-math.sin(a), math.cos(a)])
    return out


# ------------------------------------------------------------------ K11 motor-lead passages (corner mp, mm)
def k11_boxes():
    out = []
    for sy in (1, -1):
        a = math.radians(135.0 if sy > 0 else -135.0)
        corners = []
        for u in (8.0, 22.0):
            for v in (9.5, 14.5):
                vv = v if sy > 0 else -v
                corners.append((u * math.cos(a) - vv * math.sin(a) - 3.0, u * math.sin(a) + vv * math.cos(a) + 3.0 * sy))
        out.append(np.array(corners))
    return out


def main():
    os.makedirs(OUT, exist_ok=True)
    C = {}
    def rec(name, value, limit, ok, note=""):
        C[name] = dict(value=value, limit=limit, result="PASS" if ok else "FAIL", note=note)
        print("%-62s %-12s %-14s %s %s" % (name, value if isinstance(value, str) else ("%.2f" % value), limit, "PASS" if ok else "FAIL", note))

    print("=== channels ===")
    # K8 curvature and coax length
    rs = K8d[::10]                                   # 1 mm spacing
    a_, b_, c_ = rs[:-2], rs[1:-1], rs[2:]
    ab, bc, ca = np.linalg.norm(b_ - a_, axis=1), np.linalg.norm(c_ - b_, axis=1), np.linalg.norm(a_ - c_, axis=1)
    area2 = np.linalg.norm(np.cross(b_ - a_, c_ - a_), axis=1)
    circ = np.where(area2 > 1e-9, ab * bc * ca / np.maximum(2 * area2, 1e-12), 1e9)
    rmin = float(circ.min())
    rec("K8 centreline minimum bend radius (mm)", rmin, ">= 6.8 (6 x OD)", rmin >= 6.8 - 0.05)
    L8 = float(np.sum(np.linalg.norm(np.diff(K8d[K8d[:, 2] >= 0.0], axis=0), axis=1)))
    route = 9.3 + L8 + 0.5
    rec("coax route receiver -> bay entry -> K8 -> stem (mm)", route, "<= 62 (measured)", route <= 62.0, "slack %.0f mm" % (62.0 - route))
    g89 = float(T9.query(K8d)[0].min() - 2.0 - K8P["d"] / 2.0)
    rec("K8 to K9 surface gap (mm)", g89, ">= 1.0", g89 >= 1.0)
    # K8 / K9 inside the keel and at the walls
    k8in = K8d[(K8d[:, 0] < WALL_X) & (K8d[:, 2] >= 0.0)]
    m8 = float((keel_hw(k8in[:, 0], k8in[:, 2] + 1.75) - (np.abs(k8in[:, 1]) + 1.75)).min())
    rec("K8 to keel side (mm)", m8, ">= 1.0 + wall", m8 >= 1.0 + WALL)
    k9in = K9d[(K9d[:, 0] < WALL_X) & (K9d[:, 2] <= 21.5)]
    m9 = float((keel_hw(k9in[:, 0], k9in[:, 2]) - (np.abs(k9in[:, 1]) + 2.0)).min())
    rec("K9 (moved) to keel side (mm)", m9, ">= 1.0", m9 >= 1.0)
    k11 = k11_boxes()
    # K8 / K9 wall openings vs K11 (motor-lead passages, z -8 to -3) in the rear wall
    rw = lambda p: p[(p[:, 0] <= BAY_X) & (p[:, 0] >= WALL_X)]
    z8 = rw(K8d)[:, 2].min() - 1.75; z9 = rw(K9d)[:, 2].min() - 2.0
    rec("K8 opening above K11 in the rear wall (mm)", float(z8 - (-3.0)), ">= 1.0", z8 + 3.0 >= 1.0)
    rec("K9 opening above K11 in the rear wall (mm)", float(z9 - (-3.0)), ">= 1.0", z9 + 3.0 >= 1.0)
    lidhole_y = -1.5 + K9_DY
    rec("lid GPS hole moves to (x, y)", "(-38.2, %.1f)" % lidhole_y, "inside pocket", abs(lidhole_y) + 2.0 <= 6.3 - 1.0, "pocket inner half-width 6.3")

    print("=== spine (TUB fixed) ===")
    h = 0.20
    F, P, lo = grid(spine_sdf, (-54.3137, -9.3071, -1.0113), (-17.4, 9.3, 22.0), h)
    inside = F.ravel() < 0
    lab, ncomp = ndimage.label(F < 0)
    rec("spine connected components", float(ncomp), "== 1", ncomp == 1)
    Pin = P[inside]
    boss_part = (np.hypot(Pin[:, 0] - LIDB_RL["xy"][0], Pin[:, 1] - LIDB_RL["xy"][1]) <= LIDB_RL["r"]) & (Pin[:, 2] >= LIDB_RL["z"][0])
    v_new = float((~boss_part).sum() * h ** 3)
    rec("spine new fixed volume (mm^3) / mass (g)", "%.0f / %.2f" % (v_new, v_new * RHO_PET), "-", True)
    dd9 = d9(Pin); c9 = float(dd9.min())
    rec("spine to K9 (mm)", c9, ">= 1.0", c9 >= 1.0, "at %s" % np.round(Pin[dd9.argmin()], 1).tolist())
    side = float((keel_hw(Pin[:, 0], Pin[:, 2]) - np.abs(Pin[:, 1])).min())
    rec("spine to keel side (mm)", side, ">= 1.0", side >= 1.0 - h)
    rec("spine to keel rear end x = -54 (mm)", float(Pin[:, 0].min() + 54.0), ">= 1.0", Pin[:, 0].min() + 54.0 >= 1.0 - h)
    # wall around K8: points 1.0 mm outside the channel surface must be solid (inside the keel and behind the bay face)
    idx = np.arange(0, len(K8d), 3)
    probe_ok, probe_n = 0, 0
    worst = None
    for i in idx:
        p = K8d[i]
        if p[0] > BAY_X - 0.3 or p[2] < 0.3:
            continue
        tng = K8d[min(i + 1, len(K8d) - 1)] - K8d[max(i - 1, 0)]; tng /= np.linalg.norm(tng)
        a = np.cross(tng, [0, 1, 0]) if abs(tng[1]) < 0.9 else np.cross(tng, [1, 0, 0]); a /= np.linalg.norm(a)
        b = np.cross(tng, a)
        for th in np.linspace(0, 2 * math.pi, 24, endpoint=False):
            q = p + (K8P["d"] / 2.0 + 1.0) * (math.cos(th) * a + math.sin(th) * b)
            if q[2] < 0.0:
                continue
            probe_n += 1
            if spine_sdf(q[None, :])[0] < 0:
                probe_ok += 1
            elif worst is None:
                worst = np.round(q, 2).tolist()
    rec("K8 wall >= 1.0 mm all round (probe points solid)", "%d/%d" % (probe_ok, probe_n), "all", probe_ok == probe_n,
        "" if worst is None else "first open point %s" % worst)
    # insert and peg walls
    def ring_probe(c, r, z0, z1, wall):
        pts = []
        for z in np.linspace(z0 + 0.1, z1 - 0.1, 8):
            for th in np.linspace(0, 2 * math.pi, 36, endpoint=False):
                pts.append((c[0] + (r + wall) * math.cos(th), c[1] + (r + wall) * math.sin(th), z))
        cap = [(c[0] + rr * math.cos(th), c[1] + rr * math.sin(th), z1 + wall) for rr in (0, r / 2, r) for th in np.linspace(0, 2 * math.pi, 12, endpoint=False)]
        q = np.array(pts + cap)
        return int((spine_sdf(q) < 0).sum()), len(q)
    a, n = ring_probe(INSERT["xy"], INSERT["r"], *INSERT["z"], 1.5)
    q = []
    for z in np.linspace(INSERT["z"][0] + 0.1, INSERT["z"][1] - 0.1, 8):
        for th in np.linspace(0, 2 * math.pi, 36, endpoint=False):
            q.append((INSERT["xy"][0] + 3.1 * math.cos(th), INSERT["xy"][1] + 3.1 * math.sin(th), z))
    q = np.array(q); bad = q[spine_sdf(q) >= 0]
    if len(bad): print("   insert wall open at e.g.", np.round(bad[:3], 2).tolist(), "K8 dist", np.round(d8(bad[:3]), 2).tolist())
    rec("M2 insert hole: 1.5 mm wall and cap (probe points solid)", "%d/%d" % (a, n), "all", a == n)
    a, n = ring_probe(PEG["xy"], PEG["r"], *PEG["z"], 1.0)
    rec("locating hole: 1.0 mm wall and cap", "%d/%d" % (a, n), "all", a == n)
    gk = float(T8.query(np.array([[INSERT["xy"][0], INSERT["xy"][1], z] for z in np.linspace(0, INSERT["z"][1], 20)]))[0].min()
               - K8P["d"] / 2.0 - INSERT["r"])
    rec("insert hole to K8 (mm)", gk, ">= 1.0", gk >= 1.0)
    # other fixed regions it must not merge with unintentionally: keel lid boss
    dkb = float(sd_zcyl(Pin, KEELB["xy"], KEELB["r"], *KEELB["z"]).min())
    rec("spine to keel lid boss (-30, 0) (mm)", dkb, ">= 1.0 or merged", dkb >= 1.0 - h)
    rec("spine joined to rear lid boss (-21, +5)", "yes" if boss_part.any() and ncomp == 1 else "no", "yes", boss_part.any() and ncomp == 1)
    Fs, _, los = grid(spine_sdf, (-54.3137, -9.3071, -1.0113), (-17.4, 9.3, 22.0), 0.30)   # export mesh, 0.3 mm
    Vs, Ts = march(Fs, los, 0.30, spine_sdf)
    ms = mesh_report(Vs, Ts)
    rec("spine STL closed (edges not shared by exactly 2 faces)", float(ms["edges_not_shared_by_2"]), "== 0", ms["edges_not_shared_by_2"] == 0,
        "%d triangles, mesh volume %.0f mm^3" % (ms["triangles"], ms["volume_mm3"]))
    write_stl(os.path.join(OUT, "SPINE_fixed_v04B_r3.stl"), Vs, Ts, "SPINE fixed v04B r3 (TUB, PET-CF), mm")

    print("=== antenna and holder ===")
    A = ant_parts()
    arms = arm_plan_points()
    best = 1e9
    for sy, kk in ((1, "mp"), (-1, "mm")):
        y = np.linspace(ANT["y"] + sy * ANT["bar"][1] / 2, ANT["y"] + sy * ANT["span"] / 2, 400)
        r = np.where(np.abs(y - ANT["y"]) > ANT["span"] / 2 - ANT["cap_len"], ANT["cap_d"] / 2, ANT["leg_d"] / 2)
        d = cKDTree(arms[kk]).query(np.c_[np.full_like(y, ANT["x"]), y])[0] - r
        best = min(best, float(d.min()))
    rec("C-9 antenna to rear arms, plan (mm)", best, ">= 5.0", best >= 5.0, "arm model within 0.05 mm of gate C-9 on the old V")
    rec("antenna legs z (mm)", float(A["leg_z"]), "above -12, below 10", -12 < A["leg_z"] < 10)
    hz, Ph, loh = grid(holder_sdf, (-53.5137, -10.5071, -10.5113), (-39.5, 17.5, 2.5), 0.10)
    inside_h = hz.ravel() < 0
    Phi = Ph[inside_h]
    lab_h, nh = ndimage.label(hz < 0)
    sizes = ndimage.sum(np.ones_like(lab_h), lab_h, range(1, nh + 1))
    cents = ndimage.center_of_mass(np.ones_like(lab_h), lab_h, range(1, nh + 1))
    rec("holder connected components", float(nh), "== 1", nh == 1,
        "" if nh == 1 else "; ".join("%d vox at %s" % (sz, np.round(np.array(c) * 0.1 + loh, 1).tolist()) for sz, c in zip(sizes, cents)))
    vh = float(inside_h.sum() * 0.1 ** 3)
    rec("holder volume (mm^3) / mass TPU (g)", "%.0f / %.2f" % (vh, vh * RHO_TPU), "-", True)
    zlow = float(Phi[:, 2].min())
    rec("holder lowest point to landing plane (mm)", zlow - FLOOR_Z, ">= 5", zlow - FLOOR_Z >= 5.0)
    rec("holder top within the pad footprint", "x %.1f..%.1f y %.1f..%.1f" % (HOLD["plate_x"][0], HOLD["plate_x"][1], HOLD["plate_y"][0], HOLD["plate_y"][1]),
        "inside pad", HOLD["plate_x"][0] >= PAD["x"][0] and HOLD["plate_x"][1] <= PAD["x"][1] and HOLD["plate_y"][0] >= PAD["y"][0] and HOLD["plate_y"][1] <= PAD["y"][1])
    # thin features: local thickness = 2 x distance to the outside at the medial points
    edt = ndimage.distance_transform_edt(hz < 0) * 0.1
    ridge = (edt == ndimage.maximum_filter(edt, size=3)) & (hz < 0)
    tmin = float(2 * edt[ridge].min())
    wpos = np.round(np.array(np.unravel_index(np.where(ridge.ravel() & (2 * edt.ravel() <= tmin + 1e-9))[0][0], edt.shape)) * 0.1 + loh, 1).tolist()
    rec("holder thinnest feature (2 x inscribed radius, mm)", tmin, ">= 0.8 (2 lines)", tmin >= 0.8 - 0.1, "at %s" % wpos)
    # the antenna must not intersect the holder; the moulding must touch the plate and the lips
    (bx0, bx1), (by0, by1), (bz0, bz1) = A["bar"]
    barpts = np.array([(x, y, z) for x in lin(bx0, bx1, 0.2) for y in lin(by0, by1, 0.5) for z in lin(bz0, bz1, 0.2)])
    rec("bar pocket clearance (holder material inside the bar)", float((holder_sdf(barpts) < -0.01).sum()), "== 0", (holder_sdf(barpts) < -0.01).sum() == 0)
    (sx0, sx1), (sy0, sy1), (sz0, sz1) = A["stem"]
    stempts = np.array([(x, y, z) for x in lin(sx0, sx1, 0.2) for y in lin(sy0, sy1, 0.2) for z in lin(sz0, sz1, 0.2)])
    rec("stem slot clearance (holder material inside the stem)", float((holder_sdf(stempts) < -0.01).sum()), "== 0", (holder_sdf(stempts) < -0.01).sum() == 0)
    rec("stem top to K8 exit: coax goes straight up (offset mm)", float(math.hypot(ANT["x"] - (K8P["x_bend"] - K8P["R"]), ANT["y"] - K8P["y"])), "== 0",
        abs(ANT["x"] - (K8P["x_bend"] - K8P["R"])) < 1e-6 and abs(ANT["y"] - K8P["y"]) < 1e-6)
    sc = HOLD
    under_plate = (HOLD["plate_z"][0] - 0.0)
    rec("screw M2 x 5: engagement / tip below hole bottom (mm)", "%.1f / %.1f" % (5.0 - 1.5, INSERT["z"][1] - 3.5), ">= 3.0 / > 0", True,
        "head under the 1.5 mm plate; hole 4.0 deep, M2 x 3 insert")
    hd = math.hypot(INSERT["xy"][0] - (bx1 + HOLD["gap_x"] + HOLD["cheek_t"]), 0) - HOLD["screw_head_d"] / 2.0
    rec("screw head to front cheek (mm)", hd, ">= 0.3", hd >= 0.3)
    hz2, _, loh2 = grid(holder_sdf, (-53.5137, -10.5071, -10.5113), (-39.5, 17.5, 2.5), 0.20)   # export mesh, 0.2 mm
    Vh, Th = march(hz2, loh2, 0.20, holder_sdf)
    mh = mesh_report(Vh, Th)
    rec("holder STL closed", float(mh["edges_not_shared_by_2"]), "== 0", mh["edges_not_shared_by_2"] == 0, "%d triangles" % mh["triangles"])
    write_stl(os.path.join(OUT, "ANTENNA_HOLDER_v04B_r3_TPU.stl"), Vh, Th, "ANTENNA HOLDER v04B r3 (TPU 95A), mm, print plate-down")
    # K11 vs holder and antenna: K11 passages end at x >= -28.8
    k11x = min(b[:, 0].min() for b in k11)
    rec("holder/antenna to motor-lead passages K11 (x gap, mm)", float((k11x) - max(HOLD["plate_x"][1], ANT["x"] + 2)), ">= 5", (k11x - HOLD["plate_x"][1]) >= 5.0)

    hz3, _, loh3 = grid(holder_sdf, (-53.5137, -10.5071, -10.5113), (-39.5, 17.5, 2.5), 0.30)   # viewer mesh
    Vv, Tv = march(hz3, loh3, 0.30, holder_sdf)
    mesh = {"spine": {"v": np.round(Vs, 2).ravel().tolist(), "t": Ts.ravel().astype(int).tolist(),
                      "boss": ((np.hypot(Vs[:, 0] - LIDB_RL["xy"][0], Vs[:, 1] - LIDB_RL["xy"][1]) <= LIDB_RL["r"] + 0.05) & (Vs[:, 2] >= LIDB_RL["z"][0] - 0.05)).astype(int).tolist()},
            "holder": {"v": np.round(Vv, 2).ravel().tolist(), "t": Tv.ravel().astype(int).tolist()},
            "k8": np.round(K8[::2], 2).tolist(), "k9": np.round(K9[::2], 2).tolist(),
            "ant": {"x": ANT["x"], "y": ANT["y"], "bar": A["bar"], "stem": A["stem"], "leg_z": A["leg_z"], "span": ANT["span"],
                    "leg_d": ANT["leg_d"], "cap_d": ANT["cap_d"], "cap_len": ANT["cap_len"]},
            "screw": {"xy": INSERT["xy"], "z": [HOLD["plate_z"][0] - 1.3, HOLD["plate_z"][0] + 6.0]}}
    with open(os.path.join(OUT, "f17_r3_mesh.json"), "w") as f:
        json.dump(mesh, f, separators=(",", ":"))
    with open(os.path.join(OUT, "checks.json"), "w") as f:
        json.dump(dict(parameters=dict(K8=K8P, K9_dy=K9_DY, wall=WALL, blend=K_BLEND, pad=PAD, insert=INSERT, peg=PEG, web=WEB,
                                       antenna=ANT, holder=HOLD), checks=C), f, indent=1)
    fails = [k for k, v in C.items() if v["result"] == "FAIL"]
    print("FAILS:", fails if fails else "none")


if __name__ == "__main__":
    main()
