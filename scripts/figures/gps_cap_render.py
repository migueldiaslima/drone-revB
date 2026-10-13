"""gps_cap_render.py - renders of the GPS cap on the rev 4 deck (main chat, 2026-10-13).
Run from the repo root after s07_gps_cap.py: python3 scripts/figures/gps_cap_render.py"""
import os
import sys
import numpy as np
import pyvista as pv

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "scripts", "geometry_main"))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import s06_geometry_v04B as v4      # noqa: E402
import s07_gps_cap as gc            # noqa: E402

pv.OFF_SCREEN = True


def mesh(w, tol=0.02):
    out = []
    for s in w.solids().vals():
        vs, tris = s.tessellate(tol, 0.2)
        out.append(pv.PolyData(np.array([v.toTuple() for v in vs]), np.hstack([[3, a, b, c] for a, b, c in tris])))
    m = out[0]
    for o in out[1:]:
        m = m.merge(o)
    return m.compute_normals(split_vertices=True, feature_angle=35)


body, d = gc.build()
deck, holes = v4.gps_deck_tools()
K, _ = v4.keepouts()
deck = deck.cut(holes).cut(K["K9_gps_channel"])
M = {"cap": mesh(body), "gps": mesh(gc.gps_dummy(d)), "deck": mesh(deck)}


def shot(name, cam, title, clip=None, cap_op=1.0):
    p = pv.Plotter(off_screen=True, window_size=(1600, 1200))
    p.set_background("white")
    for k, col, op in (("deck", "#e8792b", 1.0), ("gps", "#3aa655", 1.0), ("cap", "#2f6fd6", cap_op)):
        m = M[k] if clip is None else M[k].clip_box(clip, invert=False)
        p.add_mesh(m, color=col, opacity=op, specular=0.25)
    p.add_legend([["GPS cap v2 (TPU 95A HF, press pins)", "#2f6fd6"], ["GM10 Nano 12 x 17 x 5 envelope", "#3aa655"],
                  ["TUB GPS deck, rim, cap bosses (fixed)", "#e8792b"]], bcolor="white", face="rectangle", size=(0.3, 0.14))
    p.add_text(title, font_size=12, color="black")
    p.camera_position = cam
    p.enable_anti_aliasing("ssaa")
    path = os.path.join(ROOT, "figures", "gps_cap_%s.png" % name)
    p.screenshot(path)
    p.close()
    print(path)


f = (-44, 0, 26)
shot("1_installed", [(-5, -45, 60), f, (0, 0, 1)], "GPS cap on the deck: window over the antenna, TPU press pins into the boss holes")
shot("2_section_x44", [(-5, 0, 28), f, (0, 0, 1)], "Section at x = -44 looking -x: press pins in the boss holes, 0.3 mm clamp on the module top",
     clip=(-44, 0, -30, 30, 0, 40))
