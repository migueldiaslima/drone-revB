# stress_th.py - Stage 7 route A (build log item 66): stresses of the thresholded print-geometry model
# TH_r4b_i30_final, static steps LC1, LC2a, LC2b, LC3a, solid elements only (distribution factor 1).
# Per part (TUB, LID, ARM) and step: element value = maximum over the integration points of
#   von Mises, maximum principal (tension), minimum principal (compression), S33 (global z normal);
# statistics over the solid elements: maximum, 99.9th and 99th percentile (by element count), the volume above
# each percentile, and the 5 highest elements with their centroids. With allowables given, the utilisation
# (value x FS / allowable) and the volume above allowable / FS.
# Run on nexus in /tmp/mdias_H4r4/TH:
#   abaqus python ~/drone_revB/stage6/scripts/stress_th.py TH_r4b_i30_final.odb dist_TH_r4_i30_final.inp
#   optional environment: ST_FS=1.5  ST_ALLOW_VM=<MPa>  ST_ALLOW_T=<MPa tension>  ST_ALLOW_C=<MPa compression>
#   ST_ALLOW_Z=<MPa, S33 tension>   (values from the Stage 7 brief; without them only stresses are printed)
# First prints the field outputs of each static step; stops with a clear message if S is not in the odb.
# ASCII only; runs under abaqus python (py3) and python3 with the offline mock (scripts/post/test_stress/).
from __future__ import print_function
import sys, os
import numpy as np
from odbAccess import openOdb

args = [a for a in sys.argv[1:]]
odbp = [a for a in args if a.lower().endswith('.odb')]
distp = [a for a in args if a.lower().endswith('.inp')]
if not odbp or not distp:
    raise SystemExit('usage: stress_th.py <TH odb> <dist_TH_...inp>')
odbp, distp = odbp[0], distp[0]
STEPS = ('LC1', 'LC2a', 'LC2b', 'LC3a')
FS = float(os.environ.get('ST_FS', '1.5'))
ALLOW = dict((k, float(os.environ[e])) for k, e in (('vm', 'ST_ALLOW_VM'), ('p1', 'ST_ALLOW_T'), ('p3', 'ST_ALLOW_C'), ('s33', 'ST_ALLOW_Z'))
             if os.environ.get(e))

# solid elements: stiffness factor 1 in the TH distribution
solid = set()
cur = None
for ln in open(distp):
    if ln.startswith('*DISTRIBUTION TABLE'):
        cur = 'S' if 'Stiffness' in ln else 'M'
        continue
    if cur != 'S' or ln.startswith('*') or ln.startswith(' ') or not ln.strip():
        continue
    p = ln.split(',')
    if float(p[1]) > 0.5:
        solid.add(int(p[0]))
print('%s: %d solid elements (stiffness factor 1)' % (distp, len(solid)))
if not solid:
    raise SystemExit('no solid element found in %s' % distp)

o = openOdb(os.path.abspath(odbp), readOnly=True)
for sn in STEPS:
    if sn not in o.steps.keys():
        raise SystemExit('step %s not in the odb (steps: %s)' % (sn, list(o.steps.keys())))
    fr = o.steps[sn].frames[len(o.steps[sn].frames) - 1]
    print('step %s, last frame: field outputs %s' % (sn, sorted(fr.fieldOutputs.keys())))
    if 'S' not in fr.fieldOutputs.keys():
        raise SystemExit('S (stress) not written in step %s: rebuild the TH with TH_STRESS=1 (th04_build.py) and rerun' % sn)

# parts, element centroids and volumes (corner nodes), as arrays indexed by element label per instance
inst_names = list(o.rootAssembly.instances.keys())
PCODE = {'TUB': 1, 'LID': 2, 'ARM': 3}
PNAME = dict((v, k) for k, v in PCODE.items())
geo = {}
cnt = {}
for iname in inst_names:
    ins = o.rootAssembly.instances[iname]
    nl = np.asarray([n.label for n in ins.nodes])
    if not len(nl):
        continue
    X = np.zeros((nl.max() + 1, 3))
    X[nl] = np.asarray([n.coordinates for n in ins.nodes], dtype=float)
    els = [e for e in ins.elements if e.type.upper().startswith('C3D')]
    if not els:
        continue
    el = np.asarray([e.label for e in els])
    con = np.asarray([e.connectivity[:4] for e in els])
    P = X[con]
    c = np.zeros((el.max() + 1, 3))
    v = np.zeros(el.max() + 1)
    c[el] = P.mean(axis=1)
    v[el] = np.abs(np.einsum('ij,ij->i', P[:, 1] - P[:, 0], np.cross(P[:, 2] - P[:, 0], P[:, 3] - P[:, 0]))) / 6.0
    part = np.zeros(el.max() + 1, dtype=int)
    for k in ins.elementSets.keys():
        for pn, code in PCODE.items():
            if k.upper().endswith('ALL_' + pn):
                ls = np.asarray([e.label for e in ins.elementSets[k].elements])
                part[ls[ls <= el.max()]] = code
    sol = np.zeros(el.max() + 1, dtype=bool)
    sl = np.asarray(sorted(solid))
    sol[sl[sl <= el.max()]] = True
    geo[iname] = dict(c=c, v=v, part=part, sol=sol, n=el.max() + 1)
    for code in (1, 2, 3):
        cnt[PNAME[code]] = cnt.get(PNAME[code], 0) + int((part == code).sum())
print('parts (element sets ALL_TUB / ALL_LID / ALL_ARM): %s' % ', '.join('%s %d' % (k, cnt[k]) for k in sorted(cnt)))
if any(cnt.get(k, 0) == 0 for k in PCODE):
    raise SystemExit('part element sets not found as expected: %s' % cnt)


def invariants(S):
    """S: n x 6 (S11, S22, S33, S12, S13, S23) -> von Mises, max principal, min principal"""
    a, b, c, d, e, f = [S[:, i] for i in range(6)]
    vm = np.sqrt(0.5 * ((a - b) ** 2 + (b - c) ** 2 + (c - a) ** 2) + 3.0 * (d * d + e * e + f * f))
    M = np.zeros((len(S), 3, 3))
    M[:, 0, 0], M[:, 1, 1], M[:, 2, 2] = a, b, c
    M[:, 0, 1] = M[:, 1, 0] = d
    M[:, 0, 2] = M[:, 2, 0] = e
    M[:, 1, 2] = M[:, 2, 1] = f
    w = np.linalg.eigvalsh(M)
    return vm, w[:, 2], w[:, 0]


QN = (('vm', 'von Mises'), ('p1', 'max principal'), ('p3', 'min principal'), ('s33', 'S33 (z)'))
summary = []
for sn in STEPS:
    fr = o.steps[sn].frames[len(o.steps[sn].frames) - 1]
    acc = {}
    for iname, g in geo.items():
        n = g['n']
        acc[iname] = np.vstack([np.full(n, -np.inf), np.full(n, -np.inf), np.full(n, np.inf), np.full(n, -np.inf)])
    for blk in fr.fieldOutputs['S'].bulkDataBlocks:
        iname = blk.instance.name if blk.instance is not None else inst_names[0]
        if iname not in geo:
            continue
        labs = np.asarray(blk.elementLabels).ravel()
        S = np.asarray(blk.data, dtype=float).reshape(len(labs), -1)
        if S.shape[1] < 6:
            raise SystemExit('S has %d components in step %s (expected 6, 3D solids)' % (S.shape[1], sn))
        vm, p1, p3 = invariants(S[:, :6])
        R = acc[iname]
        np.maximum.at(R[0], labs, vm)
        np.maximum.at(R[1], labs, p1)
        np.minimum.at(R[2], labs, p3)
        np.maximum.at(R[3], labs, S[:, 2])
    val = {}
    for iname, g in geo.items():
        R = acc[iname]
        ok = np.nonzero(g['sol'] & (g['part'] > 0) & np.isfinite(R[0]))[0]
        for code in (1, 2, 3):
            m = ok[g['part'][ok] == code]
            if len(m):
                val.setdefault(PNAME[code], []).append((R[:, m].T, g['v'][m], g['c'][m]))
    print('=' * 20, sn, '(%d solid elements with stress)' % sum(sum(len(t[1]) for t in v) for v in val.values()))
    for pn in ('TUB', 'LID', 'ARM'):
        if pn not in val:
            continue
        A = np.vstack([t[0] for t in val[pn]])
        V = np.concatenate([t[1] for t in val[pn]])
        C = np.vstack([t[2] for t in val[pn]])
        for j, (q, qn) in enumerate(QN):
            x = -A[:, j] if q == 'p3' else A[:, j]             # compression as a positive magnitude
            mx = x.max()
            p999, p99 = np.percentile(x, 99.9), np.percentile(x, 99.0)
            top = np.argsort(-x)[:5]
            line = '%-4s %-14s max %7.2f  p99.9 %7.2f  p99 %7.2f MPa' % (pn, qn, mx, p999, p99)
            if q in ALLOW:
                lim = ALLOW[q] / FS
                line += ' | allowable/FS %.2f: util max %.2f p99.9 %.2f, volume above %.3f mm^3 (%d el.)' % (
                    lim, mx / lim, p999 / lim, V[x > lim].sum(), int((x > lim).sum()))
                summary.append((sn, pn, q, mx / lim, p999 / lim))
            print(line)
            print('      top 5 at %s' % '; '.join('(%.1f, %.1f, %.1f) %.1f' % (C[t][0], C[t][1], C[t][2], x[t]) for t in top))
o.close()
if summary:
    print('=' * 20, 'utilisation (value x FS / allowable), worst per part and quantity over the four steps')
    for pn in ('TUB', 'LID', 'ARM'):
        for q, qn in QN:
            r = [s for s in summary if s[1] == pn and s[2] == q]
            if r:
                w = max(r, key=lambda s: s[4])
                print('%-4s %-14s p99.9 %.2f (%s), max %.2f -> %s' % (pn, qn, w[4], w[0], max(s[3] for s in r),
                      'PASS' if w[4] <= 1.0 else 'CHECK'))
    print('acceptance (proposed, Stage 7 brief): p99.9 utilisation <= 1; maxima listed for the peak locations')
