
## ideation
Core insight: each final position is independent in cost, so the minimum operations to reach a target final string is just `sum(abs(caption[i]-target[i]))`. The real constraint is structural: the final string’s maximal runs must all have length `>=3`. Thus `n<3` is impossible; for `n>=3` it is always possible by making one run of length `n`.

Main difficulty is not the minimum cost but returning the lexicographically smallest final string among all minimum-cost finals. A DP that only stores costs is insufficient; a DP that stores strings/parents naively can be too heavy or tie-break incorrectly.

The planned run-state DP is sound: state should represent either a boundary/no open run, or an open run `(last_char, run_len_capped_at_3)` where `3` means “length at least 3 and closable.” Transitions: continue same char always allowed; switch to a different char only from capped length `3`; final answer must be closable at `n`. This gives `O(26*3*n)`.

Key pitfalls:
- “Every character appears in groups” means maximal consecutive runs, not total frequency. `aaabaa` is invalid because the trailing `aa` run has length 2.
- Need an explicit boundary/start state; otherwise reconstruction can mishandle the first run or final closing.
- Lexicographic tie-breaking should be done greedily using suffix optimal costs: at each index try `'a'..'z'`, keep the first char whose transition can still achieve the global optimum.
- Python memory is a concern: a full `(n+1) x 79` table of Python ints may be large. Use a flat `array('q')`/similar compact storage, or another memory-conscious reconstruction method.
- INF can be modest: max cost is `25*n <= 1.25e6`, but use something safely larger.
- Validate the claim that impossibility is exactly `n==1` or `n==2`.

## worker: Verify the core lemmas: (1) min operations to reac
Verified the four core lemmas both by proof and by the brute-force checks above.

1. Per-position distance lemma: each operation moves one index by exactly one step on the alphabet line graph `a-b-...-z`. The graph distance between two letters is `abs(ord(x)-ord(y))`, so position `i` needs at least that many operations and exactly that many by always moving toward the target. Positions are independent, so total minimum operations to a fixed target string is the sum of per-position distances.

2. Existence iff `n >= 3`: if `n < 3`, every maximal run has length at most `n < 3`, so no good caption exists. If `n >= 3`, repeating any single letter `n` times creates one maximal run of length `n >= 3`, and it is reachable with finite cost `sum(abs(caption[i]-letter))`.

3. Validity is about maximal consecutive runs, not total frequency. Example: `"aaabaa"` has four total `'a'`s but is invalid because the trailing maximal `"aa"` run has length 2.

4. Capping run length at 3 is sufficient: after a prefix, future feasibility depends only on the current open run’s last character and whether its length is `1`, `2`, or `>=3`. Exact lengths beyond 3 behave identically: continuing the same char keeps the run closable, and switching chars is allowed exactly when the capped length is 3. Cost is additive and already accumulated, so no information is lost by merging all lengths `>=3`.

The verifier exhaustively compares the capped-state DP against brute force for all captions over a 3-letter alphabet up to length 6, plus random spot-checks for lengths 7 and 8.

## worker: Implement backward suffix DP over states {boundary
- Implemented the backward suffix DP exactly as tasked: flat `array('q')` of size `(n+1) * 79` (state 0 = boundary, states `1 + c*3 + (l-1)` = open run of letter `c` with capped length `l ∈ {1,2,3}`). Terminal row `i == n`: boundary and all `(c, 3)` states get cost 0; `(c, 1)`/`(c, 2)` stay `INF`.
- Transitions per position: `(c,1)`/`(c,2)` may only continue (`t == c`); `(c,3)` may continue or close and open any `(t,1)` with `t != c`; boundary opens any `(t,1)`. The `min over t != c of |x-t| + g[i+1][(t,1)]` is computed in O(26) per position via a two-smallest-values trick (use the global min unless its argmin equals `c`, else the second min), so the whole backward pass is `O(n·(26 + 78))` ≈ 2·10⁷ simple ops for `n = 5·10⁴`, with ~31.6 MB of int64 storage.
- The forward min-cost DP is redundant: `g[0][boundary]` is exactly the optimum of the same capped-run transition system that was already brute-force-verified in the workspace (exhaustive on a 3-letter alphabet up to length 6, random at 7–8), so the backward table is correct by the adjoint/reverse-DP argument.
- Reconstruction greedily picks, left to right, the smallest letter `'a'..'z'` whose transition satisfies `dist + g[i+1][next] == remaining_optimum`; the standard exchange argument shows this yields the lexicographically smallest string among all minimum-cost good captions.
- Hand-checked the examples: `"cdcd" -> "cccc"` (cost 2), `"aca" -> "aaa"` (cost 2), `"bc" -> ""` (`n < 3`), `"abc" -> "bbb"` (cost 2), `"zzz" -> "zzz"` (cost 0).

## worker: Add tests: the three examples, n=1/2/3/4/5, alread
- Added a comprehensive test harness under `if __name__ == "__main__":` (the `Solution` class itself is unchanged from the verified implementation).
- **Independent oracle**: `brute_force` enumerates *all* good target strings by splitting `n` into run-length compositions with every part `≥ 3`, assigning letters with adjacent runs distinct, computing the exact per-position distance cost for each candidate, and returning the lexicographically smallest among minimum-cost candidates. This shares no code with the DP, so it is a true cross-check. A safe pruning (partial cost already exceeding the best) speeds it up.
- **Coverage as tasked**:
  - The three statement examples (`cdcd→cccc`, `aca→aaa`, `bc→""`).
  - `n = 1, 2` (impossible → `""`) and assorted `n = 3, 4, 5` cases.
  - Already-good strings (must be returned unchanged, cost 0), including multi-run ones like `"aaabbbcccdddeee"`.
  - All-same strings for every letter at lengths 3 and 10; all-alternating strings (`abab…`, `azaz…`, `cdcd…`).
  - Alphabet-boundary cases: all `'a'`, all `'z'`, and mixed `a/z` strings.
  - Tricky frequency-vs-maximal-run cases (`"aaabaa"`, `"aabaa"`, `"bbaabb"`).
  - **Exhaustive**: every caption over `{a,b,c}` of lengths 3–6 (1080 captions) compared against brute force.
  - **Randomized**: tiny `n` (3–10) with a small alphabet (`abcdez`, includes a boundary letter) and full-alphabet random strings for `n = 3..7`, all vs. brute force.
  - Large-`n` smoke tests: `n = 50000` random strings — asserts the result is good, has correct length, cost is between 0 and the best single-run cost (an always-achievable upper bound), and prints runtime; plus all-`'a'`/all-`'z'`/`"ab"*25000` at max size.
- Every exact check also validates that a nonempty result has length `n` and satisfies the good-caption run property via `is_good`.
- The brute force agrees with the DP on all exhaustive and randomized cases run locally during development; the exhaustive 3-letter check up to length 6 matches the earlier workspace verification of the capped-state DP.
