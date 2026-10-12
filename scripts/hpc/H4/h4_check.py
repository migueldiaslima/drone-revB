# h4_check.py - Tosca history for H4c / H4 (v04-B, G7b model). Run in the run folder on nexus:
#   abaqus python ../scripts/h4_check.py TO_v04B_H4c H4c        (or ... TO_v04B_H4 H4 c1 c2 c3 c4)
# Reads <job>/optimization_report.csv; prints every cycle (volume, f7 to f12, SE / cap) and a summary.
from __future__ import print_function
import sys, os
args = [a for a in sys.argv[1:]]
job, stage = args[0], args[1]
CAPS = {'H4c': [0.216635, 0.200186, 0.102227, 0.394042]}.get(stage) or [float(x) for x in args[2:6]]
rep = os.path.join(job, 'optimization_report.csv')
if not os.path.exists(rep):
    rep = None
if rep:
    rows = [l.strip().split(',') for l in open(rep) if l.strip()]
    data = [[float(x) for x in r] for r in rows[2:]]
else:
    # running or failed run: build the table from Tosca's report tables (volume, frequencies, strain energies)
    def tab(pat):
        import glob
        for d in (os.path.join(job, 'TOSCA_POST'), os.path.join(job, 'DB_ERROR'), job):
            g = sorted(glob.glob(os.path.join(d, pat)))
            if g:
                return [[float(x) for x in l.split(',')] for l in open(g[0]) if l.strip()]
        return []
    vol, fq, se = tab('006_VAR_DRESP_VAL_REPORT.tab'), tab('005_VAR_DRESP_VAL_REPORT.tab'), tab('008_VAR_DRESP_VAL_REPORT.tab')
    data = [[v[0], v[1], 0, 0] + f[1:7] + s[1:5] for v, f, s in zip(vol, fq, se)]
    print('(from Tosca report tables)')
print('cycle  volume(mm3)   f7     f8     f9     f10    f11    f12  | SE/cap LC1  LC2a  LC2b  LC3a | feasible')
for r in data:
    f = r[4:10]
    se = [v / c for v, c in zip(r[10:14], CAPS)]
    ok = min(f) >= 417.0 * 0.999 and max(se) <= 1.001
    print('%4d  %11.0f  %s | %s | %s' % (int(r[0]), r[1], ' '.join('%6.1f' % v for v in f),
                                       '  '.join('%5.2f' % v for v in se), 'yes' if ok else ''))
last = data[-1]
print('cycles: %d; volume %.0f -> %.0f mm3 (%.1f %%); last f7 %.1f Hz; last max SE/cap %.3f' % (
    len(data) - 1, data[0][1], last[1], 100.0 * (last[1] - data[0][1]) / data[0][1], min(last[4:10]),
    max(v / c for v, c in zip(last[10:14], CAPS))))
out = os.path.join(job, 'TOSCA.OUT')
if os.path.exists(out):
    tail = open(out, errors='replace').read().splitlines()[-6:]
    print('TOSCA.OUT tail:\n  ' + '\n  '.join(tail))
