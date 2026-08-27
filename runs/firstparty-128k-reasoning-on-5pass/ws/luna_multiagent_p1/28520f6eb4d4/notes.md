- **Visibility condition:** Building \(i\) is visible from \((0,h)\) exactly when its top slope \((H_i-h)/X_i\) is strictly larger than the top slope of every preceding building. Equality is blocking because the segment touches the preceding building.
- **Pair threshold:** For \(j<i\), the two top slopes are equal at
  \[
  T_{j,i}=\frac{X_iH_j-X_jH_i}{X_i-X_j}.
  \]
  Building \(i\) is blocked by \(j\) when \(h\le T_{j,i}\). Hence the required answer is the maximum threshold over all pairs.
- **Special cases:** If the maximum threshold is negative, height \(0\) already sees every building, so the output is \(-1\). If it is zero, the output is \(0\). For \(N=1\), there are no blocking pairs, so the output is \(-1\).
- **Hull reduction:** For a fixed current point \(P=(X_i,H_i)\), \(T_{j,i}\) is the \(x=0\) intercept of the line through \(P\) and the previous point \(Q_j\). A point below the upper convex hull cannot maximize this intercept; along a hull edge the intercept is monotone, so an endpoint is sufficient.
- **Hull maintenance:** Previous points are processed in increasing \(X\). Maintain the upper hull and remove the middle point \(B\) from \(A,B,C\) when
  \[
  (x_B-x_A)(H_C-H_A)-(H_B-H_A)(x_C-x_A)\ge 0.
  \]
  This also safely removes collinear middle points.
- **Queries:** For adjacent hull points \(A,B\), \(T(A)\ge T(B)\) exactly when \(\operatorname{orient}(P,A,B)\ge0\). The threshold sequence on the upper hull is unimodal, so binary search finds a maximizing hull point.
- **Exact arithmetic:** Hull orientation, binary-search comparisons, and fraction comparisons use Python integers. Only the final rational maximum is converted to floating point and printed with 18 digits after the decimal point.
- **Complexity:** Each point is inserted and removed from the hull at most once. Each query is \(O(\log N)\), for total \(O(N\log N)\) time and \(O(N)\) memory.
- **Validation:** The algorithm yields the sample outputs \(1.5\), \(-1\), \(0\), and \(17.142857142857142350\), and handles collinear points and zero or negative maximum thresholds correctly.
