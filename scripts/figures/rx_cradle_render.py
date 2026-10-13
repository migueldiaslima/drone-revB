"""rx_cradle_render.py - renders of the receiver cradle (main chat, 2026-10-13).
Run from the repo root after s07_receiver_cradle.py: python3 scripts/figures/rx_cradle_render.py
Output: figures/rx_cradle_*.png"""
import os
import sys
import numpy as np
import pyvista as pv

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "scripts", "geometry_main"))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import s06_geometry_v04B as v4          # noqa: E402
import s07_receiver_cradle as rc        # noqa: E402
import s06_gates_v04B as G              # noqa: E402

pv.OFF_SCREEN = True
OUTD = os.path.join(ROOT, "figures")
TPU, RX, FC, HW, CAP, TUBC = "#e8792b", "#2f6fd6", "#2e7d4f", "#555a63", "#7b5ea7", "#c9cdd2"


def mesh(shapes, tol=0.02):
    out = []
    for s in shapes:
        vs, tris = s.tessellate(tol, 0.2)
        pts = np.array([v.toTuple() for v in vs])
        out.append(pv.PolyData(pts, np.hstack([[3, a, b, c] for a, b, c in tris])))
    m = out[0]
    for o in out[1:]:
        m = m.merge(o)
    return m.compute_normals(split_vertices=True, feature_angle=35)


def sol(w):
    return w.solids().vals() if hasattr(w, "solids") else [w]


body, d = rc.build()
C = v4.components()
M = {"cradle": mesh(sol(body)), "rx": mesh(sol(rc.receiver_dummy(d))),
     "fc": mesh(sol(C["fc_board"])), "fcparts": mesh(sol(C["fc_heatsink_and_parts_under_cradle_max"])),
     "cap": mesh(sol(C["capacitor"])),
     "hw": mesh([s for k in C if k.startswith(("screw_", "nut_", "grommet_", "damping_"))
                 for s in sol(C[k])])}


def shot(name, cam, items, title, tub=False, clip=None):
    p = pv.Plotter(off_screen=True, window_size=(1600, 1200))
    p.set_background("white")
    kw = dict(specular=0.25)
    for k, col, op in items:
        m = M[k] if clip is None else M[k].clip_box(clip, invert=False)
        if m.n_points:
            p.add_mesh(m, color=col, opacity=op, **kw)
    if tub:
        T, _ = G.by_name(os.path.join(ROOT, "geometry", "v04B_r4", "TUB.step"))
        p.add_mesh(mesh(T["TUB_DESIGN"] + T["TUB_FIXED"], 0.08), color=TUBC, opacity=0.15, **kw)
    p.add_text(title, font_size=12, color="black")
    p.add_legend([["cradle (TPU 95A HF)", TPU], ["receiver 18.4 x 10.4 x 4.0 envelope", RX], ["FC board", FC],
                  ["FC parts envelope (z <= 3.8, Q-60)", "#9cc9a8"], ["capacitor", CAP], ["screws, nuts, grommets", HW]],
                 bcolor="white", face="rectangle", size=(0.27, 0.2))
    p.camera_position = cam
    p.enable_anti_aliasing("ssaa")
    path = os.path.join(OUTD, "rx_cradle_%s.png" % name)
    p.screenshot(path)
    p.close()
    print(path)


f = (0, 8, 6)
shot("1_part", [(45, -40, 45), f, (0, 0, 1)], [("cradle", TPU, 1.0)], "Receiver cradle v1, TPU 95A HF, 0.89 g")
shot("2_installed", [(55, -55, 55), f, (0, 0, 1)],
     [("cradle", TPU, 1.0), ("rx", RX, 0.55), ("fc", FC, 1.0), ("fcparts", "#9cc9a8", 0.35), ("cap", CAP, 1.0), ("hw", HW, 1.0)],
     "Installed on the pp and mp screws (ears between lock nut and nylon nut)")
shot("3_section_x0", [(70, 8, 8), (0, 8, 6), (0, 0, 1)],
     [("cradle", TPU, 1.0), ("rx", RX, 0.8), ("fc", FC, 1.0), ("fcparts", "#9cc9a8", 0.5), ("cap", CAP, 1.0)],
     "Section at x = 0, looking -x: snap lips, floor 1.4, 0.3 mm over the FC parts envelope",
     clip=(0, 30, -30, 30, -10, 30))
shot("4_in_tub", [(-60, -70, 90), (0, 0, 4), (0, 0, 1)],
     [("cradle", TPU, 1.0), ("rx", RX, 0.6), ("fc", FC, 1.0), ("cap", CAP, 1.0), ("hw", HW, 1.0)],
     "In the bay (tub transparent)", tub=True)
