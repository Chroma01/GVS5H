#!/usr/bin/env python3
"""Single call vs manager across model scale, LCB-100 at 128k (runs/128k-clean).

"Single call" is one API call with no tools and no loop -- the raw model, not an agent.
On disk that arm is still named `*_single.json`, so the code keys stay `single`.

Same chart as plot_16k_reason_off_5_pass.py, minus the per-model paired test: this run is
1 pass per condition, so only the cross-model Tukey HSD is shown.

    uv run --with matplotlib --with numpy --with scipy python escalation/run_bench_script/plot_128k_reason_off_1_pass.py

Writes plots/<title-slug>_{light,dark}.png.
"""
import json
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

from plot_16k_reason_off_5_pass import (
    ALPHA, DOT, EDGE_LW, FIGSIZE, FILLS, FS_BODY, FS_HEAD, FS_NOTE, FS_TITLE,
    MARGINS, MODELS, PLOTS, THEMES,
    apply_theme, boot_ci, head_label, model_block, ring, side_panel, slug,
    tint, tukey, wrap_title,
)

HERE = os.path.dirname(os.path.abspath(__file__))
ESC = os.path.dirname(HERE)             # escalation/, one level up from run_bench_script/
RESULTS = os.path.join(ESC, "runs/128k-clean/results")

TITLE = ("Manager vs single call across model scale "
         "— LCB-100, 1 pass, 128k max tokens, reasoning OFF")

# see the note on CAPTION in plot_16k_reason_off_5_pass.py: make_figures_tex.py renders
# these into the figure's LaTeX caption, where they are set in real \footnotesize
CAPTION = "\\textbf{Reasoning off:} 128k $\\times$ 1-pass control."


def notes(stats):
    return [
        "Fill: light = single call (one call, no tools), dark = with manager. 128k max "
        "tokens, reasoning off (ESCALATION_OR_REASONING=none), 1 pass per condition.",
        "Δ = with manager − single call, in percentage points. With one pass per condition "
        "there is no within-model repeat, so no per-model p is shown.",
        "Each block under the axis heads with the model's size, not its name — 9B and "
        "35B are too close on the log axis of (a) for a name to fit — and the legend maps "
        "fill colour to name. The curves in (a) connect each condition's own 4 points "
        "(monotone cubic): they interpolate, they are not fits.",
        f"Tukey groups: models sharing a letter have indistinguishable Δ (HSD, "
        f"α {ALPHA}); HSD ignores that all models saw the same 100 problems, so it is "
        "conservative.",
    ]


# --------------------------------------------------------------------------- data

def load_arm(model, arm):
    """-> (qids, passed[N] bool). One file per config: this run is a single pass.

    The .regraded.json twin, for the reason in plot_16k_reason_off_5_pass.load_arm.
    """
    lcb = json.load(open(f"{RESULTS}/{model}_{arm}.regraded.json")).get("lcb")
    recs = lcb["records"]
    return [r["question_id"] for r in recs], np.array([bool(r["passed"]) for r in recs])


def compute():
    stats = []
    for key, (label, params) in MODELS.items():
        (q_s, s), (q_m, m) = load_arm(key, "single"), load_arm(key, "multiagent")
        assert q_s == q_m, f"{key}: arms cover different problems"
        s, m = s.astype(float), m.astype(float)
        stats.append(dict(
            key=key, label=label, params=params, d=100 * (m - s),
            single=100 * s.mean(), multi=100 * m.mean(),
            delta=100 * (m - s).mean(),
            delta_ci=tuple(100 * v for v in boot_ci(m - s)),
        ))
    return stats


# --------------------------------------------------------------------------- plot

def draw(stats, letters, theme="light", save=None):
    t = THEMES[theme]
    apply_theme(t)
    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(**MARGINS)

    # axes geometry must be final before y_offset() converts point offsets to data units
    ax.set_xscale("log")
    ax.set_xticks([1e10, 1e11, 1e12], ["10B", "100B", "1T"])
    ax.minorticks_off()
    # x padding is half a value label wide at each end, no more: the models have to sit
    # as far apart as the axis allows for the per-model blocks below to clear each other
    ax.set(xlim=(6e9, 4.2e12), ylim=(0, 95))
    ax.set_ylabel("Accuracy (pass@1, %)", fontsize=FS_BODY, color=t["ink2"])
    ax.xaxis.grid(False)
    ax.yaxis.grid(True)
    ax.set_axisbelow(True)
    ax.tick_params(length=0, labelsize=FS_BODY)
    for spine in ("left", "bottom"):
        ax.spines[spine].set_color(t["axis"])

    # ---- one curve per condition, through its own points (no extrapolation)
    from scipy.interpolate import PchipInterpolator
    lx = np.log10([st["params"] for st in stats])
    span = np.linspace(lx.min(), lx.max(), 300)
    totals = {}
    for arm, style in (("single", "--"), ("multi", "-")):
        ys = [st[arm] for st in stats]
        totals[arm] = ys[-1] - ys[0]
        ax.plot(10 ** span, PchipInterpolator(lx, ys)(span), ls=style, lw=1.6,
                color=t["muted"], alpha=0.9, zorder=1)

    # ---- both arms share the model's x, so each pair reads as one vertical stack.
    # Value labels go above the upper arm and below the lower one: models are 0.9in
    # apart on the page, and a label beside a dot would run into the next one along.
    for st in stats:
        x = st["params"]
        fill = dict(zip(("single", "multi"), FILLS[st["key"]]))
        upper = "multi" if st["multi"] >= st["single"] else "single"
        for arm in ("single", "multi"):
            y = st[arm]
            ax.scatter([x], [y], s=DOT, color=fill[arm], zorder=4,
                       edgecolor=ring(fill[arm], theme), linewidth=EDGE_LW)
            dy, va = (12, "bottom") if arm == upper else (-12, "top")
            ax.annotate(f"{y:.0f}", xy=(x, y), xytext=(0, dy),
                        textcoords="offset points", ha="center", va=va,
                        fontsize=FS_BODY, color=t["ink"])

    # ---- per-model block under the axis: size, delta, Tukey group. The head row is
    # the size, not the name: 9B and 35B are 0.6 of a decade apart, about 1.2in here,
    # and "Qwen3.5-9b" at 9pt is wider than that. The legend carries colour -> name.
    for i, st in enumerate(stats):
        drop = model_block(ax, st["params"], [
            (head_label(st), FS_HEAD, "bold", t["ink"]),
            (f"Δ {st['delta']:+.0f} pp", FS_NOTE, "normal", t["ink2"]),
            (f"group {letters[i]}", FS_NOTE, "normal", t["ink2"])])

    ax.annotate("Total parameters, log scale", xy=(0.5, 0), xycoords="axes fraction",
                xytext=(0, -(drop + 12)), textcoords="offset points",
                ha="center", va="top", fontsize=FS_BODY, color=t["ink2"])

    # ---- right column: one swatch pair per model, the two condition curves, notes
    pairs, names = [], []
    for st in stats:
        light, dark = FILLS[st["key"]]
        pairs.append(tuple(
            Line2D([], [], marker="o", ls="", ms=12, color=c,
                   markeredgecolor=ring(c, theme), markeredgewidth=EDGE_LW)
            for c in (light, dark)))
        names.append(st["label"])

    # label wraps: the column is ~2.4in wide on the page, one line would not fit
    trend = [Line2D([], [], ls="--", lw=1.6, color=t["muted"],
                    label=f"Single call\n{totals['single']:+.0f} pts, 9B → 2.8T"),
             Line2D([], [], ls="-", lw=1.6, color=t["muted"],
                    label=f"With manager\n{totals['multi']:+.0f} pts, 9B → 2.8T")]

    fig.suptitle(wrap_title(TITLE), x=MARGINS["left"], ha="left", y=0.99,
                 va="top", fontsize=FS_TITLE, fontweight="bold", color=t["ink"],
                 linespacing=1.25)
    side_panel(fig, t, pairs, names, trend,
               trend_kw=dict(handletextpad=0.7, handlelength=2.2))
    if save:
        # no crop: the canvas is authored at exactly PAGE_SCALE x its printed size
        fig.savefig(save)
        print("wrote", save)
    return fig


def main():
    stats = compute()
    pmat, letters = tukey(stats)

    hdr = f"{'model':13s} {'single':>7s} {'multi':>7s} {'delta':>7s} {'95% CI':>16s}  Tukey"
    print(hdr)
    print("-" * len(hdr))
    for i, st in enumerate(stats):
        print(f"{st['label']:13s} {st['single']:7.1f} {st['multi']:7.1f} {st['delta']:+7.1f}"
              f"   [{st['delta_ci'][0]:+5.1f},{st['delta_ci'][1]:+6.1f}]  {letters[i]}")

    names = [st["label"] for st in stats]
    print("\nTukey HSD across models on the per-problem delta:")
    for i in range(len(stats)):
        for j in range(i + 1, len(stats)):
            print(f"  {names[i]:12s} vs {names[j]:12s} "
                  f"gap {stats[i]['delta'] - stats[j]['delta']:+6.1f} pp"
                  f"   p {pmat[i][j]:.4g}")

    os.makedirs(PLOTS, exist_ok=True)
    for theme in ("light", "dark"):
        draw(stats, letters, theme,
             save=os.path.join(PLOTS, f"{slug(TITLE)}_{theme}.png"))


if __name__ == "__main__":
    main()
