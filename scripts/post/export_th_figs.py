# export_th_figs.py - report figures (build log item 70; docs/report_figures_setup.md items 7, 15, 16): export from the
# final thresholded model (odb, distribution, input) everything needed to draw, in the set-up workspace,
#   - the mode shapes 7 to 12 (displacement of the solid-body surface nodes),
#   - the mesh (surface triangles of the solid body, element counts per part),
#   - the set-up: tie and coupling surfaces (nodes), reference points, boundary conditions and loads per step.
# Writes th_figs.npz (numbers) and th_figs_setup.txt (the *Boundary, *Cload, *Dload, *Dsload, *Coupling, *Tie and
# *Mass blocks of the input as text, per step). Prints counts and checks; stops with a clear message on a mismatch.
# Run on nexus in /tmp/mdias_H4r4/TH (about 3 to 5 min):
#   abaqus python ~/drone_revB/stage6/scripts/export_th_figs.py TH_r4b_i30_final.odb dist_TH_r4_i30_final.inp TH_r4b_i30_final.inp
# ASCII only; abaqus python (py3) and python3 with the offline mock (scripts/post/test_stress/, mkmock_figs.py).
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
    raise SystemExit('usage: export_th_figs.py <TH odb> <dist_TH_...inp> <TH job .inp>')
odbp, distp, inpp = odbp[0], distp[0], inpp[0]
FACES = ((0, 1, 2), (0, 3, 1), (1, 3, 2), (2, 3, 0))

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
print('%s: %d solid elements' % (distp, len(solid)))

# input keywords for the set-up figure (text, per step)
txt = open(inpp).read().splitlines()
keep_kw = ('*BOUNDARY', '*CLOAD', '*DLOAD', '*DSLOAD', '*COUPLING', '*DISTRIBUTING', '*KINEMATIC', '*TIE', '*MASS',
           '*ELEMENT,TYPE=MASS', '*STEP', '*STATIC', '*FREQUENCY', '*ENDSTEP', '*INERTIARELIEF')
blocks, step, take = [], 'model', False
surfs = []
for i, ln in enumerate(txt):
    u = ln.upper().replace(' ', '')
    if ln.startswith('*') and not ln.startswith('**'):
        take = any(u.startswith(k) for k in keep_kw)
        if u.startswith('*STEP'):
            m = re.search(r'NAME=([^,]+)', ln, flags=re.I)
            step = m.group(1) if m else '?'
        if u.startswith('*TIE,'):
            j = i + 1
            while j < len(txt) and not txt[j].startswith('*'):
                surfs += [t.strip() for t in txt[j].split(',') if t.strip()]
                j += 1
        if u.startswith('*COUPLING,'):
            m = re.search(r'surface\s*=\s*([^,\s]+)', ln, flags=re.I)
            if m:
                surfs.append(m.group(1).strip())
    if take:
        blocks.append('%-6s | %s' % (step, ln))
surfs = sorted(set(surfs))
open('th_figs_setup.txt', 'w').write('\n'.join(blocks) + '\n')
print('th_figs_setup.txt: %d lines (boundary, loads, couplings, ties, masses, steps); %d tie / coupling surfaces' % (
    len(blocks), len(surfs)))

o = openOdb(os.path.abspath(odbp), readOnly=True)
ra = o.rootAssembly
inames = list(ra.instances.keys())
if len(inames) != 1:
    raise SystemExit('expected one (flattened) instance, found %s' % inames)
ins = ra.instances[inames[0]]
nl = np.asarray([n.label for n in ins.nodes])
X = np.zeros((nl.max() + 1, 3))
X[nl] = np.asarray([n.coordinates for n in ins.nodes], dtype=float)
els = [e for e in ins.elements if e.type.upper().startswith('C3D')]
el = np.asarray([e.label for e in els])
con = np.asarray([e.connectivity[:4] for e in els])
NE = el.max() + 1
row = -np.ones(NE, dtype=int)
row[el] = np.arange(len(el))
issol = np.zeros(len(el), dtype=bool)
rs = row[solid[solid < NE]]
issol[rs[rs >= 0]] = True
PCODE = {}
part = np.zeros(len(el), dtype=int)
for k in sorted(ins.elementSets.keys()):
    ku = k.upper()
    for pn in ('TUB', 'LID', 'ARM'):
        if ku.endswith('ALL_' + pn):
            name = pn if pn != 'ARM' else 'ARM_' + re.sub(r'^ARM_?', '', ku.split('-')[0]).lower()
            PCODE[name] = len(PCODE) + 1
            ls = np.asarray([e.label for e in ins.elementSets[k].elements])
            part[row[ls]] = PCODE[name]
counts = dict((n, (int((part == c).sum()), int(((part == c) & issol).sum()))) for n, c in PCODE.items())
print('elements per part (all / solid): %s' % ', '.join('%s %d / %d' % (n, a, b) for n, (a, b) in sorted(counts.items())))

# free faces of the solid body
sidx = np.nonzero(issol)[0]
F = np.vstack([np.c_[con[sidx, a], con[sidx, b], con[sidx, c]] for a, b, c in FACES])
fpart = np.tile(part[sidx], 4)
Fs = np.sort(F, axis=1).astype(np.int64)
key = Fs[:, 0] * (1 << 42) + Fs[:, 1] * (1 << 21) + Fs[:, 2]
_, inv, cnt = np.unique(key, return_inverse=True, return_counts=True)
free = cnt[inv.ravel()] == 1
SF, SP = F[free], fpart[free]
snodes = np.unique(SF)
idx = -np.ones(nl.max() + 1, dtype=int)
idx[snodes] = np.arange(len(snodes))
print('solid body surface: %d triangles, %d nodes' % (len(SF), len(snodes)))

# modes 7 to 12
st = o.steps['FREQ']
freqs, U = [], []
for i in range(7, 13):
    fr = st.frames[i]
    m = re.search(r'Freq\s*=\s*([0-9.Ee+-]+)', fr.description)
    freqs.append(float(m.group(1)) if m else float('nan'))
    u = np.zeros((nl.max() + 1, 3))
    for b in fr.fieldOutputs['U'].bulkDataBlocks:
        if b.instance is None or b.instance.name != inames[0]:
            continue
        u[np.asarray(b.nodeLabels).ravel()] = np.asarray(b.data, dtype=float).reshape(-1, 3)[:, :3]
    U.append(u[snodes].astype(np.float32))
    pk = snodes[np.argmax(np.linalg.norm(u[snodes], axis=1))]
    print('mode %d: %.1f Hz, peak surface node at (%.1f, %.1f, %.1f)' % (i, freqs[-1], X[pk][0], X[pk][1], X[pk][2]))

# tie and coupling surface nodes, reference points
surf_names, surf_nodes = [], []
allsurf = {}
for k in ra.surfaces.keys():
    allsurf[k.upper()] = ra.surfaces[k]
for k in ins.surfaces.keys():
    allsurf.setdefault(k.upper(), ins.surfaces[k])
for s in surfs:
    keyn = s.upper()
    cand = [k for k in allsurf if k == keyn or k.endswith('.' + keyn) or k.endswith('_' + keyn) or keyn.endswith(k)]
    if not cand:
        raise SystemExit('surface %s not found in the odb' % s)
    srf = allsurf[cand[0]]
    ns = []
    try:
        for item in srf.nodes:
            ns += [n.label for n in (item if not hasattr(item, 'label') else [item])]
    except Exception:
        ns = []
    if not ns:
        for arr, farr in zip(srf.elements, srf.faces):
            for e, f in zip(arr, farr):
                fi = int(re.sub(r'\D', '', str(f))) - 1
                ns += [e.connectivity[q] for q in FACES[fi]]
    ns = np.unique(np.asarray(ns, dtype=int))
    surf_names.append(s)
    surf_nodes.append(ns)
    print('  surface %-28s %6d nodes' % (s, len(ns)))
rp_names, rp_xyz = [], []
for src in [ra] + [ins]:
    for k in src.nodeSets.keys():
        if 'RP' in k.upper() or k.upper().startswith('CP_'):
            for item in src.nodeSets[k].nodes:
                for n in (item if not hasattr(item, 'label') else [item]):
                    rp_names.append(k)
                    rp_xyz.append(n.coordinates)
print('reference-point node sets: %d nodes in %d sets' % (len(rp_names), len(set(rp_names))))
o.close()

np.savez_compressed('th_figs.npz', X=X[snodes].astype(np.float32), faces=idx[SF].astype(np.int32),
                    face_part=SP.astype(np.int8), part_names=np.asarray(sorted(PCODE, key=lambda n: PCODE[n])),
                    U=np.stack(U), freqs=np.asarray(freqs),
                    surf_names=np.asarray(surf_names),
                    surf_xyz=np.asarray([X[n].astype(np.float32) for n in surf_nodes], dtype=object),
                    rp_names=np.asarray(rp_names), rp_xyz=np.asarray(rp_xyz, dtype=float).reshape(-1, 3),
                    counts=np.asarray([[PCODE[n]] + list(counts[n]) for n in counts]))
print('written th_figs.npz (%.1f MB)' % (os.path.getsize('th_figs.npz') / 1e6))
