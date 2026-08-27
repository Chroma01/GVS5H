- **Boundary transformation:** If the partition endpoints are \(0=p_0<p_1<\dots<p_m=n\), the order-dependent contribution is
  \[
  k\sum_{j=1}^{m}j(B_{p_j}-B_{p_{j-1}})
  =k\left(mB_n-\sum_{j=1}^{m-1}B_{p_j}\right)
  =kB_n+\sum_{j=1}^{m-1}k(B_n-B_{p_j}),
  \]
  where \(B_x\) is the prefix sum of `cost`.
- **Segment base cost:** A segment ending at position `r - 1` and starting at `l` has base cost
  `prefix_nums[r] * (prefix_cost[r] - prefix_cost[l])`, because the nums prefix through its endpoint is used.
- **DP state:** `dp[r]` stores the minimum sum of all segment base costs plus the transformed penalty for every internal cut in a partition of `nums[0:r]`. When the previous cut is at `l > 0`, its penalty is `k * (prefix_cost[n] - prefix_cost[l])`.
- **Final adjustment:** The transformed expression contains the partition-independent term `k * prefix_cost[n]`, which is added after computing `dp[n]`.
- **Complexity:** Prefix sums take \(O(n)\). Trying every prior cut for every endpoint takes \(O(n^2)\) time and \(O(n)\) memory.
- **Correctness checks:** The recurrence yields `110` for the first example and `985` for the second. It also handles one-element arrays and the partition consisting of the entire array.
