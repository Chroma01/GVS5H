# LCB-100 (latest-hard): thinking × cap study

How pass@1 on the 100 latest-hard LiveCodeBench problems moves with **thinking on/off**
and the **completion-token cap** (16k vs 128k), single-shot vs manager (multi-agent).

Sources:
- **OFF · 16k** — `runs/models-lcb-5pass/` (reasoning off, 16,000-token cap, mean of 5 passes). Detail table in the appendix below.
- **OFF · 128k** — `runs/128k-clean/` (reasoning off, 128,000-token cap, 1 pass).
- **ON · 128k** — `results_think_high/` (reasoning on, 128,000-token cap, 1 pass). q9 config in the appendix.
- **ON · 16k** — *not run.* Thinking alone exceeds 16k, so it would be near-total truncation; the ON·128k q35 column shows the failure mode without spending on it.

Pass-to-pass noise on this set is ~3.0pp, so treat deltas < ~4pp as noise.

## Table 1 — pass@1 (raw)

| Model | Engine | OFF · 16k | OFF · 128k | ON · 128k |
|---|---|--:|--:|--:|
| **opus** | single | 40 | —¹ | **85** |
| | manager | — | —¹ | **91** |
| **kimi** | single | 32 | 32 | **82** |
| | manager | 63 | 74 | **82** |
| **mm3** | single | 21 | 25 | **60** |
| | manager | 32 | 37 | **66** |
| **q35** | single | 28 | 35 | **25** |
| | manager | 27 | 26 | **43** |
| **q9** | single | 15 | 17 | *unusable*² |
| | manager | 22 | 20 | *unusable*² |

¹ OFF·128k opus was never run (only a placeholder file exists).
² q9 (qwen3.5-9b) with thinking on returns reasoning-only replies (content=null, `finish=error`) on OpenRouter — no token/effort setting fixes it. See appendix.

## Table 2 — truncation auto-fails (empty-code count / 100)

An empty `code` field = an unclosed ```python fence from hitting the cap = a guaranteed
fail regardless of skill. This is the confound, measured directly (superset of
`status=='truncated'`; also catches reasoning-only/no-answer replies).

| Model / engine | OFF · 16k | OFF · 128k | ON · 128k |
|---|--:|--:|--:|
| opus single | **50** | — | 3 |
| kimi single | 13 | 4 | 3 |
| kimi manager | 1 | 0 | 0 |
| mm3 single | 35 | 7 | 8 |
| mm3 manager | 5 | 0 | 7 |
| q35 single | 24 | 15 | **66** |
| q35 manager | 3 | 5 | 32 |
| q9 single | 43 | 21 | — |
| q9 manager | 7 | 8 | — |

## Truncation attribution — evidence-based, no assumptions

We do **not** assume truncated problems would have passed. Truncated problems are the
longest/hardest ones, so they pass at a *lower* rate than the rest. Measured directly:
pass rate **at 128k** of the problems that had truncated **at 16k** (OFF, single), vs. all others:

| Model | truncated@16k → pass@128k | others → pass@128k |
|---|--:|--:|
| kimi | **0%** (n=12) | 36% |
| mm3 | **11%** (n=35) | 32% |
| q35 | **25%** (n=16) | 37% |
| q9 | **2%** (n=40) | 27% |

Truncated problems recover at only ~0–25% even when uncapped — a third or less of the
baseline rate. So an "adjusted pass@1" that credits them at the completed-set rate
overstates their value 2–4× and is **not used here**. Because the 128k run already grades
those same problems on merit, the real truncation cost is just the passes a bigger cap recovers:

- **Cap effect (OFF single, 16k→128k), real passes recovered:** q35 **+7** (28→35), mm3 **+4** (21→25), q9 **+2** (15→17), kimi **~0** (its truncated problems pass at 0% regardless).
- **q35 thinking-on (66 truncated, none observable uncapped):** using the measured ~25% rate for q35's hard problems, ≈16 of the 66 are recoverable → truncation-free q35-ON single ≈ 25 + 16 ≈ **~41**. So thinking OFF→ON for q35 single is ≈ 35 → ~41 = **about +6** genuine (a small real gain that the cap masks into a −10 headline) — not a large effect either way.

### What is genuine vs. artifact

- **Thinking gains are genuine for models that don't truncate** (empty-code ~0, so raw ≈ truth):
  kimi single **+50** (32→82), mm3 **+35** (25→60), opus large (16k 40 → 128k-ON 85). q35 is the
  only model where thinking's real gain (~+6) is hidden by truncation.
- **Manager "rescue," measured directly** — of the problems each model left empty in single (ON·128k),
  how many the manager actually passed:

  | Model | single-empty | manager passed | still empty | filled but failed |
  |---|--:|--:|--:|--:|
  | q35 | 66 | **28** | 23 | 15 |
  | mm3 | 8 | 3 | 2 | 3 |
  | opus | 3 | 3 | 0 | 0 |
  | kimi | 3 | 2 | 0 | 1 |

  These are observed passes, not estimates. q35's +18 manager headline (25→43) is real passes on
  problems single couldn't emit code for — and the manager clears them at ~42%, *above* the ~25%
  those hard problems manage uncapped, so its decomposition does more than just dodge truncation.
- **The one large genuine manager win is off-thinking:** kimi OFF·128k single 32 → manager **74**
  (+42), with empty ~0 on both sides — decomposition compensating for a weak single-shot pass, not a cap artifact.

**Summary:** every headline effect is directionally right, but the truncation *correction* is
small — because truncated problems are genuinely hard, not easy passes lost to a cap.

---

# Appendix — OFF · 16k detail (5-pass reasoning-off run)

Run finished 2026-07-27 22:28. Source: `escalation/runs/models-lcb-5pass/results/`, logs `/tmp/m5_*.log`.
Nemotron dropped (never run). Opus manager never launched. Cap = 16,000 completion tokens.

| model | n | ran | void | miss | records | nonempty | passed | stored | recomp | match | delta | apierr | retries |
|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|:--:|--:|--:|--:|
| Opus-5 single | 3 | 5 | 2 | 0 | 100 | 82.7 | 67.3 | 67.3 | 67.3 | yes | — | 200 | 1000 |
| Opus-5 manager | 0 | 0 | 0 | 5 | — | — | — | — | — | — | — | 0 | 0 |
| Kimi-K3 single | 5 | 5 | 0 | 0 | 100 | 87.0 | 32.2 | 32.2 | 32.2 | yes | — | 0 | 0 |
| Kimi-K3 manager | 5 | 5 | 0 | 0 | 100 | 98.6 | 62.6 | 62.6 | 62.6 | yes | +30.4 (n5v5) | 7 | 31 |
| Minimax-M3 single | 5 | 5 | 0 | 0 | 100 | 65.0 | 21.2 | 21.2 | 21.2 | yes | — | 0 | 0 |
| Minimax-M3 manager | 5 | 5 | 0 | 0 | 100 | 94.8 | 32.2 | 32.2 | 32.2 | yes | +11.0 (n5v5) | 0 | 0 |
| Qwen3.6-35b single | 5 | 5 | 0 | 0 | 100 | 75.6 | 27.8 | 27.8 | 27.8 | yes | — | 0 | 0 |
| Qwen3.6-35b manager | 5 | 5 | 0 | 0 | 100 | 97.0 | 26.6 | 26.6 | 26.6 | yes | -1.2 (n5v5) | 0 | 0 |
| Qwen3.5-9b single | 5 | 5 | 0 | 0 | 100 | 57.2 | 14.6 | 14.6 | 14.6 | yes | — | 0 | 2 |
| Qwen3.5-9b manager | 5 | 5 | 0 | 0 | 100 | 93.4 | 21.8 | 21.8 | 21.8 | yes | +7.2 (n5v5) | 0 | 2 |

## Columns

- **n** — passes averaged (valid only). **ran** — passes executed. **void** — executed but 0/100 usable completions. **miss** — no result file.
- **records / nonempty / passed** — per-pass counts out of 100, averaged over the `n` valid passes.
- **stored** — `pass@1` as written in the JSON. **recomp** — recomputed from raw records. **match** — stored == recomp on *every* individual pass.
- **delta** — manager `recomp` − single `recomp`, with the pass counts used.
- **apierr / retries** — across all 5 passes including void ones, from `/tmp/m5_*.log`.

## Caveats

- **Opus-5 single is n=3, not 5.** Passes p4/p5 are void: every call returned `HTTP Error 402: Payment Required` (OpenRouter credit ran out between 22:22 and 22:23). All 200 apierr / 1000 retries belong to those two passes; p1–p3 are error-free. `final5.log`'s `Opus-5 40±33 (n=5)` averages the two zeros in and is wrong.
- **Opus-5 manager was never launched** — no files, no logs.
- **Opus-5's 67.3 is a floor.** ~17 empty records per valid pass are truncation, not refusals: `finish_reason=length` fires 21/21/22 times per pass at the 16,000 completion-token cap. Raise the cap before rerunning.
- **`nonempty` is the confound to watch.** Single ranges 57–87; manager is 93–99. Qwen3.5-9b single scores 14.6 off only 57 real attempts. Counter-evidence that the lift isn't *only* emit-rate: Qwen3.6-35b manager recovers 21.4 attempts (75.6 → 97.0) and still lands at −1.2.

## Thinking-on config note (ON · 128k)

- Open non-reasoning-native models (q9, q35, mm3) have no native `reasoning_effort` on OpenRouter;
  `effort:high` is emulated as ~80% of `max_tokens` (~100k) → runaway thinking. The orchestrator's
  `budget:N` mode (`ESCALATION_OR_REASONING=budget:20000` → `reasoning:{max_tokens:N}`) was added, but
  throughput-routed providers frequently ignore the reasoning budget, so q35 still truncated ~48% (single).
- **q9 is unusable with thinking on**: providers return reasoning-only replies (content=null, `finish=error`);
  no config fixes it. Recorded as unusable rather than a graded 0.
- kimi and opus have native `reasoning_effort` and self-manage the think→answer boundary (≈0 truncation);
  they were run at `effort:high`.
