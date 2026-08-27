- **Random-tree model:** Each parent \(P_i\) is chosen independently and uniformly from \(1,\ldots,i-1\). Therefore the sum over all \((N-1)!\) trees equals \((N-1)!\) times the expected distance in this random recursive tree.
- **Edge criterion:** Edge \(i\) separates vertices \(u,v\) exactly when precisely one of \(u,v\) belongs to the subtree rooted at \(i\).
- **Single ancestry probability:** For \(i<x\), \(\Pr(i\text{ is an ancestor of }x)=1/i\). For \(i=x\), the probability is \(1\).
- **Joint ancestry probability:** For \(i<u<v\), subtree membership indicators of later vertices follow a Pólya urn with initial counts \(1\) and \(i-1\). Equivalently, they are conditionally iid with a Beta\((1,i-1)\) parameter, giving
  \[
  \Pr(i\text{ ancestor of both }u,v)=\frac{2}{i(i+1)}.
  \]
- **Edge probabilities for \(u<v\):**
  - \(2\le i<u\):
    \[
    \Pr(i\text{ lies on path})=
    \frac1i+\frac1i-\frac4{i(i+1)}
    =\frac{2(i-1)}{i(i+1)}.
    \]
  - \(i=u\): edge \(u\) is on the path unless \(u\) is an ancestor of \(v\), so probability \((u-1)/u\). For \(u=1\), no such edge exists.
  - \(u<i<v\): probability \(1/i\), since \(i\) cannot be an ancestor of \(u\).
  - \(i=v\): probability \(1\), because \(v\) is an endpoint.
  - \(i>v\): probability \(0\).
- **Preprocessing:** Store prefix sums of \(A_i\cdot 2(i-1)/(i(i+1))\) and \(A_i/i\). Each query is answered in \(O(1)\), after \(O(N)\) preprocessing.
- **Modulo arithmetic:** All fractions use modular inverses modulo \(998244353\), and the final expected value is multiplied by \((N-1)!\).
