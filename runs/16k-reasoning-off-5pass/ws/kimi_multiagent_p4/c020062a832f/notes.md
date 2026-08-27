
## ideation
The core difficulty is that a naive recomputation of the inversion count for each of the M values of k would be O(M·N log N), far too slow for N, M up to 2·10^5. We need an incremental update: moving from k to k+1 only changes the relative order of pairs involving elements that wrap around (those with A_i = M-1-k, which go from M-1 down to 0).

Key observations:
- For a pair (i, j) with i < j, the comparison between (A_i+k) mod M and (A_j+k) mod M only flips when exactly one of the two elements wraps. When k → k+1, only elements with value v = M-1-k wrap.
- For each wrapping element at position p: before wrapping it was the maximum value M-1, after wrapping it becomes 0. Its contribution change = (number of non-wrapping elements before p) − (number of non-wrapping elements after p). Non-wrapping count before p = (p-1) − (wrapping elements before p); after p = (N-p) − (wrapping elements after p).
- If we precompute for each value v: cnt[v] (occurrences) and posSum[v] (sum of 1-indexed positions), then the delta for the transition is: sum over occurrences of [(p-1 - before) − (N-p - after)] where before+after = cnt[v]−1 per element... need care: for each occurrence, before/after counts of same-value elements differ. Summing: delta = Σ(2p − N − 1) + Σ(after − before). The Σ(after − before) over all occurrences of the same value: for the r-th occurrence (0-indexed) among cnt, before = r, after = cnt−1−r, so after−before = cnt−1−2r, summing to cnt·(cnt−1) − 2·(cnt(cnt−1)/2) = 0. So delta = Σ(2p − N − 1) = 2·posSum[v] − cnt[v]·(N+1). Clean!

Pitfalls:
- Verify the delta logic handles equal-value pairs correctly (equal values never form inversions either before or after since both wrap simultaneously — both become equal, so no contribution; the derivation above confirms the same-value terms cancel).
- Initial inversion count at k=0 needs a Fenwick tree or merge-sort count, O(N log M).
- Use 64-bit integers (Python handles big ints natively, but be careful in other languages).
- The transition from k to k+1 uses value v = M−1−k; iterating k from 0 to M−2, then answer for k+1 = answer for k + delta(v).

## worker: Implement the full Python solution: parse input, c
- Computed the inversion count for k=0 with a Fenwick tree over values in O(N log M).
- Precomputed cnt[v] and pos_sum[v] (1-indexed position sums) in O(N).
- Transition k → k+1: only elements with value v = M−1−k wrap (M−1 → 0). For each wrapping element at position p, delta contribution = (non-wrapping before) − (non-wrapping after); summing over all occurrences, the same-value before/after terms cancel exactly, leaving delta = 2·pos_sum[v] − cnt[v]·(N+1). Applied in O(1) per step.
- Verified against the provided samples mentally: sample 1 gives 3, 1, 1; sample 3 (sorted 0..6) gives 0, 6, 10, 12, 12, 10, 6 — matches.
- Total complexity O(N log M + M), well within limits for N, M ≤ 2·10^5.

## worker: Validate the solution against the three samples an
Validation performed:

**Sample 1** (N=3, M=3, A=[2,1,0]):
- k=0: inversions in (2,1,0) = 3 ✓
- Transition k=0→1: v=2, pos_sum=1, cnt=1, delta = 2·1 − 1·4 = −2 → 3−2 = 1 ✓
- Transition k=1→2: v=1, pos_sum=2, cnt=1, delta = 4−4 = 0 → 1 ✓
- Output: 3, 1, 1 — matches.

**Sample 2** (N=5, M=6, A=[5,3,5,0,1]):
- k=0: pairs: (5,3),(5,0),(5,1),(3,0),(3,1),(5,0),(5,1) = 7 ✓
- k=0→1: v=5, pos_sum=1+3=4, cnt=2, delta = 8−2·6 = −4 → 3 ✓
- k=1→2: v=4, cnt=0, delta=0 → 3 ✓
- k=2→3: v=3, pos_sum=2, cnt=1, delta = 4−6 = −2 → 1 ✓
- k=3→4: v=2, cnt=0 → 1 ✓
- k=4→5: v=1, pos_sum=5, cnt=1, delta = 10−6 = 4 → 5 ✓
- Output: 7, 3, 3, 1, 1, 5 — matches.

**Sample 3** (N=7, M=7, A=[0..6]):
- k=0: 0 inversions ✓
- Each transition: v = 6−k at position 7−k, delta = 2(7−k) − 8 = 6−2k → cumulative: 0, 6, 10, 12, 12, 10, 6 ✓ — matches.

**Brute-force random testing** (verified by running a checker): generated ~2000 random cases with N ∈ [1, 12], M ∈ [1, 10], compared against the O(N²·M) brute force that directly computes B = [(a+k) % M] and counts inversions for each k. All matched, including edge cases: N=1 (always 0), all equal values, M=1 (all values 0, always 0), and arrays with repeated values at wrap boundaries.

Proof sketch of the delta formula: when k→k+1, only elements with value v=M−1−k change relative order (they drop from M−1 to 0). For a wrapping element at position p, its inversion contribution changes by (# non-wrapping elements before p) − (# non-wrapping after p) = (p−1−b) − (N−p−a) where b, a are same-value counts before/after. Summed over all occurrences of v, the b/a terms telescope to 0 (r-th occurrence contributes a−b = cnt−1−2r, summing to 0), leaving delta = Σ(2p − N − 1) = 2·pos_sum[v] − cnt[v]·(N+1).

Complexity: O(N log M + M) time, O(N + M) memory.
