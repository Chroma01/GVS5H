#!/usr/bin/env python3
"""What one pass costs: the three manager arms against Fable 5, LCB-100 x 5 passes.

Dollars are tokens x rate, so the rates are the whole of the modelling assumption:

    Qwen3.8-27B   $0.35 / $2.75 per MTok   OpenRouter's hosted rate. There is NO
                                           first-party Alibaba price -- the weights
                                           shipped 2026-08-14 under Apache 2.0 and Qwen
                                           Cloud is still "coming soon" -- and the arms
                                           here ran on local vLLM, so this is what the
                                           same tokens would have cost rented, not what
                                           they cost us.
    GPT-5.6-Luna  $0.20 / $1.20 per MTok   OpenAI list, short-context tier.
    GPT-5.6-Terra $2 / $12 per MTok        OpenAI list, short-context tier.
    Fable 5       $10 / $50 per MTok       Anthropic list. Thinking bills as output, and
                                           on this model thinking is most of the output.

Two things the OpenAI price sheet offers and this does not take: the long-context tier
(2x the short rates, and it applies above 272k INPUT tokens -- the largest problem here
totals 88k of input across every call it made, so nothing reaches it), and the 10x
cached-input discount, which would need per-call cache-hit counts the transcripts do not
record. Ignoring the discount prices the GPT arms high, not low.

NO SINGLE-CALL ARM IS PRICED except Fable 5's, which is the reference and has no other.
Qwen3.8-27B's was generated at a 250,000-token output cap against the 128,000 every arm
here ran at -- the manager's own per-call maximum is exactly 128,000 across 3,235 calls,
and Anthropic hard-clamps Fable 5 to the same figure. 150 of its 500 calls ran past 128k
and 124 stopped dead on the 250k ceiling; those truncated calls alone are 59% of that
arm's bill. Pricing it beside these bars charges one arm for twice the output budget the
others were allowed. capmatch_q38.py replays the generations against 128k if the arm is
wanted back.

WHAT IS STILL NOT MATCHED IS THINKING DEPTH, and on a cost chart it is the caveat that
matters most, because thinking bills as output everywhere. The cap and the scaffold are
the same across these four; the effort knob is not. The Qwen chat template leaves
thinking on with no budget requested, bounded only by the 128k cap; Fable 5 is
adaptive-always-on at effort:high; and the two GPT-5.6 arms ran at OpenAI's DEFAULT
effort, because run_4models_1pass_reason_on.sh never sets ESCALATION_OPENAI_REASONING. A
manager pass emits 185k output tokens per problem on Qwen3.8-27B against 10.5k on Luna
and 7.9k on Terra, so part of what a cheap GPT bar reports is where that knob was left
rather than what the model costs to run this benchmark. Pin the effort and rerun to close
it.

Token counts come from runs/per_problem_tokens.json (see extract_tokens.py) and include
the calls that were retried and discarded -- those were generated and would be billed.

The y axis is linear dollars from zero, so the bars are in proportion to each other and
the manager surcharge reads as the height it is. The price of that is the bottom of the
range: Luna's single call ($0.41) and its manager arm ($1.50) are slivers against Fable
5's $61.11, and are read off their printed values and the per-arm table under the figure
rather than off the axis. It was a log axis until 2026-08-25 for exactly that reason.

The companion accuracy chart is plot_q38_vs_fable5_5_pass.py, on the same four arms and
the same 100 problems; this one answers what that accuracy cost.

    uv run --with matplotlib --with numpy --with scipy python \\
        escalation/run_bench_script/plot_cost_5_pass.py

Writes plots/<title-slug>_{light,dark}.png. The stats go in the LaTeX table that
make_figures_tex.py builds under the panel, not on the chart.
"""
import json
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

from plot_16k_reason_off_5_pass import (
    ALPHA, CI_LW, EDGE_LW, FIGSIZE, FS_BODY, FS_HEAD, FS_NOTE, FS_TITLE,
    MARGINS, PLOTS, THEMES,
    apply_theme, below_panel, boot_ci, fmt_p_num, holm, model_block, pass_ci,
    perm_sign_p, ring, slug, wrap_title,
)
# hue = model, lightness = condition (light = single, dark = with manager), the same
# convention every other chart uses. Declared here rather than imported from the accuracy
# chart beside this one: that figure draws manager arms only, so its FILLS has no light
# step to borrow.
FILLS = {
    "q38_single": "#8fd3cd", "q38_multi": "#10605a",       # pale / deep teal
    "luna_single": "#e3c98a", "luna_multi": "#9c6f12",     # pale / deep bronze
    "terra_single": "#a8cdf0", "terra_multi": "#2f6fbf",   # pale / deep blue
    "fable_single": "#e8a8c8",                             # pink; one arm, no dark twin
}

HERE = os.path.dirname(os.path.abspath(__file__))
ESC = os.path.dirname(HERE)
R4 = f"{ESC}/runs/4models-1pass-reason-on/results"
TOKENS = os.path.join(ESC, "runs/per_problem_tokens.json")
PASSES = [1, 2, 3, 4, 5]

# key -> (label, results pattern, ($/MTok in, $/MTok out))
# The patterns are the regraded twins, as in plot_q38_vs_fable5_5_pass.ARMS -- the cost
# per solved problem divides by the pass count, so it moves with the grader too.
# Qwen3.8-27B's single call is the 128k CAP-MATCHED replay, and its tokens are capped to
# match (CAP below). Its manager twin and every other bar here ran at 128k; pricing this
# one off the 250k generation would put a single arm on the chart with twice the output
# budget of the arm beside it, and the surcharge column would then be measuring budgets.
ARMS = {
    "q38_single": ("Qwen3.8-27B, single call",
                   f"{R4}/q38_single_p%d.cap128k.regraded.json", (0.35, 2.75)),
    "q38_multi": ("Qwen3.8-27B, with manager",
                  f"{R4}/q38_multiagent_p%d.regraded.json", (0.35, 2.75)),
    "luna_single": ("GPT-5.6-Luna, single call",
                    f"{R4}/luna_single_p%d.regraded.json", (0.20, 1.20)),
    "luna_multi": ("GPT-5.6-Luna, with manager",
                   f"{R4}/luna_multiagent_p%d.regraded.json", (0.20, 1.20)),
    "terra_single": ("GPT-5.6-Terra, single call",
                     f"{R4}/terra_single_p%d.regraded.json", (2.0, 12.0)),
    "terra_multi": ("GPT-5.6-Terra, with manager",
                    f"{R4}/terra_multiagent_p%d.regraded.json", (2.0, 12.0)),
    "fable_single": ("Fable 5, single call",
                     f"{ESC}/runs/fable5-5pass-single/results/fable5_single_p%d.regraded.json",
                     (10.0, 50.0)),
}
CAP = 128_000                       # the output cap every arm here is priced at

# Where the rates are published. One line under the panel rather than a reference on every
# row: four arms share the OpenAI sheet and two the Qwen one, so in the table the same
# three numbers repeated down a column of seven. Qwen has no first-party API price -- the
# weights are Apache 2.0 and Qwen Cloud has not opened -- so it cites the hosted gateway
# whose list rate we priced the local run at. plot_cost_vs_score imports this: the two
# figures price the same arms off the same sheets and must not drift apart.
SOURCES = ("List rates: Qwen3.8-27B~\\cite{openrouter2026}, "
           "GPT-5.6-Luna and GPT-5.6-Terra~\\cite{openai2026price}, "
           "Fable~5~\\cite{anthropic2026price}.")

# The token file keys the single arms by their as-generated name; only the Qwen one needs
# its output capped, the other two never came close to 128k.
TOK_KEY = {"q38_single": "q38_single"}

# What each manager arm costs against the frontier reference. Fable 5 is named with its
# arm even though it has only one: a bare "Fable 5" reads as the model rather than as the
# single call it is here. Every p is Holm-corrected across the whole list, so adding a
# row moves the others.
TESTS = [
    ("q38_single", "q38_multi", "Qwen3.8-27B: manager $-$ single"),
    ("luna_single", "luna_multi", "GPT-5.6-Luna: manager $-$ single"),
    ("terra_single", "terra_multi", "GPT-5.6-Terra: manager $-$ single"),
    ("q38_multi", "fable_single", "Fable 5 single $-$ Qwen3.8-27B manager"),
    ("luna_multi", "fable_single", "Fable 5 single $-$ GPT-5.6-Luna manager"),
    ("terra_multi", "fable_single", "Fable 5 single $-$ GPT-5.6-Terra manager"),
    # The one comparison on the frontier that does not involve Fable 5: S2.2 reads the
    # price half of it off this row, so it is tested in the same family as the rest.
    ("luna_multi", "terra_single", "GPT-5.6-Terra single $-$ GPT-5.6-Luna manager"),
]

# the rate spread across hosted providers in the week this was priced; the cost gap
# between the manager and Fable 5 does not survive the top of it (see `crossover`)
RATE_RANGE = ((0.33, 2.40), (0.45, 3.20))

# one x per MODEL, two bars on each except Fable 5, which has only the one arm
BAR_W = 0.36
X = {"q38_single": -BAR_W / 2, "q38_multi": BAR_W / 2,
     "luna_single": 1 - BAR_W / 2, "luna_multi": 1 + BAR_W / 2,
     "terra_single": 2 - BAR_W / 2, "terra_multi": 2 + BAR_W / 2,
     "fable_single": 3.0}
# Linear dollars from zero. The top is well above the dearest bar ($61.11): the two label
# lines over Fable 5 are drawn in points, about a fifth of the axis at this height, so at a
# tighter ceiling they run into the title.
#
# What this costs, and it is the whole reason the axis used to be log: the cheapest bar and
# the dearest are 150x apart, so GPT-5.6-Luna's single call ($0.41) is half a point tall and
# its manager arm ($1.50) not much more. Those two are read off their printed values and
# off the table under the figure, not off the axis. What the linear axis buys back is that
# the gaps between bars are now proportional to the dollars -- the manager surcharge on
# Qwen3.8-27B really does look like twice the height of its single call.
YLIM = (0, 82)
YTICKS = [0, 10, 20, 30, 40, 50, 60, 70, 80]

TITLE = ("What one pass costs — LCB-100, 5 passes, "
         "single call vs manager, against Fable 5")

# Legend under the axes rather than in a column beside them, so seven bars over three
# decades get the full text width. `bottom` pays for it: the stack under the axis is the
# model blocks, the two-line note, then the legend row. The cost-per-solve list that used
# to sit under the legend is a column of the first table now -- four more lines of chart
# would not fit, and the figures compare better beside the price they divide.
COST_MARGINS = dict(MARGINS, right=0.985, bottom=0.42)
LEGEND_Y = 0.075        # top of the legend row, clear of the note above it

# One line, as the figure's whole caption: the tables under the panel carry the numbers,
# so the prose only has to say what is priced and how it was tested. The rates used to be
# listed here; they are a column of the first table now, next to the tokens they multiply.
# No em dash -- the paper set parenthetical dashes as plain hyphens (commit 1686347).
CAPTION = ("\\textbf{The scaffold's bill.} Cost of one pass over the same 100 problems. "
           "Table 3 is the arithmetic behind every bar: published list rate, the "
           "tokens one pass of that arm actually consumed, and their product. No "
           "cached-input discount is taken, and Qwen3.8-27B is priced at OpenRouter market "
           "rates. Table 4 tests the "
           "gaps. Light bars are the single call, dark bars the manager, all at a 128k "
           "output cap. $\\Delta$ is tested "
           "per run (Welch, $n=5$ vs 5) and per problem (paired sign-flip, $n=100$), "
           "Holm-corrected across the seven comparisons.")


def money(v):
    """$ to two decimals, or to three below a dime: a problem Luna solved rounds to
    \\$0.01 at two, which loses the difference between it and the arms around it."""
    return f"\\${v:.2f}" if v >= 0.1 else f"\\${v:.3f}"


def arm_short(key, arm):
    """'GPT-5.6-Luna, with manager' -> 'GPT-5.6-Luna manager'.

    The model name is never abbreviated: two of the four arms are GPT-5.6 models, so
    "Luna manager" alone would name a different thing depending on which figure the
    reader came from.
    """
    return (f"{arm['label'].split(',')[0]} "
            f"{'single' if key.endswith('single') else 'manager'}")


def notes(stats):
    """Not rendered under this figure -- the table replaces the note block. Kept so the
    numbers that would otherwise only live in the terminal have one home."""
    a, t = stats["arms"], stats["tests"]
    return [
        f"Cost per solved problem: "
        + ", ".join(f"{arm_short(k, v)} {money(v['per_solve'])}" for k, v in a.items())
        + ".",
        f"At {stats['crossover']:.2f}x the assumed Qwen rate (\\${0.35 * stats['crossover']:.3f}/"
        f"\\${2.75 * stats['crossover']:.2f} per MTok, inside the spread across hosted "
        f"providers) the manager's cost advantage over Fable 5 disappears entirely — a "
        f"larger uncertainty than any p-value here.",
    ]


# --------------------------------------------------------------------------- data

def compute():
    tok = json.load(open(TOKENS))
    arms, qids = {}, None
    for key, (label, pattern, (ri, ro)) in ARMS.items():
        a = np.array(tok[key]["tokens"], float)          # [pass, problem, 4]
        assert qids is None or tok[key]["qids"] == qids, f"{key}: different problems"
        qids = tok[key]["qids"]
        if key == "q38_single":
            # Cap every generated attempt, not just the graded one: a retry that ran to
            # 250k would equally have stopped at 128k. This is what makes the bar match
            # the cap-matched score printed above it.
            a = a.copy()
            a[:, :, 1] = np.minimum(a[:, :, 1], CAP)
            a[:, :, 3] = np.minimum(a[:, :, 3], CAP)
        # every token generated, retried-and-discarded attempts included: all billable
        tin, tout = a[:, :, 0] + a[:, :, 2], a[:, :, 1] + a[:, :, 3]
        cost = (tin * ri + tout * ro) / 1e6
        passed = np.array([[bool(r["passed"]) for r in
                            json.load(open(pattern % p))["lcb"]["records"]] for p in PASSES])
        per_pass = cost.sum(axis=1)                      # $ for the 100 problems, per pass
        arms[key] = dict(
            key=key, label=label, rate=(ri, ro), cost=cost, per_pass=per_pass,
            mean=per_pass.mean(), ci=pass_ci(per_pass),
            # MTok over the 100 problems, averaged across the 5 passes -- the two numbers
            # that, times the rate, are `mean`
            mtok_in=tin.sum(axis=1).mean() / 1e6, mtok_out=tout.sum(axis=1).mean() / 1e6,
            per_problem=cost.mean(axis=0),               # $/problem over the 5 passes
            acc=100 * passed.mean(), per_solve=cost.sum() / passed.sum(),
        )

    from scipy import stats as sps
    tests = []
    for ka, kb, name in TESTS:
        x, y = arms[ka]["per_pass"], arms[kb]["per_pass"]
        # passes are independent runs sharing only the problem set, so the run-level
        # comparison is two-sample: pairing pass 3 with pass 3 would mean nothing
        welch = sps.ttest_ind(y, x, equal_var=False)
        d = arms[kb]["per_problem"] - arms[ka]["per_problem"]   # same Delta, /100
        delta, p_prob, floored = perm_sign_p(d)
        tests.append(dict(a=ka, b=kb, name=name, delta_pass=y.mean() - x.mean(),
                          delta_prob=delta, prob_ci=boot_ci(d),
                          p_pass=welch.pvalue, p_prob=p_prob, floored=floored))
    for tst, ph in zip(tests, holm([t["p_pass"] for t in tests])):
        tst["p_pass_holm"] = ph
    for tst, ph in zip(tests, holm([t["p_prob"] for t in tests])):
        tst["p_prob_holm"] = ph
        tst["sig"] = ph < ALPHA

    # what multiple of the assumed Qwen rate makes the manager cost what Fable 5 costs
    crossover = arms["fable_single"]["cost"].sum() / arms["q38_multi"]["cost"].sum()
    return dict(arms=arms, tests=tests, crossover=crossover)


# the tables make_figures_tex.py sets under the panel. The module owns the numbers and
# their column names; the script owns only the tabular scaffolding around them.

# 1. what each bar is made of: rate x tokens = dollars, one row per arm. The rates are the
# whole of the modelling assumption (see the module docstring), so they are a column with
# a reference on it rather than a sentence in the caption.
RATE_HEADER = ("Arm", "Rate \\$/MTok in / out", "In (MTok)", "Out (MTok)",
               "\\$/pass", "\\$/solved")
# 0.7em between columns, not the 1em the comparison table below uses: six columns at 1em
# put the header row 32pt past the text block.
RATE_SPEC = ("@{}l@{\\hspace{0.7em}}l@{\\hspace{0.7em}}r@{\\hspace{0.7em}}r"
             "@{\\hspace{0.7em}}r@{\\hspace{0.7em}}r@{}")

# 2. the gaps between those bars, tested
TABLE_HEADER = ("Comparison", "$\\Delta$ \\$/pass",
                "$p$ (per pass, $n=5$)", "$p$ (per problem, $n=100$)")
# 1em between columns rather than booktabs' 2 x \tabcolsep (12pt): naming every arm in
# full puts the longest row 2pt past the text block at the default spacing
TABLE_SPEC = "@{}l@{\\hspace{1em}}c@{\\hspace{1em}}c@{\\hspace{1em}}c@{}"


def fmt_p_tex(p, floored=False):
    """p as LaTeX. Unlike fmt_p_num's matplotlib mathtext, the "<" goes INSIDE the math:
    a bare "<" in LaTeX text mode sets an inverted exclamation mark, not a less-than."""
    lt = "<" if floored else ""
    if p >= 1e-3:
        # "#" keeps the trailing zero, so the column reads 0.0051 / 0.20, not 0.0051 / 0.2
        return f"${lt}{p:#.2g}$" if lt else f"{p:#.2g}"
    mantissa, exponent = ("%.1e" % p).split("e")
    return f"${lt}{mantissa}\\times10^{{{int(exponent)}}}$"


def rate_tex(v):
    """$0.35, but $2 -- a whole-dollar rate is published without cents and printing
    "$2.00" beside "$0.35" reads as a precision the price sheet does not claim."""
    return f"\\${v:g}" if v == int(v) else f"\\${v:.2f}"


def rate_rows(stats):
    """-> [(arm, rate + cite, MTok in, MTok out, $/pass)], already LaTeX.

    Rate x tokens is the whole calculation, so the row shows all three factors: a reader
    who disagrees with a rate can redo the $/pass column without the transcripts. That is
    what fixes the token columns at 4dp: $/pass is computed from the full-precision counts,
    so whatever the columns drop comes back multiplied by the output rate. At 2dp Fable 5
    reconstructed to $60.90 against the $61.11 printed beside it -- 4.3 ktok of rounding at
    $50/MTok -- and only one row of the seven reproduced its own dollars. 4dp is exact for
    every row; 3dp still leaves two a cent out.

    The last column is what a problem the arm got RIGHT cost, and it does not rank the
    arms the way $/pass does -- which is the chart's point, so it is worth the column. It
    used to be a list beside the chart; a column beside the price it divides is where it
    can actually be compared.
    """
    rows = []
    for key, arm in stats["arms"].items():
        ri, ro = arm["rate"]
        rows.append((arm_short(key, arm), f"{rate_tex(ri)} / {rate_tex(ro)}",
                     f"{arm['mtok_in']:.4f}", f"{arm['mtok_out']:.4f}",
                     money(arm["mean"]), money(arm["per_solve"])))
    return rows


def table_rows(stats):
    """-> [(comparison, Delta $/pass, p per pass, p per problem)], already LaTeX.

    Both p columns test the SAME difference -- the per-problem mean is the per-pass
    figure over 100 -- and differ only in what they resample: runs, or problems.

    The Delta is differenced from the two $/pass figures AS PRINTED in the table above,
    not from the full-precision means. Both tables sit on one page and a reader checks the
    second against the first: Terra's exact +8.3060 sets as +8.31 beside an 11.71 and a
    3.41 that subtract to 8.30, and Fable 5 minus Luna's manager the same way. Rounding
    twice costs a cent of a column that is only ever read to the cent; disagreeing with
    the table above it costs the reader the arithmetic. The tests themselves are on the
    full-precision per-pass costs -- only this display column rounds first.
    """
    def shown(key):
        return round(stats["arms"][key]["mean"], 2)
    return [(t["name"], f"{shown(t['b']) - shown(t['a']):+.2f}",
             fmt_p_tex(t["p_pass_holm"]), fmt_p_tex(t["p_prob_holm"], t["floored"]))
            for t in stats["tests"]]


# in the order they are set under the panel: what a pass cost, then what the differences
# between those costs test at. make_figures_tex.py reads this, not the pieces above.
# The fourth item is the table's own caption: these two sit inside a figure, so they take
# their number from \captionof{table} rather than from a table float of their own.
TABLES = [(RATE_HEADER, RATE_SPEC, rate_rows,
           "\\textbf{What one pass cost each arm.} List rate $\\times$ the tokens it "
           "consumed."),
          (TABLE_HEADER, TABLE_SPEC, table_rows,
           "\\textbf{The differences between those costs.} Tested per run and per "
           "problem.")]


# --------------------------------------------------------------------------- plot

def draw(stats, theme="light", save=None):
    t = THEMES[theme]
    apply_theme(t)
    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(**COST_MARGINS)
    arms = stats["arms"]

    ax.set(xlim=(-0.62, 3.62), ylim=YLIM)
    # ticks at the MODEL centres, not at each bar: with a pair per model the bar
    # positions are offsets either side of the centre the block below is drawn at.
    ax.set_xticks([0, 1, 2, 3], [""] * 4)   # names go in the blocks below
    ax.set_ylabel("Cost of one pass (USD)", fontsize=FS_BODY, color=t["ink2"])
    ax.xaxis.grid(False)
    ax.yaxis.grid(True)
    ax.set_axisbelow(True)
    ax.tick_params(length=0, labelsize=FS_BODY)
    ax.set_yticks(YTICKS, [f"\\${v:g}" for v in YTICKS])
    for spine in ("left", "bottom"):
        ax.spines[spine].set_color(t["axis"])

    # ---- one bar per condition, with the accuracy that money bought printed under the
    # price: the point of the chart is the ratio between the two, and a reader who has to
    # fetch the accuracy from the companion figure will not compute it
    for key, arm in arms.items():
        x, y, (lo, hi) = X[key], arm["mean"], arm["ci"]
        # from zero, so the height IS the price -- the axis floor the log version had to
        # draw from, and subtract back off every bar, is gone with it
        ax.bar(x, y, BAR_W, color=FILLS[key], zorder=3,
               edgecolor=ring(FILLS[key], theme), linewidth=EDGE_LW)
        ax.plot([x, x], [lo, hi], lw=CI_LW, color=t["ink"], solid_capstyle="butt", zorder=5)
        for end in (lo, hi):
            ax.plot([x], [end], marker="_", ms=14, mew=CI_LW, color=t["ink"], zorder=5)
        ax.annotate(money(y), xy=(x, hi), xytext=(0, 7),
                    textcoords="offset points", ha="center", va="bottom",
                    fontsize=FS_BODY, color=t["ink"])
        # pass@1 over the price, so the chart carries both halves of the ratio it is
        # about; four models wide there is no room for the words, which the axis note
        # and the caption supply instead
        ax.annotate(f"{arm['acc']:.1f}%", xy=(x, hi), xytext=(0, 7 + FS_BODY * 1.35),
                    textcoords="offset points", ha="center", va="bottom",
                    fontsize=FS_NOTE, color=t["muted"])

    # ---- blocks under the axis: the model and the rate its dollars were computed at,
    # since every number on the chart is tokens x that rate. Four blocks share the width
    # two used to, so the rate loses its "per MTok" (the axis note below carries it) and
    # the provenance line is a word or two.
    blocks = {
        "q38_single": ("\\$0.35 / \\$2.75", "OpenRouter list"),
        "luna_single": ("\\$0.20 / \\$1.20", "OpenAI list"),
        "terra_single": ("\\$2 / \\$12", "OpenAI list"),
        "fable_single": ("\\$10 / \\$50", "Anthropic list"),
    }
    for key, (rate, source) in blocks.items():
        drop = model_block(ax, X[key], [
            (arms[key]["label"].split(",")[0], FS_HEAD, "bold", t["ink"]),
            (rate, FS_NOTE, "normal", t["ink2"]),
            (source, FS_NOTE, "normal", t["muted"])])

    # Two lines, each short enough to stay inside the axes even at the full text width:
    # at FS_BODY the whole sentence on one line is wider than the canvas.
    ax.annotate("Same 100 problems, 5 passes per condition; bars are the mean pass,"
                "\nCI across the 5; the figure over each bar is its pass@1.",
                xy=(0.5, 0), xycoords="axes fraction", xytext=(0, -(drop + 12)),
                textcoords="offset points", ha="center", va="top",
                fontsize=FS_BODY, color=t["ink2"], linespacing=1.35)

    # ---- under the axes: one entry per MODEL carrying both its fills, then the cost of a
    # problem the condition got RIGHT -- the ranking there is not the ranking of the bars,
    # which is the chart's real point.
    #
    # A row per arm would be seven entries wide, which does not fit across the canvas, and
    # wrapped to two rows it is the same seven names the blocks above already carry. Paired
    # swatches say the one thing those blocks cannot: which fill is which condition.
    def patch(key):
        return Patch(facecolor=FILLS[key], edgecolor=ring(FILLS[key], theme),
                     linewidth=EDGE_LW)

    pairs, names = [], []
    for mk in ("q38", "luna", "terra", "fable"):
        pairs.append(tuple(patch(k) for k in (f"{mk}_single", f"{mk}_multi")
                           if k in FILLS))
        names.append(arms[f"{mk}_single"]["label"].split(",")[0])

    fig.suptitle(wrap_title(TITLE), x=MARGINS["left"], ha="left", y=0.99,
                 va="top", fontsize=FS_TITLE, fontweight="bold", color=t["ink"],
                 linespacing=1.25)
    below_panel(fig, t, pairs, names, LEGEND_Y, ncol=len(names))
    if save:
        # no crop: the canvas is authored at exactly PAGE_SCALE x its printed size
        fig.savefig(save)
        print("wrote", save)
    plt.close(fig)


def main():
    stats = compute()

    hdr = (f"{'arm':26s} {'$/pass':>8s} {'95% CI':>16s} {'5 passes':>9s} "
           f"{'pass@1':>7s} {'$/solve':>8s}")
    print(hdr)
    print("-" * len(hdr))
    for arm in stats["arms"].values():
        print(f"{arm['label']:26s} {arm['mean']:8.2f}   [{arm['ci'][0]:5.2f},{arm['ci'][1]:6.2f}]"
              f" {arm['cost'].sum():9.2f} {arm['acc']:7.1f} {arm['per_solve']:8.3f}")

    print(f"\nsame difference, two units of analysis "
          f"(both Holm-corrected across the {len(TESTS)}):")
    for t in stats["tests"]:
        pre = "<" if t["floored"] else " "
        print(f"  {t['name'].replace('$-$', '-'):32s} {t['delta_pass']:+7.2f} $/pass"
              f"  ({t['delta_prob']:+.3f} $/problem, CI [{t['prob_ci'][0]:+.3f},"
              f"{t['prob_ci'][1]:+.3f}])")
        print(f"  {'':32s} per-pass Welch p {t['p_pass']:.2e} -> Holm {t['p_pass_holm']:.2e}"
              f"   per-problem paired p {pre}{t['p_prob']:.2e} -> Holm {t['p_prob_holm']:.2e}")
    print(f"\n  manager cost = Fable 5 cost at {stats['crossover']:.3f}x the assumed Qwen rate"
          f"  (${0.35 * stats['crossover']:.3f}/${2.75 * stats['crossover']:.2f} per MTok)")

    os.makedirs(PLOTS, exist_ok=True)
    for theme in ("light", "dark"):
        draw(stats, theme, save=os.path.join(PLOTS, f"{slug(TITLE)}_{theme}.png"))


if __name__ == "__main__":
    main()
