# -*- coding: ascii -*-
"""
s06_gates_v04B.py - gates G0 to G2 and G5 for the v04-B export (brief section 11).
  G0 file identity: solid count and names, design and fixed volumes against v04B_volumes.json;
     ARM files identical to the v03-B arms after moving them back by (3 sx, 3 sy, 0)
  G1 Boolean bookkeeping per part (TUB, LID): design AND fixed = 0; (design OR fixed) XOR
     (envelope minus keep-outs, recomputed) < 0.01 mm^3; every keep-out AND part = 0; every
     fixed solid touches the design solid of its part
  G2 face test (s06_split_acceptance.py) on every STEP of the model
  G5 assembly clash and clearances C-1 to C-9
Usage: python3 s06_gates_v04B.py [G0 G1 G2 G5]. Writes abaqus_v04B/gates_v04B.json. ASCII only.
"""
import hashlib
import json
import os
import re
import sys
import cadquery as cq
from OCP.BRepExtrema import BRepExtrema_DistShapeShape

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import s06_geometry_v04B as v4          # noqa: E402
import s06_split_acceptance as acc      # noqa: E402

D = v4.OUT
TOL = 0.01
RES = {}


def step_solids(path):
    """Named products in order and the solids of the file (cadquery import order)."""
    txt = open(path).read()
    names = re.findall(r"PRODUCT\('([^']*)'", txt)
    shp = cq.importers.importStep(path)
    return names, shp.solids().vals()


def by_name(path, want=None):
    """Map product name -> list of solids, using the STEP text order of MANIFOLD_SOLID_BREP ids."""
    txt = open(path).read()
    prods = [(int(m.group(1)), m.group(2)) for m in re.finditer(r"#(\d+) = PRODUCT\('([^']*)'", txt)]
    sols = [int(m) for m in re.findall(r"#(\d+) = MANIFOLD_SOLID_BREP", txt)]
    names, solids = step_solids(path)
    out = {}
    leaf = [p for p in prods if not p[1].startswith("TUB") or p[1] in ("TUB_DESIGN", "TUB_FIXED")]
    # cadquery assemblies: one product per named part, solids follow in id order
    named = [p for p in prods if p[1] in (want or WANT).get(os.path.basename(path), [])]
    named.sort()
    for i, (pid, nm) in enumerate(named):
        nxt = named[i + 1][0] if i + 1 < len(named) else 10 ** 12
        out[nm] = [s for s, sid in zip(solids, sols) if pid < sid < nxt] if len(sols) == len(solids) else []
    return out, solids


WANT = {"TUB.step": ["TUB_DESIGN", "TUB_FIXED"], "LID.step": ["LID_DESIGN", "LID_FIXED"],
        "ARM_pp.step": ["ARM_DESIGN", "ARM_FIXED"], "ARM_pm.step": ["ARM_DESIGN", "ARM_FIXED"],
        "ARM_mp.step": ["ARM_DESIGN", "ARM_FIXED"], "ARM_mm.step": ["ARM_DESIGN", "ARM_FIXED"]}


def wp(solids):
    w = cq.Workplane("XY").add(solids[0])
    for s in solids[1:]:
        w = w.union(cq.Workplane("XY").add(s), clean=False)
    return w


def vol(solids):
    return sum(s.Volume() for s in solids)


def dist(a, b):
    sa = a.val().wrapped if hasattr(a, "val") else a.wrapped
    sb = b.val().wrapped if hasattr(b, "val") else b.wrapped
    if hasattr(a, "vals") and len(a.vals()) > 1:
        sa = cq.Compound.makeCompound(a.vals()).wrapped
    if hasattr(b, "vals") and len(b.vals()) > 1:
        sb = cq.Compound.makeCompound(b.vals()).wrapped
    d = BRepExtrema_DistShapeShape(sa, sb)
    d.Perform()
    return d.Value()


def common_vol(a, b):
    try:
        c = a.intersect(b)
        return sum(s.Volume() for s in c.solids().vals())
    except Exception:
        return float("nan")


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


# ------------------------------------------------------------------ G0
def g0():
    ref = json.load(open(os.path.join(D, "v04B_volumes.json")))["volumes_mm3"]
    rows, ok = [], True
    for f in ("TUB.step", "LID.step"):
        parts, solids = by_name(os.path.join(D, f))
        for nm in WANT[f]:
            v = vol(parts.get(nm, []))
            good = abs(v - ref[nm]) < TOL and len(parts.get(nm, [])) > 0
            ok &= good
            rows.append({"file": f, "body": nm, "solids": len(parts.get(nm, [])), "vol_mm3": round(v, 3),
                         "expected": ref[nm], "pass": good})
    for t in ("pp", "pm", "mp", "mm"):
        f = "ARM_%s.step" % t
        parts, solids = by_name(os.path.join(D, f))
        old, _ = by_name(os.path.join(v4.SRC_ARMS, f))
        sx, sy = v4.CORNERS[t]
        back = cq.Vector(-v4.SHIFT * sx, -v4.SHIFT * sy, 0.0)
        a = wp([x.translate(back) for x in parts["ARM_DESIGN"] + parts["ARM_FIXED"]])
        b = wp(old["ARM_DESIGN"] + old["ARM_FIXED"])
        diff = vol(a.cut(b).solids().vals()) + vol(b.cut(a).solids().vals())
        same = diff < TOL
        vd, vf = vol(parts.get("ARM_DESIGN", [])), vol(parts.get("ARM_FIXED", []))
        good = same and abs(vd - 8036.9) < 0.1 and abs(vf - 2933.5) < 0.1
        ok &= good
        rows.append({"file": f, "identical_to_v03B_after_moving_back": same, "boolean_difference_mm3": round(diff, 5), "design_mm3": round(vd, 2), "fixed_mm3": round(vf, 2),
                     "solids": len(solids), "pass": good})
    RES["G0"] = {"pass": ok, "rows": rows}
    print("G0", "PASS" if ok else "FAIL")
    for r in rows:
        print("  ", r)


# ------------------------------------------------------------------ G1
def g1():
    K, cko = v4.keepouts()
    out, ok = {}, True
    # recompute expected solids independently of the exported split
    env_t = v4.tub_envelope(cko)
    fin_des, fin_nd = v4.fin_parts(cko)
    fc, lidb, ant, ins = v4.tub_fixed_tools()
    exp_t = env_t.union(fin_des).union(lidb).union(fc).union(ant).cut(v4.union_all([K[k] for k in K]).union(ins)).union(fin_nd)
    lid_d, lid_f, _, _ = v4.build_lid()
    exp_l = lid_d.union(lid_f)
    arms = {}
    for t in ("pp", "pm", "mp", "mm"):
        parts, _ = by_name(os.path.join(D, "ARM_%s.step" % t))
        arms[t] = wp(parts["ARM_DESIGN"] + parts["ARM_FIXED"])
    for f, exp in (("TUB.step", exp_t), ("LID.step", exp_l)):
        parts, _ = by_name(os.path.join(D, f))
        dname, fname = WANT[f]
        d, fx = wp(parts[dname]), wp(parts[fname])
        both = d.union(fx, clean=False)
        ov = common_vol(d, fx)
        x1 = vol(both.cut(exp).solids().vals()) if both.cut(exp).vals() else 0.0
        x2 = vol(exp.cut(both).solids().vals()) if exp.cut(both).vals() else 0.0
        kov = {k: round(common_vol(both, w), 4) for k, w in K.items()}
        floating = []
        for i, s in enumerate(parts[fname]):
            dd = dist(cq.Workplane("XY").add(s), d)
            if dd > 1e-6:
                floating.append((i, round(dd, 4), [round(c, 2) for c in s.Center().toTuple()]))
        good = ov < TOL and x1 < TOL and x2 < TOL and all(v < TOL for v in kov.values()) and not floating
        ok &= good
        out[f] = {"design_and_fixed_mm3": round(ov, 5), "exported_minus_expected_mm3": round(x1, 5),
                  "expected_minus_exported_mm3": round(x2, 5), "keepout_overlap_mm3": kov,
                  "floating_fixed_solids": floating, "pass": good}
        print("G1", f, "PASS" if good else "FAIL", json.dumps(out[f]))
    arm_ko = {}
    for t, a in arms.items():
        arm_ko[t] = {k: round(common_vol(a, w), 4) for k, w in K.items() if k != "K12_props_motors_arm_clearances"}
        good = all(v < TOL for v in arm_ko[t].values())
        ok &= good
    out["ARM_vs_new_keepouts"] = arm_ko
    print("G1 arms vs new keep-outs", json.dumps(arm_ko))
    RES["G1"] = {"pass": ok, **out}


# ------------------------------------------------------------------ G2
def g2():
    rows, ok = [], True
    files = ["TUB.step", "LID.step"] + ["ARM_%s.step" % t for t in ("pp", "pm", "mp", "mm")]
    for f in files:
        n, nf, a, w, bad = acc.test(os.path.join(D, f))
        rows.append({"file": f, "solids": n, "faces": nf, "smallest_mm2": round(a, 3), "narrowest_mm": round(w, 3), "failing": bad})
        ok &= bad == 0
        print("G2 %-12s solids %2d faces %4d smallest %.3f mm^2 narrowest %.3f mm failing %d" % (f, n, nf, a, w, bad))
    RES["G2"] = {"pass": ok, "rows": rows}



# ------------------------------------------------------------------ G3
def features():
    K, cko = v4.keepouts()
    fc, lidb, ant, ins = v4.tub_fixed_tools()
    lb = v4.P["lid_boss"]
    tub = {k: w for k, w in K.items() if k not in ("K4_components_above_fc", "K5_nut_columns", "K12_props_motors_arm_clearances")}
    tub.update({"FC bosses dia 6.4": fc, "lid bosses dia 6": lidb, "antenna boss dia 5.4": ant,
                "insert holes (lid bosses, antenna boss)": ins,
                "boss support wedges": v4.boss_wedges()})
    L = v4.P["lid"]; z0, z1 = L["z"]
    cb = L["cap_boss"]
    lid = {"screw pads": v4.union_all([v4.zcyl(x, y, d / 2.0, z0, z1) for (x, y), d in zip(lb["xy"], L["pad_d"])]),
           "pad holes and countersinks": v4.union_all([v4.zcyl(x, y, L["pad_hole_d"] / 2.0, z0 - 1, z1 + 1).union(
               v4.cone(x, y, z1 - (L["csk_d"] - L["pad_hole_d"]) / 2.0, L["pad_hole_d"] / 2.0, z1 + 0.01, L["csk_d"] / 2.0 + 0.01)) for x, y in lb["xy"]]),
           "GPS cap bosses": v4.union_all([v4.zcyl(cb["x"], s * cb["y"], cb["d"] / 2.0, *cb["z"]) for s in (1, -1)]),
           "GPS hole": v4.zcyl(L["gps_hole"][0], L["gps_hole"][1], L["gps_hole"][2] / 2.0, z0 - 1, z1 + 1),
           "C cutout": v4.box(L["c_cut"]["pocket_x"][0], L["tab"]["x"][1] + 1, -L["c_cut"]["pocket_y"], L["c_cut"]["pocket_y"], z0 - 1, z1 + 1),
           "front tab": v4.box(L["tab"]["x"][0], L["tab"]["x"][1], -L["tab"]["y"], L["tab"]["y"], z0, z1),
           "pocket rim": v4.box(L["pocket_in"]["x"][0] - L["rim_t"], L["pocket_in"]["x"][1] + L["rim_t"], -L["pocket_in"]["y"] - L["rim_t"],
                                L["pocket_in"]["y"] + L["rim_t"], *L["rim_z"]),
           "plate frame inner edge": v4.box(-L["plate"][0] / 2 + L["frame_w"], L["plate"][0] / 2 - L["frame_w"],
                                           -L["plate"][1] / 2 + L["frame_w"], L["plate"][1] / 2 - L["frame_w"], z0, z1)}
    return tub, lid


def g3():
    import s06_tangency_audit as ta
    tubf, lidf = features()
    base = ta.run(os.path.join(v4.SRC_ARMS, "BODY.step"), verbose=False)
    rt = ta.run(os.path.join(D, "TUB.step"), tubf, verbose=False)
    rl = ta.run(os.path.join(D, "LID.step"), lidf, verbose=False)
    def key(x):
        return (x.get("angle_deg", x.get("dist_mm")), x["faces"])
    def classify(item):
        x, y, z = item["at"]
        if "angle_deg" in item and abs(item["angle_deg"] - 4.8) < 0.1:
            return "existing v03-B: fin boss dia 12 inside the fin nose R5 (fin nose, D-055)"
        if "dist_mm" in item and abs(item["dist_mm"] - 0.106) < 0.01:
            return "existing v03-B: fin root fillet end at z = 10 (watch item)"
        if "dist_mm" in item and abs(item["dist_mm"] - 0.5) < 0.01 and abs(z - 5.0) < 0.01:
            return "K1 (+-17.5) to K2 (+-17.0) step at z = 5, faces at 90 deg (brief values; v03-B had the same 0.5 mm FC / void step at z = 6)"
        return "NEW"
    new = [w for w in rt["wedges"] + rt["strips"] + rl["wedges"] + rl["strips"] if classify(w) == "NEW"]
    summ = {}
    for w in rt["wedges"] + rt["strips"]:
        c = classify(w)
        summ[c] = summ.get(c, 0) + 1
    ok = not new
    for rep in (rt, rl):
        for k, v in rep["features"].items():
            a, d = v["min_interior_angle_deg"], v["min_dist_to_untouched_face_mm"]
            ledge = d is not None and abs(d - 0.5) < 1e-3 and v["at"] is not None and abs(v["at"][2] - 5.0) < 1e-3
            v["note"] = "0.5 mm is the K1 / K2 step at z = 5 (faces at 90 deg)" if ledge else ""
            v["pass"] = (a is None or a >= ta.ANG_MIN) and (d is None or d >= ta.DIST_MIN - 1e-3 or ledge)
    RES["G3"] = {"pass": ok, "baseline_v03B_BODY": {"wedges": len(base["wedges"]), "strips": len(base["strips"])},
                 "TUB_flags_by_cause": summ, "new_flags": new, "TUB_features": rt["features"], "LID_features": rl["features"],
                 "LID_flags": len(rl["wedges"]) + len(rl["strips"])}
    print("G3", "PASS" if ok else "FAIL", json.dumps(summ, indent=1))
    for nm, rep in (("TUB", rt), ("LID", rl)):
        for k, v in rep["features"].items():
            print("   %s %-40s faces %3d  min angle %s  min dist %s  %s" % (nm, k, v["faces"], v["min_interior_angle_deg"],
                                                                         v["min_dist_to_untouched_face_mm"], "ok" if v["pass"] else "CHECK"))
    if new:
        print("   NEW:", new)


# ------------------------------------------------------------------ G4
def g4():
    import s06_gmsh_meshtest_loc as gm
    rows = {}
    for h in (1.5, 1.0):
        for f, path in (("TUB", os.path.join(D, "TUB.step")), ("LID", os.path.join(D, "LID.step")),
                        ("v03B_BODY", os.path.join(v4.SRC_ARMS, "BODY.step"))):
            n, qmin, nb, cl, nv = gm.run(path, h)
            rows["%s_%.1f" % (f, h)] = {"tets": n, "min_gamma": round(qmin, 4), "below_0.05": nb,
                                        "clusters": [([round(float(c), 1) for c in p], k) for p, k in cl]}
            print("G4 %-10s h=%.1f tets %7d min gamma %.4f below 0.05: %d" % (f, h, n, qmin, nb))
    import math as _m
    base = [p for p, k in rows["v03B_BODY_1.0"]["clusters"]]
    mv = lambda p: [p[0] + v4.SHIFT * _m.copysign(1, p[0]), p[1] + v4.SHIFT * _m.copysign(1, p[1]), p[2]]
    same = all(any(_m.dist(p, mv(b)) < 1.5 for b in base) for p, k in rows["TUB_1.0"]["clusters"])
    ok = rows["TUB_1.5"]["below_0.05"] == 0 and rows["LID_1.5"]["below_0.05"] == 0 and rows["LID_1.0"]["below_0.05"] == 0 \
        and rows["TUB_1.0"]["below_0.05"] <= rows["v03B_BODY_1.0"]["below_0.05"]
    RES["G4"] = {"pass": ok, "TUB_1.0_low_tets_at_same_places_as_v03B": same, **rows}
    print("G4", "PASS" if ok else "FAIL", "(TUB 1.0 low tets at the v03-B places, moved with the corners: %s)" % same)

# ------------------------------------------------------------------ G5
def g5():
    K, cko = v4.keepouts()
    C = v4.components()
    tub_p, _ = by_name(os.path.join(D, "TUB.step"))
    lid_p, _ = by_name(os.path.join(D, "LID.step"))
    TUB = wp(tub_p["TUB_DESIGN"] + tub_p["TUB_FIXED"])
    LID = wp(lid_p["LID_DESIGN"] + lid_p["LID_FIXED"])
    ARM = {}
    for t in ("pp", "pm", "mp", "mm"):
        parts, _ = by_name(os.path.join(D, "ARM_%s.step" % t))
        ARM[t] = wp(parts["ARM_DESIGN"] + parts["ARM_FIXED"])
    PROP = cko["prop_sweep"]
    MOT = cko["motor_body"]
    frame = {"TUB": TUB, "LID": LID, "PROP_SWEEP_3mm": PROP, "MOTORS": MOT}
    frame.update({"ARM_" + t: a for t, a in ARM.items()})
    # pairs that coexist by design (screw through grommet and board, wires soldered to the XT30, ...)
    def skip(a, b):
        pair = {a, b}
        pref = lambda s, p: s.startswith(p)
        for x, y in ((a, b), (b, a)):
            if pref(x, "fc_board") and (pref(y, "grommet") or pref(y, "screw")):
                return True
            if pref(x, "grommet") and pref(y, "screw"):
                return True
            if pref(x, "damping") and pref(y, "screw"):
                return True
            if pref(x, "nut") and pref(y, "screw"):
                return True
            if pref(x, "receiver_cradle") and pref(y, "screw"):
                return True
            if x == "pigtail" and y == "xt30_female_on_tab":
                return True
            if x in ("antenna_holder", "antenna_junction") and y in ("antenna_V", "antenna_coax", "antenna_junction", "antenna_holder"):
                return True
            if x == "antenna_V" and y == "antenna_coax":
                return True
            if x == "fc_heatsink_and_parts_under_cradle_max" and y == "fc_board":
                return True
        return False
    inter = []
    names = list(C)
    for i, a in enumerate(names):
        for fnm, fw in frame.items():
            if fnm in ("PROP_SWEEP_3mm", "MOTORS") and a in ("battery", "strap", "xt30_female_on_tab", "gps_module", "gps_cap"):
                pass
            v = common_vol(C[a], fw)
            if v > 1e-3:
                inter.append((a, fnm, round(v, 4)))
        for b in names[i + 1:]:
            if skip(a, b):
                continue
            v = common_vol(C[a], C[b])
            if v > 1e-3:
                inter.append((a, b, round(v, 4)))
    # FC insertion (step 4): board, grommets and capacitor swept from the seat up past the rim
    sweep = v4.box(-16.5, 16.5, -16.5, 16.5, -5.0, 30.0)
    c1 = dist(sweep, TUB)
    # lid placement: lid against everything fitted in the bay before step 12
    bay = [k for k in C if not k.startswith(("battery", "strap", "gps_", "xt30", "lid_screw", "antenna", "pigtail"))]
    lid_clear = min(dist(LID, C[k]) for k in bay)
    lid_clear_who = min(bay, key=lambda k: dist(LID, C[k]))
    reg = v4.build_tub(K, cko)[2]
    WALL = v4.box(-23.0, -20.5, -23.0, 23.0, -15.0, 21.5)
    lidb = reg["fixed_lid_bosses"]
    cl = {
        "C-1 FC + capacitor sweep to TUB (>= 0.25)": c1,
        "C-2 lid bosses and support wedges to the FC insertion path (+-16.5 prism) (>= 0.25)": dist(lidb.union(v4.boss_wedges()), sweep),
        "C-2 lid bosses to K5 (>= 1.0)": dist(lidb, K["K5_nut_columns"]),
        "C-2 lid bosses to prop sweep + 3 (>= 1.0)": dist(lidb, PROP),
        "C-3 pigtail to ARM_pm (>= 1.0)": dist(C["pigtail"], ARM["pm"]),
        "C-3 pigtail to the pm fin and the front bosses (TUB outside x = 23) (>= 1.0)": dist(C["pigtail"], TUB.intersect(v4.box(23.01, 80, -80, 80, -20, 30))),
        "C-3 pigtail to the front window edges (> 0)": dist(C["pigtail"].intersect(v4.box(20.0, 23.5, -12, 2, -5, 6)), TUB),
        "C-4 XT30 to prop sweep + 3 (> 0)": dist(C["xt30_female_on_tab"], PROP),
        "C-4 pigtail riser to prop sweep + 3 (> 0)": dist(C["pigtail"], PROP),
        "C-5 capacitor to pm lock nut (>= 1.0)": dist(C["capacitor"], C["nut_lock_pm"]),
        "C-5 capacitor to receiver cradle (>= 1.0)": dist(C["capacitor"], C["receiver_cradle"]),
        "C-5 capacitor to LID (>= 1.0)": dist(C["capacitor"], LID),
        "C-6 cradle floor to FC parts (>= 0.3; parts assumed <= z 3.8, Q-60)": dist(C["receiver_cradle"], C["fc_heatsink_and_parts_under_cradle_max"]),
        "C-7 K8 (antenna) to K11 openings in the rear wall (>= 1.0)": dist(K["K8_antenna_channel"].intersect(WALL), K["K11_motor_lead_passages"].intersect(WALL)),
        "C-7 K8 (antenna) to K9 openings in the rear wall (>= 1.0)": dist(K["K8_antenna_channel"].intersect(WALL), K["K9_gps_channel"].intersect(WALL)),
        "C-7 K9 to K11 openings in the rear wall (>= 1.0)": dist(K["K9_gps_channel"].intersect(WALL), K["K11_motor_lead_passages"].intersect(WALL)),
        "C-8 USB plug to ARM_pm (>= 0.5)": dist(C["usb_plug"], ARM["pm"]),
        "C-8 USB plug to TUB (> 0)": dist(C["usb_plug"], TUB),
        "C-9 antenna V to ARM_mp (>= 5)": dist(C["antenna_V"], ARM["mp"]),
        "C-9 antenna V to ARM_mm (>= 5)": dist(C["antenna_V"], ARM["mm"]),
        "C-9 antenna V to prop sweep + 3 (> 0)": dist(C["antenna_V"], PROP),
        "lid placement: LID to bay contents (> 0)": lid_clear,
    }
    bb = C["antenna_V"].val().BoundingBox()
    cl["C-9 antenna V z range (above -12, below 10)"] = (round(bb.zmin, 2), round(bb.zmax, 2))
    cl = {k: (round(v, 3) if isinstance(v, float) else v) for k, v in cl.items()}
    cl["lid placement: nearest bay item"] = lid_clear_who
    RES["G5"] = {"interferences": inter, "clearances": cl, "pass": not inter}
    print("G5 interferences:", inter)
    for k, v in cl.items():
        print("   %-70s %s" % (k, v))


if __name__ == "__main__":
    which = sys.argv[1:] or ["G0", "G1", "G2", "G3", "G4", "G5"]
    fn = {"G0": g0, "G1": g1, "G2": g2, "G3": g3, "G4": g4, "G5": g5}
    old = {}
    p = os.path.join(D, "gates_v04B.json")
    if os.path.exists(p):
        old = json.load(open(p))
    for w in which:
        fn[w]()
    old.update(RES)
    json.dump(old, open(p, "w"), indent=1, default=str)
