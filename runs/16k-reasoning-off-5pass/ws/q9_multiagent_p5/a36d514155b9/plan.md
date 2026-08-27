The problem asks for the sum of Manhattan distances between all pairs of pieces across all valid arrangements. Since the pieces are identical and the grid is symmetric, we can separate the Manhattan distance into row differences and column differences. The total sum is the sum of (row distance sum) + (column distance sum). For the row component, we treat the problem as placing k items in m rows with capacities n, calculating the expected or total distance between row indices. Similarly for columns. We can solve this by iterating over each possible row (or column) index `i`, calculating how many ways we can place the k pieces such that one piece is at row `i` and another is at a different row `j`, weighted by `|i - j|`. Alternatively, we can use a combinatorial approach: fix one piece at a specific cell, calculate the number of ways to place the remaining k-1 pieces, and sum the distances from that fixed cell to all other possible cells, then divide by k (since each pair is counted twice) and multiply by the number of ways to choose the fixed cell's position relative to the rest. However, a more direct linear scan approach is efficient: for each row `i`, calculate the contribution of pairs where one piece is in row `i` and the other is in row `j`. The number of ways to choose positions in row `i` is `C(n, 1) = n` (if we pick one specific cell) but actually we need to choose `c_i` pieces in row `i`. This gets complex.
Let's refine: Total Sum = Sum over all pairs of cells (u, v) of (Manhattan(u, v) * Number of arrangements where u and v both have pieces).
Number of arrangements where specific cells u and v have pieces: We need to place k-2 remaining pieces in the remaining `m*n - 2` cells. This is `C(m*n - 2, k - 2)`.
So, Total Sum = `C(m*n - 2, k - 2)` * Sum over all pairs (u, v) of `|x_u - x_v| + |y_u - y_v|`.
The sum over all pairs of `|x_u - x_v|` can be calculated by iterating over rows. For a fixed row `i` and row `j`, there are `n` columns, so `n^2` pairs of cells between row `i` and `j`. The distance is `|i - j|`.
Sum of `|i - j|` for all `1 <= i, j <= m` is `2 * sum_{i=1}^{m} sum_{j=i+1}^{m} (j - i)`.
Let `S_row = sum_{i=1}^{m} sum_{j=i+1}^{m} (j - i)`. Then total row contribution is `n^2 * S_row`.
Similarly, `S_col = sum_{i=1}^{n} sum_{j=i+1}^{n} (j - i)`. Total col contribution is `m^2 * S_col`.
Finally, multiply by `C(m*n - 2, k - 2)`.
Wait, the example 1: m=2, n=2, k=2.
Total cells = 4. Pairs of cells = 6.
Arrangements: C(4, 2) = 6.
Formula check: `C(4-2, 2-2) = C(2, 0) = 1`.
Sum of distances over all pairs of cells:
Rows: 1, 2. `S_row = |1-2| = 1`. `n^2 * S_row = 4 * 1 = 4`.
Cols: 1, 2. `S_col = |1-2| = 1`. `m^2 * S_col = 4 * 1 = 4`.
Total sum = 4 + 4 = 8.
Result = 8 * 1 = 8. Matches Example 1.
Example 2: m=1, n=4, k=3.
Cells = 4. Arrangements = C(4, 3) = 4.
Formula: `C(4-2, 3-2) = C(2, 1) = 2`.
Rows: m=1. `S_row = 0`. Contribution = 0.
Cols: n=4. `S_col = |1-2| + |1-3| + |1-4| + |2-3| + |2-4| + |3-4| = 1+2+3+1+2+1 = 10`.
`m^2 * S_col = 1 * 10 = 10`.
Total sum = 10.
Result = 10 * 2 = 20. Matches Example 2.

So the algorithm is:
1. Calculate `total_cells = m * n`.
2. Calculate `combinations = C(total_cells - 2, k - 2) % MOD`.
3. Calculate `sum_row_diffs` for 1..m: `2 * sum_{i=1}^{m-1} i * (m - i)`.
   Actually, `sum_{i=1}^{m} sum_{j=i+1}^{m} (j-i)`.
   Let `d = j-i`. For a fixed `d` from 1 to `m-1`, there are `m-d` pairs.
   Sum = `sum_{d=1}^{m-1} d * (m-d)`.
   This can be computed in O(1) using formulas for sum of integers and sum of squares.
   `sum_{d=1}^{k} d = k(k+1)/2`.
   `sum_{d=1}^{k} d^2 = k(k+1)(2k+1)/6`.
   Here `k = m-1`.
   `Sum = m * sum(d) - sum(d^2)`.
4. Calculate `sum_col_diffs` similarly for 1..n.
5. `ans = ( (n*n * sum_row_diffs + m*m * sum_col_diffs) % MOD * combinations ) % MOD`.