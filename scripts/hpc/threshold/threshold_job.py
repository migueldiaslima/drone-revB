# threshold_job.py - D-066 item 3: plain Abaqus jobs on the H3 cycle 40 design cut at iso levels.
# Elements with density >= iso get stiffness and mass factor 1 (solid); the others get stiffness 1e-6
# and mass 1e-9 (air; the lower mass keeps air modes far above modes 7 to 12). Same flattened model
# Tosca ran (couplings, ties, point masses, steps); Tosca-only items removed (SENSITIVITY=ADJOINT,
# *DESIGN RESPONSE blocks). Also prints how Tosca 2024 scaled stiffness and mass against density
# (D-066 item 1). Run in /tmp/mdias_H3/TH:
#   abaqus python ../scripts/threshold_job.py c40.odb 0.3 0.5
from __future__ import print_function
import sys, re
import numpy as np
from odbAccess import openOdb

args = sys.argv[1:]
odbp = [a for a in args if a.lower().endswith('.odb')][0]
isos = [float(a) for a in args if not a.lower().endswith('.odb')] or [0.5]
MODEL = 'TO_v03B_H3-Job.inp'
DIST = 'tosca_distribution.inp'

# densities from the odb (flattened model, labels as in the input)
o = openOdb(odbp, readOnly=True)
st = o.steps['FREQ']
fr = [f for f in st.frames if any('MAT_PROP_NORMALIZED' in k.upper() for k in f.fieldOutputs.keys())][-1]
key = [k for k in fr.fieldOutputs.keys() if 'MAT_PROP_NORMALIZED' in k.upper()][0]
rho = {}
for b in fr.fieldOutputs[key].bulkDataBlocks:
    d = np.asarray(b.data).reshape(len(b.elementLabels), -1)[:, 0]
    for l, v in zip(np.asarray(b.elementLabels).tolist(), d.tolist()):
        rho[l] = max(v, rho.get(l, -1.0))
o.close()
print('densities read: %d elements' % len(rho))

# split the distribution file into its two tables
lines = open(DIST).read().splitlines()
tab = {}
cur = None
head = {}
for ln in lines:
    if ln.startswith('*DISTRIBUTION TABLE'):
        cur = 'S' if 'Stiffness' in ln else 'M'
        head[cur] = [ln]
        tab[cur] = {}
        continue
    if cur is None:
        continue
    if ln.startswith('*') or ln.startswith('  RATIO') or ln.startswith(' ,'):
        head[cur].append(ln)
        continue
    p = ln.split(',')
    tab[cur][int(p[0])] = (float(p[1]), float(p[2]))
print('table rows: stiffness %d, mass %d' % (len(tab['S']), len(tab['M'])))

# D-066 item 1: what Tosca used against density
print('\nTosca 2024 scaling against density (sample):')
print('   rho      stiffness   (rho^3)     mass        mass/rho')
labs = sorted(l for l in rho if l in tab['S'])
r = np.array([rho[l] for l in labs])
for target in (0.001, 0.01, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.8, 1.0):
    i = int(np.argmin(np.abs(r - target)))
    l = labs[i]
    s, m = tab['S'][l][0], tab['M'][l][0]
    print('  %6.4f   %10.4e  %10.4e  %10.4e  %8.3f' % (rho[l], s, rho[l] ** 3, m, m / max(rho[l], 1e-12)))

# thresholded tables and models
txt = open(MODEL).read()
txt = re.sub(r',\s*SENSITIVITY=ADJOINT', '', txt, flags=re.I)
out, skip = [], False
for ln in txt.splitlines():
    if ln.upper().startswith('*DESIGN RESPONSE'):
        skip = True
        continue
    if skip and ln.startswith('*') and not ln.startswith('**'):
        skip = False
    if not skip:
        out.append(ln)
base = '\n'.join(out) + '\n'
print('\nmodel: %d DESIGN RESPONSE blocks removed, SENSITIVITY removed' % len(re.findall(r'^\*DESIGN RESPONSE', txt, flags=re.M | re.I)))
for iso in isos:
    tag = 'TH%02d' % int(round(iso * 10))
    dname = 'dist_%s.inp' % tag
    nsol = 0
    with open(dname, 'w') as f:
        for k, lo, hi in (('S', 1e-6, 1.0), ('M', 1e-9, 1.0)):
            f.write('\n'.join(head[k]) + '\n')
            for l in sorted(tab[k]):
                solid = rho.get(l, 1.0) >= iso
                if k == 'S' and solid:
                    nsol += 1
                f.write('%d, %.6e, %.6e\n' % (l, hi if solid else lo, tab[k][l][1]))
    with open(tag + '.inp', 'w') as f:
        f.write(base.replace('*INCLUDE, INPUT=' + DIST, '*INCLUDE, INPUT=' + dname))
    print('%s: iso %.1f, %d of %d table elements solid -> %s.inp + %s' % (tag, iso, nsol, len(tab['S']), tag, dname))
