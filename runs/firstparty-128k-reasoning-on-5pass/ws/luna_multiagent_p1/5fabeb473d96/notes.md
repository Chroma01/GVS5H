- **Tree distribution:** Every parent choice \(P_i\) is independent and uniform over \(1,\ldots,i-1\). Thus there are \((N-1)!\) trees, and the required answer is \((N-1)!\) times the expected distance.

- **Edge criterion:** Edge \((P_i,i)\) lies on the path between \(u<v\) exactly when exactly one of \(u,v\) belongs to the subtree rooted at \(i\).

- **Descendant probability:** For any \(x>i\), the probability that \(x\) is in the subtree rooted at \(i\) is \(1/i\).

- **Case \(i>v\):** Neither query vertex can be below \(i\), so the contribution is zero.

- **Case \(u<i<v\):** Vertex \(u\) is not below \(i\), while \(v\) is below \(i\) with probability \(1/i\). The separation probability is \(1/i\).

- **Case \(i=v\):** Vertex \(v\) is always in its own subtree and \(u<v\) cannot be below \(v\), so the separation probability is \(1\).

- **Case \(i=u\):** Vertex \(u\) is always in its own subtree. Vertex \(v\) is below \(u\) with probability \(1/u\), so the separation probability is \(1-1/u\).

- **Case \(i<u<v\):** Let \(S_t\) be the size of the subtree rooted at \(i\) after vertices through \(t\) have been inserted. For \(t\ge i\), \(\mathbb E[S_t]=t/i\). Writing \(G_t=\mathbb E[S_t(S_t-1)]\), the insertion recurrence gives
  \[
  G_{t+1}=\left(1+\frac2t\right)G_t+\frac2i,
  \]
  hence
  \[
  G_t=\frac{2t(t-i)}{i(i+1)}.
  \]
  Taking \(t=u-1\), the probability that both \(u\) and \(v\) are descendants of \(i\) is
  \[
  \frac{\mathbb E[S_{u-1}^2+S_{u-1}]}{u(u-1)}
  =\frac{2}{i(i+1)}.
  \]
  Therefore the separation probability is
  \[
  \frac2i-\frac4{i(i+1)}
  =\frac{2(i-1)}{i(i+1)}.
  \]

- **Preprocessing:** Prefix sums of \(A_i/i\) and \(A_i\,2(i-1)/(i(i+1))\) allow each query to be answered in \(O(1)\), after \(O(N)\) preprocessing. Total complexity is \(O(N+Q)\).
