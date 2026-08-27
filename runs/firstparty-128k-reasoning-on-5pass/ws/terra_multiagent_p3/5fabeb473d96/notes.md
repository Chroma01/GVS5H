- **Core reduction:** There are exactly \((N-1)!\) parent arrays. Treat a uniformly selected parent array as a random recursive tree, compute expected distance, then multiply by \((N-1)!\) modulo \(998244353\).
- **Edge indicator:** The edge associated with vertex \(i\) is on the path between \(u<v\) iff \(i\) is an ancestor of exactly one of \(u,v\). Thus its expected contribution is \(A_i\) times that probability.
- **Ancestor probabilities:** For \(i<j\), \(\Pr(i\text{ is ancestor of }j)=1/i\). For two distinct later vertices \(u,v>i\), \(\Pr(i\text{ is ancestor of both})=2/(i(i+1))\).
- **Case \(i<u\):** By inclusion-exclusion, the probability of being ancestor of exactly one endpoint is \(2/i-4/(i(i+1))=2(i-1)/(i(i+1))\).
- **Case \(i=u\):** Vertex \(u\) is always its own ancestor, and it is an ancestor of \(v\) with probability \(1/u\). The edge is used with probability \((u-1)/u\). For \(u=1\), no such edge exists.
- **Case \(u<i<v\):** Such an \(i\) cannot be an ancestor of \(u\), and is an ancestor of \(v\) with probability \(1/i\).
- **Case \(i=v\):** The edge of \(v\) is always on the path, so its probability is \(1\).
- **Formula:** Expected distance is
  \[
  \sum_{i=2}^{u-1} A_i\frac{2(i-1)}{i(i+1)}
  + [u\ge2]A_u\frac{u-1}{u}
  + \sum_{i=u+1}^{v-1} A_i\frac1i
  + A_v.
  \]
- **Preprocessing:** Build modular inverses and two prefix sums: one for \(A_i\cdot2(i-1)/(i(i+1))\), and one for \(A_i/i\). Each query is then answered in \(O(1)\); preprocessing is \(O(N)\).
- **Implementation detail:** The low-coefficient prefix value at \(i=N\) is never queried because its range ends at \(u-1\le N-1\), so it may safely be set to zero.
