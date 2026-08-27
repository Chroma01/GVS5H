- **Gap representation:** Let \(g_j=x_{j+1}-x_j\) for \(1\le j<N\). The leftmost coordinate \(x_1\) never changes, because every operation keeps the two outer pieces fixed.
- **Effect of one operation:** For four consecutive coordinates \(a<b<c<d\), the inner pieces move to \(a+d-c\) and \(a+d-b\). In sorted order, the four coordinates become \(a,\ a+d-c,\ a+d-b,\ d\), so the three gaps \((g_i,g_{i+1},g_{i+2})\) become \((g_{i+2},g_{i+1},g_i)\). Thus the operation swaps \(g_i\) and \(g_{i+2}\).
- **Reachable permutations:** Swaps at distance two are adjacent swaps within the subsequence of odd-indexed gaps and within the subsequence of even-indexed gaps. Therefore, arbitrary permutations of odd-indexed gaps and arbitrary permutations of even-indexed gaps are independently reachable.
- **Objective:** The coordinate sum is
  \[
  \sum_{k=1}^N x_k
  =N x_1+\sum_{j=1}^{N-1}(N-j)g_j.
  \]
  The weights \(N-j\) strictly decrease as \(j\) increases. Since each parity class can be permuted independently, the rearrangement inequality shows that each parity subsequence should be sorted in ascending order, pairing larger gaps with smaller weights.
- **Complexity:** Sorting the two parity classes costs \(O(N\log N)\) time and \(O(N)\) memory. All calculations use Python integers.
