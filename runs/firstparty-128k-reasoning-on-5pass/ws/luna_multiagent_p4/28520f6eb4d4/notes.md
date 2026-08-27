- **Visibility criterion:** For viewpoint \((0,h)\), building \(i\) has top slope \((H_i-h)/X_i\). Since all \(X_i>0\), the lower slope endpoints \(-h/X_i\) increase with \(i\). Building \(i\) is hidden exactly when its top slope is no greater than the maximum top slope of an earlier building.
- **Pairwise condition:** For \(j<i\), building \(j\) blocks building \(i\) when
  \[
  \frac{H_j-h}{X_j}\ge\frac{H_i-h}{X_i},
  \]
  equivalent to
  \[
  h\le\frac{X_iH_j-X_jH_i}{X_i-X_j}.
  \]
  Therefore the maximum invalid height is the maximum such pairwise threshold.
- **Geometric reformulation:** The threshold is the \(y\)-intercept at \(x=0\) of the line through \((X_j,H_j)\) and \((X_i,H_i)\). For fixed \(i\), maximizing it is equivalent to minimizing the slope from the current point to an earlier point.
- **Convex hull query:** The minimum slope to earlier points is attained on their lower convex hull. Slopes along this hull are unimodal for a fixed rightmost query point, so binary search finds the optimum in \(O(\log N)\).
- **Complexity:** The hull is maintained in amortized \(O(N)\), and all queries take \(O(N\log N)\). Integer cross multiplication avoids precision issues; floating point is used only for final output.
- **Edge cases:** If the maximum threshold is negative, every non-negative height sees all buildings, so output `-1`. A threshold of exactly zero means the answer is `0`.
