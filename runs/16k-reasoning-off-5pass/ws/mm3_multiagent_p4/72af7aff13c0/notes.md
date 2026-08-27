
## ideation
- The problem asks to compute the sum over all monotone paths (only right/down) from (1,1) to (H,W) of the product of cell values, after each point update.
- Since updates are just changing a single cell's value, we can maintain a linear combination of the cell values.
- For a path, the coefficient of `A[i][j]` is the number of paths that go through `(i,j)`. For monotone paths on an `H×W` grid, this number is `C(i+j-2, i-1) * C(H+W-i-j, H-i)`. This follows from splitting the path at `(i,j)`.
- So the total sum is `S = Σ C(i+j-2, i-1) * C(H+W-i-j, H-i) * A[i][j] (mod p)`.
- Precompute factorials and inverse factorials up to `N = H+W` (actually need up to `H+W` for binomials). Since `HW ≤ 200000`, `H+W` can be up to ~400000, but it's safe to precompute up to `2*10^5` or slightly more.
- Compute weight `W[i][j] = C(i+j-2, i-1) * C(H-i + W-j, H-i) % p` for all cells.
- Initial sum `cur = Σ W[i][j] * A[i][j] % p`.
- For each operation, we know current position `(sh, sw)`. Move in direction `d_i` to `(h, w)`, update `A[h][w] = a_i`. The change in `cur` is `W[h][w] * (a_i - A_old)`. Update `cur`, then set `(sh, sw) = (h, w)`.
- Note: `a_i` and `A_old` are taken modulo p; subtraction may be negative, add p.
- Complexity: O(H+W + HW + Q) time, O(HW) memory.

## worker: Implement the solution in Python: read input, prec
- The solution uses the combinatorial identity: the number of monotone paths through cell (i,j) is `C(i+j-2, i-1) * C(H-i+W-j, H-i)`.
- Precomputes factorials and inverse factorials up to `H+W` to evaluate binomial coefficients in O(1).
- Maintains a running sum `cur` of `weight[i][j] * A[i][j]`. Each update changes only one cell, so we adjust `cur` by `weight * (new - old)`.
- Complexity: O(H+W + HW + Q) time, O(HW) memory, which fits constraints (`HW ≤ 2e5`, `Q ≤ 2e5`).
