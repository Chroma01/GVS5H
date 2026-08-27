- **Perimeter mapping:** Every boundary point is mapped to a unique coordinate in `[0, 4*side)`, ordered counterclockwise. Bottom includes both bottom corners, right owns the top-right corner, top owns the top-left corner, and left contains only its interior points.

- **Distance reduction:** The answer is at most `side` because `k >= 4` and the cyclic perimeter gaps sum to `4*side`. For any candidate `D <= side`, two boundary points have Manhattan distance at least `D` exactly when their shorter perimeter separation is at least `D`. Points on the same or adjacent sides follow the corresponding boundary route; points on opposite sides always have Manhattan distance at least `side`, so they impose no stricter condition.

- **Circular feasibility:** A selected set is valid precisely when every cyclic gap between consecutive selected perimeter positions is at least `D`.

- **Greedy selection:** After fixing the first selected point, repeatedly choose the earliest point at least `D` farther along the perimeter. This greedy choice leaves maximal space for all remaining points and is sufficient for checking that starting point.

- **Wraparound:** Duplicate the sorted coordinates with one perimeter length added. The transition table is computed over all duplicated indices, while a candidate sequence is restricted to fewer than one full cycle from its starting index. The final gap back to the start is checked explicitly.

- **Complexity:** Each feasibility check takes `O(n + nk)` time using two pointers and greedy transitions, where `n = len(points)` and `k <= 25`. Binary search contributes `O(log side)` checks. Memory usage is `O(n)`.

- **Verification:** The implementation matches all three examples. Exhaustive small-square comparisons against brute-force subset enumeration, including cases crossing the perimeter coordinate origin and points on corners, validate the circular greedy check and the Manhattan/perimeter reduction.
