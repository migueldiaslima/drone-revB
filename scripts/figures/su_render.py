# su_render.py - shaded triangle-mesh views for the report figures (set-up chat): orthographic projection,
# painter's algorithm (triangles sorted far to near), Lambert shading with one light, optional scalar colouring.
# Used by fig_th_modes.py, fig_th_setup.py and fig_iso_snapshots.py. ASCII only.
import struct
import numpy as np
from matplotlib.collections import PolyCollection
import matplotlib.cm as cm
import matplotlib.colors as mcolors

VIEWS = {'iso': (-35.0, 30.0), 'iso_rear': (145.0, 25.0), 'top': (-90.0, 90.0), 'side': (-90.0, 0.0),
         'front': (0.0, 0.0), 'below': (-35.0, -35.0)}


def read_stl(fn):
    d = open(fn, 'rb').read()
    n = struct.unpack('<I', d[80:84])[0]
    return np.frombuffer(d[84:84 + 50 * n], dtype=[('n', '<f4', 3), ('v', '<f4', (3, 3)), ('a', '<u2')])['v'].astype(float)


def basis(az, el):
    a, e = np.radians(az), np.radians(el)
    d = np.array([np.cos(e) * np.cos(a), np.cos(e) * np.sin(a), np.sin(e)])      # towards the viewer
    up = np.array([0.0, 0.0, 1.0]) if abs(el) < 89.0 else np.array([-np.sin(a), np.cos(a), 0.0])
    r = np.cross(up, d)
    r /= np.linalg.norm(r)
    u = np.cross(d, r)
    return r, u, d


def draw(ax, T, view='iso', values=None, cmap='viridis', vmin=None, vmax=None, color=(0.55, 0.57, 0.6),
         edge=None, lw=0.0, alpha=1.0, light=(0.4, -0.5, 0.75)):
    """T: (n, 3, 3) triangles; values: per-triangle scalars (or None for a plain colour). Returns the mappable."""
    az, el = VIEWS[view] if isinstance(view, str) else view
    r, u, d = basis(az, el)
    P = np.stack([T @ r, T @ u], axis=-1)
    depth = (T @ d).mean(axis=1)
    n = np.cross(T[:, 1] - T[:, 0], T[:, 2] - T[:, 0])
    n /= np.maximum(np.linalg.norm(n, axis=1)[:, None], 1e-12)
    L = np.asarray(light, dtype=float)
    L /= np.linalg.norm(L)
    shade = 0.35 + 0.65 * np.abs(n @ L)
    o = np.argsort(depth)
    sm = None
    if values is None:
        rgb = np.clip(np.asarray(color)[None, :] * shade[:, None], 0, 1)
    else:
        norm = mcolors.Normalize(vmin=np.min(values) if vmin is None else vmin, vmax=np.max(values) if vmax is None else vmax)
        sm = cm.ScalarMappable(norm=norm, cmap=cmap)
        rgb = sm.to_rgba(values)[:, :3] * (0.55 + 0.45 * shade[:, None])
    fc = np.c_[np.clip(rgb, 0, 1), np.full(len(rgb), alpha)]
    pc = PolyCollection(P[o], facecolors=fc[o], edgecolors=(edge if edge is not None else 'face'), linewidths=lw)
    ax.add_collection(pc)
    ax.set_xlim(P[..., 0].min(), P[..., 0].max())
    ax.set_ylim(P[..., 1].min(), P[..., 1].max())
    ax.set_aspect('equal')
    ax.axis('off')
    return sm, (r, u, d)


def project(xyz, view):
    az, el = VIEWS[view] if isinstance(view, str) else view
    r, u, d = basis(az, el)
    return np.c_[xyz @ r, xyz @ u]
