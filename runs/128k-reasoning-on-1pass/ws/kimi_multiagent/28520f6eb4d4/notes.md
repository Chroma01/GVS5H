
## ideation
Core difficulty: visibility looks geometric/continuous, but for a fixed target building i the best Q is its top `(X_i, H_i)`: raising Q raises the segment height at every intermediate building `j < i`. Buildings after i cannot block the segment from `x=0` to `X_i`. Thus building i is visible iff the line from `(0,h)` to `(X_i,H_i)` is strictly above every previous top `(X_j,H_j)` at `x=X_j`.

This reduces to computing, for each i, the maximum over `j < i` of the y-intercept of the chord through `(X_j,H_j)` and `(X_i,H_i)`:

`b_ji = (X_i*H_j - X_j*H_i) / (X_i - X_j)`.

Building i is visible iff `h > max_j b_ji`; equality means grazing a blocker top and counts as not visible. So the answer is `max_i max_j b_ji` if that value is `>= 0`; if it is `< 0`, even height 0 sees everything and output must be exactly `-1`. Sample 3 is the key equality case: answer `0`, not `-1`.

Geometrically only upper-hull vertices of the points `(X_i,H_i)` can attain the maximum chord intercept. The proposed plan is the right shape: online append points with increasing x, maintain an upper hull, and binary-search the hull for the vertex maximizing the intercept with the new point. Main risks are orientation and predicate correctness: `cross(...) >= 0` vs `> 0`, whether the hull is upper/lower, and whether `slope_less(mid, mid+1, q)` truly tests that the objective increases from hull[mid] to hull[mid+1]. A wrong sign gives a local minimum, the wrong endpoint, or failure on collinear data.

Pitfalls: strict visibility vs inclusive intersection; `-1` condition is max threshold `< 0`, not `<= 0`; N=1 has no blockers and should be `-1`; keep comparisons integer/exact until final division; denominators are positive because x increases; collinear points can be popped without changing the max value but must not break binary search unimodality; output `-1` exactly, never `-1.000`.

## worker: Prove the reduction: for each i, Q=(X_i,H_i) is op
- For a fixed target building `i` and fixed viewing height `h`, let `Q = (X_i, q)`. At an earlier building `j < i`, the segment height is
  `h + (q - h) * X_j / X_i`.
  This is strictly increasing in `q`, so choosing the top `q = H_i` maximizes clearance over every earlier building simultaneously. Buildings after `i` cannot intersect the segment.
- Since all relevant heights are nonnegative, the segment cannot pass below an earlier building; it must pass strictly above its top. Touching the top is an intersection and therefore blocks visibility.
- Thus building `i` is visible iff for every `j < i`:
  `h > (X_i * H_j - X_j * H_i) / (X_i - X_j)`.
  Define `B` as the maximum of these values over all pairs `j < i`. Building `i` is visible iff `h > B_i`, so some building is invisible iff `h <= B`.
- If `B >= 0`, the answer is exactly `B`: equality grazes a blocker and is still not visible. If `B < 0`, height `0` already sees everything, so print `-1`. Hence `B = 0` correctly prints `0`, not `-1`.
- For a fixed right point, maximizing the chord's y-intercept is equivalent to minimizing its slope. Only upper-hull vertices can attain this minimum. The maintained hull has decreasing edge slopes, making slopes to the new point unimodal, so binary search finds the optimum. All comparisons remain exact integer operations until the final division.
- Complexity: `O(N log N)` time and `O(N)` memory.

## worker: Implement an exact O(N^2) brute force (integer cro
Added an exact O(N^2) brute force that scans every blocker/target pair j < i, keeps the maximum rational intercept by cross-multiplication, and returns None only when the maximum numerator is negative; therefore B = 0 remains answer 0 while B < 0 becomes -1. The differential tester compares exact rational answers, not floats, and reports points, hull answer, brute answer, and a witness pair on mismatch. It covers the samples, N=1, horizontal/equal-threshold cases, collinear zero/positive intercept cases, decreasing and increasing heights, exhaustive small cases, seeded random structured cases, and big-coordinate integer-stress cases. The program still solves stdin by default; running with --selftest executes the tester and exits nonzero on mismatch.
