- **Run compression:** Replacing each maximal block of equal values by one run gives `M` runs. With no useful swaps, each run requires one deletion, so the baseline is `M`.

- **Effect of a swap:** An adjacent swap can reduce the number of runs by at most two. A reduction by two occurs exactly for four consecutive runs with values `x, y, x, y`, when both inner runs have length one. Swapping their boundary elements changes them into two merged runs and improves the total answer by one.

- **Unequal lengths:** If either inner run has length greater than one, one swap cannot merge both equal-value pairs. Such a swap has no positive net benefit and is excluded.

- **Overlapping improvements:** After applying a useful swap, the resulting outer run can be used by the next useful swap. Therefore, patterns ending three runs apart are compatible. The dynamic program uses `dp[i-3]`, not `dp[i-4]`.

- **Dynamic programming:** `dp[i]` is the maximum number of useful swaps obtainable from the first `i` runs. The transitions are `dp[i] = dp[i-1]` and, for a valid `x,y,x,y` pattern ending at `i`, `dp[i] = max(dp[i], dp[i-3] + 1)`.

- **Correctness validation:** An exhaustive shortest-path solver for small sequences can represent each state by its current tuple, with edges for every adjacent swap and every valid prefix deletion. Comparing exact BFS distances against the run-compression DP confirms the recurrence on small inputs, including unequal run lengths and overlapping alternating patterns.

- **Complexity:** Run compression and dynamic programming are both linear in `N` per test case. Total complexity is `O(sum N)` and memory usage is `O(N)`.
