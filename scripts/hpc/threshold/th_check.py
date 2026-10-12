# th_check.py - results of the thresholded jobs against Tosca cycle 40. Run in /tmp/mdias_H3/TH:
#   abaqus python ../scripts/th_check.py TH03 TH05
from __future__ import print_function
import sys, os, re
from odbAccess import openOdb

CAPS = [0.183803, 0.141901, 0.0923811, 0.213138]
rep = '../H3/TO_v03B_H3/optimization_report.csv'
tos = None
if os.path.exists(rep):
    for l in open(rep):
        if l.startswith('40,'):
            tos = [float(x) for x in l.split(',')[1:]]
rows = []
if tos:
    rows.append(('Tosca c40', None, tos[3:9], tos[9:13]))
for job in [a for a in sys.argv[1:] if not a.endswith('.py')]:
    mass = None
    if os.path.exists(job + '.dat'):
        m = re.findall(r'TOTAL MASS OF MODEL\s+([0-9.Ee+-]+)', open(job + '.dat', errors='replace').read())
        mass = float(m[-1]) * 1e6 if m else None
    o = openOdb(os.path.abspath(job + '.odb'), readOnly=True)
    st = o.steps['FREQ']
    fs = [float(re.search(r'Freq\s*=\s*([0-9.Ee+-]+)', st.frames[i].description).group(1)) for i in range(7, 13)]
    se = []
    for sn in ('LC1', 'LC2a', 'LC2b', 'LC3a'):
        hr = [r for k, r in o.steps[sn].historyRegions.items() if k.startswith('Assembly')][0]
        d = hr.historyOutputs['ALLSE'].data
        se.append(d[len(d) - 1][1])
    o.close()
    rows.append((job, mass, fs, se))
print('%-10s %8s | %s | %s' % ('model', 'mass g', '  f7     f8     f9    f10    f11    f12 (Hz)', 'SE/cap LC1  LC2a  LC2b  LC3a'))
for n, m, fs, se in rows:
    print('%-10s %8s | %s | %s' % (n, '%.1f' % m if m else '-', ' '.join('%6.1f' % f for f in fs),
                                  '  '.join('%5.2f' % (s / c) for s, c in zip(se, CAPS))))
print('pass criteria: modes 7 to 12 >= 417 Hz (goal) / 290 Hz (hard, D-035); SE/cap <= 1; D-066: within 5 % of Tosca')
