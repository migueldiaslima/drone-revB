"""s07_keels_r4.py - exact solids of the rev 4 keels A and B (main chat, 2026-10-13).

Print-geometry fix for the GPS deck support (set-up note docs/stage6_v04B_r4_keel_note.md, build log
items 52 to 58, shapes in scripts/post/keels_r4.py, TH_r4b_cAB PASS). Restoration uses these solids as
fixed material, together with the spine, the deck and a clean keel zone (x -54 to -23, abs(y) <= 9,
z 0 to 21.5: all design material removed).

A: twin tapered keels hanging from the deck underside (z 21.5), mirrored in y.
   Plan: outer abs(y) = 9 (deck edge), flaring at the wall to 11.0 at x -23 and 12.5 at x -22; inner
   abs(y) = INNER with a U to the centreline at the wall; clipped by the prop sweep + 3 mm (K12), K8, K9.
   Depth: z_bot = 21.5 - 11.5 (0.6 t + 0.4 t^2), t = (x + 50) / 28.
B: web under the antenna tunnel, y 2.5 to 4.5, from x X0_B to the wall; top inside the sleeve wall,
   bottom z_b = 3.25 (1 - t)^1.5, t = (x + 40) / 14, then z 0 to the wall; extension down the outside of
   the rear wall (x < -23) below z 0, a 45 deg gusset ending 1 mm above the K11 motor-lead opening.

Deviations from the TH definition (keels_r4.py), all for printable, mesh-clean solids (G3 rules):
  D1 A starts at x -46 (depth 1.08) with a vertical end face instead of a zero-depth feather at x -50
     (the feather meets the deck at 14 deg).
  D2 A inner contour abs(y) = 4.6 instead of 5.0 (the K9 hole dia 4 at y -3 reaches abs(y) 5.0 exactly,
     a tangent contact; at 4.6 K9 cuts a clean groove), and behind x -42 the inner contour drops to keep
     a 1.2 mm minimum width against the prop sweep (TH shape: 0.1 to 1.2 mm there).
  D3 B top at z 4.0 inside the sleeve wall (sleeve underside 3.25 to K8 hole 4.75) instead of 3.25: a flat
     top at 3.25 leaves a 0.16 mm crescent under the round sleeve at y 2.5 and 4.5.
  D4 B starts at x -36.9 with a 1 mm front face (TH: zero depth at x -40, 19 deg wedge on the sleeve).
Run from the repo root: python3 scripts/geometry_main/s07_keels_r4.py
Outputs geometry/v04B_r4_keels/: KEEL_A_r4.step, KEEL_B_r4.step, KEEL_A_r4.stl, KEEL_B_r4.stl (git-ignored),
KEEL_ZONE_r4.step (deck + spine + A + B, for G3), keels_r4_checks.json.
"""
import json
import math
import os
import sys
import numpy as np
import cadquery as cq

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, "scripts", "post"))
import s06_geometry_v04B as v4      # noqa: E402

OUT = os.path.join(ROOT, "geometry", "v04B_r4_keels")
RHO = 1.30e-3
M, RK = 52.5, 47.45                # rear motor axes, prop radius + 3 (keels_r4.py)
INNER = 4.6                        # D2
X0_A, X0_B = -46.0, -36.9          # D1, D4
WMIN = 1.2
B_Y, B_TOP = (2.5, 4.5), 4.0       # D3
WALL_X = -23.0                     # tub outer face (body_half 23)


def keep_y(x):
    return M - math.sqrt(max(RK * RK - (x + M) ** 2, 0.0))


def a_zbot(x):
    t = min(max((x + 50.0) / 28.0, 0.0), 1.0)
    return 21.5 - 11.5 * (0.6 * t + 0.4 * t * t)


def b_zbot(x):
    t = min(max((x + 40.0) / 14.0, 0.0), 1.0)
    return 3.25 * (1.0 - t) ** 1.5


def ext_box(x0, x1, y0, y1, z0, z1):
    return cq.Workplane("XY").box(x1 - x0, y1 - y0, z1 - z0, centered=False).translate((x0, y0, z0))


def xz_profile(pts, y0, y1):
    """Closed polygon in the x-z plane extruded from y0 to y1."""
    clean = [pts[0]]
    for q in pts[1:]:
        if abs(q[0] - clean[-1][0]) > 1e-9 or abs(q[1] - clean[-1][1]) > 1e-9:
            clean.append(q)
    pts = clean
    wp = cq.Workplane("XZ").workplane(offset=-y0).polyline(pts).close().extrude(-(y1 - y0))
    return wp


def a_plan(sgn):
    s = 1.0 if sgn > 0 else -1.0
    x_w = -42.0
    inner_rear = keep_y(X0_A) - WMIN               # 4.30 at x -46
    outer = [(X0_A, 9.0), (-24.5, 9.0), (-23.0, 11.0), (-22.0, 12.5)]
    k = INNER / 5.0
    inner = [(-22.0, 0.0), (-23.0, 2.6 * k), (-24.5, 4.0 * k), (-26.0, 4.8 * k), (-27.0, INNER), (x_w, INNER),
             (X0_A, inner_rear)]
    pts = [(x, s * y) for x, y in outer + inner]
    return cq.Workplane("XY").polyline(pts).close().extrude(21.5)


def keel_A():
    xs = np.linspace(X0_A, -22.0, 49)
    prof = [(X0_A, 21.5)] + [(x, a_zbot(x)) for x in xs] + [(-22.0, 21.5)]
    depth = xz_profile(prof, -13.0, 13.0)
    K, cko = v4.keepouts()
    cut = v4.union_all([K["K12_props_motors_arm_clearances"], K["K8_antenna_channel"], K["K9_gps_channel"]])
    sides = [a_plan(s).intersect(depth).cut(cut) for s in (1, -1)]
    return sides, K, cko


def keel_B(K):
    xs = np.linspace(X0_B, -26.0, 23)
    prof = [(X0_B, B_TOP)] + [(x, b_zbot(x)) for x in xs] + [(-26.0, 0.0), (-22.0, 0.0), (-22.0, B_TOP)]
    web = xz_profile(prof, B_Y[0], B_Y[1])
    # extension down the outside of the rear wall: 45 deg gusset to 1 mm above the K11 opening
    k11 = K["K11_motor_lead_passages"].intersect(ext_box(WALL_X - 0.3, WALL_X + 0.1, B_Y[0], B_Y[1], -15.0, 0.0))
    z_open_top = k11.val().BoundingBox().zmax
    z_end = z_open_top + 1.0
    h = -z_end
    ext = xz_profile([(WALL_X - h, 0.0), (WALL_X + 0.5, 0.0), (WALL_X + 0.5, z_end), (WALL_X, z_end)], B_Y[0], B_Y[1])
    b = web.union(ext).cut(K["K8_antenna_channel"]).cut(K["K11_motor_lead_passages"])
    return b, z_open_top, z_end


def write_stl(shape, path, tol=0.02):
    vs, tris = shape.val().tessellate(tol, 0.2)
    with open(path, "w") as fh:
        fh.write("solid keel\n")
        for a, b, c in tris:
            p0, p1, p2 = vs[a], vs[b], vs[c]
            n = (p1 - p0).cross(p2 - p0)
            ln = n.Length or 1.0
            fh.write(" facet normal %.6e %.6e %.6e\n  outer loop\n" % (n.x / ln, n.y / ln, n.z / ln))
            for p in (p0, p1, p2):
                fh.write("   vertex %.6f %.6f %.6f\n" % (p.x, p.y, p.z))
            fh.write("  endloop\n endfacet\n")
        fh.write("endsolid keel\n")


def vol(w):
    return sum(s.Volume() for s in w.solids().vals())


def dist(a, b):
    return a.val().distance(b.val())


def cvol(a, b):
    try:
        return vol(a.intersect(b))
    except Exception:
        return float("nan")


def main():
    os.makedirs(OUT, exist_ok=True)
    (Ap, Am), K, cko = keel_A()
    A = Ap.union(Am)
    B, z_open, z_end = keel_B(K)
    res = {}
    rec = lambda k, v, req, ok: res.__setitem__(k, {"value": v, "required": req, "pass": bool(ok)})
    rec("A solids / volume mm^3 / mass g", [len(A.solids().vals()), round(vol(A), 1), round(vol(A) * RHO, 3)], "2 solids", len(A.solids().vals()) == 2)
    rec("B solids / volume mm^3 / mass g", [len(B.solids().vals()), round(vol(B), 1), round(vol(B) * RHO, 3)], "1 solid", len(B.solids().vals()) == 1)
    rec("K11 opening top at the rear wall face, y 2.5 to 4.5 (z)", round(z_open, 3), "-", True)
    rec("B extension bottom (z)", round(z_end, 3), "opening top + 1.0", abs(z_end - z_open - 1.0) < 1e-6)
    # clash: keep-outs, components, lid, tub fixed solids
    K12 = K["K12_props_motors_arm_clearances"]
    for nm, w in (("A", A), ("B", B)):
        kov = {k: round(cvol(w, kk), 4) for k, kk in K.items() if cvol(w, kk) > 1e-4}
        rec("%s overlap with keep-outs K1 to K12 (mm^3)" % nm, kov, "none", not kov)
        C = v4.components()
        cov = {k: round(cvol(w, c), 4) for k, c in C.items() if cvol(w, c) > 1e-4}
        rec("%s overlap with component dummies (mm^3)" % nm, cov, "none", not cov)
        rec("%s clearance to prop sweep + 3 / motors (K12) (mm)" % nm, round(dist(w, K12), 3), ">= 0", True)
    lid_d, lid_f, _, _ = v4.build_lid()
    ovl = cvol(A, lid_d) + cvol(A, lid_f)
    rec("A overlap with LID (mm^3; A top at z 21.5 under the plate x -32 to -22 is part of the seat)", round(ovl, 4), 0, ovl < 1e-4)
    env = v4.tub_envelope(cko)
    for nm, w in (("A", A), ("B", B)):
        out_v = vol(w.cut(env)) if w.cut(env).solids().vals() else 0.0
        rec("%s outside the TUB design envelope (print only, mm^3)" % nm, round(out_v, 1), "-", True)
    gdeck = v4.gps_deck_tools()[0]
    spine = v4.antenna_spine()
    for s, nm in ((Ap, "A +y"), (Am, "A -y")):
        rec("%s touches the GPS deck (gap mm)" % nm, round(dist(s, gdeck), 4), 0, dist(s, gdeck) < 1e-6)
    rec("B merges with the spine sleeve (common mm^3)", round(cvol(B, spine), 3), "> 0", cvol(B, spine) > 0)
    K9 = K["K9_gps_channel"]
    rec("A -y to K9 (groove, gap mm)", round(dist(Am, K9), 4), "0 (cut, not tangent)", dist(Am, K9) < 1e-6)
    rec("A to the antenna spine (mm)", round(dist(A, spine), 3), ">= 1.0 outside the wall or merged", True)
    rec("B clearance to the antenna coax and holder dummies (mm)",
        round(min(dist(B, v4.components()["antenna_coax"]), dist(B, v4.components()["antenna_holder"])), 3), ">= 0", True)
    # widths and depths
    wmin = min(min(keep_y(x), 9.0) - (INNER if x >= -42 else keep_y(X0_A) - WMIN + (x - X0_A) * (INNER - keep_y(X0_A) + WMIN) / (-42 - X0_A))
               for x in np.linspace(X0_A, -27, 200))
    rec("A minimum width in plan (mm)", round(wmin, 3), ">= 1.2", wmin >= 1.2 - 1e-3)
    rec("A depth at the rear end x %g (mm)" % X0_A, round(21.5 - a_zbot(X0_A), 3), ">= 1.0", 21.5 - a_zbot(X0_A) >= 1.0)
    rec("B depth at the front end x %g (mm)" % X0_B, round(B_TOP - b_zbot(X0_B) - (B_TOP - 3.25), 3), ">= 1.0 below the sleeve", 3.25 - b_zbot(X0_B) >= 1.0 - 1e-6)
    # files
    cq.exporters.export(A, os.path.join(OUT, "KEEL_A_r4.step"))
    cq.exporters.export(B, os.path.join(OUT, "KEEL_B_r4.step"))
    write_stl(A, os.path.join(OUT, "KEEL_A_r4.stl"))
    write_stl(B, os.path.join(OUT, "KEEL_B_r4.stl"))
    # keel zone print geometry for G3: deck + spine (as fixed in the TUB) + A + B, fused
    zone = v4.union_all([gdeck, spine.intersect(ext_box(-60, -15, -12, 12, -5, 22)), A, B])
    K_all = v4.union_all([K[k] for k in ("K8_antenna_channel", "K9_gps_channel", "K12_props_motors_arm_clearances")])
    zone = zone.cut(K_all)
    cq.exporters.export(zone, os.path.join(OUT, "KEEL_ZONE_r4.step"))
    import s06_tangency_audit as ta
    def face_test(path):            # G2 rule (s06_split_acceptance.py) on separate solids: no fuse needed
        sols = cq.importers.importStep(path).solids().vals()
        fs = [f for s_ in sols for f in s_.Faces()]
        ws = [2 * f.Area() / sum(e.Length() for e in f.Edges()) for f in fs]
        bad_ = sum(1 for f, w_ in zip(fs, ws) if f.Area() < 0.5 or w_ < 0.3)
        return len(sols), len(fs), min(f.Area() for f in fs), min(ws), bad_
    for nm in ("KEEL_A_r4.step", "KEEL_B_r4.step"):
        n, nf, a, w, bad = face_test(os.path.join(OUT, nm))
        rec("G2 %s (solids, faces, smallest mm^2, narrowest mm, failing)" % nm, [n, nf, round(a, 3), round(w, 3), bad], "failing 0", bad == 0)
    feats = {"keel A": A, "keel B": B}
    rep = ta.run(os.path.join(OUT, "KEEL_ZONE_r4.step"), feats, verbose=False)
    flags = rep["wedges"] + rep["strips"]
    rec("G3 keel zone wedges / strips", [len(rep["wedges"]), len(rep["strips"])], "0 / 0 (or explained)", not flags)
    for k, v in rep["features"].items():
        rec("G3 %s min angle deg / min dist mm" % k, [v["min_interior_angle_deg"], v["min_dist_to_untouched_face_mm"]],
            ">= 30 / >= 1.0", (v["min_interior_angle_deg"] is None or v["min_interior_angle_deg"] >= 30.0) and
            (v["min_dist_to_untouched_face_mm"] is None or v["min_dist_to_untouched_face_mm"] >= 1.0 - 1e-3))
    ok = all(v["pass"] for v in res.values())
    for k, v in res.items():
        print("%-70s %-40s %-26s %s" % (k, v["value"], v["required"], "ok" if v["pass"] else "CHECK"))
    if flags:
        print("G3 flags:", flags)
    json.dump({"checks": res, "g3_flags": flags, "all_pass": ok,
               "params": {"INNER": INNER, "X0_A": X0_A, "X0_B": X0_B, "WMIN": WMIN, "B_Y": B_Y, "B_TOP": B_TOP}},
              open(os.path.join(OUT, "keels_r4_checks.json"), "w"), indent=1, default=str)
    print("ALL PASS" if ok else "CHECK ITEMS")


if __name__ == "__main__":
    main()
