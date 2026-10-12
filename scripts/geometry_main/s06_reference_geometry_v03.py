# -*- coding: ascii -*-
"""
s06_reference_geometry_v03.py - reference geometry v03, two variants (D-051 to D-053).

  B  repairable: J3 joint at D-049 sizes, only dia 12 bolt bosses fixed (fin 10 mm, prongs 5 mm);
     the rest of the fin and prongs is design space bounded by the D-048 shapes
  C  one-piece: no joint; body and arms one continuous design region
Common to both (changes from v02):
  battery plate and GPS pad: 3 mm perimeter frames fixed (plus the strap band across the
  plate), interiors design; motor pads: screw bosses (dia 6) and a motor contact ring (dia 16 to
  dia 20.8) fixed, rest of the pad design; insert holes from the outer prong face, 3 mm deep
  (2 mm shoulder); motor wire channels moved off the arm axis (v = 9.5 to 14.5) because the
  v01 channels ran through the fin (F-026); strap tunnel roof raised from z = 21 to the plate
  underside at z = 21.5, removing a 0.5 mm body sliver (F-027).
  D-054 (2026-10-08): arm design/fixed split with through-fork dia 12 bolt bosses, upper boss
  extended to the arm top (set-up chat F-8, F-9); FC boss cylinders removed from the design
  body (set-up chat DV-2). D-055: fin bosses extended. D-056: GPS keel design region.
Outputs: stage6/geometry_v03/{B,C}/... STEP per role, params, checks. ASCII only.
"""
import json
import math
import os
import sys
import cadquery as cq

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))
import s04_reference_geometry as g          # noqa: E402
import s06_reference_geometry_v02 as r      # noqa: E402

OUT = os.path.join(HERE, "geometry_v03")
g.P["tunnel_z"] = [18.0, 21.5]   # F-027: tunnel roof = plate underside (no 0.5 mm sliver)
P = dict(r.P)
P.update({
    "version": "v03",
    "boss_d": 12.0, "insert_len": 3.0,
    "plate_frame_w": 3.0, "strap_band_half_x": 9.0, "gps_frame_w": 3.0,
    "pad_ring_d": [16.0, 20.8], "pad_screw_boss_d": 6.0,
    "wire_channel_local": {"u": [11.5, 22.0], "v": [9.5, 14.5], "z": [-8.0, -3.0]},
    "variant_C_arm_u_start": 18.0,
    "fin_boss_extension": True,       # D-055 (Q-54): D-054 rule applied to the fin bosses
    # D-056 rev: GPS keel, flared by the prop keep-outs above z = 10, 1.86 mm clear of the fin root fillets
    "gps_keel": {"x": [-50.0, -19.0], "y_half": 9.0, "z": [0.0, 21.5]},
})
RHO = 1.30e-3   # g/mm^3
box, zcyl, vcyl = r.box, r.zcyl, r.vcyl
U_B, HALF_FIN, V_IN, V_OUT = r.U_B, r.HALF_FIN, r.V_IN, r.V_OUT


def vol(wp):
    return sum(s.Volume() for s in wp.vals()) if wp is not None and wp.vals() else 0.0


def union_all(lst):
    out = None
    for w in lst:
        if w is None or not w.vals():
            continue
        out = w if out is None else out.union(w)
    return out


# ---------------------------------------------------------------- local (one arm) pieces
def bolt_holes_local():
    holes = None
    for z in P["bolt_z"]:
        h = vcyl(U_B, z, P["bolt_hole_d"] / 2.0, -V_OUT - 1, V_OUT + 1)
        h = h.union(vcyl(U_B, z, P["insert_hole_d"] / 2.0, V_OUT - P["insert_len"], V_OUT + 1))
        holes = h if holes is None else holes.union(h)
    return holes


def bosses_local(v0, v1):
    return union_all([vcyl(U_B, z, P["boss_d"] / 2.0, v0, v1) for z in P["bolt_z"]])


def hardware_local():
    out = []
    for z in P["bolt_z"]:
        out.append(("bolt", vcyl(U_B, z, 2.75, -V_OUT - 3.0, -V_OUT).union(vcyl(U_B, z, 1.5, -V_OUT, -V_OUT + 20.0))))
        out.append(("insert", vcyl(U_B, z, 2.3, V_OUT - P["insert_len"], V_OUT).cut(vcyl(U_B, z, 1.5, 0, 20))))
    return out


def wire_channel_local():
    w = P["wire_channel_local"]
    return box(w["u"][0], w["u"][1], w["v"][0], w["v"][1], w["z"][0], w["z"][1])


def arm_envelope_C_local():
    """Arm envelope from u = 18 (inside the body square) to the pad, no slot."""
    u0 = P["variant_C_arm_u_start"]
    us, R, zt = P["arm_step_u"], P["arm_step_fillet"], P["arm_top_z"]
    u_end = r.UM + P["pad_flange_r"]
    prof = (cq.Workplane("XZ").moveTo(u0, -15.0).lineTo(r.UC, -15.0)
            .lineTo(r.UM, P["arm_bottom_under_pad"]).lineTo(u_end, P["arm_bottom_under_pad"])
            .lineTo(u_end, 0.0).lineTo(us + R, 0.0)
            .threePointArc((us + R - R * math.cos(math.radians(45)), R - R * math.sin(math.radians(45))), (us, R))
            .lineTo(us, zt).lineTo(u0, zt).close().extrude(40.0, both=True))
    plan = r.plan_local().union(box(u0, P["prong_u_start"] + 0.01, -V_OUT, V_OUT, -40, 40))
    return plan.intersect(prof)


# ---------------------------------------------------------------- global pieces
def to_g(wp, sx, sy):
    return r.to_global(wp, sx, sy)


def keepouts_v03():
    ko = dict(g.keepouts())
    ko["keepout_wire_channels"] = union_all([to_g(wire_channel_local(), sx, sy) for sx, sy in g.DIAG])
    ko["keepout_motor_screws_shaft"] = r.motor_clearances()
    ko["keepout_motor_wire_exit"] = union_all([to_g(r.wire_exit_local(), sx, sy) for sx, sy in g.DIAG])
    ko["keepout_motor_body"] = union_all([zcyl(sx * g.M, sy * g.M, P["motor_keepout_r"], 0.0, g.P["motor_h"]) for sx, sy in g.DIAG])
    return ko


def plate_parts():
    px, py = g.P["plate_xy"]
    zt, t = g.P["plate_top_z"], g.P["plate_t"]
    w = P["plate_frame_w"]
    plate = box(-px / 2, px / 2, -py / 2, py / 2, zt - t, zt)
    inner = box(-px / 2 + w, px / 2 - w, -py / 2 + w, py / 2 - w, zt - t - 1, zt + 1)
    band = box(-P["strap_band_half_x"], P["strap_band_half_x"], -py / 2, py / 2, zt - t, zt)
    nd = plate.cut(inner).union(band)
    gx, gy = g.P["gps_x"], g.P["gps_y"]
    gw = P["gps_frame_w"]
    gps = box(gx[0], gx[1], gy[0], gy[1], zt - t, zt)
    gin = box(gx[0] + gw, gx[1] - gw, gy[0] + gw, gy[1] - gw, zt - t - 1, zt + 1)
    gps_nd = gps.cut(gin).cut(plate)
    return nd, plate.cut(nd), gps_nd, gps.cut(plate).cut(gps_nd)


def pad_parts():
    nd_l, des_l = [], []
    hp = g.P["motor_hole_pitch"] / 2.0
    t = g.P["motor_pad_t"]
    for sx, sy in g.DIAG:
        cx, cy = sx * g.M, sy * g.M
        disc = zcyl(cx, cy, g.P["motor_pad_d"] / 2.0, -t, 0.0)
        ring = zcyl(cx, cy, P["pad_ring_d"][1] / 2.0, -t, 0.0).cut(zcyl(cx, cy, P["pad_ring_d"][0] / 2.0, -t - 1, 1))
        nd = ring
        for hx in (-hp, hp):
            for hy in (-hp, hp):
                nd = nd.union(zcyl(cx + hx, cy + hy, P["pad_screw_boss_d"] / 2.0, -t, 0.0))
        nd_l.append(nd)
        des_l.append(disc.cut(nd))
    return union_all(nd_l), union_all(des_l)


def build_common(ko):
    body = g.body_domain(ko)
    bosses_fc = g.nondesign()["nd_fc_bosses"]
    # DV-2: remove the full FC boss cylinders (bosses and their screw holes) from the design body
    bp = g.P["fc_boss_pitch"] / 2.0
    body = body.cut(union_all([zcyl(sx * bp, sy * bp, g.P["fc_boss_d"] / 2.0, g.P["body_floor_z"] - 1, g.P["fc_z"][0])
                               for sx, sy in g.DIAG]))
    # D-056 (Q-55): central keel design region under the GPS overhang, in the 2 mm wide corridor
    # between the two rear prop keep-outs (centreline is 2.05 mm outside both)
    k = P.get("gps_keel")
    if not k:
        keel = None
    else:
        keel = box(k["x"][0], k["x"][1], -k["y_half"], k["y_half"], k["z"][0], k["z"][1])
    if keel is None:
        plate_nd, plate_des, gps_nd, gps_des = plate_parts()
        pad_nd, pad_des = pad_parts()
        cut_all = [ko[kk] for kk in ("keepout_motor_screws_shaft", "keepout_motor_wire_exit", "keepout_motor_body", "keepout_prop_sweep")]
        return body, bosses_fc, plate_nd, plate_des, gps_nd, gps_des, pad_nd.cut(union_all(cut_all)), pad_des.cut(union_all(cut_all))
    keel_cut = keel
    for kk in ("keepout_prop_sweep", "keepout_strap_tunnel", "keepout_usb_window", "keepout_wire_channels"):
        keel_cut = keel_cut.cut(ko[kk])
    P["_keel_removed_by_keepouts_mm3"] = round(vol(keel) - vol(keel_cut), 3)
    body = body.union(keel_cut)
    plate_nd, plate_des, gps_nd, gps_des = plate_parts()
    pad_nd, pad_des = pad_parts()
    cut_all = [ko[k] for k in ("keepout_motor_screws_shaft", "keepout_motor_wire_exit", "keepout_motor_body", "keepout_prop_sweep")]
    pad_nd = pad_nd.cut(union_all(cut_all))
    pad_des = pad_des.cut(union_all(cut_all))
    return body, bosses_fc, plate_nd, plate_des, gps_nd, gps_des, pad_nd, pad_des


def cut_keepouts(wp, ko, keys):
    for k in keys:
        wp = wp.cut(ko[k])
    return wp


ARM_KO = ("keepout_motor_screws_shaft", "keepout_motor_wire_exit", "keepout_motor_body", "keepout_prop_sweep")
BODY_KO = ("keepout_fc", "keepout_component_void", "keepout_strap_tunnel", "keepout_usb_window",
           "keepout_wire_channels", "keepout_prop_sweep")


def build_B(common, ko):
    body, bfc, plate_nd, plate_des, gps_nd, gps_des, pad_nd, pad_des = common
    holes = bolt_holes_local()
    fin_env = r.fin_local()
    ftools = bosses_local(-HALF_FIN - 1, HALF_FIN + 1)
    if P.get("fin_boss_extension", False):
        # D-054 applied to the fin: bosses extended to the fin top and bottom (no tangency)
        zl, zu = min(P["bolt_z"]), max(P["bolt_z"])
        bd = P["boss_d"] / 2.0
        ftools = ftools.union(box(U_B - bd, U_B + bd, -HALF_FIN - 1, HALF_FIN + 1, zu, r.Z1 + 1.0))
        ftools = ftools.union(box(U_B - bd, U_B + bd, -HALF_FIN - 1, HALF_FIN + 1, r.Z0 - 1.0, zl))
    fin_b = ftools.intersect(fin_env)
    fin_nd_l, fin_des_l = fin_b.cut(holes), fin_env.cut(fin_b).cut(holes)
    # D-054: through-fork dia 12 bosses, upper boss extended to the arm top; one tool set
    # splits the whole arm envelope, so design and fixed faces coincide (no tangent slivers)
    env = r.arm_design_local().union(r.prongs_local())
    tools = bosses_local(-V_OUT - 1, V_OUT + 1)
    zu = max(P["bolt_z"])
    tools = tools.union(box(U_B - P["boss_d"] / 2.0, U_B + P["boss_d"] / 2.0, -V_OUT - 1, V_OUT + 1, zu, P["arm_top_z"] + 1.0))
    pr_nd_l = env.intersect(tools).cut(holes)
    arm_l = env.cut(tools).cut(holes)
    hw_l = hardware_local()
    fin_nd, fin_des, pr_nd, arms, hw = [], [], [], {}, {}
    for sx, sy in g.DIAG:
        tag = ("p" if sx > 0 else "m") + ("p" if sy > 0 else "m")
        fin_nd.append(to_g(fin_nd_l, sx, sy))
        fin_des.append(cut_keepouts(to_g(fin_des_l, sx, sy), ko, ("keepout_wire_channels",)))
        pr_nd.append(to_g(pr_nd_l, sx, sy))
        a = to_g(arm_l, sx, sy)
        a = cut_keepouts(a, ko, ARM_KO).cut(pad_nd)
        a = a.union(pad_des.intersect(zcyl(sx * g.M, sy * g.M, 13.0, -10, 10)))
        arms["design_arm_" + tag] = a
        for i, (kind, w) in enumerate(hw_l):
            hw["%s_%s_%d" % (kind, tag, i)] = to_g(w, sx, sy)
    body_des = body.union(plate_des).union(gps_des).union(union_all(fin_des))
    parts = {
        "body_design": body_des,
        "body_nd_fin_bosses": union_all(fin_nd),
        "body_nd_fc_bosses": bfc,
        "body_nd_plate_frame": plate_nd,
        "body_nd_gps_frame": gps_nd,
        "arm_nd_prong_bosses": union_all(pr_nd),
        "arm_nd_motor_pads": pad_nd,
    }
    parts.update(arms)
    return parts, hw


def build_C(common, ko):
    body, bfc, plate_nd, plate_des, gps_nd, gps_des, pad_nd, pad_des = common
    arms = []
    for sx, sy in g.DIAG:
        a = to_g(arm_envelope_C_local(), sx, sy)
        a = cut_keepouts(a, ko, ARM_KO + BODY_KO).cut(pad_nd).cut(bfc)
        a = a.union(pad_des.intersect(zcyl(sx * g.M, sy * g.M, 13.0, -10, 10)))
        arms.append(a)
    des = body.union(plate_des).union(gps_des).union(union_all(arms))
    parts = {
        "frame_design": des,
        "nd_fc_bosses": bfc,
        "nd_plate_frame": plate_nd,
        "nd_gps_frame": gps_nd,
        "nd_motor_pads": pad_nd,
    }
    return parts, {}


def export(objs, path):
    asm = cq.Assembly()
    for name, wp in objs.items():
        if wp is not None and wp.vals():
            asm.add(wp, name=name)
    asm.export(path, exportType="STEP")


def table(parts):
    rows = {}
    for k, w in parts.items():
        rows[k] = {"vol_mm3": round(vol(w), 1), "mass_solid_g": round(vol(w) * RHO, 2)}
    nd = sum(v["mass_solid_g"] for k, v in rows.items() if "_nd" in k or k.startswith("nd_"))
    des = sum(v["mass_solid_g"] for k, v in rows.items() if "design" in k)
    rows["_sum"] = {"fixed_g": round(nd, 2), "design_solid_g": round(des, 2), "left_in_61.4g_budget": round(61.4 - nd, 2)}
    return rows


def main():
    ko = keepouts_v03()
    common = build_common(ko)
    res = {}
    for name, fn in (("B", build_B), ("C", build_C)):
        d = os.path.join(OUT, name)
        os.makedirs(d, exist_ok=True)
        parts, hw = fn(common, ko)
        for k, w in parts.items():
            export({k: w}, os.path.join(d, "revB_v03%s_%s.step" % (name, k)))
        allp = dict(parts); allp.update(hw); allp.update({k: v for k, v in ko.items()})
        export(allp, os.path.join(d, "revB_v03%s_reference.step" % name))
        if hw:
            export(hw, os.path.join(d, "revB_v03%s_hardware.step" % name))
        t = table(parts)
        if name == "B":
            fin_all = union_all([parts["body_design"], parts["body_nd_fin_bosses"]])
            arm_all = union_all([parts[k] for k in parts if k.startswith("design_arm")] + [parts["arm_nd_prong_bosses"]])
            t["_checks"] = {"body_to_arm_min_gap_mm": round(r.min_dist(fin_all, arm_all), 3),
                            "arm_overlap_keepouts_mm3": round(sum(vol(arm_all.intersect(v)) for v in ko.values()), 3)}
        else:
            t["_checks"] = {"design_overlap_keepouts_mm3": round(sum(vol(parts["frame_design"].intersect(ko[k])) for k in ARM_KO + BODY_KO), 3)}
        with open(os.path.join(d, "revB_v03%s_mass_table.json" % name), "w") as fh:
            json.dump(t, fh, indent=2)
        res[name] = t
        print(name, json.dumps(t, indent=1))
    with open(os.path.join(OUT, "revB_params_v03.json"), "w") as fh:
        json.dump(P, fh, indent=2)
    return res


if __name__ == "__main__":
    main()
