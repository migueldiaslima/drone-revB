# th04_build.py - D-082 (b): thresholded jobs of H4 cycle 31 at iso 0.4 with both lid connections.
#   TH04b: lid tied over the seat (TIE_LIDRIM, as optimised)
#   TH04a: lid tied at the five screw bosses only (TIE_LID_1..5, G7a)
# Elements with density >= 0.4: stiffness and mass factor 1; others: stiffness 1e-6, mass 1e-9 (air).
# Tosca-only keywords removed (SENSITIVITY, DESIGN RESPONSE blocks); Lanczos shift kept (DV-24).
# Run in /tmp/mdias_H4/TH:   abaqus python ~/drone_revB/stage6/scripts/th04_build.py c31.odb
from __future__ import print_function
import sys, re
import numpy as np
from odbAccess import openOdb

ISO = 0.4
odbp = [a for a in sys.argv[1:] if a.lower().endswith('.odb')][0]
MODEL = 'TO_v04B_H4-Job.inp'
DIST = 'tosca_distribution.inp'

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

tab, head, cur = {}, {}, None
for ln in open(DIST).read().splitlines():
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
print('distribution rows: stiffness %d, mass %d' % (len(tab.get('S', {})), len(tab.get('M', {}))))
if len(tab.get('S', {})) == 0 or len(tab.get('M', {})) == 0:
    print('first lines of %s:' % DIST)
    print('\n'.join(open(DIST).read().splitlines()[:12]))
    raise SystemExit('distribution tables not parsed: send the lines above')

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
lines = out
# Lanczos shift (DV-24)
for i, ln in enumerate(lines):
    if ln.upper().startswith('*FREQUENCY') and i + 1 < len(lines):
        if re.match(r'^\s*20,\s*,\s*,\s*,', lines[i + 1]):
            lines[i + 1] = '20, , , -100., ,'
        print('frequency data line: %s' % lines[i + 1])
base = '\n'.join(lines) + '\n'
if not re.search(r'^\*Include, input=' + re.escape(DIST), base, flags=re.M | re.I):
    raise SystemExit('include of %s not found in %s' % (DIST, MODEL))

# tie variants
m = re.search(r'^(\*Tie,[^\n]*name=TIE_LIDRIM[^\n]*)\n([^\n]*)\n', base, flags=re.M | re.I)
if not m:
    raise SystemExit('TIE_LIDRIM block not found')
hdr, data = m.group(1), m.group(2)
print('seat tie: %s | %s' % (hdr, data))
five = ''
for k in range(1, 6):
    five += re.sub(r'name=TIE_LIDRIM', 'name=TIE_LID_%d' % k, hdr, flags=re.I) + '\n'
    five += 'TUB-1_S_TUB_BOSS_%d, LID-1_S_LID_PAD_%d\n' % (k, k)
variants = {'TH04b': base, 'TH04a': base.replace(m.group(0), five)}
print('TH04a ties:\n' + five)

dname = 'dist_TH04.inp'
nsol = 0
with open(dname, 'w') as f:
    for k, lo in (('S', 1e-6), ('M', 1e-9)):
        f.write('\n'.join(head[k]) + '\n')
        for l in sorted(tab[k]):
            solid = rho.get(l, 1.0) >= ISO
            if k == 'S' and solid:
                nsol += 1
            f.write('%d, %.6e, %.6e\n' % (l, 1.0 if solid else lo, tab[k][l][1]))
for tag, t in variants.items():
    t2 = re.sub(r'^(\*Include, input=)' + re.escape(DIST), r'\g<1>' + dname, t, flags=re.M | re.I)
    open(tag + '.inp', 'w').write(t2)
    print('%s.inp written (%d ties named TIE_LID)' % (tag, len(re.findall(r'name=TIE_LID', t2, flags=re.I))))
print('iso %.1f: %d of %d design elements solid' % (ISO, nsol, len(tab['S'])))
