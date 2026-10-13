# th04_build.py - D-082 (b): thresholded jobs of H4 cycle 31 at iso 0.4 with both lid connections.
#   TH04b: lid tied over the seat (TIE_LIDRIM, as optimised)
#   TH04a: lid tied at the five screw bosses only (TIE_LID_1..5, G7a)
# Elements with density >= 0.4: stiffness and mass factor 1; others: stiffness 1e-6, mass 1e-9 (air).
# Tosca-only keywords removed (SENSITIVITY, DESIGN RESPONSE blocks); Lanczos shift kept (DV-24).
# Run in /tmp/mdias_H4/TH:   abaqus python ~/drone_revB/stage6/scripts/th04_build.py c31.odb
from __future__ import print_function
import sys, re, os
import numpy as np
from odbAccess import openOdb

ISO = 0.4
odbp = [a for a in sys.argv[1:] if a.lower().endswith('.odb')][0]
NOISL = 'noislands' in sys.argv          # item 44: solid pieces not connected to the main frame -> air
SUF = '_ni' if NOISL else ''
TOL = 0.2                                    # mm, node proximity counted as a connection (ties), as th04_islands.py
MODEL = 'TO_v04B_H4-Job.inp'
R4 = os.environ.get('TH_REV', '') == 'r4'   # rev 4 (build log item 50): H4 r4 deck, seat tie only, jobs TH_r4b
if R4:
    MODEL = 'TO_v04B_r4_H4-Job.inp'
ISO = float(os.environ.get('TH_ISO', ISO))     # item 51: other iso levels, job suffix _iNN
ISUF = ('_i%02d' % int(round(ISO * 100))) if 'TH_ISO' in os.environ else ''
DIST = 'tosca_distribution.inp'
TAGX = os.environ.get('TH_TAG', '')          # item 52: job name suffix for box variants
# item 52: TH_BOXES = 'x0,x1,y0,y1,z0,z1,iso;...' : TUB elements whose corner-node centroid lies in a box use
# that box's iso level instead of ISO (iso 0 = forced solid). Prints the volume and mass added against ISO.
BOXES = []
for b in [t for t in os.environ.get('TH_BOXES', '').split(';') if t.strip()]:
    v = [float(x) for x in b.split(',')]
    if len(v) != 7:
        raise SystemExit('TH_BOXES entry needs 7 numbers: %s' % b)
    BOXES.append(v)

o = openOdb(odbp, readOnly=True)
st = o.steps['FREQ']
fr = [f for f in st.frames if any('MAT_PROP_NORMALIZED' in k.upper() for k in f.fieldOutputs.keys())][-1]
key = [k for k in fr.fieldOutputs.keys() if 'MAT_PROP_NORMALIZED' in k.upper()][0]
rho = {}
for b in fr.fieldOutputs[key].bulkDataBlocks:
    d = np.asarray(b.data).reshape(len(b.elementLabels), -1)[:, 0]
    for l, v in zip(np.asarray(b.elementLabels).tolist(), d.tolist()):
        rho[l] = max(v, rho.get(l, -1.0))
print('densities read: %d elements' % len(rho))

def find(par, i):
    while par[i] != i:
        par[i] = par[par[i]]
        i = par[i]
    return i

island = set()
if NOISL:
    insts = o.rootAssembly.instances
    nid, xyz, elab, econ = {}, [], [], []
    for iname in insts.keys():
        for n in insts[iname].nodes:
            nid[(iname, n.label)] = len(xyz)
            xyz.append(n.coordinates)
        for e in insts[iname].elements:
            if e.type.upper().startswith('C3D'):
                elab.append(e.label)
                econ.append([nid[(iname, c)] for c in e.connectivity])
    xyz = np.asarray(xyz, dtype=float)
    nel = len(elab)
    solid = [rho.get(l, 1.0) >= ISO for l in elab]
    par = list(range(nel))
    owner = {}
    for i in range(nel):
        if not solid[i]:
            continue
        for n in econ[i]:
            j = owner.get(n)
            if j is None:
                owner[n] = i
            else:
                ri, rj = find(par, i), find(par, j)
                if ri != rj:
                    par[ri] = rj
    cell = {}
    for n in owner:
        cell.setdefault(tuple((xyz[n] // TOL).astype(int).tolist()), []).append(n)
    for k, ns in cell.items():
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                for dz in (-1, 0, 1):
                    m = cell.get((k[0] + dx, k[1] + dy, k[2] + dz))
                    if not m:
                        continue
                    for n1 in ns:
                        for n2 in m:
                            if n2 <= n1:
                                continue
                            d = xyz[n1] - xyz[n2]
                            if d[0] * d[0] + d[1] * d[1] + d[2] * d[2] <= TOL * TOL:
                                ri, rj = find(par, owner[n1]), find(par, owner[n2])
                                if ri != rj:
                                    par[ri] = rj
    size = {}
    for i in range(nel):
        if solid[i]:
            r = find(par, i)
            size[r] = size.get(r, 0) + 1
    main = max(size, key=lambda r: size[r])
    comps = {}
    for i in range(nel):
        if solid[i]:
            r = find(par, i)
            if r != main:
                island.add(elab[i])
                comps.setdefault(r, []).append(i)
    print('islands: %d components, %d elements set to air (main frame %d elements)' % (len(comps), len(island), size[main]))
    for r, mem in sorted(comps.items(), key=lambda t: -len(t[1])):
        c = xyz[[econ[i][0] for i in mem]].mean(axis=0)
        print('  %6d elements, centroid about (%.1f, %.1f, %.1f)' % (len(mem), c[0], c[1], c[2]))
boxiso = {}
SHAPES = [t.strip() for t in os.environ.get('TH_SHAPES', '').split(',') if t.strip()]   # item 56: keels_r4 shapes forced solid
# item 57: TH_CLEAN = 'x0,x1,y0,y1,z0,z1' : every TUB DESIGN element whose corner-node centroid lies in the box is set to
# air (leftover optimiser material removed); TUB fixed elements are never touched; TH_SHAPES elements override (solid).
CLEAN = [float(v) for v in os.environ.get('TH_CLEAN', '').split(',') if v.strip()]
if CLEAN and len(CLEAN) != 6:
    raise SystemExit('TH_CLEAN needs 6 numbers x0,x1,y0,y1,z0,z1')
if SHAPES or CLEAN:
    inst = o.rootAssembly.instances[list(o.rootAssembly.instances.keys())[0]]
    tubk = [k for k in inst.elementSets.keys() if k.upper().endswith('ALL_TUB')]
    desk = [k for k in inst.elementSets.keys() if k.upper().endswith('DESIGN_TUB')]
    if not tubk or not desk:
        raise SystemExit('TUB element sets not found (ALL_TUB %s, DESIGN_TUB %s)' % (tubk, desk))
    tub = set(e.label for e in inst.elementSets[tubk[0]].elements)
    des_tub = set(e.label for e in inst.elementSets[desk[0]].elements)
    print('TUB: %d elements, %d design, %d fixed (sets %s, %s)' % (len(tub), len(des_tub), len(tub - des_tub), tubk[0], desk[0]))
    xyzn = dict((n.label, n.coordinates) for n in inst.nodes)
    labs, cen, vols = [], [], []
    for e in inst.elements:
        if e.label not in tub or not e.type.upper().startswith('C3D'):
            continue
        p = np.asarray([xyzn[c] for c in e.connectivity[:4]], dtype=float)
        labs.append(e.label)
        cen.append(p.mean(axis=0))
        vols.append(abs(np.dot(p[1] - p[0], np.cross(p[2] - p[0], p[3] - p[0]))) / 6.0)
    labs = np.asarray(labs)
    cen = np.asarray(cen)
    vols = np.asarray(vols)
    isdes = np.asarray([l in des_tub for l in labs.tolist()])
    r_el = np.asarray([rho.get(l, 1.0) for l in labs.tolist()])
    shp = np.zeros(len(labs), dtype=bool)
    if SHAPES:
        for d in [os.path.dirname(os.path.abspath(__file__)) if '__file__' in globals() else '', os.path.expanduser('~/drone_revB/stage6/scripts')]:
            if d and d not in sys.path:
                sys.path.insert(0, d)
        import keels_r4
        for sh in SHAPES:
            m = keels_r4.SHAPES[sh](cen[:, 0], cen[:, 1], cen[:, 2])
            shp |= m
            nf = int((m & ~isdes).sum())
            add = m & (r_el < ISO)
            print('shape %s: %d TUB elements (%d of them fixed), volume %.1f mm^3 = %.2f g; not solid at iso %.2f before: %.1f mm^3 = %.2f g' % (
                sh, int(m.sum()), nf, vols[m].sum(), vols[m].sum() * 1.30e-3, ISO, vols[add].sum(), vols[add].sum() * 1.30e-3))
    if CLEAN:
        x0, x1, y0, y1, z0, z1 = CLEAN
        inb = (cen[:, 0] >= x0) & (cen[:, 0] <= x1) & (cen[:, 1] >= y0) & (cen[:, 1] <= y1) & (cen[:, 2] >= z0) & (cen[:, 2] <= z1)
        cl = inb & isdes & ~shp
        for l in labs[cl].tolist():
            boxiso[l] = 2.0                      # never reached by a density: air
        was = cl & (r_el >= ISO)
        print('clean box %s: %d TUB elements inside (%d design, %d fixed kept, %d in shapes); leftover design material removed (solid at iso %.2f, outside the shapes): %d elements, %.1f mm^3 = %.2f g' % (
            CLEAN, int(inb.sum()), int((inb & isdes).sum()), int((inb & ~isdes).sum()), int((inb & shp).sum()), ISO, int(was.sum()), vols[was].sum(), vols[was].sum() * 1.30e-3))
    for l in labs[shp].tolist():
        boxiso[l] = 0.0                          # forced solid (overrides the clean box)
    # summary of the TUB after the overrides (elements in the TUB only)
    fin = np.asarray([r_el[i] >= boxiso.get(labs[i], ISO) for i in range(len(labs))])
    print('TUB solid after overrides: %d elements, %.1f mm^3 = %.2f g (before: %d elements, %.1f mm^3 = %.2f g)' % (
        int(fin.sum()), vols[fin].sum(), vols[fin].sum() * 1.30e-3, int((r_el >= ISO).sum()), vols[r_el >= ISO].sum(), vols[r_el >= ISO].sum() * 1.30e-3))
if BOXES:
    inst = o.rootAssembly.instances[list(o.rootAssembly.instances.keys())[0]]
    tubk = [k for k in inst.elementSets.keys() if k.upper().endswith('ALL_TUB')]
    if not tubk:
        raise SystemExit('TUB element set not found')
    tub = set(e.label for e in inst.elementSets[tubk[0]].elements)
    xyzn = dict((n.label, n.coordinates) for n in inst.nodes)
    added_v = 0.0
    nbox = 0
    for e in inst.elements:
        if e.label not in tub or not e.type.upper().startswith('C3D'):
            continue
        p = np.asarray([xyzn[c] for c in e.connectivity[:4]], dtype=float)
        c = p.mean(axis=0)
        for x0, x1, y0, y1, z0, z1, bi in BOXES:
            if x0 <= c[0] <= x1 and y0 <= c[1] <= y1 and z0 <= c[2] <= z1:
                boxiso[e.label] = bi
                nbox += 1
                r = rho.get(e.label, 1.0)
                if r >= bi and r < ISO:
                    added_v += abs(np.dot(p[1] - p[0], np.cross(p[2] - p[0], p[3] - p[0]))) / 6.0
                break
    print('boxes %s: %d TUB elements inside; volume added against iso %.2f: %.1f mm^3 = %.2f g (1.30e-3 g/mm^3)' % (
        BOXES, nbox, ISO, added_v, added_v * 1.30e-3))
o.close()

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
ndr, nsub = 0, 0
for ln in txt.splitlines():
    kw = ln.upper().replace(' ', '')
    if kw.startswith('*DESIGNRESPONSE'):
        skip = True
        ndr += 1
        continue
    # suboptions of *DESIGN RESPONSE (H4 deck: *GLOBALRESPONSE; also *ELEMENTRESPONSE, *NODERESPONSE)
    if skip and ln.startswith('*') and not ln.startswith('**'):
        if kw.split(',')[0].endswith('RESPONSE'):
            nsub += 1
            continue
        skip = False
    if not skip:
        out.append(ln)
lines = out
print('removed: %d DESIGN RESPONSE blocks, %d response suboptions' % (ndr, nsub))
left = [ln for ln in lines if ln.startswith('*') and not ln.startswith('**')
        and ln.upper().replace(' ', '').split(',')[0].endswith('RESPONSE')]
if left:
    raise SystemExit('response keywords still in the deck: %s' % left[:3])
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
variants = {'TH_r4b' + ISUF + TAGX: base} if R4 else {'TH04b': base, 'TH04a': base.replace(m.group(0), five)}   # r4: no lid pads (DV-26)
print('TH04a ties:\n' + five)

dname = ('dist_TH_r4%s%s%s.inp' % (ISUF, TAGX, SUF)) if R4 else ('dist_TH04%s.inp' % SUF)
nsol = 0
with open(dname, 'w') as f:
    for k, lo in (('S', 1e-6), ('M', 1e-9)):
        f.write('\n'.join(head[k]) + '\n')
        for l in sorted(tab[k]):
            solid = rho.get(l, 1.0) >= boxiso.get(l, ISO) and l not in island
            if k == 'S' and solid:
                nsol += 1
            f.write('%d, %.6e, %.6e\n' % (l, 1.0 if solid else lo, tab[k][l][1]))
for tag0, t in variants.items():
    tag = tag0 + SUF
    t2 = re.sub(r'^(\*Include, input=)' + re.escape(DIST), r'\g<1>' + dname, t, flags=re.M | re.I)
    open(tag + '.inp', 'w').write(t2)
    print('%s.inp written (%d ties named TIE_LID)' % (tag, len(re.findall(r'name=TIE_LID', t2, flags=re.I))))
print('iso %.1f: %d of %d design elements solid' % (ISO, nsol, len(tab['S'])))
