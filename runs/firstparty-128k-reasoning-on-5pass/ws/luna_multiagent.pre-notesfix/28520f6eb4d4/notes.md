
## ideation
The core difficulty is reducing visibility to an extremal geometric condition without checking all \(O(N^2)\) pairs. For a building \(i\) to the right of the observation point, it is enough to consider the line from the observer to the top of building \(i\): if that line clears every earlier building, some point of \(i\) is visible; if an earlier building intersects or rises above that line, the entire building is blocked. For a candidate observer height \(m\), building \(j<i\) blocks building \(i\) exactly when \((H_j-m)/X_j \ge (H_i-m)/X_i\). Thus the bad heights form an initial interval \([0,M]\), where \(M\) is the largest relevant pairwise line-intercept value. Equality is blocking, so the endpoint itself must be included. If \(M<0\), height zero is already sufficient and the required output is \(-1\).

## worker: Derive and implement a robust solution, preferably
For a pair \(j<i\), the critical observer height is the \(y\)-intercept
\[
\frac{X_iH_j-X_jH_i}{X_i-X_j}.
\]
The answer is the maximum nonnegative such value.

For fixed \(i\), this equals
\[
H_i-X_i\frac{H_i-H_j}{X_i-X_j},
\]
so we need the previous building \(j\) minimizing the slope to building \(i\). Such a point always lies on the upper convex hull of previous buildings.

The hull is maintained online with the usual monotone-stack rule. Slopes from a point to the vertices of the upper hull are unimodal, allowing a binary-search query in \(O(\log N)\). All comparisons use integer arithmetic, avoiding precision issues. Total complexity is \(O(N\log N)\), with \(O(N)\) memory.
