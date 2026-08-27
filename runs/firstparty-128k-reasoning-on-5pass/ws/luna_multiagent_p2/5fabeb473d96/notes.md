- **Expectation conversion:** Choosing every parent \(P_i\) uniformly and independently from \([1,i-1]\) gives each of the \((N-1)!\) parent sequences equal probability. Therefore, the required sum is \((N-1)!\) times the expected distance.

- **Edge contributions:** For \(u<v\), the expected contribution of edge \(i\) is:
  - \(2\le i<u\): \(\frac{2(i-1)}{i(i+1)}\)
  - \(i=u\): \(1-\frac1u\)
  - \(u<i<v\): \(\frac1i\)
  - \(i=v\): \(1\)

- **Prefix sums:** Precompute prefix sums of \(A_i\cdot\frac{2(i-1)}{i(i+1)}\) and \(A_i/i\). For \(u>1\), combine the first prefix through \(u-1\), the contribution of edge \(u\), the reciprocal prefix over \(u+1,\ldots,v-1\), and \(A_v\). For \(u=1\), only the reciprocal range \(2,\ldots,v-1\) and \(A_v\) are needed.

- **Modular arithmetic:** All divisions use modular inverses modulo \(998244353\). Inverses are generated linearly through \(N+2\).

- **Complexity:** Preprocessing takes \(O(N)\), each query takes \(O(1)\), and memory usage is \(O(N)\).
