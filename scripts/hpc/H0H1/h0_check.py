# h0_check.py - H0 version check (D-061). Run on nemix in the H0 folder:
#   abq2025 python ../scripts/h0_check.py H0_ref
# Compares the Abaqus 2025 reference job with the local Abaqus 2022 values (N-06-07), tolerance 0.5 %.
from __future__ import print_function
import sys, os, re
from odbAccess import openOdb

job = sys.argv[-1] if len(sys.argv) > 1 else 'H0_ref'
TOL = 0.5  # per cent
REF_MASS_G = 333.70
REF_F = [489.93, 521.51, 524.32, 573.63, 681.81, 749.44]          # modes 7 to 12, Hz (local 2022)
REF_SE = {'LC1': 0.090893, 'LC2a': 0.069877, 'LC2b': 0.045459, 'LC3a': 0.10466}  # N mm (local 2022)
fails = []

def cmp(label, got, ref):
    d = 100.0 * (got - ref) / ref
    ok = abs(d) <= TOL
    print('%-22s %12.6g   local 2022 %12.6g   diff %+7.3f %%   %s' % (label, got, ref, d, 'PASS' if ok else 'FAIL'))
    if not ok:
        fails.append(label)

print('=== H0 check: %s ===' % job)
# mass from the .dat (printed by the analysis input processor)
mass = None
dat = job + '.dat'
if os.path.exists(dat):
    txt = open(dat).read()
    m = re.search(r'TOTAL MASS OF MODEL\s+([0-9.Ee+-]+)', txt)
    if m:
        mass = float(m.group(1)) * 1e6   # t -> g
if mass is None:
    print('mass: not found in %s (look for TOTAL MASS OF MODEL)' % dat)
    fails.append('mass not found')
else:
    cmp('mass (g)', mass, REF_MASS_G)

o = openOdb(os.path.abspath(job + '.odb'), readOnly=True)
st = o.steps['FREQ']
for i, ref in zip(range(7, 13), REF_F):
    d = st.frames[i].description
    f = float(re.search(r'Freq\s*=\s*([0-9.Ee+-]+)', d).group(1))
    cmp('f%d (Hz)' % i, f, ref)
for sn, ref in sorted(REF_SE.items()):
    s = o.steps[sn]
    hr = [r for k, r in s.historyRegions.items() if k.startswith('Assembly')][0]
    data = hr.historyOutputs['ALLSE'].data
    cmp('ALLSE %s (N mm)' % sn, data[len(data) - 1][1], ref)
ra = o.rootAssembly
for sn in sorted(REF_SE.keys()):
    fr = o.steps[sn].frames[len(o.steps[sn].frames) - 1]
    if 'RF' not in fr.fieldOutputs.keys():
        print('RF %s: not in output' % sn)
        continue
    tot = [0.0, 0.0, 0.0]; mx = 0.0
    for nm in ('SET_RP_JNT_PP', 'SET_RP_JNT_PM', 'SET_RP_JNT_MP'):
        key = [k for k in ra.nodeSets.keys() if k.upper() == nm]
        if not key:
            continue
        for val in fr.fieldOutputs['RF'].getSubset(region=ra.nodeSets[key[0]]).values:
            for i in range(3):
                tot[i] += val.data[i]
                mx = max(mx, abs(val.data[i]))
    good = mx < 1e-6
    print('RF %-5s max %.2e N, sum (%+.1e, %+.1e, %+.1e)   %s' % (sn, mx, tot[0], tot[1], tot[2], 'PASS' if good else 'FAIL'))
    if not good:
        fails.append('reactions ' + sn)
o.close()
print('=== H0 %s ===' % ('PASS' if not fails else 'FAIL: ' + ', '.join(fails)))
