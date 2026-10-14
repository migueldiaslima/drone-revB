# fig_iso_snapshots.py - report figure (docs/report_figures_setup.md item 3): iso surfaces of the production
# optimisation at several saved cycles (iso_mt.py output, whole frame), two views per cycle. ASCII only.
# Usage: python3 fig_iso_snapshots.py <out.png> <iso> <label1>=<stl1> <label2>=<stl2> ...
#   e.g. python3 fig_iso_snapshots.py su_iso_snapshots.png 0.3 "cycle 0"=mt_..._000_030.stl "cycle 10"=...
import sys, os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import su_render as R

out, iso = sys.argv[1], sys.argv[2]
items = [a.split('=', 1) for a in sys.argv[3:]]
fig, axs = plt.subplots(2, len(items), figsize=(5.5 * len(items), 9.5), squeeze=False)
for k, (lab, fn) in enumerate(items):
    T = R.read_stl(fn)
    vol = np.einsum('ij,ij->i', T[:, 0], np.cross(T[:, 1], T[:, 2])).sum() / 6.0
    R.draw(axs[0][k], T, 'iso')
    R.draw(axs[1][k], T, 'below')
    axs[0][k].set_title('%s (enclosed volume %.0f mm$^3$)' % (lab, vol), fontsize=11)
    print('%s: %d triangles, %.1f mm^3' % (lab, len(T), vol))
fig.suptitle('Production optimisation: iso-density surface %s at saved cycles (top: view from above, bottom: from below)' % iso, fontsize=12)
plt.tight_layout()
plt.savefig(out, dpi=200)
print('written', out)
