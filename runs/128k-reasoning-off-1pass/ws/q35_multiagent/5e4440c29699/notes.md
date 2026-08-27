
## ideation
The core difficulty lies in efficiently counting all valid paths in a grid with a rectangular hole, where paths can start at any valid block and move only right or up. A brute-force simulation is impossible due to constraints ($10^6$). The key insight is to use the Principle of Inclusion-Exclusion (PIE) on the geometry of the valid region.

The valid region is the full rectangle $[0, W] \times [0, H]$ minus the hole $[L, R-1] \times [D, U-1]$.
Instead of subtracting "bad" paths directly (which is complex because a path might enter and exit the hole), we can decompose the valid region into a union of simpler rectangular regions that do not contain the hole, or use PIE on the full grid by subtracting paths that touch the hole.

However, a more robust and standard approach for "grid with hole" path counting (summing over all start/end pairs) is to define a function `CountPaths(W, H)` that calculates the total number of paths in a solid $W \times H$ grid (coordinates $0..W, 0..H$).
The valid region can be viewed as the full grid minus the hole.
Using PIE on the set of paths:
Total Valid Paths = (Paths in Full Grid) - (Paths that touch the Hole).
Calculating "Paths that touch the Hole" is tricky.

Alternative Decomposition:
The valid region is the union of 4 rectangles:
1. Left: $[0, L-1] \times [0, H]$
2. Right: $[R, W] \times [0, H]$
3. Bottom: $[0, W] \times [0, D-1]$
4. Top: $[0, W] \times [U, H]$

Note: These rectangles overlap. For example, the bottom-left corner is in both Left and Bottom.
We can use PIE on these 4 sets.
$|A \cup B \cup C \cup D| = \sum |A| - \sum |A \cap B| + \sum |A \cap B \cap C| - |A \cap B \cap C \cap D|$.

Each intersection of these axis-aligned rectangles is also an axis-aligned rectangle (possibly empty).
For a rectangle defined by $x \in [x_1, x_2]$ and $y \in [y_1, y_2]$, the number of paths is `CountPaths(x_2 - x_1, y_2 - y_1)`.
Wait, `CountPaths(W, H)` should be defined for a grid of width $W$ and height $H$ (points $0..W, 0..H$).
If the rectangle is $[x_1, x_2] \times [y_1, y_2]$, the width is $x_2 - x_1$ and height is $y_2 - y_1$.
So we need a function `Solve(W, H)` that returns the total number of paths in a $(W+1) \times (H+1)$ grid of points.

The intersections will be:
- Single rects: Left, Right, Bottom, Top.
- Pairs: Left$\cap$Bottom, Left$\cap$Top, Right$\cap$Bottom, Right$\cap$Top. (Left$\cap$Right is empty if $L \le R$, Bottom$\cap$Top is empty if $D \le U$).
- Triples: Left$\cap$Bottom$\cap$Top (empty), etc. Only Left$\cap$Bottom$\cap$Right? No, Left and Right are disjoint. So only intersections involving one from {Left, Right} and one from {Bottom, Top} are non-empty for pairs. Triples involving Left, Right and Bottom would be empty.
- Quadruple: Empty.

So we only need to compute `Solve` for specific sub-rectangles.
We need to implement `Solve(W, H)` efficiently.
Formula for `Solve(W, H)`:
$\sum_{dx=0}^W \sum_{dy=0}^H (W - dx + 1)(H - dy + 1) \binom{dx+dy}{dx}$
This can be computed in $O(W+H)$ or $O(1)$ with precomputed factorials and prefix sums of binomial coefficients. Given $W, H \le 10^6$, $O(W+H)$ is acceptable if we only call it a constant number of times (which we do, ~8 times).

Pitfalls:
- Modulo arithmetic at every step.
- Handling empty rectangles (width or height < 0) by returning 0.
- Correctly identifying the coordinates of the intersection rectangles.
- The definition of `Solve(W, H)`: input is the span (max - min), so for $[0, L-1]$, width is $L-1$. If $L=0$, width is -1 -> empty.

## worker: Implement a modular arithmetic helper class or fun
1.  **Problem Decomposition**: The problem asks for the number of paths in a grid with a rectangular hole. The valid region is the union of 4 rectangles: Left, Right, Bottom, and Top of the hole.
2.  **Inclusion-Exclusion Principle (PIE)**: Since these 4 rectangles overlap, we use PIE. The valid paths are those that lie entirely within the union of these 4 rectangles.
    *   Sum of paths in single rectangles.
    *   Subtract paths in pairwise intersections.
    *   Add paths in triple intersections (which are empty in this configuration).
    *   Subtract paths in quadruple intersection (empty).
3.  **Counting Paths in a Rectangle**: The function `count_paths(w, h)` computes the total number of paths in a grid of width `w` and height `h` (coordinates $0..w, 0..h$).
    *   The formula derived is: $\sum_{i=0}^w (w+1-i) \left[ (h+1) \binom{i+h+1}{i+1} - (i+1) \binom{i+h+1}{i+2} \right]$.
    *   This allows $O(W)$ computation per rectangle, which is efficient enough given $W, H \le 10^6$ and only ~8 calls.
4.  **Modular Arithmetic**: All calculations are performed modulo 998244353. Factorials and inverse factorials are precomputed for $O(1)$ combination calculations.
5.  **Edge Cases**: Rectangles with negative width or height (e.g., if $L=0$, Left rectangle has width -1) return 0 paths.
