
## ideation
The core difficulty: we need to minimize the maximum run length after at most `numOps` arbitrary bit flips. This is a decision problem (is a given max run length `L` achievable?) combined with optimization (find the smallest feasible `L`).

Key insight: For a fixed target max run length `L`, to break a run of identical bits of length `len` into pieces of length at most `L`, we need to flip at least `ceil(len / (L+1))` characters within that run (place a flipped bit every `L+1` positions). The flips needed across all runs sum to the minimum required flips. If this sum ≤ `numOps`, `L` is feasible.

The decision is monotonic in `L` (if `L` works, any larger `L` also works), so we can binary search on `L` from 1 to `n`.

Alternative DP: DP on positions with state of current run length, but that's O(n^2 * nOps) = O(n^3), too slow. The greedy split-by-pieces approach is optimal and simple.

Pitfalls:
- Edge case `L = 0`: impossible unless string is empty (n≥1), so search from 1 to n.
- Single runs of length 1 need 0 flips (ceil(1/(L+1)) = 1? No, ceil(1/2)=1 — wait, that's wrong for L=1. Let's verify: a run of length 1 with L=1: pieces of length ≤1, so the piece itself is length 1, no flip needed. Formula: we need at most L consecutive identical. If len ≤ L, 0 flips. The placement of flips every L+1 gives: floor((len-1)/(L+1)) + 1? Actually, to split len into chunks of max size L, we need at least ceil(len/L) - 1 flips (cut after every L characters). Equivalent: ceil(len/(L+1)) flips needed. Check: len=1, L=1: ceil(1/2)=1 — but 0 flips suffice since the run is already length 1 ≤ L. So the formula is: `max(0, ceil(len/(L+1)))` but for len=1, L=1 this gives 1, wrong.

Correction: The number of pieces after splitting a run of length `len` into pieces of length ≤ `L` is `ceil(len/L)`. The number of flips (cuts) needed is `pieces - 1 = ceil(len/L) - 1`. For len=1, L=1: ceil(1/1)-1 = 0. ✓ For len=5, L=2: ceil(5/2)-1 = 3-1=2. Place flipped bits at positions 2 and 4 (1-indexed) to get pieces [0,1], [3], [5] with max length 2. ✓

So correct formula: `max(0, ceil(len/L) - 1)`.

- numOps can be 0: must verify feasibility only with 0 flips.
- n ≤ 1000: O(n log n) is trivial.

## worker: Implement the `minLength` method with binary searc
The solution uses binary search on the target maximum run length `L`. For each candidate `L`, we greedily compute the minimum number of flips required by scanning all maximal runs of identical characters. A run of length `run_len` needs `ceil(run_len / L) - 1` flips to be split into pieces of length at most `L` (placing flipped bits at positions `L, 2L, ...` within the run). If `run_len <= L`, no flips are needed. The decision is monotonic: if `L` is feasible, any larger `L` is also feasible. Binary search over `L ∈ [1, n]` yields the minimum feasible value. Complexity is `O(n log n)`, well within the `n ≤ 1000` constraint. Edge cases (numOps = 0, single-character runs, all-identical strings) are handled correctly by the formula.
