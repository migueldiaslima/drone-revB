# restore_r4.py - v04-B rev 4 print set (D-044, D-087; build log item 59): restoration of the H4 rev 4 cycle 28
# iso 0.4 surfaces with the exact non-design geometry, per part, plus T-5 and T-7 reports.
#   result = ((iso - KEEL_ZONE_BOX) U fixed U keels) n (envelope U keels)        (TUB)
#   result = (iso U fixed) n envelope                                             (LID, ARM_pp)
# iso: marching-tet STL from iso_mt.py, 6 Taubin iterations here (T-3); fixed and envelope: the part STEP meshed
# with gmsh (each solid closed, design cells recognised by volume), keels from geometry/v04B_r4_keels (STEP).
# Needs python3 with numpy, manifold3d, gmsh. Run on nexus (see the README at the end of the build log item):
#   python3 restore_r4.py <iso dir> <geometry dir> <out dir>
# ASCII only. Stops with a clear message if any volume table does not match.
from __future__ import print_function
import os, sys, struct, json
import numpy as np
import gmsh
from manifold3d import Manifold, Mesh

ISO_DIR, GEO_DIR, OUT = (sys.argv[1:4] + [None, None, None])[:3]
if not OUT:
    raise SystemExit('usage: python3 restore_r4.py <iso dir> <geometry dir (repo geometry/)> <out dir>')
os.makedirs(OUT, exist_ok=True)
RHO = 1.30e-3                                   # g/mm^3 PET-CF
ZONE = (-54.0, -23.0, -9.0, 9.0, 0.0, 21.5)      # D-087 clean keel zone
H = float(os.environ.get('RESTORE_H', '0.3'))    # gmsh surface size of the exact geometry (mm), item 22: 0.3
PARTS = {
    'TUB': dict(iso='mt_c28_TUB_040.stl', step='v04B_r4/TUB.step', design=[39538.45], vexp=(39538.45, 12796.26),
                keels=['v04B_r4_keels/KEEL_A_r4.step', 'v04B_r4_keels/KEEL_B_r4.step'], zone=True),
    'LID': dict(iso='mt_c28_LID_040.stl', step='v04B_r4/LID.step', design=[1139.11, 1217.86], vexp=(2356.98, 3417.08),
                keels=[], zone=False),
    'ARM_pp': dict(iso='mt_c28_ARMS_040.stl', step='v04B_r4/ARM_pp.step', design=[8036.91], vexp=(8036.91, 2933.50),
                   keels=[], zone=False, quadrant=(1, 1)),
}
report = {}


def stop(msg):
    raise SystemExit('RESTORE STOPPED: ' + msg)


def vol(m):
    return m.volume() if hasattr(m, 'volume') else m.get_volume()


def to_manifold(V, F, label):
    mesh = Mesh(vert_properties=np.ascontiguousarray(V, dtype=np.float32), tri_verts=np.ascontiguousarray(F, dtype=np.uint32))
    m = Manifold(mesh)
    st = str(m.status())
    if 'NoError' not in st:
        try:
            mesh.merge()
            m = Manifold(mesh)
            st = str(m.status())
        except Exception:
            pass
    if 'NoError' not in st:
        stop('%s is not a valid closed manifold (%s)' % (label, st))
    return m


def weld(T, tol=1e-5):
    P = T.reshape(-1, 3)
    key = np.round(P / tol).astype(np.int64)
    _, idx, inv = np.unique(key, axis=0, return_index=True, return_inverse=True)
    F = inv.reshape(-1, 3)
    F = F[(F[:, 0] != F[:, 1]) & (F[:, 1] != F[:, 2]) & (F[:, 0] != F[:, 2])]
    return P[idx].astype(float), F


def read_stl(fn):
    d = open(fn, 'rb').read()
    n = struct.unpack('<I', d[80:84])[0]
    return np.frombuffer(d[84:84 + 50 * n], dtype=[('n', '<f4', 3), ('v', '<f4', (3, 3)), ('a', '<u2')])['v'].astype(float)


def write_stl(fn, m):
    me = m.to_mesh()
    V = np.asarray(me.vert_properties)[:, :3].astype(float)
    F = np.asarray(me.tri_verts).astype(np.int64)
    T = V[F]
    n = np.cross(T[:, 1] - T[:, 0], T[:, 2] - T[:, 0])
    n /= np.maximum(np.linalg.norm(n, axis=1)[:, None], 1e-12)
    rec = np.zeros(len(T), dtype=[('n', '<f4', 3), ('v', '<f4', (3, 3)), ('a', '<u2')])
    rec['n'] = n
    rec['v'] = T
    with open(fn, 'wb') as f:
        f.write(b'restore_r4 print set'.ljust(80, b' '))
        f.write(struct.pack('<I', len(T)))
        f.write(rec.tobytes())
    return len(T)


def taubin(V, F, it=6, lam=0.5, mu=-0.53):
    E = np.vstack([F[:, [0, 1]], F[:, [1, 2]], F[:, [2, 0]]])
    E = np.unique(np.sort(E, axis=1), axis=0)
    deg = np.bincount(E.ravel(), minlength=len(V)).astype(float)
    for _ in range(it):
        for f in (lam, mu):
            S = np.zeros_like(V)
            np.add.at(S, E[:, 0], V[E[:, 1]])
            np.add.at(S, E[:, 1], V[E[:, 0]])
            V = V + f * (S / np.maximum(deg, 1)[:, None] - V)
    return V


def step_solids(fn, h):
    """mesh every solid of a STEP file (fragmented, so shared faces are conformal); returns [(volume, V, F)]"""
    gmsh.initialize()
    gmsh.option.setNumber('General.Terminal', 0)
    gmsh.model.add('m')
    gmsh.model.occ.importShapes(fn)
    gmsh.model.occ.synchronize()
    ents = gmsh.model.getEntities(3)
    if len(ents) > 1:
        gmsh.model.occ.fragment(ents[:1], ents[1:])
        gmsh.model.occ.synchronize()
    gmsh.option.setNumber('Mesh.MeshSizeMax', h)
    gmsh.option.setNumber('Mesh.MeshSizeMin', h / 6.0)
    gmsh.option.setNumber('Mesh.MeshSizeFromCurvature', 16)
    gmsh.model.mesh.generate(2)
    tags, xyz, _ = gmsh.model.mesh.getNodes()
    X = np.zeros((int(tags.max()) + 1, 3))
    X[tags.astype(int)] = xyz.reshape(-1, 3)
    out = []
    for dim, v in gmsh.model.getEntities(3):
        tris = []
        for sd, s in gmsh.model.getBoundary([(3, v)], oriented=True, recursive=False):
            et, _, nt = gmsh.model.mesh.getElements(2, abs(s))
            for t, n in zip(et, nt):
                if t != 2:
                    continue
                f = np.asarray(n, dtype=np.int64).reshape(-1, 3)
                tris.append(f[:, ::-1] if s < 0 else f)
        F = np.vstack(tris)
        used, Fi = np.unique(F, return_inverse=True)
        V = X[used]
        Fi = Fi.reshape(-1, 3)
        sv = np.einsum('ij,ij->i', V[Fi[:, 0]], np.cross(V[Fi[:, 1]], V[Fi[:, 2]])).sum() / 6.0
        if sv < 0:
            Fi = Fi[:, ::-1]
        out.append((gmsh.model.occ.getMass(3, v), V, Fi))
    gmsh.finalize()
    return out


def union(ms):
    r = ms[0]
    for m in ms[1:]:
        r = r + m
    return r


for name, P in PARTS.items():
    print('=' * 20, name)
    rep = {}
    # exact geometry
    sol = step_solids(os.path.join(GEO_DIR, P['step']), H)
    vols = sorted(round(v, 2) for v, _, _ in sol)
    print('%s solids: %d, volumes %s' % (P['step'], len(sol), vols if len(vols) < 12 else vols[:6] + ['...'] + vols[-3:]))
    des, fix = [], []
    for v, V, F in sol:
        isdes = any(abs(v - d) < 0.5 for d in P['design'])
        (des if isdes else fix).append(to_manifold(V, F, '%s solid %.2f' % (name, v)))
    vd = sum(vol(m) for m in des)
    vf = sum(vol(m) for m in fix)
    print('design %.2f (expected %.2f), fixed %.2f (expected %.2f) mm^3' % (vd, P['vexp'][0], vf, P['vexp'][1]))
    if abs(vd - P['vexp'][0]) > 0.005 * P['vexp'][0] or abs(vf - P['vexp'][1]) > 0.005 * P['vexp'][1]:
        stop('%s design / fixed volumes do not match the export (mesh at h %.2f)' % (name, H))
    keels = []
    for k in P['keels']:
        ks = step_solids(os.path.join(GEO_DIR, k), H)
        for v, V, F in ks:
            keels.append(to_manifold(V, F, '%s %.1f' % (k, v)))
        print('%s: %d solids, %.1f mm^3' % (k, len(ks), sum(v for v, _, _ in ks)))
    fixed = union(fix + keels) if (fix + keels) else None
    env = union(des + fix + keels)
    # iso surface
    T = read_stl(os.path.join(ISO_DIR, P['iso']))
    if 'quadrant' in P:
        c = T.mean(axis=1)
        sx, sy = P['quadrant']
        T = T[(sx * c[:, 0] > 0) & (sy * c[:, 1] > 0)]
    V, F = weld(T)
    V = taubin(V, F)
    iso = to_manifold(V, F, '%s iso surface' % name)
    v_iso = vol(iso)
    print('iso 0.4 (6 Taubin iterations): %.1f mm^3, %d pieces' % (v_iso, len(iso.decompose())))
    base = iso
    if P['zone']:
        x0, x1, y0, y1, z0, z1 = ZONE
        box = Manifold.cube((x1 - x0, y1 - y0, z1 - z0)).translate((x0, y0, z0))
        base = iso - box
        print('keel zone cleaned: %.1f mm^3 removed (fixed solids and keels added back below)' % (v_iso - vol(base)))
    kept = base ^ env
    if vol(base) - vol(kept) > 0.2 * vol(base):
        stop('%s: %.0f of %.0f mm^3 of the iso surface lie outside the envelope: STEP and iso not in the same position?' % (
            name, vol(base) - vol(kept), vol(base)))
    res = (base + fixed) ^ env if fixed is not None else kept
    v_res = vol(res)
    pieces = res.decompose()
    rep.update(iso=round(v_iso, 1), after_zone=round(vol(base), 1), trimmed=round(vol(base) - vol(kept), 1),
               restored=round(v_res - vol(kept), 1), result=round(v_res, 1), mass_g=round(v_res * RHO, 2),
               pieces=[round(vol(p), 2) for p in sorted(pieces, key=lambda p: -vol(p))][:5])
    print('trimmed outside the envelope %.1f, fixed restored %.1f mm^3' % (rep['trimmed'], rep['restored']))
    print('RESULT %s: %.1f mm^3 = %.2f g, %d piece(s) %s  -> T-5 %s' % (name, v_res, v_res * RHO, len(pieces), rep['pieces'],
          'PASS' if len(pieces) == 1 else 'CHECK (more than one piece)'))
    nt = write_stl(os.path.join(OUT, 'restored_%s_r4_c28_iso040.stl' % name), res)
    print('written restored_%s_r4_c28_iso040.stl (%d triangles)' % (name, nt))
    rep['manifold'] = res
    report[name] = rep

# T-7: keep-outs and parts against each other
print('=' * 20, 'T-7')
ko = step_solids(os.path.join(GEO_DIR, 'v04B_r4/KEEPOUTS_v04B.step'), H)
t7 = []
for i, (v, V, F) in enumerate(ko):
    k = to_manifold(V, F, 'keep-out %d' % i)
    for name in report:
        ov = vol(report[name]['manifold'] ^ k)
        t7.append((name, i, round(v, 2), round(ov, 3)))
        if ov > 0.05:
            print('  %s in keep-out solid %d (%.2f mm^3): overlap %.3f mm^3' % (name, i, v, ov))
names = list(report)
for a in range(len(names)):
    for b in range(a + 1, len(names)):
        ov = vol(report[names[a]]['manifold'] ^ report[names[b]]['manifold'])
        print('  %s with %s: overlap %.3f mm^3' % (names[a], names[b], ov))
        t7.append((names[a], names[b], None, round(ov, 3)))
bad = [r for r in t7 if r[3] > 1.0]
print('T-7: %d keep-out solids x %d parts checked; overlaps above 1 mm^3 (meshing noise of coincident faces is below that): %d -> %s' % (len(ko), len(report), len(bad), 'PASS' if not bad else 'CHECK'))
for name in report:
    report[name].pop('manifold')
json.dump(dict(parts=report, t7=t7, h=H, zone=ZONE), open(os.path.join(OUT, 'restore_r4.json'), 'w'), indent=1)
tot = report['TUB']['mass_g'] + report['LID']['mass_g'] + 4 * report['ARM_pp']['mass_g']
print('frame mass (TUB + LID + 4 x ARM_pp): %.2f g' % tot)
