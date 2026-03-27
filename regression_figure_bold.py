import re
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

# ============================================================
# Font settings (important for EPS/PDF)
# ============================================================
mpl.rcParams["ps.fonttype"] = 42
mpl.rcParams["pdf.fonttype"] = 42

# ============================================================
# Data
# ============================================================
rows = [
    ("Age (per 10 years)", "SARD-ILD (vs. SARD-noILD)", "1.13 (1.07, 1.20)", "1.13 (1.07, 1.20)"),
    ("Age (per 10 years)", "RA-ILD (vs. RA-noILD)",     "1.10 (1.02, 1.20)", "1.11 (1.02, 1.21)"),
    ("Age (per 10 years)", "SSc-ILD (vs. SSc-noILD)",   "0.94 (0.81, 1.09)", "0.95 (0.82, 1.10)"),
    ("Age (per 10 years)", "SjD-ILD (vs. SjD-noILD)",   "1.11 (1.00, 1.23)", "1.12 (1.01, 1.25)"),
    ("Age (per 10 years)", "SLE-ILD (vs. SLE-noILD)",   "1.30 (1.15, 1.48)", "1.31 (1.15, 1.49)"),
    ("Age (per 10 years)", "MCTD-ILD (vs. MCTD-noILD)", "1.13 (0.94, 1.36)", "1.15 (0.95, 1.39)"),
    ("Age (per 10 years)", "IIM-ILD (vs. IIM-noILD)",   "1.06 (0.86, 1.32)", "1.07 (0.86, 1.33)"),

    ("Male sex (vs. Female sex)", "SARD-ILD (vs. SARD-noILD)", "1.04 (0.84, 1.27)", "0.96 (0.78, 1.19)"),
    ("Male sex (vs. Female sex)", "RA-ILD (vs. RA-noILD)",     "0.93 (0.70, 1.23)", "0.88 (0.66, 1.16)"),
    ("Male sex (vs. Female sex)", "SSc-ILD (vs. SSc-noILD)",   "1.00 (0.56, 1.77)", "1.05 (0.59, 1.88)"),
    ("Male sex (vs. Female sex)", "SjD-ILD (vs. SjD-noILD)",   "0.82 (0.52, 1.29)", "0.76 (0.48, 1.21)"),
    ("Male sex (vs. Female sex)", "SLE-ILD (vs. SLE-noILD)",   "0.57 (0.26, 1.24)", "0.51 (0.23, 1.13)"),
    ("Male sex (vs. Female sex)", "MCTD-ILD (vs. MCTD-noILD)", "0.79 (0.34, 1.81)", "0.83 (0.35, 1.93)"),
    ("Male sex (vs. Female sex)", "IIM-ILD (vs. IIM-noILD)",   "1.48 (0.72, 3.03)", "1.62 (0.78, 3.39)"),

    ("Ever Smoking (vs. Never Smoking)", "SARD-ILD (vs. SARD-noILD)", "1.09 (0.93, 1.28)", "1.04 (0.88, 1.22)"),
    ("Ever Smoking (vs. Never Smoking)", "RA-ILD (vs. RA-noILD)",     "1.08 (0.87, 1.35)", "1.05 (0.84, 1.32)"),
    ("Ever Smoking (vs. Never Smoking)", "SSc-ILD (vs. SSc-noILD)",   "0.79 (0.53, 1.18)", "0.80 (0.53, 1.19)"),
    ("Ever Smoking (vs. Never Smoking)", "SjD-ILD (vs. SjD-noILD)",   "1.02 (0.76, 1.36)", "0.99 (0.74, 1.33)"),
    ("Ever Smoking (vs. Never Smoking)", "SLE-ILD (vs. SLE-noILD)",   "1.20 (0.83, 1.74)", "1.11 (0.77, 1.62)"),
    ("Ever Smoking (vs. Never Smoking)", "MCTD-ILD (vs. MCTD-noILD)", "0.83 (0.48, 1.44)", "0.80 (0.45, 1.40)"),
    ("Ever Smoking (vs. Never Smoking)", "IIM-ILD (vs. IIM-noILD)",   "0.67 (0.35, 1.28)", "0.61 (0.31, 1.19)"),
]

df = pd.DataFrame(rows, columns=["group", "label", "unadjusted", "adjusted"])

def parse_or_ci(s):
    m = re.match(r"([0-9.]+)\s*\(([0-9.]+),\s*([0-9.]+)\)", s)
    return float(m.group(1)), float(m.group(2)), float(m.group(3))

df[["u_or","u_lo","u_hi"]] = df["unadjusted"].apply(lambda x: pd.Series(parse_or_ci(x)))
df[["a_or","a_lo","a_hi"]] = df["adjusted"].apply(lambda x: pd.Series(parse_or_ci(x)))

def fmt(x): return f"{x:>4.2f}"
def fmt_ci(or_, lo, hi): return f"{fmt(or_)} ({fmt(lo)}, {fmt(hi)})"

df["u_txt"] = df.apply(lambda r: fmt_ci(r.u_or, r.u_lo, r.u_hi), axis=1)
df["a_txt"] = df.apply(lambda r: fmt_ci(r.a_or, r.a_lo, r.a_hi), axis=1)

group_order = df["group"].unique()

rows_out = []
for g in group_order:
    rows_out.append({"kind":"header","label":g})
    for _, r in df[df.group==g].iterrows():
        rows_out.append({"kind":"data", **r})
    rows_out.append({"kind":"space"})

plot_df = pd.DataFrame(rows_out[:-1])
plot_df["y"] = np.arange(len(plot_df))[::-1]
n = len(plot_df)

fig = plt.figure(figsize=(14.5, max(10, 0.42*n)))
gs = GridSpec(1,5,width_ratios=[3.5,2.6,2.0,2.6,2.0], wspace=0.03)

axL = fig.add_subplot(gs[0,0])
axU = fig.add_subplot(gs[0,1], sharey=axL)
axUt = fig.add_subplot(gs[0,2], sharey=axL)
axA = fig.add_subplot(gs[0,3], sharey=axL)
axAt = fig.add_subplot(gs[0,4], sharey=axL)

xmin, xmax = 0.2, 4.0

def hide(ax):
    ax.set_xlim(0,1); ax.set_ylim(-1,n); ax.axis("off")

def forest(ax,title):
    ax.set_xscale("log")
    ax.set_xlim(xmin,xmax)
    ax.set_ylim(-1,n)
    ax.axvline(1, ls="--", lw=1)
    ax.set_title(title, fontsize=11, fontweight="bold", pad=6)
    ax.set_yticks([])
    ax.set_xticks([0.25,0.5,1,2,4])
    ax.get_xaxis().set_major_formatter(plt.ScalarFormatter())
    ax.grid(axis="x", ls=":", lw=0.7)
    for s in ["top","right","left"]: ax.spines[s].set_visible(False)

hide(axL); hide(axUt); hide(axAt)
forest(axU,"Panel A. Unadjusted")
forest(axA,"Panel B. Multivariable adjusted")

for _, r in plot_df.iterrows():
    y = r.y

    if r.kind=="header":
        axL.text(0,y,r.label,fontweight="bold",va="center")
        continue
    if r.kind=="space": continue

    axL.text(0.04,y,r.label,va="center")

    u_sig = (r.u_lo > 1) or (r.u_hi < 1)
    a_sig = (r.a_lo > 1) or (r.a_hi < 1)

    axU.errorbar(
        r.u_or, y,
        xerr=[[r.u_or-r.u_lo],[r.u_hi-r.u_or]],
        fmt="o", color="black", capsize=3,
        markersize=8 if u_sig else 6,
        markeredgewidth=1.5 if u_sig else 1.0,
        elinewidth=1.5 if u_sig else 1.0
    )

    axA.errorbar(
        r.a_or, y,
        xerr=[[r.a_or-r.a_lo],[r.a_hi-r.a_or]],
        fmt="s", color="black", capsize=3,
        markersize=8 if a_sig else 6,
        markeredgewidth=1.5 if a_sig else 1.0,
        elinewidth=1.5 if a_sig else 1.0
    )

    axUt.text(
        0, y, r.u_txt,
        va="center", ha="left",
        fontweight="bold" if u_sig else "normal"
    )
    axAt.text(
        0, y, r.a_txt,
        va="center", ha="left",
        fontweight="bold" if a_sig else "normal"
    )

    axU.set_xlabel("Odds Ratio", fontsize=10)
    axA.set_xlabel("Odds Ratio", fontsize=10)

fig.subplots_adjust(left=0.04,right=0.98,top=0.95,bottom=0.05,wspace=0.03)

plt.savefig("forest_plot.eps", format="eps", dpi=600)
plt.savefig("forest_plot.pdf", bbox_inches="tight")
plt.savefig("forest_plot.png", dpi=600, bbox_inches="tight")

plt.show()