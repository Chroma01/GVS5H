
## ideation
Core difficulty: this is exactly thresholded Levenshtein distance (`insert/delete/replace` cost 1), but `|S|,|T| <= 500000` makes full `O(nm)` DP impossible. The saving constraint is `K <= 20`, so only a narrow diagonal band around `i=j` can matter: any alignment with `|i-j| > K` already needs more than `K` indels.

Key observations:
- Necessary condition: `abs(len(S)-len(T)) <= K`; otherwise immediate `No`.
- Trimming common prefix/suffix is safe and can massively shrink the instance; handle overlap carefully so the remaining middle parts are well-defined.
- After trimming, if one side is empty, answer is just whether the other length `<= K`.
- Banded DP recurrence is standard edit distance, computed only for `j ∈ [i-K, i+K]`, with values capped at `K+1` as INF. Rolling rows suffice.
- Early abandon is valid: if every in-band cell of a row exceeds `K`, no `<=K` path can pass through that prefix row.

Main pitfalls:
- Python speed: worst-case band is about `(n+m)*(2K+1)` ≈ 20M cells, feasible only with tight loops, bytes input, local variable binding, and no per-row large allocations.
- Memory/indexing: avoid full 2D DP. Either use two full rolling rows but update only the band with careful clearing of boundary cells, or use compact `2K+3` windows with correct offset alignment.
- Off-by-one at band edges: `curr[j-1]`, `prev[j]`, and `prev[j-1]` may lie just outside the valid band and must read as INF.
- Prefix/suffix trimming must not cross each other; after trimming, re-check length difference.
- Do not use generic Myers bit-parallel exact distance blindly; `O(nm/64)` is still far too large for 500k unless combined with a threshold/banded variant.

## worker: Implement a complete first-pass solution: bytes in
- The operation set is exactly Levenshtein distance, so we decide `dist(S,T) <= K`.
- Instead of banded cell-by-cell DP (~20M Python-level cell updates, too slow in CPython), I used the **furthest-reaching diagonal-transition** algorithm (Landau–Vishkin/Myers style):
  - `f_d(k)` = furthest `i` reachable on diagonal `k = i - j` with cost ≤ d.
  - Recurrence: max of substitution (`f_{d-1}(k)+1`), deletion (`f_{d-1}(k-1)+1`), insertion (`f_{d-1}(k+1)`), then extend through free matches ("snake").
  - Only diagonals `|k| ≤ d ≤ K ≤ 20` exist, so at most ~`(K+1)(2K+1) ≈ 861` states total — trivial Python-level work.
- Out-of-grid moves are **rejected** (not clamped); propagation along the `i=n` / `j=m` frontiers still happens correctly via insertion/deletion moves, so no unsound clamping.
- Snake extension (`lcp`) is done with exponential + binary search over `bytes` slice comparisons, which run at C speed; total comparison work is bounded by ~861 × O(n) bytes worst case (sub-second), and typically far less.
- Verified by hand on all three samples plus edge cases (equal strings, single-char substitute, swaps, length-diff rejection, empty-frontier propagation).
