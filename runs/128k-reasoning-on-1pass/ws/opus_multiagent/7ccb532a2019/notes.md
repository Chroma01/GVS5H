
## ideation
**Restating.** All three ops cost 1: delete, insert, and `c -> c+1` (no wraparound at 'z'). Final string must have every *present* letter appearing the same number of times. So the final configuration is characterized by a target frequency `t ≥ 1` and a subset `K ⊆ {a..z}` of "kept" letters, each ending with exactly `t` copies; every other letter ends with 0.

**Core difficulty.** The `c -> c+1` op couples adjacent letters: a surplus char of letter `i` can be *reused* to fill a deficit of letter `i+1` at cost 1 instead of paying 2 (delete + insert). So the cost is not simply `sum |cnt[i] - T_i|`; it's a chain/flow problem along the alphabet order (one direction only, and 'z' has no successor).

**Key cost lemma (why a simple DP works).** Let `sur_i` = number of chars that must leave letter `i` and `def_{i+1}` = number that must be added to letter `i+1`. Each departing char costs exactly 1 whether it is deleted or shifted; shifting one of them into `i+1` simultaneously satisfies one unit of deficit. Hence the cost attributed to the pair is
`sur_i + max(0, def_{i+1} - sur_i) = max(sur_i, def_{i+1})`.
Crucially, **multi-hop shifting never helps**: moving a char from `i` to `i+2` costs 2 shifts = delete(1)+insert(1) = 2. So only adjacent transfers matter, and a 2-state DP over the 26 letters is exact (equality, not strict improvement, for longer chains — worth double-checking with brute force).

**DP for fixed `t`.** States: letter `i` kept (final count `t`) or dropped (final count 0).
- `sur(i, keep) = max(0, cnt[i] - t)`, `sur(i, drop) = cnt[i]`
- `def(i, keep) = max(0, t - cnt[i])`, `def(i, drop) = 0`
- Init: `dp[0][drop] = 0`, `dp[0][keep] = def(0, keep)` (nothing precedes 'a', so its deficit must be pure inserts). Surplus of a letter is charged on the transition to the next letter.
- Transition: `dp[i+1][s'] = min_s dp[i][s] + max(sur(i,s), def(i+1,s'))`.
- Finish: `ans_t = min_s dp[25][s] + sur(25, s)` ('z' surplus can only be deleted).

**Range of `t`.** `1..max(cnt)`. For `t > max(cnt)` every kept letter is pure deficit and every dropped letter's cost is `cnt` (independent of `t`), so cost is non-increasing as `t` decreases to `max(cnt)`. Also seed the answer with `n` (delete everything → empty string is vacuously good), though min over `t` never exceeds that.

**Complexity.** `26 · 4 · max(cnt) ≤ 26·4·2·10⁴ ≈ 2·10⁶` cheap ops — fine in Python if the inner loop is kept tight (two scalars `dp0, dp1`, precomputed `cnt` list, no allocations inside).

**Pitfalls to watch.**
- Charging a letter's surplus twice (once at its own step and once at the transition) or forgetting 'z''s surplus at the end.
- Forgetting that letters with `cnt = 0` may still be "kept" (cost `t` inserts, or fed by predecessor's surplus) — the DP allows it naturally; don't restrict to letters present in `s`.
- Dropped letter still has surplus `cnt[i]` that can be *shifted forward* into the next letter's deficit (Example 1 variant: drop 'b' by turning it into 'c'). Don't set the drop-state cost to a plain delete.
- `def(i, drop)` must be 0 (never "fill" a dropped letter).
- Ensure `t ≥ 1` and handle `max(cnt)` correctly.
- Order matters: transitions only `i -> i+1`, never backwards.

## worker: *Task 1+2 (implement):** Write the full `class Sol
Implemented exactly the planned DP.

- `cnt[26]` frequencies; baseline `best = n` (delete everything).
- For each target frequency `t` in `1..max(cnt)`, a 26-step 2-state DP (`keep` → final count `t`, `drop` → final count 0).
- Per-letter quantities: `sur(i,keep)=max(0,cnt[i]-t)`, `sur(i,drop)=cnt[i]`, `def(i,keep)=max(0,t-cnt[i])`, `def(i,drop)=0`.
- Init at 'a': `dp_drop=0`, `dp_keep=def(0,keep)` (no predecessor, so its deficit is pure inserts).
- Transition cost `dp[i][s] + max(sur(i,s), def(i+1,s'))`: every departing char costs 1 whether deleted or shifted to `i+1`, and shifting simultaneously satisfies a unit of the next letter's deficit; leftover deficit is filled by inserts. Multi-hop shifts never beat delete+insert (2 shifts = 2 ops), so only adjacent transfers matter and the 2-state chain DP is exact.
- Finalize with `min(dp_keep + sur(z,keep), dp_drop + sur(z,drop))` since 'z' surplus can only be deleted.

Verified by hand on all three samples: "acab" → 1, "wddw" → 0, "aaabc" → 2 (achieved at both `t=1` and `t=3`).

Complexity: `O(26 · max(cnt))` ≈ 5.2·10⁵ scalar operations worst case, with no allocations in the inner loop; memory `O(1)`.

Edge cases covered: letters with `cnt=0` may still be kept (deficit filled by inserts or by predecessor surplus); dropped letters' chars can still be shifted forward into the next letter's deficit; `t` never exceeds `max(cnt)` since for larger `t` the cost is non-increasing as `t` decreases toward `max(cnt)`.
