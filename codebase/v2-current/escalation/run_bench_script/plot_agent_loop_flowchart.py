#!/usr/bin/env python3
"""Manager-worker control flow, in plain English -- two diagrams of the same loop.

FIG_CURRENT is the paper's Figure 4: the loop as multiagent.py runs it today, i.e. the v2
scaffold that S3.1 describes and that produced the pinned-backend arms of S2.1. The round
budget is 10; after a round that wrote fresh code, solution.py is run against the problem's
public stdin samples and the verdict is handed to the manager as ground truth (and vetoes a
"done" verdict); and a worker cut off at the token limit gets its partial attempt digested
by an extra call before the manager sees the round. Its layout is its own grid, not the
source PNG's.

FIG_46710A5 documents the ORIGINAL scaffold -- the version behind the OpenRouter-served
results in S2.3 -- and is no longer the figure the paper includes. It is a reconstruction of
`paper/agent_loop_flowchart_plain_english.png`, whose generating script was lost. Box
positions, fills, borders and font sizes were measured back off that PNG, so the output
matches it closely; it is a redraw, not a pixel copy. It documents multiagent.py @
46710a5, which is what its title records: MULTIAGENT_MAX_ITERS was 4 there, and the
sample-test verifier does not appear at all. Keep it -- it is the only drawing of the
scaffold that produced S2.3, and the paper's S3 table of v2-vs-original differences is
read off the pair.

    uv run --with matplotlib python escalation/run_bench_script/plot_agent_loop_flowchart.py

Writes plots/<title-slug>_{light,dark}.png, one pair per diagram.
"""
import os
import re

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

HERE = os.path.dirname(os.path.abspath(__file__))
ESC = os.path.dirname(HERE)             # escalation/, one level up from run_bench_script/
PLOTS = os.path.join(ESC, "plots")      # every chart script writes here

# Each figure carries its own canvas, a pixel grid with y running downward. For the
# 46710a5 figure that grid is the source PNG's, so every coordinate in it is a
# measurement off that image rather than a guess. DPI 130 matches the other charts in
# this directory; raising it scales a diagram, since text is sized in points.
DPI = 130

# Light values are sampled from the source PNG; the surface/ink/muted entries coincide
# with THEMES["light"] in plot_16k_reason_off_5_pass.py, which is where they came from.
# `check` is the one fill the source PNG has no value for -- it marks the sample-test
# run, the only step in either diagram that is not a model call.
THEMES = {
    "light": dict(
        surface="#fcfcfb", ink="#0b0b0b", ink2="#52514e", muted="#898781",
        wire="#c3c2b7",
        fills=dict(lead="#e9e6fa", helper="#ddf1ea", decision="#fdeeda", terminal="#f0efe9",
                   check="#dde9f4"),
        edges=dict(lead="#b7b0e8", helper="#a5dbc9", decision="#efc38d", terminal="#cecdc2",
                   check="#9cbfdd"),
    ),
    "dark": dict(
        surface="#1a1a19", ink="#ffffff", ink2="#c3c2b7", muted="#898781",
        wire="#4a4a46",
        fills=dict(lead="#2b2747", helper="#1d3a33", decision="#3d3122", terminal="#2c2c2a",
                   check="#1e2a38"),
        edges=dict(lead="#6b62b0", helper="#4a9078", decision="#a87c3c", terminal="#4d4c47",
                   check="#4d7196"),
    ),
}

FS_TITLE, FS_HEAD, FS_SUB, FS_LABEL, FS_LEGEND, FS_NOTE = 9.75, 8.25, 7.0, 7.0, 7.5, 7.25
SWATCH_W, SWATCH_H = 29, 19             # legend swatch, shared by both figures

# --- figure 1: multiagent.py as the current tree runs it, the paper's Figure 4 ----------
# Same loop, wider canvas: the sample-test gate and the cut-off digest are two more steps
# in the worker column, and the manager's verdict is now checked against the gate first.
# Ordering note: in code the manager answers done/continue and the gate then overrides a
# "done" that fails the samples. A failing gate forces continue either way, so asking the
# gate FIRST -- as drawn -- is the same control flow with one fewer wire.

TITLE_CUR = "How the manager arm answers one question — multiagent.py, current tree"

# (kind, x0, y0, x1, y1, heading, subtext)
BOXES_CUR = [
    ("terminal", 450, 100, 670, 150, "One question comes in", None),
    ("lead", 443, 190, 677, 258, "Lead agent: plan", "write a plan, list 3–6 tasks"),
    ("helper", 423, 296, 697, 385, "Helper agent: brainstorm",
     "suggest approaches only\n(asked not to solve it yet)"),
    ("lead", 423, 419, 697, 514, "Lead agent: manage",
     "tidy list, pick the next task\ncannot finish on an empty workspace"),
    ("decision", 400, 557, 720, 642, "Did the last round fail\nthe public sample tests?",
     "(a fail vetoes the manager)"),
    ("decision", 456, 686, 664, 742, "Is the work finished?", None),
    ("decision", 96, 790, 330, 865, "Is an answer already saved?", "(check the workspace)"),
    ("terminal", 85, 925, 226, 981, "Skip", "the write-up"),
    ("decision", 760, 790, 1033, 879, "Another task left, and fewer\nthan 10 rounds used?",
     "(none named → first unfinished task)"),
    ("decision", 766, 925, 1027, 1000, "Is it the same task", "we just handed out?"),
    ("helper", 760, 1045, 1033, 1120, "Helper agent: do the task",
     "updates the answer, rewrites the notes"),
    ("decision", 760, 1165, 1033, 1240, "Was it cut off at", "the token limit?"),
    ("helper", 440, 1165, 700, 1240, "Helper agent: summarise", "the cut-off attempt"),
    ("decision", 760, 1290, 1033, 1370, "Did this round write fresh code?",
     "(and does the problem ship stdin tests?)"),
    ("check", 745, 1415, 1048, 1495, "Run solution.py on the samples",
     "verdict goes to the manager as ground truth"),
    ("helper", 250, 1290, 530, 1365, "Helper agent writes", "the final answer"),
    ("terminal", 240, 1425, 620, 1487, "Hand back the solution", "and answer files for grading"),
]

# Elbow polylines; the arrowhead lands on the last point.
WIRES_CUR = [
    [(560, 150), (560, 190)],                                      # start -> plan
    [(560, 258), (560, 296)],                                      # plan -> brainstorm
    [(560, 385), (560, 419)],                                      # brainstorm -> manage
    [(560, 514), (560, 557)],                                      # manage -> sample gate
    [(560, 642), (560, 686)],                                      # gate: samples fine
    [(720, 585), (1090, 585), (1090, 835), (1033, 835)],           # gate: failed -> loop
    [(456, 714), (213, 714), (213, 790)],                          # finished? yes
    [(664, 714), (895, 714), (895, 790)],                          # finished? no
    [(155, 865), (155, 925)],                                      # saved? yes -> skip
    [(295, 865), (295, 1290)],                                     # saved? no  -> write-up
    [(760, 855), (380, 855), (380, 1290)],                         # rounds left? no
    [(766, 962), (380, 962)],                                      # same task? yes, merges in
    [(895, 879), (895, 925)],                                      # rounds left? yes
    [(895, 1000), (895, 1045)],                                    # same task? no -> do it
    [(895, 1120), (895, 1165)],                                    # worker -> cut off?
    [(760, 1202), (700, 1202)],                                    # cut off -> summarise it
    [(575, 1240), (575, 1265), (800, 1265), (800, 1290)],          # digest rejoins the round
    [(895, 1240), (895, 1290)],                                    # not cut off
    [(895, 1370), (895, 1415)],                                    # fresh code -> run samples
    [(1033, 1330), (1120, 1330)],                                  # no fresh code, no verdict
    [(1048, 1455), (1120, 1455), (1120, 466), (697, 466)],         # round -> back to manager
    [(155, 981), (155, 1456), (240, 1456)],                        # skip -> hand back
    [(390, 1365), (390, 1425)],                                    # write-up -> hand back
]

# (text, x, y) -- centred on the point
LABELS_CUR = [
    ("yes", 750, 570), ("no", 585, 664),
    ("yes", 422, 700), ("no", 698, 700),
    ("yes", 133, 897), ("no", 325, 890),
    ("no — out of rounds", 545, 841),
    ("yes (nothing changed)", 545, 948),
    ("yes", 918, 903), ("no", 918, 1024),
    ("yes", 730, 1188), ("no", 918, 1266),
    ("yes", 918, 1394), ("no", 1074, 1313),
    ("back to the manager", 908, 447),
]

# Packed left-to-right with a constant 60px gap rather than spread across the canvas:
# each x is the previous one plus that entry's measured width (swatch 29 + 14 + label).
LEGEND_CUR = [("lead", "lead agent", 80), ("helper", "helper agent", 259),
              ("decision", "decision", 453), ("terminal", "start / end", 615),
              ("check", "sample-test run (no model call)", 790)]

# No note band under this one: everything the 46710a5 notes explain -- the round budget,
# what the sample gate does and when it produces no verdict -- the paper now says in the
# S3.1 prose and the caption that run beside the figure, and a second account of it here
# is one more thing to keep in sync. `notes` is absent from its entry below, not empty.


# --- figure 2: multiagent.py @ 46710a5, the ORIGINAL scaffold (§2.3) --------------------
# Not the figure the paper includes; kept because it is the only drawing of the scaffold
# behind §2.3, and §3's list of v2-vs-original differences is read off the pair.

TITLE_46 = "How the manager arm answers one question — multiagent.py @ 46710a5"

BOXES_46 = [
    ("terminal", 324, 106, 545, 155, "One question comes in", None),
    ("lead", 318, 196, 552, 264, "Lead agent: plan", "write a plan, list 3–6 tasks"),
    ("helper", 298, 304, 571, 393, "Helper agent: brainstorm",
     "suggest approaches only\n(asked not to solve it yet)"),
    ("lead", 298, 427, 571, 522, "Lead agent: manage",
     "tidy list, pick the next task\ncannot finish on an empty workspace"),
    ("decision", 331, 565, 538, 621, "Is the work finished?", None),
    ("decision", 93, 661, 327, 736, "Is an answer already saved?", "(check the workspace)"),
    ("decision", 615, 654, 888, 743, "Another task left, and fewer\nthan 4 rounds used?",
     "(none named → first unfinished task)"),
    ("terminal", 80, 803, 221, 859, "Skip", "the write-up"),
    ("decision", 621, 793, 882, 868, "Is it the same task", "we just handed out?"),
    ("helper", 258, 925, 505, 1000, "Helper agent writes", "the final answer"),
    ("helper", 615, 925, 888, 1000, "Helper agent: do the task", "updates answer + what's next"),
    ("terminal", 245, 1064, 624, 1126, "Hand back the solution", "and answer files for grading"),
]

WIRES_46 = [
    [(434.5, 155), (434.5, 196)],                                  # start -> plan
    [(434.5, 264), (434.5, 304)],                                  # plan -> brainstorm
    [(434.5, 393), (434.5, 427)],                                  # brainstorm -> manage
    [(434.5, 522), (434.5, 565)],                                  # manage -> finished?
    [(331, 593), (210, 593), (210, 661)],                          # finished? yes
    [(538, 593), (751, 593), (751, 654)],                          # finished? no
    [(150, 736), (150, 803)],                                      # saved? yes -> skip
    [(290, 736), (290, 925)],                                      # saved? no  -> write-up
    [(751, 743), (751, 793)],                                      # rounds left? yes
    [(751, 868), (751, 925)],                                      # same task? no -> do it
    [(615, 698), (368, 698), (368, 925)],                          # rounds left? no
    [(621, 830), (447, 830), (447, 925)],                          # same task? yes
    [(888, 962), (924, 962), (924, 474), (571, 474)],              # worker -> back to manager
    [(150, 859), (150, 1095), (245, 1095)],                        # skip -> hand back
    [(381.5, 1000), (381.5, 1064)],                                # write-up -> hand back
]

LABELS_46 = [
    ("yes", 270, 575), ("no", 645, 575),
    ("back to the manager", 752, 451),
    ("no — out of rounds", 491, 678),
    ("yes", 128, 768), ("no", 323, 758),
    ("yes", 778, 767), ("no", 778, 895),
    ("yes (nothing changed)", 534, 810),
]

LEGEND_46 = [("lead", "lead agent", 80), ("helper", "helper agent", 311),
             ("decision", "decision", 542), ("terminal", "start / end", 773)]

# The source set the code tokens (solution.py, answer.md, ANSWER:, MULTIAGENT_MAX_ITERS)
# in a monospace face. Reproducing that with mathtext \mathtt puts math spacing around
# the punctuation -- "solution. py", "ANSWER : " -- so these are plain text instead. The
# wording is unchanged; only the face differs.
NOTES_46 = [
    "The manager owns the loop; the workspace files are the only state a role sees, "
    "and no task carries a result field.",
    "•  “Is an answer already saved?” is always yes on code problems — the manager "
    "cannot report finished with an empty",
    "    solution.py, so the “no” branch is reachable only for math "
    "(an answer.md holding no ANSWER: line).",
    "•  4 rounds is the MULTIAGENT_MAX_ITERS default at this commit; "
    "the uncommitted tree raises it to 10.",
    "•  A worker's own “solved” claim never ends the loop — only the manager's verdict does.",
]
NOTE_DY = 21.5                          # only this figure carries a note band


# (title, canvas, boxes, wires, labels, legend + its y, and optionally notes + their first y)
FIGURES = [
    # Width is the flowchart's own right edge (the return lane at x=1120) plus a margin
    # matching the left one; height is the legend plus the same margin under it.
    dict(title=TITLE_CUR, size=(1200, 1600), boxes=BOXES_CUR, wires=WIRES_CUR,
         labels=LABELS_CUR, legend=LEGEND_CUR, legend_y=1541),
    dict(title=TITLE_46, size=(1015, 1354), boxes=BOXES_46, wires=WIRES_46,
         labels=LABELS_46, legend=LEGEND_46, legend_y=1156,
         notes=NOTES_46, note_y0=1218),
]


def slug(text):
    """Title -> filename stem, so the two never drift apart."""
    return re.sub(r"_+", "_", re.sub(r"[^a-z0-9-]+", "_",
                                     text.lower().replace("—", " "))).strip("_")


def draw(figure, theme="light", save=None):
    t = THEMES[theme]
    W, H = figure["size"]
    plt.rcParams.update({
        "figure.facecolor": t["surface"], "savefig.facecolor": t["surface"],
        "font.family": "sans-serif", "font.size": 10,
        "mathtext.default": "regular", "mathtext.fontset": "dejavusans",
    })
    fig = plt.figure(figsize=(W / DPI, H / DPI), dpi=DPI)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set(xlim=(0, W), ylim=(H, 0))       # y inverted: pixel coordinates, origin top-left
    ax.axis("off")
    ax.set_facecolor(t["surface"])

    ax.text(W / 2, 72, figure["title"], ha="center", va="center",
            fontsize=FS_TITLE, fontweight="bold", color=t["ink"])

    for kind, x0, y0, x1, y1, head, sub in figure["boxes"]:
        ax.add_patch(FancyBboxPatch(
            (x0, y0), x1 - x0, y1 - y0,
            boxstyle="round,pad=0,rounding_size=6",
            facecolor=t["fills"][kind], edgecolor=t["edges"][kind], linewidth=1.1, zorder=2))
        if sub is None:
            ax.text((x0 + x1) / 2, (y0 + y1) / 2, head, ha="center", va="center",
                    fontsize=FS_HEAD, color=t["ink"], zorder=3, linespacing=1.5)
        else:
            # Heading sits in the upper part of the box, subtext below it. A two-line
            # subtext is centred higher (0.36 rather than 0.26 of the span up from the
            # bottom) so its second line clears the lower border: measured against the
            # source PNG that leaves ~15px under the brainstorm box's last line and
            # ~18px under the manage box's, which are the only two with two-line subs.
            nh, ns = head.count("\n") + 1, sub.count("\n") + 1
            span = y1 - y0
            head_y = y0 + span * (0.30 if ns == 1 else 0.26) + (nh - 1) * 5
            sub_y = y1 - span * (0.26 if ns == 1 else 0.36)
            ax.text((x0 + x1) / 2, head_y, head, ha="center", va="center",
                    fontsize=FS_HEAD, color=t["ink"], zorder=3, linespacing=1.45)
            ax.text((x0 + x1) / 2, sub_y, sub, ha="center", va="center",
                    fontsize=FS_SUB, color=t["ink2"], zorder=3, linespacing=1.6)

    for pts in figure["wires"]:
        if len(pts) > 2:               # elbows first, so the head sits on the last leg only
            ax.plot([p[0] for p in pts[:-1]], [p[1] for p in pts[:-1]],
                    color=t["wire"], lw=1.2, solid_capstyle="butt",
                    solid_joinstyle="miter", zorder=1)
        ax.annotate("", xy=pts[-1], xytext=pts[-2],
                    arrowprops=dict(arrowstyle="-|>", color=t["wire"], lw=1.2,
                                    shrinkA=0, shrinkB=0, mutation_scale=9), zorder=1)

    for text, x, y in figure["labels"]:
        ax.text(x, y, text, ha="center", va="center", fontsize=FS_LABEL, color=t["ink2"])

    for kind, text, x in figure["legend"]:
        ax.add_patch(FancyBboxPatch(
            (x, figure["legend_y"]), SWATCH_W, SWATCH_H,
            boxstyle="round,pad=0,rounding_size=5",
            facecolor=t["fills"][kind], edgecolor=t["edges"][kind], linewidth=1.1))
        ax.text(x + SWATCH_W + 14, figure["legend_y"] + SWATCH_H / 2, text,
                ha="left", va="center", fontsize=FS_LEGEND, color=t["ink2"])

    for i, note in enumerate(figure.get("notes", ())):
        ax.text(78, figure["note_y0"] + NOTE_DY * i, note, ha="left", va="center",
                fontsize=FS_NOTE, color=t["muted"])

    if save:
        fig.savefig(save, dpi=DPI)
        print("wrote", save)
    plt.close(fig)


def main():
    os.makedirs(PLOTS, exist_ok=True)
    for figure in FIGURES:
        for theme in ("light", "dark"):
            draw(figure, theme,
                 save=os.path.join(PLOTS, f"{slug(figure['title'])}_{theme}.png"))


if __name__ == "__main__":
    main()
