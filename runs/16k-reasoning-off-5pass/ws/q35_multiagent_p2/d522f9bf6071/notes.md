
## ideation
The core difficulty lies in efficiently computing the maximum weight for up to 4 non-overlapping intervals and then reconstructing the lexicographically smallest set of indices. 

Key challenges:
1. **Large coordinate space**: Coordinates can be up to 10^9, so we cannot use a simple array-based DP over coordinates. However, since we only care about relative ordering, we can compress coordinates or use binary search on sorted end points.
2. **Lexicographical requirement**: After finding the maximum score, we need to pick the smallest index intervals that still allow achieving that score. This requires careful reconstruction.
3. **Efficient queries**: For each interval, we need to quickly find the best previous interval that ends before the current one starts (for DP) and the best future intervals (for reconstruction).

Approach:
1. Sort intervals by end time (and by index for tie-breaking to help with lexicographical order later if needed, but actually for DP we just need end time).
2. Use DP where `dp[k][i]` = max weight using k intervals from the first i intervals (sorted by end time).
3. To compute `dp[k][i]`, we need the max value of `dp[k-1][j]` for all j such that interval j ends before interval i starts. We can use binary search to find the rightmost j with end < start_i, and then use a prefix max array for each k to get the max in O(1).
4. After computing DP table, the answer is `dp[4][n-1]` (or max over k=1..4).
5. For reconstruction: iterate through original indices in increasing order. For each interval, check if including it (given the last chosen interval's end) can lead to the optimal remaining score. Use the DP table to check: if we choose interval i, then the remaining score should be `dp[remaining_slots][best_future_index]` which we can precompute as a suffix max array.

Pitfalls:
- Not handling the non-overlapping condition correctly (intervals sharing boundary are overlapping).
- Incorrectly computing the DP transitions due to not using prefix/suffix max arrays efficiently.
- Reconstruction logic must ensure that the chosen intervals are non-overlapping and that the total score matches the optimal.

## worker: Sort intervals by end point and create a mapping t
1. **Sorting and DP Setup**: The intervals are sorted by end time to facilitate DP. The DP state `best[k][i]` stores the maximum weight achievable using at most `k` intervals from the first `i` intervals (sorted by end time).
2. **Prefix Maximum for Transitions**: For each `k`, we compute `best[k][i]` by considering whether to include the current interval or not. The transition uses binary search to find the rightmost interval that ends before the current interval starts, and then uses the precomputed `best[k-1]` for that position.
3. **Reconstruction with Suffix Maximum**: To handle the lexicographical requirement, we precompute a suffix maximum array `suf_start` on intervals sorted by start time. This allows us to efficiently check, for any interval, the maximum weight achievable from intervals that start after the current interval's end.
4. **Greedy Selection for Lexicographical Order**: During reconstruction, we iterate through original indices in increasing order. For each interval, if it is non-overlapping with the last chosen interval and including it allows achieving the remaining required weight (using the precomputed `suf_start`), we select it.
