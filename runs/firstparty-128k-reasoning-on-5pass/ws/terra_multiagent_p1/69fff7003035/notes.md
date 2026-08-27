- **Generating polynomial:** Let \(c_d\) be the number of values in \([1,N]\) having exactly \(d\) decimal digits. Define \(P(t)=\prod_d(1+10^d t)^{c_d}\). The coefficient \(p_k=[t^k]P(t)\) equals the sum of \(10^{\text{total digit length}}\) over all size-\(k\) subsets of \(\{1,\ldots,N\}\).
- **Fixed value contribution:** For a fixed value \(x\) with digit length \(d\), exclude it using \(Q_d(t)=P(t)/(1+10^d t)\), with coefficients \(q_{d,k}\). Choosing a suffix subset of size \(k\) produces multiplier \(10^{\text{suffix digit total}}\), and its elements can be arranged in \(k!\) orders while the prefix has \((N-1-k)!\) orders. Thus the total contribution of one such \(x\) is
  \[
  x\sum_{k=0}^{N-1}q_{d,k}k!(N-1-k)!.
  \]
  Sum this multiplier times the arithmetic-series sum of all values having digit length \(d\).
- **Quotients:** No polynomial division or inverse is needed. Since \(P=(1+a t)Q\), where \(a=10^d\), coefficients satisfy \(q_0=p_0=1\) and \(q_k=p_k-aq_{k-1}\). This computes each of at most six quotients in \(O(N)\).
- **Computing P:** Each factor has coefficients \(\binom{c_d}{k}10^{dk}\), generated in linear time using modular inverses. Multiply the at most six factors with NTT convolution; factors are processed in increasing digit length, giving overall \(O(N\log N)\) time. The maximum transform size is at most the next power of two above \(2N+1\), valid for modulus 998244353.
- **Complexity:** Factor generation, factorials, quotient scans, and final summation are \(O(N)\). NTT products are \(O(N\log N)\). Memory usage is \(O(N)\).
