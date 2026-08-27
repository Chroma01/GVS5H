The problem reduces to checking for each building whether its top is visible from the viewpoint (0, h).  
A building i is hidden by a previous building j iff the line from (0, h) to (X_i, H_i) passes through (X_j, H_j).  
Solving for h gives the critical height  

\[
h_{j,i}=\frac{H_jX_i-H_iX_j}{X_i-X_j}
\]

(the y‑intercept of the line through the two points).  
Building i is visible exactly when \(h>\max_{j<i}h_{j,i}\).  
Thus the answer is \(\max_i\bigl(\max_{j<i}h_{j,i}\bigr)\); if this maximum is negative, all buildings are visible at height 0 and we output –1.

For a fixed i we need the maximum of a rational function over previous points.  
Geometrically, this is the maximum y‑intercept of lines joining the query point to previous points – the “upper tangent” problem.  
The set of previous points can be kept as an **upper convex hull** (the envelope of points that are never below a line segment).  
On each edge of this hull the function \(h_{j,i}\) is monotonic, and its values at the vertices form a unimodal sequence.  
We can therefore:

1. Maintain the upper hull while processing buildings in increasing X.
2. For each new building, binary‑search the hull to find the point maximising \(h_{j,i}\).

All comparisons are performed with exact integer arithmetic to avoid floating‑point errors; the final value is converted to a double for output.

The algorithm runs in \(O(N\log N)\) time and \(O(N)\) memory.