- **Prefix transformation:** Let \(P_r=\sum_{i=1}^r A_i\), with \(P_0=0\). Every subarray sum is \(P_r-P_j\) for \(0\le j<r\).
- **Binomial expansion:** For each current prefix \(x=P_r\),
  \[
  \sum_{j<r}(x-P_j)^K
  =\sum_{t=0}^{K}\binom{K}{t}(-1)^t x^{K-t}\sum_{j<r}P_j^t.
  \]
- **Maintained state:** `moments[t]` stores \(\sum_{j<r}P_j^t\) before processing the current prefix. It is initialized with \(P_0\), so `moments[0] = 1`.
- **Ordering:** The contribution for the current prefix is computed before inserting it into the moments, ensuring only valid \(j<r\) pairs are counted.
- **Complexity:** Each of the \(N\) prefixes performs \(O(K)\) work. Total complexity is \(O(NK)\), with \(O(K)\) memory.
- **Modular arithmetic:** Prefixes, powers, moments, and the final answer are reduced modulo \(998244353\).
