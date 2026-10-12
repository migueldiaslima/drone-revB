# -*- coding: ascii -*-
"""
s06_tangency_audit.py - gate G3: tangency audit of region boundaries (brief section 11).

The meshing failures of v03-B came from boundaries that touched tangentially or nearly so.
After a general fuse of all solids of a part (shared faces at design/fixed boundaries, as
Abaqus merges them), every solid is checked for the two shapes that produce slivers:
  (a) a wedge: two faces of one solid meeting along an edge at an interior angle below
      30 deg (a tangent contact gives 0 deg); sampled at 7 points per edge
  (b) a strip: two faces of one solid that share no vertex but come closer than 1.0 mm
      (one production element), e.g. a boundary running 0.14 mm from a tangent line
Feature table: for each named feature tool, the faces of the part lying on the tool
boundary, with the smallest interior angle at their edges and the smallest distance to any
face of the same solid they do not touch.
Usage: python3 s06_tangency_audit.py part.step [baseline.step]. ASCII only.
"""
import math
import sys
import cadquery as cq
from OCP.BOPAlgo import BOPAlgo_Builder
from OCP.BRep import BRep_Tool
from OCP.BRepAdaptor import BRepAdaptor_Curve, BRepAdaptor_Surface
from OCP.BRepClass import BRepClass_FaceClassifier
from OCP.BRepExtrema import BRepExtrema_DistShapeShape
from OCP.BRepTools import BRepTools
from OCP.BRepLProp import BRepLProp_SLProps
from OCP.GeomAPI import GeomAPI_ProjectPointOnSurf
from OCP.TopAbs import TopAbs_EDGE, TopAbs_FACE, TopAbs_IN, TopAbs_REVERSED, TopAbs_VERTEX, TopAbs_SOLID
from OCP.TopExp import TopExp, TopExp_Explorer
from OCP.TopTools import TopTools_IndexedDataMapOfShapeListOfShape, TopTools_IndexedMapOfShape
from OCP.TopoDS import TopoDS
from OCP.gp import gp_Pnt, gp_Pnt2d, gp_Vec

ANG_MIN = 30.0
DIST_MIN = 1.0


def fuse(path):
    shp = cq.importers.importStep(path)
    b = BOPAlgo_Builder()
    for s in shp.solids().vals():
        b.AddArgument(s.wrapped)
    b.Perform()
    out = []
    e = TopExp_Explorer(b.Shape(), TopAbs_SOLID)
    while e.More():
        out.append(TopoDS.Solid_s(e.Current()))
        e.Next()
    return out


def normal_at(face, p):
    surf = BRep_Tool.Surface_s(face)
    proj = GeomAPI_ProjectPointOnSurf(p, surf)
    u, v = proj.LowerDistanceParameters()
    ad = BRepAdaptor_Surface(face)
    pr = BRepLProp_SLProps(ad, u, v, 1, 1e-6)
    if not pr.IsNormalDefined():
        return None, (u, v)
    n = pr.Normal()
    nv = gp_Vec(n.X(), n.Y(), n.Z())
    if face.Orientation() == TopAbs_REVERSED:
        nv.Reverse()
    return nv, (u, v)


def inside(face, p):
    surf = BRep_Tool.Surface_s(face)
    proj = GeomAPI_ProjectPointOnSurf(p, surf)
    if proj.NbPoints() == 0 or proj.LowerDistance() > 1e-3:
        return False
    u, v = proj.LowerDistanceParameters()
    c = BRepClass_FaceClassifier(face, gp_Pnt2d(u, v), 1e-7)
    return c.State() == TopAbs_IN


def interior_angle(f1, f2, edge, t):
    ca = BRepAdaptor_Curve(edge)
    p = gp_Pnt(); d1 = gp_Vec()
    ca.D1(t, p, d1)
    if d1.Magnitude() < 1e-12:
        return None
    tv = d1.Normalized()
    n1, _ = normal_at(f1, p)
    n2, _ = normal_at(f2, p)
    if n1 is None or n2 is None:
        return None
    dirs = []
    for f, n in ((f1, n1), (f2, n2)):
        c = n.Crossed(tv)
        if c.Magnitude() < 1e-9:
            return None
        c.Normalize()
        ok = None
        for sgn in (1, -1):
            q = gp_Pnt(p.X() + sgn * 0.02 * c.X(), p.Y() + sgn * 0.02 * c.Y(), p.Z() + sgn * 0.02 * c.Z())
            if inside(f, q):
                ok = c.Multiplied(sgn)
                break
        if ok is None:
            return None
        dirs.append(ok)
    phi = math.degrees(dirs[0].Angle(dirs[1]))
    convex = n1.Dot(dirs[1]) < 0
    return phi if convex else 360.0 - phi


def audit_solid(sol, si):
    fmap = TopTools_IndexedMapOfShape()
    TopExp.MapShapes_s(sol, TopAbs_FACE, fmap)
    faces = [TopoDS.Face_s(fmap.FindKey(i)) for i in range(1, fmap.Extent() + 1)]
    ef = TopTools_IndexedDataMapOfShapeListOfShape()
    TopExp.MapShapesAndAncestors_s(sol, TopAbs_EDGE, TopAbs_FACE, ef)
    vf = TopTools_IndexedDataMapOfShapeListOfShape()
    TopExp.MapShapesAndAncestors_s(sol, TopAbs_VERTEX, TopAbs_FACE, vf)
    fidx = {}
    for i, f in enumerate(faces):
        fidx.setdefault(f.__hash__(), []).append((i, f))

    def index_of(f):
        for i, g in fidx.get(f.__hash__(), []):
            if g.IsSame(f):
                return i
        return None
    # adjacency through vertices
    adj = [set() for _ in faces]
    for k in range(1, vf.Extent() + 1):
        lst = [index_of(TopoDS.Face_s(x)) for x in vf.FindFromIndex(k)]
        lst = [x for x in lst if x is not None]
        for a in lst:
            adj[a].update(lst)
    edges = []
    for k in range(1, ef.Extent() + 1):
        e = TopoDS.Edge_s(ef.FindKey(k))
        if BRep_Tool.Degenerated_s(e):
            continue
        fl = [TopoDS.Face_s(x) for x in ef.FindFromIndex(k)]
        uniq = []
        for f in fl:
            if not any(f.IsSame(g) for g in uniq):
                uniq.append(f)
        if len(uniq) != 2:
            continue
        ca = BRepAdaptor_Curve(e)
        t0, t1 = ca.FirstParameter(), ca.LastParameter()
        angs = []
        for j in range(7):
            t = t0 + (t1 - t0) * (0.05 + 0.9 * j / 6.0)
            a = interior_angle(uniq[0], uniq[1], e, t)
            if a is not None:
                angs.append(a)
        if angs:
            pm = BRepAdaptor_Curve(e).Value(0.5 * (t0 + t1))
            edges.append((min(angs), index_of(uniq[0]), index_of(uniq[1]), (pm.X(), pm.Y(), pm.Z())))
    # strips: non-adjacent faces closer than DIST_MIN
    boxes = []
    for f in faces:
        bb = cq.Face(f).BoundingBox()
        boxes.append((bb.xmin, bb.ymin, bb.zmin, bb.xmax, bb.ymax, bb.zmax))
    strips = []
    nearest = [(1e9, None)] * len(faces)
    for i in range(len(faces)):
        for j in range(i + 1, len(faces)):
            if j in adj[i]:
                continue
            a, b = boxes[i], boxes[j]
            gap = max(a[0] - b[3], b[0] - a[3], a[1] - b[4], b[1] - a[4], a[2] - b[5], b[2] - a[5], 0.0)
            if gap > 3.0:
                continue
            d = BRepExtrema_DistShapeShape(faces[i], faces[j])
            d.Perform()
            v = d.Value()
            p = d.PointOnShape1(1)
            loc = (p.X(), p.Y(), p.Z())
            if v < nearest[i][0]:
                nearest[i] = (v, loc)
            if v < nearest[j][0]:
                nearest[j] = (v, loc)
            if v < DIST_MIN:
                strips.append((v, i, j, loc))
    return faces, edges, strips, nearest


def ftype(f):
    return cq.Face(f).geomType()


def run(path, features=None, verbose=True):
    sols = fuse(path)
    rep = {"file": path, "solids": len(sols), "wedges": [], "strips": [], "features": {}}
    allfaces = []
    for si, s in enumerate(sols):
        faces, edges, strips, nearest = audit_solid(s, si)
        allfaces.append((si, faces, edges, nearest))
        for a, i, j, p in edges:
            if a < ANG_MIN:
                rep["wedges"].append({"solid": si, "angle_deg": round(a, 2), "faces": (ftype(faces[i]), ftype(faces[j])),
                                      "at": tuple(round(c, 2) for c in p)})
        for v, i, j, p in strips:
            rep["strips"].append({"solid": si, "dist_mm": round(v, 3), "faces": (ftype(faces[i]), ftype(faces[j])),
                                  "at": tuple(round(c, 2) for c in p)})
    if features:
        for name, tool in features.items():
            amin, dmin, nf, where = 400.0, 1e9, 0, None
            for si, faces, edges, nearest in allfaces:
                on = set()
                for i, f in enumerate(faces):
                    pnt = point_on_face(f)
                    if min_face_dist(pnt, tool) < 1e-3:
                        on.add(i)
                nf += len(on)
                for a, i, j, p in edges:
                    if (i in on) != (j in on):
                        amin = min(amin, a)
                for i in on:
                    if nearest[i][0] < dmin:
                        dmin, where = nearest[i][0], nearest[i][1]
            rep["features"][name] = {"faces": nf, "min_interior_angle_deg": round(amin, 1) if amin < 400 else None,
                                     "min_dist_to_untouched_face_mm": round(dmin, 3) if dmin < 1e8 else None,
                                     "at": tuple(round(c, 2) for c in where) if where else None}
    if verbose:
        print("%s: %d solids, %d wedges < %g deg, %d strips < %g mm" % (path, len(sols), len(rep["wedges"]), ANG_MIN,
                                                                       len(rep["strips"]), DIST_MIN))
        for w in rep["wedges"]:
            print("   wedge", w)
        for s in sorted(rep["strips"], key=lambda x: x["dist_mm"]):
            print("   strip", s)
        for k, v in rep["features"].items():
            print("   feature %-34s %s" % (k, v))
    return rep


_FACE_CACHE = {}


class _P:
    def __init__(self, x, y, z):
        self.x, self.y, self.z = x, y, z


def point_on_face(f):
    u0, u1, v0, v1 = BRepTools.UVBounds_s(f)
    surf = BRep_Tool.Surface_s(f)
    for fu, fv in ((0.5, 0.5), (0.3, 0.5), (0.5, 0.3), (0.7, 0.6), (0.2, 0.2), (0.8, 0.8)):
        u, v = u0 + fu * (u1 - u0), v0 + fv * (v1 - v0)
        c = BRepClass_FaceClassifier(f, gp_Pnt2d(u, v), 1e-7)
        if c.State() == TopAbs_IN:
            p = surf.Value(u, v)
            return _P(p.X(), p.Y(), p.Z())
    p = surf.Value(0.5 * (u0 + u1), 0.5 * (v0 + v1))
    return _P(p.X(), p.Y(), p.Z())


def min_face_dist(pnt, tool):
    key = id(tool)
    if key not in _FACE_CACHE:
        _FACE_CACHE[key] = [f for s in tool.vals() for f in s.Faces()]
    v = cq.Vertex.makeVertex(pnt.x, pnt.y, pnt.z).wrapped
    best = 1e9
    for f in _FACE_CACHE[key]:
        bb = f.BoundingBox()
        if (pnt.x < bb.xmin - 0.01 or pnt.x > bb.xmax + 0.01 or pnt.y < bb.ymin - 0.01 or pnt.y > bb.ymax + 0.01
                or pnt.z < bb.zmin - 0.01 or pnt.z > bb.zmax + 0.01):
            continue
        d = BRepExtrema_DistShapeShape(v, f.wrapped)
        d.Perform()
        best = min(best, d.Value())
        if best < 1e-4:
            break
    return best


if __name__ == "__main__":
    for p in sys.argv[1:]:
        run(p)
