
## ideation
The core difficulty lies in efficiently computing the sum of Manhattan distances between all pairs of cells in an m x n grid, and then multiplying this by the number of arrangements that include any specific pair of cells.

1.  **Linearity of Summation**: Instead of iterating over all arrangements (which is impossible due to large constraints), we can swap the order of summation. We sum over all unordered pairs of distinct cells `(u, v)` the product of:
    *   The Manhattan distance between `u` and `v`.
    *   The number of valid arrangements where both `u` and `v` contain pieces.
    
2.  **Counting Arrangements**: For any two distinct cells `u` and `v`, if we fix pieces at these locations, we need to place the remaining `k-2` pieces in the remaining `m*n - 2` cells. The number of ways to do this is `C(m*n - 2, k - 2)`. This factor is constant for all pairs `(u, v)`.

3.  **Summing Distances**: The total answer is `C(m*n - 2, k - 2) * S`, where `S` is the sum of Manhattan distances between all unordered pairs of distinct cells in the grid.
    *   Manhattan distance `d((x1,y1), (x2,y2)) = |x1-x2| + |y1-y2|`.
    *   `S = S_x + S_y`, where `S_x` is the sum of `|x1-x2|` over all pairs, and `S_y` is the sum of `|y1-y2|` over all pairs.
    *   **Calculating S_x**: The x-coordinate depends only on the row. For a fixed column, the rows are `0` to `m-1`. The sum of absolute differences for all pairs of rows is `sum_{i=0}^{m-1} sum_{j=i+1}^{m-1} (j - i)`. This sum is the same for each of the `n` columns. So, `S_x = n * (sum of |i-j| for all pairs of rows)`.
    *   **Calculating S_y**: Similarly, `S_y = m * (sum of |j-l| for all pairs of columns)`.
    *   **Formula for sum of absolute differences**: For a sequence `0, 1, ..., L-1`, the sum of `|i-j|` for all `0 <= i < j <= L-1` is `L*(L-1)*(L+1)/6`? Let's derive it.
        Sum = `sum_{i=0}^{L-1} sum_{j=i+1}^{L-1} (j-i)`.
        Let `d = j-i`. For a fixed `d` from `1` to `L-1`, how many pairs `(i,j)` have `j-i=d`? `i` can range from `0` to `L-1-d`, so there are `L-d` such pairs.
        Sum = `sum_{d=1}^{L-1} d * (L-d) = L * sum_{d=1}^{L-1} d - sum_{d=1}^{L-1} d^2`.
        `sum_{d=1}^{L-1} d = (L-1)L/2`.
        `sum_{d=1}^{L-1} d^2 = (L-1)L(2L-1)/6`.
        So, Sum = `L * (L-1)L/2 - (L-1)L(2L-1)/6 = (L-1)L [ L/2 - (2L-1)/6 ] = (L-1)L [ (3L - 2L + 1)/6 ] = (L-1)L(L+1)/6`.
        So for dimension with size `L`, the sum of absolute differences for all pairs is `L*(L-1)*(L+1)/6`.
    *   Therefore:
        `S_x = n * [ m*(m-1)*(m+1)/6 ]`
        `S_y = m * [ n*(n-1)*(n+1)/6 ]`
        `S = S_x + S_y`

4.  **Modular Arithmetic**: Since the result can be large, all calculations must be done modulo `10^9 + 7`. We need to compute combinations `C(N, K) mod P`. This requires precomputing factorials and their modular inverses. Note that `N = m*n - 2` and `K = k - 2`. Given constraints `m*n <= 10^5`, we can precompute factorials up to `10^5`.

5.  **Pitfalls**:
    *   Division by 6 requires modular inverse.
    *   Ensure all intermediate products are taken modulo `10^9 + 7`.
    *   Handle edge cases where `k < 2`? Constraints say `k >= 2`, so `C(m*n-2, k-2)` is valid as long as `m*n >= 2`, which is given.

## worker: (none)
The solution uses linearity of expectation/summation. Instead of iterating over all arrangements, we consider each unordered pair of cells `(u, v)`. The contribution of this pair to the total sum is `Manhattan(u, v) * C(m*n - 2, k - 2)`, because there are `C(m*n - 2, k - 2)` arrangements that include both `u` and `v`.

The sum of Manhattan distances over all unordered pairs of cells is split into x and y components:
- `S_x = n * sum_{0<=i<j<m} |i-j|`
- `S_y = m * sum_{0<=l<p<n} |l-p|`

The sum of absolute differences for indices `0` to `L-1` is `L*(L-1)*(L+1)/6`. This is derived from `sum_{d=1}^{L-1} d*(L-d)`.

All calculations are performed modulo `10^9 + 7`. Factorials and their modular inverses are precomputed to efficiently calculate combinations. The modular inverse of 6 is computed using Fermat's Little Theorem.
