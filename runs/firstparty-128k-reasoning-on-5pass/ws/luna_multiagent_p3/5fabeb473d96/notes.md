- **Tree distribution:** Every parent choice is independent and uniform over earlier vertices, so there are exactly \((N-1)!\) rooted recursive trees.

- **Edge contribution:** The total distance is obtained by summing, over every edge \(k\), its weight multiplied by the probability that removing that edge separates the queried vertices.

- **Edge \(v\):** For \(u<v\), the edge connecting \(v\) to its parent always lies on the path, so its probability is \(1\).

- **Edge \(u\):** For \(u\ge 2\), this edge fails to separate the endpoints exactly when \(u\) is an ancestor of \(v\). That event has probability \(1/u\), giving separation probability \(1-1/u\).

- **Intermediate edges:** For \(u<k<v\), vertex \(k\) cannot be an ancestor of \(u\). The edge \(k\) separates the endpoints exactly when \(k\) is an ancestor of \(v\), with probability \(1/k\).

- **Lower-index edges:** For \(2\le k<u\), the corrected separation probability is
  \[
  \Pr(k\text{ separates }u,v)=\frac{2(k-1)}{k(k+1)}.
  \]
  This is independent of the queried vertices once both indices exceed \(k\).

- **Prefix sums:** Precompute weighted prefix sums of \(A_k/k\) and \(A_k\cdot 2(k-1)/(k(k+1))\). Each query is then answered in \(O(1)\) time.

- **Modular arithmetic:** All divisions use precomputed modular inverses modulo \(998244353\). The expected weighted distance is multiplied by \((N-1)!\) to obtain the required sum over all trees.

- **Validation:** The formulas give sample 1 outputs \(2\) and \(3\), sample 2 output \(100\), and handle boundary cases such as \(u=1\), \(u=2\), and \(v=u+1\).
