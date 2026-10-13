# g7_check.py - gate G7 on one reference job (brief section 11, export note section 4).
# Run in the G7 folder on nexus:   abaqus python ../scripts/g7_check.py G7a_ref
# Reports: mass (332.79 g +-0.1 %), modes 1 to 20 with a shape description (where the motion is),
# lid / GPS modes below 417 Hz, ALLSE / ALLWK and caps, support reactions, untied tie nodes,
# solver warnings. Last line: "G7 <job>: PASS" or "G7 <job>: FAIL (...)". ASCII only.
from __future__ import print_function
import sys, os, re, math
from odbAccess import openOdb

job = [x for x in sys.argv[1:] if not x.startswith('-') and '=' not in x and not x.replace('.', '', 1).isdigit()][-1]
MASS_EXP, FMIN = 332.79, 417.0
# expected mass: environment variable G7_MASS (abaqus python rewrites key=value arguments, item 48)
if os.environ.get('G7_MASS'):
    MASS_EXP = float(os.environ['G7_MASS'])
R2 = 1.0 / math.sqrt(2.0)
CORN = {'pp': (1, 1), 'pm': (1, -1), 'mp': (-1, 1), 'mm': (-1, -1)}
fails = []


def last(seq):
    return seq[len(seq) - 1]


print('=== G7 check: %s ===' % job)
txt = open(job + '.dat', errors='replace').read() if os.path.exists(job + '.dat') else ''
mm = re.search(r'TOTAL MASS OF MODEL\s+([0-9.Ee+-]+)', txt)
if mm:
    mass = float(mm.group(1)) * 1e6
    d = 100.0 * (mass - MASS_EXP) / MASS_EXP
    ok = abs(d) <= 0.1
    print('mass %.3f g (expected %.2f, %+.3f %%)  %s' % (mass, MASS_EXP, d, 'OK' if ok else 'FAIL'))
    if not ok:
        fails.append('mass')
else:
    print('mass: TOTAL MASS OF MODEL not found in .dat')
    fails.append('mass not found')
for pat in (r'NUMBER OF ELEMENTS IS\s+\d+', r'NUMBER OF NODES IS\s+\d+', r'TOTAL NUMBER OF VARIABLES IN THE MODEL\s+\d+'):
    for s in re.findall(pat, txt)[-1:]:
        print('  ' + ' '.join(s.split()))
msg = open(job + '.msg', errors='replace').read() if os.path.exists(job + '.msg') else ''
print('solver: numerical singularity warnings %d, zero pivots %d, wallclock %s' % (
    len(re.findall(r'NUMERICAL SINGULARITY', msg)), len(re.findall(r'ZERO PIVOT', msg)),
    (re.findall(r'WALLCLOCK TIME \(SEC\)\s*=\s*(\d+)', msg) or ['?'])[-1]))

o = openOdb(os.path.abspath(job + '.odb'), readOnly=True)
ra = o.rootAssembly


def rp_label(name):
    k = [s for s in ra.nodeSets.keys() if s.upper() == name.upper()]
    if not k:
        return None
    ns = ra.nodeSets[k[0]]
    for nodes in ns.nodes:
        for n in nodes:
            return (ns.instanceNames[0] if ns.instanceNames else None, n.label)
    return None


rps = {}
for n in ['BATT', 'GPS', 'FC', 'ANT'] + ['MOT_' + c for c in CORN] + ['JNT_' + c for c in CORN]:
    rps[n] = rp_label('SET_RP_' + n)

# ---------- modes ----------
st = o.steps['FREQ']
print('--- modes ---')
print('mode  f (Hz)   peak |U| at (instance, x, y, z)        share |U|^2 TUB / LID / ARMS   battery / GPS   shape')
for i in range(1, min(21, len(st.frames))):
    fr = st.frames[i]
    f = float(re.search(r'Freq\s*=\s*([0-9.Ee+-]+)', fr.description).group(1))
    if i <= 6:
        if f > 1.0:
            fails.append('rigid mode %d at %.2f Hz' % (i, f))
        print('%3d  %8.3f   rigid-body %s' % (i, f, 'ok' if f <= 1.0 else 'FAIL'))
        continue
    U = fr.fieldOutputs['U']
    sh = {'TUB-1': 0.0, 'LID-1': 0.0, 'ARMS': 0.0}
    peak, where = 0.0, None
    byrp = {}
    for v in U.values:
        u = v.data
        m2 = u[0] * u[0] + u[1] * u[1] + u[2] * u[2]
        iname = v.instance.name if v.instance is not None else None
        if iname is None:
            for k, lab in rps.items():
                if lab and lab[1] == v.nodeLabel:
                    byrp[k] = u
            continue
        key = 'ARMS' if iname.startswith('ARM') else iname
        if key in sh:
            sh[key] += m2
        if m2 > peak:
            peak, where = m2, (iname, v.nodeLabel)
    tot = sum(sh.values()) or 1.0
    xyz = o.rootAssembly.instances[where[0]].getNodeFromLabel(where[1]).coordinates
    um = math.sqrt(peak)
    bat = math.sqrt(sum(x * x for x in byrp['BATT'])) / um if 'BATT' in byrp else float('nan')
    gps = math.sqrt(sum(x * x for x in byrp['GPS'])) / um if 'GPS' in byrp else float('nan')
    # shape label
    if where[0] == 'LID-1':
        lab = 'LID: GPS deck' if xyz[0] < -30 else ('LID: front tab / plate front' if xyz[0] > 23 else 'LID: plate')
    elif where[0].startswith('ARM'):
        uz = dict((c, byrp['MOT_' + c][2]) for c in CORN if 'MOT_' + c in byrp)
        if len(uz) == 4:
            s = dict((c, 1 if uz[c] > 0 else -1) for c in uz)
            big = max(abs(x) for x in uz.values())
            inplane = big < 0.3 * um
            if inplane:
                lab = 'arms in plane'
            elif s['pp'] == s['pm'] == s['mp'] == s['mm']:
                lab = 'arms: umbrella'
            elif s['pp'] == s['mm'] and s['pm'] == s['mp']:
                lab = 'arms: saddle (pp+mm vs pm+mp)'
            elif s['pp'] == s['pm'] and s['mp'] == s['mm']:
                lab = 'arms: front vs rear'
            elif s['pp'] == s['mp'] and s['pm'] == s['mm']:
                lab = 'arms: left vs right'
            else:
                lab = 'arms: mixed'
        else:
            lab = 'arms'
    else:
        lab = 'TUB: GPS deck' if (xyz[0] < -32.4 and xyz[2] > 21.4) else ('TUB (keel)' if xyz[0] < -20 else 'TUB')   # rev 4: deck on the TUB
    if bat > 0.5:
        lab += ', battery moving'
    is_local = where[0] == 'LID-1' or sh['LID-1'] / tot > 0.5
    flag = ''
    if i <= 12 and f < FMIN:
        flag = '  << BELOW 417 Hz'
        fails.append('mode %d %.1f Hz (%s)' % (i, f, lab))
    elif i > 12 and f < FMIN:
        flag = '  << below 417 Hz outside the band'
        fails.append('mode %d %.1f Hz below 417 outside the band' % (i, f))
    print('%3d  %8.2f   %-7s (%6.1f, %6.1f, %6.1f)   %5.2f / %5.2f / %5.2f        %5.2f / %5.2f   %s%s%s' % (
        i, f, where[0], xyz[0], xyz[1], xyz[2], sh['TUB-1'] / tot, sh['LID-1'] / tot, sh['ARMS'] / tot,
        bat, gps, lab, ' [local lid mode]' if is_local else '', flag))

# ---------- static steps ----------
print('--- static steps ---')
for sn in ('LC1', 'LC2a', 'LC2b', 'LC3a'):
    s = o.steps[sn]
    hr = [r for k, r in s.historyRegions.items() if k.startswith('Assembly')][0]
    se = last(hr.historyOutputs['ALLSE'].data)[1]
    wk = last(hr.historyOutputs['ALLWK'].data)[1] if 'ALLWK' in hr.historyOutputs.keys() else float('nan')
    fr = last(s.frames)
    umax, w = 0.0, ''
    for v in fr.fieldOutputs['U'].values:
        if v.magnitude > umax:
            umax, w = v.magnitude, '%s.%d' % (v.instance.name if v.instance else 'RP', v.nodeLabel)
    mx, n = 0.0, 0
    for nm in ('SET_RP_JNT_PP', 'SET_RP_JNT_PM', 'SET_RP_JNT_MP'):
        key = [k for k in ra.nodeSets.keys() if k.upper() == nm]
        if key:
            for v in fr.fieldOutputs['RF'].getSubset(region=ra.nodeSets[key[0]]).values:
                n += 1
                mx = max(mx, max(abs(x) for x in v.data[:3]))
    ok = mx < 1e-6 and n == 3
    if not ok:
        fails.append('reactions ' + sn)
    print('%-5s ALLSE %.6g  ALLWK %.6g  cap 2 x ALLSE %.6g N mm | max |U| %.4g mm at %s | RF max %.2e N over %d nodes %s' % (
        sn, se, wk, 2 * se, umax, w, mx, n, 'ok' if ok else 'FAIL'))

# ---------- untied tie nodes ----------
key = [k for k in ra.nodeSets.keys() if k.upper() == 'WARNNODEMISSMAININTERSECT']
fin, lid, other = 0, 0, []
if key:
    ns = ra.nodeSets[key[0]]
    for iname, nodes in zip(ns.instanceNames, ns.nodes):
        for nd in nodes:
            x, y, z = nd.coordinates
            on_fin = False
            for c, (sx, sy) in CORN.items():
                s = (sx * x + sy * y) * R2
                t = (-sy * x + sx * y) * R2
                if s > 14 and abs(abs(t) - 5.0) < 0.01:
                    on_fin = True
            if on_fin:
                fin += 1
            elif abs(z - 21.5) < 1e-3:
                lid += 1
                other.append((iname, round(x, 2), round(y, 2)))
            else:
                other.append((iname, round(x, 2), round(y, 2), round(z, 2)))
print('untied secondary nodes: %d on the fin boss faces (joint, expected about 172 at 2.5 / 1.5), %d on the lid seat (expected 0), %d elsewhere%s' % (
    fin, lid, len(other) - lid, (': ' + str(other[:12])) if other else ''))
if lid or len(other) - lid:
    fails.append('untied lid / other nodes %d' % len(other))
o.close()
print('G7 %s: %s' % (job, 'PASS' if not fails else 'FAIL (' + '; '.join(fails) + ')'))
