- **Prefix representation:** Every subarray sum is \(P_r-P_j\), where \(P_i\) is the prefix sum through index \(i\), and \(0 \le j < r \le N\).
- **Binomial expansion:** For each current prefix \(x=P_r\),
  \[
  \sum_{j<r}(x-P_j)^K
  =\sum_{t=0}^{K}\binom{K}{t}x^{K-t}(-1)^t
  \left(\sum_{j<r}P_j^t\right).
  \]
- **Maintained state:** `moments[t]` stores the sum of \(P_j^t\) over all previously processed prefixes, including \(P_0=0\). Thus initially `moments[0]=1` and all higher moments are zero.
- **Update order:** The contribution for the current prefix is computed before adding its powers to `moments`, ensuring only \(j<r\) are included.
- **Modular arithmetic:** Prefix sums, powers, moments, and the final answer are reduced modulo \(998244353\). Alternating signs from the binomial formula are handled directly.
- **Complexity:** Each element performs \(O(K)\) work and uses \(O(K)\) additional memory, giving \(O(NK)\) time and \(O(K)\) space.
