# -*- coding: ascii -*-
"""s06_gmsh_meshtest_loc.py - s06_gmsh_meshtest.py plus the location of every tet below gamma 0.05
(clustered to 1 mm). Usage: python3 s06_gmsh_meshtest_loc.py size file.step [...]. ASCII only."""
import sys
import gmsh
import numpy as np


def run(path, h):
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
        types, tags, nodes = gmsh.model.mesh.getElements(3)
        allt = np.concatenate([np.asarray(t) for t in tags])
        q = np.asarray(gmsh.model.mesh.getElementQualities(list(allt), "gamma"))
        bad = allt[q < 0.05]
        locs = []
        for e in bad:
            _, nn, _, _ = gmsh.model.mesh.getElement(int(e))
            xyz = np.array([gmsh.model.mesh.getNode(int(n))[0] for n in nn[:4]])
            locs.append(xyz.mean(axis=0))
        clusters = []
        for p in locs:
            for c in clusters:
                if np.linalg.norm(c[0] - p) < 1.5:
                    c[1] += 1
                    break
            else:
                clusters.append([p, 1])
        return len(allt), float(q.min()), int((q < 0.05).sum()), clusters, len(gmsh.model.getEntities(3))
    finally:
        gmsh.finalize()


if __name__ == "__main__":
    h = float(sys.argv[1])
    for p in sys.argv[2:]:
        n, qmin, nb, cl, nv = run(p, h)
        print("%-24s h=%.2f volumes %2d tets %7d min gamma %.4f tets below 0.05: %d" % (p.split("/")[-1], h, nv, n, qmin, nb))
        for c, k in sorted(cl, key=lambda x: (round(x[0][2]), round(x[0][0]))):
            print("    %3d tets near (%.1f, %.1f, %.1f)" % (k, c[0], c[1], c[2]))
