# h3ref_check.py - H3 reference job at 1.0 mm (D-063): mass, modes 7 to 12, ALLSE and the caps
# (2 x ALLSE), support reactions, model size, run time and memory. Run in the H3ref folder:
#   abq2025 python ../scripts/h3ref_check.py H3_ref
from __future__ import print_function
import sys, os, re
from odbAccess import openOdb

job = sys.argv[-1] if len(sys.argv) > 1 else 'H3_ref'
H0_F = [489.93, 521.51, 524.32, 573.63, 681.81, 749.44]
H0_SE = {'LC1': 0.090893, 'LC2a': 0.069877, 'LC2b': 0.045459, 'LC3a': 0.10466}
print('=== H3 reference check: %s ===' % job)
for fn, pats in ((job + '.dat', (r'TOTAL MASS OF MODEL\s+\S+', r'NUMBER OF ELEMENTS IS\s+\d+',
                                 r'NUMBER OF NODES IS\s+\d+', r'TOTAL NUMBER OF VARIABLES IN THE MODEL\s+\d+',
                                 r'MEMORY TO MINIMIZE I/O[^\n]*\n[^\n]*\n[^\n]*\n[^\n]*')),
                 (job + '.msg', (r'WALLCLOCK TIME \(SEC\)\s*=\s*\d+', r'MAXIMUM MEMORY USED[^\n]*'))):
    if os.path.exists(fn):
        txt = open(fn, errors='replace').read()
        for p in pats:
            for s in re.findall(p, txt)[-1:]:
                print('  ' + ' '.join(s.split()))
o = openOdb(os.path.abspath(job + '.odb'), readOnly=True)
st = o.steps['FREQ']
for i, h0 in zip(range(7, 13), H0_F):
    f = float(re.search(r'Freq\s*=\s*([0-9.Ee+-]+)', st.frames[i].description).group(1))
    print('f%-2d %8.2f Hz   (2.5 / 1.5 mesh %8.2f, %+.2f %%)' % (i, f, h0, 100.0 * (f - h0) / h0))
print('step   ALLSE (N mm)   cap = 2 x ALLSE   (2.5 / 1.5 mesh ALLSE, diff)')
for sn in ('LC1', 'LC2a', 'LC2b', 'LC3a'):
    s = o.steps[sn]
    hr = [r for k, r in s.historyRegions.items() if k.startswith('Assembly')][0]
    d = hr.historyOutputs['ALLSE'].data
    se = d[len(d) - 1][1]
    print('%-5s %12.6g   %12.6g      (%.6g, %+.2f %%)' % (sn, se, 2 * se, H0_SE[sn], 100.0 * (se - H0_SE[sn]) / H0_SE[sn]))
ra = o.rootAssembly
for sn in ('LC1', 'LC2a', 'LC2b', 'LC3a'):
    fr = o.steps[sn].frames[len(o.steps[sn].frames) - 1]
    mx, n = 0.0, 0
    for nm in ('SET_RP_JNT_PP', 'SET_RP_JNT_PM', 'SET_RP_JNT_MP'):
        key = [k for k in ra.nodeSets.keys() if k.upper() == nm]
        if key:
            for v in fr.fieldOutputs['RF'].getSubset(region=ra.nodeSets[key[0]]).values:
                n += 1
                mx = max(mx, max(abs(x) for x in v.data[:3]))
    print('RF %-5s max %.2e N over %d support nodes   %s' % (sn, mx, n, 'ok' if (mx < 1e-6 and n == 3) else 'CHECK'))
o.close()
