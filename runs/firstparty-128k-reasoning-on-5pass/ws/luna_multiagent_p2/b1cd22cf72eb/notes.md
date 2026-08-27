- **Reduction:** Let the final upper length at position \(i\) be \(A_i\), and let the common pair sum be \(H\). The final lower length is \(H-A_i\).
- **Allowed interval:** Since teeth can only be shortened, \(0 \le A_i \le U_i\) and \(0 \le H-A_i \le D_i\). Therefore:
  \[
  \max(0,H-D_i) \le A_i \le \min(U_i,H).
  \]
- **Cost:** Every final pair has total length \(H\), so the retained total is \(NH\). Consequently, grinding cost is
  \[
  \sum_i(U_i+D_i)-NH.
  \]
  Thus, maximizing feasible \(H\) minimizes the cost.
- **Feasibility check:** Maintain the interval of all possible values of \(A_i\) reachable while satisfying previous positions. From reachable interval \([low, high]\), the next position can reach \([low-X, high+X]\), which is intersected with its own allowed interval. If the intersection becomes empty, \(H\) is infeasible.
- **Optimization:** Feasibility is monotone in \(H\): if a value is feasible, every smaller nonnegative value is feasible. Binary search the maximum feasible \(H\), with upper bound \(\min_i(U_i+D_i)\).
- **Complexity:** Each feasibility check is \(O(N)\), and binary search takes \(O(\log V)\), where \(V \le 2\cdot10^9\). Total complexity is \(O(N\log V)\), using Python integers for safe arithmetic.
