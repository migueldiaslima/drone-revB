"""report_plots.py - report plots in one style (vector PDF) from data/report/*.csv.
Run from the repo root: python3 scripts/figures/report_plots.py
Writes report/figures/plot_history.pdf, plot_keels.pdf, plot_capacity.pdf, plot_strength.pdf,
plot_power_models.pdf, plot_campbell.pdf"""
import csv
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA = os.path.join(ROOT, "data", "report")
OUT = os.path.join(ROOT, "report", "figures")
C = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100"]          # categorical slots 1 to 4 (validated palette)
INK, MUTED, GRID = "#28323c", "#6b7078", "#e3e5e8"
plt.rcParams.update({"font.family": "serif", "font.size": 9, "axes.edgecolor": MUTED, "axes.labelcolor": INK,
                     "xtick.color": MUTED, "ytick.color": MUTED, "axes.grid": True, "grid.color": GRID,
                     "grid.linewidth": 0.6, "axes.spines.top": False, "axes.spines.right": False,
                     "legend.frameon": False, "lines.linewidth": 1.6, "pdf.fonttype": 42})


def rows(name):
    with open(os.path.join(DATA, name)) as fh:
        return list(csv.DictReader(fh))


def history():
    r = rows("h4r4_history.csv")
    cyc = [int(x["cycle"]) for x in r]
    fig, ax = plt.subplots(3, 1, figsize=(6.4, 6.2), sharex=True)
    for a in ax:
        a.axvspan(15, 22, color="#f2efe9", zorder=0, lw=0)
    ax[0].plot(cyc, [float(x["design_volume_mm3"]) / 1000 for x in r], color=C[0])
    ax[0].set_ylabel("Design volume (cm$^3$)")
    for k in range(8, 13):
        ax[1].plot(cyc, [float(x["f%d_Hz" % k]) for x in r], color="#b7bcc3", lw=1.0)
    ax[1].plot(cyc, [float(x["f7_Hz"]) for x in r], color=C[0], label="first elastic mode")
    ax[1].axhline(417, color=INK, lw=0.9, ls="--")
    ax[1].text(0.3, 422, "417 Hz goal", va="bottom", fontsize=8, color=INK)
    ax[1].text(0.3, 600, "modes 8 to 12", fontsize=8, color=MUTED)
    ax[1].set_ylabel("Frequency (Hz)")
    ax[1].legend(loc="upper right")
    for c, lc in zip(C, ("LC1", "LC2a", "LC2b", "LC3a")):
        ax[2].plot(cyc, [float(x["SE_cap_" + lc]) for x in r], color=c, label=lc)
    ax[2].axhline(1.0, color=INK, lw=0.9, ls="--")
    ax[2].set_ylabel("Compliance / cap")
    ax[2].set_xlabel("Optimisation cycle")
    ax[2].legend(ncol=4, loc="lower right", handlelength=2.2)
    ax[0].text(18.5, ax[0].get_ylim()[1] * 0.97, "overshoot", ha="center", va="top", fontsize=8, color=MUTED)
    fig.align_ylabels(ax)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "plot_history.pdf"))


def keels():
    r = rows("th_comparison.csv")
    names = {"TH_r4b": "As optimised, iso 0.4", "TH_r4b_i30": "As optimised, iso 0.3", "TH_r4b_L": "Local iso 0.15",
             "TH_r4b_S": "Two side webs", "TH_r4b_cA": "Keels A", "TH_r4b_cAB": "Keels A + web B",
             "TH_r4b_i30_final": "Print geometry, iso 0.3"}
    sel = [x for x in r if x["model"] in names]
    fig, ax = plt.subplots(figsize=(6.4, 2.8))
    y = range(len(sel))
    f7 = [float(x["f7_Hz"]) for x in sel]
    col = [C[0] if x["result"] == "PASS" else "#b7bcc3" for x in sel]
    ax.barh(list(y), f7, color=col, height=0.55)
    ax.axvline(417, color=INK, lw=0.9, ls="--")
    ax.text(417, -0.75, "417 Hz", fontsize=8, color=INK, ha="center", va="bottom")
    for i, (v, x) in enumerate(zip(f7, sel)):
        ax.text(v + 6, i, "%.1f Hz, %s" % (v, x["result"].lower()), va="center", fontsize=8, color=INK)
    ax.set_yticks(list(y))
    ax.set_yticklabels([names[x["model"]] for x in sel])
    ax.invert_yaxis()
    ax.set_xlim(0, 560)
    ax.set_xlabel("First elastic mode of the thresholded model (Hz)")
    ax.grid(axis="y", visible=False)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "plot_keels.pdf"))


def capacity():
    r = [x for x in rows("stage7_capacity.csv") if x["table"] == "lever"]
    um, uj, Sxy, Mj = 74.25, 37.24, 54.4, 21216.0
    u = [float(x["u_mm"]) for x in r]
    Z = [float(x["Z_mm3"]) for x in r]
    F = [Sxy * z / (um - uu) for z, uu in zip(Z, u)]
    Fj = Mj / (um - uj)
    fig, ax = plt.subplots(1, 2, figsize=(6.6, 2.8))
    ax[0].plot(u, Z, color=C[0])
    ax[0].set_xlabel("Distance from the frame centre, u (mm)")
    ax[0].set_ylabel("Section modulus Z (mm$^3$)")
    ax[1].plot(u, F, color=C[0], label="arm section")
    ax[1].axhline(Fj, color=C[1], lw=1.4, label="joint (%.0f N)" % Fj)
    ax[1].axhline(Fj / 1.5, color=C[1], lw=0.9, ls="--", label="joint / 1.5")
    i = F.index(min(F))
    ax[1].plot([u[i]], [F[i]], "o", color=C[0], ms=5)
    ax[1].annotate("%.0f N at u %.0f" % (F[i], u[i]), (u[i], F[i]), xytext=(-60, -28), textcoords="offset points",
                   fontsize=8, color=INK, arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.6))
    ax[1].set_xlabel("Distance from the frame centre, u (mm)")
    ax[1].set_ylabel("Vertical tip force to fail (N)")
    ax[1].set_ylim(0, max(F) * 1.05)
    ax[1].legend(loc="upper right", fontsize=8)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "plot_capacity.pdf"))


def strength():
    r = rows("stage7_strength.csv")
    parts = ["TUB", "LID", "ARM_pp", "ARM_pm", "ARM_mp", "ARM_mm"]
    lab = {"TUB": "Tub", "LID": "Lid", "ARM_pp": "Arm 1", "ARM_pm": "Arm 2", "ARM_mp": "Arm 3", "ARM_mm": "Arm 4"}
    checks = [("VM", "von Mises"), ("S33", "tension across layers"), ("TSH", "shear between layers")]
    fig, ax = plt.subplots(figsize=(6.4, 2.6))
    w = 0.26
    for k, (ck, name) in enumerate(checks):
        vals = [max(float(x["P99_9_vol_weighted_MPa"]) / float(x["limit_MPa"]) for x in r if x["part"] == p and x["check"] == ck) for p in parts]
        ax.bar([i + (k - 1) * w for i in range(len(parts))], vals, width=w * 0.9, color=C[k], label=name)
    ax.set_xticks(range(len(parts)))
    ax.set_xticklabels([lab[p] for p in parts])
    ax.set_ylabel("Highest utilisation, P99.9")
    ax.set_ylim(0, 0.045)
    ax.legend(ncol=3, loc="upper right", fontsize=8)
    ax.grid(axis="x", visible=False)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "plot_strength.pdf"))


BENCH = [(17311.1, 91.2, 25.9), (25611.5, 202.2, 76.6), (30692.7, 292.4, 127.6), (35219.6, 380.5, 182.5),
         (40750.1, 514.1, 277.8)]      # manufacturer bench: RPM, thrust g, electrical power W


def power_models():
    """Bench power with the four fitted models (coefficients from the sizing chapter) and the hover point."""
    models = [("M1, $a n^3$", 4.18e-12, 0.0, 0.0, C[3], ":"), ("M2, $a n^3 + c$", 4.00e-12, 0.0, 8.2, C[1], "--"),
              ("M3, $a n^3 + b n$ (central)", 3.828e-12, 4.668e-4, 0.0, C[0], "-"),
              ("M4, $a n^3 + b n + c$", 3.64e-12, 1.03e-3, -10.6, C[2], "-.")]
    n = [8000 + 200 * i for i in range(170)]
    fig, axs = plt.subplots(1, 2, figsize=(6.4, 2.9), gridspec_kw={"width_ratios": [1.25, 1]})
    for k, ax in enumerate(axs):
        ax.axvspan(8000, 17311, color="#f2efe9", lw=0, zorder=0)
        for name, a, b, c, col, ls in models:
            ax.plot(n, [a * x ** 3 + b * x + c for x in n], color=col, ls=ls, label=name)
        ax.plot([r[0] for r in BENCH], [r[2] for r in BENCH], "o", color=INK, ms=4, label="bench data")
        ax.axvline(14440, color=INK, lw=0.9, ls="--")
        ax.set_xlabel("Rotor speed (RPM)")
    axs[0].set_ylabel("Electrical power per motor (W)")
    axs[0].set_xlim(8000, 42000)
    axs[0].set_xticks([10000, 20000, 30000, 40000])
    axs[1].set_xticks([10000, 12500, 15000, 17500, 20000])
    axs[0].set_ylim(-5, 290)
    axs[0].legend(loc="upper left", fontsize=7.5)
    axs[1].set_xlim(10000, 20000)
    axs[1].set_ylim(0, 40)
    axs[1].text(14600, 37, "hover", fontsize=8, color=INK, va="top")
    axs[1].text(17450, 3, "bench\ndata", fontsize=8, color=MUTED)
    axs[1].text(10300, 3, "extrapolated", fontsize=8, color=MUTED)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "plot_power_models.pdf"))


def campbell():
    """Rotor excitations against the first six elastic modes of the printed geometry (thresholded check)."""
    modes = [431.0, 432.5, 437.2, 441.4, 457.2, 533.4]
    rpm = [0, 45000]
    fig, ax = plt.subplots(figsize=(6.4, 3.4))
    ax.axvspan(14440, 40750, color="#f2efe9", lw=0, zorder=0)
    ax.plot(rpm, [r / 60.0 for r in rpm], color=C[0], label="1P (imbalance)")
    ax.plot(rpm, [3 * r / 60.0 for r in rpm], color=C[1], label="3P (blade passing)")
    for k, f in enumerate(modes):
        ax.axhline(f, color=C[2], lw=1.0 if k else 1.6, alpha=1.0 if k == 0 else 0.55)
    ax.axhline(290, color=INK, lw=0.9, ls=":")
    ax.text(600, 296, "290 Hz requirement", fontsize=8, color=INK)
    ax.text(600, 550, "modes 7 to 12 of the printed frame, 431.0 to 533.4 Hz", fontsize=8, color=C[2])
    ax.axvline(14440, color=INK, lw=0.9, ls="--")
    ax.plot([14440, 14440], [241, 722], "o", color=INK, ms=4)
    ax.text(14700, 236, "241 Hz", fontsize=8, color=INK, va="top")
    ax.text(14700, 728, "722 Hz", fontsize=8, color=INK, va="bottom")
    ax.text(27600, 1120, "flight range\n14,440 to 40,750 RPM", fontsize=8, color=MUTED, ha="center")
    ax.set_xlim(0, 45000)
    ax.set_ylim(0, 1300)
    ax.set_xlabel("Rotor speed (RPM)")
    ax.set_ylabel("Frequency (Hz)")
    ax.legend(loc="upper left", fontsize=8)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "plot_campbell.pdf"))


def merit():
    """Frequency merit index E^(1/3)/rho in the layer plane and across layers (Bambu data sheets, dry)."""
    data = [("PLA", 11.2, 10.4, "heat"), ("PLA-CF", 11.5, 10.6, "heat"), ("PETG HF", 9.5, 9.0, "heat"),
            ("PETG-CF", 10.8, 8.8, ""), ("ASA", 12.8, 12.2, ""), ("PET-CF", 13.0, 10.0, ""),
            ("PAHT-CF", 14.8, 12.2, ""), ("PPA-CF", 18.2, 13.0, "printer")]
    fig, ax = plt.subplots(figsize=(6.4, 2.8))
    w = 0.38
    for i, (name, xy, z, gate) in enumerate(data):
        a = 0.35 if gate else 1.0
        ax.bar(i - w / 2, xy, width=w * 0.92, color=C[0], alpha=a, label="in the layer plane" if i == 3 else None)
        ax.bar(i + w / 2, z, width=w * 0.92, color=C[1], alpha=a, label="across the layers" if i == 3 else None)
        if gate:
            ax.text(i, max(xy, z) + 0.4, "fails " + gate, ha="center", fontsize=7, color=MUTED)
    ax.set_xticks(range(len(data)))
    ax.set_xticklabels([d[0] for d in data], fontsize=8)
    ax.set_ylabel("$E^{1/3}/\\rho$ (MPa$^{1/3}$ cm$^3$/g)")
    ax.set_ylim(0, 20.5)
    ax.legend(loc="upper left", fontsize=8)
    ax.grid(axis="x", visible=False)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "plot_merit.pdf"))


if __name__ == "__main__":
    history()
    keels()
    capacity()
    strength()
    power_models()
    campbell()
    merit()
    print("ok")
