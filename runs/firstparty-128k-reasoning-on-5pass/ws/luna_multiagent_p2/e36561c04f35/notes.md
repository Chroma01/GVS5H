- **Run compression:** Consecutive equal elements can be deleted in one operation, so compress the sequence into maximal runs. If there are `R` runs, deleting each run separately costs `R`.

- **Useful swap condition:** A swap can improve the answer only when the sequence of runs has the form `x^p, y, x, y^q`, where the two middle runs are singletons. Swapping the middle `y` and `x` changes this to `x^(p+1), y^(q+1)`, reducing the number of runs by two while costing one swap. Thus the total answer decreases by one.

- **Why singleton middle runs are necessary:** If either middle run has length greater than one, swapping one boundary element does not merge the two corresponding runs. Moving all of such a run costs at least as much as simply deleting it, so it cannot yield a net improvement.

- **Pattern test:** For boundary `b` between runs `b-1` and `b` (zero-based), it is useful exactly when:
  - `length[b] == length[b+1] == 1`;
  - `runs[b-1] == runs[b+1]`;
  - `runs[b] == runs[b+2]`.

- **Compatibility:** Useful swaps whose boundaries differ by one or two interfere. Boundaries at distance at least three can be realized simultaneously. Therefore the useful swaps form a maximum independent-set problem on a path with spacing at least three.

- **Dynamic programming:** Let `dp[b]` be the maximum number of compatible useful swaps among boundaries up to `b`. For a useful boundary:
  `dp[b] = max(dp[b-1], dp[b-3] + 1)`,
  with the second term treated as `1` when `b < 3`. For a non-useful boundary, `dp[b] = dp[b-1]`.

- **Answer:** Each selected useful swap lowers the baseline run-deletion cost by one, so the result is `R - dp[R-1]`.

- **Complexity:** Run compression and dynamic programming are both linear. Total complexity is `O(sum N)` and memory usage is `O(N)` per test case.
