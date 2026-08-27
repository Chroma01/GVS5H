1. Sort intervals by their right endpoint to facilitate dynamic programming.
2. Use dynamic programming where `dp[k][i]` represents the maximum weight achievable using at most `k` non-overlapping intervals from the first `i` intervals (sorted by right endpoint).
3. For each interval `i`, find the latest interval `j` that does not overlap with `i` (i.e., `r_j < l_i`) using binary search.
4. Update `dp[k][i]` as `max(dp[k][i-1], dp[k-1][j] + weight_i)` for each `k` from 1 to 4.
5. After filling the DP table, backtrack from `dp[4][n-1]` to determine which indices were chosen, ensuring lexicographically smallest result by preferring smaller indices when weights are equal.