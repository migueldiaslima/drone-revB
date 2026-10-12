# -*- coding: ascii -*-
"""
s06_reference_geometry_v02.py - reference geometry v02, quadcopter frame rev B.

Changes from v01 (s04_reference_geometry.py, kept unchanged and imported here):
  F-022  arm no longer touches the body along one edge: arms join the body only through
         the J3 fin-and-fork joint (D-047, D-048, D-049); arm and body are separate parts
  D-046  arm envelope: top z = +10 to the motor keep-out, R3 step down to z = 0, root
         20.3 mm wide (fork), tapering to 10 mm and blended (R5) into a 24 mm pad flange
  F-022  motor screw-head and shaft-clip clearances cut through the arm under the pad;
         motor wire exit keep-out
Local frame per arm: u along the arm (body corner at u = 28.28), v across, z up.

Outputs (stage6/geometry_v02/):
  revB_design_body_v02.step     body design domain (as v01)
  revB_design_arms_v02.step     four arm design domains
  revB_nondesign_v02.step       battery plate, GPS pad, FC bosses, motor pads, fins (with
                                root fillets and nose), prongs
  revB_keepout_v02.step         v01 keep-outs + screw heads, shaft clip, wire exit
  revB_hardware_v02.step        M3 x 20 bolts and M3 inserts (not in the FE model)
  revB_reference_v02.step       everything
  revB_params_v02.json
ASCII only. Requires cadquery.
"""
import json
import math
import os
import sys
import cadquery as cq
from OCP.BRepExtrema import BRepExtrema_DistShapeShape

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import s04_reference_geometry as g   # noqa: E402

OUT = os.path.join(HERE, "geometry_v02")
os.makedirs(OUT, exist_ok=True)

P = dict(g.P)
P.update({
    "version": "v02",
    "joint": "J3 fin and fork (D-047, D-048, D-049)",
    "fin_t": 10.0, "fin_z": [-15.0, 10.0], "fin_root_fillet": 5.0, "fin_u_start": 18.0,
    "bolt_u": 33.0, "bolt_z": [-9.0, 4.0], "bolt_d": 3.0, "bolt_hole_d": 3.2, "edge_dist": 6.0,
    "side_gap": 0.15, "nose_gap": 0.5,
    "prong_t": 5.0, "prong_u_start": 26.5,
    "insert_hole_d": 4.0, "insert_len": 4.0,
    "arm_top_z": 10.0, "arm_step_u": 55.5, "arm_step_fillet": 3.0, "motor_keepout_r": 11.5,
    "arm_fork_end_u": 40.0, "arm_taper_end_u": 62.0, "arm_tip_half_w": 5.0,
    "pad_flange_r": 12.0, "pad_blend_r": 5.0, "arm_bottom_under_pad": -6.0,
    "screw_head_clear_d": 4.5, "shaft_clear_d": 6.0, "wire_exit": [3.5, 5.0, 4.0],
})
UC = g.P["body_half"] * math.sqrt(2.0)   # 28.28, body corner along the arm
UM = g.M * math.sqrt(2.0)                # 70.0, motor axis
T_F, GAP_S, GAP_N = P["fin_t"], P["side_gap"], P["nose_gap"]
HALF_FIN = T_F / 2.0
V_IN = HALF_FIN + GAP_S               # 5.15, inner prong face
V_OUT = V_IN + P["prong_t"]           # 10.15, outer prong face
U_B = P["bolt_u"]
NOSE_C = U_B + P["edge_dist"] - HALF_FIN      # nose arc centre, tip at U_B + 6
NOSE_TIP = NOSE_C + HALF_FIN
SLOT_C = NOSE_C + GAP_N - GAP_S       # slot end arc centre (radius V_IN): tip gap = GAP_N
SLOT_TIP = SLOT_C + V_IN
Z0, Z1 = P["fin_z"]


def box(u0, u1, v0, v1, z0, z1):
    return cq.Workplane("XY").box(u1 - u0, v1 - v0, z1 - z0, centered=False).translate((u0, v0, z0))


def zcyl(u, v, r, z0, z1):
    return cq.Workplane("XY").workplane(offset=z0).center(u, v).circle(r).extrude(z1 - z0)


def vcyl(u, z, r, v0, v1):
    """Cylinder along +v from v0 to v1."""
    return cq.Workplane("XZ").workplane(offset=-v0).center(u, z).circle(r).extrude(-(v1 - v0))


def square_local(z0, z1):
    h = g.P["body_half"]
    sq = cq.Workplane("XY").box(2 * h, 2 * h, z1 - z0, centered=False).translate((-h, -h, z0))
    return sq.rotate((0, 0, 0), (0, 0, 1), -45)


def zbot(u):
    if u <= UC:
        return -15.0
    if u >= UM:
        return P["arm_bottom_under_pad"]
    return -15.0 + 9.0 * (u - UC) / (UM - UC)


# ---------------------------------------------------------------- joint, local frame
def _arc_mid(c, p0, p1, r, ccw=True):
    a0 = math.atan2(p0[1] - c[1], p0[0] - c[0])
    a1 = math.atan2(p1[1] - c[1], p1[0] - c[0])
    if ccw and a1 < a0:
        a1 += 2 * math.pi
    if not ccw and a1 > a0:
        a1 -= 2 * math.pi
    am = 0.5 * (a0 + a1)
    return (c[0] + r * math.cos(am), c[1] + r * math.sin(am))


def fin_local():
    """Fin (10 mm) outside the body square, with R5 plan-view root fillets against the two
    body corner faces and a full round nose. Built analytically in plan, extruded in z."""
    R = P["fin_root_fillet"]
    h = HALF_FIN
    vc = h + R
    uc = UC + R * math.sqrt(2.0) - vc            # fillet centre (uc, +-vc)
    t1 = (uc, h)                                  # tangent point on the fin side
    t2 = (uc - R / math.sqrt(2.0), vc - R / math.sqrt(2.0))   # tangent point on the body face
    wp = cq.Workplane("XY").workplane(offset=Z0).moveTo(*t2)
    wp = wp.threePointArc(_arc_mid((uc, vc), t2, t1, R, ccw=True), t1)
    wp = wp.lineTo(NOSE_C, h).threePointArc((NOSE_TIP, 0.0), (NOSE_C, -h)).lineTo(uc, -h)
    t2m = (t2[0], -t2[1])
    wp = wp.threePointArc(_arc_mid((uc, -vc), (uc, -h), t2m, R, ccw=True), t2m)
    wp = wp.lineTo(UC, 0.0).close()
    return wp.extrude(Z1 - Z0)


def slot_local():
    """Slot cut from the arm: 10.3 mm wide, round end with 0.5 mm nose gap."""
    s = box(0.0, SLOT_C, -V_IN, V_IN, -30, 30).union(zcyl(SLOT_C, 0, V_IN, -30, 30))
    return s


def prongs_local():
    """Non-design prongs: 5 mm plates from u = 26.5 to the fork end, inside the arm envelope."""
    u0, u1 = P["prong_u_start"], P["arm_fork_end_u"]
    pr = box(u0, u1, V_IN, V_OUT, -20, 20).union(box(u0, u1, -V_OUT, -V_IN, -20, 20))
    return pr.intersect(envelope_profile_local()).cut(slot_local())


def envelope_profile_local():
    """Side profile (u, z) of the arm envelope, extruded wide in v."""
    us, R = P["arm_step_u"], P["arm_step_fillet"]
    u_end = UM + P["pad_flange_r"]
    zt = P["arm_top_z"]
    wp = (cq.Workplane("XZ").moveTo(P["prong_u_start"] - 1.0, -15.0).lineTo(UC, -15.0)
          .lineTo(UM, P["arm_bottom_under_pad"]).lineTo(u_end, P["arm_bottom_under_pad"])
          .lineTo(u_end, 0.0).lineTo(us + R, 0.0)
          .threePointArc((us + R - R * math.cos(math.radians(45)), R - R * math.sin(math.radians(45))), (us, R))
          .lineTo(us, zt).lineTo(P["prong_u_start"] - 1.0, zt).close())
    return wp.extrude(40.0, both=True)


def plan_local():
    """Plan shape (u, v): 20.3 mm fork to u = 40, taper to 10 mm at u = 54, R5 blend into the
    24 mm pad flange. Built analytically, extruded in z."""
    u0, uf = P["prong_u_start"], P["arm_fork_end_u"]
    ut = 54.0
    hw, rf, rb = P["arm_tip_half_w"], P["pad_flange_r"], P["pad_blend_r"]
    vc = hw + rb
    uc = UM - math.sqrt((rf + rb) ** 2 - vc ** 2)          # blend centre (uc, +-vc)
    k = rf / (rf + rb)
    tc = (UM + (uc - UM) * k, vc * k)                      # tangent point on the flange circle
    wp = (cq.Workplane("XY").workplane(offset=-40).moveTo(u0, -V_OUT).lineTo(uf, -V_OUT)
          .lineTo(ut, -hw).lineTo(uc, -hw)
          .threePointArc(_arc_mid((uc, -vc), (uc, -hw), (tc[0], -tc[1]), rb, ccw=False), (tc[0], -tc[1]))
          .threePointArc((UM + rf, 0.0), tc)
          .threePointArc(_arc_mid((uc, vc), tc, (uc, hw), rb, ccw=False), (uc, hw))
          .lineTo(ut, hw).lineTo(uf, V_OUT).lineTo(u0, V_OUT).close())
    return wp.extrude(80)


def arm_design_local():
    a = plan_local().intersect(envelope_profile_local())
    a = a.cut(slot_local()).cut(prongs_local())
    return a


def hardware_local():
    bolts, ins, holes_fin, holes_arm = [], [], [], []
    for z in P["bolt_z"]:
        head = vcyl(U_B, z, 2.75, -V_OUT - 3.0, -V_OUT)
        shank = vcyl(U_B, z, 1.5, -V_OUT, -V_OUT + 20.0)
        bolts.append(head.union(shank))
        ins_body = vcyl(U_B, z, 2.3, V_OUT - P["insert_len"], V_OUT).cut(vcyl(U_B, z, 1.5, 0, 20))
        ins.append(ins_body)
        holes_fin.append(vcyl(U_B, z, P["bolt_hole_d"] / 2.0, -HALF_FIN - 1, HALF_FIN + 1))
        holes_arm.append(vcyl(U_B, z, P["bolt_hole_d"] / 2.0, -V_OUT - 1, V_OUT + 1)
                         .union(vcyl(U_B, z, P["insert_hole_d"] / 2.0, V_OUT - P["insert_len"], V_OUT + 1)))
    return bolts, ins, holes_fin, holes_arm


# ---------------------------------------------------------------- assembly in global frame
def to_global(wp, sx, sy):
    return wp.rotate((0, 0, 0), (0, 0, 1), math.degrees(math.atan2(sy, sx)))


def motor_clearances():
    ko = None
    hp = g.P["motor_hole_pitch"] / 2.0
    for sx, sy in g.DIAG:
        cx, cy = sx * g.M, sy * g.M
        k = zcyl(cx, cy, P["shaft_clear_d"] / 2.0, -20, 0.5)
        for hx in (-hp, hp):
            for hy in (-hp, hp):
                k = k.union(zcyl(cx + hx, cy + hy, P["screw_head_clear_d"] / 2.0, -20, -g.P["motor_pad_t"]))
                k = k.union(zcyl(cx + hx, cy + hy, g.P["motor_hole_d"] / 2.0, -20, 0.5))
        ko = k if ko is None else ko.union(k)
    return ko


def wire_exit_local():
    w, l, h = P["wire_exit"]
    return box(UM - P["motor_keepout_r"] - l, UM - P["motor_keepout_r"] + 0.5, -w / 2, w / 2, 0.0, h)


def min_dist(a, b):
    d = BRepExtrema_DistShapeShape(a.val().wrapped, b.val().wrapped)
    d.Perform()
    return d.Value()


def vol(wp):
    return sum(s.Volume() for s in wp.vals())


def build():
    ko = g.keepouts()
    body = g.body_domain(ko)
    nd = g.nondesign()
    mclear = motor_clearances()
    fin_l = fin_local()
    bolts_l, ins_l, hf_l, ha_l = hardware_local()
    fin_l = fin_l.cut(hf_l[0]).cut(hf_l[1])
    prongs_l = prongs_local().cut(ha_l[0]).cut(ha_l[1])
    arm_l = arm_design_local().cut(ha_l[0]).cut(ha_l[1]).cut(wire_exit_local())
    motor_ko_l = zcyl(UM, 0, P["motor_keepout_r"], 0.0, g.P["motor_h"])
    arm_l = arm_l.cut(motor_ko_l)
    parts = {"design_body": body}
    fins, prongs, arms, bolts, inserts, wires = None, None, {}, [], [], None
    for sx, sy in g.DIAG:
        tag = ("p" if sx > 0 else "m") + ("p" if sy > 0 else "m")
        f = to_global(fin_l, sx, sy)
        fins = f if fins is None else fins.union(f)
        p = to_global(prongs_l, sx, sy).cut(nd["nd_motor_pads"])
        prongs = p if prongs is None else prongs.union(p)
        a = to_global(arm_l, sx, sy).cut(mclear).cut(nd["nd_motor_pads"]).cut(ko["keepout_prop_sweep"])
        arms["design_arm_" + tag] = a
        bolts += [to_global(b, sx, sy) for b in bolts_l]
        inserts += [to_global(i, sx, sy) for i in ins_l]
        wx = to_global(wire_exit_local(), sx, sy)
        wires = wx if wires is None else wires.union(wx)
    nd2 = dict(nd)
    nd2["nd_fins"] = fins
    nd2["nd_prongs"] = prongs
    ko2 = dict(ko)
    ko2["keepout_motor_screws_shaft"] = mclear
    ko2["keepout_motor_wire_exit"] = wires
    hw = {"bolt_%02d" % i: b for i, b in enumerate(bolts)}
    hw.update({"insert_%02d" % i: x for i, x in enumerate(inserts)})
    return parts, arms, nd2, ko2, hw


def export(objs, fname):
    asm = cq.Assembly()
    for name, wp in objs.items():
        asm.add(wp, name=name)
    asm.export(os.path.join(OUT, fname), exportType="STEP")


def checks(parts, arms, nd2, ko2):
    body, fins, prongs = parts["design_body"], nd2["nd_fins"], nd2["nd_prongs"]
    a = arms["design_arm_pp"]
    rep = {}
    rep["fin_to_prong_gap"] = min_dist(fins, prongs)
    rep["fin_to_arm_design_gap"] = min_dist(fins, a)
    rep["body_to_arm_design_gap"] = min_dist(body, a)
    rep["body_to_prongs_gap"] = min_dist(body, prongs)
    rep["fin_overlap_body_mm3"] = vol(fins.intersect(body)) if fins.intersect(body).vals() else 0.0
    rep["arm_overlap_keepouts_mm3"] = sum(vol(a.intersect(k)) for k in ko2.values() if a.intersect(k).vals())
    rep["fin_touches_body_area_check_dist"] = min_dist(fins, body)
    rep["vol_body"] = vol(body)
    rep["vol_arm_each"] = vol(a)
    rep["vol_fins_total"] = vol(fins)
    rep["vol_prongs_total"] = vol(prongs)
    rep["vol_nondesign_total"] = sum(vol(w) for w in nd2.values())
    rep["nose_tip_u"] = NOSE_TIP
    rep["slot_tip_u"] = SLOT_TIP
    return rep


def main():
    parts, arms, nd2, ko2, hw = build()
    export(parts, "revB_design_body_v02.step")
    export(arms, "revB_design_arms_v02.step")
    export(nd2, "revB_nondesign_v02.step")
    export(ko2, "revB_keepout_v02.step")
    export(hw, "revB_hardware_v02.step")
    allp = dict(parts); allp.update(arms); allp.update(nd2); allp.update(ko2); allp.update(hw)
    export(allp, "revB_reference_v02.step")
    with open(os.path.join(OUT, "revB_params_v02.json"), "w") as fh:
        json.dump(P, fh, indent=2)
    rep = checks(parts, arms, nd2, ko2)
    with open(os.path.join(OUT, "revB_checks_v02.json"), "w") as fh:
        json.dump(rep, fh, indent=2)
    for k, v in rep.items():
        print("%-34s %10.3f" % (k, v))
    return parts, arms, nd2, ko2, hw


if __name__ == "__main__":
    main()
