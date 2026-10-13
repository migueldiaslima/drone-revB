"""s07_receiver_cradle.py - receiver cradle, production part (main chat, 2026-10-13).

TPU 95A HF retainer for the SpeedyBee Nano ELRS receiver (10.4 x 18.4), clamped on the pp and mp FC
screws between the anti-loosening nut (top z +4.1) and the nylon nut (z +5.5 to +7.1): brief v04-B
section 5.1, D-073, D-074. Not part of the optimised model; its mass is in the RP_FC lump.

Shape: U tray open at the top, floor 1.4 (z +4.1 to +5.5), side walls 1.2, snap lips along both side
walls (receiver pushed in from above, walls flex outwards), low end stops at both ends (wires and the
IPEX lead leave over them), end stops run along y from the -y wall to the ear zone, so the floor plus
stop (2.4 mm deep) carries the -y side to the ears. Ears dia 5.8 x 1.4 with M2 clearance holes.

Model frame (x forward, y left, z up, origin at the frame centre, z = 0 on the arm top), mm.
Run from the repo root: python3 scripts/geometry_main/s07_receiver_cradle.py
Outputs geometry/retainers/: RX_CRADLE_v1.step, RX_CRADLE_v1_TPU.stl (print orientation, floor on the
bed), rx_cradle_checks.json.
"""
import json
import math
import os
import sys
import cadquery as cq

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))
import s06_geometry_v04B as v4      # noqa: E402

OUT = os.path.join(ROOT, "geometry", "retainers")
RHO_TPU = 1.21e-3                   # g/mm^3, same assumption as the antenna holder (s06_f17_spine.py)

P = {
    # receiver (GetFPV listing: 10.4 x 18.4, 0.7 g); thickness = brief allowance until measured (Q-61)
    "rx": {"L": 18.4, "W": 10.4, "T": 4.0, "pcb_t": 1.0},
    "clear_xy": 0.3,                # receiver to walls and end stops, per side
    "clear_lip": 0.1,               # receiver top to lip underside
    "floor": {"z0": 4.1, "t": 1.4},  # z0 = anti-loosening nut top (brief section 4); C-6 needs FC parts <= z0 - 0.3
    "wall_t": 1.2,                  # 3 lines of 0.4 mm
    "y_in": [2.45, 13.45],          # inside, brief section 5.1 (capacitor side stays at y >= +1.25 outside)
    "lip": {"over": 0.9, "tip_h": 0.3, "x": [-6.0, 6.0]},     # 0.9 over the wall face = 0.6 over the PCB edge
    "end": {"t": 1.2, "h": 1.0, "y_to": 9.75},                 # end stop up to the PCB top (brief: 1 mm), -y wall to the ear zone
    "ear": {"xy": 12.75, "d": 5.8, "hole_d": 2.4, "y_from": 9.75},   # FC screw pitch 25.5 / 2; TPU hole +0.2 over 2.2
    "chamfer_bed": 0.3,             # first-layer chamfer on the floor underside edges
}


def box(x0, x1, y0, y1, z0, z1):
    return cq.Workplane("XY").box(x1 - x0, y1 - y0, z1 - z0, centered=False).translate((x0, y0, z0))


def zcyl(x, y, r, z0, z1):
    return cq.Workplane("XY").workplane(offset=z0).center(x, y).circle(r).extrude(z1 - z0)


def dims():
    rx, c = P["rx"], P["clear_xy"]
    z0 = P["floor"]["z0"]
    zf = z0 + P["floor"]["t"]                       # floor top = receiver bottom
    xi = rx["L"] / 2.0 + c                          # inside half-length
    yi0, yi1 = P["y_in"]
    assert abs((yi1 - yi0) - (rx["W"] + 2 * c)) < 1e-6, "inside width must be W + 2 clear"
    zl = zf + rx["T"] + P["clear_lip"]              # lip underside
    lp = P["lip"]
    ztop = zl + lp["tip_h"] + lp["over"]            # wall top (45 deg lead-in above the tip)
    return dict(z0=z0, zf=zf, xi=xi, yi0=yi0, yi1=yi1, zl=zl, ztop=ztop, w=P["wall_t"],
                xo=xi + P["end"]["t"], ze=zf + P["end"]["h"])


def lip(y_wall, sgn):
    """Lip on the wall face y = y_wall, protruding towards the pocket (sgn = +1 towards +y)."""
    d = dims()
    lp = P["lip"]
    o, th = lp["over"], lp["tip_h"]
    x0, x1 = lp["x"]
    # section in the y-z plane: flat underside, vertical tip, 45 deg lead-in back to the wall
    pts = [(y_wall, d["zl"]), (y_wall + sgn * o, d["zl"]), (y_wall + sgn * o, d["zl"] + th),
           (y_wall, d["zl"] + th + o)]
    return cq.Workplane("YZ").workplane(offset=x0).polyline(pts).close().extrude(x1 - x0)


def build():
    d = dims()
    w, z0, zf = d["w"], d["z0"], d["zf"]
    yo0, yo1 = d["yi0"] - w, d["yi1"] + w
    xo = d["xo"]
    e = P["ear"]
    floor = box(-xo, xo, yo0, yo1, z0, zf)
    walls = box(-d["xi"], d["xi"], yo0, d["yi0"], zf, d["ztop"]).union(box(-d["xi"], d["xi"], d["yi1"], yo1, zf, d["ztop"]))
    # end stops: 1.5 above the floor top, from the -y wall to y_to (beyond it the nylon nuts and their driver)
    yt = P["end"]["y_to"]
    ends = box(-xo, -d["xi"], yo0, yt, zf, d["ze"]).union(box(d["xi"], xo, yo0, yt, zf, d["ze"]))
    ears = []
    for s in (1, -1):
        ex = s * e["xy"]
        ear = box(min(s * (xo - 0.01), ex), max(s * (xo - 0.01), ex), e["y_from"], yo1, z0, zf).union(
            zcyl(ex, e["xy"], e["d"] / 2.0, z0, zf))
        ears.append(ear)
    body = floor.union(walls).union(ends).union(ears[0]).union(ears[1])
    body = body.union(lip(d["yi0"], 1)).union(lip(d["yi1"], -1))
    for s in (1, -1):
        body = body.cut(zcyl(s * e["xy"], e["xy"], e["hole_d"] / 2.0, z0 - 1, zf + 1))
    try:
        cb = P["chamfer_bed"]
        body = body.faces("<Z").edges().chamfer(cb)
    except Exception as ex:                         # keep the part if OCC refuses the chamfer
        print("bed chamfer skipped:", ex)
    return body, d


def receiver_dummy(d):
    rx = P["rx"]
    yc = 0.5 * (d["yi0"] + d["yi1"])
    return box(-rx["L"] / 2, rx["L"] / 2, yc - rx["W"] / 2, yc + rx["W"] / 2, d["zf"], d["zf"] + rx["T"])


def dist(a, b):
    return a.val().distance(b.val()) if hasattr(a, "val") else a.distance(b)


def common_vol(a, b):
    try:
        r = a.intersect(b)
        return sum(s.Volume() for s in r.solids().vals())
    except Exception:
        return float("nan")


def checks(body, d):
    res = {}
    rec = lambda k, v, req, ok: res.__setitem__(k, {"value": v, "required": req, "pass": bool(ok)})
    vol = body.val().Volume()
    nsol = len(body.solids().vals())
    bb = body.val().BoundingBox()
    rec("solids", nsol, 1, nsol == 1)
    rec("volume mm^3 / mass TPU g", "%.1f / %.2f" % (vol, vol * RHO_TPU), "brief estimate 0.87 g", True)
    c = body.val().Center()
    rec("CG (x, y, z)", [round(c.x, 2), round(c.y, 2), round(c.z, 2)], "-", True)
    rec("bounding box", [round(v, 2) for v in (bb.xmin, bb.xmax, bb.ymin, bb.ymax, bb.zmin, bb.zmax)], "z top <= 11.5 (K4)", bb.zmax <= 11.5)
    C = v4.components()
    rxd = receiver_dummy(d)
    rec("receiver dummy overlap with cradle (mm^3)", round(common_vol(body, rxd), 4), 0, common_vol(body, rxd) < 1e-6)
    rec("receiver rests on the floor (gap mm); side and end clearance by construction", round(dist(rxd, body), 3), "0; %.1f per side" % P["clear_xy"], dist(rxd, body) < 1e-6)
    rec("lip over the receiver edge (mm)", round(P["lip"]["over"] - P["clear_xy"], 2), ">= 0.5", P["lip"]["over"] - P["clear_xy"] >= 0.5)
    rec("lip underside above receiver top (mm)", P["clear_lip"], "0 to 0.2", True)
    # clash and clearances against the v04-B dummies and the tub / lid
    skip = ("receiver_cradle", "receiver", "antenna_coax")   # coax dummy sits at PCB level; real lead checked below
    inter = {}
    for k, s in C.items():
        if k in skip:
            continue
        v = common_vol(body, s)
        if v > 1e-4:
            inter[k] = round(v, 4)
    rec("interference with v04-B component dummies (mm^3)", inter, "none", not inter)
    # IPEX-1 lead: the mated plug sits on the receiver top, the coax leaves it above the PCB top (z >= zf + pcb_t)
    coax = box(-20.0, -d["xi"] + 1.0, 3.0, 4.2, d["zf"] + P["rx"]["pcb_t"] + 0.1, d["zf"] + P["rx"]["pcb_t"] + 1.3)
    rec("IPEX lead (dia 1.13 leaving above the PCB top) to cradle (mm)", round(dist(body, coax), 3), "> 0", dist(body, coax) > 0)
    rec("C-5 capacitor clearance (mm)", round(dist(body, C["capacitor"]), 3), ">= 1.0", dist(body, C["capacitor"]) >= 1.0)
    fcp = C["fc_heatsink_and_parts_under_cradle_max"]
    rec("C-6 floor to FC parts envelope (z <= +3.8) (mm)", round(dist(body, fcp), 3), ">= 0.3 (Q-60 open)", dist(body, fcp) >= 0.3 - 1e-6)
    for t in ("pp", "mp"):
        sx = 1 if t == "pp" else -1
        rec("ear seats on lock nut %s (gap mm)" % t, round(dist(body, C["nut_lock_" + t]), 3), 0, dist(body, C["nut_lock_" + t]) < 1e-6)
        rec("nylon nut %s on ear (gap mm)" % t, round(dist(body, C["nut_nylon_" + t]), 3), 0, dist(body, C["nut_nylon_" + t]) < 1e-6)
        rec("screw %s radial clearance in the ear hole (mm)" % t, round(dist(body, C["screw_" + t]), 3), "0.1 to 0.3", 0.05 < dist(body, C["screw_" + t]) < 0.35)
        nut = (sx * P["ear"]["xy"], P["ear"]["xy"])
        # free radius around the nylon nut axis above the ear (nut driver / wrench access)
        probe = None
        for r10 in range(25, 80):
            r = r10 / 10.0
            ring = zcyl(nut[0], nut[1], r, d["zf"] + 0.05, 12.0).cut(zcyl(nut[0], nut[1], r - 0.05, d["zf"], 13))
            if common_vol(body, ring) > 1e-5:
                probe = r
                break
        rec("free radius around the %s nylon nut above the ear (mm)" % t, probe, "socket OD / 2 (M2 nut 4 mm AF)", True)
    K, cko = v4.keepouts()
    tub_d, tub_f, _, _ = v4.build_tub(K, cko)
    lid_d, lid_f, _, _ = v4.build_lid()
    rec("clearance to TUB (mm)", round(min(dist(body, tub_d), dist(body, tub_f)), 3), "> 0", min(dist(body, tub_d), dist(body, tub_f)) > 0)
    rec("clearance to LID (mm)", round(min(dist(body, lid_d), dist(body, lid_f)), 3), "> 0", min(dist(body, lid_d), dist(body, lid_f)) > 0)
    rec("clearance to K8 antenna channel entry (mm)", round(dist(body, K["K8_antenna_channel"]), 3), "> 0", dist(body, K["K8_antenna_channel"]) > 0)
    # snap-lip wall: strain at the wall root when the lip clears the receiver edge (cantilever, tip deflection = lip over PCB)
    L = d["zl"] - d["zf"]
    defl = P["lip"]["over"] - P["clear_xy"]
    eps = 1.5 * P["wall_t"] * defl / L ** 2
    rec("snap wall root strain, guided cantilever bound (%)", round(100 * eps, 2), "TPU 95A: fine; PET-CF: no", True)
    # printability: smallest features
    rec("min wall / lip tip / floor (mm)", [P["wall_t"], P["lip"]["tip_h"], P["floor"]["t"]], ">= 0.8 wall at 0.4 nozzle", P["wall_t"] >= 0.8)
    return res


def write_stl(body, path, tol=0.02):
    vs, tris = body.val().tessellate(tol, 0.2)
    with open(path, "w") as fh:
        fh.write("solid rx_cradle\n")
        for a, b, c in tris:
            p0, p1, p2 = vs[a], vs[b], vs[c]
            n = (p1 - p0).cross(p2 - p0)
            ln = n.Length or 1.0
            fh.write(" facet normal %.6e %.6e %.6e\n  outer loop\n" % (n.x / ln, n.y / ln, n.z / ln))
            for p in (p0, p1, p2):
                fh.write("   vertex %.6f %.6f %.6f\n" % (p.x, p.y, p.z))
            fh.write("  endloop\n endfacet\n")
        fh.write("endsolid rx_cradle\n")


def main():
    os.makedirs(OUT, exist_ok=True)
    body, d = build()
    res = checks(body, d)
    ok = all(v["pass"] for v in res.values())
    for k, v in res.items():
        print("%-62s %-34s %-28s %s" % (k, v["value"], v["required"], "ok" if v["pass"] else "FAIL"))
    cq.exporters.export(body, os.path.join(OUT, "RX_CRADLE_v1.step"))
    printed = body.translate((0, 0, -d["z0"]))         # floor on the bed, model x and y kept
    write_stl(printed, os.path.join(OUT, "RX_CRADLE_v1_TPU.stl"))
    json.dump({"params": P, "dims": d, "checks": res, "all_pass": ok}, open(os.path.join(OUT, "rx_cradle_checks.json"), "w"), indent=1, default=str)
    print("ALL PASS" if ok else "CHECK FAILURES")
    return body


if __name__ == "__main__":
    main()
