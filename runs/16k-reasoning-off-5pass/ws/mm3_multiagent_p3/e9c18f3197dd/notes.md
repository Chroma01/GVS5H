
## ideation
**Core difficulty:**
We must cover every `t` in `target` (size ≤ 4) with at least one element of `nums` (size ≤ 5e4) that is a multiple of `t`. We can only increment `nums`. The cost of turning a specific `num` into a value that is simultaneously a multiple of a set `S ⊆ target` is `max(0, lcm(S) * ceil(num / lcm(S)) - num)` if S is non-empty, or 0 if we leave it alone. We want the minimum total cost.

**Key insight (tiny target size):**
Because `|target| ≤ 4`, there are at most `2^4 = 16` non-empty subsets of `target`. We can use a DP over subsets (bitmask DP) to decide, for each `num`, which subset of uncovered targets it should "cover". The classic `target length <= 4` hint strongly suggests this.

**DP formulation:**
- Let `m = len(target)`. There are `2^m` subsets (including empty).
- `dp[mask]` = minimum total cost to make `nums` cover exactly the set of targets represented by `mask` (mask bits set = targets already covered). We want `dp[full_mask]`.
- Initialize `dp[0] = 0`, others = +inf.
- For each `num` in `nums`:
  - For each `mask` (in decreasing order to avoid reuse within the same `num`, or use a temporary array):
    - For each non-empty submask `sub` of `~mask & full_mask` (i.e., targets not yet covered):
      - `cost = max(0, lcm(sub) * ceil(num / lcm(sub)) - num)`.
      - Update `dp[mask | sub] = min(dp[mask | sub], dp[mask] + cost)`.
- Also consider not using this `num` at all: `dp[mask]` stays the same (we process masks in-place in decreasing order so the "not used" case is preserved).

**Precomputation:**
- For each of the `2^m - 1` non-empty subsets, precompute:
  - `lcm_val[subset]`: lcm of the target values in that subset.
  - `cost[num][subset]`: increments needed to raise `num` to the next multiple of `lcm_val[subset]`.
- `ceil_div(a, b) = (a + b - 1) // b`.

**Why this is optimal:**
- Every `num` either does nothing, or is assigned to cover some set of yet-uncovered targets. The best way to cover that set with a given `num` is exactly `lcm(sub)` (the smallest value ≥ `num` that is a multiple of all of them). Any higher value is wasted, any lower value fails the multiple condition.
- Since `m` is tiny, iterating all submasks per `num` is fine: `O(n * 3^m)` worst case, but with `m ≤ 4` that's `n * 81 ≤ 4e6`.

**Pitfalls:**
- LCM overflow: target[i] ≤ 1e4, max LCM of 4 values ≤ ~8400 (lcm(1..4)=12, lcm of 1..10=2520; lcm of primes up to 1e4 can exceed int32 but Python handles big ints; just clamp or accept).
- A `num` might already be a multiple of some targets; cost 0 for the subset containing just those targets.
- Don't use a target as a multiple of another target trick unless necessary; the subset DP handles it naturally (e.g., covering both 5 and 10 with 10).
- Since each `num` is used at most once, we must process DP updates so that one element cannot cover two disjoint subsets simultaneously. The standard trick: iterate masks from high to low, and for each submask, update `dp[mask | sub]` from `dp[mask]`. This is a 0/1 knapsack-style transition over subsets.
- Edge case: `target` length up to 4 but `nums` can be smaller? Constraint says `target.length <= nums.length`, so coverage is feasible if we allow using any `num` (we can always increment a `num` to the LCM of a subset containing all targets — but feasibility is guaranteed by constraints).

**Complexities:**
- Time: `O(n * 2^m * 2^m)` if naively iterating submasks of `~mask` each time. With `m ≤ 4`, we can precompute `cost[num][sub]` for all `2^m - 1` subsets and then for each `num` do a single DP pass over masks, trying all submasks. Better: for each `num`, iterate over all `2^m` masks, and for each, try all submasks. This is `O(n * 3^m)` which is fine. Simpler: for each `num`, for each subset `sub` (non-empty), compute `new_mask = mask | sub` and update. This is `O(n * 2^m * 2^m) = O(n * 4^m)`, also fine for `m ≤ 4` (~ `5e4 * 256 = 1.28e7`).
- Space: `O(2^m)`.

**Verification with examples:**
- Example 1: nums=[1,2,3], target=[4]. Subsets: {4}. lcm=4. Costs: 1->3, 2->2, 3->1. Min covering mask {4} = 1. ✓
- Example 2: nums=[8,4], target=[10,5]. Subsets: {5}, {10}, {5,10}. lcm({5,10})=10. Costs: for 8 to cover {5,10}=2, for 4 to cover {5}=1, {10}=6, {5,10}=6. Best: 8 covers {5,10} for 2. ✓
- Example 3: nums=[7,9,10], target=[7]. 10 is already multiple of... wait 10 mod 7 = 3, 9 mod 7=2, 7 mod 7=0. So 7 is already a multiple of itself. Cost 0. ✓

## worker: Implement the subset DP solution in Python: precom
Implemented subset DP with precomputed LCMs for all non-empty target subsets (m ≤ 4, so at most 15 subsets). For each `num`, iterate over all DP states and all non-empty submasks of currently uncovered targets, computing the cost to raise `num` to the next multiple of the LCM of that submask. Uses a temporary `new_dp` to prevent reusing the same `num` element for two disjoint subsets (0/1 knapsack). Submask enumeration via `sub = (sub - 1) & uncovered` ensures we try exactly the non-empty subsets of uncovered targets. The empty submask (not using this num) is handled by initializing `new_dp = dp[:]`. Time complexity: O(n * 3^m) ≤ 5e4 * 81 ≈ 4e6, which is well within limits.
