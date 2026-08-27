
## ideation
- Core difficulty: combine weighted interval scheduling DP (n up to 5e4, k up to 4) with lexicographic tie-breaking on the chosen index list. The DP must track not just max weight but the lexicographically smallest index sequence achieving it.
- Key observations:
  - Sort intervals by right endpoint; for each interval i, find p(i) = last interval (in sorted order) with r < l_i via binary search. Note: sharing an endpoint counts as overlapping, so we need r_prev < l_i (strict).
  - DP[i][k] = best (weight, index-list) using intervals among first i sorted intervals, choosing exactly/at most k. Recurrence: skip interval i-1, or take it (combine with DP[p(i)][k-1]).
  - Lexicographic comparison of index lists: when weights tie, compare lists element-wise; shorter prefix list is smaller. Since all weights positive, max weight will use as many intervals as beneficial, but ties can occur between different counts (e.g., weight 5 with 1 interval vs 3+2 with 2). Comparing full lists handles this.
  - Indices in the output refer to original indices; sorted order preserves increasing right endpoints, and chosen indices will naturally be appended in sorted order, but the output list must be the indices in increasing order? Check examples: Example 2 output [1,3,5,6] — sorted ascending. Since we pick intervals in chronological order, indices may not be ascending automatically (original indices arbitrary vs sorted order). Wait — lexicographic comparison is on the index array as returned; the problem implies the returned array lists indices of chosen intervals. Examples show ascending order. Need to confirm: chosen set's indices sorted ascending is the canonical form. Lexicographic comparison across different sets: compare sorted index lists. So we should compare/store sorted index lists. But careful: DP builds lists in chronological order; the lexicographic comparison should be on sorted-ascending index lists. Taking interval i appends its original index; the list may not be sorted ascending. Safer: store tuple of indices in the order chosen (chronological), but compare as sorted? Hmm — the answer array is just "array of indices"; examples output ascending. The lexicographic comparison presumably applies to the returned array, which we can output sorted ascending. To minimize lexicographically, we want the smallest first index, etc. The DP tie-break should compare the final sorted lists. Since appending happens chronologically, two candidate lists differ; comparing them as sorted tuples is correct only if we sort. Simplest: store the tuple as built (chronological), and at comparison time compare sorted versions? That could be inconsistent during DP (prefix comparisons). Alternative: note that lexicographic minimum of final sorted list is achieved by greedy earliest-index choices; a cleaner known approach (LeetCode 3001-ish "maximum weight" problem) does DP storing path and compares tuples directly where path is built in sorted-by-right order but with original indices... Actually in the known problem (LC "Maximum Total Weight..." / similar), the path comparison uses the list of original indices in the order selected, and the answer is expected sorted? In LC 3418 (Maximum Amount of Money... no). Let me think: this is LC 3001? It's "Find the Lexicographically Smallest Array..." no. It's LC 3418? The known problem "maximumWeight" with up to 4 intervals is LC 3418 "Maximum Amount of Money Robot Can Earn"? No — it's LC 3001? Actually it's LC 3418... The known accepted approach: sort by end, DP with (k) dimension, store path list, compare (weight, path) where path compared lexicographically as-is (chronological order of selection), and output path sorted? In the known problem, output is the list of indices in increasing order because... In example 2, chronological selection by right endpoint: intervals sorted by right: idx6 [3,5,5], idx2 [4,7,3], idx1 [6,7,7], idx4 [7,8,2], idx0 [5,8,1], idx3 [9,10,6], idx5 [11,14,3]. Chosen: 6,1,3,5 chronologically → output [1,3,5,6] sorted. So output must be sorted ascending. Lexicographic comparison on sorted lists. During DP, comparing candidate solutions: compare (weight, sorted tuple). Storing sorted tuple at each state is fine since appending then sorting small lists (≤4) is cheap.
  - Pitfalls:
    - Overlap rule: r_prev < l_i strictly (boundary touch = overlap). Binary search with bisect_left on rights for l_i - 1, i.e., bisect_left(rights, l_i).
    - n=5e4, k≤4 → DP table 5e4×5 storing tuples; memory fine if we store only best per state, but reconstruction via stored parent pointers or storing tuples directly (each ≤4 ints) is fine: 250k tuples.
    - Comparison cost: tuples ≤4 elements, cheap.
    - "Up to 4": answer can be fewer; with positive weights, more intervals always add weight, but feasibility may limit. Take best over k=0..4 at final state.
    - Use (weight, negated?) — we compare weight descending, tuple ascending; implement custom compare.
    - Duplicate intervals / same endpoints: stable sort fine; p(i) must exclude itself (search among indices < i).
    - Large weights: sum up to 4e9, fits in Python int trivially.
- Complexity: O(n log n + n*k*L) where L≤4 tuple compare → effectively O(n log n).

## worker: Implement the full solution: sort intervals by rig
- **Algorithm**: Weighted interval scheduling with at most 4 picks.
  - Sort intervals by right endpoint; `prev[j]` via `bisect_left(rights, l_j, 0, j)` gives the count of earlier sorted intervals ending strictly before `l_j` (boundary touch = overlap, hence strict `<`).
  - `dp[j][k]` stores `(max_weight, lexicographically_smallest_sorted_index_tuple)` over the first `j` sorted intervals choosing exactly `k`. Transition: skip interval `j-1`, or take it and extend `dp[prev[j-1]][k-1]`.
  - Comparison: higher weight wins; on tie, the smaller sorted tuple wins (Python tuple comparison matches the spec: element-wise, shorter prefix is smaller).
  - Final answer: best over `dp[n][0..4]`.
- **Correctness on examples**:
  - Example 1: best weight 8 from indices {2,3} → `[2,3]`. ✓
  - Example 2: best weight 21 from {1,3,5,6} → `[1,3,5,6]`. ✓
- **Edge cases handled**:
  - Single interval → returns `[0]`.
  - All mutually overlapping with equal weights → picks the single lowest-index one (weight tie, lexicographic comparison across different cardinalities: e.g., `(5, (0,))` vs `(5, (1,))` → `(0,)`; also `(5,(0,))` beats `(5,(0,1))`? No — weights differ there since positive weights make 2 intervals weight 10 > 5, so cardinality ties only arise when total weights are equal, handled by tuple compare).
  - Lexicographic tie across cardinalities, e.g., weight 5 via one interval index 3 vs 2+3 via indices 0,4 → compares `(3,)` vs `(0,4)` → `(0,4)` wins, matching spec (first differing element 0 < 3).
  - Tuple kept sorted ascending at each step (≤4 elements, sorting is O(1)); the stored tuple is exactly the canonical output form, so prefix-based DP comparisons remain consistent with final comparison.
- **Complexity**: O(n log n) for sorting + binary searches; DP is O(n·K) with O(K log K) tuple ops (K=4) → effectively O(n log n) time, O(n·K) space. n = 5·10⁴ is fine.

## worker: Test the implementation against both provided exam
- Verified the DP implementation against both provided examples: `[2,3]` and `[1,3,5,6]` — both pass.
- Added a brute-force checker (all subsets of size ≤ 4, inclusive-boundary overlap test `max(l1,l2) <= min(r1,r2)`, tie-break on sorted index list) and fuzzed 300 random small cases — all match the DP output exactly.
- Edge cases confirmed:
  - Single interval → `[0]`.
  - All-overlapping equal weights → `[0]` (lexicographically smallest single index).
  - Cross-cardinality weight tie (`(3,)` vs `(0,4)` both weight 5) → `[0,4]`, confirming tuple comparison across different lengths matches the spec.
  - Chain of exactly 4 disjoint intervals → all four taken.
  - Chain of 5 disjoint → top-4 by weight `[1,2,3,4]`.
  - Boundary touch `[1,3]`/`[3,5]` treated as overlapping (cannot combine); strict `r < l` via `bisect_left(rights, l)` is correct, and `[1,3]`/`[4,5]` does combine.
- The test harness is guarded by `if __name__ == "__main__":`, so the `Solution` class remains importable on its own; the submitted code is unchanged from the reviewed implementation.
