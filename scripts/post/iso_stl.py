# iso_stl.py - writes the raw iso surface of a Tosca cycle as binary STL (elements with density >= iso,
# fixed regions included) and counts the connected pieces. No smoothing: a quick look and a
# connectivity check, not the print file. Run on nexus:
#   abaqus python iso_stl.py <saved cycle odb> 0.3 0.5
from __future__ import print_function
import sys, struct
import numpy as np
from odbAccess import openOdb

args = sys.argv[1:]
path = [a for a in args if a.lower().endswith('.odb')][0]
isos = [float(a) for a in args if not a.lower().endswith('.odb') and a.replace('.', '', 1).isdigit()] or [0.3, 0.5]
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
fr = st.frames[0]
key = [k for k in fr.fieldOutputs.keys() if 'MAT_PROP_NORMALIZED' in k.upper()][0]
dens = {}
for b in fr.fieldOutputs[key].bulkDataBlocks:
    iname = b.instance.name if b.instance is not None else ''
    d = np.asarray(b.data).reshape(len(b.elementLabels), -1)[:, 0]
    for l, v in zip(np.asarray(b.elementLabels).tolist(), d.tolist()):
        dens[(iname, l)] = max(v, dens.get((iname, l), -1.0))
# corner faces of a C3D10 (first 4 nodes), outward order not needed for a viewer
TF = ((0, 2, 1), (0, 1, 3), (1, 2, 3), (0, 3, 2))
xyz = {}
for iname in ra.instances.keys():
    for nd in ra.instances[iname].nodes:
        xyz[(iname, nd.label)] = nd.coordinates
tag = path.rsplit('_', 1)[-1].replace('.odb', '')
for iso in isos:
    faces = {}
    parent = {}
    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a
    nel = 0
    for iname in ra.instances.keys():
        inst = ra.instances[iname]
        for e in inst.elements:
            if not e.type.startswith('C3D'):
                continue
            if keep is not None and (iname, e.label) not in keep:
                continue
            if dens.get((iname, e.label), 1.0) < iso:
                continue
            nel += 1
            c = [(iname, n) for n in e.connectivity[:4]]
            for n in c:
                parent.setdefault(n, n)
            r0 = find(c[0])
            for n in c[1:]:
                r = find(n)
                if r != r0:
                    parent[r] = r0
            for f in TF:
                k = tuple(sorted((c[f[0]], c[f[1]], c[f[2]])))
                if k in faces:
                    del faces[k]
                else:
                    faces[k] = (c[f[0]], c[f[1]], c[f[2]])
    roots = {}
    for n in parent:
        r = find(n)
        roots[r] = roots.get(r, 0) + 1
    sizes = sorted(roots.values(), reverse=True)
    fn = 'iso_%s%s_%03d.stl' % (tag, ('_' + PART) if PART else '', int(round(iso * 100)))
    with open(fn, 'wb') as f:
        f.write(b'iso surface'.ljust(80, b' '))
        f.write(struct.pack('<I', len(faces)))
        for tri in faces.values():
            p = [np.asarray(xyz[n], dtype=float) for n in tri]
            nrm = np.cross(p[1] - p[0], p[2] - p[0])
            ln = np.linalg.norm(nrm)
            nrm = nrm / ln if ln > 0 else nrm
            f.write(struct.pack('<12fH', *(list(nrm) + list(p[0]) + list(p[1]) + list(p[2]) + [0])))
    print('iso %.1f: %d elements kept, %d surface triangles -> %s; connected pieces: %d (node counts of the largest: %s)' % (
        iso, nel, len(faces), fn, len(sizes), sizes[:6]))
o.close()
