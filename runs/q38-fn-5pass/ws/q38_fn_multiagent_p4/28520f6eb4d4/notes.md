- **Visibility reduction:** For target building `i`, choosing its top maximizes the line height at every earlier coordinate, so building `i` is visible exactly when the segment from `(0, h)` to `(X_i, H_i)` is strictly above every earlier building top.
- **Pair threshold:** For `j < i`, strict visibility against `j` is
  `h > (H_j * X_i - H_i * X_j) / (X_i - X_j)`.
  Let `M` be the maximum over all pairs. If `M < 0`, then `h = 0` sees all buildings. Otherwise the maximum failing height is exactly `M`, because `h = M` still touches a blocking top and any `h > M` clears all buildings.
- **Adjacent-pair reduction:** With `u = 1 / X` and `v = H / X`, the threshold is the slope between transformed points. Since `X` increases, `u` decreases. For `a < b < c`, `slope(a, c)` is a positive weighted average of `slope(a, b)` and `slope(b, c)`, so it cannot exceed the larger adjacent slope. Therefore the global maximum is attained by some consecutive pair in input order.
- **Exact rational selection:** Scan consecutive pairs, compute numerator `H_prev * X_cur - H_cur * X_prev` and denominator `X_cur - X_prev`. Compare fractions by cross multiplication using Python integers, keeping the largest rational exactly.
- **Output formatting:** If there is no pair or the best numerator is negative, print exactly `-1`. Otherwise print `best_num / best_den` as a float with 18 digits after the decimal point. Double precision is sufficient for the required `1e-9` absolute or relative tolerance. Zero thresholds print `0.000000000000000000`, not `-1`.
- **Edge cases:** `N = 1` has no blocking pair and prints `-1`. A maximum threshold of zero means height `0` fails due to strict inequality, so the answer is `0`.
- **Complexity:** `O(N)` time and `O(1)` extra memory.
