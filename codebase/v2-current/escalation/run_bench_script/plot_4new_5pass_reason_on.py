#!/usr/bin/env python3
"""Single call vs manager for the four pinned-backend models, LCB-100 x 5 passes at 128k, ON.

The companion to plot_16k_reason_off_5_pass.py (the paper's Figure 4) for the model set of
S2.1. Dots are pass@1 per condition with 95% CIs across the five passes; brackets carry the
per-model paired permutation test, Holm-corrected across the three models that have both
arms.

Each manager arm is ALSO tested against Fable 5's single call -- the dashed rule across the
panel -- since Fable 5 is here as the ceiling and a bar sitting just under the rule invites
the question of whether it is really under it. Those three tests are Holm-corrected as their
own family of 3, not pooled with the three within-model ones, so that they stay the same
numbers plot_q38_vs_fable5_5_pass.py reports -- that chart is no longer in the paper, but it
is still the second reading of this comparison and the two should not disagree. The sign
differs: here it is manager minus Fable 5, so a negative number means the bar is under the
rule, which is what the eye reads off the chart; that script reports Fable 5 minus the
manager.

Two things differ from the 16k chart deliberately:

  * The x axis is CATEGORICAL, not parameter count. Three of these four models have
    undisclosed sizes, so a scale axis would be three placeholder positions and one real
    one -- which invites exactly the cross-model reading the data cannot support. Models are
    ordered by single-call score instead, left to right, which makes the shrinking manager
    gain legible without asserting anything about size.

  * Fable 5 contributes ONE arm. It was run single-only, so it has no delta and no bracket;
    it is here as the single-call ceiling the other three are measured against.

Reads the *.regraded.json files (see escalation/regrade.py and paper S3.3), and for
Qwen3.8's single arm the *.cap128k.regraded.json replay, so every arm is at 128k and every
arm is scored on the fixed evaluator -- matching the S2.1 table exactly.

    uv run --with matplotlib --with numpy --with scipy python escalation/run_bench_script/plot_4new_5pass_reason_on.py

Writes plots/<title-slug>_{light,dark}.png and the _bars variants.
"""
import json
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

from plot_16k_reason_off_5_pass import (
    ALPHA, CI_LW, DOT, EDGE_LW, FIGSIZE, FS_BODY, FS_NOTE, FS_STAR, FS_SUB, FS_TITLE,
    MARGINS, PLOTS, THEMES,
    apply_theme, fmt_p_num, holm, pass_ci, perm_sign_p, ring, slug, stars, wrap_title,
)
from matplotlib.legend_handler import HandlerTuple

HERE = os.path.dirname(os.path.abspath(__file__))
ESC = os.path.dirname(HERE)
PASSES = [1, 2, 3, 4, 5]
R4 = f"{ESC}/runs/4models-1pass-reason-on/results"
RF = f"{ESC}/runs/fable5-5pass-single/results"

# key -> (label, single pattern, manager pattern or None). Left-to-right order is the draw
# order; see the module docstring on why it is by single-call score rather than by size.
# Qwen3.8's single arm is the 128k cap-matched replay, not the 250k generation, so all four
# columns are at one cap (paper S3.2, "Cap-matching").
MODELS = [
    ("q38",   "Qwen3.8-27B",   f"{R4}/q38_single_p%d.cap128k.regraded.json",
                               f"{R4}/q38_multiagent_p%d.regraded.json"),
    ("luna",  "GPT-5.6-Luna",  f"{R4}/luna_single_p%d.regraded.json",
                               f"{R4}/luna_multiagent_p%d.regraded.json"),
    ("terra", "GPT-5.6-Terra", f"{R4}/terra_single_p%d.regraded.json",
                               f"{R4}/terra_multiagent_p%d.regraded.json"),
    ("fable", "Claude Fable 5", f"{RF}/fable5_single_p%d.regraded.json", None),
]

# The 250k generation the q38 replay was cut from, read so the console table can report
# what the cap costs instead of the number being carried by hand. The caption used to
# quote it too; that sentence is gone, since S2.2 already costs the cap out.
Q38_ASGEN = f"{R4}/q38_single_p%d.regraded.json"

# hue = model, lightness = condition, the convention the other four charts use. Teal and
# magenta are carried over from the Qwen3.8-vs-Fable-5 chart so the two figures name the
# same models in the same colours; the GPT pair take blue and green.
FILLS = {
    "q38":   ("#8fd3cd", "#10605a"),   # pale teal / deep teal
    "luna":  ("#a8cdf0", "#2f6fbf"),   # light blue / blue
    "terra": ("#a8d878", "#4a9e2f"),   # light green / green
    "fable": ("#e8a8c8", "#a8306a"),   # pink; single arm only, dark used for its ring
}
FABLE_DARK = FILLS["fable"][1]         # the rule at Fable 5's score, and its ring

TITLE = ("Manager vs single call, four models "
         "— LCB-100, 5 passes, 128k max tokens, reasoning ON")

CAPTION = ("\\textbf{Manager vs.\\ single call.} 128k $\\times$ 5 passes, "
           "reasoning on.")

BAR_W = 0.34
YLIM = 168          # headroom for four tiers over the tallest bar: the within-model
                    # bracket, then one spanning bracket per manager arm out to Fable 5

# The legend runs UNDER the axes here, not down a right-hand column as in the sibling
# charts, which buys the axes the whole text width -- the three cross-model brackets are
# nearly that wide and were cramped in the 0.65 the column left them. It costs height, so
# it is one row. FIGSIZE stays put -- a taller canvas would trip \panelplot's height cap
# and rescale the type (see the note on PAGE_SCALE in plot_16k_reason_off_5_pass.py).
M4 = dict(MARGINS, right=0.985, bottom=0.145)
LEG_Y = 0.015       # legend box bottom, figure fraction

# Annotation tiers are sized in POINTS and converted, so the stack stays legible if YLIM
# or the margins move: a gap fixed in data units silently tightens as YLIM grows.
AX_H_PT = FIGSIZE[1] * 72 * (M4["top"] - M4["bottom"])
_u = lambda pt: pt * YLIM / AX_H_PT
STAR_H = _u(FS_STAR + 4)        # the within-model Δ label, plus its 3pt offset
TIER_GAP = _u(FS_NOTE + 10)     # one cross-model bracket, its label and the air over it


def notes(stats):
    """The figure's caption, trimmed to what a reader needs to read the chart.

    Anything the marks already say (which models are n.s., that the x axis is
    categorical) or that belongs to the run rather than the figure (why Fable 5 has no
    manager arm) lives in the body text, not here.
    """
    tested = [s for s in stats if s["has_mgr"]]
    # Only the p values are given: every Δ is already printed on its bracket.
    gaps = ", ".join(f"{s['label']} {fmt_p_num(s['vs_p_holm'], 2, s['vs_floored'])}"
                     for s in tested)
    # ... and the floor is only worth explaining when a printed p actually hits it.
    floor = ' "<" is the permutation floor.' if any(s["vs_floored"] for s in tested) else ""
    return [
        "Bars are pass@1 on the same 100 problems, the line through each the 95% CI across "
        "the 5 passes (t, df = 4). \"Single call\" is one call with no tools and no loop; "
        "Fable 5 ran single-only, so it has one bar.",
        f"Short brackets are with manager − single call, long brackets the same arm against "
        f"Fable 5. Both are paired sign-flip permutation tests, unit = problem (n = 100), "
        f"Holm-corrected within each family of 3: * p < .05, ** p < .01, *** p < .001.{floor}"
        f" The three within-model Δ all clear p < 1e-4; against Fable 5, p = {gaps}.",
        "Every arm is at a 128k cap and re-scored on the corrected evaluator (§3.3); "
        "Qwen3.8-27B's single arm is the 128k cap-matched replay of a 250k generation, "
        "which §3.2 describes and §2.2 costs out.",
    ]


# --------------------------------------------------------------------------- data

def load_arm(pattern):
    """-> (qids, passed[P, N] bool). One file per pass, same 100 ids in the same order."""
    qids, rows = None, []
    for p in PASSES:
        recs = json.load(open(pattern % p))["lcb"]["records"]
        ids = [r["question_id"] for r in recs]
        if qids is None:
            qids = ids
        assert ids == qids, f"{pattern % p}: id drift"
        rows.append([bool(r["passed"]) for r in recs])
    return qids, np.array(rows, float)


def compute():
    stats, qids0 = [], None
    for key, label, s_pat, m_pat in MODELS:
        qids, s = load_arm(s_pat)
        if qids0 is None:
            qids0 = qids
        assert qids == qids0, f"{key}: different problem set"
        st = dict(key=key, label=label, has_mgr=m_pat is not None,
                  single=100 * s.mean(), single_scores=100 * s.mean(axis=1),
                  single_ci=pass_ci(100 * s.mean(axis=1)),
                  single_prob=s.mean(axis=0))
        if key == "q38":
            _, g = load_arm(Q38_ASGEN)
            st["single_asgen"] = 100 * g.mean()
        if m_pat is not None:
            _, m = load_arm(m_pat)
            st.update(multi=100 * m.mean(), multi_scores=100 * m.mean(axis=1),
                      multi_ci=pass_ci(100 * m.mean(axis=1)),
                      multi_prob=m.mean(axis=0),
                      delta=100 * (m.mean() - s.mean()))
            # paired on the problem: mean over passes per problem, then sign-flip
            d = m.mean(axis=0) - s.mean(axis=0)
            _, p, floored = perm_sign_p(d)
            st.update(p_raw=p, floored=floored)
        stats.append(st)
    tested = [s for s in stats if s["has_mgr"]]
    for s, p in zip(tested, holm([s["p_raw"] for s in tested])):
        s["p_holm"] = p

    # Second family: each manager arm against Fable 5's single call, same 100 problems and
    # the same paired test. Held to its own Holm family of 3 rather than pooled with the
    # within-model tests above -- see the module docstring.
    ref = next(s for s in stats if s["key"] == "fable")["single_prob"]
    for s in tested:
        d = s["multi_prob"] - ref
        obs, p, floored = perm_sign_p(d)
        s.update(vs_fable=100 * obs, vs_p_raw=p, vs_floored=floored)
    for s, p in zip(tested, holm([s["vs_p_raw"] for s in tested])):
        s["vs_p_holm"] = p
    return stats


# --------------------------------------------------------------------------- plot

def draw(stats, kind, theme="light", save=None):
    t = THEMES[theme]
    apply_theme(t)
    bars = kind == "bars"
    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(**M4)
    ax.set(xlim=(-0.6, len(stats) - 0.4), ylim=(0, YLIM))
    ax.set_ylabel("Accuracy (pass@1, %)", fontsize=FS_BODY, color=t["ink2"])
    ax.xaxis.grid(False)
    ax.yaxis.grid(True)
    ax.set_axisbelow(True)
    ax.set_xticks(range(len(stats)), [s["label"] for s in stats], fontsize=FS_BODY)
    ax.tick_params(length=0, labelsize=FS_BODY)
    for spine in ("left", "bottom"):
        ax.spines[spine].set_color(t["axis"])

    # Fable 5's score as a rule across the panel. The cross-model brackets carry the test;
    # the rule is what makes a 1-10 pp residual read as above or below the ceiling at a
    # glance, three column positions away from the bar it belongs to.
    fable = next(s for s in stats if s["key"] == "fable")["single"]
    ax.axhline(fable, ls=(0, (6, 4)), lw=1.6, color=FABLE_DARK, alpha=0.85, zorder=2)

    arm_x, tops = {}, []      # (i, arm) -> x, and each within-model bracket's label top
    for i, s in enumerate(stats):
        light, dark = FILLS[s["key"]]
        arms = [("single", light, -BAR_W / 2 if s["has_mgr"] else 0.0)]
        if s["has_mgr"]:
            arms.append(("multi", dark, BAR_W / 2))
        for arm, fill, dx in arms:
            y, lo, hi = s[arm], *s[f"{arm}_ci"]
            # In dots mode the pair is spread WIDER than the bars, not narrower: two
            # markers a bar-width apart overlap once each carries a CI whisker and a value
            # label, and Terra's arms are only 8 points apart to begin with.
            x = i + (dx if bars else dx * 1.5)
            arm_x[(i, arm)] = x
            if bars:
                ax.bar(x, y, BAR_W, color=fill, edgecolor=ring(fill, theme),
                       linewidth=EDGE_LW, zorder=3)
            else:
                ax.scatter([x], [y], s=DOT, color=fill, zorder=4,
                           edgecolor=ring(fill, theme), linewidth=EDGE_LW)
            # 95% CI across the five passes -- the error bar the request is about
            ax.plot([x, x], [lo, hi], color=ring(fill, theme), lw=CI_LW, zorder=5,
                    solid_capstyle="round")
            for cap in (lo, hi):
                ax.plot([x - 0.045, x + 0.045], [cap, cap], color=ring(fill, theme),
                        lw=CI_LW, zorder=5)
            # Labels go vertically, not sideways: single below its lower CI cap, manager
            # above its upper one. Offsetting them left/right instead puts one group's
            # right-hand label into the next group's left-hand one -- the gap between
            # adjacent columns is narrower than two labels wide.
            below = arm == "single" and s["has_mgr"]
            # The upper labels get a surface-coloured backing: the Fable-5 rule crosses the
            # ones that land near it, and a bare label reads as struck through. The lower
            # ones sit on their own bar, where a patch would just be a white box.
            ax.annotate(f"{y:.1f}", xy=(x, lo if below else hi),
                        xytext=(0, -15 if below else 8), textcoords="offset points",
                        ha="center", va="bottom", fontsize=FS_BODY, color=t["ink"],
                        zorder=6, bbox=None if below else dict(
                            facecolor=t["surface"], edgecolor="none",
                            boxstyle="square,pad=0.12"))
        if s["has_mgr"]:
            # bracket carrying the paired test, clear of both CI caps and both labels
            top = max(s["single_ci"][1], s["multi_ci"][1]) + 11
            xl, xr = i - BAR_W / 2, i + BAR_W / 2
            if not bars:
                xl, xr = i - BAR_W * 1.5 / 2, i + BAR_W * 1.5 / 2
            ax.plot([xl, xl, xr, xr], [top - 1.6, top, top, top - 1.6],
                    color=t["muted"], lw=1.0, zorder=4)
            lbl = f"{s['delta']:+.1f}  {stars(s['p_holm'])}"
            ax.annotate(lbl, xy=((xl + xr) / 2, top), xytext=(0, 3),
                        textcoords="offset points", ha="center", va="bottom",
                        fontsize=FS_STAR, color=t["ink2"])
            tops.append(top + STAR_H)

    # ---- cross-model brackets: each manager arm out to Fable 5's mark, one tier each.
    # Nearest span lowest, so the three nest instead of crossing. Their right ends are
    # fanned across Fable 5's bar rather than stacked on one x, which would put three
    # stubs on the same vertical line.
    fable_i = next(i for i, s in enumerate(stats) if s["key"] == "fable")
    tested = [(i, s) for i, s in enumerate(stats) if s["has_mgr"]]
    y = max(tops) + TIER_GAP
    for rank, (i, s) in enumerate(reversed(tested)):    # right to left = nearest first
        xl = arm_x[(i, "multi")]
        xr = arm_x[(fable_i, "single")] + (rank - 1) * 0.11
        ax.plot([xl, xl, xr, xr], [y - 2.6, y, y, y - 2.6],
                color=t["muted"], lw=1.0, zorder=4)
        mark = stars(s["vs_p_holm"]) or "n.s."
        # Named "<model> manager", not just "<model>": the bracket starts at the manager
        # bar, and a bare model name reads as the whole model rather than one of its arms.
        ax.annotate(f"{s['label']} manager {s['vs_fable']:+.1f} {mark}",
                    xy=((xl + xr) / 2, y), xytext=(0, 2), textcoords="offset points",
                    ha="center", va="bottom", fontsize=FS_NOTE,
                    color=t["ink2"] if s["vs_p_holm"] < ALPHA else t["muted"])
        y += TIER_GAP

    # No model legend: under the axes it would sit directly beneath the x ticks and repeat
    # them word for word. What the ticks do NOT say is which fill is which arm, so the row
    # is the condition key instead -- neutral swatches, because the convention being named
    # is the lightness step, which every hue on the chart makes in its own colour.
    def swatch(colour):
        return Line2D([], [], marker="o", ls="", ms=12, color=colour,
                      markeredgecolor=ring(colour, theme), markeredgewidth=EDGE_LW)

    # The pair must keep the light -> dark order on BOTH surfaces, since that ordering is
    # the whole content of the key; a theme swap that inverts it would say the opposite.
    pale, deep = ("#d5d4cd", "#6f6d67") if theme == "light" else ("#b8b6ae", "#5e5c57")
    key = [(swatch(pale), "single call"),
           (swatch(deep), "with manager"),
           (Line2D([], [], ls=(0, (6, 4)), lw=1.6, color=FABLE_DARK),
            f"Fable 5 single call, {fable:.1f}%")]

    fig.suptitle(wrap_title(TITLE), x=M4["left"], ha="left", y=0.99, va="top",
                 fontsize=FS_TITLE, fontweight="bold", color=t["ink"], linespacing=1.25)
    leg = fig.legend([h for h, _ in key], [n for _, n in key], loc="lower center",
                     bbox_to_anchor=(0.5, LEG_Y), ncol=len(key), frameon=False,
                     fontsize=FS_SUB, labelcolor=t["ink2"], handletextpad=0.7,
                     handlelength=2.2, columnspacing=2.8)
    fig.add_artist(leg)
    if save:
        fig.savefig(save)
        print("wrote", save)
    return fig


def main():
    stats = compute()
    hdr = (f"{'model':16} {'single':>16} {'manager':>16} {'delta':>7} {'Holm p':>10}"
           f" {'vs Fable':>9} {'Holm p':>10}")
    print(hdr)
    print("-" * len(hdr))
    for s in stats:
        sci = f"{s['single']:5.1f} [{s['single_ci'][0]:4.1f},{s['single_ci'][1]:5.1f}]"
        if s["has_mgr"]:
            mci = f"{s['multi']:5.1f} [{s['multi_ci'][0]:4.1f},{s['multi_ci'][1]:5.1f}]"
            print(f"{s['label']:16} {sci:>16} {mci:>16} {s['delta']:+7.1f} "
                  f"{fmt_p_num(s['p_holm'], 2, s['floored']):>10} {s['vs_fable']:+9.1f} "
                  f"{fmt_p_num(s['vs_p_holm'], 2, s['vs_floored']):>10}")
        else:
            print(f"{s['label']:16} {sci:>16} {'- (single only)':>16} {'-':>7} {'-':>10} "
                  f"{'reference':>9} {'-':>10}")
    q38 = next(s for s in stats if s["key"] == "q38")
    print(f"\nQwen3.8-27B single as generated at 250k: {q38['single_asgen']:.1f} "
          f"({q38['single_asgen'] - q38['single']:+.1f} vs the 128k replay the chart uses)")

    os.makedirs(PLOTS, exist_ok=True)
    for theme in ("light", "dark"):
        for kind in ("dots", "bars"):
            suffix = "_bars" if kind == "bars" else ""
            draw(stats, kind, theme,
                 save=os.path.join(PLOTS, f"{slug(TITLE)}{suffix}_{theme}.png"))


if __name__ == "__main__":
    main()
