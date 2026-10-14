# fig_th_figs.py - report figures from th_figs.npz (export_th_figs.py on nexus): mode shapes 7 to 12 of the final
# thresholded model, the mesh, and the set-up (tie and coupling surfaces, reference points). ASCII only.
# Usage: python3 fig_th_figs.py th_figs.npz th_figs_setup.txt <out dir>
#   -> su_th_modes.png, su_th_mesh.png, su_th_setup.png
import sys, os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import su_render as R

npz, setup, out = sys.argv[1], sys.argv[2], sys.argv[3]
Z = np.load(npz, allow_pickle=True)
X, F, U, fr = Z['X'].astype(float), Z['faces'], Z['U'].astype(float), Z['freqs']
T0 = X[F]
span = np.ptp(X, axis=0).max()

# modes: deformed surface coloured by the displacement magnitude (normalised per mode)
fig, axs = plt.subplots(2, 3, figsize=(18, 11))
for k, ax in enumerate(axs.ravel()):
    u = U[k]
    mag = np.linalg.norm(u, axis=1)
    s = 0.08 * span / max(mag.max(), 1e-12)
    Td = (X + s * u)[F]
    val = mag[F].mean(axis=1) / mag.max()
    R.draw(ax, Td, 'iso', values=val, cmap='viridis', vmin=0, vmax=1)
    pk = X[np.argmax(mag)]
    ax.set_title('Mode %d, %.1f Hz; largest motion at (%.0f, %.0f, %.0f) mm' % (k + 7, fr[k], pk[0], pk[1], pk[2]), fontsize=10)
fig.suptitle('Final thresholded model: elastic modes 7 to 12 (free-free), displacement magnitude normalised per mode, deformation exaggerated', fontsize=12)
plt.tight_layout()
plt.savefig(os.path.join(out, 'su_th_modes.png'), dpi=200)
plt.close()

# mesh: whole body and a zoom on one corner, triangle edges drawn
fig, axs = plt.subplots(1, 2, figsize=(18, 8))
R.draw(axs[0], T0, 'iso', edge=(0.15, 0.15, 0.15), lw=0.05)
axs[0].set_title('Solid body of the thresholded model, surface of the 1.0 mm tetrahedral mesh', fontsize=10)
c = T0.mean(axis=1)
m = (c[:, 0] > 15) & (c[:, 1] > 15)
if m.sum() < 100:
    m = (c[:, 0] > np.percentile(c[:, 0], 70))
R.draw(axs[1], T0[m], 'iso', edge=(0.1, 0.1, 0.1), lw=0.15)
axs[1].set_title('Zoom: +x+y corner (fin, arm root and arm)', fontsize=10)
cnt = Z['counts']
names = list(Z['part_names'])
txt = '; '.join('%s %d elements (%d solid)' % (names[int(r[0]) - 1], r[1], r[2]) for r in cnt)
fig.suptitle(txt, fontsize=9)
plt.tight_layout()
plt.savefig(os.path.join(out, 'su_th_mesh.png'), dpi=200)
plt.close()

# set-up: body in light grey, tie and coupling surfaces by type, reference points
GROUPS = [('motor seat couplings', ('MOT_SEAT',), '#d62728'), ('joint ties (fin and prong bosses, joint faces)', ('JNT', 'PRONG_BOSS', 'FIN_BOSS'), '#1f77b4'),
          ('lid seat tie', ('RIM_UNDER_LID', 'LID_BOTTOM'), '#2ca02c'), ('battery seat coupling', ('BATT_SEAT',), '#ff7f0e'),
          ('FC, GPS and antenna seat couplings', ('FC_SEAT', 'GPS_SEAT', 'ANT_PAD'), '#9467bd')]
fig, axs = plt.subplots(1, 2, figsize=(18, 8))
for ax, view in zip(axs, ('iso', 'below')):
    R.draw(ax, T0, view, color=(0.85, 0.85, 0.87), alpha=1.0)
    for lab, keys, col in GROUPS:
        pts = [p for nm, p in zip(Z['surf_names'], Z['surf_xyz']) if any(k in str(nm).upper() for k in keys)]
        if pts:
            P = R.project(np.vstack(pts).astype(float), view)
            ax.scatter(P[:, 0], P[:, 1], s=0.3, c=col, label=lab, rasterized=True)
    if len(Z['rp_xyz']):
        P = R.project(Z['rp_xyz'], view)
        ax.scatter(P[:, 0], P[:, 1], s=40, marker='x', c='k', label='reference points')
        xl, yl = ax.get_xlim(), ax.get_ylim()
        ax.set_xlim(min(xl[0], P[:, 0].min() - 3), max(xl[1], P[:, 0].max() + 3))
        ax.set_ylim(min(yl[0], P[:, 1].min() - 3), max(yl[1], P[:, 1].max() + 3))
    ax.set_title('view: %s' % view, fontsize=10)
axs[0].legend(markerscale=12, fontsize=9, loc='lower left')
fig.suptitle('Tie and coupling surfaces (nodes, drawn without hidden-point removal) and reference points of the thresholded model', fontsize=11)
plt.tight_layout()
plt.savefig(os.path.join(out, 'su_th_setup.png'), dpi=200)
plt.close()
print('written su_th_modes.png, su_th_mesh.png, su_th_setup.png in', out)
