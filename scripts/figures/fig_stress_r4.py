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
title = sys.argv[1].split('/')[-1].replace('.npz', '')
title = title[title.find('stress_'):] if 'stress_' in title else title
fig, axs = plt.subplots(2, 3, figsize=(21, 12))
o = np.argsort(vm[~ex])
for row, vmax, lab in ((0, LIM, 'scale 0 to the limit 36.3 MPa'), (1, float(np.percentile(vm[~ex], 99.9)), 'scale 0 to the 99.9th percentile')):
    for a, (i, j, pl) in zip(axs[row], [(0, 1, 'plan (x-y)'), (0, 2, 'side (x-z)'), (1, 2, 'front (y-z)')]):
        a.scatter(c[ex, i], c[ex, j], s=0.3, c='#bbbbbb', rasterized=True, label='tie / coupling (excluded)')
        sc = a.scatter(c[~ex][o, i], c[~ex][o, j], s=0.6, c=vm[~ex][o], cmap='viridis', vmin=0, vmax=vmax, rasterized=True)
        a.set_aspect('equal'); a.grid(alpha=.3); a.set_title('%s, %s' % (pl, lab), fontsize=9)
        a.legend(markerscale=10, fontsize=7, loc='upper right')
    cb = fig.colorbar(sc, ax=axs[row], shrink=0.8, extend='max'); cb.set_label('von Mises (MPa)')
fig.suptitle('%s: von Mises at the element centroids, solid elements; max %.2f MPa (limit 36.3)' % (title, vm[~ex].max()))
plt.savefig(out, dpi=80)
print('written', out)
