# R5 - read-only. Locates the untied tie secondary nodes (node set WarnNodeMissMainIntersect)
# in revB_v03B_ref.odb from the data check. Run with File > Run Script from the job folder.
from __future__ import print_function
from odbAccess import openOdb
import math, os
ODB = 'revB_v03B_ref.odb'
o = openOdb(os.path.abspath(ODB), readOnly=True)
ra = o.rootAssembly
key = [k for k in ra.nodeSets.keys() if k.upper() == 'WARNNODEMISSMAININTERSECT']
if not key:
    print('node set not found; assembly node sets: %s' % sorted(ra.nodeSets.keys()))
else:
    ns = ra.nodeSets[key[0]]
    R2 = 1.0 / math.sqrt(2.0)
    corners = {'pp': (1, 1), 'pm': (1, -1), 'mp': (-1, 1), 'mm': (-1, -1)}
    groups = {}
    other = []
    total = 0
    for inst_name, nodes in zip(ns.instanceNames, ns.nodes):
        for n in nodes:
            total += 1
            x, y, z = n.coordinates
            found = False
            for c, (sx, sy) in corners.items():
                s = (sx * x + sy * y) * R2
                t = (-sy * x + sx * y) * R2
                if s > 10 and abs(abs(t) - 5.0) < 0.01:
                    side = 'L' if t > 0 else 'R'
                    r = math.sqrt((s - 33.0) ** 2 + (z + 9.0) ** 2)   # distance from the lower bolt axis
                    g = groups.setdefault((c, side), [])
                    g.append((s, z, r))
                    found = True
            if not found:
                other.append((inst_name, n.label, x, y, z))
    print('=== R5: %d untied secondary nodes ===' % total)
    for k in sorted(groups.keys()):
        g = groups[k]
        zs = [v[1] for v in g]; ss = [v[0] for v in g]
        inside = len([v for v in g if v[2] < 5.9 and v[1] > -14.45])
        print('%s_%s: %3d nodes | z %.2f to %.2f | s %.2f to %.2f | inside prong disk and above z=-14.5: %d' % (
            k[0], k[1], len(g), min(zs), max(zs), min(ss), max(ss), inside))
    print('nodes not on a fin boss face: %d %s' % (len(other), other[:10]))
o.close()
