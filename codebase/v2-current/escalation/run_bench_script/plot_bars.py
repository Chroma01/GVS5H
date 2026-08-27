#!/usr/bin/env python3
"""Bar-chart twins of the three single-vs-manager charts: same numbers, same annotations.

One figure per condition, matching the dot/line originals one for one:

    plot_16k_reason_off_5_pass.py    -> 16k,  reasoning OFF, 5 passes
    plot_128k_reason_off_1_pass.py   -> 128k, reasoning OFF, 1 pass
    plot_128k_reason_on_1_pass.py    -> 128k, reasoning ON,  1 pass

Every statistic is imported from those modules rather than recomputed, so a bar can
never disagree with the dot it replaces. Only the drawing differs, in three ways:

  - x is categorical (models left to right by size). A log parameter axis means
    nothing for bars, so the size moves into the per-model block below the axis.
  - the paired-test bracket sits ABOVE each pair instead of beside it: the bars now
    fill the vertical space the side bracket used.
  - no interpolation curves. The first-to-last totals stay in the legend -- they are
    the difference between two measured models, not an artifact of the curve.

    uv run --with matplotlib --with numpy --with scipy python escalation/run_bench_script/plot_bars.py

Writes plots/<title-slug>_bars_{light,dark}.png -- six files.
"""
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

import plot_16k_reason_off_5_pass as p16
import plot_128k_reason_off_1_pass as p128off
import plot_128k_reason_on_1_pass as p128on
from plot_16k_reason_off_5_pass import (
    EDGE_LW, FIGSIZE, FS_BODY, FS_HEAD, FS_NOTE, FS_STAR, FS_TITLE,
    MARGINS, PLOTS, THEMES,
    apply_theme, fmt_p_num, head_label, model_block, ring, side_panel, slug, stars,
    tukey, wrap_title,
)

BAR_W = 0.38        # each bar; the pair spans 2*BAR_W with no gap between them
CI_LW = 1.6


# Each condition names its source module plus the things that genuinely differ between
# the three originals: y range, decimal places, whether per-arm CIs and per-model p
# exist, and what the first->last trend line is called. The notes live in the source
# module now -- one set per condition, covering both twins, rendered into the figure's
# LaTeX caption by make_figures_tex.py.
CONDITIONS = [
    dict(mod=p16, fills=p16.FILLS, ylim=100, dp=1, ci=True, per_model_p=True,
         span="9B → 2.8T", xlabel="Models, in order of total parameters"),
    dict(mod=p128off, fills=p128off.FILLS, ylim=95, dp=0, ci=False, per_model_p=False,
         span="9B → 2.8T", xlabel="Models, in order of total parameters"),
    dict(mod=p128on, fills=p128on.FILLS, ylim=105, dp=0, ci=False, per_model_p=False,
         span="35B → Opus-5",
         xlabel="Models, in order of total parameters (Opus-5 last, size undisclosed)"),
]


def draw(cond, stats, letters, theme="light", save=None):
    t = THEMES[theme]
    apply_theme(t)
    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(**MARGINS)

    n = len(stats)
    xs = np.arange(n, dtype=float)
    dp, fills = cond["dp"], cond["fills"]

    ax.set(xlim=(-0.65, n - 0.35), ylim=(0, cond["ylim"]))
    ax.set_xticks(xs, [""] * n)          # names live in the per-model block below
    ax.set_ylabel("Accuracy (pass@1, %)", fontsize=FS_BODY, color=t["ink2"])
    ax.xaxis.grid(False)
    ax.yaxis.grid(True)
    ax.set_axisbelow(True)
    ax.tick_params(length=0, labelsize=FS_BODY)
    for spine in ("left", "bottom"):
        ax.spines[spine].set_color(t["axis"])

    # ---- one pair of bars per model: light = single, dark = with manager
    tops = []
    for x, st in zip(xs, stats):
        fill = dict(zip(("single", "multi"), fills[st["key"]]))
        pair_top = 0
        for arm, off in (("single", -BAR_W / 2), ("multi", BAR_W / 2)):
            y = st[arm]
            ax.bar(x + off, y, BAR_W, color=fill[arm], zorder=3,
                   edgecolor=ring(fill[arm], theme), linewidth=EDGE_LW)
            label_y = y
            if cond["ci"]:
                lo, hi = st[f"{arm}_ci"]
                # drawn as a plain line + caps rather than errorbar(): an interval
                # narrower than the bar edge still has to be visible
                ax.plot([x + off, x + off], [lo, hi], lw=CI_LW, color=t["ink"],
                        solid_capstyle="butt", zorder=5)
                for end in (lo, hi):
                    ax.plot([x + off], [end], marker="_", ms=14, mew=CI_LW,
                            color=t["ink"], zorder=5)
                label_y = hi
            # nudged apart from the pair's centre line: where the two arms score
            # within a point of each other the labels sit at the same height, and
            # centred on their own bars they would touch
            ax.annotate(f"{y:.{dp}f}", xy=(x + off, label_y),
                        xytext=(8 if off > 0 else -8, 6),
                        textcoords="offset points", ha="center", va="bottom",
                        fontsize=FS_BODY, color=t["ink"])
            pair_top = max(pair_top, label_y)
        tops.append(pair_top)

    # ---- bracket over each pair with the Holm p graded above it. Only where repeats
    # exist: a single pass has no within-model test, exactly as in the dot versions.
    # The p itself is in the block under the axis, as it is there -- at 10pt a chip
    # reading "p <2 x 10^-5" is an inch wide and the pairs are 1.2in apart.
    if cond["per_model_p"]:
        head = 0.16 * cond["ylim"]       # clearance for the value labels already drawn
        for x, st, top in zip(xs, stats, tops):
            y = top + head
            col = t["ink2"] if st["sig"] else t["muted"]
            drop = 0.018 * cond["ylim"]
            ax.plot([x - BAR_W / 2, x - BAR_W / 2, x + BAR_W / 2, x + BAR_W / 2],
                    [y - drop, y, y, y - drop], lw=1.6, color=col,
                    solid_joinstyle="miter", zorder=4)
            mark = stars(st["p_holm"])
            ax.annotate(mark or "n.s.", xy=(x, y), xytext=(0, 4),
                        textcoords="offset points", ha="center", va="bottom",
                        fontsize=FS_STAR if mark else FS_NOTE,
                        color=t["ink"] if mark else t["muted"], zorder=5)

    # ---- per-model block under the axis: size, delta, Holm p, Tukey group
    for x, st, i in zip(xs, stats, range(n)):
        sig = st.get("sig", True)
        col = t["ink2"] if sig else t["muted"]
        rows = [(head_label(st), FS_HEAD, "bold", t["ink"]),
                (f"Δ {st['delta']:+.{dp}f} pp", FS_NOTE, "normal", col)]
        if cond["per_model_p"]:
            rows.append((f"p {fmt_p_num(st['p_holm'], 1, st['floored'])}",
                         FS_NOTE, "normal", col))
        rows.append((f"group {letters[i]}", FS_NOTE, "normal", t["ink2"]))
        drop = model_block(ax, x, rows)

    # the categorical axis needs saying what the order is; the dot twins get it free
    # from their log parameter axis
    ax.annotate(cond["xlabel"], xy=(0.5, 0), xycoords="axes fraction",
                xytext=(0, -(drop + 12)), textcoords="offset points",
                ha="center", va="top", fontsize=FS_BODY, color=t["ink2"])

    # ---- right column: a light/dark swatch pair per model and the trend totals
    swatches, names = [], []
    for st in stats:
        light, dark = fills[st["key"]]
        swatches.append(tuple(
            Patch(facecolor=c, edgecolor=ring(c, theme), linewidth=EDGE_LW)
            for c in (light, dark)))
        names.append(st["label"])

    span = cond["span"]
    totals = {arm: stats[-1][arm] - stats[0][arm] for arm in ("single", "multi")}
    trend = [Patch(facecolor="none", edgecolor="none",
                   label=f"Single call\n{totals['single']:+.{dp}f} pts, {span}"),
             Patch(facecolor="none", edgecolor="none",
                   label=f"With manager\n{totals['multi']:+.{dp}f} pts, {span}")]

    fig.suptitle(wrap_title(cond["mod"].TITLE), x=MARGINS["left"], ha="left", y=0.99,
                 va="top", fontsize=FS_TITLE, fontweight="bold", color=t["ink"],
                 linespacing=1.25)
    side_panel(fig, t, swatches, names, trend,
               trend_kw=dict(handletextpad=0.0, handlelength=0.0))
    if save:
        # no crop: the canvas is authored at exactly PAGE_SCALE x its printed size
        fig.savefig(save)
        print("wrote", save)
    plt.close(fig)


def main():
    os.makedirs(PLOTS, exist_ok=True)
    for cond in CONDITIONS:
        stats = cond["mod"].compute()
        _, letters = tukey(stats)      # the pairwise p values go in the caption
        print(f"\n{cond['mod'].TITLE}")
        for i, st in enumerate(stats):
            extra = (f"  p_holm {st['p_holm']:.2e}" if cond["per_model_p"] else "")
            print(f"  {st['label']:13s} single {st['single']:5.1f}  multi {st['multi']:5.1f}"
                  f"  Δ {st['delta']:+6.1f}  Tukey {letters[i]}{extra}")
        for theme in ("light", "dark"):
            draw(cond, stats, letters, theme,
                 save=os.path.join(PLOTS, f"{slug(cond['mod'].TITLE)}_bars_{theme}.png"))


if __name__ == "__main__":
    main()
