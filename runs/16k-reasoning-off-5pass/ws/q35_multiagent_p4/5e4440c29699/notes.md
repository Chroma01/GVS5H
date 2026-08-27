
## ideation
The problem asks for the number of valid paths in a grid with a rectangular hole. A valid path consists of a sequence of adjacent blocks (lattice points) moving only right or up. The blocks are defined as the rectangle $[0, W] \times [0, H]$ excluding the open rectangle $(L, R] \times (D, U]$.

The core difficulty is efficiently counting paths that avoid the hole. A direct dynamic programming approach over the grid is too slow ($O(WH)$). Instead, we use the principle of inclusion-exclusion (complementary counting):
1. Calculate the total number of paths in the full rectangle $[0, W] \times [0, H]$ without considering the hole.
2. Subtract the number of paths that pass through at least one point in the hole.

To count invalid paths (those touching the hole), we use the "first entry" method. Each invalid path has a unique first point $(x,y)$ in the hole. We sum over all $(x,y)$ in the hole:
- The number of valid paths from any valid start point to $(x,y)$ that do not touch the hole before $(x,y)$. Let this be $First(x,y)$.
- The number of paths from $(x,y)$ to any end point in the full grid (valid or not, since we are counting paths in the full grid that touch the hole). Let this be $End(x,y)$.

$First(x,y)$ can be derived from the number of paths in the full grid from any start to the neighbors of $(x,y)$ that are valid. Specifically, the path must enter the hole from the left ($x-1, y$) or from the bottom ($x, y-1$). Since the hole is a rectangle, the valid predecessors are on the boundaries $x=L+1$ (coming from $x=L$) and $y=D+1$ (coming from $y=D$).
We derived that $First(x,y) = S(L, y) + S(x, D)$, where $S(u,v)$ is the total number of paths in a full grid from any start to $(u,v)$.
$S(u,v) = \binom{u+v+2}{2} - 1$.

$End(x,y)$ is the number of paths from $(x,y)$ to any point in $[0, W] \times [0, H]$, which is $\binom{(W-x)+(H-y)+2}{2} - 1$.

The total invalid paths is $\sum_{x=L+1}^R \sum_{y=D+1}^U First(x,y) \times End(x,y)$.
This double sum can be expanded into terms involving sums of binomial coefficients, which can be computed in $O(1)$ or $O(W+H)$ using precomputed factorials and prefix sums of combinatorial identities.

The total full paths can also be computed using combinatorial identities in $O(W+H)$.

Pitfalls:
- Modulo arithmetic at every step.
- Correctly handling the indices for the hole boundaries.
- Efficient computation of the large sums for invalid paths.

## worker: Implement modular arithmetic and precompute factor
The solution uses complementary counting.
1. **Total Full Paths**: Calculated by summing over all possible displacements $(dx, dy)$ the number of paths weighted by the number of valid start positions. The inner sum over $dy$ is computed using combinatorial identities involving sums of binomial coefficients, allowing $O(W+H)$ computation.
2. **Invalid Paths**: Calculated by summing over all points $(x,y)$ in the hole the number of paths that first enter the hole at $(x,y)$.
   - $First(x,y)$ is the number of paths from valid starts to $(x,y)$ avoiding the hole. This is derived as $S(L,y) + S(x,D)$, where $S(u,v)$ is the total paths in a full grid to $(u,v)$.
   - $End(x,y)$ is the number of paths from $(x,y)$ to any end point in the full grid.
   - The double sum for invalid paths is decomposed into two single sums (Term 1 and Term 2) by swapping the order of summation. Each term involves sums of cubic binomial coefficients, which are computed using the identity $\sum_{k=0}^N C(k+r, r) = C(N+r+1, r+1)$.
3. **Complexity**: Precomputing factorials takes $O(W+H)$. Computing total full paths takes $O(W)$. Computing invalid paths takes $O(U-D + R-L)$. Overall complexity is $O(W+H)$, which fits within the constraints.
