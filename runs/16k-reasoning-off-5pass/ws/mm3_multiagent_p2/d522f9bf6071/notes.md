
## ideation
The problem is a variant of weighted interval scheduling with a limit of at most 4 intervals. We need to maximize total weight and, among optimal solutions, return the lexicographically smallest list of original indices (sorted ascending).

Key observations:
- `n` can be up to 5·10⁴, so an O(n²) DP is too slow. We need O(n log n) or O(n·k·log n) where k=4.
- Classic approach: sort intervals by end coordinate, then DP over sorted order. For each interval `i`, we need the best solution using up to `k` intervals that ends before `i` starts. This can be found with binary search on the sorted ends.
- Since k ≤ 4 is tiny, we can maintain `dp[k][i]` = best (weight, index_tuple) for the first `i+1` sorted intervals using exactly `k` intervals (or up to `k`?). It's easier to store "up to k" by allowing k=0..4 and taking max over k at the end.
- State representation: For each `k` and each `i`, store `(total_weight, index_tuple)`. The index_tuple must be sorted ascending to make lexicographic comparison straightforward. Python compares tuples element-wise, which matches the required lexicographic order.
- Transition:
  - Not take `i`: `dp[k][i] = dp[k][i-1]`.
  - Take `i` (if k ≥ 1): find `j` = rightmost interval with `r_j < l_i`. Then candidate = `(weight_i + dp[k-1][j].weight, tuple(sorted((i,) + dp[k-1][j].indices)))`.
  - Choose the better candidate: higher weight wins; if equal weight, smaller index_tuple wins (lexicographically).
- Base: `dp[0][i] = (0, ())` for all i.
- Final answer: best among `dp[k][n-1]` for k=0..4, preferring higher weight, then lexicographically smaller tuple, then shorter length (which is automatic if we compare tuples element-wise because shorter tuple is smaller when prefixes match).
- Pitfalls:
  - Intervals sharing a boundary are considered overlapping, so condition is `r_j < l_i` (strict).
  - Original indices must be preserved; sorting changes order, so store original index alongside.
  - Lexicographic comparison of tuples: Python compares element by element; if one tuple is a prefix of the other, the shorter one is smaller. This matches the problem's definition.
  - Need to handle empty selection (k=0) correctly.
  - Binary search on ends array: use `bisect_left(ends, l_i) - 1` to get last index with end < l_i.
  - Complexity: O(n·k·log n) = O(n log n) since k=4.

## worker: Implement the `maximumWeight` method in the `Solut
Implemented the weighted interval scheduling DP with k up to 4. Key points:
- Sorted intervals by end coordinate while preserving original indices.
- `dp[k][i]` stores the best `(weight, indices_tuple)` using at most `k` non-overlapping intervals from the first `i+1` sorted intervals.
- For each `i`, binary search finds predecessor `j` with `r_j < l_i` (strictly less, as sharing boundaries counts as overlapping).
- Transitions: skip (inherit from `i-1`) or take (combine with `dp[k-1][j]` and add current). Indices are merged in sorted order to maintain ascending order for lexicographic comparison.
- Tie-breaking: among equal weights, Python's tuple comparison gives the lexicographically smallest tuple, which matches the problem's requirement (shorter tuple is considered smaller when one is prefix of the other).
- Final answer scans all `k=0..4` and picks max weight, then min indices tuple.
