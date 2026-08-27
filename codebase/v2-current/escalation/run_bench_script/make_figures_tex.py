#!/usr/bin/env python3
"""Write paper/fig-*.tex: the three two-panel figures, captions and all.

The charts carry only what has to sit beside a mark. Everything else -- how to read
the fills, what the test was, the pairwise Tukey p values, the emit rates -- is
caption text, which LaTeX sets at real \\footnotesize instead of the ~5pt an in-chart
note block could manage at this canvas size.

Each condition module owns its own CAPTION and notes(stats); this script only turns
them into LaTeX and pairs them with the two PNGs the plot scripts wrote. Numbers
inside a note are read off `stats`, so a re-run updates the paper -- nothing here is
transcribed by hand.

    uv run --with matplotlib --with numpy --with scipy python \\
        escalation/run_bench_script/make_figures_tex.py

Run it after the plot scripts; paper.tex \\inputs the files it writes.
"""
import os

import plot_16k_reason_off_5_pass as p16
import plot_128k_reason_off_1_pass as p128off
import plot_128k_reason_on_1_pass as p128on
import plot_q38_vs_fable5_5_pass as pq38
import plot_4new_5pass_reason_on as p4new
import plot_cost_5_pass as pcost
import plot_cost_vs_score as pcvs
from plot_16k_reason_off_5_pass import slug, tukey, tukey_sentence

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))    # repo root
PAPER = os.path.join(ROOT, "paper")

# Figures 1-3 of the paper, in the order they appear there, then the ones written but not
# yet \input anywhere. `tukey` is off where there is no across-model HSD to report: the
# Qwen3.8-Max vs Fable-5 figure has two models and one of them has a single arm, so its
# three comparisons are the paired tests in its own notes.
FIGURES = [
    dict(mod=p128on, out="fig-128k-reason-on.tex"),
    dict(mod=p16, out="fig-16k-reason-off.tex"),
    dict(mod=p128off, out="fig-128k-reason-off.tex"),
    # tukey=False: the four pinned-backend models are not a scale series, and three of
    # them have undisclosed sizes, so a cross-model HSD would be uninterpretable.
    # Bars only: with four models and no scale axis the dot panel showed the same eight
    # numbers in the same left-to-right order, so it was a second rendering rather than a
    # second view. The CIs it carried are on the bars too.
    dict(mod=p4new, out="fig-4new-5pass.tex", tukey=False, panels=("bars",),
         captions=("Accuracy per condition, with 95\\% CIs across the 5 passes.",
                   "Accuracy per condition, with 95\\% CIs across the 5 passes.")),
    # plot_q38_vs_fable5_5_pass is deliberately absent: its four manager-vs-Fable-5 bars
    # and all three of its p values are already in Figure 1's long brackets and caption,
    # so the paper dropped it rather than print the comparison twice. The script and its
    # PNGs are kept -- it is still the place those numbers are computed.
    # Single panel: this chart is one scatter, not a dots/bars pair.
    dict(mod=pcvs, out="fig-cost-vs-score.tex", tukey=False, panels=("dots",),
         captions=("Cost against accuracy, all seven pinned-backend arms.", "")),
    # one panel, then the module's own table, then a one-line caption. The tables are
    # written to their own file so paper.tex can \input the cost-vs-score figure between
    # the chart and them: a barrier flushes floats in declaration order, and with the two
    # tables ahead of it Figure 3 was pushed onto a sheet of its own a page later.
    dict(mod=pcost, out="fig-cost.tex", tukey=False, table=True,
         tables_out="fig-cost-tables.tex"),
]

# The notes are written as plain prose with real Unicode; these are the characters
# that would otherwise be a LaTeX special or a missing glyph. Order matters: the
# backslash has to go first, or it would escape the escapes.
TEX = [
    ("\\", "\\textbackslash{}"),
    ("%", "\\%"), ("&", "\\&"), ("#", "\\#"), ("_", "\\_"),
    ("{", "\\{"), ("}", "\\}"), ("~", "\\textasciitilde{}"), ("^", "\\textasciicircum{}"),
    ("Δ", "$\\Delta$"), ("α", "$\\alpha$"), ("×", "$\\times$"), ("−", "$-$"),
    ("→", "$\\to$"), ("≥", "$\\ge$"), ("≤", "$\\le$"), ("<", "$<$"), (">", "$>$"),
    ("—", "-"), ("–", "--"), ("’", "'"),
    # Currency. A note cannot write a bare "$" -- tex() treats dollar signs as math
    # delimiters (so fmt_p_num's mathtext survives), and a note about prices would pair
    # them up and set half its words in math italics. Notes write "¤12.34"; this maps it
    # to a real escaped dollar. It has to sit AFTER the backslash rule above, or the
    # backslash it introduces would itself be escaped.
    ("¤", "\\$"),
]


def tex(text):
    """Prose -> LaTeX. Straight double quotes become a proper open/close pair.

    Spans between dollar signs are passed through untouched: fmt_p_num() writes a
    small p as matplotlib mathtext ($2\\times10^{-7}$), which is already LaTeX, and
    escaping it would print the backslashes.
    """
    out, opening = [], True
    for i, span in enumerate(text.split("$")):
        if i % 2:                                  # inside math: already LaTeX
            out.append(f"${span}$")
            continue
        for a, b in TEX:
            span = span.replace(a, b)
        for ch in span:
            if ch == '"':
                out.append("``" if opening else "''")
                opening = not opening
            else:
                out.append(ch)
    return "".join(out)


def figure_tex(fig, stats, pmat):
    """One float page: dot panel, bar panel, then the caption with the notes.

    `panels` in the registry selects which of the two are drawn. A figure asking for one
    of them gets no subfigure wrapper and no (a)/(b) sublabel -- a lone panel labelled (b)
    reads as a figure with a missing half.
    """
    mod = fig["mod"]
    stem = slug(mod.TITLE)
    notes = [tex(n) for n in mod.notes(stats)]
    if pmat is not None:
        notes.append(tex(tukey_sentence(stats, pmat)))
    caps = fig.get("captions", ("Accuracy by model scale.",
                                "The same numbers as paired bars."))
    wanted = fig.get("panels", ("dots", "bars"))
    available = {"dots": (f"{stem}_light.png", caps[0]),
                 "bars": (f"{stem}_bars_light.png", caps[1])}
    chosen = [available[k] for k in wanted]
    if len(chosen) == 1:
        panels = f"\\panelplot{{\\plotdir/{chosen[0][0]}}}"
    else:
        panels = "\n".join(
            f"\\begin{{subfigure}}{{\\linewidth}}\n"
            f"  \\centering\n"
            f"  \\panelplot{{\\plotdir/{png}}}\n"
            f"  \\caption{{{cap}}}\n"
            f"\\end{{subfigure}}{sep}"
            for (png, cap), sep in zip(chosen, ("\\\\[0.7ex]", "")))
    # Two panels plus these notes fill a page, so those go on a [p] float page. One panel
    # does not: on [p] it prints a half-empty sheet, and it is small enough to sit in the
    # text near the paragraph that cites it.
    where = "[p]" if len(chosen) > 1 else "[tbp]"
    return (
        "% Generated by escalation/run_bench_script/make_figures_tex.py -- do not edit.\n"
        "% The caption text lives in that chart's plot script, next to the numbers it\n"
        "% describes; re-run the script to update this file.\n"
        f"\\begin{{figure}}{where}\n"
        "\\centering\n"
        f"{panels}\n"
        f"\\caption{{{mod.CAPTION} "
        # The notes run on from the caption itself, as one paragraph: they are prose
        # about the same chart, and a note per line reads as a list of unrelated
        # remarks. They stay a size down, which is enough to separate them from the
        # title sentence without a break.
        "\\footnotesize\\normalfont\n"
        + " ".join(notes) + "}\n"
        "\\end{figure}\n")


def sources(mod):
    """The rate-source line, set under the rate table, or "" for a module without rates.

    It goes with the table rather than under the chart because the rates are a column of
    that table: the reference belongs beside the numbers it publishes, not beside bars
    that are those numbers already multiplied out. The chart no longer carries it at all -
    both priced figures used to repeat the same line under their panels.
    """
    if not getattr(mod, "SOURCES", None):
        return ""
    # \par first: a tabular is an hbox, so without it the line runs on beside the table
    # instead of under it.
    return f"\\par\\vspace{{0.6ex}}\n{{\\footnotesize {mod.SOURCES}}}\n"


def tabular(header, spec, rows):
    """One booktabs tabular. The rows arrive as LaTeX from the module, so nothing here
    is escaped or reformatted."""
    head = " & ".join(f"\\textbf{{{c}}}" for c in header)
    body = "\n".join(" & ".join(r) + " \\\\" for r in rows)
    return (f"\\begin{{tabular}}{{{spec}}}\n"
            "\\toprule\n"
            f"{head} \\\\\n"
            "\\midrule\n"
            f"{body}\n"
            "\\bottomrule\n"
            "\\end{tabular}\n")


def table_figure_tex(fig, stats):
    """The panel as its own figure float, and the module's tables as their own.

    Returns the two as separate strings, one file each, so the paper can put another
    float between them.

    Measured against a 650pt text block: panel 243pt, caption 106pt, tables 255pt. Kept in
    one float that is 605pt -- 93% of a page -- which only [p] can ever place, so it always
    took a sheet of its own and could never sit beside the paragraphs that read it. Split,
    the figure is 54% and fits at the top of a text page, and the tables (39%) float
    separately to wherever they land.

    Booktabs and the column specs follow the tables already in paper.tex.
    """
    mod = fig["mod"]
    head = (
        "% Generated by escalation/run_bench_script/make_figures_tex.py -- do not edit.\n"
        "% The caption text and the table numbers live in that chart's plot script;\n"
        "% re-run the script to update this file.\n")
    figure = (
        # [!b], not [tbp]: at 54% of the text block the split panel DOES fit beside text,
        # but a top float on the page it is declared on lands above the \S2.2 heading and
        # above the tail of \S2.1 -- the figure printing before the section it belongs to.
        # Bottom placement keeps it after the heading. The ! waives \bottomfraction, which
        # defaults to 30% and would otherwise reject a 54% float outright.
        "\\begin{figure}[!b]\n"
        "\\centering\n"
        f"\\panelplot{{\\plotdir/{slug(mod.TITLE)}_light.png}}\n"
        f"\\caption{{{mod.CAPTION}}}\n"
        "\\end{figure}\n")
    # Real table floats rather than \captionof inside the figure: they carried table
    # numbers before and still do, but now they can be placed independently of the chart.
    # h before b, and no t: paper.tex declares these inside \S2.2, and a top float lands
    # above that heading and above the tail of \S2.1, so the cost tables would print
    # before the section that introduces them. `h` puts them straight under the opening
    # paragraph that quotes their numbers; `b` is the fallback, and pinning them there
    # outright left a half-page of white between the paragraph and Table 3. The ! waives
    # \bottomfraction (30%), which the pair at 39% of the block would otherwise fail.
    # The rate line goes under the first table, which is the one with the rate column;
    # \vspace* on the later ones keeps that footnotesize line from crowding the next
    # caption when the two tables land on the same page (\floatsep does not apply to
    # floats set `h`, so the space has to travel inside the box).
    tables = "\n".join(
        "\\begin{table}[!hb]\n"
        + ("" if i == 0 else "\\vspace*{2ex}\n")
        + "\\centering\n"
        "\\small\n"
        f"\\caption{{{cap}}}\n"
        + tabular(header, spec, rows(stats))
        + (sources(mod) if i == 0 else "") +
        "\\end{table}\n"
        for i, (header, spec, rows, cap) in enumerate(mod.TABLES))
    return head + figure, head + tables


def main():
    for fig in FIGURES:
        stats = fig["mod"].compute()
        if fig.get("table"):
            figure, tables = table_figure_tex(fig, stats)
            for name, body in ((fig["out"], figure), (fig["tables_out"], tables)):
                path = os.path.join(PAPER, name)
                with open(path, "w") as fh:
                    fh.write(body)
                print("wrote", path)
            continue
        pmat = tukey(stats)[0] if fig.get("tukey", True) else None
        path = os.path.join(PAPER, fig["out"])
        with open(path, "w") as fh:
            fh.write(figure_tex(fig, stats, pmat))
        print("wrote", path)


if __name__ == "__main__":
    main()
