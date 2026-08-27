- **Insertion recurrence:** For a permutation \(B\) of \(1,\ldots,m\), insert \(x=m+1\), with digit length \(d\), at a cut. Write \(B=UV\), where \(V\) has decimal length \(L(V)\). The new concatenation is
  \[
  f(U,x,V)=f(B)+(10^d-1)f(U)10^{L(V)}+x10^{L(V)}.
  \]
  Therefore, if \(S_m=\sum_B f(B)\), \(R_m=\sum_{B,\text{cuts}} f(U)10^{L(V)}\), and \(V_m=\sum_{B,\text{cuts}}10^{L(V)}\), then
  \[
  S_{m+1}=(m+1)S_m+(10^d-1)R_m+xV_m.
  \]
  This is a valid insertion recurrence, but \(R_m,V_m\) are not determined by \(S_m\), and directly maintaining all needed cut/suffix statistics leads to growing substring-like information rather than an immediate scalar O(N) recurrence.
- **Priority reformulation:** Give every number an independent continuous random priority; a permutation is obtained by sorting priorities increasingly. For fixed \(x\), condition on its priority being \(t\). Every other element independently lies after \(x\) with probability \(1-t\). Thus a number with digit length \(e\) contributes expected place-value factor \(t+(1-t)10^e\).
- **Contribution formula:** Let \(c_e\) be the count of e-digit numbers and define \(L_e(t)=10^e+(1-10^e)t\). For a fixed e-digit \(x\),
  \[
  \mathbb E[10^{\text{suffix digit length after }x}]
  =\int_0^1 \frac{\prod_j L_j(t)^{c_j}}{L_e(t)}\,dt.
  \]
  The desired sum is \(N!\) times the sum of \(x\) times this expectation over all \(x\). All values sharing a digit length have the same integral, so only sums of numbers in each class are needed.
- **Efficient polynomial construction:** There are at most six digit lengths. Let \(P(t)=\prod_eL_e(t)^{c_e}\), \(D(t)=\prod_eL_e(t)\), and
  \[
  E(t)=\sum_e c_eL'_e(t)\prod_{j\ne e}L_j(t).
  \]
  Logarithmic differentiation gives \(D(t)P'(t)=E(t)P(t)\). Comparing coefficients computes every coefficient of degree-N polynomial \(P\) using O(6N) operations. For each digit length, divide \(P\) by its linear \(L_e\) by a linear coefficient recurrence, integrate coefficients using modular inverses of \(1,\ldots,N\), and multiply by the sum of values in that class.
- **Complexity:** O(N times number of digit lengths), hence O(N), with O(N) memory. The shown implementation uses modular polynomial coefficients and is valid because N is below the prime modulus.
