- **Shape characterization:** The black cells must form a northwest-closed set. If a cell is black, every cell above it and every cell to its left must also be black, because each column and row is a black prefix. Conversely, any northwest-closed set has the required prefix form in every row and column.

- **Conflict condition:** A prescribed white cell `(x_w, y_w)` forces every cell `(x, y)` with `x >= x_w` and `y >= y_w` to be white, since such a cell is southeast of it. Therefore, a prescribed black cell `(x_b, y_b)` is incompatible exactly when `x_b >= x_w` and `y_b >= y_w` for some prescribed white cell.

- **Sufficiency:** If no such conflicting pair exists, construct the black set as the union, over all prescribed black cells `(x_b, y_b)`, of the rectangles `[1, x_b] × [1, y_b]`. This set is northwest-closed and contains every prescribed black cell. A prescribed white cell would belong to this union only if it were northwest of some prescribed black cell, which is precisely the forbidden conflict. Thus all prescribed colors are respected.

- **Sweep:** Sort all prescribed cells by row. At each row, process white cells before black cells so whites in the same row are included. Maintain the minimum column among all whites seen so far. For a black cell at column `y`, a conflict exists iff this minimum is at most `y`.

- **Complexity:** Sorting takes `O(M log M)` time, and the sweep takes `O(M)` time. Memory usage is `O(M)`. The value of `N` only supplies the boundary for the initial minimum and does not affect the asymptotic complexity.
