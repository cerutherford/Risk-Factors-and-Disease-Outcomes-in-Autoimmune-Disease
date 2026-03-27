import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

# ==============================
# Data
# ==============================
all_of_us = 626396
all_sard = 9546
not_sard = all_of_us - all_sard

diseases = [
    ("RA", 5080, 355),
    ("SLE", 1950, 136),
    ("SSc", 520, 167),
    ("SjD", 3291, 224),
    ("IIM", 207, 65),
    ("MCTD", 332, 85),
]

# ==============================
# Setup
# ==============================
fig, ax = plt.subplots(figsize=(22, 10.5))
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis("off")

def box(x, y, w, h, text, fc="#f2f2f2", fs=11, bold=False, lw=1.6):
    rect = Rectangle(
        (x - w / 2, y - h / 2), w, h,
        facecolor=fc, edgecolor="black", linewidth=lw
    )
    ax.add_patch(rect)
    ax.text(
        x, y, text,
        ha="center", va="center",
        fontsize=fs,
        fontweight="bold" if bold else "normal",
        wrap=True
    )

def line(x1, y1, x2, y2, lw=1.2):
    ax.plot([x1, x2], [y1, y2], color="black", lw=lw)

# ==============================
# Layout coordinates
# ==============================
x_center = 0.50

y_all = 0.885
y_sard = 0.72
y_disease = 0.50
y_bottom = 0.28

# horizontal splitter below SARD box
y_split = 0.615

# disease x positions
xs = [0.08, 0.24, 0.40, 0.56, 0.72, 0.88]

# ==============================
# Top boxes
# ==============================
box(
    x_center, y_all, 0.30, 0.085,
    f"All of Us participants\nn={all_of_us:,}",
    fc="#f2f2f2", fs=15, bold=True
)

box(
    x_center, y_sard, 0.26, 0.085,
    f"Met SARD definition\nn={all_sard:,}",
    fc="#f2f2f2", fs=14, bold=True
)

line(x_center, y_all - 0.0425, x_center, y_sard + 0.0425, lw=1.4)

# Right exclusion box (moved slightly left)
x_excl = 0.79
box(
    x_excl, y_sard, 0.28, 0.075,
    f"Did not meet SARD definition\nn={not_sard:,}",
    fc="#f9f9f9", fs=12
)

line(x_center + 0.13, y_sard, x_excl - 0.14, y_sard, lw=1.3)

# ==============================
# Splitter under SARD box
# ==============================
line(x_center, y_sard - 0.0425, x_center, y_split, lw=1.3)
line(xs[0], y_split, xs[-1], y_split, lw=1.3)

# ==============================
# Disease boxes
# ==============================
disease_w = 0.145
disease_h = 0.085

for x, (name, total, ild) in zip(xs, diseases):
    line(x, y_split, x, y_disease + disease_h / 2, lw=1.2)
    box(
        x, y_disease, disease_w, disease_h,
        f"Met {name} definition\nn={total:,}",
        fc="#f2f2f2", fs=12, bold=True
    )

# ==============================
# Bottom ILD split boxes
# ==============================
small_w = 0.10
small_h = 0.078
offset = 0.044

for x, (name, total, ild) in zip(xs, diseases):
    did_not_meet_ild = total - ild

    # connectors from disease box to lower boxes
    line(x, y_disease - disease_h / 2, x - offset, y_bottom + small_h / 2, lw=1.1)
    line(x, y_disease - disease_h / 2, x + offset, y_bottom + small_h / 2, lw=1.1)

    # met ILD algorithm
    box(
        x - offset, y_bottom, small_w, small_h,
        f"Met {name}-ILD\nalgorithm\nn={ild:,}",
        fc="#f2f2f2", fs=10.5
    )

    # did not meet ILD algorithm
    box(
        x + offset, y_bottom, small_w, small_h,
        f"Did not meet\n{name}-ILD algorithm\nn={did_not_meet_ild:,}",
        fc="#f9f9f9", fs=10
    )

# ==============================
# Title and note
# ==============================
ax.text(
    0.5, 0.972,
    "Ascertainment of SARD and SARD-ILD Cohorts in All of Us",
    ha="center", va="top", fontsize=18, fontweight="bold"
)

ax.text(
    0.5, 0.065,
    "Note: Disease-specific cohorts are not mutually exclusive; some participants met more than one SARD algorithm.",
    ha="center", va="center", fontsize=11, style="italic"
)

# ==============================
# Save
# ==============================
plt.tight_layout(rect=[0.02, 0.04, 0.98, 0.96])
plt.savefig("flowchart_final.png", dpi=600, bbox_inches="tight")
plt.savefig("flowchart_final.pdf", bbox_inches="tight")
plt.show()