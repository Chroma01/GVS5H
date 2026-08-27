- **Visibility threshold:** To see building \(i\), aiming at its roof is always optimal. For every earlier building \(j<i\), the segment from observer \((0,h)\) to roof \((X_i,H_i)\) avoids building \(j\) exactly when
  \[
  h > \frac{H_jX_i-H_iX_j}{X_i-X_j}.
  \]
  Equality is blocked because touching another building counts as intersection.

- **Global answer:** Let \(B_{j,i}\) be the fraction above. All buildings are visible exactly when \(h>\max_{j<i}B_{j,i}\). Therefore the requested maximum non-visible height is that maximum if it is nonnegative; if it is negative, height zero already works and the output is `-1`.

- **Key simplification:** No actual convex hull is needed. Transform each roof point by
  \[
  (X_i,H_i)\mapsto (u_i,v_i)=\left(\frac1{X_i},\frac{H_i}{X_i}\right).
  \]
  Since \(X_i\) increases, \(u_i\) decreases. For every \(j<i\),
  \[
  B_{j,i}=\frac{v_j-v_i}{u_j-u_i},
  \]
  the secant slope in transformed coordinates.

- **Why adjacent pairs suffice:** The secant slope between transformed points \(j\) and \(i\) is a positive-denominator weighted average of the consecutive secant slopes between points \(j,j+1,\ldots,i\). Hence it cannot exceed the maximum consecutive slope. Consequently,
  \[
  \max_{j<i} B_{j,i}=\max_{i=1}^{N-1}B_{i,i+1}.
  \]
  This is an \(O(N)\) degeneration of the possible monotone-hull viewpoint: every long secant is already bounded by an adjacent transformed edge, so neither an upper nor lower hull must be maintained.

- **Exact comparison:** For adjacent pair \(i,i+1\),
  \[
  B_i=\frac{H_iX_{i+1}-H_{i+1}X_i}{X_{i+1}-X_i}.
  \]
  Denominators are positive. Compare fractions \(a/b\) and \(c/d\) using `a*d > c*b`. Python integers safely handle all products exactly.

- **Edge cases:** If \(N=1\), there are no blockers, so output `-1`. If the maximum fraction is exactly zero, output zero, not `-1`, because height zero still touches a blocking roof.
