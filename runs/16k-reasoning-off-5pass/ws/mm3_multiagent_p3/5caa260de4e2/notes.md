
## ideation
**Core difficulty:** The cost formula contains the subarray index `i` multiplicatively with a running sum, creating a 2D DP over (position, #subarrays). With n ≤ 1000, naive O(n²) per group-level is O(n³) — too slow — so we need the **divide-and-conquer DP optimization** (monotone opt / Monge-array property) to bring each group-level layer down to O(n log n), total O(n² log n) ≈ 10⁷ ops, fine for n=1000.

**Recurrence (key derivation):**
- Let `P[i] = sum(nums[0..i-1])`, `C[i] = sum(cost[0..i-1])`.
- A subarray `[l..r]` that is the `g`-th subarray costs `(P[r+1]-P[l] + k·g)·(C[r+1]-C[l])`.
- Define `dp[g][i]` = min cost to partition first `i` elements into `g` subarrays:
  `dp[g][i] = min_{j<i} dp[g-1][j] + (P[i]-P[j] + k·g)·(C[i]-C[j])`.
- Answer = `min_g dp[g][n]`.

**Monotonicity:** Expanding the transition gives a form that satisfies the quadrangle inequality (Monge), so the optimal `j` for `dp[g][i]` is non-decreasing in `i`. This justifies D&C optimization.

**Pitfalls:**
- Off-by-one on the `+k·g` term (subarray index is 1-based).
- `dp_prev[0] = 0` (zero elements, zero cost) but `dp_cur[0] = inf` for `g ≥ 1`.
- Search range in D&C recursion must clamp `optR` to `mid-1`.
- Initialize `answer` to `inf`; the optimal g is anywhere in `[1, n]`.
- Use large `INF` (e.g., 10**30) to avoid overflow; values can reach ~10^9.
- Need `from typing import List` for the signature.

## worker: Compute prefix sums `P` for nums and `C` for cost 
- Computed the two prefix sums `P` (nums) and `C` (cost) of length `n+1`, so `P[i] = sum(nums[0..i-1])` and similarly for `C[i]`.
- Initialized the `g=0` layer: `dp_prev[0] = 0` (empty prefix with zero subarrays is free) and all other entries set to `INF` to mark unreachable states.
- The D&C helper `compute` now operates on this `dp_prev` and writes results into `dp_cur` for a fixed group count `g`. The recurrence used is
  `dp[g][i] = min_{j<i} dp[g-1][j] + (P[i]-P[j] + k*g) * (C[i]-C[j])`,
  which follows directly from the problem's cost formula with subarray index `g`.
- The `optL..optR` window passed into the recursive call constrains the search for the optimal split point `j`, exploiting the Monge/quadrangle property that the optimal `j` is monotone in `i`. Each layer costs `O(n log n)`, so the full run is `O(n^2 log n)` — well within the `n ≤ 1000` constraint.
- The global answer is the minimum of `dp_cur[n]` across all group counts `g = 1..n`, since the optimal partition could use any number of subarrays up to `n`.
- Edge cases handled: `dp_prev[0] = 0` ensures the first subarray is reachable from the empty prefix, and clamping `end = min(optR, mid-1)` keeps `j < i` valid.
