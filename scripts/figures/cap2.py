import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Wedge
f,axs=plt.subplots(1,2,figsize=(12,6))
for ax,t in zip(axs,["A: lid rib from above, FC is the stop below","B: lid clip that hugs the capacitor (also holds it from below)"]):
    ax.add_patch(Rectangle((-17,21.5),34,2.5,fc="#cfe2f3",ec="b"));ax.text(-16,22.2,"LID (fitted last)",fontsize=8)
    ax.add_patch(Rectangle((-16.5,-2.5),33,1.6,fc="g",alpha=.6));ax.text(-16,-2.2,"FC board",fontsize=8,color="w")
    ax.add_patch(Rectangle((-14,-0.9),24,5.9,fc="#d9ead3",ec="g"));ax.text(-13,1.5,"FC components / heat sink (top about +5)",fontsize=7)
    ax.add_patch(Circle((-5.75,10.75),5.25,fc="#f4cccc",ec="r",lw=2));ax.text(-8.6,10.5,"capacitor",fontsize=8)
    ax.annotate("",(-5.75,5.0),(-12,8.3),arrowprops=dict(arrowstyle="->",color="k",lw=2))
    ax.text(-17.5,7.6,"impact: inertia\npushes it down",fontsize=7)
    ax.set_xlim(-18,18);ax.set_ylim(-4,26);ax.set_aspect("equal");ax.set_title(t,fontsize=10)
    ax.set_xlabel("y (mm)");ax.set_ylabel("z (mm)")
ax=axs[0]
ax.add_patch(Rectangle((-12.5,17.0),13.5,4.5,fc="#cfe2f3",ec="b"))
ax.add_patch(Rectangle((-12.5,9),1.2,8,fc="#cfe2f3",ec="b"));ax.add_patch(Rectangle((-0.2,9),1.2,8,fc="#cfe2f3",ec="b"))
ax.text(1.5,15,"rib legs: stop up and\nsideways only (1 mm gap)",fontsize=7)
ax.text(0.8,6.3,"gap about 0.75 mm: the FC top\nis the only stop downward",fontsize=7,color="r")
ax=axs[1]
ax.add_patch(Rectangle((-12.0,17.0),12.5,4.5,fc="#cfe2f3",ec="b"))
ax.add_patch(Wedge((-5.75,10.75),6.45,-35,215,width=1.2,fc="#cfe2f3",ec="b"))
ax.text(1.5,15,"C-shaped clip on the lid,\nwraps past the widest point;\nflexes and snaps over the\ncapacitor as the lid goes down",fontsize=7)
ax.text(1.5,8.0,"lips below the middle hold it\nup: it no longer reaches the FC",fontsize=7,color="b")
f.tight_layout();f.savefig("cap_options.png",dpi=150)
