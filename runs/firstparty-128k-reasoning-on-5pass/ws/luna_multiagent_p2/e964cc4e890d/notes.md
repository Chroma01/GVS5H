- **Graph characterization:** Strong connectivity is equivalent to every proper prefix of vertices having an added matching edge entering it from the suffix. The fixed path always supplies an edge leaving every proper prefix.
- **Permutation model:** Number white vertices and black vertices from left to right. If black position \(j\) is paired with white \(\pi_j\), then \(\pi\) is a permutation of \(1,\ldots,N\).
- **Cut condition:** Let \(t_j\) be the number of whites before the \((j+1)\)-st black. For \(1\le j<N\), the condition is \(\max(\pi_1,\ldots,\pi_j)>t_j\).
- **Inclusion-exclusion recurrence:** If \(f[j]\) is the signed contribution of subsets whose last selected bad cut is \(j\), then
  \(f[j]=-\bigl(\sum_{i<j}f[i](t_j-i)!\bigr)/(t_j-j)!\).
  The final answer is \(N!+\sum_{j=1}^{N-1}f[j](N-j)!\).
- **CDQ optimization:** During a CDQ merge \([l,m)\to[m,r)\), all already-known \(f[i]\) for \(i\in[l,m)\) contribute to right-side queries. Since \(t_j\) is nondecreasing, shifting by \(t_m\) turns these contributions into one ordinary convolution with the factorial sequence.
- **Complexity:** Each CDQ level performs total \(O(N\log N)\) NTT work, giving \(O(N\log^2N)\) time and \(O(N\log N)\) temporary allocation over execution, with \(O(N)\) persistent arrays.
