# -*- coding: ascii -*-
"""s06_render_v04B.py - figure sheet of the v04-B export (fig06_v04B_export.png). ASCII only."""
import os
import cadquery as cq
from PIL import Image, ImageDraw, ImageFont
from s06_render import render
import s06_geometry_v04B as v4
import s06_gates_v04B as G

D = v4.OUT
C_TD, C_TF, C_LD, C_LF, C_ARM, C_CMP = "#b4cae6", "#3f6aa6", "#f5c08f", "#c0561a", "#d9d6cf", "#3d9a5b"


def items():
    tp, _ = G.by_name(os.path.join(D, "TUB.step"))
    lp, _ = G.by_name(os.path.join(D, "LID.step"))
    tub = [(cq.Workplane("XY").add(s), C_TD, 1.0) for s in tp["TUB_DESIGN"]] + [(cq.Workplane("XY").add(s), C_TF, 1.0) for s in tp["TUB_FIXED"]]
    lid = [(cq.Workplane("XY").add(s), C_LD, 1.0) for s in lp["LID_DESIGN"]] + [(cq.Workplane("XY").add(s), C_LF, 1.0) for s in lp["LID_FIXED"]]
    arms = []
    for t in ("pp", "pm", "mp", "mm"):
        ap, _ = G.by_name(os.path.join(D, "ARM_%s.step" % t))
        arms += [(cq.Workplane("XY").add(s), C_ARM, 1.0) for s in ap["ARM_DESIGN"] + ap["ARM_FIXED"]]
    return tub, lid, arms


def main():
    tub, lid, arms = items()
    C = v4.components()
    bay = ["fc_board", "capacitor", "receiver_cradle", "receiver", "pigtail", "usb_plug", "antenna_coax", "antenna_holder",
           "antenna_V", "antenna_junction"] + [k for k in C if k.startswith(("nut_", "grommet", "damping", "screw_"))]
    comp = [(C[k], C_CMP, 1.0) for k in bay]
    top = ["xt30_female_on_tab", "gps_module", "gps_cap", "battery", "strap"] + [k for k in C if k.startswith("lid_screw")]
    comp_top = [(C[k], "#7a7a7a" if k == "battery" else C_CMP, 0.35 if k == "battery" else 1.0) for k in top]
    lid_up = [(w.translate((0, 0, 30)), c, o) for w, c, o in lid]
    shots = [
        ("Tub (design light, fixed dark)", tub, dict(view=(0.9, -1.3, 1.0), zoom=1.25)),
        ("Tub from the rear", tub, dict(view=(-1.0, 0.7, 0.6), zoom=1.25)),
        ("Tub from below", tub, dict(view=(0.6, -0.8, -1.0), zoom=1.25)),
        ("Lid (design light, fixed dark)", lid, dict(view=(0.9, -1.3, 1.0), zoom=1.3)),
        ("Bay contents in the tub (lid off)", tub + comp, dict(view=(0.7, -1.0, 1.3), zoom=1.3)),
        ("Assembly with arms, lid and battery", tub + arms + lid + comp + comp_top, dict(view=(0.9, -1.3, 0.8), zoom=1.0)),
    ]
    files = []
    for i, (lab, it, kw) in enumerate(shots):
        f = os.path.join(D, "v04B_view%d.png" % i)
        render(it, f, size=(1000, 800), **kw)
        files.append((lab, f))
    fb = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 26)
    fr = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
    W, H = 3 * 640, 2 * 560 + 120
    sheet = Image.new("RGB", (W, H), "white")
    dr = ImageDraw.Draw(sheet)
    dr.text((20, 12), "v04-B export: tub, lid, arms and component dummies", fill="#0b0b0b", font=fb)
    for k, (lab, f) in enumerate(files):
        im = Image.open(f).convert("RGB").resize((640, 512))
        x, y = (k % 3) * 640, 60 + (k // 3) * 560
        sheet.paste(im, (x, y + 30))
        dr.text((x + 15, y), lab, fill="#52514e", font=fr)
    leg = [(C_TD, "tub design"), (C_TF, "tub fixed"), (C_LD, "lid design"), (C_LF, "lid fixed"), (C_ARM, "arm (unchanged)"), (C_CMP, "component dummy")]
    x = 20
    for col, lab in leg:
        dr.rectangle([x, H - 45, x + 22, H - 23], fill=col, outline="#333333"); dr.text((x + 30, H - 47), lab, fill="#333333", font=fr)
        x += 60 + int(dr.textlength(lab, font=fr))
    sheet.save(os.path.join(D, "fig06_v04B_export.png"))


if __name__ == "__main__":
    main()
