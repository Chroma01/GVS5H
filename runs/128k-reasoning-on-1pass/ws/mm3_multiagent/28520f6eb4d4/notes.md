
## ideation
The problem asks for the maximum height \(h \ge 0\) at coordinate 0 from which at least one building is not visible.  
A building \(i\) is visible from \((0, h)\) iff the line from \((0, h)\) to \((X_i, H_i)\) has a slope greater than the slope to any previous building \(j < i\):  
\[
\frac{H_i - h}{X_i} > \max_{j < i} \frac{H_j - h}{X_j}.
\]  
Solving for \(h\) gives the critical height for each pair \((j, i)\):  
\[
h_{j,i} = \frac{H_j X_i - H_i X_j}{X_i - X_j}.
\]  
Building \(i\) is visible exactly when \(h > \max_{j < i} h_{j,i}\).  
Thus all buildings are visible iff \(h > M\), where  
\[
M = \max_{i} \max_{j < i} h_{j,i}.
\]  
If \(M < 0\), then even at \(h = 0\) all buildings are visible, so the answer is \(-1\); otherwise the answer is \(M\).

Geometrically, \(h_{j,i}\) is the y-intercept of the line through \((X_j, H_j)\) and \((X_i, H_i)\). For a fixed new point \((X_i, H_i)\), the maximum y-intercept over previous points is achieved on the **upper convex hull** of the previous points. Maintaining the upper hull while scanning buildings in increasing \(X\) allows efficient queries.

For each new building, we binary‑search the hull to find the point maximizing the y-intercept. The function is unimodal along the hull, so comparing values at adjacent vertices suffices. All comparisons are done with exact integer arithmetic to avoid floating‑point errors; the final value is converted to a double for output.

The algorithm runs in \(O(N \log N)\) time and \(O(N)\) memory.

## worker: **Read input**: store arrays `X[0..N-1]`, `H[0..N-
The algorithm computes the maximum height \(h\) from which at least one building is hidden.  
For a building \(i\) to be visible from \((0, h)\) we need  

\[
h > \max_{j<i} h_{j,i}, \qquad
h_{j,i} = \frac{H_j X_i - H_i X_j}{X_i - X_j},
\]

the y‑intercept of the line through the two points.  
All buildings are visible exactly when \(h > M\) where  

\[
M = \max_i \max_{j<i} h_{j,i}.
\]

If \(M < 0\) the answer is \(-1\); otherwise it is \(M\).

Geometrically, for a fixed \(i\) the maximum of \(h_{j,i}\) over previous points is attained on the **upper convex hull** of those points.  
We maintain the hull while scanning the buildings in increasing \(X\).  
For each new building we binary‑search the hull to find the point maximizing the y‑intercept (the function along the hull is unimodal).  
All comparisons are performed with exact integer arithmetic to avoid floating‑point errors; the final value is converted to a double for output.

The algorithm runs in \(O(N \log N)\) time and \(O(N)\) memory, well within the limits.
