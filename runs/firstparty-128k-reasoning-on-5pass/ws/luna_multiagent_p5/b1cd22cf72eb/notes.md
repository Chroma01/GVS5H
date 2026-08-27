- **Fixed common height:** If the final common pair sum is \(H\), let \(A_i\) be the final upper tooth length. Since only reductions are allowed, \(0 \le A_i \le U_i\), and the final lower length \(H-A_i\) must satisfy \(0 \le H-A_i \le D_i\). Therefore:
  \[
  \max(0,H-D_i) \le A_i \le \min(U_i,H).
  \]
- **Adjacent constraint:** The selected upper lengths must satisfy \(|A_i-A_{i+1}| \le X\).
- **Interval propagation:** After processing position \(i-1\), suppose every value in reachable interval \([L,R]\) can be selected. Values at distance at most \(X\) from some reachable value form \([L-X,R+X]\). Intersecting this with the current tooth's allowed interval gives the next reachable interval. An empty intersection means \(H\) is infeasible.
- **Monotonicity:** If height \(H\) is feasible, every smaller height \(H'\) is feasible. Given a feasible sequence \(A_i\), replace each value by \(A'_i=\min(A_i,H')\). Clipping preserves the adjacent difference bound, and the resulting values satisfy the constraints for \(H'\). Thus binary search can find the maximum feasible \(H\).
- **Search bounds:** Height zero is always feasible. No feasible height exceeds \(\min_i(U_i+D_i)\), so binary search uses this as the exclusive upper bound.
- **Cost:** For common height \(H\), the final total tooth length is \(NH\). The initial total is \(\sum_i(U_i+D_i)\), so the grinding cost is \(\sum_i(U_i+D_i)-NH\).
- **Complexity:** Each feasibility check is \(O(N)\), and binary search performs \(O(\log 10^9)\) checks. Total complexity is \(O(N\log 10^9)\), with \(O(N)\) memory.
