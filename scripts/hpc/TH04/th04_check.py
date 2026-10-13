# th04_check.py - D-082 (b) report: TH04b (seat tie) and TH04a (five boss ties) against H4 cycle 31.
#   abaqus python ~/drone_revB/stage6/scripts/th04_check.py TH04b TH04a
from __future__ import print_function
import sys, os, re
from odbAccess import openOdb
CAPS = [0.2192642, 0.2036868, 0.1037085, 0.3987864]       # 2 x H4 cycle 0 ALLSE (N mm)
TOSCA = ('Tosca c31', None, [416.4, 417.1, 417.7, 418.6, 501.2, 504.5], [c * r / 2.0 for c, r in zip(CAPS, (1.59, 1.41, 1.63, 2.10))])
if os.environ.get('TH_REV', '') == 'r4':   # rev 4 H4 cycle 28 (build log item 50); caps from TOSCA.OUT cycle 0
    CAPS = [0.2191128, 0.2044869, 0.1041570, 0.4040888]
    TOSCA = ('Tosca c28', None, [416.7, 417.2, 418.4, 423.7, 461.7, 496.5], [c * r / 2.0 for c, r in zip(CAPS, (1.58, 1.40, 1.60, 2.02))])
rows = [TOSCA]
for job in [a for a in sys.argv[1:] if not a.endswith('.py')]:
    txt = open(job + '.dat', errors='replace').read() if os.path.exists(job + '.dat') else ''
    mm = re.findall(r'TOTAL MASS OF MODEL\s+([0-9.Ee+-]+)', txt)
    mass = float(mm[-1]) * 1e6 if mm else None
    o = openOdb(os.path.abspath(job + '.odb'), readOnly=True)
    st = o.steps['FREQ']
    fs, where = [], []
    for i in range(7, 13):
        fr = st.frames[i]
        fs.append(float(re.search(r'Freq\s*=\s*([0-9.Ee+-]+)', fr.description).group(1)))
        best, xyz = 0.0, None
        for v in fr.fieldOutputs['U'].values:
            if v.instance is not None and v.magnitude > best:
                best, xyz = v.magnitude, (v.instance.name, v.nodeLabel)
        c = o.rootAssembly.instances[xyz[0]].getNodeFromLabel(xyz[1]).coordinates
        where.append('(%.0f, %.0f, %.0f)' % (c[0], c[1], c[2]))
    se, rf = [], []
    ra = o.rootAssembly
    for sn in ('LC1', 'LC2a', 'LC2b', 'LC3a'):
        hr = [r for k, r in o.steps[sn].historyRegions.items() if k.startswith('Assembly')][0]
        d = hr.historyOutputs['ALLSE'].data
        se.append(d[len(d) - 1][1])
        fr = o.steps[sn].frames[len(o.steps[sn].frames) - 1]
        regs = [ra.nodeSets[k] for k in ra.nodeSets.keys() if 'RP_JNT' in k.upper()]
        for iname in ra.instances.keys():
            regs += [ra.instances[iname].nodeSets[k] for k in ra.instances[iname].nodeSets.keys() if 'RP_JNT' in k.upper()]
        mx = 0.0
        for reg in regs:
            for v in fr.fieldOutputs['RF'].getSubset(region=reg).values:
                mx = max(mx, max(abs(x) for x in v.data[:3]))
        rf.append(mx)
    o.close()
    rows.append((job, mass, fs, se))
    print('%s: peaks of modes 7 to 12 at %s' % (job, ', '.join(where)))
    print('%s: max support reaction per step %s N' % (job, ', '.join('%.1e' % r for r in rf)))
print('%-10s %8s | %s | %s' % ('model', 'mass g', '  f7     f8     f9    f10    f11    f12 (Hz)', 'SE/cap LC1  LC2a  LC2b  LC3a'))
for n, m, fs, se in rows:
    ok = min(fs) >= 417.0 and max(s / c for s, c in zip(se, CAPS)) <= 1.0
    print('%-10s %8s | %s | %s | %s' % (n, '%.1f' % m if m else '-', ' '.join('%6.1f' % f for f in fs),
          '  '.join('%5.2f' % (s / c) for s, c in zip(se, CAPS)), 'PASS' if ok else ('-' if m is None else 'FAIL')))
print('pass: modes 7 to 12 >= 417 Hz and SE/cap <= 1 (caps 2 x H4 cycle 0); hard minimum 290 Hz (D-035)')
