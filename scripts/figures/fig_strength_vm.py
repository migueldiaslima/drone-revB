# fig_strength_vm.py - report figure: von Mises at the element centroids of the solid elements of the
# thresholded model for one load case (stress_th.py output npz), plan, side and front view, on two scales:
# 0 to the limit, and 0 to the volume-weighted 99.9th percentile of the whole frame.
# Each point is an element, sorted so the highest values are drawn on top; tie / coupling elements grey.
# Usage: python3 fig_strength_vm.py <stress npz> <out.png> "<case label>"
import sys, numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

D = np.load(sys.argv[1])
out = sys.argv[2]
case = sys.argv[3] if len(sys.argv) > 3 else ''
c, vm, ex, vol = D['cen'], D['VM'], D['excl'].astype(bool), D['vol']
LIM = 36.3

# volume-weighted P99.9 over the checked solid elements (same definition as stress_th.py)
s, v = vm[~ex], vol[~ex]
o = np.argsort(s)
cv = np.cumsum(v[o])
p999 = float(s[o][np.searchsorted(cv, 0.999 * cv[-1])])
print('checked elements %d, max %.2f MPa, volume-weighted P99.9 %.2f MPa' % (s.size, s.max(), p999))

fig = plt.figure(figsize=(12, 7.2))
gs = GridSpec(2, 3, figure=fig, width_ratios=[1.0, 1.0, 1.0], height_ratios=[1, 1], wspace=0.25, hspace=0.32,
              left=0.05, right=0.90, top=0.93, bottom=0.07)
views = [(0, 1, 'plan', 'x (mm)', 'y (mm)'), (0, 2, 'side', 'x (mm)', 'z (mm)'), (1, 2, 'front', 'y (mm)', 'z (mm)')]
oo = np.argsort(vm[~ex])
cs, vs = c[~ex][oo], vm[~ex][oo]
for row, vmax, lab in ((0, LIM, 'scale 0 to the limit, %.1f MPa' % LIM),
                       (1, p999, 'scale 0 to the 99.9th percentile, %.2f MPa' % p999)):
    for col, (i, j, nm, xl, yl) in enumerate(views):
        a = fig.add_subplot(gs[row, col])
        a.scatter(c[ex, i], c[ex, j], s=0.15, c='#bbbbbb', rasterized=True, linewidths=0)
        sc = a.scatter(cs[:, i], cs[:, j], s=0.25, c=vs, cmap='viridis', vmin=0, vmax=vmax,
                       rasterized=True, linewidths=0)
        a.set_aspect('equal'); a.set_xlim(-68, 68)
        a.set_ylim(-68, 68) if j == 1 else a.set_ylim(-18, 30)
        a.set_title('%s, %s' % (nm, lab), fontsize=8)
        a.set_xlabel(xl, fontsize=8); a.set_ylabel(yl, fontsize=8); a.tick_params(labelsize=7)
    pos = fig.add_subplot(gs[row, 2]).get_position(); fig.axes[-1].remove()
    cax = fig.add_axes([0.92, pos.y0 + 0.05, 0.012, pos.height - 0.10])
    cb = fig.colorbar(sc, cax=cax, extend='max'); cb.set_label('von Mises (MPa)', fontsize=8)
    cb.ax.tick_params(labelsize=7)
fig.suptitle('von Mises stress, %s; largest element %.2f MPa against the limit %.1f MPa (grey: elements at couplings and ties)'
             % (case, s.max(), LIM), fontsize=9)
plt.savefig(out, dpi=200)
print('written', out)
