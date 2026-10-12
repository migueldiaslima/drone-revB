# -*- coding: ascii -*-
"""
f17_antenna_link.py - figures for F-17 (antenna boss island, H4 cycle 31) and the proposed
fixed link, drawn from the v04-B revision 2 generator parameters (s06_geometry_v04B.py P,
keepouts(), components()). Plain matplotlib, no CAD kernel: every solid near the keel is a box,
cylinder, or tube on a centreline, so the sections and clearances are exact for those primitives.
Approximate (labelled in the figures): rear arm outline in plan (corridor width 10, D-046).

Writes figures/f17_1_current.png, f17_2_link.png, f17_3_antenna.png and prints the clearances.
Coordinates: x forward, y left, z up, mm. ASCII only.
"""
import math
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Polygon

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(os.path.dirname(HERE)), "figures")

# ---------------- v04-B revision 2 parameters (s06_geometry_v04B.py, P) ----------------
M = 52.5 + 0.003 - 0.003          # motor axis coordinate (M_NEW = 52.497, shown as 52.5)
R_KEEP = 47.45                    # prop radius 44.45 + 3
R_PROP = 44.45
KEEL = dict(x=(-54.0, -22.0), yh=9.0, z=(0.0, 21.5))
BODY_H, BAY, FLOOR_Z, CHAMFER_Z, RIM_Z = 23.0, 20.5, -15.0, 10.0, 21.5
ANT = dict(x=-44.0, y=0.0, r=2.7, z=(0.0, 6.5), ins_r=1.6, ins_z=(-1.0, 4.5))
LIDB = [(21.0, 9.5), (21.0, -9.5), (-21.0, 5.0), (-21.0, -5.0), (-30.0, 0.0)]
LIDB_R, LIDB_Z, LIDB_INS = 3.0, (15.5, 21.5), (17.0, 22.5)
LID_Z = (21.5, 24.0)
DECK = dict(x=(-54.0, -30.0), yh=10.0)
HOLDER = dict(x=(-50.0, -38.0), y=(-9.0, 9.0), z=(-5.2, 0.0))
JUNC = dict(x=(-47.75, -40.25), y=(-7.0, 7.0), z=(-4.0, 0.0))
V_START, V_LEN, V_Z = 7.0, 18.0, -2.0
GPS = dict(x=(-52.5, -35.5), y=(-6.0, 6.0), z=(24.0, 29.0))
GPS_CAP = dict(x=(-54.0, -34.0), y=(-12.0, 12.0), z=(29.0, 30.2))


# ---------------- channels as centrelines (K8 antenna dia 3.5, K9 GPS dia 4) ----------------
def arc(c, r, a0, a1, plane, n=40):
    t = np.linspace(a0, a1, n)
    if plane == "xz":
        return np.c_[c[0] + r * np.cos(t), np.full(n, c[1]), c[2] + r * np.sin(t)]


def k8():
    y, zh, xb, R = 3.5, 7.0, -33.0, 5.0
    leg = np.c_[np.linspace(-18.5, xb, 30), np.full(30, y), np.full(30, zh)]
    bend = arc((xb, y, zh - R), R, math.pi / 2, math.pi, "xz")          # (-33, z 7) to (-38, z 2)
    vert = np.c_[np.full(10, xb - R), np.full(10, y), np.linspace(zh - R, -1.0, 10)]
    return np.vstack([leg, bend, vert]), 1.75


def k9():
    xv, yv, zb, R, zh = -38.2, -1.5, 10.0, 5.0, 5.0
    xw, yw = -23.0, -3.5
    ang = math.atan2(yw - yv, xw - xv)
    Lh = (-BAY + 2.0 - xv) / math.cos(ang) - R
    vert = np.c_[np.full(20, xv), np.zeros(20), np.linspace(RIM_Z + 0.5, zb, 20)]
    bend = arc((xv + R, 0.0, zb), R, math.pi, 1.5 * math.pi, "xz")      # (xv, z 10) to (xv + 5, z 5)
    leg = np.c_[np.linspace(xv + R, xv + R + Lh, 30), np.zeros(30), np.full(30, zh)]
    p = np.vstack([vert, bend, leg])
    dx = p[:, 0] - xv
    x = xv + dx * math.cos(ang) - p[:, 1] * math.sin(ang)
    y = dx * math.sin(ang) + p[:, 1] * math.cos(ang) + yv
    return np.c_[x, y, p[:, 2]], 2.0


def densify(p, step=0.1):
    out = [p[0]]
    for a, b in zip(p[:-1], p[1:]):
        n = max(1, int(np.linalg.norm(b - a) / step))
        out.extend(a + (b - a) * (i / float(n)) for i in range(1, n + 1))
    return np.array(out)


K8, R8 = k8()
K9, R9 = k9()
K8d, K9d = densify(K8), densify(K9)


def keel_half_width(x, z):
    """Keel half-width: 9, cut above z = 10 by the rear prop sweep + 3 mm (R 47.45 about the motor axis)."""
    if z < CHAMFER_Z:
        return KEEL["yh"]
    d = abs(x) - M
    return min(KEEL["yh"], M - math.sqrt(max(R_KEEP ** 2 - d * d, 0.0)))


# ---------------- solids sampled as point clouds for clearance checks ----------------
def lin(a, b, h):
    """Samples from a to b inclusive, spacing at most h."""
    return np.linspace(a, b, max(2, int(math.ceil(abs(b - a) / h)) + 1))


def cyl_pts(cx, cy, r, z0, z1, h=0.25):
    pts = []
    for z in lin(z0, z1, h):
        for rr in lin(0.0, r, h):
            n = max(1, int(2 * math.pi * rr / h))
            for t in np.linspace(0, 2 * math.pi, n, endpoint=False):
                pts.append((cx + rr * math.cos(t), cy + rr * math.sin(t), z))
    return np.array(pts)


def box_pts(x0, x1, y0, y1, z0, z1, h=0.25):
    X, Y, Z = np.meshgrid(lin(x0, x1, h), lin(y0, y1, h), lin(z0, z1, h), indexing="ij")
    return np.c_[X.ravel(), Y.ravel(), Z.ravel()]


def strut_pts(p0, p1, ty, tn, h=0.25):
    """Prism along p0 -> p1 (in an x-z plane), width ty in y (centred on p0[1]), thickness tn normal to the axis."""
    p0, p1 = np.array(p0, float), np.array(p1, float)
    L = np.linalg.norm(p1 - p0)
    ax = (p1 - p0) / L
    nrm = np.array([-ax[2], 0.0, ax[0]])
    pts = []
    for s in lin(0.0, L, h):
        for u in lin(-ty / 2, ty / 2, h):
            for v in lin(-tn / 2, tn / 2, h):
                pts.append(p0 + ax * s + np.array([0, u, 0]) + nrm * v)
    return np.array(pts)


def clearance(pts, line, r):
    best = 1e9
    for i in range(0, len(pts), 4000):
        d = np.sqrt(((pts[i:i + 4000, None, :] - line[None, :, :]) ** 2).sum(-1)).min()
        best = min(best, d)
    return best - r


def gap_cyl_cyl(a, b):
    """Plan gap between two vertical cylinders (centre distance minus radii)."""
    return math.hypot(a[0] - b[0], a[1] - b[1]) - a[2] - b[2]


# ---------------- proposed link L1 (fixed, TUB_FIXED), +y side of the keel ----------------
L1 = dict(
    pad_lo=(-46.7, -41.3, -2.7, 4.8, 3.0, 9.0),       # widens the antenna boss towards +y and upwards (x0, x1, y0, y1, z0, z1)
    strut=((-43.5, 3.2, 7.5), (-31.5, 3.2, 17.5), 3.2, 5.0),   # p0, p1, width in y, thickness
    pad_hi=(-33.0, -27.0, 0.0, 4.8, 15.5, 21.5),       # joins the keel lid boss (-30, 0)
)


def l1_points():
    a = box_pts(*L1["pad_lo"])
    p0, p1, ty, tn = L1["strut"]
    b = strut_pts(p0, p1, ty, tn)
    c = box_pts(*L1["pad_hi"])
    return np.vstack([a, b, c]), (a, b, c)


def l1_volume():
    x0, x1, y0, y1, z0, z1 = L1["pad_lo"]
    v_lo = (x1 - x0) * (y1 - y0) * (z1 - z0)
    p0, p1, ty, tn = L1["strut"]
    v_st = np.linalg.norm(np.subtract(p1, p0)) * ty * tn
    x0, x1, y0, y1, z0, z1 = L1["pad_hi"]
    v_hi = (x1 - x0) * (y1 - y0) * (z1 - z0)
    return v_lo, v_st, v_hi


# ---------------- report ----------------
def report():
    print("--- current (v04-B rev 2) ---")
    ab = (ANT["x"], ANT["y"], ANT["r"])
    print("antenna boss to keel lid boss (-30, 0): plan gap %.1f mm, vertical gap %.1f mm (boss top z %.1f, lid boss bottom z %.1f)"
          % (gap_cyl_cyl(ab, (-30.0, 0.0, LIDB_R)), LIDB_Z[0] - ANT["z"][1], ANT["z"][1], LIDB_Z[0]))
    for (x, y) in LIDB[2:4]:
        print("antenna boss to rear lid boss (%.0f, %.0f): plan gap %.1f mm" % (x, y, gap_cyl_cyl(ab, (x, y, LIDB_R))))
    print("antenna boss to rear wall outer face x = -23: %.1f mm" % (-23.0 - (ANT["x"] + ANT["r"])))
    print("antenna boss top to keel top / lid underside z 21.5: %.1f mm" % (RIM_Z - ANT["z"][1]))
    boss = cyl_pts(ANT["x"], ANT["y"], ANT["r"], *ANT["z"])
    print("antenna boss to K8 (antenna channel): %.2f mm" % clearance(boss, K8d, R8))
    print("antenna boss to K9 (GPS channel):     %.2f mm" % clearance(boss, K9d, R9))
    col = cyl_pts(ANT["x"], ANT["y"], ANT["r"], ANT["z"][1], RIM_Z)
    print("vertical column dia 5.4 above the boss to z 21.5: K9 %.2f mm, K8 %.2f mm" % (clearance(col, K9d, R9), clearance(col, K8d, R8)))
    cl = strut_pts((-41.3, 0.0, 5.0), (-32.7, 0.0, 15.5), 4.0, 4.0)
    print("straight centreline strut boss -> keel lid boss (y = 0): K9 %.2f mm (negative = through the channel)" % clearance(cl, K9d, R9))
    print("keel half-width above z = 10: x -54 %.1f, -44 %.1f, -38 %.1f, -30 %.1f mm"
          % tuple(keel_half_width(x, 15.0) for x in (-54, -44, -38, -30)))
    print("--- link L1 ---")
    pts, parts = l1_points()
    for nm, pp in zip(("pad at antenna boss", "strut", "pad at keel lid boss"), parts):
        print("%-22s K8 %.2f mm, K9 %.2f mm" % (nm, clearance(pp, K8d, R8), clearance(pp, K9d, R9)))
    zmax_ok = all(abs(p[1]) <= keel_half_width(p[0], p[2]) + 1e-6 for p in pts[::7])
    ymax = max(p[1] - keel_half_width(p[0], p[2]) for p in pts[::7])
    print("L1 inside the keel envelope: %s (max y beyond the keel side %.2f mm)" % (zmax_ok, ymax))
    v = l1_volume()
    tot = v[0] + v[1] + v[2]
    print("L1 gross volume (overlaps with bosses not removed): pad %.0f + strut %.0f + pad %.0f = %.0f mm^3 = %.2f g"
          % (v[0], v[1], v[2], tot, tot * 1.30e-3))
    print("--- antenna ---")
    arm_axis = lambda x, y: abs(x + y) / math.sqrt(2.0)     # rear-left arm axis y = -x
    tipV = (ANT["x"] - V_LEN * math.cos(math.radians(45)), V_START + V_LEN * math.sin(math.radians(45)))
    tipT = (ANT["x"], V_START + V_LEN)
    for nm, t in (("90 deg V (as modelled)", tipV), ("straight T (180 deg)", tipT)):
        d = arm_axis(*t)
        print("%-24s tip at (%.1f, %.1f, %.1f): %.1f mm from the arm axis in plan, %.1f mm beyond a 10 mm corridor; %.1f mm from the motor axis"
              % (nm, t[0], t[1], V_Z, d, d - 5.0, math.hypot(t[0] + M, t[1] - M)))


# ---------------- drawing helpers ----------------
C = dict(design="#cfe2f3", fixed="#3d6fb6", lid="#e9a46a", lidfix="#c55a11", comp="#4caf6a", chan="#d62728",
         link="#ff9900", air="#ffffff")


def rect(ax, x0, x1, y0, y1, **kw):
    ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, **kw))


def tube_2d(ax, pts, r, i, j, **kw):
    """Draw a tube as a thick band in the projection (i, j)."""
    from matplotlib.collections import PolyCollection
    p = pts[:, [i, j]]
    polys = []
    for a, b in zip(p[:-1], p[1:]):
        d = b - a
        L = np.hypot(*d)
        if L < 1e-9:
            continue
        n = np.array([-d[1], d[0]]) / L * r
        polys.append([a + n, b + n, b - n, a - n])
    for c in p[::3]:
        ax.add_patch(Circle(c, r, lw=0, **kw))
    ax.add_collection(PolyCollection(polys, lw=0, **kw))


def side(ax, link=False, title=""):
    """Section y = 0 with K8 (y = 3.5) and K9 (y about -1.5) projected."""
    rect(ax, -23.0, -20.5, -6.0, RIM_Z, fc=C["design"], ec="k", lw=0.6)        # rear wall
    rect(ax, -23.0, -15.0, FLOOR_Z, -6.0, fc=C["design"], ec="k", lw=0.6)       # floor
    rect(ax, KEEL["x"][0], -23.0, 0.0, RIM_Z, fc=C["design"], ec="k", lw=0.8)   # keel
    rect(ax, KEEL["x"][0], -15.0, LID_Z[0], LID_Z[1], fc=C["lidfix"], ec="k", lw=0.6, alpha=0.55)
    rect(ax, *GPS["x"], *GPS["z"], fc=C["comp"], ec="k", lw=0.5, alpha=0.8)
    rect(ax, *GPS_CAP["x"], *GPS_CAP["z"], fc=C["comp"], ec="k", lw=0.5, alpha=0.5)
    tube_2d(ax, K8, R8, 0, 2, fc="#f2a3a3")
    tube_2d(ax, K9, R9, 0, 2, fc="#cdb5e6")
    rect(ax, -30 - LIDB_R, -30 + LIDB_R, *LIDB_Z, fc=C["fixed"], ec="k", lw=0.6)
    rect(ax, -21 - LIDB_R, -21 + LIDB_R, *LIDB_Z, fc=C["fixed"], ec="k", lw=0.6, alpha=0.6)
    rect(ax, ANT["x"] - ANT["r"], ANT["x"] + ANT["r"], *ANT["z"], fc=C["fixed"], ec="k", lw=0.8)
    rect(ax, ANT["x"] - ANT["ins_r"], ANT["x"] + ANT["ins_r"], ANT["z"][0], ANT["ins_z"][1], fc="w", ec="k", lw=0.4)
    rect(ax, *HOLDER["x"], *HOLDER["z"], fc=C["comp"], ec="k", lw=0.5, alpha=0.45)
    rect(ax, *JUNC["x"], *JUNC["z"], fc=C["comp"], ec="k", lw=0.5, alpha=0.9)
    ax.plot([ANT["x"], ANT["x"] - V_LEN * math.cos(math.radians(45))], [V_Z, V_Z], color="#1b5e20", lw=2.5)
    ax.axhline(FLOOR_Z, color="#b22222", lw=1.5)
    ax.text(-57, FLOOR_Z + 0.6, "landing plane z = -15", color="#b22222", fontsize=7)
    if link:
        x0, x1, y0, y1, z0, z1 = L1["pad_lo"]; rect(ax, x0, x1, z0, z1, fc=C["link"], ec="k", lw=0.6)
        x0, x1, y0, y1, z0, z1 = L1["pad_hi"]; rect(ax, x0, x1, z0, z1, fc=C["link"], ec="k", lw=0.6)
        p0, p1, ty, tn = L1["strut"]
        p0, p1 = np.array(p0), np.array(p1)
        ax_ = (p1 - p0) / np.linalg.norm(p1 - p0); n = np.array([-ax_[2], 0, ax_[0]]) * tn / 2
        poly = [p0 + n, p1 + n, p1 - n, p0 - n]
        ax.add_patch(Polygon([(q[0], q[2]) for q in poly], fc=C["link"], ec="k", lw=0.6))
    # labels
    ax.annotate("antenna boss dia 5.4 x 6.5\n(fixed, 0.15 g)", (ANT["x"], 4.5), (-61, 11), fontsize=7,
                arrowprops=dict(arrowstyle="->", lw=0.6))
    ax.annotate("keel lid boss (-30, 0)\n(fixed, lid tie)", (-30, 18.5), (-36, 31), fontsize=7,
                arrowprops=dict(arrowstyle="->", lw=0.6))
    ax.annotate("K9 GPS channel dia 4\n(at y about -1.5)", (-38.6, 18), (-63, 26.5), fontsize=7, color="#6a3d9a",
                arrowprops=dict(arrowstyle="->", lw=0.6, color="#6a3d9a"))
    ax.annotate("K8 antenna channel dia 3.5\n(at y = +3.5, projected)", (-35.5, 6.4), (-21, 1.5), fontsize=7, color=C["chan"],
                arrowprops=dict(arrowstyle="->", lw=0.6, color=C["chan"]))
    ax.annotate("holder (TPU, separate)\nwith T junction", (-49, -4.5), (-62, -11), fontsize=7,
                arrowprops=dict(arrowstyle="->", lw=0.6))
    ax.text(-53.5, 22.2, "lid (separate print): GPS deck", fontsize=7)
    ax.text(-52.5, 15.5, "keel\n(design)", fontsize=7)
    ax.annotate("rear lid bosses (-21, +-5)", (-21, 19), (-19.5, 28), fontsize=7, arrowprops=dict(arrowstyle="->", lw=0.6))
    ax.text(-22.7, -11.5, "tub", fontsize=7)
    ax.set_xlim(-64, -14); ax.set_ylim(-17, 33)
    ax.set_aspect("equal"); ax.grid(alpha=0.25)
    ax.set_xlabel("x (mm), forward ->"); ax.set_ylabel("z (mm)")
    ax.set_title(title, fontsize=9)


def plan(ax, link=False, title=""):
    xs = np.linspace(KEEL["x"][0], -23.0, 200)
    hw = np.array([keel_half_width(x, 15.0) for x in xs])
    ax.fill_between(xs, -9, 9, color=C["design"], lw=0)
    ax.text(-53.5, -13, "dotted: keel side above z = 10\n(cut by the rear prop sweep + 3)", fontsize=6.5)
    ax.plot([KEEL["x"][0], -23, -23, KEEL["x"][0], KEEL["x"][0]], [-9, -9, 9, 9, -9], "k", lw=0.8)
    ax.plot(xs, hw, "k:", lw=0.8)
    ax.plot(xs, -hw, "k:", lw=0.8)
    rect(ax, -23.0, -12.0, -BODY_H, BODY_H, fc=C["design"], ec="k", lw=0.6)
    rect(ax, -20.5, -12.0, -BAY, BAY, fc="w", ec="k", lw=0.4, ls="--")
    for sy in (1, -1):
        mx, my = -M, sy * M
        ax.add_patch(Circle((mx, my), R_PROP, fc="none", ec="m", ls="--", lw=0.7))
        # rear arm corridor, approximate: 10 mm wide band from the joint to the motor
        s = np.array([1.0, -sy]) / math.sqrt(2.0)       # unit vector along the arm, away from the centre is (-1, sy)
        u = np.array([-1.0, sy]) / math.sqrt(2.0)
        nrm = np.array([-u[1], u[0]])
        a, b = u * 30.0, u * (M * math.sqrt(2.0))
        ax.add_patch(Polygon([a + 5 * nrm, b + 5 * nrm, b - 5 * nrm, a - 5 * nrm], fc="#dddddd", ec="grey", lw=0.5, alpha=0.8))
        ax.add_patch(Circle((mx, my), 9.5, fc="#bbbbbb", ec="grey", lw=0.5))
    tube_2d(ax, K8, R8, 0, 1, fc="#f2a3a3")
    tube_2d(ax, K9, R9, 0, 1, fc="#cdb5e6")
    for (x, y) in LIDB[2:]:
        ax.add_patch(Circle((x, y), LIDB_R, fc=C["fixed"], ec="k", lw=0.5))
    rect(ax, *HOLDER["x"], *HOLDER["y"], fc=C["comp"], ec="k", lw=0.5, alpha=0.35)
    rect(ax, *JUNC["x"], *JUNC["y"], fc=C["comp"], ec="k", lw=0.5, alpha=0.9)
    ax.add_patch(Circle((ANT["x"], ANT["y"]), ANT["r"], fc=C["fixed"], ec="k", lw=0.8))
    for sy in (1, -1):
        x0, y0 = ANT["x"], sy * V_START
        ax.plot([x0, x0 - V_LEN * math.cos(math.radians(45))], [y0, y0 + sy * V_LEN * math.sin(math.radians(45))],
                color="#1b5e20", lw=2.5)
    if link:
        x0, x1, y0, y1, z0, z1 = L1["pad_lo"]; rect(ax, x0, x1, y0, y1, fc=C["link"], ec="k", lw=0.6, alpha=0.9)
        x0, x1, y0, y1, z0, z1 = L1["pad_hi"]; rect(ax, x0, x1, y0, y1, fc=C["link"], ec="k", lw=0.6, alpha=0.9)
        p0, p1, ty, tn = L1["strut"]
        rect(ax, p0[0], p1[0], p0[1] - ty / 2, p0[1] + ty / 2, fc=C["link"], ec="k", lw=0.6, alpha=0.9)
        ax.add_patch(Circle((-30.0, 0.0), LIDB_R, fc=C["fixed"], ec="k", lw=0.5))
    ax.text(-57.5, 30, "rear-left arm (approx.)", fontsize=7, color="grey")
    ax.text(-36, 39, "prop disc (blades z 13 to 18.5)", fontsize=7, color="m")
    ax.set_xlim(-64, -14); ax.set_ylim(-36, 42)
    ax.set_aspect("equal"); ax.grid(alpha=0.25)
    ax.set_xlabel("x (mm), forward ->"); ax.set_ylabel("y (mm), left")
    ax.set_title(title, fontsize=9)


def rear(ax, link=False, title=""):
    """Section x = -44 seen from behind (y to the right is -y, so mirror: plot -y on the horizontal axis)."""
    def Y(y):
        return -np.asarray(y)
    zz = np.linspace(0, RIM_Z, 100)
    hw = np.array([keel_half_width(-44.0, z) for z in zz])
    ax.fill_betweenx(zz, Y(hw), Y(-hw), color=C["design"], lw=0)
    ax.plot(np.r_[Y(hw), Y(-hw[::-1]), Y(hw[0])], np.r_[zz, zz[::-1], zz[0]], "k", lw=0.8)
    rect(ax, -10.0, 10.0, *LID_Z, fc=C["lidfix"], ec="k", lw=0.6, alpha=0.55)
    rect(ax, -6.0, 6.0, *GPS["z"], fc=C["comp"], ec="k", lw=0.5, alpha=0.8)
    rect(ax, -12.0, 12.0, *GPS_CAP["z"], fc=C["comp"], ec="k", lw=0.5, alpha=0.5)
    rect(ax, -ANT["r"], ANT["r"], *ANT["z"], fc=C["fixed"], ec="k", lw=0.8)
    rect(ax, -ANT["ins_r"], ANT["ins_r"], ANT["z"][0], ANT["ins_z"][1], fc="w", ec="k", lw=0.4)
    rect(ax, *HOLDER["y"], *HOLDER["z"], fc=C["comp"], ec="k", lw=0.5, alpha=0.45)
    rect(ax, *JUNC["y"], *JUNC["z"], fc=C["comp"], ec="k", lw=0.5, alpha=0.9)
    for sy in (1, -1):
        ax.plot([-sy * V_START, -sy * (V_START + V_LEN * math.sin(math.radians(45)))], [V_Z, V_Z], color="#1b5e20", lw=2.5)
    # channels in front of the section (x -40 to -36), dashed outlines
    k9v = K9[K9[:, 2] >= 10.0]
    yv = -k9v[:, 1].mean()
    rect(ax, yv - R9, yv + R9, 10.0, RIM_Z, fc="#9467bd", alpha=0.25, ec="#6a3d9a", ls="--", lw=0.6)
    rect(ax, -3.5 - R8, -3.5 + R8, -1.0, 8.75, fc=C["chan"], alpha=0.2, ec=C["chan"], ls="--", lw=0.6)
    ax.text(-14, 26.5, "channels drawn dashed lie 6 mm in front\nof this section (x -38), shown for position", fontsize=6.5)
    if link:
        x0, x1, y0, y1, z0, z1 = L1["pad_lo"]; rect(ax, -y1, -y0, z0, z1, fc=C["link"], ec="k", lw=0.6, alpha=0.9)
        p0, p1, ty, tn = L1["strut"]
        rect(ax, -(p0[1] + ty / 2), -(p0[1] - ty / 2), p0[2] - 2, p1[2] + 2, fc=C["link"], ec="k", lw=0.6, alpha=0.5, ls="--")
    ax.axhline(FLOOR_Z, color="#b22222", lw=1.5)
    ax.text(7.5, 13.5, "keel narrows above z = 10\n(rear prop sweep + 3 mm)", fontsize=6.5)
    ax.text(3.6, 17.5, "K9", fontsize=7, color="#6a3d9a")
    ax.text(-9.5, 7.5, "K8", fontsize=7, color=C["chan"])
    ax.text(-28, -9, "V element", fontsize=7, color="#1b5e20")
    ax.set_xlim(-30, 30); ax.set_ylim(-17, 33)
    ax.set_aspect("equal"); ax.grid(alpha=0.25)
    ax.set_xlabel("y (mm), seen from behind: right of the page = -y"); ax.set_ylabel("z (mm)")
    ax.set_title(title, fontsize=9)


def legend(fig, link=False):
    items = [(C["design"], "tub design region (Tosca decides)"), (C["fixed"], "tub fixed region (always kept)"),
             (C["lidfix"], "lid (separate part)"), (C["comp"], "components and retainers"),
             ("#f2a3a3", "K8 antenna channel dia 3.5 (keep-out)"), ("#cdb5e6", "K9 GPS channel dia 4 (keep-out)")]
    if link:
        items.append((C["link"], "proposed fixed link L1"))
    h = [Rectangle((0, 0), 1, 1, fc=c, ec="k", lw=0.4) for c, _ in items]
    fig.legend(h, [t for _, t in items], loc="lower center", ncol=4, fontsize=8, frameon=False)


def fig_current():
    f, axs = plt.subplots(1, 3, figsize=(17, 6.6), gridspec_kw=dict(width_ratios=[1.0, 1.0, 0.9]))
    side(axs[0], title="(a) side section on the centreline y = 0 (channels projected)")
    plan(axs[1], title="(b) plan view from above")
    rear(axs[2], title="(c) section at x = -44 through the boss, from behind")
    legend(f)
    f.suptitle("F-17: antenna boss in the v04-B design space (export revision 2). Nothing fixed links it to the frame;\n"
               "at H4 cycle 31 every keel element around it fell below density 0.3, so at iso 0.4 it is a loose 0.15 g part",
               fontsize=11)
    f.tight_layout(rect=(0, 0.06, 1, 0.93))
    f.savefig(os.path.join(OUT, "f17_1_current.png"), dpi=150)


def fig_link():
    f, axs = plt.subplots(1, 3, figsize=(17, 6.6), gridspec_kw=dict(width_ratios=[1.0, 1.0, 0.9]))
    side(axs[0], link=True, title="(a) side: L1 from the antenna boss up to the keel lid boss\n(it only overlaps K9 in this projection: it lies at y +1.6 to +4.8, K9 at y <= +0.5)")
    plan(axs[1], link=True, title="(b) plan: L1 passes on the +y side of K9 (centreline is blocked)")
    rear(axs[2], link=True, title="(c) section at x = -44: pad widens the boss to +y")
    axs[0].plot([-41.3, -32.7], [5.0, 15.5], color="k", ls=":", lw=1.2)
    axs[0].annotate("dotted: a straight strut on y = 0\nwould cut through K9", (-36.5, 11.5), (-33, -9), fontsize=7,
                    arrowprops=dict(arrowstyle="->", lw=0.6))
    legend(f, link=True)
    f.suptitle("Proposed fixed link L1 (TUB_FIXED): lower pad, 3.2 x 5 mm strut at y = +1.6 to +4.8, upper pad into the keel lid boss",
               fontsize=11)
    f.tight_layout(rect=(0, 0.06, 1, 0.95))
    f.savefig(os.path.join(OUT, "f17_2_link.png"), dpi=150)


def fig_antenna():
    f, axs = plt.subplots(1, 2, figsize=(12, 6.5))
    for ax, mode in zip(axs, ("V", "T")):
        rect(ax, KEEL["x"][0], -23.0, -9.0, 9.0, fc=C["design"], ec="k", lw=0.6)
        rect(ax, -23.0, -12.0, -BODY_H, BODY_H, fc=C["design"], ec="k", lw=0.6)
        for sy in (1, -1):
            mx, my = -M, sy * M
            ax.add_patch(Circle((mx, my), R_PROP, fc="none", ec="m", ls="--", lw=0.7))
            u = np.array([-1.0, sy]) / math.sqrt(2.0)
            nrm = np.array([-u[1], u[0]])
            a, b = u * 30.0, u * (M * math.sqrt(2.0))
            ax.add_patch(Polygon([a + 5 * nrm, b + 5 * nrm, b - 5 * nrm, a - 5 * nrm], fc="#dddddd", ec="grey", lw=0.5))
            ax.add_patch(Circle((mx, my), 9.5, fc="#bbbbbb", ec="grey", lw=0.5))
        rect(ax, *JUNC["x"], *JUNC["y"], fc=C["comp"], ec="k", lw=0.6)
        ax.add_patch(Circle((ANT["x"], 0), ANT["r"], fc=C["fixed"], ec="k", lw=0.6))
        for sy in (1, -1):
            if mode == "V":
                tip = (ANT["x"] - V_LEN * math.cos(math.radians(45)), sy * (V_START + V_LEN * math.sin(math.radians(45))))
                ax.plot([ANT["x"], tip[0]], [sy * V_START, tip[1]], color="#1b5e20", lw=3)
                ax.plot([ANT["x"]], [sy * V_START], "ro", ms=6)
            else:
                tip = (ANT["x"], sy * (V_START + V_LEN))
                ax.plot([ANT["x"], tip[0]], [sy * V_START, tip[1]], color="#1b5e20", lw=3)
            d = abs(tip[0] + sy * 0 + (-sy) * 0)
        if mode == "V":
            ax.set_title("As modelled: 90 deg V. Each element is bent 45 deg right where it\nleaves the moulded T junction (red dots)", fontsize=9)
            ax.annotate("tip about 26 mm from the arm axis", (-56.7, 19.7), (-62, 33), fontsize=7, arrowprops=dict(arrowstyle="->", lw=0.6))
        else:
            ax.set_title("Alternative: straight T (180 deg), no bend; elements along y\nunder the keel, tips at y = +-25", fontsize=9)
            ax.annotate("tip about 13 mm from the arm axis", (-44, 25), (-62, 33), fontsize=7, arrowprops=dict(arrowstyle="->", lw=0.6))
        ax.annotate("T junction 14 x 7.5 x 4\n(measured)", (-44, -5), (-38, -28), fontsize=7, arrowprops=dict(arrowstyle="->", lw=0.6))
        ax.set_xlim(-66, -14); ax.set_ylim(-38, 40); ax.set_aspect("equal"); ax.grid(alpha=0.25)
        ax.set_xlabel("x (mm), forward ->"); ax.set_ylabel("y (mm), left")
    f.suptitle("Receiver antenna under the keel, plan view (z = -2, 15 mm below the blade plane). Arm outline approximate",
               fontsize=11)
    f.tight_layout(rect=(0, 0, 1, 0.94))
    f.savefig(os.path.join(OUT, "f17_3_antenna.png"), dpi=150)


if __name__ == "__main__":
    report()
    fig_current()
    fig_link()
    fig_antenna()
    print("figures written to", OUT)
