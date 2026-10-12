# -*- coding: ascii -*-
"""
s04_reference_geometry.py - reference geometry (STEP) for quadcopter frame rev B.

Generates, from one parameter set (journal Stage 3 design-space table, D-024 to
D-032, D-036):
  revB_design_body_v01.step     centre-body design domain (keep-outs removed)
  revB_design_arms_v01.step     four arm corridors (separate parts, D-028)
  revB_nondesign_v01.step       battery plate, GPS pad, motor pads, FC bosses
  revB_keepout_v01.step         prop sweep, motors, FC, component void, battery,
                                strap tunnel, USB window, wire channels
  revB_reference_v01.step       all of the above in one file
  revB_params_v01.json          the parameters used
Coordinates: origin at frame centre, z = 0 on the arm top face, x forward,
y left, z up, mm. ASCII only. Requires cadquery.
"""
import json
import math
import cadquery as cq

P = {
    "wheelbase": 140.0,
    "prop_radius": 44.45,
    "prop_clearance": 3.0,
    "blade_z": [13.0, 18.5],
    "body_half": 20.0,
    "body_floor_z": -15.0,
    "body_chamfer_z": 10.0,
    "plate_top_z": 24.0,
    "plate_t": 2.5,
    "plate_xy": [64.0, 34.0],
    "arm_width": 10.0,
    "arm_root_zmin": -15.0,
    "arm_tip_zmin": -6.0,
    "motor_pad_d": 24.0,
    "motor_pad_t": 3.0,
    "motor_hole_pitch": 9.0,
    "motor_hole_d": 2.2,
    "motor_centre_hole_d": 6.0,
    "motor_d": 20.8,
    "motor_h": 15.5,
    "motor_clearance": 2.2,
    "fc_xy": [33.0, 33.0],
    "fc_z": [-6.0, 6.0],
    "fc_boss_pitch": 25.5,
    "fc_boss_d": 6.0,
    "fc_boss_hole_d": 3.2,
    "void_xy": [32.0, 32.0],
    "void_z": [6.0, 18.0],
    "tunnel_w_x": 18.0,
    "tunnel_z": [18.0, 21.0],
    "usb_w": 12.0,
    "usb_h": 8.0,
    "usb_z_centre": 2.0,
    "usb_side": "-y",
    "wire_channel": 5.0,
    "wire_channel_z_centre": -5.5,
    "gps_x": [-50.0, -30.0],
    "gps_y": [-10.0, 10.0],
    "battery": [59.0, 30.0, 32.0],
}

M = P["wheelbase"] / (2.0 * math.sqrt(2.0))
R_KEEP = P["prop_radius"] + P["prop_clearance"]
DIAG = [(1, 1), (1, -1), (-1, 1), (-1, -1)]


def box(x0, x1, y0, y1, z0, z1):
    return cq.Workplane("XY").box(x1 - x0, y1 - y0, z1 - z0, centered=False).translate((x0, y0, z0))


def zcyl(cx, cy, r, z0, z1):
    return cq.Workplane("XY").workplane(offset=z0).center(cx, cy).circle(r).extrude(z1 - z0)


# ---------------------------------------------------------------- keep-outs
def keepouts():
    parts = {}
    zb0 = P["blade_z"][0] - P["prop_clearance"]
    zb1 = P["blade_z"][1] + P["prop_clearance"]
    sweep = None
    motors = None
    for sx, sy in DIAG:
        c = zcyl(sx * M, sy * M, R_KEEP, zb0, zb1)
        sweep = c if sweep is None else sweep.union(c)
        m = zcyl(sx * M, sy * M, (P["motor_d"] + P["motor_clearance"]) / 2.0, 0.0, P["motor_h"])
        motors = m if motors is None else motors.union(m)
    parts["keepout_prop_sweep"] = sweep
    parts["keepout_motors"] = motors
    fx, fy = P["fc_xy"]
    parts["keepout_fc"] = box(-fx / 2, fx / 2, -fy / 2, fy / 2, P["fc_z"][0], P["fc_z"][1])
    vx, vy = P["void_xy"]
    parts["keepout_component_void"] = box(-vx / 2, vx / 2, -vy / 2, vy / 2, P["void_z"][0], P["void_z"][1])
    h = P["body_half"]
    tw = P["tunnel_w_x"]
    parts["keepout_strap_tunnel"] = box(-tw / 2, tw / 2, -h - 1, h + 1, P["tunnel_z"][0], P["tunnel_z"][1])
    uw, uh, uz = P["usb_w"], P["usb_h"], P["usb_z_centre"]
    ys = -1.0 if P["usb_side"] == "-y" else 1.0
    y0, y1 = sorted((ys * (fy / 2 - 1.0), ys * (h + 1.0)))
    parts["keepout_usb_window"] = box(-uw / 2, uw / 2, y0, y1, uz - uh / 2, uz + uh / 2)
    wc = P["wire_channel"]
    zc = P["wire_channel_z_centre"]
    chans = None
    for sx, sy in DIAG:
        ang = math.degrees(math.atan2(sy, sx))
        c = (cq.Workplane("XY").box(16.0, wc, wc).translate((h * math.sqrt(2.0) - 2.0, 0, zc))
             .rotate((0, 0, 0), (0, 0, 1), ang))
        chans = c if chans is None else chans.union(c)
    parts["keepout_wire_channels"] = chans
    bx, by, bz = P["battery"]
    parts["keepout_battery"] = box(-bx / 2, bx / 2, -by / 2, by / 2, P["plate_top_z"], P["plate_top_z"] + bz)
    return parts


# ---------------------------------------------------------------- design domains
def body_domain(ko):
    h = P["body_half"]
    lower = box(-h, h, -h, h, P["body_floor_z"], P["body_chamfer_z"])
    ch = (M * math.sqrt(2.0) - R_KEEP) * math.sqrt(2.0)   # |x| + |y| limit above the chamfer level
    c = ch - h
    octo = [(c, h), (-c, h), (-h, c), (-h, -c), (-c, -h), (c, -h), (h, -c), (h, c)]
    zt = P["plate_top_z"] - P["plate_t"]
    upper = (cq.Workplane("XY").workplane(offset=P["body_chamfer_z"])
             .polyline(octo).close().extrude(zt - P["body_chamfer_z"]))
    dom = lower.union(upper)
    for k in ("keepout_fc", "keepout_component_void", "keepout_strap_tunnel",
              "keepout_usb_window", "keepout_wire_channels", "keepout_prop_sweep"):
        dom = dom.cut(ko[k])
    return dom


def arm_domain(sx, sy):
    """Corridor along one diagonal; bottom rises from arm_root_zmin to arm_tip_zmin."""
    r0 = P["body_half"] * math.sqrt(2.0)
    r1 = M * math.sqrt(2.0)
    w = P["arm_width"]
    prof = [(r0, P["arm_root_zmin"]), (r1, P["arm_tip_zmin"]), (r1, 0.0), (r0, 0.0)]
    arm = (cq.Workplane("XZ").polyline(prof).close().extrude(w / 2.0, both=True))
    ang = math.degrees(math.atan2(sy, sx))
    return arm.rotate((0, 0, 0), (0, 0, 1), ang)


# ---------------------------------------------------------------- non-design
def nondesign():
    parts = {}
    px, py = P["plate_xy"]
    zt = P["plate_top_z"]
    parts["nd_battery_plate"] = box(-px / 2, px / 2, -py / 2, py / 2, zt - P["plate_t"], zt)
    gx, gy = P["gps_x"], P["gps_y"]
    parts["nd_gps_pad"] = box(gx[0], gx[1], gy[0], gy[1], zt - P["plate_t"], zt)
    pads = None
    hp = P["motor_hole_pitch"] / 2.0
    for sx, sy in DIAG:
        cx, cy = sx * M, sy * M
        pad = zcyl(cx, cy, P["motor_pad_d"] / 2.0, -P["motor_pad_t"], 0.0)
        pad = pad.cut(zcyl(cx, cy, P["motor_centre_hole_d"] / 2.0, -P["motor_pad_t"] - 1, 1))
        for hx in (-hp, hp):
            for hy in (-hp, hp):
                pad = pad.cut(zcyl(cx + hx, cy + hy, P["motor_hole_d"] / 2.0, -P["motor_pad_t"] - 1, 1))
        pads = pad if pads is None else pads.union(pad)
    parts["nd_motor_pads"] = pads
    bp = P["fc_boss_pitch"] / 2.0
    bosses = None
    for sx, sy in DIAG:
        b = zcyl(sx * bp, sy * bp, P["fc_boss_d"] / 2.0, P["body_floor_z"], P["fc_z"][0])
        b = b.cut(zcyl(sx * bp, sy * bp, P["fc_boss_hole_d"] / 2.0, P["body_floor_z"] + 2.0, P["fc_z"][0] + 1))
        bosses = b if bosses is None else bosses.union(b)
    parts["nd_fc_bosses"] = bosses
    return parts


def export(objs, fname):
    asm = cq.Assembly()
    for name, wp in objs.items():
        asm.add(wp, name=name)
    asm.save(fname, exportType="STEP")


def main():
    ko = keepouts()
    body = body_domain(ko)
    arms = {"design_arm_%s%s" % ("p" if sx > 0 else "m", "p" if sy > 0 else "m"): arm_domain(sx, sy) for sx, sy in DIAG}
    nd = nondesign()
    export({"design_body": body}, "revB_design_body_v01.step")
    export(arms, "revB_design_arms_v01.step")
    export(nd, "revB_nondesign_v01.step")
    export(ko, "revB_keepout_v01.step")
    allp = {"design_body": body}
    allp.update(arms); allp.update(nd); allp.update(ko)
    export(allp, "revB_reference_v01.step")
    for name, wp in [("design_body", body)] + list(arms.items())[:1] + list(nd.items()):
        print("%-24s volume %9.1f mm^3" % (name, wp.val().Volume()))
    with open("revB_params_v01.json", "w") as fh:
        json.dump(P, fh, indent=2)
    # STL for a quick visual check
    cq.exporters.export(body, "check_body.stl")
    cq.exporters.export(arms["design_arm_pp"], "check_arm.stl")
    cq.exporters.export(nd["nd_battery_plate"].union(nd["nd_gps_pad"]).union(nd["nd_motor_pads"]).union(nd["nd_fc_bosses"]), "check_nd.stl")


if __name__ == "__main__":
    main()
