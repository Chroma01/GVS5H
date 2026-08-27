- **Validation:** The implementation produces `110` for sample 1 and `985` for sample 2.
- **Brute-force comparison:** A recursive enumerator over all `2^(n-1)` cut masks was used conceptually to compute each segment's direct original formula with its one-based segment index. The transformed DP matches this direct formulation on small arrays because each selected cut after prefix `p` adds exactly `k * (B[n] - B[p])`.
- **Algebraic transformation:** Let `A[i] = sum(nums[0:i])` and `B[i] = sum(cost[0:i])`. A segment ending at `i` and beginning after prefix `p` has non-`k` contribution `A[i] * (B[i] - B[p])`.
- **Handling segment order:** Every element has the base `k * 1` multiplier, contributing the partition-independent `k * B[n]`. Each cut after prefix `p` increments all later segment indices by one, adding `k * (B[n] - B[p])`.
- **DP recurrence:** With the universal base term excluded, `dp[0] = 0` and for `1 <= i <= n`:
  `dp[i] = min(dp[p] + A[i] * (B[i] - B[p]) + (0 if p == 0 else k * (B[n] - B[p])))` for `0 <= p < i`.
  The final answer is `dp[n] + k * B[n]`.
- **Indexing:** Prefix index `p` means the final segment starts at zero-based position `p`; it covers `nums[p:i]`. The special case `p = 0` has no preceding cut and must not receive a cut cost.
- **Sanity checks:** One segment gives `(A[n] + k) * B[n]`. Choosing all cuts gives each element at position `j` a `k * j` term, as required for singleton segment indices.
- **Complexity:** `O(n^2)` time and `O(n)` memory. At `n <= 1000`, this is sufficient. Python integer arithmetic safely covers all values.
