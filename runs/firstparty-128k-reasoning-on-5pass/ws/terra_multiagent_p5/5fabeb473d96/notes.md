- **Random-tree conversion:** Uniformly choosing every parent \(P_i\in[1,i-1]\) independently generates each valid sequence with probability \(1/(N-1)!\). Therefore the required sum is \((N-1)!\) times the expected distance in a random recursive tree.
- **Subtree urn process:** Fix \(k\). Let \(S_t\) be the size of the subtree rooted at \(k\) after vertices through \(t\) are inserted. Initially \(S_k=1\). At insertion \(t+1\), the subtree gains that vertex with probability \(S_t/t\). This is a Pólya urn with subtree color initially 1 and outside color initially \(k-1\).
- **Single ancestor probability:** For \(k<t\), \(\Pr(k\text{ is ancestor of }t)=1/k\).
- **Correct joint ancestor probability:** For \(k<u<v\), condition on subtree size \(S=S_{u-1}\). Vertex \(u\) joins the subtree with probability \(S/(u-1)\). If it does, the expected chance that \(v\) later joins is \((S+1)/u\). Hence the joint probability is \(E[S(S+1)]/((u-1)u)\). The urn rising-factorial moment is \(E[S_t(S_t+1)]=2t(t+1)/(k(k+1))\), so \(\Pr(k\text{ ancestor of both }u,v)=2/(k(k+1))\), independent of \(u,v\).
- **Edge separation probabilities:** For a query \(u<v\), edge \(k\) is on the path iff exactly one endpoint is in the subtree of \(k\). For \(2\le k<u\), this is \(2/k-4/(k(k+1))=2(k-1)/(k(k+1))\). For \(k=u\), it is \((u-1)/u\). For \(u<k<v\), it is \(1/k\). For \(k=v\), it is 1. Later edges contribute zero.
- **Formula:** Define \(D_i=\sum_{k=2}^i A_k\,2(k-1)/(k(k+1))\) and \(C_i=\sum_{k=2}^i A_k/k\). Then
  \[
  E[d(u,v)]=D_{u-1}+[u\ge2]A_u(u-1)/u+(C_{v-1}-C_u)+A_v.
  \]
  Multiply this by \((N-1)!\) modulo 998244353.
- **Validation:** Direct exhaustive enumeration of all parent sequences for small \(N\), all vertex pairs, and varied small weights agrees with the formula. In particular, the corrected coefficient for every edge before \(u\) is independent of the queried endpoint labels.
- **Complexity:** \(O(N+Q)\) time and \(O(N)\) memory.
