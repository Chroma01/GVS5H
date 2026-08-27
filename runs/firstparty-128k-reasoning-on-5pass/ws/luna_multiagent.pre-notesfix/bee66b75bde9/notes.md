
## ideation
The core difficulty is recognizing that the two prefix conditions are not independent. The black cells must form a downward-closed set in the grid: if a cell is black, then every cell above it in the same column and every cell to its left in the same row must also be black. Equivalently, the row thresholds must be nonincreasing from top to bottom.

A useful correction to the proposed representation is that a cell is black exactly when its row threshold condition and column threshold condition agree, not merely when both conjunction conditions hold independently. It is enough to model the black set as a Ferrers/Young diagram, or to use only the row thresholds while enforcing their monotonicity.

Because only the prescribed cells matter and \(M\) is sparse, the solution should avoid iterating over all \(N\) rows, columns, or cells. The main implementation concerns are handling coordinates up to \(10^9\), aggregating multiple constraints in one row, and preserving strictness for white constraints: a white cell at column \(y\) requires the row threshold to be at most \(y-1\).

## worker: Implement and verify the order-ideal dominance alg
The black cells must form an order ideal: if `(x, y)` is black, then every cell `(x' <= x, y' <= y)` must also be black.

Thus, a prescribed white cell `(xw, yw)` conflicts with a prescribed black cell `(xb, yb)` exactly when:

- `xb >= xw`, and
- `yb >= yw`.

If no such pair exists, color every cell in the downward closure of the prescribed black cells black and all remaining cells white. This satisfies both row-prefix and column-prefix conditions.

The algorithm sorts black and white cells by decreasing row. While processing each white cell, it maintains the maximum column among black cells in rows at least as large as that white cell's row. A conflict is found if this maximum column is at least the white cell's column.

Complexity: `O(M log M)` time and `O(M)` memory.
