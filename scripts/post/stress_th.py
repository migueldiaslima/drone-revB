# stress_th.py - Stage 7 route A (build log items 66, 67; brief docs/stage7_brief.md): strength check of the
# thresholded print-geometry model TH_r4b_i30_final, static steps LC1, LC2a, LC2b, LC3a.
# Brief (c), (d): per part (TUB, LID, each ARM) and step, solid elements only (stiffness factor 1 in the TH
# distribution), element-average (centroid) stress = mean of the integration-point components, three checks:
#   VM   von Mises                      limit 36.3 MPa   (S_xy 54.4 / 1.5)
#   S33  tension across the layers     limit 15.9 MPa   (S_z 23.9 / 1.5; compression not checked)
#   TSH  sqrt(S13^2 + S23^2)            limit 15.9 MPa   (S_z as shear allowable, assumption)
# Acceptance (brief c): (1) volume-weighted 99.9th percentile <= limit; (2) elements above a limit grouped into
# edge-connected clusters (shared element edge = two shared corner nodes); a cluster passes if its volume is below
# 1 mm^3 and it touches the surface (has an element with a free face); reported with volume, centroid, fixed /
# design share and distance to the nearest coupling or tie node; (3) elements with a node on a coupling or tie
# surface (names read from the *Tie and *Coupling keywords of the TH .inp) are excluded and their maxima reported
# separately; (4) the ten highest elements per part and step (after exclusion) with coordinates.
# Writes stress_<job>_<step>.npz (centroids, volumes, VM, S33, TSH, part code, excluded flag) for the figure.
# Run on nexus in /tmp/mdias_H4r4/TH:
#   abaqus python ~/drone_revB/stage6/scripts/stress_th.py TH_r4b_i30_final.odb dist_TH_r4_i30_final.inp TH_r4b_i30_final.inp
# Stops with a clear message if S is missing, a part set or a tie / coupling surface is not found.
# ASCII only; abaqus python (py3) and python3 with the offline mock (scripts/post/test_stress/).
from __future__ import print_function
import sys, os, re
import numpy as np
from odbAccess import openOdb

args = sys.argv[1:]
odbp = [a for a in args if a.lower().endswith('.odb')]
inps = [a for a in args if a.lower().endswith('.inp')]
distp = [a for a in inps if os.path.basename(a).lower().startswith('dist')]
inpp = [a for a in inps if not os.path.basename(a).lower().startswith('dist')]
if not odbp or not distp or not inpp:
    raise SystemExit('usage: stress_th.py <TH odb> <dist_TH_...inp> <TH job .inp>')
odbp, distp, inpp = odbp[0], distp[0], inpp[0]
STEPS = ('LC1', 'LC2a', 'LC2b', 'LC3a')
LIM = (('VM', 'von Mises', 36.3), ('S33', 'S33 tension (across layers)', 15.9), ('TSH', 'sqrt(S13^2 + S23^2)', 15.9))
CL_VMAX = 1.0      # mm^3, cluster volume limit (brief c 2)
FACES = ((0, 1, 2), (0, 3, 1), (1, 3, 2), (2, 3, 0))     # C3D4 / C3D10 corner faces S1 to S4

# solid elements: stiffness factor 1 in the TH distribution
solid = []
cur = None
for ln in open(distp):
    if ln.startswith('*DISTRIBUTION TABLE'):
        cur = 'S' if 'Stiffness' in ln else 'M'
        continue
    if cur != 'S' or ln.startswith('*') or ln.startswith(' ') or not ln.strip():
        continue
    p = ln.split(',')
    if float(p[1]) > 0.5:
        solid.append(int(p[0]))
solid = np.asarray(solid)
print('%s: %d solid elements (stiffness factor 1)' % (distp, len(solid)))
if not len(solid):
    raise SystemExit('no solid element in %s' % distp)

# tie and coupling surfaces from the TH input
txt = open(inpp).read().splitlines()
surfs = []
for i, ln in enumerate(txt):
    u = ln.upper().replace(' ', '')
    if u.startswith('*TIE,'):
        j = i + 1
        while j < len(txt) and not txt[j].startswith('*'):
            surfs += [t.strip() for t in txt[j].split(',') if t.strip()]
            j += 1
    if u.startswith('*COUPLING,'):
        m = re.search(r'surface\s*=\s*([^,\s]+)', ln, flags=re.I)
        if m:
            surfs.append(m.group(1).strip())
surfs = sorted(set(surfs))
print('tie and coupling surfaces in %s: %d (%s)' % (inpp, len(surfs), ', '.join(surfs)))
if not surfs:
    raise SystemExit('no *Tie or *Coupling surface found in %s' % inpp)

o = openOdb(os.path.abspath(odbp), readOnly=True)
for sn in STEPS:
    if sn not in o.steps.keys():
        raise SystemExit('step %s not in the odb (steps: %s)' % (sn, list(o.steps.keys())))
    fr = o.steps[sn].frames[len(o.steps[sn].frames) - 1]
    print('step %s, last frame: field outputs %s' % (sn, sorted(fr.fieldOutputs.keys())))
    if 'S' not in fr.fieldOutputs.keys():
        raise SystemExit('S (stress) not written in step %s: rebuild the TH with TH_STRESS=1 (th04_build.py) and rerun' % sn)

ra = o.rootAssembly
inames = list(ra.instances.keys())
if len(inames) != 1:
    raise SystemExit('expected one (flattened) instance, found %s' % inames)
iname = inames[0]
ins = ra.instances[iname]
nl = np.asarray([n.label for n in ins.nodes])
X = np.zeros((nl.max() + 1, 3))
X[nl] = np.asarray([n.coordinates for n in ins.nodes], dtype=float)
els = [e for e in ins.elements if e.type.upper().startswith('C3D')]
el = np.asarray([e.label for e in els])
con = np.asarray([e.connectivity[:4] for e in els])
NE = el.max() + 1
row = -np.ones(NE, dtype=int)
row[el] = np.arange(len(el))
P = X[con]
cen = P.mean(axis=1)
vol = np.abs(np.einsum('ij,ij->i', P[:, 1] - P[:, 0], np.cross(P[:, 2] - P[:, 0], P[:, 3] - P[:, 0]))) / 6.0
issol = np.zeros(len(el), dtype=bool)
rs = row[solid[solid < NE]]
issol[rs[rs >= 0]] = True

# parts: TUB, LID, each ARM (element sets ending ALL_TUB, ALL_LID, ALL_ARM; arm named by its set prefix)
part = np.zeros(len(el), dtype=int)
pnames = {}
for k in sorted(ins.elementSets.keys()):
    ku = k.upper()
    for pn in ('TUB', 'LID', 'ARM'):
        if ku.endswith('ALL_' + pn):
            name = pn if pn != 'ARM' else 'ARM_' + re.sub(r'^ARM_?', '', ku.split('-')[0]).lower()
            code = len(pnames) + 1
            pnames[code] = name
            ls = np.asarray([e.label for e in ins.elementSets[k].elements])
            part[row[ls]] = code
design = np.zeros(len(el), dtype=bool)
for k in ins.elementSets.keys():
    if re.search(r'DESIGN_(TUB|LID|ARM)', k.upper()):
        ls = np.asarray([e.label for e in ins.elementSets[k].elements])
        design[row[ls]] = True
cnt = dict((pnames[c], int((part == c).sum())) for c in pnames)
print('parts: %s; design elements %d' % (', '.join('%s %d' % (k, cnt[k]) for k in sorted(cnt)), int(design.sum())))
narm = len([n for n in pnames.values() if n.startswith('ARM')])
if 'TUB' not in cnt or 'LID' not in cnt or narm != 4:
    raise SystemExit('part element sets not as expected (TUB, LID, 4 arms): %s' % cnt)

# nodes on tie and coupling surfaces
NODE_ON = np.zeros(nl.max() + 1, dtype=bool)
allsurf = {}
for k in ra.surfaces.keys():
    allsurf[k.upper()] = ra.surfaces[k]
for k in ins.surfaces.keys():
    allsurf.setdefault(k.upper(), ins.surfaces[k])
missing = []
for s in surfs:
    key = s.upper()
    cand = [k for k in allsurf if k == key or k.endswith('.' + key) or k.endswith('_' + key) or key.endswith(k)]
    if not cand:
        missing.append(s)
        continue
    srf = allsurf[cand[0]]
    nn = 0
    try:
        for arr in srf.nodes:
            ls = [n.label for n in arr]
            NODE_ON[ls] = True
            nn += len(ls)
    except Exception:
        pass
    if nn == 0:                     # fall back on element faces
        for arr, farr in zip(srf.elements, srf.faces):
            for e, f in zip(arr, farr):
                fi = int(re.sub(r'\D', '', str(f))) - 1
                c = e.connectivity
                NODE_ON[[c[q] for q in FACES[fi]]] = True
                nn += 3
    print('  surface %s (%s): %d nodes' % (s, cand[0], nn))
if missing:
    raise SystemExit('tie / coupling surfaces not found in the odb: %s (odb surfaces: %s)' % (missing, sorted(allsurf)[:40]))
excl = NODE_ON[con].any(axis=1)
print('elements with a node on a tie or coupling surface: %d (%d of them solid), excluded from the checks' % (
    int(excl.sum()), int((excl & issol).sum())))

# free faces of the solid body (surface elements)
sidx = np.nonzero(issol)[0]
fk = []
for a, b, c in FACES:
    f = np.sort(np.c_[con[sidx, a], con[sidx, b], con[sidx, c]], axis=1).astype(np.int64)
    fk.append(f[:, 0] * (1 << 42) + f[:, 1] * (1 << 21) + f[:, 2])
fk = np.concatenate(fk)
_, inv, fc = np.unique(fk, return_inverse=True, return_counts=True)
free = (fc[inv.ravel()] == 1).reshape(4, -1).any(axis=0)
surface = np.zeros(len(el), dtype=bool)
surface[sidx[free]] = True
print('solid elements with a free face (surface): %d of %d' % (int(surface.sum()), len(sidx)))
xn = np.nonzero(NODE_ON)[0]
XN = X[xn]


def wpct(x, w, q):
    o_ = np.argsort(x)
    cw = np.cumsum(w[o_])
    return x[o_][min(np.searchsorted(cw, q / 100.0 * cw[-1]), len(x) - 1)]


def clusters(idx):
    """edge-connected groups of element rows idx"""
    if not len(idx):
        return []
    par = np.arange(len(idx))

    def f(i):
        while par[i] != i:
            par[i] = par[par[i]]
            i = par[i]
        return i
    eg = {}
    for k, r in enumerate(idx.tolist()):
        c = con[r]
        for a in range(4):
            for b in range(a + 1, 4):
                key = (min(c[a], c[b]), max(c[a], c[b]))
                j = eg.get(key)
                if j is None:
                    eg[key] = k
                else:
                    ri, rj = f(k), f(j)
                    if ri != rj:
                        par[ri] = rj
    g = {}
    for k in range(len(idx)):
        g.setdefault(f(k), []).append(idx[k])
    return [np.asarray(v) for v in g.values()]


summary = []
for sn in STEPS:
    fr = o.steps[sn].frames[len(o.steps[sn].frames) - 1]
    acc = np.zeros((NE, 6))
    nip = np.zeros(NE)
    for blk in fr.fieldOutputs['S'].bulkDataBlocks:
        labs = np.asarray(blk.elementLabels).ravel()
        S = np.asarray(blk.data, dtype=float).reshape(len(labs), -1)
        if S.shape[1] < 6:
            raise SystemExit('S has %d components in step %s (expected 6)' % (S.shape[1], sn))
        np.add.at(acc, labs, S[:, :6])
        np.add.at(nip, labs, 1.0)
    Se = acc[el] / np.maximum(nip[el], 1)[:, None]
    has = nip[el] > 0
    a, b, c, d, e, f6 = [Se[:, i] for i in range(6)]
    VAL = {'VM': np.sqrt(0.5 * ((a - b) ** 2 + (b - c) ** 2 + (c - a) ** 2) + 3.0 * (d * d + e * e + f6 * f6)),
           'S33': c, 'TSH': np.sqrt(e * e + f6 * f6)}
    np.savez_compressed('stress_%s_%s.npz' % (os.path.splitext(os.path.basename(odbp))[0], sn),
                        cen=cen[issol & has].astype(np.float32), vol=vol[issol & has].astype(np.float32),
                        VM=VAL['VM'][issol & has].astype(np.float32), S33=c[issol & has].astype(np.float32),
                        TSH=VAL['TSH'][issol & has].astype(np.float32), part=part[issol & has], excl=excl[issol & has])
    print('=' * 24, sn)
    for code in sorted(pnames):
        pn = pnames[code]
        inp_ = issol & has & (part == code)
        chk = inp_ & ~excl
        ex = inp_ & excl
        for q, qn, lim in LIM:
            x = VAL[q]
            p999 = wpct(x[chk], vol[chk], 99.9)
            over = np.nonzero(chk & (x > lim))[0]
            cls = clusters(over)
            bad = []
            for cl in cls:
                v = vol[cl].sum()
                ok = v < CL_VMAX and surface[cl].any()
                ccen = (cen[cl] * vol[cl][:, None]).sum(axis=0) / v
                dist = np.sqrt(((XN - ccen) ** 2).sum(axis=1)).min() if len(XN) else -1.0
                if not ok:
                    bad.append(cl)
                print('  cluster %s %-4s %-3s: %d el., %.3f mm^3, max %.1f MPa at (%.1f, %.1f, %.1f), surface el. %d, design %d / fixed %d, '
                      'nearest tie/coupling node %.1f mm -> %s' % (sn, pn, q, len(cl), v, x[cl].max(), ccen[0], ccen[1], ccen[2],
                      int(surface[cl].sum()), int(design[cl].sum()), int((~design[cl]).sum()), dist, 'ok' if ok else 'FAIL'))
            res = 'PASS' if (p999 <= lim and not bad) else 'FAIL'
            exm = x[ex].max() if ex.any() else 0.0
            print('%-7s %-4s %-30s P99.9 %6.2f / %.1f MPa (util %.2f) | max %6.2f | above: %d el. in %d clusters (%d failing) | '
                  'excluded (tie/coupling) max %6.2f | %s' % (pn, sn, qn, p999, lim, p999 / lim, x[chk].max(), len(over), len(cls),
                                                            len(bad), exm, res))
            summary.append((pn, sn, q, p999 / lim, x[chk].max(), len(bad), res))
            top = np.nonzero(chk)[0][np.argsort(-x[chk])[:10]]
            print('        top 10 %s: %s' % (q, '; '.join('%.1f (%.1f, %.1f, %.1f)' % (x[t], cen[t][0], cen[t][1], cen[t][2]) for t in top)))
o.close()
print('=' * 24, 'summary (worst step per part and check)')
for pn in [pnames[c] for c in sorted(pnames)]:
    for q, qn, lim in LIM:
        r = [s for s in summary if s[0] == pn and s[2] == q]
        w = max(r, key=lambda s: s[3])
        print('%-7s %-4s P99.9 util %.2f (%s), max %.1f MPa, failing clusters %d -> %s' % (
            pn, q, w[3], w[1], max(s[4] for s in r), sum(s[5] for s in r), 'PASS' if all(s[6] == 'PASS' for s in r) else 'FAIL'))
g = max(summary, key=lambda s: s[3])
print('governing: %s %s %s, P99.9 util %.2f' % g[:4])
