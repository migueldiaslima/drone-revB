# -*- coding: ascii -*-
"""
s06_arm_split_fix_v03B.py - re-split the v03-B arm STEP files into design and fixed regions
without degenerate faces (Stage 6 Abaqus set-up chat, 2026-10-08).

Input : abaqus_v03B/ARM_xx.step (ARM_DESIGN + ARM_FIXED, from s06_abaqus_inputs_v03B.py)
Output: abaqus_v03B_fix/ARM_xx.step (ARM_DESIGN + ARM_FIXED)

Rule (arm envelope unchanged, joint interface unchanged):
  envelope = union of the original design and fixed solids (unified)
  boss tool, per bolt (axes 33 mm along the arm diagonal, z = -9 and z = 4):
      cylinder dia 12 along the bolt axis through the full fork width (+-11 mm)
  upper bolt only: plus a 12 mm wide block from the bolt axis (z = 4) up to the arm top
      (the dia 12 boss is otherwise tangent to the arm top z = 10)
  motor pad: unchanged (original fixed pad solid)
  fixed  = envelope AND tools
  design = envelope MINUS tools
Acceptance: after a general fuse of design and fixed, no face below 0.5 mm^2 and no face
narrower than 0.3 mm (2 x area / perimeter).
Requires OCP (cadquery-ocp). ASCII only.
"""
import math
import os
import re
import sys

from OCP.BOPAlgo import BOPAlgo_Builder
from OCP.BRep import BRep_Builder
from OCP.BRepAlgoAPI import BRepAlgoAPI_Common, BRepAlgoAPI_Cut, BRepAlgoAPI_Fuse
from OCP.BRepGProp import BRepGProp
from OCP.BRepPrimAPI import BRepPrimAPI_MakeBox, BRepPrimAPI_MakeCylinder
from OCP.GProp import GProp_GProps
from OCP.Interface import Interface_Static
from OCP.ShapeUpgrade import ShapeUpgrade_UnifySameDomain
from OCP.STEPCAFControl import STEPCAFControl_Writer
from OCP.STEPControl import STEPControl_AsIs, STEPControl_Reader
from OCP.TCollection import TCollection_ExtendedString
from OCP.TDataStd import TDataStd_Name
from OCP.TDocStd import TDocStd_Document
from OCP.TopAbs import TopAbs_FACE, TopAbs_SOLID
from OCP.TopExp import TopExp_Explorer
from OCP.TopoDS import TopoDS, TopoDS_Compound
from OCP.XCAFDoc import XCAFDoc_DocumentTool
from OCP.gp import gp_Ax2, gp_Dir, gp_Pnt

BOLT_S = 33.0          # bolt line, mm along the arm diagonal
BOLT_Z = (-9.0, 4.0)   # lower and upper bolt axes
BOSS_R = 6.0           # dia 12 bosses (D-051)
HALF_W = 11.0          # tool half-length across the fork (fork 20.3 mm wide)
TOP_EXT = 7.0          # block height above the upper axis (clipped by the arm top)


def explore(shape, kind):
    e = TopExp_Explorer(shape, kind)
    out = []
    while e.More():
        out.append(TopoDS.Solid(e.Current()) if kind == TopAbs_SOLID else TopoDS.Face(e.Current()))
        e.Next()
    return out


def volume(s):
    p = GProp_GProps()
    BRepGProp.VolumeProperties_s(s, p)
    return p.Mass()


def unify(s):
    u = ShapeUpgrade_UnifySameDomain(s, True, True, False)
    u.Build()
    return u.Shape()


def load_arm(path):
    text = open(path).read()
    ids = [int(m) for m in re.findall(r"#(\d+) = MANIFOLD_SOLID_BREP", text)]
    fixed_id = int(re.search(r"#(\d+) = PRODUCT\('ARM_FIXED'", text).group(1))
    n_design = sum(i < fixed_id for i in ids)
    r = STEPControl_Reader()
    r.ReadFile(path)
    r.TransferRoots()
    solids = explore(r.OneShape(), TopAbs_SOLID)
    return solids[:n_design], solids[n_design:]


def split(design, fixed, sx, sy):
    s2 = 1.0 / math.sqrt(2.0)
    u = (sx * s2, sy * s2)
    n = (-sy * s2, sx * s2)
    env = design[0]
    for f in design[1:] + fixed:
        env = BRepAlgoAPI_Fuse(env, f).Shape()
    env = unify(env)
    tools = []
    for zc in BOLT_Z:
        p = gp_Pnt(BOLT_S * u[0] - HALF_W * n[0], BOLT_S * u[1] - HALF_W * n[1], zc)
        tools.append(BRepPrimAPI_MakeCylinder(gp_Ax2(p, gp_Dir(n[0], n[1], 0)), BOSS_R, 2 * HALF_W).Shape())
    p = gp_Pnt((BOLT_S - BOSS_R) * u[0] - HALF_W * n[0], (BOLT_S - BOSS_R) * u[1] - HALF_W * n[1], BOLT_Z[1])
    tools.append(BRepPrimAPI_MakeBox(gp_Ax2(p, gp_Dir(0, 0, 1), gp_Dir(u[0], u[1], 0)), 2 * BOSS_R, 2 * HALF_W, TOP_EXT).Shape())
    # the motor pad is the fixed solid farthest out along the arm
    def s_of(sol):
        p = GProp_GProps()
        BRepGProp.VolumeProperties_s(sol, p)
        c = p.CentreOfMass()
        return c.X() * u[0] + c.Y() * u[1]
    pad = max(fixed, key=s_of)
    tool = tools[0]
    for t in tools[1:] + [pad]:
        tool = BRepAlgoAPI_Fuse(tool, t).Shape()
    new_fixed = explore(unify(BRepAlgoAPI_Common(env, tool).Shape()), TopAbs_SOLID)
    new_design = explore(unify(BRepAlgoAPI_Cut(env, tool).Shape()), TopAbs_SOLID)
    return new_design, new_fixed


def acceptance(solids, amin=0.5, wmin=0.3):
    b = BOPAlgo_Builder()
    for s in solids:
        b.AddArgument(s)
    b.Perform()
    seen = set()
    bad = []
    for f in explore(b.Shape(), TopAbs_FACE):
        h = f.__hash__()
        if h in seen:
            continue
        seen.add(h)
        pa = GProp_GProps()
        BRepGProp.SurfaceProperties_s(f, pa)
        pl = GProp_GProps()
        BRepGProp.LinearProperties_s(f, pl)
        a = pa.Mass()
        w = 2.0 * a / pl.Mass()
        if a < amin or w < wmin:
            bad.append((round(a, 4), round(w, 4)))
    return len(seen), bad


def compound(solids):
    c = TopoDS_Compound()
    b = BRep_Builder()
    b.MakeCompound(c)
    for s in solids:
        b.Add(c, s)
    return c


def write_step(path, design, fixed):
    doc = TDocStd_Document(TCollection_ExtendedString("XmlOcaf"))
    st = XCAFDoc_DocumentTool.ShapeTool_s(doc.Main())
    for name, sh in (("ARM_DESIGN", compound(design)), ("ARM_FIXED", compound(fixed))):
        lab = st.AddShape(sh, False)
        TDataStd_Name.Set_s(lab, TCollection_ExtendedString(name))
    Interface_Static.SetCVal_s("write.step.unit", "MM")
    w = STEPCAFControl_Writer()
    w.SetNameMode(True)
    w.Transfer(doc, STEPControl_AsIs)
    w.Write(path)


def main(src, dst):
    os.makedirs(dst, exist_ok=True)
    for tag in ("pp", "pm", "mp", "mm"):
        sx = 1 if tag[0] == "p" else -1
        sy = 1 if tag[1] == "p" else -1
        d0, f0 = load_arm(os.path.join(src, "ARM_%s.step" % tag))
        d1, f1 = split(d0, f0, sx, sy)
        nf, bad = acceptance(d1 + f1)
        print("ARM_%s: design %d solid %.1f mm3 (was %.1f), fixed %d solids %.1f mm3 (was %.1f), faces %d, acceptance %s"
              % (tag, len(d1), sum(map(volume, d1)), sum(map(volume, d0)),
                 len(f1), sum(map(volume, f1)), sum(map(volume, f0)), nf, "PASS" if not bad else "FAIL %s" % bad))
        write_step(os.path.join(dst, "ARM_%s.step" % tag), d1, f1)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "abaqus_v03B", sys.argv[2] if len(sys.argv) > 2 else "abaqus_v03B_fix")
