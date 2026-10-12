# -*- coding: ascii -*-
"""s06_gmsh_meshtest.py - independent meshing test for design/fixed split STEP files.
Imports all solids, fragments them (shared faces at the internal boundaries, as Abaqus
'merge, retain intersecting boundaries'), meshes with 2nd-order-ready linear tets at a given
size, and reports success, element count and the worst element quality (gamma: 1 = ideal,
near 0 = sliver). Usage: python3 s06_gmsh_meshtest.py size file.step [...]. ASCII only."""
import sys
import gmsh


def mesh_test(path, h):
    gmsh.initialize()
    gmsh.option.setNumber("General.Terminal", 0)
    gmsh.option.setNumber("Geometry.OCCImportLabels", 0)
    gmsh.model.add("t")
    try:
        ents = gmsh.model.occ.importShapes(path)
        vols = [e for e in ents if e[0] == 3]
        if len(vols) > 1:
            gmsh.model.occ.fragment(vols[:1], vols[1:])
        gmsh.model.occ.synchronize()
        gmsh.option.setNumber("Mesh.MeshSizeMax", h)
        gmsh.option.setNumber("Mesh.MeshSizeMin", h / 50.0)
        gmsh.option.setNumber("Mesh.MeshSizeFromCurvature", 12)
        gmsh.option.setNumber("Mesh.Algorithm3D", 1)
        gmsh.model.mesh.generate(3)
        types, tags, _ = gmsh.model.mesh.getElements(3)
        n = sum(len(t) for t in tags)
        allt = [x for t in tags for x in t]
        q = gmsh.model.mesh.getElementQualities(allt, "gamma") if allt else [0]
        qmin = min(q)
        nbad = sum(1 for x in q if x < 0.05)
        return "OK", n, qmin, nbad, len(gmsh.model.getEntities(3))
    except Exception as ex:
        return "FAIL: %s" % str(ex)[:80], 0, 0.0, 0, 0
    finally:
        gmsh.finalize()


if __name__ == "__main__":
    h = float(sys.argv[1])
    for p in sys.argv[2:]:
        st, n, q, nb, nv = mesh_test(p, h)
        print("%-34s h=%.2f  %-6s volumes %2d  tets %7d  min gamma %.4f  tets below 0.05: %d"
              % (p.split("/")[-1], h, st, nv, n, q, nb))
