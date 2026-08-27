
## ideation
The core difficulty lies in efficiently updating the sum of path products after a single cell value change. A naive recomputation of the DP table is $O(HW)$ per query, which is too slow given $Q, HW \le 200,000$.

The key insight is to decompose the total sum of path products into contributions from each cell.
Let $DP_{down}[h][w]$ be the sum of products of all paths from $(1,1)$ to $(h,w)$.
Let $DP_{up}[h][w]$ be the sum of products of all paths from $(h,w)$ to $(H,W)$.
The total answer is $DP_{down}[H][W]$.

We can express the total sum as:
$$ \text{Total} = \sum_{h=1}^H \sum_{w=1}^W \left( \text{Sum of products from } (1,1) \text{ to neighbors of } (h,w) \right) \times A_{h,w} \times \left( \text{Sum of products from neighbors of } (h,w) \text{ to } (H,W) \right) $$

Specifically, let:
- $Pre[h][w] = DP_{down}[h-1][w] + DP_{down}[h][w-1]$ (with $DP_{down}[0][w]=0, DP_{down}[h][0]=0$). This represents the sum of path products reaching the immediate predecessors of $(h,w)$.
- $Suf[h][w] = DP_{up}[h+1][w] + DP_{up}[h][w+1]$ (with $DP_{up}[H+1][w]=0, DP_{up}[h][W+1]=0$). This represents the sum of path products starting from the immediate successors of $(h,w)$.

Then, the contribution of cell $(h,w)$ to the total sum is $Pre[h][w] \times A_{h,w} \times Suf[h][w]$.
Crucially, $Pre[h][w]$ depends only on $A$ values in the rectangle $[1,h] \times [1,w]$ excluding $(h,w)$ itself (specifically from above and left). $Suf[h][w]$ depends only on $A$ values in the rectangle $[h,H] \times [w,W]$ excluding $(h,w)$ itself (specifically from below and right).

When $A_{r,c}$ is updated to $A'_{r,c}$:
1. $Pre[r][c]$ remains unchanged because it depends on $DP_{down}$ values from cells $(r-1,c)$ and $(r,c-1)$, which are not affected by $A_{r,c}$.
2. $Suf[r][c]$ remains unchanged because it depends on $DP_{up}$ values from cells $(r+1,c)$ and $(r,c+1)$, which are not affected by $A_{r,c}$.
3. The total sum changes by $(A'_{r,c} - A_{r,c}) \times Pre[r][c] \times Suf[r][c]$.

Thus, we can precompute $Pre$ and $Suf$ tables in $O(HW)$ and answer each query in $O(1)$.

Pitfalls:
- Modular arithmetic: Ensure all additions and multiplications are modulo 998244353. Handle negative differences correctly by adding the modulus before taking modulo.
- Boundary conditions: Carefully handle indices for $Pre$ and $Suf$ at the edges of the grid.
- Input size: $HW$ can be up to 200,000, so use efficient I/O and avoid recursion depth issues (use iterative DP).

## worker: (None)
The solution relies on decomposing the total sum of path products into independent contributions from each cell.
1.  **DP Definitions**:
    *   $Down[h][w]$: Sum of products of all paths from $(1,1)$ to $(h,w)$.
    *   $Up[h][w]$: Sum of products of all paths from $(h,w)$ to $(H,W)$.
2.  **Contribution Formula**: The total sum of path products is equal to $\sum_{h,w} Pre[h][w] \times A_{h,w} \times Suf[h][w]$, where:
    *   $Pre[h][w] = Down[h-1][w] + Down[h][w-1]$ (sum of path products reaching the immediate predecessors of $(h,w)$).
    *   $Suf[h][w] = Up[h+1][w] + Up[h][w+1]$ (sum of path products starting from the immediate successors of $(h,w)$).
3.  **Invariance**: When $A_{r,c}$ is updated, $Pre[r][c]$ and $Suf[r][c]$ do not change. This is because $Pre[r][c]$ depends only on $Down$ values from cells strictly above or to the left of $(r,c)$, and $Suf[r][c]$ depends only on $Up$ values from cells strictly below or to the right of $(r,c)$. The value $A_{r,c}$ itself does not influence these "incoming" and "outgoing" sums for its own cell.
4.  **Update Efficiency**: The change in the total sum is simply $(A'_{r,c} - A_{r,c}) \times Pre[r][c] \times Suf[r][c]$. This allows for $O(1)$ updates per query after an $O(HW)$ precomputation.
5.  **Complexity**: Precomputation takes $O(HW)$ time and space. Each query takes $O(1)$ time. Total time complexity is $O(HW + Q)$, which fits within the constraints ($HW, Q \le 200,000$).
