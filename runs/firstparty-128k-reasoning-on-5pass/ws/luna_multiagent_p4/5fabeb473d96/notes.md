- **Random-tree interpretation:** Each parent sequence is equally likely, and there are \((N-1)!\) sequences. Compute the expected distance in the random recursive tree, then multiply by \((N-1)!\) modulo \(998244353\).

- **Edge-path criterion:** For edge \(i\), let \(X_i(x)\) indicate that \(i\) is an ancestor of \(x\). Edge \(i\) is on the path between \(u<v\) exactly when \(X_i(u)\) and \(X_i(v)\) differ.

- **Single ancestor probability:** For \(i<x\), \(\Pr[X_i(x)=1]=1/i\). For \(i=x\), the probability is \(1\).

- **Joint ancestor probability:** For \(2\le i<u<v\),
  \[
  \Pr[X_i(u)=1 \text{ and } X_i(v)=1]=\frac{2}{i(i+1)}.
  \]
  This follows by tracking the subtree size \(S_t\) of \(i\). Its second moment is
  \[
  \mathbb E[S_t^2]=\frac{2t(t+1)}{i(i+1)}-\frac{t}{i},
  \]
  which gives the joint probability after conditioning on \(i\) being an ancestor of \(u\).

- **Edge coefficients:** The probability that edge \(i\) lies on the path from \(u\) to \(v\) is:
  - \(0\) if \(i>v\);
  - \(1\) if \(i=v\);
  - \(1/i\) if \(u<i<v\);
  - \((u-1)/u\) if \(i=u\) and \(u\ge2\);
  - \(2(i-1)/(i(i+1))\) if \(2\le i<u\).
  The root has no associated edge, so \(u=1\) needs no special edge term.

- **Query preprocessing:** Store prefix sums of weighted coefficients \(2(i-1)/(i(i+1))\) and \(1/i\). Each query is answered in \(O(1)\) after modular inverses are precomputed or calculated during preprocessing.

- **Complexity:** The implementation uses \(O(N+Q)\) time apart from modular inverse calls and \(O(N)\) memory. With the current direct `pow` calls, preprocessing is \(O(N\log MOD)\); this is still acceptable for \(N\le2\cdot10^5\).
