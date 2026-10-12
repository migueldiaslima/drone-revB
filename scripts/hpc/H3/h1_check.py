# h1_check.py - H1 Tosca smoke test with inertia relief (D-061). Run on nemix in the H1 folder:
#   abq2025 python ../scripts/h1_check.py TO_v03B_H1
# Reads <job>/optimization_report.csv and <job>/TOSCA.OUT.
from __future__ import print_function
import sys, os, re

job = sys.argv[-1] if len(sys.argv) > 1 else 'TO_v03B_H1'
d = job
REF_F = [489.93, 521.51, 524.32, 573.63, 681.81, 749.44]
REF_SE = [0.090893, 0.069877, 0.045459, 0.10466]
CAPS = [0.18179, 0.13975, 0.09092, 0.20932]
fails = []

print('=== H1 check: %s ===' % job)
out = os.path.join(d, 'TOSCA.OUT')
if os.path.exists(out):
    keys = ('ERROR', 'inertia', 'INERTIA', 'PEDE', 'interpol', 'INTERPOL', 'not allowed', 'version', 'Version')
    seen = set()
    for line in open(out, errors='replace'):
        if any(k in line for k in keys):
            s = line.strip()[-150:]
            if s not in seen:
                seen.add(s)
                print('  TOSCA.OUT: ' + s)
    if 'not allowed' in open(out, errors='replace').read():
        fails.append('inertia relief refused')
else:
    print('TOSCA.OUT not found in %s' % d)
    fails.append('no TOSCA.OUT')

rep = os.path.join(d, 'optimization_report.csv')
if not os.path.exists(rep):
    print('optimization_report.csv not found')
    fails.append('no report')
else:
    rows = [l.strip().split(',') for l in open(rep) if l.strip()]
    hdr = [h.strip() for h in rows[0]]
    data = [[float(x) for x in r] for r in rows[2:]]   # row 1 is Norm-Values
    print('cycle  vol_frac   f7      f8      f9      f10     f11     f12   |  SE LC1    LC2a     LC2b     LC3a')
    for r in data:
        print('%3d   %7.4f  %s |  %s' % (int(r[0]), r[1], ' '.join('%7.1f' % v for v in r[4:10]),
                                         ' '.join('%8.5f' % v for v in r[10:14])))
    c0 = data[0]
    for i, (g, ref) in enumerate(zip(c0[4:10], REF_F)):
        if abs(g - ref) / ref > 0.005:
            fails.append('cycle 0 f%d differs from H0/local by more than 0.5 %%' % (i + 7))
    for i, (g, ref) in enumerate(zip(c0[10:14], REF_SE)):
        if abs(g - ref) / ref > 0.005:
            fails.append('cycle 0 SE %d differs from H0/local by more than 0.5 %%' % i)
    last = data[-1]
    if not last[1] < c0[1]:
        fails.append('volume did not fall')
    for i, v in enumerate(last[4:10]):
        if v < 417.0:
            print('  note: f%d = %.1f Hz below 417 at the last cycle (allowed transiently)' % (i + 7, v))
    for i, (v, cap) in enumerate(zip(last[10:14], CAPS)):
        print('  last cycle SE/cap LC%d: %.3f' % (i, v / cap))
    print('cycles completed: %d' % (len(data) - 1))
print('=== H1 %s ===' % ('PASS' if not fails else 'CHECK: ' + '; '.join(fails)))
