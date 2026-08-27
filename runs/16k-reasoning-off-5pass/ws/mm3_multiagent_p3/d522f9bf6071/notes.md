
## ideation
- Core difficulty: selecting up to 4 non-overlapping intervals with maximum total weight, with tie-breaking by lexicographically smallest index list. The constraints (N up to 5e4) require an efficient O(N log N) or O(N) solution after sorting.
- Candidate approaches: 
  1. DP after sorting intervals by right endpoint, with state (i, k) representing the best (weight, sorted index tuple) for picking exactly k intervals among the first i+1 intervals. This is exactly the given plan.
  2. DP with segment tree: for each k, maintain a data structure over right endpoints to query the best previous state, but storing the lexicographically smallest index list complicates the update logic. Still possible but more complex.
  3. Greedy with lookahead: not suitable because weights are arbitrary.
  4. State compression: since K=4, we can keep full DP table; no need for further compression.
- The given plan is correct and efficient. Key steps:
  - Sort intervals by right endpoint, keep original indices.
  - Precompute p[i] using binary search on the sorted right endpoints to find the last interval with r < l_i.
  - DP over i and k, storing (weight, tuple of sorted indices). Compare states by weight first, then lexicographically on the index tuple.
  - Initialize invalid states with weight -1.
  - For each interval i, consider not taking (inherit from i-1) and taking (combine with best from p[i]).
  - At the end, pick the best state across k=0..4.
- Pitfalls:
  - Strict non-overlap: must use r_j < l_i, not ≤.
  - Lexicographic order: the index list must be sorted to represent the set canonically; otherwise, comparisons may be inconsistent.
  - Handling invalid states: ensure that transitions from invalid states are not taken.
  - Base cases: dp[i][0] = (0, ()) always; for k≥1, start with invalid.
  - When taking interval i, if k=1, the previous state is empty; if k>1, need a valid previous state from p[i].
  - Binary search limit: use bisect_left with hi=i to ensure we only look at intervals before i.
  - Memory: storing dp for all i is acceptable (5e4 * 5 states).
  - The final answer must be a list of indices in increasing order (as per examples).

## worker: Implement the DP solution in Python: sort interval
The solution implements the DP plan:
1. Sort intervals by right endpoint, keeping original indices.
2. Precompute predecessor array `p[i]` using binary search on right endpoints to find the last non-overlapping interval (strict `r < l_i`).
3. Run DP where `dp[i][k]` stores `(weight, sorted_indices_tuple)` for the best selection of exactly `k` non-overlapping intervals among the first `i+1` intervals (in sorted order).
4. For each interval, consider skipping (inherit from `dp[i-1]`) or taking (combine with best from `dp[p[i]]`).
5. State comparison: first by weight (higher is better), then by lexicographic order of the index tuple.
6. Final answer is the best state across `k = 0..4` from `dp[n-1]`.

Key details:
- The index tuple is always kept sorted to enable consistent lexicographic comparison.
- When combining states, we sort the new tuple of indices.
- Time complexity: O(N log N) for sorting and binary searches + O(N·K) for DP with K=4, which is efficient for N up to 5e4.
