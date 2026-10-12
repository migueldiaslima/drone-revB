# iso_mt.py - iso surface of a Tosca cycle by marching tetrahedra on nodal densities (element
# density averaged to the corner nodes), the same principle as Tosca's smoothing: surfaces follow the
# iso level through the elements instead of the jagged element faces. Domain boundary faces are kept
# where the nodal density is above the iso level and clipped where it crosses. Writes binary STL.
# Run on nexus:  abaqus python iso_mt.py <saved cycle odb> 0.3 0.5
from __future__ import print_function
import sys, struct
import numpy as np
from odbAccess import openOdb

args = sys.argv[1:]
path = [a for a in args if a.lower().endswith('.odb')][0]
isos = [float(a) for a in args if not a.lower().endswith('.odb') and a.replace('.', '', 1).isdigit()] or [0.5]
o = openOdb(path, readOnly=True)
ra = o.rootAssembly

# part filter (build log item 47): words TUB, LID or ARMS keep only that part (element sets of the flattened
# Tosca odb: <PART>-1_ALL_<PART>, ARM_xx-1_ALL_ARM); word KEEL also writes a crop around the keel lid boss.
WORDS = [a.lstrip('-').upper() for a in args]
PART = [w for w in WORDS if w in ('TUB', 'LID', 'ARMS')]
PART = PART[0] if PART else ''
KEEL = 'KEEL' in WORDS
KEEL_BOX = ((-42.0, -12.0, 4.0), (-18.0, 12.0, 24.0))     # boss 5 at (-30, 0), top z 21.5
keep = None
if PART:
    keep = set()
    for iname in ra.instances.keys():
        es = ra.instances[iname].elementSets
        want = 'ARM' if PART == 'ARMS' else PART
        ks = [k for k in es.keys() if k.upper().endswith('_ALL_' + want) or k.upper() == 'ALL_' + want]
        for k in ks:
            keep.update((iname, e.label) for e in es[k].elements)
        print('part %s: element sets %s' % (PART, ', '.join(ks[:6])))
    print('part %s: %d elements' % (PART, len(keep)))
    if not keep:
        raise SystemExit('no elements found for part %s' % PART)
st = o.steps['FREQ']
fr = [f for f in st.frames if any('MAT_PROP_NORMALIZED' in k.upper() for k in f.fieldOutputs.keys())][-1]
key = [k for k in fr.fieldOutputs.keys() if 'MAT_PROP_NORMALIZED' in k.upper()][0]
dens = {}
for b in fr.fieldOutputs[key].bulkDataBlocks:
    iname = b.instance.name if b.instance is not None else ''
    d = np.asarray(b.data).reshape(len(b.elementLabels), -1)[:, 0]
    for l, v in zip(np.asarray(b.elementLabels).tolist(), d.tolist()):
        dens[(iname, l)] = max(v, dens.get((iname, l), -1.0))

# global node index and tets (corner nodes)
gid = {}
X = []
T = []
D = []
for iname in ra.instances.keys():
    inst = ra.instances[iname]
    for nd in inst.nodes:
        gid[(iname, nd.label)] = len(X)
        X.append(nd.coordinates)
    for e in inst.elements:
        if not e.type.startswith('C3D'):
            continue
        if keep is not None and (iname, e.label) not in keep:
            continue
        T.append([gid[(iname, n)] for n in e.connectivity[:4]])
        D.append(dens.get((iname, e.label), 1.0))
o.close()
X = np.asarray(X, dtype=float)
T = np.asarray(T, dtype=np.int64)
D = np.asarray(D, dtype=float)
# nodal density = mean of the attached elements
s = np.zeros(len(X)); c = np.zeros(len(X))
for j in range(4):
    np.add.at(s, T[:, j], D)
    np.add.at(c, T[:, j], 1.0)
V = np.where(c > 0, s / np.maximum(c, 1), 0.0)
print('tets %d, nodes %d' % (len(T), len(X)))

# boundary faces of the whole mesh (used by one tet only)
FI = np.array([[0, 2, 1], [0, 1, 3], [1, 2, 3], [0, 3, 2]])
F = T[:, FI].reshape(-1, 3)
Fs = np.sort(F, axis=1)
_, inv, cnt = np.unique(Fs, axis=0, return_inverse=True, return_counts=True)
BF = F[cnt[inv.ravel()] == 1]

def interp(a, b, iso):
    sw = a > b                         # canonical edge direction so shared points are bit-identical
    a, b = np.where(sw, b, a), np.where(sw, a, b)
    va, vb = V[a], V[b]
    t = ((iso - va) / np.where(np.abs(vb - va) < 1e-12, 1e-12, vb - va))[:, None]
    return X[a] + t * (X[b] - X[a])

EDGES = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]

def orient(tris, hi_pts):
    n = np.cross(tris[:, 1] - tris[:, 0], tris[:, 2] - tris[:, 0])
    cen = tris.mean(axis=1)
    flip = np.einsum('ij,ij->i', n, hi_pts - cen) > 0   # normal must point away from solid
    tris[flip] = tris[flip][:, [0, 2, 1]]
    return tris

def write_stl(fn, tris):
    nrm = np.cross(tris[:, 1] - tris[:, 0], tris[:, 2] - tris[:, 0])
    ln = np.linalg.norm(nrm, axis=1)[:, None]
    nrm = nrm / np.where(ln > 0, ln, 1)
    rec = np.zeros(len(tris), dtype=[('n', '<f4', 3), ('v', '<f4', (3, 3)), ('a', '<u2')])
    rec['n'] = nrm; rec['v'] = tris
    with open(fn, 'wb') as f:
        f.write(b'iso surface marching tets'.ljust(80, b' '))
        f.write(struct.pack('<I', len(tris)))
        f.write(rec.tobytes())


for iso in isos:
    out = []
    vals = V[T]                       # (nt, 4)
    above = vals >= iso
    na = above.sum(axis=1)
    for k in (1, 2, 3):
        sel = np.where(na == k)[0]
        if len(sel) == 0:
            continue
        Ts = T[sel]
        A = above[sel]
        hi = (X[Ts] * A[:, :, None]).sum(axis=1) / k
        if k in (1, 3):
            # single vertex on its own side: triangle on its three edges
            lone = np.argmax(A if k == 1 else ~A, axis=1)
            others = np.array([[j for j in range(4) if j != i] for i in range(4)])[lone]
            L = Ts[np.arange(len(Ts)), lone]
            P = [interp(L, Ts[np.arange(len(Ts)), others[:, m]], iso) for m in range(3)]
            out.append(orient(np.stack(P, axis=1), hi))
        else:
            # two above, two below: quad split into two triangles
            ia = np.argsort(~A, axis=1, kind='stable')
            a0, a1, b0, b1 = [Ts[np.arange(len(Ts)), ia[:, m]] for m in range(4)]
            p1 = interp(a0, b0, iso); p2 = interp(a0, b1, iso)
            p3 = interp(a1, b1, iso); p4 = interp(a1, b0, iso)
            out.append(orient(np.stack([p1, p2, p3], axis=1), hi))
            out.append(orient(np.stack([p1, p3, p4], axis=1), hi))
    # boundary caps
    bv = V[BF] >= iso
    nb = bv.sum(axis=1)
    full = BF[nb == 3]
    out.append(X[full])               # outward order from the tet face definition
    part = np.where((nb == 1) | (nb == 2))[0]
    caps = []
    for i in part:
        f = BF[i]
        poly = []
        for j in range(3):
            a, b = f[j], f[(j + 1) % 3]
            if V[a] >= iso:
                poly.append(X[a])
            if (V[a] >= iso) != (V[b] >= iso):
                poly.append(interp(np.array([a]), np.array([b]), iso)[0])
        for j in range(1, len(poly) - 1):
            caps.append([poly[0], poly[j], poly[j + 1]])
    if caps:
        out.append(np.asarray(caps))
    tris = np.concatenate(out, axis=0)
    tag = path.rsplit('/', 1)[-1].replace('.odb', '')
    fn = 'mt_%s%s_%03d.stl' % (tag, ('_' + PART) if PART else '', int(round(iso * 100)))
    sets = [(fn, tris)]
    if KEEL:
        cen = tris.mean(axis=1)
        inb = np.all((cen >= KEEL_BOX[0]) & (cen <= KEEL_BOX[1]), axis=1)
        sets.append((fn.replace('.stl', '_keel.stl'), tris[inb]))
    for fn, tris in sets:
        write_stl(fn, tris)
        print('iso %.2f: %d triangles -> %s' % (iso, len(tris), fn))

