"""s06_cae_expected_v04B.py - expected CAE surface areas and cells for v04-B revision 4 (main chat, 2026-10-13).
Fuses each part's solids (OCP) and measures the tie, seat and coupling surfaces listed in
docs/stage6_v04B_r4_export_note.md. Output: geometry/v04B_r4/cae_expected_v04B_r4.json.
Run from scripts/geometry_main: python3 s06_cae_expected_v04B.py"""
import sys, os, json, math, hashlib
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(HERE))
import cadquery as cq
import s06_gates_v04B as G
v4 = G.v4
D = v4.OUT
out = {}
T, _ = G.by_name(os.path.join(D, "TUB.step")); L, _ = G.by_name(os.path.join(D, "LID.step"))
def fused(sols):
    f = sols[0].fuse(*sols[1:])
    try:
        f = f.clean()
    except Exception:
        pass
    return f
FT = fused(T["TUB_DESIGN"] + T["TUB_FIXED"]); FL = fused(L["LID_DESIGN"] + L["LID_FIXED"])
def faces_at(sol, z, up):
    r = []
    for f in sol.Faces():
        if f.geomType() != "PLANE": continue
        bb = f.BoundingBox()
        if abs(bb.zmin - z) > 1e-4 or abs(bb.zmax - z) > 1e-4: continue
        n = f.normalAt(f.Center())
        if (n.z > 0.99 and up) or (n.z < -0.99 and not up): r.append(f)
    return r
def area_in(faces, region):
    a = 0.0
    for f in faces:
        c = f.intersect(region)
        a += sum(x.Area() for x in c.Faces()) if c is not None else 0.0
    return a
def rbox(x0, x1, y0, y1, z0, z1):
    return cq.Solid.makeBox(x1 - x0, y1 - y0, z1 - z0, cq.Vector(x0, y0, z0))
tt = faces_at(FT, 21.5, True)
out["TUB_top_z21.5_external_total"] = (round(sum(f.Area() for f in tt), 3), len(tt))
under_plate = rbox(-32, 32, -17, 17, 21, 22)
out["TIE_LIDRIM_secondary_TUB_top_under_lid (x -32..32, |y|<=17)"] = round(area_in(tt, under_plate), 3)
out["TUB_top_|y|<=17_all_x (rev 2 style partition, y only)"] = round(area_in(tt, rbox(-80, 80, -17, 17, 21, 22)), 3)
out["TUB_top_keel_strip_x_-32.5..-32_outside_lid"] = round(area_in(tt, rbox(-80, -32, -17, 17, 21, 22)), 3)
lb = faces_at(FL, 21.5, False)
out["TIE_LIDRIM_main_LID_bottom_z21.5"] = (round(sum(f.Area() for f in lb), 3), len(lb))
lt = faces_at(FL, 24.0, True)
out["LID_top_z24_total"] = (round(sum(f.Area() for f in lt), 3), len(lt))
P = v4.P["lid"]; px, py = P["plate"]; w = P["frame_w"]; bh = P["band_half_x"]
frame_band = rbox(-px/2, px/2, -py/2, py/2, 23.5, 24.5).cut(rbox(-px/2 + w, -bh, -py/2 + w, py/2 - w, 23, 25)).cut(rbox(bh, px/2 - w, -py/2 + w, py/2 - w, 23, 25))
out["S_BATT_SEAT frame + band, x +-32"] = round(area_in(lt, frame_band), 3)
out["S_BATT_SEAT_expected 64x34 - 2 x 20x28"] = 64*34 - 2*20*28
out["LID_top_within_x+-32 (frame, band, pads, links, design)"] = round(area_in(lt, rbox(-32, 32, -17, 17, 23.5, 24.5)), 3)
fx = fused(L["LID_FIXED"]) if len(L["LID_FIXED"]) > 1 else L["LID_FIXED"][0]
out["LID_FIXED_top_within_x+-32"] = round(area_in(faces_at(fx, 24.0, True), rbox(-32, 32, -17, 17, 23.5, 24.5)), 3)
gs = [f for f in faces_at(FT, 24.0, True) if f.BoundingBox().xmin > -53 and f.BoundingBox().xmax < -35 and abs(f.BoundingBox().ymax) < 6.5]
out["S_GPS_SEAT"] = (round(sum(f.Area() for f in gs), 3), len(gs), [round(v, 3) for v in (gs[0].BoundingBox().xmin, gs[0].BoundingBox().xmax, gs[0].BoundingBox().ymin, gs[0].BoundingBox().ymax)] if gs else None)
xy = v4.P["lid_boss"]["xy"]
out["boss_tops"] = [round(area_in(tt, cq.Solid.makeCylinder(3.0, 1.0, cq.Vector(x, y, 21.0))), 3) for x, y in xy]
out["pad_bottoms (lid bottom inside dia 6)"] = [round(area_in(lb, cq.Solid.makeCylinder(3.0, 1.0, cq.Vector(x, y, 21.0))), 3) for x, y in xy]
out["deck_bottom_faces_on_air (TUB external, z 21.5, x<-32.5, facing down)"] = round(sum(f.Area() for f in faces_at(FT, 21.5, False) if f.BoundingBox().xmax <= -32.4), 3)
deck = [s for s in T["TUB_FIXED"] if s.BoundingBox().zmax > 24.5][0]
out["gap_LID_to_GPS_deck_mm"] = round(G.dist(cq.Workplane("XY").add(L["LID_DESIGN"] + L["LID_FIXED"]), cq.Workplane("XY").add(deck)), 4)
out["deck_cell"] = {"vol": round(deck.Volume(), 3), "bbox": [round(v, 2) for v in (lambda b: (b.xmin, b.xmax, b.ymin, b.ymax, b.zmin, b.zmax))(deck.BoundingBox())]}
out["TUB_FIXED_cells"] = sorted([round(s.Volume(), 2) for s in T["TUB_FIXED"]])
out["LID_cells"] = {"design": [round(s.Volume(), 2) for s in L["LID_DESIGN"]], "fixed": [round(s.Volume(), 2) for s in L["LID_FIXED"]]}
out["sha256"] = {f: hashlib.sha256(open(os.path.join(D, f), "rb").read()).hexdigest() for f in sorted(os.listdir(D)) if f.endswith(".step") or f.endswith(".csv")}
json.dump(out, open(os.path.join(D, "cae_expected_v04B_r4.json"), "w"), indent=1)
print(json.dumps(out, indent=1))
