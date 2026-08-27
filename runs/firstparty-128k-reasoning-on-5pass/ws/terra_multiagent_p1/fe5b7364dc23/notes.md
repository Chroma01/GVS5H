- **Approach:** Let prefix sums be \(S_0=0\), \(S_r=\sum_{i=1}^r A_i\). Every subarray sum is \(S_r-S_{l-1}\). For each current right endpoint \(r\), sum \((S_r-S_j)^K\) over all earlier prefix indices \(0\le j<r\).
- **Expansion:** By the binomial theorem,
  \[
  (S_r-S_j)^K=\sum_{t=0}^{K}\binom{K}{t}S_r^{K-t}(-1)^tS_j^t.
  \]
  Maintain `moments[t] = sum(S_j^t)` for all already inserted prefix sums \(j\).
- **Streaming order:** Initialize `moments[0] = 1` for \(S_0=0\). For each newly computed `prefix = S_r`, first calculate its contribution using existing moments, then insert its powers into moments. This guarantees only `j < r` are paired.
- **Complexity:** Computing powers, contribution, and moment updates costs \(O(K)\) per element. Total time is \(O(NK)\), memory is \(O(K)\), valid for \(N\le 2\cdot10^5\), \(K\le10\).
- **Modulo:** All prefix sums, powers, binomial coefficients, moments, and answer are evaluated modulo \(998244353\). Alternating signs are handled by addition/subtraction followed by modulo normalization.
- **Binomial coefficients:** The code constructs \(\binom{K}{t}\) iteratively using modular inverses. Since \(K\le10<998244353\), all inverses exist.
