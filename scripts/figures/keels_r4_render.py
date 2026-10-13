"""keels_r4_render.py - renders of the exact keels A and B (main chat, 2026-10-13).
Run from the repo root after s07_keels_r4.py: python3 scripts/figures/keels_r4_render.py
Output: figures/keels_r4_*.png"""
import os
import sys
import numpy as np
import pyvista as pv
import cadquery as cq

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "scripts", "geometry_main"))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import s06_geometry_v04B as v4          # noqa: E402
import s06_gates_v04B as G              # noqa: E402

pv.OFF_SCREEN = True
D = os.path.join(ROOT, "geometry", "v04B_r4_keels")


def mesh(shapes, tol=0.03):
    out = []
    for s in shapes:
        vs, tris = s.tessellate(tol, 0.2)
        out.append(pv.PolyData(np.array([v.toTuple() for v in vs]), np.hstack([[3, a, b, c] for a, b, c in tris])))
    m = out[0]
    for o in out[1:]:
        m = m.merge(o)
    return m.compute_normals(split_vertices=True, feature_angle=35)


A = mesh(cq.importers.importStep(os.path.join(D, "KEEL_A_r4.step")).solids().vals())
B = mesh(cq.importers.importStep(os.path.join(D, "KEEL_B_r4.step")).solids().vals())
T, _ = G.by_name(os.path.join(ROOT, "geometry", "v04B_r4", "TUB.step"))
fixed = [s for s in T["TUB_FIXED"] if s.BoundingBox().xmax < -15]
FX = mesh(fixed)
TD = mesh(T["TUB_DESIGN"], 0.08)
C = v4.components()
ANT = mesh([s for k in C if k.startswith("antenna") for s in C[k].solids().vals()])
GPS = mesh([s for k in ("gps_module",) for s in C[k].solids().vals()])


def shot(name, cam, title):
    p = pv.Plotter(off_screen=True, window_size=(1600, 1200))
    p.set_background("white")
    p.add_mesh(TD, color="#c9cdd2", opacity=0.12)
    p.add_mesh(FX, color="#e8792b", specular=0.25)
    p.add_mesh(A, color="#2f6fd6", specular=0.25)
    p.add_mesh(B, color="#c23b3b", specular=0.25)
    p.add_mesh(ANT, color="#555a63")
    p.add_mesh(GPS, color="#3aa655")
    p.add_legend([["keel A (fixed, new)", "#2f6fd6"], ["web B + wall gusset (fixed, new)", "#c23b3b"],
                  ["fixed: GPS deck, spine, bosses", "#e8792b"], ["TUB design envelope (transparent)", "#c9cdd2"],
                  ["antenna + holder", "#555a63"], ["GPS", "#3aa655"]], bcolor="white", face="rectangle", size=(0.3, 0.22))
    p.add_text(title, font_size=12, color="black")
    p.camera_position = cam
    p.enable_anti_aliasing("ssaa")
    path = os.path.join(ROOT, "figures", "keels_r4_%s.png" % name)
    p.screenshot(path)
    p.close()
    print(path)


f = (-36, 0, 10)
shot("1_rear_below", [(-110, -80, -40), f, (0, 0, 1)], "Keels A and B under the GPS deck (from rear, below)")
shot("2_side", [(-36, -140, 10), f, (0, 0, 1)], "Side view from -y (keel zone x -54 to -23 cleaned)")
shot("3_rear_above", [(-120, 60, 70), f, (0, 0, 1)], "From rear, above (+y side)")
