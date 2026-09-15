#!/usr/bin/env python3
"""Single call vs manager, accuracy and cost, LCB-100 x 5 passes at 128k, reasoning ON."""
import json
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle

from plot_16k_reason_off_5_pass import (
    CI_LW, EDGE_LW, FIGSIZE, FS_BODY, FS_SUB, FS_TITLE,
    MARGINS, PLOTS, THEMES,
    apply_theme, fmt_p_num, holm, pass_ci, perm_sign_p, ring, slug, wrap_title, write_figure,
)

import palette

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
RUNS = os.path.join(ROOT, "runs")
VERDICTS = json.load(open(os.path.join(RUNS, "patched_verdicts.json")))
TOKENS = os.path.join(RUNS, "per_problem_tokens.json")
PASSES = [1, 2, 3, 4, 5]

R4 = "4models-1pass-reason-on"
FN = "q38-fn-5pass"

MODELS = [
    ("q38",   (R4, "q38_single_p%d.cap128k"),          (R4, "q38_multiagent_p%d")),
    ("q38fn", (FN, "q38_fn_single_p%d"),               (FN, "q38_fn_multiagent_p%d")),
    ("terra", (R4, "terra_single_p%d"),                (R4, "terra_multiagent_p%d")),
    ("luna",  (R4, "luna_single_p%d"),                 (R4, "luna_multiagent_p%d")),
    ("fable", ("fable5-5pass-single", "fable5_single_p%d"), None),
]

# List $/MTok in, out. ARMS in plot_cost_5_pass.py is the source of truth and carries the
# citations; these must stay in step with it.
RATES = {"q38": (0.214, 2.550), "q38fn": (0.150, 0.470), "terra": (2.0, 12.0),
         "luna": (0.20, 1.20), "fable": (10.0, 50.0)}
CAP = 128_000

# Add a key here to reserve its slot without plotting it, for a run that is still going.
PENDING = set()

TITLE = ("Manager vs single call, five models ranked by manager score "
         "— LCB-100, 5 passes, 128k max tokens, reasoning ON")
TITLE_COST = ("What one pass costs, five models ranked by manager score "
              "— LCB-100, 5 passes, 128k max tokens, reasoning ON")

# suffix picks the pair of fields compute() stores; xlim leaves room past the longest bar
# for its value label, so the axis stops ticking short of it.
FIGURES = [
    dict(suffix="", title=TITLE, xlabel="Accuracy (pass@1, %)", xlim=112,
         xticks=range(0, 101, 20), fmt=lambda v: f"{v:.1f}", ref=lambda v: f"{v:.1f}%"),
    dict(suffix="_cost", title=TITLE_COST, xlabel="Cost of one pass (USD)", xlim=78,
         xticks=range(0, 61, 20), fmt=lambda v: f"${v:.2f}", ref=lambda v: f"${v:.2f}"),
]

BAR_W = 0.36
PITCH = 1.0

FIGSIZE_V = (FIGSIZE[0], FIGSIZE[0] * 0.56)
M6 = dict(MARGINS, left=0.225, right=0.99, top=0.855, bottom=0.175)
TITLE_X = 0.02
LEG_Y = 0.012


# --------------------------------------------------------------------------- data

def load_arm(run, stem):
    qids, rows = None, []
    for p in PASSES:
        arm = stem % p
        base = os.path.join(RUNS, run, "results", arm)
        if os.path.exists(base + ".patched.json"):
            recs = json.load(open(base + ".patched.json"))["lcb"]["records"]
        else:
            # No patched twin written yet; apply the verdicts make_patched_files.py would.
            recs = json.load(open(base + ".json"))["lcb"]["records"]
            verdicts = VERDICTS[run][arm]["verdicts"]
            for r in recs:
                r["passed"] = verdicts[r["question_id"]]
        ids = [r["question_id"] for r in recs]
        if qids is None:
            qids = ids
        assert ids == qids, f"{arm}: id drift"
        rows.append([bool(r["passed"]) for r in recs])
    return qids, np.array(rows, float)


def arm_cost(tok, tok_key, rate):
    ri, ro = rate
    a = np.array(tok[tok_key]["tokens"], float)
    if tok_key == "q38_single":
        # Priced at the 128k cap its accuracy arm is replayed at, not the 250k it ran under.
        a = a.copy()
        a[:, :, 1] = np.minimum(a[:, :, 1], CAP)
        a[:, :, 3] = np.minimum(a[:, :, 3], CAP)
    tin, tout = a[:, :, 0] + a[:, :, 2], a[:, :, 1] + a[:, :, 3]
    return ((tin * ri + tout * ro) / 1e6).sum(axis=1)


def compute():
    tok = json.load(open(TOKENS))
    stats, qids0 = [], None
    for key, s_arm, m_arm in MODELS:
        label = palette.LABELS[key]
        if key in PENDING:
            stats.append(dict(key=key, label=label, pending=True, has_mgr=True))
            continue
        qids, s = load_arm(*s_arm)
        if qids0 is None:
            qids0 = qids
        assert qids == qids0, f"{key}: different problem set"
        sc = arm_cost(tok, f"{key}_single", RATES[key])
        st = dict(key=key, label=label, pending=False, has_mgr=m_arm is not None,
                  single=100 * s.mean(), single_ci=pass_ci(100 * s.mean(axis=1)),
                  single_prob=s.mean(axis=0),
                  single_cost=sc.mean(), single_cost_ci=pass_ci(sc))
        if m_arm is not None:
            _, m = load_arm(*m_arm)
            mc = arm_cost(tok, f"{key}_multi", RATES[key])
            st.update(multi=100 * m.mean(), multi_ci=pass_ci(100 * m.mean(axis=1)),
                      multi_prob=m.mean(axis=0), delta=100 * (m.mean() - s.mean()),
                      multi_cost=mc.mean(), multi_cost_ci=pass_ci(mc))
            _, p, floored = perm_sign_p(m.mean(axis=0) - s.mean(axis=0))
            st.update(p_raw=p, floored=floored)
        stats.append(st)

    tested = [s for s in stats if s["has_mgr"] and not s["pending"]]
    for s, p in zip(tested, holm([s["p_raw"] for s in tested])):
        s["p_holm"] = p

    ref = next(s for s in stats if s["key"] == "fable")["single_prob"]
    for s in tested:
        obs, p, floored = perm_sign_p(s["multi_prob"] - ref)
        s.update(vs_fable=100 * obs, vs_p_raw=p, vs_floored=floored)
    for s, p in zip(tested, holm([s["vs_p_raw"] for s in tested])):
        s["vs_p_holm"] = p
    # Fable 5 has no manager arm and leads as the reference; the rest by manager score, best first.
    return sorted(stats, key=lambda s: (s["has_mgr"], -s.get("multi", 0)))


# --------------------------------------------------------------------------- plot

def draw(stats, fig_cfg, theme="light", save=None):
    sfx, fmt = fig_cfg["suffix"], fig_cfg["fmt"]
    t = THEMES[theme]
    apply_theme(t)
    fig, ax = plt.subplots(figsize=FIGSIZE_V)
    fig.subplots_adjust(**M6)
    ys = [i * PITCH for i in range(len(stats))]
    ax.set(ylim=(ys[-1] + 0.62, -0.62), xlim=(0, fig_cfg["xlim"]))
    ax.set_xlabel(fig_cfg["xlabel"], fontsize=FS_BODY, color=t["ink2"], loc="right")
    ax.xaxis.grid(False)
    ax.yaxis.grid(False)
    ax.set_axisbelow(True)
    ax.set_xticks(fig_cfg["xticks"])
    ax.set_yticks(ys)
    ax.set_yticklabels([s["label"] for s in stats], fontsize=FS_SUB,
                       fontweight="bold", color=t["ink"])
    ax.tick_params(length=0, labelsize=FS_BODY)
    for spine in ("left", "bottom"):
        ax.spines[spine].set_color(t["axis"])

    fable = next(s for s in stats if s["key"] == "fable")["single" + sfx]
    fable_dark = palette.FILLS["fable"][1]
    ax.axvline(fable, ls=(0, (6, 4)), lw=1.6, color=fable_dark, alpha=0.85, zorder=2)

    for y, s in zip(ys, stats):
        light, dark = palette.FILLS[s["key"]]
        if s["pending"]:
            ax.add_patch(Rectangle((0, y - BAR_W), fig_cfg["xlim"], 2 * BAR_W, facecolor=light,
                                   alpha=0.30, edgecolor=ring(dark, theme),
                                   ls=(0, (3, 3)), lw=1.0, zorder=1))
            ax.annotate("run in progress", xy=(fig_cfg["xlim"] / 2, y), ha="center",
                        va="center", fontsize=FS_SUB, style="italic",
                        color=t["muted_text"], zorder=6)
            continue
        arms = [("single", light, BAR_W / 2 if s["has_mgr"] else 0.0)]
        if s["has_mgr"]:
            arms.append(("multi", dark, -BAR_W / 2))
        for arm, fill, dy in arms:
            v, lo, hi = s[arm + sfx], *s[f"{arm}{sfx}_ci"]
            yb = y + dy
            bar = palette.bar_kw(s["key"], "manager" if arm == "multi" else "single",
                                 surface=t["surface"])
            bar.setdefault("edgecolor", ring(fill, theme))
            ax.barh(yb, v, BAR_W, linewidth=EDGE_LW, zorder=3, **bar)
            ax.plot([lo, hi], [yb, yb], color=ring(fill, theme), lw=CI_LW, zorder=5,
                    solid_capstyle="round")
            for cap in (lo, hi):
                ax.plot([cap, cap], [yb - 0.08, yb + 0.08], color=ring(fill, theme),
                        lw=CI_LW, zorder=5)
            ax.annotate(fmt(v), xy=(hi, yb), xytext=(5, 0), textcoords="offset points",
                        ha="left", va="center", fontsize=FS_SUB, color=t["ink"], zorder=6,
                        bbox=dict(facecolor=t["surface"], edgecolor="none",
                                  boxstyle="square,pad=0.10"))

    def swatch(colour):
        return Line2D([], [], marker="o", ls="", ms=12, color=colour,
                      markeredgecolor=ring(colour, theme), markeredgewidth=EDGE_LW)

    pale, deep = ("#d5d4cd", "#6f6d67") if theme == "light" else ("#b8b6ae", "#5e5c57")
    key = [(swatch(deep), "with manager"),
           (swatch(pale), "single call"),
           (Line2D([], [], ls=(0, (6, 4)), lw=1.6, color=fable_dark),
            f"Fable 5 single call, {fig_cfg['ref'](fable)}")]

    fig.suptitle(wrap_title(fig_cfg["title"]), x=TITLE_X, ha="left", y=0.99, va="top",
                 fontsize=FS_TITLE, fontweight="bold", color=t["ink"], linespacing=1.25)
    leg = fig.legend([h for h, _ in key], [n for _, n in key], loc="lower center",
                     bbox_to_anchor=(0.5, LEG_Y), ncol=len(key), frameon=False,
                     fontsize=FS_SUB, labelcolor=t["ink2"], handletextpad=0.7,
                     handlelength=2.2, columnspacing=2.8)
    fig.add_artist(leg)
    if save:
        write_figure(fig, save)
    return fig


# --------------------------------------------------------------------------- stdout

COLS = (20, 18, 18, 8, 11, 9, 11)
HEAD = ("model", "single call", "with manager", "delta", "Holm p", "vs Fable", "Holm p")
COST_COLS = (20, 15, 15, 11)
COST_HEAD = ("model", "$/pass single", "$/pass manager", "manager x")


def row(cells, cols=COLS):
    return "  ".join(c.rjust(w) if i else c.ljust(w) for i, (c, w) in enumerate(zip(cells, cols)))


def ci_txt(mean, ci):
    return f"{mean:5.1f} [{ci[0]:4.1f},{ci[1]:5.1f}]"


def report(stats):
    line = "-" * (sum(COLS) + 2 * (len(COLS) - 1))
    print("\nLCB-100, 5 passes, 128k cap, reasoning on.")
    print("delta vs the model's own single call; vs Fable is the manager against Fable 5's single call.")
    print("p: paired sign-flip permutation test, unit = problem (n = 100, 200k resamples),")
    print(f"   Holm-corrected within each family of {sum(1 for s in stats if s['has_mgr'] and not s['pending'])};"
          " < marks the permutation floor.\n")
    print(row(HEAD))
    print(line)
    for s in stats:
        if s["pending"]:
            print(row((s["label"], "run in progress", "run in progress", "-", "-", "-", "-")))
        elif s["has_mgr"]:
            print(row((s["label"], ci_txt(s["single"], s["single_ci"]),
                       ci_txt(s["multi"], s["multi_ci"]), f"{s['delta']:+.1f}",
                       fmt_p_num(s["p_holm"], 2, s["floored"]), f"{s['vs_fable']:+.1f}",
                       fmt_p_num(s["vs_p_holm"], 2, s["vs_floored"]))))
        else:
            print(row((s["label"], ci_txt(s["single"], s["single_ci"]),
                       "- (single only)", "-", "-", "reference", "-")))
    print(line)

    cline = "-" * (sum(COST_COLS) + 2 * (len(COST_COLS) - 1))
    print("\nlist rates, no cached-input or batch discount; mean over the 5 passes.\n")
    print(row(COST_HEAD, COST_COLS))
    print(cline)
    for s in stats:
        if s["pending"]:
            continue
        mgr = f"${s['multi_cost']:.2f}" if s["has_mgr"] else "-"
        mult = f"{s['multi_cost'] / s['single_cost']:.1f}x" if s["has_mgr"] else "-"
        print(row((s["label"], f"${s['single_cost']:.2f}", mgr, mult), COST_COLS))
    print(cline)


def main():
    stats = compute()
    report(stats)
    os.makedirs(PLOTS, exist_ok=True)
    for cfg in FIGURES:
        draw(stats, cfg, "light",
             save=os.path.join(PLOTS, f"{slug(cfg['title'])}_bars_light.pdf"))


if __name__ == "__main__":
    main()
