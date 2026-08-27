- **Expected-distance recurrence:** Let \(D(u,v)\) be the expected distance in a uniformly random recursive-parent tree, for \(u<v\). At insertion of vertex \(v\), its parent is uniform in \(1,\ldots,v-1\), so
  \[
  D(u,v)=A_v+\frac{1}{v-1}\sum_{p=1}^{v-1}D(u,p).
  \]
- **Closed form:** Define \(C_u=\sum_{p=1}^{u-1}D(u,p)\). Solving the recurrence by tracking \(S_t=\sum_{p=1}^{t}D(u,p)\) gives
  \[
  D(u,v)=A_v+\frac{C_u}{u}+\sum_{k=u+1}^{v-1}\frac{A_k}{k}.
  \]
  Thus each query is answerable in \(O(1)\) after prefix sums of \(A_k/k\).
- **Computing \(C_u\):** Let \(W_n=\sum_{1\le x<y\le n}D(x,y)\), the expected total pairwise distance among vertices \(1,\ldots,n\). When inserting \(n\),
  \[
  C_n=(n-1)A_n+\frac{2W_{n-1}}{n-1},
  \qquad
  W_n=W_{n-1}+C_n.
  \]
  The first term is the new edge weight for each prior endpoint. The second follows because the parent is uniform and the ordered sum of old pair distances is \(2W_{n-1}\).
- **Final conversion:** There are \((N-1)!\) equally likely parent sequences. The required sum is \((N-1)!\cdot D(u,v)\) modulo 998244353.
- **Complexity:** \(O(N+Q)\) time and \(O(N)\) memory. Modular inverses are precomputed linearly.
