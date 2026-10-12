# -*- coding: ascii -*-
"""
s06_geometry_v04B.py - v04-B geometry, revision 3 (2026-10-12, F-17): antenna spine replaces the
antenna boss; antenna channel K8 rerouted (z 6.5, one R7 bend, exit at (-49, +3.5)); GPS channel K9
and the lid GPS hole moved 1.5 mm to -y; straight T antenna hanging stem-up under the K8 exit in a
TPU holder (components). Spine shape, clearances and the holder are defined and checked in
s06_f17_spine.py (geometry/v04B_r3_f17/checks.json); this file builds the CAD version of the same
primitives without the blend fillets (the restoration uses the filleted SPINE_fixed_v04B_r3.stl).
Revision 2 (H4, TH04) is kept as git history and geometry/v04B/.

Revision 1 (2026-10-11): assemblable tub plus removable
lid (D-072 to D-078) with the 46 x 46 body and 148.5 mm wheelbase (D-079), the antenna channel
through the keel at receiver height, the 11 x 7 pigtail window and the C cutout in the lid tab
(D-080). Revision 0 (40 x 40 body) is kept in abaqus_v04B_r0/.

Writes stage6/abaqus_v04B/:
  TUB.step              TUB_DESIGN, TUB_FIXED (fin bosses, FC bosses, lid bosses, antenna spine)
  LID.step              LID_DESIGN, LID_FIXED (plate frame and strap band, GPS deck with pocket
                        rim and cap bosses, screw pads, front tab)
  ARM_xx.step           the v03-B arms (D-054, D-059), unchanged in shape, moved 3 mm in x and
                        3 mm in y away from the centre with their corner
  KEEPOUTS_v04B.step    K1 to K12 as named solids
  COMPONENTS_v04B.step  component dummies for the clash check (gate G5)
  reference_points_v04B.csv
  v04B_volumes.json
Every corner feature (fin, arm, motor, prop sweep, motor-lead passage) is the v03-B feature
moved by (3 sx, 3 sy, 0), so the joint, the arm and the arm-to-motor geometry are unchanged.
Coordinates: x forward, y left, z up, origin at the frame centre, z = 0 on the arm top. mm.
ASCII only. Requires cadquery.
"""
import csv
import json
import math
import os
import sys
import cadquery as cq
from OCP.BRepPrimAPI import BRepPrimAPI_MakeTorus, BRepPrimAPI_MakeRevol
from OCP.gp import gp_Ax1, gp_Ax2, gp_Dir, gp_Pnt

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))
import s06_reference_geometry_v03 as v3     # noqa: E402

g, r = v3.g, v3.r
OUT = os.path.join(HERE, "abaqus_v04B")
SRC_ARMS = os.path.join(HERE, "abaqus_v03B")
RHO = 1.30e-3
SHIFT = 3.0                                   # per axis; 4.243 mm along each diagonal
M_NEW = g.M + SHIFT                           # motor axis coordinate, 52.497
R_KEEP = g.R_KEEP                             # 47.45, prop radius + 3 mm

P = {
    "version": "v04B rev 3",
    "body_half": 23.0, "rim_z": 21.5, "floor_z": -15.0, "chamfer_z": 10.0,
    "motor_xy": M_NEW, "wheelbase": 2.0 * M_NEW * math.sqrt(2.0),
    "bay": {"xy": 20.5, "z": [-6.0, 21.5]},
    "fc_boss": {"pitch": 25.5, "d": 6.4, "hole_d": 2.2, "cb_d": 4.2, "cb_depth": 1.5},
    "lid_boss": {"d": 6.0, "z": [15.5, 21.5], "insert_d": 3.2, "insert_depth": 4.5,
                 "xy": [(21.0, 9.5), (21.0, -9.5), (-21.0, 5.0), (-21.0, -5.0), (-30.0, 0.0)]},
    "boss_wedge_z": [11.5, 15.5],          # 45 deg design support under the wall bosses, into the bay
    "inner_chamfer_wall": 2.5,             # corner walls above z = 10 (octagon restored)
    "fillets": {"keel_root": 2.0, "bay_corner": 2.0, "pigtail_window": 0.75,
                "usb_window": 0.75, "strap_notch": 1.0, "lid_tab_root": 2.0, "lid_deck_root": 3.0,
                },
    "keel": {"x": [-54.0, -22.0], "y_half": 9.0, "z": [0.0, 21.5]},
    # F-17 (rev 3): antenna spine, TUB fixed. Sleeve wall 1.5 around K8 from the bay face to the exit, pad in the
    # keel underside with an M2 x 3 heat-set insert and a locating hole, web up the rear wall into the rear lid boss
    "ant_spine": {"wall": 1.5, "pad": [(-53.0, -39.0), (-8.0, 8.0), (0.0, 2.2)],
                  "insert_xy": (-43.0, -1.0), "boss_d": 6.6, "boss_z": [0.0, 5.7], "insert_d": 3.2, "insert_depth": 4.0,
                  "peg_xy": (-43.0, -5.3), "peg_d": 2.0, "peg_depth": 1.1,
                  "web": [(-21.9, 4.6, 8.0), (-21.5, 5.0, 16.5)], "web_d": 3.5},
    "antenna": {"x": -49.0, "y": 3.5, "bar": (4.0, 14.0, 4.5), "stem": (3.0, 3.2, 3.0), "stem_top": -0.5,
                "leg_d": 1.4, "span": 50.0, "cap_d": 4.0, "cap_len": 5.0},
    "pigtail_window": {"y": [-10.0, 1.0], "z": [-1.8, 5.2]},
    "pigtail_low_run": {"x": [23.0, 33.0], "y": [-12.0, 3.0], "z": [-3.0, 3.0]},
    "pigtail_riser": {"x": [28.5, 33.0], "y": [-3.0, 3.0], "z": [0.0, 21.5]},
    "pigtail_under_plate": {"x": [28.5, 41.0], "y": [-1.75, 1.75], "z": [18.0, 21.5]},
    "usb_window": {"x": [-1.1, 11.9], "z": [-2.0, 6.0]},
    "usb_plug": {"x_c": 5.4, "z_c": 1.5, "shell": [8.4, 2.6], "shell_y": [-16.5, -23.5],
                 "overmold": [12.0, 7.0], "overmold_y": [-23.5, -40.0]},
    "ant_channel": {"d": 3.5, "y": 3.5, "z_h": 6.5, "x_bend": -42.0, "R": 7.0},                 # rev 3 (rev 2: z 7, x -33, R 5)
    "gps_channel": {"d": 4.0, "x_v": -38.2, "y_v": -3.0, "z_bend": 10.0, "R": 5.0, "z_h": 5.0,   # rev 3: y_v -3.0 (rev 2: -1.5)
                    "wall_hole": (-23.0, -5.0)},                                       # rev 3 (rev 2: y -3.5)
    "strap_notch": {"x": [-9.0, 9.0], "z": [18.0, 21.5]},
    "nut_col": {"d": 8.0, "z": [1.6, 21.5]},
    "lid": {"plate": [64.0, 34.0], "z": [21.5, 24.0], "frame_w": 3.0, "band_half_x": 9.0,
            "deck_x": [-54.0, -30.0], "deck_y": 10.0,
            "pocket_in": {"x": [-52.8, -35.2], "y": 6.3}, "rim_t": 1.2, "rim_z": [24.0, 26.5],
            "cap_boss": {"d": 5.4, "y": 9.3, "x": -44.0, "z": [21.5, 26.5], "insert_d": 3.2, "insert_depth": 6.0},
            "pad_d": [6.0, 6.0, 6.0, 6.0, 6.0], "pad_hole_d": 2.2, "csk_d": 3.8,
            "gps_hole": (-38.2, -3.0, 4.0),                                      # rev 3 (rev 2: y -1.5)
            "tab": {"x": [32.0, 42.0], "y": 9.0},
            "c_cut": {"pocket_x": [35.8, 39.2], "pocket_y": 3.2, "entry_half": 1.3}},
    "gps_cg": (-44.0, 0.0, 26.5),
}

box, zcyl = g.box, g.zcyl
vol, union_all = v3.vol, v3.union_all
CORNERS = {"pp": (1, 1), "pm": (1, -1), "mp": (-1, 1), "mm": (-1, -1)}


def xcyl(y, z, rad, x0, x1):
    return cq.Workplane("YZ").workplane(offset=x0).center(y, z).circle(rad).extrude(x1 - x0)


def cone(cx, cy, z0, r0, z1, r1):
    return cq.Workplane("XY").add(cq.Solid.makeCone(r0, r1, z1 - z0, cq.Vector(cx, cy, z0), cq.Vector(0, 0, 1)))


def sel(wp, p0, p1):
    return wp.edges(cq.selectors.BoxSelector(p0, p1))


def octagon_prism(ch, half, z0, z1):
    """Prism with |x|, |y| <= half and |x| + |y| <= ch."""
    c = ch - half
    pts = [(c, half), (-c, half), (-half, c), (-half, -c), (-c, -half), (c, -half), (half, -c), (half, c)]
    return cq.Workplane("XY").workplane(offset=z0).polyline(pts).close().extrude(z1 - z0)


def outer_chamfer():
    return (M_NEW * math.sqrt(2.0) - R_KEEP) * math.sqrt(2.0)      # |x| + |y| limit above z = 10 (prop sweep + 3)


def boss_wedges():
    """45 deg design support under the four wall bosses, from the wall face into the bay."""
    lb = P["lid_boss"]; a = P["bay"]["xy"]; z0, z1 = P["boss_wedge_z"]; r_ = lb["d"] / 2.0
    out = []
    for x, y in lb["xy"][:4]:
        sx = 1.0 if x > 0 else -1.0
        prof = [(sx * a, z0), (sx * (a + 12.0), z0), (sx * (a + 12.0), z1), (sx * (a - (z1 - z0)), z1)]   # 45 deg
        half = cq.Workplane("XZ").polyline(prof).close().extrude(40.0, both=True)
        out.append(zcyl(x, y, r_, z0, z1).intersect(half))
    return union_all(out)


def corner(local, sx, sy):
    """v03-B local feature rotated to its corner and moved out with it."""
    return v3.to_g(local, sx, sy).translate((SHIFT * sx, SHIFT * sy, 0.0))


def torus_quarter(centre, axis, xdir, R, rad):
    ax = gp_Ax2(gp_Pnt(*centre), gp_Dir(*axis), gp_Dir(*xdir))
    return cq.Workplane("XY").add(cq.Shape.cast(BRepPrimAPI_MakeTorus(ax, R, rad, math.pi / 2).Shape()))


# ------------------------------------------------------------------ corner features (moved v03-B)
def corner_keepouts():
    ko = {}
    ko["prop_sweep"] = union_all([zcyl(sx * M_NEW, sy * M_NEW, R_KEEP, g.P["blade_z"][0] - 3.0, g.P["blade_z"][1] + 3.0)
                                  for sx, sy in g.DIAG])
    ko["motor_body"] = union_all([zcyl(sx * M_NEW, sy * M_NEW, v3.P["motor_keepout_r"], 0.0, g.P["motor_h"])
                                  for sx, sy in g.DIAG])
    hp = g.P["motor_hole_pitch"] / 2.0
    clr = []
    for sx, sy in g.DIAG:
        cx, cy = sx * M_NEW, sy * M_NEW
        k = zcyl(cx, cy, r.P["shaft_clear_d"] / 2.0, -20, 0.5)
        for hx in (-hp, hp):
            for hy in (-hp, hp):
                k = k.union(zcyl(cx + hx, cy + hy, r.P["screw_head_clear_d"] / 2.0, -20, -g.P["motor_pad_t"]))
                k = k.union(zcyl(cx + hx, cy + hy, g.P["motor_hole_d"] / 2.0, -20, 0.5))
        clr.append(k)
    ko["motor_clearances"] = union_all(clr)
    ko["motor_wire_exit"] = union_all([corner(r.wire_exit_local(), sx, sy) for sx, sy in g.DIAG])
    w = v3.P["wire_channel_local"]
    chan = box(8.0, w["u"][1], w["v"][0], w["v"][1], w["z"][0], w["z"][1])
    ko["motor_lead_passages"] = union_all([corner(chan, sx, sy) for sx, sy in g.DIAG])
    return ko


def fin_parts(cko):
    P3 = v3.P
    holes = v3.bolt_holes_local()
    fin_env = r.fin_local()
    ftools = v3.bosses_local(-v3.HALF_FIN - 1, v3.HALF_FIN + 1)
    zl, zu = min(P3["bolt_z"]), max(P3["bolt_z"])
    bd = P3["boss_d"] / 2.0
    ftools = ftools.union(box(v3.U_B - bd, v3.U_B + bd, -v3.HALF_FIN - 1, v3.HALF_FIN + 1, zu, r.Z1 + 1.0))
    ftools = ftools.union(box(v3.U_B - bd, v3.U_B + bd, -v3.HALF_FIN - 1, v3.HALF_FIN + 1, r.Z0 - 1.0, zl))
    fin_b = ftools.intersect(fin_env)
    nd_l, des_l = fin_b.cut(holes), fin_env.cut(fin_b).cut(holes)
    nd = [corner(nd_l, sx, sy) for sx, sy in g.DIAG]
    des = [corner(des_l, sx, sy).cut(cko["motor_lead_passages"]) for sx, sy in g.DIAG]
    return union_all(des), union_all(nd)


# ------------------------------------------------------------------ channels
def gps_channel():
    c = P["gps_channel"]
    rad = c["d"] / 2.0
    xv, yv, zb, R, zh = c["x_v"], c["y_v"], c["z_bend"], c["R"], c["z_h"]
    xw, yw = c["wall_hole"]
    vert = zcyl(xv, 0.0, rad, zb, P["rim_z"] + 0.5)
    disc = cq.Workplane("XY").workplane(offset=zb).center(xv, 0.0).circle(rad).extrude(0.001).faces("<Z").val()
    bend = None
    for sgn in (1, -1):
        sol = cq.Shape.cast(BRepPrimAPI_MakeRevol(disc.wrapped, gp_Ax1(gp_Pnt(xv + R, 0, zb), gp_Dir(0, sgn, 0)), math.pi / 2).Shape())
        bb = sol.BoundingBox()
        if bb.zmin < zb - R - rad + 0.01 and bb.zmax < zb + 0.01:
            bend = cq.Workplane("XY").add(sol)
            break
    ang = math.degrees(math.atan2(yw - yv, xw - xv))
    x_end = -P["bay"]["xy"] + 2.0
    Lh = (x_end - xv) / math.cos(math.radians(ang)) - R
    leg = cq.Workplane("YZ").workplane(offset=xv + R).center(0.0, zh).circle(rad).extrude(Lh)
    ch = vert.union(bend).union(leg)
    return ch.rotate((xv, 0, 0), (xv, 0, 1), ang).translate((0, yv, 0))


def antenna_channel():
    c = P["ant_channel"]
    rad = c["d"] / 2.0
    y, zh, xb, R = c["y"], c["z_h"], c["x_bend"], c["R"]
    leg = cq.Workplane("YZ").workplane(offset=xb).center(y, zh).circle(rad).extrude(-P["bay"]["xy"] + 2.0 - xb)
    bend = torus_quarter((xb, y, zh - R), (0, -1, 0), (0, 0, 1), R, rad)
    vert = zcyl(xb - R, y, rad, P["keel"]["z"][0] - 1.0, zh - R)
    return leg.union(bend).union(vert)


# ------------------------------------------------------------------ keep-outs
def keepouts():
    cko = corner_keepouts()
    K = {}
    a = P["bay"]["xy"]
    F = P["fillets"]
    lower = box(-a, a, -a, a, P["bay"]["z"][0], P["chamfer_z"]).edges("|Z").fillet(F["bay_corner"])
    ch_in = outer_chamfer() - P["inner_chamfer_wall"] * math.sqrt(2.0)
    # 45 deg transition at the four bay corners from the rounded corners (below z about 6) to the
    # restored corner walls (z = 10): |x| + |y| <= ch_in + sqrt(2) (10 - z), so the walls stay continuous
    zb, zt = P["bay"]["z"][0] - 1.0, P["chamfer_z"]
    Lb = ch_in + math.sqrt(2.0) * (zt - zb)
    dia = (cq.Workplane("XY").workplane(offset=zb).polyline([(Lb, 0), (0, Lb), (-Lb, 0), (0, -Lb)]).close()
           .workplane(offset=zt - zb).polyline([(ch_in, 0), (0, ch_in), (-ch_in, 0), (0, -ch_in)]).close().loft())
    lower = lower.intersect(dia)
    upper = octagon_prism(ch_in, a, P["chamfer_z"], P["bay"]["z"][1] + 0.5)
    lb = P["lid_boss"]
    bosses = union_all([zcyl(x, y, lb["d"] / 2.0, lb["z"][0], lb["z"][1] + 1.0) for x, y in lb["xy"][:4]])
    upper = upper.cut(bosses).cut(boss_wedges())
    K["K1_fc_bay"] = lower.union(upper)
    fb = P["fc_boss"]; bp = fb["pitch"] / 2.0
    holes = []
    for sx, sy in g.DIAG:
        holes.append(zcyl(sx * bp, sy * bp, fb["hole_d"] / 2.0, P["floor_z"] - 1.0, -6.0 + 0.5))
        holes.append(zcyl(sx * bp, sy * bp, fb["cb_d"] / 2.0, P["floor_z"] - 1.0, P["floor_z"] + fb["cb_depth"]))
    K["K3_fc_screw_holes"] = union_all(holes)
    K["K4_components_above_fc"] = union_all([box(-9.5, 9.5, 1.25, 14.65, 4.1, 11.5),
                                             xcyl(-5.75, 10.25, 11.5 / 2.0, -6.5, 15.5),
                                             box(13.0, 17.5, -10.5, 0.5, -1.0, 16.5)])
    nc = P["nut_col"]
    K["K5_nut_columns"] = union_all([zcyl(sx * bp, sy * bp, nc["d"] / 2.0, *nc["z"]) for sx, sy in g.DIAG])
    h = P["body_half"]
    pw, lr, rs, up_ = P["pigtail_window"], P["pigtail_low_run"], P["pigtail_riser"], P["pigtail_under_plate"]
    K["K6_pigtail"] = union_all([box(a - 0.5, h + 0.5, pw["y"][0], pw["y"][1], *pw["z"]).edges("|X").fillet(F["pigtail_window"]),
                                 box(*lr["x"], *lr["y"], *lr["z"]), box(*rs["x"], *rs["y"], *rs["z"]),
                                 box(*up_["x"], *up_["y"], *up_["z"])])
    uw, up = P["usb_window"], P["usb_plug"]
    sw, sh = up["shell"]; ow, oh = up["overmold"]
    K["K7_usb"] = union_all([
        box(uw["x"][0], uw["x"][1], -h - 0.5, -a + 0.5, *uw["z"]).edges("|Y").fillet(F["usb_window"]),
        box(up["x_c"] - ow / 2, up["x_c"] + ow / 2, up["overmold_y"][1], up["overmold_y"][0], up["z_c"] - oh / 2, up["z_c"] + oh / 2)])
    K["K8_antenna_channel"] = antenna_channel()
    K["K9_gps_channel"] = gps_channel()
    sn = P["strap_notch"]
    K["K10_strap_passage"] = box(sn["x"][0], sn["x"][1], -h - 1, h + 1, sn["z"][0], sn["z"][1] + 0.5).edges("|Y").edges("<Z").fillet(F["strap_notch"])
    K["K11_motor_lead_passages"] = cko["motor_lead_passages"]
    K["K12_props_motors_arm_clearances"] = union_all([cko[k] for k in ("prop_sweep", "motor_body", "motor_clearances", "motor_wire_exit")])
    clip = box(-100, 100, -100, 100, -50, P["rim_z"])       # tub keep-outs end at the rim (the lid starts there)
    for k in ("K1_fc_bay", "K10_strap_passage"):
        K[k] = K[k].intersect(clip)
    return K, cko


# ------------------------------------------------------------------ tub
def tub_envelope(cko):
    h = P["body_half"]
    lower = box(-h, h, -h, h, P["floor_z"], P["chamfer_z"])
    upper = octagon_prism(outer_chamfer(), h, P["chamfer_z"], P["rim_z"])
    k = P["keel"]
    keel = box(k["x"][0], k["x"][1], -k["y_half"], k["y_half"], k["z"][0], k["z"][1])
    for kk in ("prop_sweep", "motor_lead_passages"):
        keel = keel.cut(cko[kk])
    env = lower.union(upper).union(keel)
    R = P["fillets"]["keel_root"]
    kx, ky = -h, k["y_half"]
    env = env.edges(cq.selectors.SumSelector(
        cq.selectors.SumSelector(cq.selectors.BoxSelector((kx - 0.05, ky - 0.05, -0.05), (kx + 0.05, ky + 0.05, 21.6)),
                                 cq.selectors.BoxSelector((kx - 0.05, -ky - 0.05, -0.05), (kx + 0.05, -ky + 0.05, 21.6))),
        cq.selectors.BoxSelector((kx - 0.05, -ky + 0.1, -0.05), (kx + 0.05, ky - 0.1, 0.05)))).fillet(R)
    return env.union(boss_wedges())


def tub_fixed_tools():
    fb = P["fc_boss"]; bp = fb["pitch"] / 2.0
    fc = union_all([zcyl(sx * bp, sy * bp, fb["d"] / 2.0, P["floor_z"], -6.0) for sx, sy in g.DIAG])
    lb = P["lid_boss"]
    lid = union_all([zcyl(x, y, lb["d"] / 2.0, *lb["z"]) for x, y in lb["xy"]])
    lid_holes = union_all([zcyl(x, y, lb["insert_d"] / 2.0, lb["z"][1] - lb["insert_depth"], lb["z"][1] + 1.0) for x, y in lb["xy"]])
    ant = antenna_spine()
    sp = P["ant_spine"]
    ant_holes = union_all([zcyl(sp["insert_xy"][0], sp["insert_xy"][1], sp["insert_d"] / 2.0, -1.0, sp["insert_depth"]),
                           zcyl(sp["peg_xy"][0], sp["peg_xy"][1], sp["peg_d"] / 2.0, -1.0, sp["peg_depth"])])
    return fc, lid, ant, union_all([lid_holes, ant_holes])


def antenna_spine():
    """F-17 (rev 3): sleeve around K8 (from x = -20 into the keel and down to the exit), pad, insert boss and web
    into the rear lid boss (-21, +5). Clipped later by the TUB envelope and cut by the keep-outs and holes, so the
    tools may overshoot the envelope. CAD version of s06_f17_spine.py without the blend fillets."""
    c, sp = P["ant_channel"], P["ant_spine"]
    ro = c["d"] / 2.0 + sp["wall"]
    y, zh, xb, R = c["y"], c["z_h"], c["x_bend"], c["R"]
    leg = cq.Workplane("YZ").workplane(offset=xb).center(y, zh).circle(ro).extrude(-20.0 - xb)
    bend = torus_quarter((xb, y, zh - R), (0, -1, 0), (0, 0, 1), R, ro)
    (px0, px1), (py0, py1), (pz0, pz1) = sp["pad"]
    pad = box(px0, px1, py0, py1, pz0, pz1)
    boss = zcyl(sp["insert_xy"][0], sp["insert_xy"][1], sp["boss_d"] / 2.0, *sp["boss_z"])
    a, b = cq.Vector(*sp["web"][0]), cq.Vector(*sp["web"][1])
    web = cq.Workplane("XY").add(cq.Solid.makeCylinder(sp["web_d"] / 2.0, (b - a).Length, a, (b - a).normalized()))
    return union_all([leg, bend, pad, boss, web])          # the bend ends at z = zh - R = -0.5, below the keel underside


def build_tub(K, cko):
    env = tub_envelope(cko)
    fin_des, fin_nd = fin_parts(cko)
    fc, lidb, ant, insert_holes = tub_fixed_tools()
    env = env.union(fin_des).union(lidb)
    cut = union_all([K[k] for k in K]).union(insert_holes)
    env_cut = env.cut(cut)
    tools = union_all([fc, lidb, ant])
    design = env_cut.cut(tools).cut(fin_nd)
    fixed = env_cut.intersect(tools).union(fin_nd)
    regions = {"fixed_fin_bosses": fin_nd, "fixed_fc_bosses": env_cut.intersect(fc),
               "fixed_lid_bosses": env_cut.intersect(lidb), "fixed_antenna_spine": env_cut.intersect(ant)}
    return design, fixed, regions, env


# ------------------------------------------------------------------ lid
def lid_parts():
    L = P["lid"]
    z0, z1 = L["z"]
    px, py = L["plate"]
    plate = box(-px / 2, px / 2, -py / 2, py / 2, z0, z1)
    dx, dy = L["deck_x"], L["deck_y"]
    deck = box(dx[0], dx[1], -dy, dy, z0, z1)
    t = L["tab"]
    tab = box(t["x"][0], t["x"][1], -t["y"], t["y"], z0, z1)
    pin = L["pocket_in"]; rt = L["rim_t"]
    rim = box(pin["x"][0] - rt, pin["x"][1] + rt, -pin["y"] - rt, pin["y"] + rt, *L["rim_z"]).cut(
        box(pin["x"][0], pin["x"][1], -pin["y"], pin["y"], L["rim_z"][0] - 1, L["rim_z"][1] + 1))
    cb = L["cap_boss"]
    capb = union_all([zcyl(cb["x"], s * cb["y"], cb["d"] / 2.0, *cb["z"]) for s in (1, -1)])
    lb = P["lid_boss"]
    pads = union_all([zcyl(x, y, d / 2.0, z0, z1) for (x, y), d in zip(lb["xy"], L["pad_d"])])
    cuts = []
    for x, y in lb["xy"]:
        cuts.append(zcyl(x, y, L["pad_hole_d"] / 2.0, z0 - 1, z1 + 1))
        hcsk = (L["csk_d"] - L["pad_hole_d"]) / 2.0
        cuts.append(cone(x, y, z1 - hcsk, L["pad_hole_d"] / 2.0, z1 + 0.01, L["csk_d"] / 2.0 + 0.01))
    for s in (1, -1):
        cuts.append(zcyl(cb["x"], s * cb["y"], cb["insert_d"] / 2.0, cb["z"][1] - cb["insert_depth"] - 0.5, cb["z"][1] + 1))
    gx, gy, gd = L["gps_hole"]
    cuts.append(zcyl(gx, gy, gd / 2.0, z0 - 1, z1 + 1))
    cc = L["c_cut"]
    pocket = box(cc["pocket_x"][0], cc["pocket_x"][1], -cc["pocket_y"], cc["pocket_y"], z0 - 1, z1 + 1).edges("|Z").fillet(0.8)
    cuts.append(pocket)
    cuts.append(box(cc["pocket_x"][1] - 0.5, t["x"][1] + 1.0, -cc["entry_half"], cc["entry_half"], z0 - 1, z1 + 1))
    return plate, deck, tab, rim, capb, pads, union_all(cuts)


def build_lid():
    L = P["lid"]
    z0, z1 = L["z"]
    px, py = L["plate"]
    plate, deck, tab, rim, capb, pads, cut = lid_parts()
    F = P["fillets"]
    t = L["tab"]; dx, dy = L["deck_x"], L["deck_y"]
    base = plate.union(deck).union(tab)
    base = sel(base, (px / 2 - 0.05, -t["y"] - 0.05, z0 - 0.1), (px / 2 + 0.05, t["y"] + 0.05, z1 + 0.1)).fillet(F["lid_tab_root"])
    base = sel(base, (-px / 2 - 0.05, -dy - 0.05, z0 - 0.1), (-px / 2 + 0.05, dy + 0.05, z1 + 0.1)).fillet(F["lid_deck_root"])
    env = base.union(rim).union(capb)
    env_cut = env.cut(cut)
    w = L["frame_w"]
    interior = box(-px / 2 + w, -L["band_half_x"], -py / 2 + w, py / 2 - w, z0 - 1, z1 + 1).union(
        box(L["band_half_x"], px / 2 - w, -py / 2 + w, py / 2 - w, z0 - 1, z1 + 1)).cut(pads)
    design = env_cut.intersect(interior)
    fixed = env_cut.cut(interior)
    frame = plate.cut(box(-px / 2 + w, px / 2 - w, -py / 2 + w, py / 2 - w, z0 - 1, z1 + 1))
    band = box(-L["band_half_x"], L["band_half_x"], -py / 2, py / 2, z0, z1)
    regions = {"fixed_plate_frame_band": env_cut.intersect(frame.union(band)),
               "fixed_gps_deck_rim_bosses": env_cut.intersect(deck.union(rim).union(capb)),
               "fixed_screw_pads": env_cut.intersect(pads), "fixed_front_tab": env_cut.intersect(tab)}
    return design, fixed, regions, env


# ------------------------------------------------------------------ arms
def arm_shapes():
    """v03-B arm STEP solids moved with their corner. Returns {tag: (design_solids, fixed_solids)}."""
    import s06_gates_v04B as G
    out = {}
    for tag, (sx, sy) in CORNERS.items():
        parts, _ = G.by_name(os.path.join(SRC_ARMS, "ARM_%s.step" % tag), {"ARM_%s.step" % tag: ["ARM_DESIGN", "ARM_FIXED"]})
        mv = cq.Vector(SHIFT * sx, SHIFT * sy, 0.0)
        out[tag] = ([s.translate(mv) for s in parts["ARM_DESIGN"]], [s.translate(mv) for s in parts["ARM_FIXED"]])
    return out


# ------------------------------------------------------------------ components (G5 dummies)
def components():
    C = {}
    bp = P["fc_boss"]["pitch"] / 2.0
    C["fc_board"] = box(-16.5, 16.5, -16.5, 16.5, -2.5, -0.9)
    C["fc_heatsink_and_parts_under_cradle_max"] = box(-9.5, 9.5, 1.25, 14.65, -0.9, 3.8)
    for tag, (sx, sy) in CORNERS.items():
        x, y = sx * bp, sy * bp
        C["damping_ring_" + tag] = zcyl(x, y, 3.0, -6.0, -5.0).cut(zcyl(x, y, 1.0, -7, -4))
        C["grommet_" + tag] = zcyl(x, y, 2.5, -5.0, 1.6).cut(zcyl(x, y, 1.0, -6, 2))
        tip = 8.5 if tag in ("pp", "mp") else 6.5
        C["screw_" + tag] = zcyl(x, y, 1.0, -13.5, tip).union(zcyl(x, y, 1.75, -14.6, -13.5))
        C["nut_lock_" + tag] = cq.Workplane("XY").workplane(offset=1.6).center(x, y).polygon(6, 4.62).extrude(2.5).cut(zcyl(x, y, 1.0, 0, 5))
        if tag in ("pp", "mp"):
            C["nut_nylon_" + tag] = cq.Workplane("XY").workplane(offset=5.5).center(x, y).polygon(6, 4.62).extrude(1.6).cut(zcyl(x, y, 1.0, 5, 8))
    cr = box(-9.5, 9.5, 1.25, 14.65, 4.1, 11.0).cut(box(-10, 10, 2.45, 13.45, 5.5, 12))
    for sx in (1, -1):
        ear = box(min(sx * 9.5, sx * 12.75), max(sx * 9.5, sx * 12.75), 9.75, 14.65, 4.1, 5.5).union(
            zcyl(sx * bp, bp, 2.9, 4.1, 5.5)).cut(zcyl(sx * bp, bp, 1.1, 3, 6))
        cr = cr.union(ear)
    C["receiver_cradle"] = cr
    C["receiver"] = box(-9.2, 9.2, 2.75, 13.15, 5.5, 9.5)
    C["capacitor"] = xcyl(-5.75, 10.25, 5.25, -6.0, 15.0)
    # pigtail: two 3 mm wires (6 x 3 side by side, 3 x 6 stacked when running forward under the plate)
    cc = P["lid"]["c_cut"]
    pxc = 0.5 * (cc["pocket_x"][0] + cc["pocket_x"][1])
    C["pigtail"] = union_all([box(14.5, 23.5, -9.0, -3.0, -0.9, 2.1),
                              box(23.0, 30.0, -6.0, 0.0, -1.5, 1.5),
                              box(29.0, 32.0, -3.0, 3.0, -1.5, 19.5),
                              box(29.0, pxc + 1.5, -1.5, 1.5, 18.5, 21.2),
                              zcyl(pxc, 1.5, 1.45, 18.5, 24.0), zcyl(pxc, -1.5, 1.45, 18.5, 24.0)])
    # XT30 female standing on the tab over the C cutout (axis z), battery male plugged from above
    C["xt30_female_on_tab"] = box(pxc - 2.625, pxc + 2.625, -5.125, 5.125, 24.0, 40.0)
    up = P["usb_plug"]; sw, sh = up["shell"]; ow, oh = up["overmold"]
    C["usb_plug"] = box(up["x_c"] - sw / 2, up["x_c"] + sw / 2, up["shell_y"][1], up["shell_y"][0], up["z_c"] - sh / 2, up["z_c"] + sh / 2).union(
        box(up["x_c"] - ow / 2, up["x_c"] + ow / 2, up["overmold_y"][1], up["overmold_y"][0], up["z_c"] - oh / 2, up["z_c"] + oh / 2))
    # antenna (rev 3): coax from the receiver -X end through K8 straight into the stem of the T, which hangs
    # stem-up under the K8 exit with the moulding vertical and the legs along y; TPU holder screwed to the spine pad
    a = P["ant_channel"]; xb, R = a["x_bend"], a["R"]
    A = P["antenna"]
    bx, by, bz = A["bar"]; sx, sy, sz = A["stem"]
    zs0 = A["stem_top"] - sz; zb0 = zs0 - bz; zl = zb0 + bz / 2.0
    C["antenna_coax"] = union_all([box(-20.0, -9.2, 3.0, 4.0, 6.0, 7.0),
                                   xcyl(a["y"], a["z_h"], 0.6, xb, -19.5),
                                   torus_quarter((xb, a["y"], a["z_h"] - R), (0, -1, 0), (0, 0, 1), R, 0.6)])   # ends at the stem top
    C["antenna_junction"] = union_all([box(A["x"] - bx / 2, A["x"] + bx / 2, A["y"] - by / 2, A["y"] + by / 2, zb0, zs0),
                                       box(A["x"] - sx / 2, A["x"] + sx / 2, A["y"] - sy / 2, A["y"] + sy / 2, zs0, A["stem_top"])])
    # holder envelope (the printable part is ANTENNA_HOLDER_v04B_r3_TPU.stl from s06_f17_spine.py)
    C["antenna_holder"] = union_all([box(-52.2, -41.0, -7.5, 8.0, -1.5, 0.0),
                                     box(-52.2, -45.7, A["y"] - by / 2 - 0.6, A["y"] + by / 2 + 0.6, zb0 - 1.0, -1.5),
                                     box(-52.2, -45.7, A["y"] - by / 2 - 4.5, A["y"] + by / 2 + 4.5, zl - 0.9, zl + 2.6)])
    el = []
    for s in (1, -1):
        y0 = A["y"] + s * by / 2; y1 = A["y"] + s * A["span"] / 2; yc = y1 - s * A["cap_len"]
        el.append(cq.Workplane("XZ").workplane(offset=-min(y0, yc)).center(A["x"], zl).circle(A["leg_d"] / 2.0).extrude(-abs(yc - y0)))
        el.append(cq.Workplane("XZ").workplane(offset=-min(yc, y1)).center(A["x"], zl).circle(A["cap_d"] / 2.0).extrude(-A["cap_len"]))
    C["antenna_V"] = union_all(el)          # key kept for gate C-9: now the straight T legs
    gx = P["gps_cg"][0]
    C["gps_module"] = box(gx - 8.5, gx + 8.5, -6.0, 6.0, 24.0, 29.0)
    cb = P["lid"]["cap_boss"]
    C["gps_cap"] = box(gx - 10.0, gx + 10.0, -12.0, 12.0, 29.0, 30.2).union(
        union_all([zcyl(cb["x"], s * cb["y"], 2.7, 26.5, 29.0) for s in (1, -1)]))
    C["battery"] = box(-29.5, 29.5, -15.0, 15.0, 24.0, 56.0)
    C["strap"] = union_all([box(-8.0, 8.0, -17.7, 17.7, 19.0, 19.5),
                            box(-8.0, 8.0, 17.2, 17.7, 19.0, 56.5), box(-8.0, 8.0, -17.7, -17.2, 19.0, 56.5),
                            box(-8.0, 8.0, -17.7, 17.7, 56.0, 56.5)])
    for i, (x, y) in enumerate(P["lid_boss"]["xy"]):
        C["lid_screw_%d" % (i + 1)] = cone(x, y, 23.2, 1.1, 24.0, 1.9).union(zcyl(x, y, 1.0, 18.0, 23.2))
    return C


# ------------------------------------------------------------------ export
def export(objs, path):
    asm = cq.Assembly()
    for name, wp in objs.items():
        if wp is not None and wp.vals():
            asm.add(wp, name=name)
    asm.export(path, exportType="STEP")


# rev 3 point masses (g): parts moved out of the RP_FC lump to where they sit; total 199.57 (the TPU holder from the
# STL, 0.93 g, is 0.43 g lighter than the 1.36 g estimate of the export note)
MASS = {"ant": 0.9 + 0.93 + 0.23 + 0.17, "gps": 2.6 + 0.84 + 0.46 + 0.33}
MASS["fc"] = 27.2 - (0.9 + 1.36 + 0.23 + 0.17) - (0.84 + 0.46 + 0.33)


def write_refpoints(path):
    rows = list(csv.reader(open(os.path.join(SRC_ARMS, "reference_points.csv"))))
    out = [rows[0]]
    for row in rows[1:]:
        if row[0] == "RP_GPS":
            gx, gy, gz = P["gps_cg"]
            m = MASS["gps"]
            row = ["RP_GPS", "GPS GM10 Nano V3 2.6 g (D-076) + TPU cap 0.84 + 2 M2 screws 0.46 + 2 inserts 0.33 (rev 3; were in the 12 g lump)",
                   "%.1f" % gx, "%.1f" % gy, "%.1f" % gz, "%.2f" % m, "%.3e" % (m * 1e-6), "0", "0", "0",
                   "S_GPS_SEAT: LID pocket floor (deck top inside the rim, z = 24)", "-"]
        elif row[0] == "RP_BATT":
            row[10] = "S_BATT_SEAT: LID top faces of plate frame + strap band (z = 24)"
        elif row[0] == "RP_FC":
            m = MASS["fc"]
            row[1] = "FC 13.6 + receiver 0.7 (antenna moved to RP_ANT) + hardware and wiring lump less the antenna and GPS parts (rev 3)"
            row[5], row[6] = "%.2f" % m, "%.3e" % (m * 1e-6)
            row[10] = "S_FC_SEAT: TUB top faces of the 4 FC bosses (z = -6), rings dia 6.4 / 2.2"
        elif row[0].startswith("RP_MOT") or row[0].startswith("RP_JNT"):
            x, y = float(row[2]), float(row[3])
            row[2] = "%.3f" % (x + SHIFT * (1 if x > 0 else -1))
            row[3] = "%.3f" % (y + SHIFT * (1 if y > 0 else -1))
        out.append(row)
        if row[0] == "RP_GPS":
            A = P["antenna"]
            out.append(["RP_ANT", "antenna 0.9 + TPU holder 0.93 (STL) + M2 x 5 screw 0.23 + M2 insert 0.17 (rev 3, F-17)",
                        "%.1f" % (A["x"] + 0.4), "%.1f" % A["y"], "-4.0", "%.2f" % MASS["ant"], "%.3e" % (MASS["ant"] * 1e-6),
                        "0", "0", "0", "S_ANT_PAD: TUB spine pad underside (z = 0) inside x -53..-39, y -8..8, less the holes", "-"])
    with open(path, "w", newline="") as fh:
        csv.writer(fh).writerows(out)


def main():
    os.makedirs(OUT, exist_ok=True)
    K, cko = keepouts()
    tub_d, tub_f, tub_reg, _ = build_tub(K, cko)
    lid_d, lid_f, lid_reg, _ = build_lid()
    C = components()
    export({"TUB_DESIGN": tub_d, "TUB_FIXED": tub_f}, os.path.join(OUT, "TUB.step"))
    export({"LID_DESIGN": lid_d, "LID_FIXED": lid_f}, os.path.join(OUT, "LID.step"))
    export(K, os.path.join(OUT, "KEEPOUTS_v04B.step"))
    export(C, os.path.join(OUT, "COMPONENTS_v04B.step"))
    arms = arm_shapes()
    V = {}
    for tag, (d, f) in arms.items():
        export({"ARM_DESIGN": cq.Workplane("XY").add(d), "ARM_FIXED": cq.Workplane("XY").add(f)},
               os.path.join(OUT, "ARM_%s.step" % tag))
        V["ARM_%s_DESIGN" % tag] = sum(s.Volume() for s in d)
        V["ARM_%s_FIXED" % tag] = sum(s.Volume() for s in f)
    write_refpoints(os.path.join(OUT, "reference_points_v04B.csv"))
    V.update({"TUB_DESIGN": vol(tub_d), "TUB_FIXED": vol(tub_f), "LID_DESIGN": vol(lid_d), "LID_FIXED": vol(lid_f)})
    V.update({"tub_" + k: vol(w) for k, w in tub_reg.items()})
    V.update({"lid_" + k: vol(w) for k, w in lid_reg.items()})
    V.update({"keepout_" + k: vol(w) for k, w in K.items()})
    V.update({"component_" + k: vol(w) for k, w in C.items()})
    V = {k: round(v, 3) for k, v in V.items()}
    with open(os.path.join(OUT, "v04B_volumes.json"), "w") as fh:
        json.dump({"volumes_mm3": V, "params": P}, fh, indent=1, default=str)
    for k in ("TUB_DESIGN", "TUB_FIXED", "LID_DESIGN", "LID_FIXED", "ARM_pp_DESIGN", "ARM_pp_FIXED"):
        print("%-14s %10.1f mm3  %7.2f g" % (k, V[k], V[k] * RHO))
    print("wheelbase %.2f mm, motor axes at +-%.3f" % (P["wheelbase"], M_NEW))
    return K, C


if __name__ == "__main__":
    main()
