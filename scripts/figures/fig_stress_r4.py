# fig_stress_r4.py - Stage 7 figure (build log item 67): von Mises (centroid) of the solid elements of the
# thresholded model for one load case, from stress_th.py output stress_<job>_<step>.npz. Three projections;
# each point is an element, sorted so the highest values are drawn on top; tie / coupling elements grey.
# Usage: python3 fig_stress_r4.py stress_TH_r4b_i30_final_LC3a.npz [out.png]
import sys, numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
D = np.load(sys.argv[1])
out = sys.argv[2] if len(sys.argv) > 2 else sys.argv[1].replace('.npz', '_vm.png')
c, vm, ex = D['cen'], D['VM'], D['excl'].astype(bool)
LIM = 36.3
fig, ax = plt.subplots(1, 3, figsize=(21, 7))
for a, (i, j, lab) in zip(ax, [(0, 1, 'plan (x-y)'), (0, 2, 'side (x-z)'), (1, 2, 'front (y-z)')]):
    a.scatter(c[ex, i], c[ex, j], s=0.3, c='#bbbbbb', rasterized=True, label='tie / coupling (excluded)')
    o = np.argsort(vm[~ex])
    sc = a.scatter(c[~ex][o, i], c[~ex][o, j], s=0.6, c=vm[~ex][o], cmap='viridis', vmin=0, vmax=LIM, rasterized=True)
    a.set_aspect('equal'); a.grid(alpha=.3); a.set_title(lab); a.legend(markerscale=10, fontsize=8, loc='upper right')
cb = fig.colorbar(sc, ax=ax, shrink=0.8, extend='max'); cb.set_label('von Mises (MPa), scale to the limit 36.3 MPa')
fig.suptitle('%s: von Mises at the element centroids, solid elements, max %.1f MPa' % (sys.argv[1].split('/')[-1].replace('.npz', ''), vm[~ex].max()))
plt.savefig(out, dpi=80)
print('written', out)
