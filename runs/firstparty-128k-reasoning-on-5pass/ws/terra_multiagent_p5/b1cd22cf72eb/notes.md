- **Optimization reduction:** If the final common pair sum is \(H\), every pair has total remaining length exactly \(H\), so the total remaining length is \(NH\). Since grinding only decreases lengths, the cost is `sum(U_i + D_i) - N*H`. Thus minimizing cost is equivalent to maximizing a feasible nonnegative integer \(H\).

- **Intervals for a fixed sum:** Let final upper lengths be \(a_i\), so final lower lengths are \(H-a_i\). Grinding constraints give
  \[
  \max(0,H-D_i) \le a_i \le \min(U_i,H).
  \]
  Write these endpoints as \(L_i\) and \(R_i\). The required upper-teeth condition is \(|a_i-a_{i+1}|\le X\).

- **Path interval feasibility criterion:** A sequence satisfying all intervals and Lipschitz constraints exists iff
  \[
  L_i \le R_j + X|i-j|
  \]
  for every pair \(i,j\). Necessity follows directly by comparing feasible values \(a_i\) and \(a_j\). For sufficiency, define
  \[
  a_i=\max_k(L_k-X|i-k|).
  \]
  This is \(X\)-Lipschitz and satisfies \(a_i\ge L_i\). The pairwise condition implies each term in the maximum is at most \(R_i\), so \(a_i\le R_i\).

- **Direct maximum formula:** The maximum feasible sum is
  \[
  H_{\max}=\min_{i,j}(D_i+U_j+X|i-j|).
  \]
  If \(H\) is at most this expression, then \(H-D_i\le U_j+X|i-j|\) for all pairs. This implies \(L_i\le R_j+X|i-j|\): if \(R_j=U_j\), it is the stated inequality; if \(R_j=H\), it is automatic since \(L_i\le H\). Hence \(H\) is feasible. Conversely, feasibility implies \(H-D_i\le U_j+X|i-j|\) for every pair, yielding the upper bound. The formula also includes \(i=j\), so \(H\le U_i+D_i\) is enforced. Nonnegativity is valid because all input lengths are positive and the formula is positive.

- **Linear-time computation:** For each index \(i\), compute
  \[
  G_i=\min_j(U_j+X|i-j|).
  \]
  A left-to-right sweep computes minima over \(j\le i\) with recurrence `best = min(U[i], best + X)`. A right-to-left sweep similarly handles \(j\ge i\). Then \(G_i\) is the minimum of the two sweep values, and
  \[
  H_{\max}=\min_i(D_i+G_i).
  \]
  Time complexity is \(O(N)\); memory is \(O(N)\).

- **Sample checks:** Sample 1 gives \(H_{\max}=4\), initial total \(31\), and cost \(31-4\cdot4=15\). Sample 2 gives \(H_{\max}=6\), hence cost \(0\). Sample 3 gives \(H_{\max}=2\), hence cost \(6000000002-4\cdot2=5999999994\).

- **Numeric safety:** Python integers safely handle the required totals; in fixed-width languages, 64-bit integers are necessary.
