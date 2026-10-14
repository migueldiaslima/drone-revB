# fig_restoration.py - report figure: the smoothed iso surface of the tub (iso 0.3) against the restored print part,
# whole tub from above and below. Usage: python3 fig_restoration.py <iso stl> <print stl> <out.png>
import sys, os, numpy as np, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import su_render as R
A, B = R.read_stl(sys.argv[1]), R.read_stl(sys.argv[2])


def refine(T, lmax=1.2, passes=6):
    # split long triangles at the midpoint of their longest edge, so that the depth sort of the painter's
    # algorithm works on Boolean output with long slivers
    for _ in range(passes):
        e = np.stack([np.linalg.norm(T[:, (k + 1) % 3] - T[:, k], axis=1) for k in range(3)], 1)
        long_ = e.max(1) > lmax
        if not long_.any():
            break
        L, S = T[long_], T[~long_]
        k = e[long_].argmax(1)
        a = L[np.arange(len(L)), k]; b = L[np.arange(len(L)), (k + 1) % 3]; c = L[np.arange(len(L)), (k + 2) % 3]
        m = 0.5 * (a + b)
        T = np.concatenate([S, np.stack([a, m, c], 1), np.stack([m, b, c], 1)])
    return T


B = refine(B)
print('restored part after refinement: %d triangles' % len(B))
fig, axs = plt.subplots(2, 2, figsize=(14, 12))
for j, (T, lab) in enumerate(((A, 'smoothed iso-density surface 0.3'), (B, 'restored print part'))):
    for i, v in enumerate(('iso', 'below')):
        R.draw(axs[i][j], T, v)
        axs[i][j].collections[-1].set_antialiased(False)   # no blending of sub-pixel triangles with hidden ones
    axs[0][j].set_title(lab, fontsize=12)
plt.tight_layout(); plt.savefig(sys.argv[3], dpi=170); print('written', sys.argv[3])
