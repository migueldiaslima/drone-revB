"""s07_gps_cap.py - GPS cap, production part (main chat, 2026-10-13).

TPU 95A HF retainer for the Flywoo GOKU GM10 Nano V3 with compass (12 x 17 x 5, listing) in the GPS pocket
of the rev 4 TUB deck (pocket inside x -52.8 to -35.2, y +-6.3, floor z 24, rim to z 26.5). Brief v04-B
section 5 (TPU cap with a window over the ceramic antenna, two M2 screws into inserts in the cap bosses),
D-073, D-086. Not part of the optimised model: its mass is in RP_GPS (4.23 g incl. cap 0.84 g estimate).

Shape: plate over the module (rounded 20 x 24, 1.2 thick) with a window over the antenna, clamping the
module top around the window with a small interference (TPU preload); two legs dia 5.4 standing on the cap
bosses at (-44, +-9.3), M2 clearance holes. The rim locates the module in x and y; the cap only holds it down.

Model frame (x forward, y left, z up), mm. Run from the repo root: python3 scripts/geometry_main/s07_gps_cap.py
Outputs geometry/retainers/: GPS_CAP_v1.step (model frame), GPS_CAP_v1_TPU.stl (print frame: plate top on the
bed, legs up), gps_cap_checks.json.
"""
import json
import os
import sys
import cadquery as cq

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))
import s06_geometry_v04B as v4      # noqa: E402

OUT = os.path.join(ROOT, "geometry", "retainers")
RHO_TPU = 1.21e-3                   # g/mm^3, same assumption as the antenna holder and the receiver cradle

L = v4.P["lid"]
CB = L["cap_boss"]                  # dia 5.4 at (-44, +-9.3), z 21.5 to 26.5, inserts dia 3.2 x 6.0
P = {
    "gps": {"L": 17.0, "W": 12.0, "H": 5.0, "x_c": v4.P["gps_cg"][0], "z0": L["rim_z"][0]},   # Flywoo listing; floor z 24
    "preload": 0.3,                 # plate underside below the module top (TPU interference)
    "plate": {"x": [-54.0, -34.0], "y": 12.0, "t": 1.2, "r": 2.0},
    "window": {"L": 9.0, "W": 9.0, "r": 1.0},          # centred on the module; assumed antenna centred (Q-63)
    "leg_d": CB["d"], "hole_d": 2.4,                   # M2 clearance in TPU (as the cradle ears)
    "bed_chamfer": 0.3,
}


def box(x0, x1, y0, y1, z0, z1):
    return cq.Workplane("XY").box(x1 - x0, y1 - y0, z1 - z0, centered=False).translate((x0, y0, z0))


def zcyl(x, y, r, z0, z1):
    return cq.Workplane("XY").workplane(offset=z0).center(x, y).circle(r).extrude(z1 - z0)


def dims():
    g = P["gps"]
    ztop_mod = g["z0"] + g["H"]
    zp0 = ztop_mod - P["preload"]
    return dict(z_mod_top=ztop_mod, zp0=zp0, zp1=zp0 + P["plate"]["t"], z_boss=CB["z"][1])


def build():
    d = dims()
    p = P["plate"]
    x0, x1 = p["x"]
    plate = (cq.Workplane("XY").workplane(offset=d["zp0"]).center(0.5 * (x0 + x1), 0)
             .rect(x1 - x0, 2 * p["y"]).extrude(p["t"]).edges("|Z").fillet(p["r"]))
    w = P["window"]
    win = (cq.Workplane("XY").workplane(offset=d["zp0"] - 1).center(P["gps"]["x_c"], 0)
           .rect(w["L"], w["W"]).extrude(p["t"] + 2).edges("|Z").fillet(w["r"]))
    body = plate.cut(win)
    for s in (1, -1):
        body = body.union(zcyl(CB["x"], s * CB["y"], P["leg_d"] / 2.0, d["z_boss"], d["zp0"] + 0.01))
        body = body.cut(zcyl(CB["x"], s * CB["y"], P["hole_d"] / 2.0, d["z_boss"] - 1, d["zp1"] + 1))
    try:
        body = body.faces(">Z").edges().chamfer(P["bed_chamfer"])     # plate top is the print bed side
    except Exception as ex:
        print("bed chamfer skipped:", ex)
    return body, d


def gps_dummy(d):
    g = P["gps"]
    return box(g["x_c"] - g["L"] / 2, g["x_c"] + g["L"] / 2, -g["W"] / 2, g["W"] / 2, g["z0"], d["z_mod_top"])


def vol(w):
    return sum(s.Volume() for s in w.solids().vals())


def cvol(a, b):
    try:
        return vol(a.intersect(b))
    except Exception:
        return float("nan")


def dist(a, b):
    return a.val().distance(b.val())


def checks(body, d):
    res = {}
    rec = lambda k, v, req, ok: res.__setitem__(k, {"value": v, "required": req, "pass": bool(ok)})
    V = vol(body)
    rec("solids", len(body.solids().vals()), 1, len(body.solids().vals()) == 1)
    rec("volume mm^3 / mass TPU g", "%.1f / %.2f" % (V, V * RHO_TPU), "estimate 0.84 g (in RP_GPS)", True)
    c = body.val().Center()
    rec("CG (x, y, z)", [round(c.x, 2), round(c.y, 2), round(c.z, 2)], "-", True)
    gd = gps_dummy(d)
    ov = cvol(body, gd)
    rec("clamp interference on the module top (mm^3, from %.1f mm preload)" % P["preload"], round(ov, 2), "> 0", ov > 0)
    g, w = P["gps"], P["window"]
    rec("clamp band around the window: x ends / y sides (mm)", [round((g["L"] - w["L"]) / 2, 2), round((g["W"] - w["W"]) / 2, 2)],
        ">= 1.0", min(g["L"] - w["L"], g["W"] - w["W"]) / 2 >= 1.0)
    K, cko = v4.keepouts()
    tub_d, tub_f, _, _ = v4.build_tub(K, cko)
    ovt = cvol(body, tub_d) + cvol(body, tub_f)
    rec("overlap with the TUB (mm^3)", round(ovt, 4), 0, ovt < 1e-4)
    rec("legs seated on the cap bosses (gap mm)", round(dist(body, tub_f), 4), 0, dist(body, tub_f) < 1e-6)
    rec("plate to the pocket rim top (mm)", round(d["zp0"] - L["rim_z"][1], 3), "> 0", d["zp0"] - L["rim_z"][1] > 0)
    lid_d, lid_f, _, _ = v4.build_lid()
    dl = min(dist(body, lid_d), dist(body, lid_f))
    rec("clearance to the LID (mm)", round(dl, 3), "> 0", dl > 0)
    C = v4.components()
    for k in ("battery", "strap"):
        rec("clearance to %s (mm)" % k, round(dist(body, C[k]), 3), "> 0", dist(body, C[k]) > 0)
    skip = ("gps_cap", "gps_module")
    inter = {k: round(cvol(body, s), 4) for k, s in C.items() if k not in skip and cvol(body, s) > 1e-4}
    rec("interference with other component dummies", inter, "none", not inter)
    rec("K9 cable hole under the module, not under the cap (no overlap mm^3)", round(cvol(body, K["K9_gps_channel"]), 4), 0,
        cvol(body, K["K9_gps_channel"]) < 1e-4)
    stack = d["zp1"] - d["z_boss"]
    rec("screw: plate + leg above the boss top (mm)", round(stack, 2), "M2 x 6 engages %.1f, M2 x 8 engages %.1f (insert hole 6.0 deep)"
        % (6 - stack, 8 - stack), True)
    rec("cap top / with M2 pan head (z)", [round(d["zp1"], 2), round(d["zp1"] + 1.3, 2)], "-", True)
    return res


def write_stl(shape, path, tol=0.02):
    vs, tris = shape.val().tessellate(tol, 0.2)
    with open(path, "w") as fh:
        fh.write("solid gps_cap\n")
        for a, b, c in tris:
            p0, p1, p2 = vs[a], vs[b], vs[c]
            n = (p1 - p0).cross(p2 - p0)
            ln = n.Length or 1.0
            fh.write(" facet normal %.6e %.6e %.6e\n  outer loop\n" % (n.x / ln, n.y / ln, n.z / ln))
            for p in (p0, p1, p2):
                fh.write("   vertex %.6f %.6f %.6f\n" % (p.x, p.y, p.z))
            fh.write("  endloop\n endfacet\n")
        fh.write("endsolid gps_cap\n")


def main():
    os.makedirs(OUT, exist_ok=True)
    body, d = build()
    res = checks(body, d)
    ok = all(v["pass"] for v in res.values())
    for k, v in res.items():
        print("%-66s %-36s %-30s %s" % (k, v["value"], v["required"], "ok" if v["pass"] else "FAIL"))
    cq.exporters.export(body, os.path.join(OUT, "GPS_CAP_v1.step"))
    printed = body.mirror("XY").translate((0, 0, d["zp1"]))     # plate top on the bed, legs up
    write_stl(printed, os.path.join(OUT, "GPS_CAP_v1_TPU.stl"))
    json.dump({"params": P, "dims": d, "checks": res, "all_pass": ok}, open(os.path.join(OUT, "gps_cap_checks.json"), "w"),
              indent=1, default=str)
    print("ALL PASS" if ok else "CHECK FAILURES")


if __name__ == "__main__":
    main()
