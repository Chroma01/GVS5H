#!/usr/bin/env python3
"""Single call vs manager across model scale, LCB-100 x 5 passes at 16k, reasoning OFF.

"Single call" is one API call with no tools and no loop -- the raw model, not an agent.
On disk that arm is still named `*_single.json`, so the code keys stay `single`.

Dots are pass@1 per condition with 95% CIs across the passes; brackets carry the
per-model paired test. Tukey HSD across models is in the per-model blocks (group
letters) and, pair by pair, in the caption make_figures_tex.py builds.

    uv run --with matplotlib --with numpy --with scipy python escalation/run_bench_script/plot_16k_reason_off_5_pass.py

Writes plots/<title-slug>_{light,dark}.png.
"""
import json
import math
import os
import re

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.legend_handler import HandlerTuple

HERE = os.path.dirname(os.path.abspath(__file__))
ESC = os.path.dirname(HERE)             # escalation/, one level up from run_bench_script/
RESULTS = os.path.join(ESC, "runs/models-lcb-5pass/results")
PLOTS = os.path.join(ESC, "plots")      # every chart script writes here
PASSES = [1, 2, 3, 4, 5]

# x = total parameters, log scale. nem (stub files) and opus (no manager arm) excluded.
# Qwen sizes are in their names; Minimax-M3 and Kimi-K3 per user (2026-07-29).
MODELS = {
    "q9": ("Qwen3.5-9B", 9e9),
    "q35": ("Qwen3.6-35B", 35e9),
    "mm3": ("Minimax-M3", 428e9),
    "kimi": ("Kimi-K3", 2.8e12),
}

# hue = model, fill lightness = condition (light = single, dark = multiagent).
# Hexes eyeballed off the reference chart, not sampled from it.
FILLS = {
    "q9": ("#b8aee8", "#3a35a5"),      # lavender / indigo
    "q35": ("#eda27f", "#a63f2e"),     # salmon / brick
    "mm3": ("#a8cdf0", "#2f6fbf"),     # light blue / blue
    "kimi": ("#a8d878", "#4a9e2f"),    # light green / green
}

TITLE = ("Manager vs single call across model scale "
         "\u2014 LCB-100, 5 passes, 16k max tokens, reasoning OFF")

# The figure's LaTeX caption: a one-line title, then the notes that used to sit in
# the chart's right column, where they could only be set at ~5pt. make_figures_tex.py
# writes both into paper/fig-<slug>.tex and paper.tex \inputs it, so nothing here is
# ever retyped by hand and a note that quotes a number cannot drift from the run.
CAPTION = "\\textbf{Reasoning off:} 16k $\\times$ 5 passes."


def notes(stats):
    return [
        "Fill: light = single call (one call, no tools), dark = with manager. Marks in "
        "(a) and bars in (b) are pass@1; the line through each is the 95% CI across the "
        "5 passes (t, df = 4) \u2014 run-to-run spread on these same 100 problems.",
        "\u0394 and p under each model: paired sign-flip permutation test, unit = problem "
        "(n = 100), Holm-corrected across the 4 models; \"<\" is the permutation floor. "
        "The bracket links a model's two conditions, and the mark above it grades that "
        "same p: * p < .05, ** p < .01, *** p < .001, n.s. otherwise.",
        "Each block under the axis heads with the model's size, not its name \u2014 9B and "
        "35B are too close on the log axis of (a) for a name to fit \u2014 and the legend maps "
        "fill colour to name. The curves in (a) connect each condition's own 4 points "
        "(monotone cubic): they interpolate, they are not fits.",
        f"Tukey groups: models sharing a letter have indistinguishable \u0394 (HSD, "
        f"\u03b1 {ALPHA}); HSD ignores that all models saw the same 100 problems, so it is "
        "conservative.",
    ]


N_PERM = 200_000
N_BOOT = 20_000
SEED = 42
ALPHA = 0.05
DOT = 150           # marker area in points^2; on the page that is a 6.9pt disc, since
                    # PAGE_SCALE halves every length. The value-label offsets and the
                    # half-and-half marker in the reasoning-on chart derive from it.
EDGE_LW = 1.6       # hairline ring on each dot, in a darker step of its own hue
CI_LW = 1.6         # 95% CI bar and its T caps

# Type scale. Every size below is the size it should READ as on the page, times the
# ratio that makes it read that way, times PAGE_SCALE.
#
# Read-as: paper.tex is an 11pt article, so its own sizes are \large 12pt for an x.x
# subsection head, \normalsize 10.95pt for body, \small 10pt, \footnotesize 9pt.
#
# Ratio: equal nominal sizes do not read equal across two faces. What the eye compares
# in mixed-case text is x-height, and the paper's Latin Modern has far less of it than
# the charts' DejaVu Sans -- 0.4306 em regular and 0.4444 bold (lmr10.afm, lmbx10.afm)
# against 0.5469 for both DejaVu weights. Set nominally equal, chart text stands ~23%
# taller through the lowercase than the prose beside it.
#
# PAGE_SCALE: each panel is drawn at \linewidth = 6.5in and the canvas below is exactly
# twice that, so a point here lands on the page at pt / PAGE_SCALE. Two things have to
# hold for that. savefig must not crop -- a "tight" bbox trims each chart by a different
# amount and so gives each its own scale -- and \panelplot's height cap must stay above
# the panel's own height, or the figure is scaled to fit it and takes the type with it.
#
# TYPE_SCALE: x-height parity makes chart type *measure* the same as the prose, but it
# still reads a shade larger beside it -- DejaVu is the wider face, with open counters
# and an even stroke where Latin Modern thins and tapers, so the same x-height carries
# more ink across a line. The whole scale is taken down a notch to settle that; one
# knob, so the sizes below stay readable as the paper sizes they are matched to.
PAGE_SCALE = 2.0
TYPE_SCALE = 0.92
X_REG = 0.4306 / 0.5469 * TYPE_SCALE    # Latin Modern / DejaVu x-height, regular
X_BOLD = 0.4444 / 0.5469 * TYPE_SCALE   # ... and bold
FS_TITLE = 12.0 * X_BOLD * PAGE_SCALE   # reads as \large, the x.x subsection head
FS_BODY = 10.95 * X_REG * PAGE_SCALE    # \normalsize: ticks, value labels, axis
                                        # captions
FS_SUB = 10.0 * X_REG * PAGE_SCALE      # \small: model legend
FS_NOTE = 9.0 * X_REG * PAGE_SCALE      # \footnotesize: the per-model blocks,
                                        # trend legend
FS_HEAD = 9.0 * X_BOLD * PAGE_SCALE     # ... and their bold head row
FS_STAR = 12.0 * X_REG * PAGE_SCALE     # significance stars

# 6.5 x 3.1in on the page: the full text width, and short enough that two panels plus
# a caption carrying the notes fit one float page (2 x 3.1 + ~2.8in of caption = 9in).
# LaTeX does not warn when a float page overruns -- the caption just slides under the
# page number -- so this height and \panelplot's cap are checked by eye on the PDF.
# Real 9-11pt type is expensive in a 6.5in-wide chart, so the chart carries only what
# has to sit next to a mark; the note block, and the pairwise Tukey p values that went
# with it, are in the figure's LaTeX caption now.
FIGSIZE = (6.5 * PAGE_SCALE, 3.1 * PAGE_SCALE)
MARGINS = dict(left=0.085, right=0.737, top=0.89, bottom=0.30)
PANEL_X = 0.762         # left edge of the right column, figure fraction. Set so the
                        # widest legend line -- the trend legend's "+NN pts, 9B -> 2.8T"
                        # -- ends about 2% of the canvas short of the right edge; the
                        # axes take the rest. Checked by measuring ink in the PNGs, so
                        # a longer label than today's needs this pulled back left.
PANEL_TOP = 0.89        # its top, level with the top of the axes
ROW_0 = 28              # per-model block: first row's drop below the axis
ROW_PITCH = 1.35        # line pitch in that block, times the row's own size

THEMES = {
    "light": dict(
        surface="#fcfcfb", ink="#0b0b0b", ink2="#52514e", muted="#898781",
        grid="#e1e0d9", axis="#c3c2b7",
    ),
    "dark": dict(
        surface="#1a1a19", ink="#ffffff", ink2="#c3c2b7", muted="#898781",
        grid="#2c2c2a", axis="#383835",
    ),
}


def apply_theme(t):
    plt.rcParams.update({
        "figure.facecolor": t["surface"], "axes.facecolor": t["surface"],
        "savefig.facecolor": t["surface"],
        "text.color": t["ink"], "axes.labelcolor": t["ink2"],
        "xtick.color": t["ink2"], "ytick.color": t["muted"],
        "axes.edgecolor": t["axis"], "grid.color": t["grid"],
        "axes.titlecolor": t["ink"],
        "font.family": "sans-serif", "font.size": 10,
        "mathtext.default": "regular", "mathtext.fontset": "dejavusans",
        "axes.spines.top": False, "axes.spines.right": False,
        "axes.grid": True, "grid.linewidth": 0.8,
        "figure.dpi": 130,
    })


# --------------------------------------------------------------------------- data

def load_arm(model, arm):
    """-> (qids, passed[P, N] bool, nonempty[P, N] bool)

    Reads the *.regraded.json twins, not the originals: LiveCodeBench's stdin mock scored
    any solution that read through sys.stdin.buffer wrong (escalation/regrade.py, paper
    S3.3), and it did not hit the arms evenly. Point this back at the plain .json and the
    chart silently reverts to the buggy grader.
    """
    qids, passed, nonempty = None, [], []
    for p in PASSES:
        fn = f"{RESULTS}/{model}_{arm}_p{p}.regraded.json"
        if not os.path.exists(fn):
            continue
        lcb = json.load(open(fn)).get("lcb")
        recs = lcb.get("records") if isinstance(lcb, dict) else None
        if not recs:                       # void pass (0 usable completions) or stub file
            continue
        ids = [r["question_id"] for r in recs]
        if qids is None:
            qids = ids
        assert ids == qids, f"{fn}: question_id order differs"
        passed.append([bool(r["passed"]) for r in recs])
        nonempty.append([bool((r.get("code") or "").strip()) for r in recs])
    if not passed:
        return None
    return qids, np.array(passed), np.array(nonempty)


# -------------------------------------------------------------------------- tests

def perm_sign_p(d, n_perm=N_PERM, seed=SEED):
    """Two-sided paired sign-flip permutation test. -> (mean, p, hit_floor)."""
    d = np.asarray(d, float)
    obs = d.mean()
    rng = np.random.default_rng(seed)
    null = (rng.choice([-1.0, 1.0], size=(n_perm, d.size)) * d).mean(axis=1)
    b = int((np.abs(null) >= abs(obs) - 1e-12).sum())
    return obs, (b + 1) / (n_perm + 1), b == 0


def boot_ci(x, n_boot=N_BOOT, seed=SEED, level=0.95):
    """Cluster bootstrap over problems (not trials)."""
    x = np.asarray(x, float)
    rng = np.random.default_rng(seed + 1)
    means = x[rng.integers(0, x.size, size=(n_boot, x.size))].mean(axis=1)
    return tuple(np.percentile(means, [(1 - level) / 2 * 100, (1 + level) / 2 * 100]))


def pass_ci(scores, level=0.95):
    """95% CI across the passes themselves: mean +- t(df) * SE, df = n_passes - 1.

    Answers "rerun these same problems, what range?" -- run-to-run spread only.
    It is NOT the interval for generalising to other problems; that one is
    boot_ci() over problems, which is roughly twice as wide.
    """
    from scipy.stats import t as t_dist
    scores = np.asarray(scores, float)
    half = t_dist.ppf((1 + level) / 2, scores.size - 1) * scores.std(ddof=1) / math.sqrt(scores.size)
    return scores.mean() - half, scores.mean() + half


def holm(pvals):
    order = sorted(range(len(pvals)), key=lambda i: pvals[i])
    out, running = [0.0] * len(pvals), 0.0
    for rank, i in enumerate(order):
        running = max(running, (len(pvals) - rank) * pvals[i])
        out[i] = min(1.0, running)
    return out


def compute():
    stats = []
    for key, (label, params) in MODELS.items():
        s, m = load_arm(key, "single"), load_arm(key, "multiagent")
        assert s and m, f"{key}: missing an arm"
        assert s[0] == m[0], f"{key}: arms cover different problems"
        sp, mp = s[1], m[1]
        s_prob, m_prob = sp.mean(axis=0), mp.mean(axis=0)   # per-problem rate, 5 passes
        delta, p_perm, floored = perm_sign_p(m_prob - s_prob)
        stats.append(dict(
            key=key, label=label, params=params, d=100 * (m_prob - s_prob),
            single=100 * sp.mean(), single_ci=pass_ci(100 * sp.mean(axis=1)),
            multi=100 * mp.mean(), multi_ci=pass_ci(100 * mp.mean(axis=1)),
            delta=100 * delta, delta_ci=tuple(100 * v for v in boot_ci(m_prob - s_prob)),
            p_perm=p_perm, floored=floored,
            ne_single=100 * s[2].mean(), ne_multi=100 * m[2].mean(),
        ))
    for st, ph in zip(stats, holm([st["p_perm"] for st in stats])):
        st["p_holm"] = ph
        st["sig"] = ph < ALPHA
    return stats


def stars(p):
    """Conventional tiers, for the marks above each p chip."""
    return "***" if p < 1e-3 else "**" if p < 1e-2 else "*" if p < ALPHA else ""


def fmt_p_num(p, sig=1, floored=False):
    """p as a plain decimal down to 0.001, then as m x 10^e mathtext."""
    prefix = "<" if floored else ""
    if p >= 1e-3:
        return prefix + f"%.{sig}g" % p
    mantissa, exponent = (f"%.{sig - 1}e" % p).split("e")
    return prefix + rf"${mantissa}\times10^{{{int(exponent)}}}$"


def wrap_title(text):
    """Break the title at its em dash, into subject and condition.

    At FS_TITLE the one-liner is wider than the canvas, and bbox_inches="tight"
    grows the figure to fit it -- which shrinks everything else once paper.tex
    scales the result to \\linewidth. TITLE itself stays one line: slug() turns it
    into the filename.
    """
    return text.replace("— ", "—\n")


def slug(text):
    """Title -> filename stem, so the two never drift apart."""
    return re.sub(r"_+", "_", re.sub(r"[^a-z0-9-]+", "_",
                                     text.lower().replace("\u2014", " "))).strip("_")


def fmt_params(n):
    return f"{n / 1e12:g}T" if n >= 1e12 else f"{n / 1e9:g}B"


def head_label(st):
    """Head row of a per-model block: the size, not the name.

    At 9pt "Qwen3.5-9B" is wider than the gap between two adjacent models in every
    one of these charts, and the legend carries colour -> name at full body size.
    Opus-5 has no public parameter count, so it heads with its name instead -- the
    dot charts park it at a placeholder x, which is no basis for printing a size.
    """
    return st["label"] if st["key"] == "opus" else fmt_params(st["params"])


def rgb(hexcolor):
    return [int(hexcolor[i:i + 2], 16) for i in (1, 3, 5)]


def ring(hexcolor, theme):
    """Hairline edge: a darker step of the fill's own hue, lighter if the fill is
    already dark on a dark surface."""
    r, g, b = rgb(hexcolor)
    lum = (0.299 * r + 0.587 * g + 0.114 * b) / 255
    f = 1 + (1 - 0.72) if (theme == "dark" and lum < 0.4) else 0.72
    return "#%02x%02x%02x" % tuple(min(255, int(c * f)) for c in (r, g, b))


def tint(hexcolor, theme, f=0.16):
    """A pale wash of the hue over the surface, for a label chip."""
    sr, sg, sb = rgb(THEMES[theme]["surface"])
    r, g, b = rgb(hexcolor)
    return "#%02x%02x%02x" % tuple(
        int(s + (c - s) * f) for s, c in ((sr, r), (sg, g), (sb, b)))


# ------------------------------------------------------------------ side panel

def _panel_height(fig, artist):
    """Drawn height of an artist in figure fractions. Needs a live renderer."""
    fig.canvas.draw()
    return artist.get_window_extent(fig.canvas.get_renderer()).transformed(
        fig.transFigure.inverted()).height


def model_block(ax, x, rows):
    """The name / size / Δ / p / Tukey stack under the axis at x.

    Pitch follows each row's own size, so a block that mixes head and fine print
    needs no hand-tuned offsets. -> total drop in points, for the axis caption.
    """
    y = ROW_0
    for text, size, weight, col in rows:
        ax.annotate(text, xy=(x, 0), xycoords=("data", "axes fraction"),
                    xytext=(0, -y), textcoords="offset points",
                    ha="center", va="top", fontsize=size, fontweight=weight, color=col)
        y += ROW_PITCH * size
    return y


def side_panel(fig, t, swatches, names, trend, trend_kw=None, panel_x=None):
    """Model legend over condition legend, down the column right of the axes.

    The first block's height is measured rather than assumed: the model list is 4
    entries here and 4 elsewhere but the labels wrap differently, so a fixed y for
    the block below would collide on the tall ones and float on the short ones.

    panel_x moves the column's left edge for a chart whose labels are longer than
    PANEL_X was set for; that chart owes the width back through its right margin.
    """
    x = PANEL_X if panel_x is None else panel_x
    gap = 0.04
    leg1 = fig.legend(swatches, names, loc="upper left",
                      bbox_to_anchor=(x, PANEL_TOP), ncol=1, frameon=False,
                      fontsize=FS_SUB, labelcolor=t["ink2"],
                      handler_map={tuple: HandlerTuple(ndivide=None, pad=0.6)},
                      handletextpad=0.7)
    fig.add_artist(leg1)
    y = PANEL_TOP - _panel_height(fig, leg1) - gap

    leg2 = fig.legend(handles=trend, loc="upper left", bbox_to_anchor=(x, y),
                      ncol=1, frameon=False, fontsize=FS_NOTE, labelcolor=t["ink2"],
                      **(trend_kw or {}))
    fig.add_artist(leg2)


def below_panel(fig, t, swatches, names, y, ncol, trend=None, trend_kw=None):
    """The same two blocks as side_panel, stacked under the axes instead of beside them.

    A chart that uses this has no right column to leave room for, so it pushes its right
    margin out to the canvas edge and pays for the legend in bottom margin instead. Worth
    it where the marks are wide -- bars and a scatter both read better across the full
    text width than they do at three quarters of it.

    `y` is the top of the legend in figure fractions, which the caller sets under whatever
    it already draws below the axis. The second block's y is measured off the first, as in
    side_panel: how many rows a `ncol`-wide legend wraps to is not known up here.
    """
    leg1 = fig.legend(swatches, names, loc="upper center", bbox_to_anchor=(0.5, y),
                      ncol=ncol, frameon=False, fontsize=FS_SUB, labelcolor=t["ink2"],
                      handler_map={tuple: HandlerTuple(ndivide=None, pad=0.6)},
                      handletextpad=0.7, columnspacing=2.2)
    fig.add_artist(leg1)
    if not trend:
        return
    leg2 = fig.legend(handles=trend, loc="upper center",
                      bbox_to_anchor=(0.5, y - _panel_height(fig, leg1) - 0.02),
                      ncol=len(trend), frameon=False, fontsize=FS_NOTE,
                      labelcolor=t["ink2"], **(trend_kw or {}))
    fig.add_artist(leg2)


def tukey_sentence(stats, pmat):
    """The 6 pairwise comparisons as one line of caption prose.

    They used to be an inset table in the chart. At 9pt the labels alone are 1.9in
    wide, a third of the panel, for numbers no mark depends on -- the group letters
    under each model already carry the grouping. The caption is the cheaper home.
    """
    parts = []
    for i in range(len(stats)):
        for j in range(i + 1, len(stats)):
            p = pmat[i][j]
            # named the way the blocks under the axis name them, and short enough
            # that all 6 comparisons stay on one caption line
            parts.append(f"{head_label(stats[i])} vs {head_label(stats[j])} "
                         f"{fmt_p_num(p, 2)}{'' if p < ALPHA else ' n.s.'}")
    joined = "; ".join(parts)
    return "Pairwise Tukey p: " + joined + ("" if joined.endswith(".") else ".")


# ----------------------------------------------------------------- cross-model

def tukey(stats, alpha=ALPHA):
    """Tukey HSD across models on the per-problem delta. -> (pvalue matrix, letters).

    Caveat: HSD assumes independent groups, but every model saw the SAME 100
    problems, so the groups are positively correlated. That inflates the pooled
    SE relative to a paired analysis, making these p-values conservative.
    """
    from scipy.stats import tukey_hsd
    res = tukey_hsd(*[st["d"] for st in stats])
    p = res.pvalue
    n = len(stats)
    means = [st["delta"] for st in stats]

    nonsig = {(i, j) for i in range(n) for j in range(i + 1, n) if p[i][j] > alpha}
    cliques = []
    for mask in range(1, 1 << n):
        members = [i for i in range(n) if mask >> i & 1]
        if all((a, b) in nonsig for a in members for b in members if a < b):
            cliques.append(set(members))

    # cover every non-significant pair (and every model) with as few cliques as possible
    edges, seen, chosen = set(nonsig), set(), []
    while edges or len(seen) < n:
        def score(c):
            return (sum((a, b) in edges for a in c for b in c if a < b), len(c - seen))
        best = max(cliques, key=score)
        if score(best) == (0, 0):
            break
        chosen.append(best)
        edges -= {(a, b) for a in best for b in best if a < b}
        seen |= best
    chosen.sort(key=lambda c: -max(means[i] for i in c))

    letters = {i: "" for i in range(n)}
    for k, c in enumerate(chosen):
        for i in c:
            letters[i] += chr(ord("a") + k)
    return p, letters


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
    ax.set(xlim=(6e9, 4.2e12), ylim=(0, 88))
    ax.set_ylabel("Accuracy (pass@1, %)", fontsize=FS_BODY, color=t["ink2"])
    ax.xaxis.grid(False)
    ax.yaxis.grid(True)
    ax.set_axisbelow(True)
    ax.tick_params(length=0, labelsize=FS_BODY)
    for spine in ("left", "bottom"):
        ax.spines[spine].set_color(t["axis"])

    def y_offset(x, y, dy_points):
        """y shifted by dy_points of display space, back in data units."""
        px = ax.transData.transform((x, y))
        return ax.transData.inverted().transform(
            (px[0], px[1] + dy_points * fig.dpi / 72.0))[1]

    def x_offset(x, dx_points):
        """x shifted by dx_points of display space, back in data units."""
        px = ax.transData.transform((x, 0))
        return ax.transData.inverted().transform(
            (px[0] + dx_points * fig.dpi / 72.0, px[1]))[0]

    gap = math.sqrt(DOT / math.pi) + EDGE_LW / 2       # dot radius + half its ring, in points

    # ---- one curve per condition, through its own points (no extrapolation).
    # PCHIP rather than a natural cubic: it passes through every point without
    # the overshoot a cubic spline would invent between them.
    from scipy.interpolate import PchipInterpolator
    lx = np.log10([st["params"] for st in stats])
    span = np.linspace(lx.min(), lx.max(), 300)
    totals = {}
    for arm, style in (("single", "--"), ("multi", "-")):
        ys = [st[arm] for st in stats]
        totals[arm] = ys[-1] - ys[0]
        ax.plot(10 ** span, PchipInterpolator(lx, ys)(span), ls=style, lw=1.6,
                color=t["muted"], alpha=0.9, zorder=1)

    # ---- marks: both arms on the model's x, light fill = single, dark = multiagent.
    # Value labels go above the upper arm and below the lower one, clearing its CI cap:
    # models are 0.9in apart on the page here, and a label beside a dot would run into
    # the next one along.
    for st in stats:
        x = st["params"]
        fill = dict(zip(("single", "multi"), FILLS[st["key"]]))
        upper = "multi" if st["multi"] >= st["single"] else "single"
        for arm in ("single", "multi"):
            y = st[arm]
            lo, hi = st[f"{arm}_ci"]
            ax.scatter([x], [y], s=DOT, color=fill[arm], zorder=4,
                       edgecolor=ring(fill[arm], theme), linewidth=EDGE_LW)
            # bar runs the full interval on top of the dot: an interval narrower
            # than the marker (Qwen3.5-9b single is +-0.7 pp) stays visible
            ax.plot([x, x], [lo, hi], lw=CI_LW, color=t["ink"],
                    solid_capstyle="butt", zorder=5)
            for end in (lo, hi):
                ax.plot([x], [end], marker="_", ms=10, mew=CI_LW,
                        color=t["ink"], zorder=5)
            end, dy, va = (hi, 5, "bottom") if arm == upper else (lo, -5, "top")
            ax.annotate(f"{y:.1f}", xy=(x, end), xytext=(0, dy),
                        textcoords="offset points", ha="center", va=va,
                        fontsize=FS_BODY, color=t["ink"])

    # ---- per-model block under the axis: size, delta, raw p -> Holm p, Tukey group.
    # The head row is the size, not the name: 9B and 35B are 0.6 of a decade apart,
    # about 1.2in here, and "Qwen3.5-9B" at 9pt is wider than that. The legend carries
    # colour -> name at full body size, where there is room for it.
    for i, st in enumerate(stats):
        col = t["ink2"] if st["sig"] else t["muted"]
        drop = model_block(ax, st["params"], [
            (head_label(st), FS_HEAD, "bold", t["ink"]),
            (f"\u0394 {st['delta']:+.1f} pp", FS_NOTE, "normal", col),
            (f"p {fmt_p_num(st['p_holm'], 1, st['floored'])}", FS_NOTE, "normal", col),
            (f"group {letters[i]}", FS_NOTE, "normal", t["ink2"])])

    ax.annotate("Total parameters, log scale", xy=(0.5, 0), xycoords="axes fraction",
                xytext=(0, -(drop + 12)), textcoords="offset points",
                ha="center", va="top", fontsize=FS_BODY, color=t["ink2"])

    # ---- "]" bracket linking each model's two dots, with the Holm p graded above it.
    # The p itself sits in the block under the axis, not on a chip here: at 10pt a chip
    # reading "p <2 x 10^-5" is an inch wide and the models are 0.9in apart.
    for st in stats:
        y1, y2 = st["single"], st["multi"]
        xa, xb = x_offset(st["params"], gap), x_offset(st["params"], gap + 8)
        col = t["ink2"] if st["sig"] else t["muted"]
        ax.plot([xa, xb, xb, xa], [y1, y1, y2, y2], lw=1.6, color=col,
                solid_joinstyle="miter", zorder=2)
        mark = stars(st["p_holm"])
        # anchored on the upper CI cap, high enough to clear the value label above it
        top = max(st["single_ci"][1], st["multi_ci"][1])
        ax.annotate(mark or "n.s.", xy=(st["params"], top), xytext=(0, 26),
                    textcoords="offset points", ha="center", va="bottom",
                    fontsize=FS_STAR if mark else FS_NOTE,
                    color=t["ink"] if mark else t["muted"], zorder=5)

    # ---- right column: one swatch pair per model, the two condition curves, Tukey
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
                    label=f"Single call\n{totals['single']:+.1f} pts, 9B \u2192 2.8T"),
             Line2D([], [], ls="-", lw=1.6, color=t["muted"],
                    label=f"With manager\n{totals['multi']:+.1f} pts, 9B \u2192 2.8T")]

    fig.suptitle(wrap_title(TITLE), x=MARGINS["left"], ha="left", y=0.99,
                 va="top", fontsize=FS_TITLE, fontweight="bold", color=t["ink"],
                 linespacing=1.25)
    side_panel(fig, t, pairs, names, trend,
               trend_kw=dict(handletextpad=0.7, handlelength=2.2))
    if save:
        # no bbox_inches="tight": the canvas is authored at exactly PAGE_SCALE x the
        # size it is printed, and a crop would scale the type differently per chart
        fig.savefig(save)
        print("wrote", save)
    return fig


def main():
    stats = compute()

    hdr = (f"{'model':13s} {'single':>7s} {'multi':>7s} {'delta':>7s} {'95% CI':>16s} "
           f"{'p_perm':>10s} {'p_holm':>9s}  nonempty")
    print(hdr)
    print("-" * len(hdr))
    for st in stats:
        pre = "<" if st["floored"] else " "
        print(f"{st['label']:13s} {st['single']:7.1f} {st['multi']:7.1f} {st['delta']:+7.1f}"
              f"   [{st['delta_ci'][0]:+5.1f},{st['delta_ci'][1]:+6.1f}]"
              f" {pre}{st['p_perm']:9.2e} {st['p_holm']:9.2e}"
              f"  {st['ne_single']:.1f} -> {st['ne_multi']:.1f}")

    pmat, letters = tukey(stats)
    names = [st["label"] for st in stats]
    print("\nTukey HSD across models on the per-problem delta:")
    for i in range(len(stats)):
        for j in range(i + 1, len(stats)):
            diff = stats[i]["d"] - stats[j]["d"]
            _, p_paired, _ = perm_sign_p(diff, n_perm=50_000)
            print(f"  {names[i]:12s} vs {names[j]:12s}  diff {diff.mean():+6.1f} pp"
                  f"   Tukey p {pmat[i][j]:7.4f}   paired-permutation p {p_paired:7.4f}")
    print("  letters: " + ", ".join(f"{names[i]}={letters[i]}" for i in range(len(stats))))

    os.makedirs(PLOTS, exist_ok=True)
    for theme in ("light", "dark"):
        draw(stats, letters, theme,
             save=os.path.join(PLOTS, f"{slug(TITLE)}_{theme}.png"))


if __name__ == "__main__":
    main()
