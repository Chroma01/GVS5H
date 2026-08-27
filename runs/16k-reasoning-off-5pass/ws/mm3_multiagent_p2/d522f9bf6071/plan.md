We need to choose up to 4 non-overlapping intervals maximizing total weight, then return the lexicographically smallest index set among optimal solutions.

The classic DP for weighted interval scheduling (1 chosen) extends naturally: sort intervals by end, then for each interval `i` compute `dp[k][i]` = best (weight sum, index tuple) using up to `k` intervals ending at or before `i`. `k` ranges 0..4.

Transitions:
- Skip `i`: `dp[k][i] = dp[k][i-1]`
- Take `i`: find the last interval `j` with `r_j < l_i` using binary search; then `dp[k][i] = (weight_i + dp[k-1][j].weight, (i,) + dp[k-1][j].indices)` if `k>=1`.
Pick the lexicographically larger tuple on ties (since we store as tuple, Python compares element-wise — but we need max total weight, and among equal weight, lexicographically smallest index list). We'll store index lists in sorted order and compare accordingly.

Answer = best among `dp[k][n-1]` for k=0..4, preferring higher weight, then lexicographically smaller list, then shorter length.

Sorting first changes indices; keep original indices in tuples.