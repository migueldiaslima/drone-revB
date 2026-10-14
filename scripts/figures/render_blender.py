"""render_blender.py - Cycles renders of the printed frame with representative component models.

Run with the bpy module (Blender 5.2 as a Python package):
    python3 scripts/figures/render_blender.py <view> [samples]
Views: R1_assembly, R2_exploded, R3_design_vs_result, R4_joint, R5_rear_underside, R6_fixed_regions
Meshes: print STLs (when present) from geometry/print/, else the design-space STLs exported to MESH_DIR.
Component models are representative: datasheet dimensions (motor dia 20.8 x 15.5, 9 x 9 M2 mount; propeller
3.5 in, pitch 2.0 in, three blades; battery 59 x 30 x 32; flight controller 33 x 33 board on 25.5 mm mounts;
receiver 18.4 x 10.4; GPS 12 x 17 x 5; T antenna legs dia 1.4, span 52), placed as in the analysis model.
Output: report/figures/<view>.png
"""
import math
import os
import sys
import bpy
import bmesh
from mathutils import Vector, Matrix, Euler

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MESH_DIR = os.environ.get("MESH_DIR", "/tmp/claude-0/meshes")
PRINT_DIR = os.path.join(ROOT, "geometry", "print")
OUT = os.path.join(ROOT, "report", "figures")
S = 0.001          # mm -> m (Blender scene units in metres keeps the camera and lights sensible)
M = 52.497         # motor axis coordinate
CORNERS = {"pp": (1, 1), "pm": (1, -1), "mp": (-1, 1), "mm": (-1, -1)}


# ------------------------------------------------------------------ scene
def reset():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.render.engine = "CYCLES"
    sc.cycles.device = "CPU"
    sc.cycles.use_denoising = True
    sc.render.film_transparent = False
    sc.view_settings.view_transform = "AgX"
    sc.view_settings.look = "AgX - Medium High Contrast"
    sc.view_settings.exposure = float(os.environ.get("EXPO", -0.3))
    w = bpy.data.worlds.new("w")
    sc.world = w
    w.use_nodes = True
    nt = w.node_tree
    bg = nt.nodes["Background"]
    bg.inputs[0].default_value = (1, 1, 1, 1)
    bg.inputs[1].default_value = float(os.environ.get("WORLD", 0.18))     # light from the environment
    cam_bg = nt.nodes.new("ShaderNodeBackground")
    cam_bg.inputs[0].default_value = (1, 1, 1, 1)
    cam_bg.inputs[1].default_value = 2.6                                    # white backdrop seen by the camera
    lp = nt.nodes.new("ShaderNodeLightPath")
    mix = nt.nodes.new("ShaderNodeMixShader")
    out = nt.nodes["World Output"]
    nt.links.new(lp.outputs["Is Camera Ray"], mix.inputs[0])
    nt.links.new(bg.outputs[0], mix.inputs[1])
    nt.links.new(cam_bg.outputs[0], mix.inputs[2])
    nt.links.new(mix.outputs[0], out.inputs[0])
    return sc


def mat(name, rgb, rough=0.55, metal=0.0, alpha=1.0, transm=0.0, coat=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*rgb, 1)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    if "Transmission Weight" in b.inputs:
        b.inputs["Transmission Weight"].default_value = transm
    if "Coat Weight" in b.inputs:
        b.inputs["Coat Weight"].default_value = coat
    b.inputs["Alpha"].default_value = alpha
    if alpha < 1:
        m.blend_method = "BLEND" if hasattr(m, "blend_method") else None
    return m


def srgb(h):
    h = h.lstrip("#")
    c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    return tuple(((x + 0.055) / 1.055) ** 2.4 if x > 0.04045 else x / 12.92 for x in c)


MAT = {}


def materials():
    MAT["pet"] = mat("PET-CF", srgb("#2e3135"), rough=0.6)
    MAT["pet_light"] = mat("PET-CF light", srgb("#6b7078"), rough=0.6)
    MAT["fixed"] = mat("fixed", srgb("#d9772b"), rough=0.5)
    MAT["design_glass"] = mat("design space", srgb("#9fb7d0"), rough=0.3, alpha=0.18)
    MAT["tpu"] = mat("TPU", srgb("#d9772b"), rough=0.45)
    MAT["metal_dark"] = mat("anodised", srgb("#26282c"), rough=0.35, metal=0.9)
    MAT["metal"] = mat("steel", srgb("#b8bcc2"), rough=0.28, metal=1.0)
    MAT["copper"] = mat("copper", srgb("#b87333"), rough=0.35, metal=1.0)
    MAT["prop"] = mat("propeller", srgb("#c9ccd1"), rough=0.25, alpha=0.55, transm=0.4)
    MAT["pcb"] = mat("pcb", srgb("#1d1f23"), rough=0.4, coat=0.5)
    MAT["chip"] = mat("chip", srgb("#111214"), rough=0.5)
    MAT["batt"] = mat("battery", srgb("#18191b"), rough=0.5)
    MAT["batt_label"] = mat("battery label", srgb("#c8322b"), rough=0.45)
    MAT["rubber"] = mat("rubber", srgb("#121314"), rough=0.85)
    MAT["xt30"] = mat("xt30", srgb("#e8c021"), rough=0.4)
    MAT["shrink_blue"] = mat("heat shrink", srgb("#2c5aa8"), rough=0.5)
    MAT["ceramic"] = mat("ceramic", srgb("#c8b48a"), rough=0.6)
    MAT["silver_patch"] = mat("patch", srgb("#d8d8d8"), rough=0.3, metal=0.8)
    MAT["wire_red"] = mat("wire red", srgb("#b3261e"), rough=0.5)
    MAT["wire_black"] = mat("wire black", srgb("#141414"), rough=0.5)
    MAT["strap"] = mat("strap", srgb("#202224"), rough=0.9)
    MAT["floor"] = mat("floor", (0.8, 0.8, 0.8), rough=0.9)


def link(obj, m):
    obj.data.materials.clear()
    obj.data.materials.append(m)
    return obj


def smooth(obj, angle=35):
    for p in obj.data.polygons:
        p.use_smooth = True
    try:
        obj.data.set_sharp_from_angle(angle=math.radians(angle))
    except Exception:
        pass
    return obj


def stl(path, m, name=None, offset=(0, 0, 0), sm=True):
    bpy.ops.wm.stl_import(filepath=path)
    o = bpy.context.selected_objects[0]
    o.name = name or os.path.basename(path)
    o.scale = (S, S, S)
    o.location = Vector(offset) * S
    if sm:
        smooth(o)
    return link(o, m)


# ------------------------------------------------------------------ primitives (mm in, scene units out)
def cyl(r, z0, z1, x=0, y=0, m=None, verts=64, axis="z", name="cyl", bevel=0.0):
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=r * S, depth=(z1 - z0) * S)
    o = bpy.context.object
    o.name = name
    if axis == "z":
        o.location = (x * S, y * S, 0.5 * (z0 + z1) * S)
    elif axis == "x":
        o.rotation_euler = (0, math.pi / 2, 0)
        o.location = (0.5 * (z0 + z1) * S, x * S, y * S)
    elif axis == "y":
        o.rotation_euler = (math.pi / 2, 0, 0)
        o.location = (x * S, 0.5 * (z0 + z1) * S, y * S)
    if bevel:
        mod = o.modifiers.new("b", "BEVEL")
        mod.width = bevel * S
        mod.segments = 3
    smooth(o, 40)
    return link(o, m) if m else o


def box(x0, x1, y0, y1, z0, z1, m=None, name="box", bevel=0.0):
    bpy.ops.mesh.primitive_cube_add(size=1)
    o = bpy.context.object
    o.name = name
    o.scale = ((x1 - x0) * S, (y1 - y0) * S, (z1 - z0) * S)
    o.location = (0.5 * (x0 + x1) * S, 0.5 * (y0 + y1) * S, 0.5 * (z0 + z1) * S)
    bpy.ops.object.transform_apply(scale=True)
    if bevel:
        mod = o.modifiers.new("b", "BEVEL")
        mod.width = bevel * S
        mod.segments = 4
        mod.limit_method = "ANGLE"
    smooth(o, 40)
    return link(o, m) if m else o


def boolean_diff(target, cutter):
    mod = target.modifiers.new("cut", "BOOLEAN")
    mod.operation = "DIFFERENCE"
    mod.object = cutter
    mod.solver = "EXACT"
    bpy.context.view_layer.objects.active = target
    bpy.ops.object.modifier_apply(modifier=mod.name)
    bpy.data.objects.remove(cutter, do_unlink=True)


# ------------------------------------------------------------------ components
def motor(sx, sy):
    x, y = sx * M, sy * M
    base = cyl(10.4, 0.0, 3.0, x, y, MAT["metal"], name="motor_base", bevel=0.3)
    bell = cyl(10.4, 3.3, 15.5, x, y, MAT["metal_dark"], name="motor_bell", bevel=0.6)
    # six cooling slots in the bell side, and the stator copper visible through them
    cyl(9.2, 3.6, 12.0, x, y, MAT["copper"], name="stator")
    for k in range(6):
        a = k * math.pi / 3 + math.pi / 6
        c = box(-1.6, 1.6, -6, 6, 5.0, 10.5, name="slot")
        c.rotation_euler = (0, 0, a)
        c.location = (x * S + 9.5 * S * math.cos(a), y * S + 9.5 * S * math.sin(a), 7.75 * S)
        boolean_diff(bell, c)
    cyl(1.0, 15.5, 22.5, x, y, MAT["metal"], name="shaft")
    cyl(3.0, 15.5, 16.2, x, y, MAT["metal"], name="bell_cap")


def propeller(sx, sy, spin):
    """Three twisted blades, R 44.45, pitch 50.8 mm; blade chord peaks at 0.35 R."""
    x0, y0, zc = sx * M, sy * M, 17.0
    cyl(4.0, 15.6, 21.0, x0, y0, MAT["prop"], name="hub")
    R, P = 44.45, 50.8
    me = bpy.data.meshes.new("blades")
    bm = bmesh.new()
    nr, nc = 40, 10
    for b in range(3):
        phi0 = b * 2 * math.pi / 3
        rows = []
        for i in range(nr + 1):
            r = 4.0 + (R - 4.0) * i / nr
            t = (r - 4.0) / (R - 4.0)
            chord = 5.5 + 7.0 * math.sin(math.pi * min(t / 0.7, 1.0) * 0.5) * (1 - 0.55 * max(0, (t - 0.35) / 0.65)) if t < 1 else 4.0
            chord = max(chord * (1 - 0.8 * t ** 6), 2.5)
            th = math.atan(P / (2 * math.pi * r)) * spin
            thick = 1.4 - 0.9 * t
            row = []
            for j in range(nc + 1):
                s = -0.5 + j / nc                      # chordwise position
                for side in (1, -1):
                    pass
                row.append((s * chord, thick * 0.5 * math.sqrt(max(0, 1 - (2 * s) ** 2))))
            rows.append((r, th, row))
        verts = []
        for (r, th, row) in rows:
            up, lo = [], []
            for (s, h) in row:
                for hh, lst in ((h, up), (-h, lo)):
                    # blade section in the local frame (chordwise c, normal n), rotated by the pitch angle th
                    c, n = s, hh
                    lx = c * math.cos(th) - n * math.sin(th) * 0
                    tz = c * math.sin(th) + n * math.cos(th)
                    tc = c * math.cos(th) - n * math.sin(th)
                    ang = phi0
                    px = x0 + r * math.cos(ang) - tc * math.sin(ang)
                    py = y0 + r * math.sin(ang) + tc * math.cos(ang)
                    lst.append(bm.verts.new(((px) * S, (py) * S, (zc + tz) * S)))
            verts.append(up + lo[::-1])
        for a, bb in zip(verts[:-1], verts[1:]):
            n = len(a)
            for k in range(n):
                bm.faces.new((a[k], a[(k + 1) % n], bb[(k + 1) % n], bb[k]))
        bm.faces.new(verts[0][::-1])
        bm.faces.new(verts[-1])
    bm.to_mesh(me)
    bm.free()
    o = bpy.data.objects.new("blades", me)
    bpy.context.collection.objects.link(o)
    smooth(o, 60)
    link(o, MAT["prop"])


def battery():
    box(-29.5, 29.5, -15.0, 15.0, 24.2, 56.0, MAT["batt"], name="battery", bevel=2.0)
    box(-29.6, 29.6, -15.1, 15.1, 36.0, 44.0, MAT["batt_label"], name="label", bevel=1.0)
    box(-8.0, 8.0, -17.7, 17.7, 56.0, 56.6, MAT["strap"], name="strap_top")
    for sy in (1, -1):
        box(-8.0, 8.0, sy * 17.1 - 0.3, sy * 17.1 + 0.3, 19.0, 56.6, MAT["strap"], name="strap_side")
    # XT30 on the lid tab and the lead
    box(34.0, 44.2, -2.6, 2.6, 24.0, 29.0, MAT["xt30"], name="xt30", bevel=0.4)
    for dy, m in ((1.3, MAT["wire_red"]), (-1.3, MAT["wire_black"])):
        cyl(0.9, 29.5, 34.0, dy, 27.0, m, axis="x", name="lead")


def flight_controller():
    box(-16.5, 16.5, -16.5, 16.5, -2.5, -0.9, MAT["pcb"], name="fc_pcb", bevel=0.3)
    box(-3.5, 3.5, -3.5, 3.5, -0.9, 0.1, MAT["chip"], name="mcu")
    for k in range(8):
        a = k * math.pi / 4
        box(-1.5, 1.5, -1.5, 1.5, -0.9, 0.2, MAT["chip"], name="fet").location = (11 * S * math.cos(a), 11 * S * math.sin(a), -0.35 * S)
    for sx, sy in CORNERS.values():
        x, y = sx * 12.75, sy * 12.75
        cyl(2.5, -5.0, 1.6, x, y, MAT["rubber"], name="grommet")
        cyl(2.31, 1.6, 4.1, x, y, MAT["metal"], verts=6, name="nut")
    # capacitor over the board
    cyl(5.25, -6.0, 15.0, -5.75, 10.25, MAT["batt"], axis="x", name="capacitor")


def receiver_gps_antenna():
    box(-9.2, 9.2, 2.75, 13.15, 5.5, 9.5, MAT["shrink_blue"], name="receiver", bevel=0.8)
    gx = -44.0
    box(gx - 8.5, gx + 8.5, -6.0, 6.0, 24.0, 25.5, MAT["pcb"], name="gps_pcb")
    box(gx - 6.0, gx + 6.0, -6.0, 6.0, 25.5, 29.0, MAT["ceramic"], name="gps_patch", bevel=0.4)
    box(gx - 4.0, gx + 4.0, -4.0, 4.0, 29.0, 29.1, MAT["silver_patch"], name="gps_patch_top")
    # T antenna under the K8 exit: stem up, legs along y at z -5.75
    ax, ay, zl = -49.0, 3.5, -5.75
    box(ax - 2.0, ax + 2.0, ay - 7.0, ay + 7.0, zl - 2.25, zl + 2.25, MAT["batt"], name="t_moulding", bevel=0.8)
    for s in (1, -1):
        cyl(0.7, ay + s * 7.0, ay + s * 21.0, ax, zl, MAT["batt"], axis="y", name="leg") if s > 0 else \
            cyl(0.7, ay - 21.0, ay - 7.0, ax, zl, MAT["batt"], axis="y", name="leg")
        cyl(2.0, ay + 21.0, ay + 26.0, ax, zl, MAT["batt"], axis="y", name="cap") if s > 0 else \
            cyl(2.0, ay - 26.0, ay - 21.0, ax, zl, MAT["batt"], axis="y", name="cap")


def joint_bolts():
    """Two steel M3 bolts per joint, axis horizontal and normal to the arm diagonal, at u 37.24, z -9.0 and +4.0."""
    uj = 37.24 / math.sqrt(2)
    for sx, sy in CORNERS.values():
        ang = math.atan2(sy, sx)             # cylinder axis after the rotation: (sin a, -cos a), normal to the arm
        for z in (-9.0, 4.0):
            o = cyl(1.5, -11.0, 11.0, 0, 0, MAT["metal"], verts=32, name="bolt")
            h = cyl(2.75, 11.0, 13.0, 0, 0, MAT["metal_dark"], verts=6, name="bolt_head")
            for ob in (o, h):
                ob.rotation_euler = (math.pi / 2, 0, ang)
                ob.location = (sx * uj * S, sy * uj * S, z * S)


# ------------------------------------------------------------------ frame
def frame(mode="print", explode=0.0):
    if mode in ("design", "fixed"):
        return frame_xray(mode)
    """mode 'print': printed parts; 'design': design space translucent over the result; 'fixed': fixed regions."""
    pr = lambda n: os.path.join(PRINT_DIR, n)
    have_print = os.path.isfile(pr("print_TUB_r4_iso030.stl"))
    if have_print:
        stl(pr("print_TUB_r4_iso030.stl"), MAT["pet"], "tub")
        stl(pr("print_LID_r4_iso030.stl"), MAT["pet"], "lid", offset=(0, 0, explode * 1.6))
        for t, (sx, sy) in CORNERS.items():
            o = stl(pr("print_ARM_pp_r4_iso030.stl"), MAT["pet"], "arm_" + t)
            o.rotation_euler = (0, 0, {"pp": 0, "pm": -math.pi / 2, "mp": math.pi / 2, "mm": math.pi}[t])
            o.location = Vector((sx * explode * 0.7, sy * explode * 0.7, 0)) * S
    else:
        for n in ("tub_design", "tub_fixed", "keel_a_r4", "keel_b_r4"):
            stl(os.path.join(MESH_DIR, n + ".stl"), MAT["pet"], n)
        for n in ("lid_design", "lid_fixed"):
            stl(os.path.join(MESH_DIR, n + ".stl"), MAT["pet"], n, offset=(0, 0, explode * 1.6))
        for t, (sx, sy) in CORNERS.items():
            for k in ("design", "fixed"):
                stl(os.path.join(MESH_DIR, "arm_%s_%s.stl" % (t, k)), MAT["pet"], "arm", offset=(sx * explode * 0.7, sy * explode * 0.7, 0))
    stl(os.path.join(MESH_DIR, "rx_cradle_v2.stl"), MAT["tpu"], "cradle", sm=False)
    stl(os.path.join(MESH_DIR, "gps_cap_v2.stl"), MAT["tpu"], "gps_cap", offset=(0, 0, explode * 1.2), sm=False)
    stl(os.path.join(ROOT, "geometry", "v04B_r3_f17", "ANTENNA_HOLDER_v04B_r3_TPU.stl"), MAT["tpu"], "holder", offset=(0, 0, -explode * 0.5))


def frame_xray(mode):
    pr = lambda n: os.path.join(PRINT_DIR, n)
    glass = MAT["design_glass"] if mode == "design" else mat("print glass", srgb("#5d636b"), rough=0.4, alpha=0.32)
    solid = MAT["pet"] if mode == "design" else MAT["fixed"]
    if mode == "design":
        stl(pr("print_TUB_r4_iso030.stl"), solid, "tub")
        o = stl(pr("print_ARM_pp_r4_iso030.stl"), solid, "arm")
        stl(os.path.join(MESH_DIR, "tub_design.stl"), glass, "tub_ds", sm=False)
        stl(os.path.join(MESH_DIR, "tub_fixed.stl"), glass, "tub_fx", sm=False)
        stl(os.path.join(MESH_DIR, "arm_pp_design.stl"), glass, "arm_ds", sm=False)
        stl(os.path.join(MESH_DIR, "arm_pp_fixed.stl"), glass, "arm_fx", sm=False)
    else:
        stl(pr("print_TUB_r4_iso030.stl"), glass, "tub")
        stl(pr("print_ARM_pp_r4_iso030.stl"), glass, "arm")
        stl(os.path.join(MESH_DIR, "tub_fixed.stl"), solid, "tub_fx", sm=False)
        stl(os.path.join(MESH_DIR, "arm_pp_fixed.stl"), solid, "arm_fx", sm=False)
        stl(os.path.join(MESH_DIR, "keel_a_r4.stl"), solid, "ka", sm=False)
        stl(os.path.join(MESH_DIR, "keel_b_r4.stl"), solid, "kb", sm=False)


def floor_and_lights(z0=-60):
    bpy.ops.mesh.primitive_plane_add(size=4, location=(0, 0, z0 * S))
    link(bpy.context.object, MAT["floor"])
    kl = float(os.environ.get("LIGHT", 0.3))
    for loc, energy, size in (((0.25, -0.35, 0.45), 60 * kl, 0.35), ((-0.4, 0.2, 0.3), 25 * kl, 0.5), ((0.0, 0.4, 0.6), 15 * kl, 0.6)):
        bpy.ops.object.light_add(type="AREA", location=loc)
        l = bpy.context.object
        l.data.energy = energy
        l.data.size = size
        d = Vector((0, 0, 0)) - Vector(loc)
        l.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()


def camera(loc, target, lens=50, ortho=None):
    bpy.ops.object.camera_add(location=loc)
    c = bpy.context.object
    d = Vector(target) - Vector(loc)
    c.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()
    c.data.lens = lens
    if ortho:
        c.data.type = "ORTHO"
        c.data.ortho_scale = ortho
    c.data.clip_start = 0.001
    bpy.context.scene.camera = c


VIEWS = {
    "R1_assembly": dict(cam=((0.30, -0.36, 0.26), (0.0, 0.0, 0.004), 60), res=(int(os.environ.get("RX", 2200)), int(os.environ.get("RY", 1400))), comps=True, explode=0),
    "R2_exploded": dict(cam=((0.30, -0.36, 0.34), (0.0, 0.0, 0.012), 55), res=(int(os.environ.get("RX", 2000)), int(os.environ.get("RY", 1250))), comps=False, explode=25),
    "R3_design_vs_result": dict(cam=((0.22, -0.26, 0.22), (0.005, 0.005, 0.0), 55), res=(int(os.environ.get("RX", 2000)), int(os.environ.get("RY", 1250))), comps=False, explode=0, mode="design"),
    "R6_fixed_regions": dict(cam=((0.22, -0.26, 0.22), (0.005, 0.005, 0.0), 55), res=(int(os.environ.get("RX", 2000)), int(os.environ.get("RY", 1250))), comps=False, explode=0, mode="fixed"),
    "R4_joint": dict(cam=((0.135, -0.035, 0.075), (0.033, 0.033, -0.002), 60), res=(int(os.environ.get("RX", 1800)), int(os.environ.get("RY", 1200))), comps=True, explode=0),
    "R5_rear_underside": dict(cam=((-0.20, -0.09, -0.075), (-0.040, 0.0, 0.004), 60), res=(int(os.environ.get("RX", 1800)), int(os.environ.get("RY", 1200))), comps=True, explode=0),
}


def render(view, samples=64):
    sc = reset()
    materials()
    v = VIEWS[view]
    frame(mode=v.get("mode", "print"), explode=v["explode"])
    if view == "R4_joint":
        joint_bolts()
    if v["comps"]:
        for sx, sy in CORNERS.values():
            motor(sx, sy)
            propeller(sx, sy, spin=1 if sx * sy > 0 else -1)
        battery()
        flight_controller()
        receiver_gps_antenna()
        joint_bolts()
    floor_and_lights(-16 if view != "R5_rear_underside" else -200)
    (loc, tgt, lens) = v["cam"]
    camera(loc, tgt, lens)
    sc.render.resolution_x, sc.render.resolution_y = v["res"]
    sc.cycles.samples = samples
    sc.render.filepath = os.path.join(OUT, view + ".png")
    bpy.ops.render.render(write_still=True)
    print("wrote", sc.render.filepath)


if __name__ == "__main__":
    view = sys.argv[1] if len(sys.argv) > 1 else "R1_assembly"
    smp = int(sys.argv[2]) if len(sys.argv) > 2 else 64
    render(view, smp)
