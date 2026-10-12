# th04_islands.py - TH04 diagnostic (build log item 43): why the thresholded models give f7 about 45 Hz
# while the static energies match Tosca. Read-only on the odbs.
#   1. Connected components of the solid elements (rho >= iso, densities of H4 cycle 31) at iso 0.4 and 0.3.
#      Elements are connected when they share a node; nodes of different elements closer than TOL are also
#      treated as connected (tied surfaces, joint gaps 0.150 mm). Every component other than the main frame
#      is listed with volume, mass, centroid and the instance node sets it touches (coupling and tie surfaces).
#   2. For each TH04 job: modes 7 to 12, peak region = nodes with |U| >= 0.8 max; which component the peak
#      nodes belong to, share of peak nodes that touch only air elements.
# Run in /tmp/mdias_H4/TH:
#   abaqus python ~/drone_revB/stage6/scripts/th04_islands.py c31.odb TH04b TH04a > TH04_islands.txt 2>&1
from __future__ import print_function
import sys, os, re
import numpy as np
from odbAccess import openOdb

ISOS = (0.4, 0.3)
TOL = 0.2           # mm, node proximity treated as a connection (ties)
RHO_MAT = 1.30e-3   # g/mm^3, PET-CF (as cyclecheck / item 15)
NLIST = 15          # islands listed per iso

args = [a for a in sys.argv[1:] if not a.endswith('.py')]
c31 = [a for a in args if a.lower().endswith('.odb')]
jobs = [a for a in args if not a.lower().endswith('.odb')]
if len(c31) != 1 or not jobs:
    raise SystemExit('usage: th04_islands.py c31.odb TH04b [TH04a]')

# densities of cycle 31 (same reading as th04_build.py)
o = openOdb(os.path.abspath(c31[0]), readOnly=True)
st = o.steps['FREQ']
fr = [f for f in st.frames if any('MAT_PROP_NORMALIZED' in k.upper() for k in f.fieldOutputs.keys())][-1]
key = [k for k in fr.fieldOutputs.keys() if 'MAT_PROP_NORMALIZED' in k.upper()][0]
rho = {}
for b in fr.fieldOutputs[key].bulkDataBlocks:
    d = np.asarray(b.data).reshape(len(b.elementLabels), -1)[:, 0]
    for l, v in zip(np.asarray(b.elementLabels).tolist(), d.tolist()):
        rho[l] = max(v, rho.get(l, -1.0))
o.close()
print('densities read: %d' % len(rho))

# mesh from the first TH04 odb (same deck as cycle 31)
o = openOdb(os.path.abspath(jobs[0] + '.odb'), readOnly=True)
insts = o.rootAssembly.instances
print('instances: %s' % ', '.join(insts.keys()))
nid = {}            # (inst, node label) -> index
xyz = []
for iname in insts.keys():
    for n in insts[iname].nodes:
        nid[(iname, n.label)] = len(xyz)
        xyz.append(n.coordinates)
xyz = np.asarray(xyz, dtype=float)
elab, econ, einst = [], [], []
for iname in insts.keys():
    for e in insts[iname].elements:
        if not e.type.upper().startswith('C3D'):
            continue
        elab.append(e.label)
        einst.append(iname)
        econ.append([nid[(iname, c)] for c in e.connectivity])
nel = len(elab)
corner = np.asarray([c[:4] for c in econ], dtype=int)
p = xyz[corner]
a = p[:, 1] - p[:, 0]
b = p[:, 2] - p[:, 0]
c = p[:, 3] - p[:, 0]
vol = np.abs(np.einsum('ij,ij->i', a, np.cross(b, c))) / 6.0
cen = p.mean(axis=1)
nodesets = {}
for iname in insts.keys():
    for k in insts[iname].nodeSets.keys():
        ns = insts[iname].nodeSets[k]
        if len(ns.nodes) < 60000:
            nodesets['%s.%s' % (iname, k)] = set(nid[(iname, n.label)] for n in ns.nodes)
print('solid elements in mesh: %d, nodes %d, total volume %.0f mm^3, node sets %d'
      % (nel, len(xyz), vol.sum(), len(nodesets)))
miss = len([l for l in elab if l not in rho])
if miss:
    print('note: %d elements without a density (taken as solid, as th04_build.py)' % miss)

def find(par, i):
    while par[i] != i:
        par[i] = par[par[i]]
        i = par[i]
    return i

def components(iso):
    solid = np.asarray([rho.get(l, 1.0) >= iso for l in elab])
    par = list(range(nel))
    owner = {}
    for i in np.nonzero(solid)[0].tolist():
        for n in econ[i]:
            j = owner.get(n)
            if j is None:
                owner[n] = i
            else:
                ri, rj = find(par, i), find(par, j)
                if ri != rj:
                    par[ri] = rj
    # proximity links between nodes of solid elements (ties)
    cell = {}
    for n in owner:
        k = tuple((xyz[n] // TOL).astype(int).tolist())
        cell.setdefault(k, []).append(n)
    nlink = 0
    for k, ns in cell.items():
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                for dz in (-1, 0, 1):
                    m = cell.get((k[0] + dx, k[1] + dy, k[2] + dz))
                    if not m:
                        continue
                    for n1 in ns:
                        for n2 in m:
                            if n2 <= n1:
                                continue
                            d = xyz[n1] - xyz[n2]
                            if d[0] * d[0] + d[1] * d[1] + d[2] * d[2] <= TOL * TOL:
                                ri, rj = find(par, owner[n1]), find(par, owner[n2])
                                if ri != rj:
                                    par[ri] = rj
                                    nlink += 1
    root = np.full(nel, -1)
    for i in np.nonzero(solid)[0].tolist():
        root[i] = find(par, i)
    node_comp = {}
    for n, i in owner.items():
        node_comp[n] = root[i]
    return solid, root, node_comp, nlink

res = {}
for iso in ISOS:
    solid, root, node_comp, nlink = components(iso)
    ids, inv = np.unique(root[solid], return_inverse=True)
    cvol = np.bincount(inv, weights=vol[solid])
    order = np.argsort(-cvol)
    main = ids[order[0]]
    print('\n== iso %.1f: %d solid elements, %d components (%d proximity links) ==' % (iso, solid.sum(), len(ids), nlink))
    print('main frame: %.0f mm^3 = %.2f g; all other components: %.1f mm^3 = %.3f g'
          % (cvol[order[0]], cvol[order[0]] * RHO_MAT, cvol.sum() - cvol[order[0]], (cvol.sum() - cvol[order[0]]) * RHO_MAT))
    print('%4s %10s %8s %24s %s' % ('#', 'vol mm^3', 'mass g', 'centroid (x, y, z) mm', 'node sets touched'))
    sel = np.nonzero(solid)[0]
    for r, k in enumerate(order[1:NLIST + 1].tolist()):
        mem = sel[inv == k]
        w = vol[mem]
        cc = (cen[mem] * w[:, None]).sum(axis=0) / w.sum()
        nodes = set()
        for i in mem.tolist():
            nodes.update(econ[i])
        touched = [s for s, ns in nodesets.items() if ns & nodes]
        print('%4d %10.1f %8.3f %24s %s' % (r + 1, cvol[k], cvol[k] * RHO_MAT,
              '(%.1f, %.1f, %.1f)' % tuple(cc.tolist()), ', '.join(sorted(touched)[:6]) or '-'))
    res[iso] = (main, node_comp, ids, order, inv)
o.close()

# modes against components at iso 0.4
main, node_comp, ids, order, inv = res[0.4]
rank = dict((ids[k], r) for r, k in enumerate(order.tolist()))
for job in jobs:
    o = openOdb(os.path.abspath(job + '.odb'), readOnly=True)
    st = o.steps['FREQ']
    print('\n== %s: modes 7 to 12 against the iso 0.4 components (0 = main frame) ==' % job)
    print('%4s %8s %6s %10s %10s %24s' % ('mode', 'f Hz', 'peak n', 'air-only', 'components', 'peak centroid'))
    for i in range(7, 13):
        frm = st.frames[i]
        f = float(re.search(r'Freq\s*=\s*([0-9.Ee+-]+)', frm.description).group(1))
        lab, mag = [], []
        for bb in frm.fieldOutputs['U'].bulkDataBlocks:
            if bb.instance is None:
                continue
            d = np.asarray(bb.data)
            mag += np.sqrt((d * d).sum(axis=1)).tolist()
            lab += [nid[(bb.instance.name, l)] for l in np.asarray(bb.nodeLabels).tolist()]
        mag = np.asarray(mag)
        lab = np.asarray(lab)
        pk = lab[mag >= 0.8 * mag.max()]
        comps = {}
        air = 0
        for n in pk.tolist():
            cmp_ = node_comp.get(n)
            if cmp_ is None:
                air += 1
            else:
                r = rank[cmp_]
                comps[r] = comps.get(r, 0) + 1
        cc = xyz[pk].mean(axis=0)
        cs = ' '.join('%d:%d' % (r, comps[r]) for r in sorted(comps)[:4]) or '-'
        print('%4d %8.1f %6d %10.2f %10s %24s' % (i, f, len(pk), float(air) / len(pk), cs,
              '(%.1f, %.1f, %.1f)' % tuple(cc.tolist())))
    o.close()
print('\ncomponents column: rank:count of peak nodes (rank 0 = main frame, 1.. = islands listed above at iso 0.4)')
