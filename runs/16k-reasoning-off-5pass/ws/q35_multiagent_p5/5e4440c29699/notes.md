
## ideation
The core difficulty is counting all valid paths in a grid with a rectangular hole, where paths can start at any block and move only Right or Up. The constraints ($W, H \le 10^6$) require an $O(W+H)$ or $O(1)$ solution after preprocessing, ruling out dynamic programming over the grid.

The strategy is:
1.  **Total Paths Calculation**: Compute the total number of paths in the full rectangle $[0, W] \times [0, H]$ without any holes. A path is defined by its start $(x_s, y_s)$ and end $(x_e, y_e)$. The number of paths from any start in $[0, x_e] \times [0, y_e]$ to $(x_e, y_e)$ is given by the combinatorial identity $\binom{x_e + y_e + 2}{x_e + 2}$. Summing this over all valid end points $(x_e, y_e)$ gives the total number of paths. This double sum can be computed efficiently using prefix sums of binomial coefficients.
2.  **Invalid Paths Calculation (Inclusion-Exclusion via First Entry)**: Subtract paths that enter the forbidden rectangle $[L, R] \times [D, U]$. A path is invalid if it visits any point in the hole. We count these by summing over the *first* point $P$ in the hole that the path visits.
    *   The first entry point must be on the "top-left" boundary of the hole relative to the movement direction (Right/Up). Specifically, it must be on the left edge $x=L$ (for $y \in [D, U]$) or the bottom edge $y=D$ (for $x \in [L, R]$).
    *   For a first entry point $P$, the path segment from the start to the point immediately preceding $P$ must lie entirely outside the hole.
    *   Due to the geometry (moving only Right/Up), if $P$ is on the left edge ($x=L, y>D$), the previous point must be $(L-1, y)$, which is outside the hole. If $P$ is on the bottom edge ($y=D, x>L$), the previous point must be $(x-1, D)$, which is outside. For the corner $(L,D)$, the previous point can be $(L-1, D)$ or $(L, D-1)$.
    *   The number of paths starting anywhere in the valid region and reaching a specific point $Q$ is $\binom{Q_x + Q_y + 2}{Q_x + 2}$.
3.  **Modulo Arithmetic**: All calculations must be performed modulo 998244353. We need factorials and inverse factorials for binomial coefficients.

Pitfalls:
*   Off-by-one errors in the combinatorial identities.
*   Double counting the corner $(L,D)$ if not handled carefully (summing left edge and bottom edge separately requires excluding the corner from one or handling it distinctly).
*   The bounds for the sums must be strictly within the valid ranges.
*   Large inputs require efficient precomputation of factorials.

## worker: Implement modular arithmetic and precompute factor
1.  **Total Paths Calculation**: The total number of paths in a full grid $[0, W] \times [0, H]$ is derived using combinatorial identities. The number of paths from any start point in $[0, x_e] \times [0, y_e]$ to $(x_e, y_e)$ is $\binom{x_e + y_e + 2}{x_e + 2}$. Summing this over all end points leads to a closed-form expression involving a single binomial coefficient minus a small correction term: $\binom{W+H+4}{H+1} - (1 + H+1 + \binom{H+2}{2})$. This allows $O(1)$ calculation after $O(W+H)$ preprocessing.
2.  **Bad Paths Calculation**: Paths entering the hole $[L, R] \times [D, U]$ are counted by summing over the *first* point of entry. Due to the monotonic movement (Right/Up), the first entry point must be on the left boundary ($x=L, y \in [D, U]$) or the bottom boundary ($y=D, x \in [L, R]$).
    *   For the corner $(L, D)$, the path could have arrived from $(L-1, D)$ or $(L, D-1)$. Both are valid previous points outside the hole.
    *   For other points on the left edge ($y > D$), the previous point must be $(L-1, y)$ to ensure the hole wasn't entered earlier.
    *   For other points on the bottom edge ($x > L$), the previous point must be $(x-1, D)$.
    *   The number of paths from any valid start to a point $(x, y)$ is $\binom{x+y+2}{x+2}$.
3.  **Complexity**: Precomputing factorials takes $O(W+H)$. The loops for bad paths run at most $O(W+H)$ times in total (specifically $O(U-D + R-L)$). The total time complexity is $O(W+H)$, which fits within the constraints ($10^6$). Space complexity is $O(W+H)$ for the factorial arrays.
4.  **Modulo Arithmetic**: All additions and subtractions are handled modulo 998244353. Division by 2 in the correction term is handled using integer division since the term is always an integer, but it's safer to compute it as `(H+2)*(H+1)//2` before modulo, or use modular inverse if it were a general division. Here, since it's a small constant correction derived from combinatorial sums, integer arithmetic is fine.
