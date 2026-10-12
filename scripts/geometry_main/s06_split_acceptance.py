# -*- coding: ascii -*-
"""s06_split_acceptance.py - acceptance test for design/fixed splits (set-up chat rule):
after a general fuse of all solids of a part, no face below 0.5 mm^2 and none narrower than
0.3 mm (2 x area / perimeter). Usage: python3 s06_split_acceptance.py file1.step [...]. ASCII only."""
import sys
import cadquery as cq
from OCP.BOPAlgo import BOPAlgo_Builder
from OCP.TopTools import TopTools_ListOfShape


def test(path):
    shp = cq.importers.importStep(path)
    solids = shp.solids().vals()
    b = BOPAlgo_Builder()
    for s in solids:
        b.AddArgument(s.wrapped)
    b.Perform()
    fused = cq.Shape.cast(b.Shape())
    worst_a, worst_w, bad = 1e9, 1e9, 0
    for f in fused.Faces():
        a = f.Area()
        per = sum(e.Length() for e in f.Edges())
        w = 2 * a / per if per > 0 else 0
        worst_a, worst_w = min(worst_a, a), min(worst_w, w)
        if a < 0.5 or w < 0.3:
            bad += 1
    return len(solids), len(fused.Faces()), worst_a, worst_w, bad


if __name__ == "__main__":
    for p in sys.argv[1:]:
        n, nf, a, w, bad = test(p)
        print("%-45s solids %2d faces %5d  smallest %.3f mm^2  narrowest %.3f mm  failing %d %s"
              % (p.split("/")[-1], n, nf, a, w, bad, "PASS" if bad == 0 else "FAIL"))
