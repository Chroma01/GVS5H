- **Visibility threshold:** For a building \(i\), it is sufficient to consider its top \((X_i,H_i)\). The top is visible exactly when the segment from \((0,h)\) to that top stays strictly above every earlier building \(j<i\) at \(X_j\). Equality is blocked because touching another building counts as intersection.
- **Pair threshold:** The line through \((0,h)\) and \((X_i,H_i)\) passes through height \(H_j\) at \(X_j\) when
  \[
  h=\frac{X_iH_j-X_jH_i}{X_i-X_j}.
  \]
  Thus the critical height is the maximum of this value over all \(j<i\). If it is negative, every nonnegative height works and the answer is \(-1\); if it is zero, the answer is \(0\).
- **Convex-hull reduction:** For fixed current point \(C=(X_i,H_i)\), maximize the \(y\)-intercept of lines joining \(C\) to previous points. Only vertices of the upper convex hull of previous points can maximize it.
- **Hull orientation:** Points are stored in increasing \(X\). The upper hull has clockwise turns, so while appending a point \(C\), remove the last point while
  \[
  \operatorname{orient}(A,B,C)\ge 0.
  \]
  Removing collinear middle points is safe because all points on the same hull edge produce the same relevant tangent value.
- **Binary query:** For consecutive hull points \(A,B\), exact algebra gives
  \[
  b_A-b_B
  =\frac{X_i\operatorname{orient}(A,B,C)}
  {(X_i-X_A)(X_i-X_B)},
  \]
  where \(b_P\) is the intercept obtained using point \(P\). Therefore \(b_A<b_B\) exactly when \(\operatorname{orient}(A,B,C)<0\). Along an upper convex chain these comparisons change sign at most once, so the intercept sequence is unimodal and binary search finds its maximum.
- **Exactness and complexity:** All orientation tests and fraction comparisons use Python integers, avoiding overflow and precision errors. Each point is inserted once and removed at most once; each query is \(O(\log N)\). Total complexity is \(O(N\log N)\), with \(O(N)\) memory.
