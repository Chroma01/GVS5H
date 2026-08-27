
## ideation
The core difficulty is converting a distance in every increasing-label recursive tree into an aggregate that can be answered for many vertex pairs. A useful linearity-of-expectation viewpoint is to consider each edge \(i\) separately: its weight contributes exactly when deleting that edge places the two queried vertices on opposite sides. Since all parent choices are independent and uniform over the earlier labels, the relevant separation probabilities depend only on the relative order of \(i\), \(u\), and \(v\). The final expectation must then be multiplied by \((N-1)!\) to obtain the sum over all parent sequences.

Important implementation issues include distinguishing the cases where \(i\) is one of the queried vertices, handling \(i<u\), \(u<i<v\), and \(v<i\) separately, and ensuring that all factorials, inverse factorials, probability expressions, and weighted sums are reduced modulo \(998244353\). The edge indexed by \(i\) is directed toward the root through its parent, so “\(i\) separates the endpoints” is equivalent to exactly one endpoint being in the descendant subtree of \(i\).

## worker: Derive and verify an explicit closed-form probabil
For an edge indexed by \(i\), let \(D_x\) be the event that \(x\) belongs to the descendant subtree of \(i\). The edge lies on the path between \(u<v\) exactly when one of \(D_u,D_v\) holds.

The required probabilities are:

- \(i<u\):
  \[
  \Pr(D_u)=\Pr(D_v)=\frac1i,\qquad
  \Pr(D_u\cap D_v)=\frac{2}{i(i+1)},
  \]
  hence
  \[
  \Pr(\text{edge }i\text{ lies on path})=
  \frac{2(i-1)}{i(i+1)}.
  \]

- \(i=u\): probability \((u-1)/u\).
- \(u<i<v\): probability \(1/i\).
- \(i=v\): probability \(1\).
- \(i>v\): probability \(0\).

Therefore the expected distance is
\[
\sum_{i=2}^{u-1} A_i\frac{2(i-1)}{i(i+1)}
+A_u\frac{u-1}{u}
+\sum_{i=u+1}^{v-1}\frac{A_i}{i}
+A_v,
\]
with the \(A_u\) term omitted when \(u=1\).

The sums are answered using two prefix arrays. Multiplication by \((N-1)!\) converts the expectation over uniformly random parent choices into the sum over all \((N-1)!\) recursive trees.
