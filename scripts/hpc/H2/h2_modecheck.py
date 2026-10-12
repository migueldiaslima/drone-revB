# h2_modecheck.py - D-066 item 2 (spurious low-density modes) and D-064 support reactions
# on one saved Tosca cycle. Run on nemix:
#   abq2025 python ../scripts/h2_modecheck.py <saved cycle odb> [--probe]
# --probe also lists the steps and field outputs (use once on an H1 odb to confirm names).
# Last line: "RESULT cycle N: OK" or "RESULT cycle N: STOP (...)". h2_watch.sh reads it.
from __future__ import print_function
import sys, re
import numpy as np
from odbAccess import openOdb

ISO = 0.3        # D-066: low-density threshold
TOP = 0.8        # peak region of a mode: nodes with |U| >= TOP * max|U|
SPUR = 0.5       # spurious if more than this share of the peak nodes touch only elements below ISO
RF_LIM = 1e-6    # D-064: support reaction limit, N
STATIC = ('LC1', 'LC2a', 'LC2b', 'LC3a')
RP_SETS = ('SET_RP_JNT_PP', 'SET_RP_JNT_PM', 'SET_RP_JNT_MP')

path = [a for a in sys.argv[1:] if a.lower().endswith('.odb')][0]
probe = '--probe' in sys.argv
m = re.search(r'_(\d+)\.odb$', path)
cyc = m.group(1) if m else '?'
stops = []
o = openOdb(path, readOnly=True)
ra = o.rootAssembly

def last(seq):
    return seq[len(seq) - 1]

# ---------- density field ----------
cands = []
for sn in o.steps.keys():
    st = o.steps[sn]
    if len(st.frames) == 0:
        continue
    for fr in (st.frames[0], last(st.frames)):
        for k in fr.fieldOutputs.keys():
            ku = k.upper()
            if 'MAT_PROP' in ku or 'DENS' in ku or 'TOSCA' in ku:
                cands.append((sn, fr, k))
if probe:
    print('steps: %s' % ', '.join('%s (%d frames)' % (s, len(o.steps[s].frames)) for s in o.steps.keys()))
    for sn in o.steps.keys():
        if len(o.steps[sn].frames):
            print('  %s last frame fields: %s' % (sn, ', '.join(last(o.steps[sn].frames).fieldOutputs.keys())))
    print('density candidates: %s' % ', '.join('%s/%s' % (c[0], c[2]) for c in cands))
if not cands:
    print('no density field found in %s' % path)
    print('RESULT cycle %s: ERROR (no density field)' % cyc)
    sys.exit(0)
pick = [c for c in cands if 'MAT_PROP_NORMALIZED' in c[2].upper()] or cands
dsn, dfr, dkey = pick[0]
print('density field: %s in step %s' % (dkey, dsn))

dens_el = {}
dens_nd = {}
for b in dfr.fieldOutputs[dkey].bulkDataBlocks:
    iname = b.instance.name if b.instance is not None else ''
    data = np.asarray(b.data).reshape(-1) if np.asarray(b.data).ndim == 1 else np.asarray(b.data)[:, 0]
    if b.elementLabels is not None and len(b.elementLabels):
        tgt, labs = dens_el, np.asarray(b.elementLabels)
    else:
        tgt, labs = dens_nd, np.asarray(b.nodeLabels)
    for l, v in zip(labs.tolist(), data.tolist()):
        k = (iname, l)
        if v > tgt.get(k, -1.0):
            tgt[k] = v

# max density of the elements around each solid node (frozen elements without a value = 1)
nmax = {}
n_el = 0
for iname in ra.instances.keys():
    for e in ra.instances[iname].elements:
        if not e.type.startswith('C3D'):
            continue
        n_el += 1
        d = dens_el.get((iname, e.label), 1.0)
        for n in e.connectivity:
            k = (iname, n)
            if d > nmax.get(k, -1.0):
                nmax[k] = d
if dens_nd and not dens_el:
    for k in nmax:
        nmax[k] = dens_nd.get(k, 1.0)
print('solid elements %d, elements with density %d, below %.1f: %d' % (
    n_el, len(dens_el), ISO, sum(1 for v in dens_el.values() if v < ISO)))

# ---------- modes 7 to 12 ----------
st = o.steps['FREQ']
print('mode  freq(Hz)  peak nodes  share<%.1f  mean dens  max |U| at (instance, x, y, z)   verdict' % ISO)
for mi in range(7, 13):
    fr = st.frames[mi]
    f = float(re.search(r'Freq\s*=\s*([0-9.Ee+-]+)', fr.description).group(1))
    keys = []
    mags = []
    for b in fr.fieldOutputs['U'].bulkDataBlocks:
        if b.instance is None:
            continue
        iname = b.instance.name
        mg = np.sqrt((np.asarray(b.data)[:, :3] ** 2).sum(axis=1))
        for l, v in zip(np.asarray(b.nodeLabels).tolist(), mg.tolist()):
            if (iname, l) in nmax:
                keys.append((iname, l))
                mags.append(v)
    mags = np.asarray(mags)
    idx = np.where(mags >= TOP * mags.max())[0]
    dn = np.asarray([nmax[keys[i]] for i in idx])
    share = float((dn < ISO).sum()) / len(idx)
    k = keys[int(mags.argmax())]
    xyz = ra.instances[k[0]].getNodeFromLabel(k[1]).coordinates
    spur = share > SPUR
    print('%3d  %8.1f  %10d  %9.2f  %9.2f  %s (%.1f, %.1f, %.1f)   %s' % (
        mi, f, len(idx), share, dn.mean(), k[0], xyz[0], xyz[1], xyz[2], 'SPURIOUS' if spur else 'ok'))
    if spur:
        stops.append('mode %d spurious at %.1f Hz, %s (%.1f, %.1f, %.1f)' % (mi, f, k[0], xyz[0], xyz[1], xyz[2]))

# ---------- support reactions ----------
for sn in STATIC:
    if sn not in o.steps.keys():
        continue
    fr = last(o.steps[sn].frames)
    if 'RF' not in fr.fieldOutputs.keys():
        print('RF %s: not in output' % sn)
        continue
    mx = 0.0
    for nm in RP_SETS:
        key = [s for s in ra.nodeSets.keys() if s.upper() == nm]
        if not key:
            continue
        for v in fr.fieldOutputs['RF'].getSubset(region=ra.nodeSets[key[0]]).values:
            mx = max(mx, max(abs(x) for x in v.data[:3]))
    print('RF %-5s max %.2e N   %s' % (sn, mx, 'ok' if mx < RF_LIM else 'ABOVE LIMIT'))
    if mx >= RF_LIM:
        stops.append('reaction %s %.2e N' % (sn, mx))
o.close()
print('RESULT cycle %s: %s' % (cyc, 'OK' if not stops else 'STOP (' + '; '.join(stops) + ')'))
