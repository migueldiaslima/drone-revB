"""r4_assembly_render.py - renders of the v04-B revision 4 assembly (main chat, 2026-10-13).
Design regions grey, fixed regions orange, components dark, GPS green, battery translucent.
Reads geometry/v04B_r4 STEP files (TUB, LID, ARM_xx) and rebuilds the component dummies from
s06_geometry_v04B.py. Run from the repo root: python3 scripts/figures/r4_assembly_render.py
Output: figures/r4_render_*.png"""
import os
import sys
import numpy as np
import pyvista as pv

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "scripts", "geometry_main"))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import s06_geometry_v04B as v4      # noqa: E402
import s06_gates_v04B as G          # noqa: E402

pv.OFF_SCREEN = True
D = os.path.join(ROOT, "geometry", "v04B_r4")
OUTD = os.path.join(ROOT, "figures")
DESIGN, FIXED, LIDDES, COMP, GPS, BATT, ANT = "#dfe2e5", "#e8792b", "#aab8c8", "#4b4f9e", "#3aa655", "#5b8fd6", "#c23b3b"


def mesh(shapes, tol=0.05):
    out = []
    for s in shapes:
        vs, tris = s.tessellate(tol, 0.3)
        if not tris:
            continue
        pts = np.array([v.toTuple() for v in vs])
        faces = np.hstack([[3, a, b, c] for a, b, c in tris])
        out.append(pv.PolyData(pts, faces))
    m = out[0]
    for o in out[1:]:
        m = m.merge(o)
    return m.compute_normals(split_vertices=True, feature_angle=35)


def solids(wp):
    return wp.solids().vals() if hasattr(wp, "solids") else [wp]


def load():
    P = {}
    T, _ = G.by_name(os.path.join(D, "TUB.step"))
    L, _ = G.by_name(os.path.join(D, "LID.step"))
    P["tub_design"], P["tub_fixed"] = mesh(T["TUB_DESIGN"]), mesh(T["TUB_FIXED"])
    P["lid_design"], P["lid_fixed"] = mesh(L["LID_DESIGN"]), mesh(L["LID_FIXED"])
    ad, af = [], []
    for t in ("pp", "pm", "mp", "mm"):
        A, _ = G.by_name(os.path.join(D, "ARM_%s.step" % t))
        ad += A["ARM_DESIGN"]; af += A["ARM_FIXED"]
    P["arm_design"], P["arm_fixed"] = mesh(ad), mesh(af)
    C = v4.components()
    _, cko = v4.keepouts()
    P["motors"] = mesh(solids(cko["motor_body"]))
    gps = [k for k in C if k.startswith("gps_")]
    ant = [k for k in C if k.startswith("antenna")]
    P["gps"] = mesh([s for k in gps for s in solids(C[k])])
    P["ant"] = mesh([s for k in ant for s in solids(C[k])])
    P["batt"] = mesh(solids(C["battery"]))
    P["strap"] = mesh(solids(C["strap"]))
    rest = [k for k in C if k not in gps + ant + ["battery", "strap"]]
    P["comp"] = mesh([s for k in rest for s in solids(C[k])])
    return P


def shot(P, name, cam, show_batt=True, lid_dz=0.0, lid_op=1.0, title="", des_op=1.0, comps=True):
    p = pv.Plotter(off_screen=True, window_size=(1600, 1200))
    p.set_background("white")
    kw = dict(smooth_shading=False, specular=0.25, show_edges=False)
    p.add_mesh(P["tub_design"], color=DESIGN, opacity=des_op, **kw)
    p.add_mesh(P["tub_fixed"], color=FIXED, **kw)
    p.add_mesh(P["arm_design"], color=DESIGN, opacity=des_op, **kw)
    p.add_mesh(P["arm_fixed"], color=FIXED, **kw)
    p.add_mesh(P["lid_design"].translate((0, 0, lid_dz)), color=LIDDES, opacity=lid_op, **kw)
    p.add_mesh(P["lid_fixed"].translate((0, 0, lid_dz)), color=FIXED, opacity=lid_op, **kw)
    if comps:
        p.add_mesh(P["motors"], color=COMP, **kw)
        p.add_mesh(P["comp"], color=COMP, **kw)
    p.add_mesh(P["gps"], color=GPS, **kw)
    p.add_mesh(P["ant"], color=ANT, **kw)
    if show_batt:
        p.add_mesh(P["batt"], color=BATT, opacity=0.25, **kw)
        p.add_mesh(P["strap"], color="#222222", opacity=0.6, **kw)
    p.add_legend([["TUB / ARM design (free)", DESIGN], ["LID design (free)", LIDDES], ["fixed (non-design)", FIXED],
                  ["components", COMP], ["GPS + cap", GPS], ["antenna + holder", ANT]] +
                 ([["battery (transparent)", BATT]] if show_batt else []), bcolor="white", face="rectangle", size=(0.24, 0.24))
    if title:
        p.add_text(title, font_size=12, color="black")
    p.camera_position = cam
    p.enable_anti_aliasing("ssaa")
    path = os.path.join(OUTD, "r4_render_%s.png" % name)
    p.screenshot(path)
    p.close()
    print(path)


if __name__ == "__main__":
    P = load()
    f = (0, 0, 10)
    shot(P, "1_assembly", [(170, -190, 170), f, (0, 0, 1)], title="v04-B rev 4, assembled")
    shot(P, "2_no_battery", [(170, -190, 170), f, (0, 0, 1)], show_batt=False, title="rev 4, battery and strap hidden")
    shot(P, "3_lid_raised", [(-160, -170, 190), (-10, 0, 15), (0, 0, 1)], show_batt=False, lid_dz=30,
         title="rev 4, lid raised 30 mm: GPS deck on the TUB, 4 lid bosses")
    shot(P, "4_rear_below", [(-170, -120, -110), (-30, 0, 5), (0, 0, 1)], show_batt=False,
         title="rev 4 from rear below: spine pad, antenna holder, GPS deck")
    shot(P, "6_fixed_xray", [(-190, -150, 140), (-15, 0, 5), (0, 0, 1)], show_batt=False, lid_dz=30, des_op=0.18, comps=False,
         title="rev 4 x-ray: design transparent, all fixed regions (spine, GPS deck, bosses, lid frame)")
    shot(P, "5_top", [(0, 0, 320), f, (1, 0, 0)], show_batt=False, title="rev 4 top view (x up)")
