- **Visibility reduction:** For observer height \(h\), the best point to use on building \(i\) is its top. Building \(i\) is visible iff its top slope \((H_i-h)/X_i\) is strictly larger than all previous top slopes. A previous building \(j\) blocks \(i\) exactly when \((H_i-h)/X_i \le (H_j-h)/X_j\).
- **Pair threshold:** For \(j<i\), equality occurs at
  \[
  h_{j,i}=\frac{H_jX_i-H_iX_j}{X_i-X_j}.
  \]
  Since \(X_i>X_j\), the difference of slopes increases with \(h\). Thus building \(i\) is blocked for \(h\le h_{j,i}\), and its first visible height is \(\max_{j<i} h_{j,i}\).
- **Global answer:** The bad-height set is monotone. The maximum non-negative bad height is \(\max_{j<i} h_{j,i}\). If this maximum is negative, all buildings are visible at height \(0\), so output exactly `-1`. If it is zero, output `0` because equality still intersects another building.
- **Envelope algorithm:** Treat each building as a line \(L_i(h)=(H_i-h)/X_i\). Slopes \(-1/X_i\) are strictly increasing because \(X_i\) is increasing. Maintain the upper envelope of previous lines with rational start heights. For a new line, pop the last hull line while
  \[
  \text{intersection}(\text{last},\text{new}) \le \text{start}(\text{last}).
  \]
  After popping, the intersection with the remaining last hull line is the first height where the new line exceeds the envelope, hence the blocking height for this building.
- **Exact arithmetic:** Store start fractions unreduced with positive denominators. Intersection numerator is \(H_{\text{old}}X_{\text{new}}-H_{\text{new}}X_{\text{old}}\), denominator is \(X_{\text{new}}-X_{\text{old}}\). All comparisons use integer cross multiplication, avoiding floating-point equality issues. Track the best non-negative fraction exactly.
- **Strictness and popping:** Visibility requires strict inequality, so equality at a candidate height is still bad. Removing hull lines on equality with `<=` is safe: such lines are never uniquely needed, and the same blocking height remains represented by the remaining envelope.
- **Output formatting:** If no non-negative candidate exists, print `-1` exactly. Otherwise print the best fraction as a floating-point value with exactly 18 digits after the decimal point using `f"{best_num / best_den:.18f}"`. The float conversion is safe for the required \(10^{-9}\) tolerance: the quotient magnitude is at most about \(10^{18}\), where relative error is around \(10^{-16}\), and small positive quotients have tiny absolute error.
- **Sample checks:** Sample 1 prints `1.500000000000000000`, sample 2 prints `-1`, sample 3 prints `0.000000000000000000`, and sample 4 prints `17.142857142857142350`.
- **Complexity and edge cases:** Each building is pushed and popped at most once, so the algorithm is \(O(N)\) amortized and \(O(N)\) memory. \(N=1\) has no blocker and outputs `-1`. Zero intersections are valid answers and must not be treated as `-1`.
