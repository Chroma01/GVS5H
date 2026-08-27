- **Random recursive tree model:** Each parent choice is independent and uniform, so all \((N-1)!\) parent sequences are equally represented. The desired sum is \((N-1)!\) times the expected distance in a random recursive tree.
- **Ancestor probability:** For labels \(k<x\), \(\Pr(k\text{ is an ancestor of }x)=1/k\).
- **Joint ancestor probability:** For \(k<u<v\), \(\Pr(k\text{ is an ancestor of both }u,v)=2/(k(k+1))\). More generally, for any fixed \(r\) later vertices, the probability all belong to the subtree of \(k\) is \(r!/(k(k+1)\cdots(k+r-1))\). For two vertices, this follows from the Pólya-urn evolution of the subtree size: descendants of \(k\) form one color beginning with size \(1\), while all other vertices form the other color beginning with size \(k-1\).
- **Edge separation probabilities:** Let the query satisfy \(u<v\), and consider edge \(k-P_k\). It contributes iff exactly one endpoint is in the subtree rooted at \(k\):
  - \(k<u\): probability \(2/k-2\cdot 2/(k(k+1))=2(k-1)/(k(k+1))\).
  - \(k=u\): probability \(1-1/u=(u-1)/u\), because \(u\) is always in its own subtree and \(v\) is there with probability \(1/u\).
  - \(u<k<v\): probability \(1/k\), since only \(v\) can be in the subtree.
  - \(k=v\): probability \(1\).
  - \(k>v\): probability \(0\).
- **Expected-distance formula:** For \(u<v\),
  \[
  \sum_{k=2}^{u-1} A_k\frac{2(k-1)}{k(k+1)}
  +[u\ge2]A_u\frac{u-1}{u}
  +\sum_{k=u+1}^{v-1}\frac{A_k}{k}
  +A_v.
  \]
  For \(u=1\), the first two terms are absent.
- **Implementation:** Precompute modular inverses, two weighted prefix sums for the first and third ranges, and \((N-1)!\). Every query is answered in \(O(1)\); preprocessing is \(O(N)\).
- **Modular arithmetic:** All probability fractions are represented modulo \(998244353\), whose size exceeds \(N+1\), so all required denominators are invertible.
