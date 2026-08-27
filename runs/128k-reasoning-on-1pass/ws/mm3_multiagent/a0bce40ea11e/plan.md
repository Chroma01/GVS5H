We need to compute the sum of \(B^p\) over all matrices \(B\) obtained by replacing each zero in \(A\) with a non-zero value modulo \(p\), where \(p\) is prime. The key observation is that over a field of characteristic \(p\), the expansion of a matrix power \((A_0 + \sum x_i E_i)^p\) simplifies due to the vanishing of binomial coefficients \(\binom{p}{k}\) for \(0<k<p\). After summing over all choices of the variables \(x_i \in \mathbb{F}_p^\times\), only terms where each variable appears a multiple of \(p-1\) times survive. Since the total length is \(p\), the only surviving terms are:
- The pure \(A_0^p\) term.
- For each zero position \((r,c)\), terms containing exactly \(p-1\) copies of the elementary matrix \(E_{rc}\) and one copy of \(A_0\).

Summing these over all positions of the single \(A_0\) gives a matrix \(T_{rc} = \sum_{t=0}^{p-1} (E_{rc})^t A_0 (E_{rc})^{p-1-t}\). By analyzing the powers of \(E_{rc}\), we obtain closed forms for \(T_{rc}\):
- If \(r = c\) (diagonal zero): \(T_{rc} = A_0 E_{rc} + E_{rc} A_0 - 2 E_{rc} A_0 E_{rc} \pmod{p}\).
- If \(r \neq c\) (off-diagonal zero):  
  - For \(p = 3\): \(T_{rc} = E_{rc} A_0 E_{rc}\).  
  - For \(p > 3\): \(T_{rc} = 0\).

The total sum is \(S = (-1)^K \bigl(A_0^p + \sum T_{rc}\bigr) \pmod{p}\), where \(K\) is the number of zeros. The case \(p = 2\) is handled separately by direct matrix squaring.