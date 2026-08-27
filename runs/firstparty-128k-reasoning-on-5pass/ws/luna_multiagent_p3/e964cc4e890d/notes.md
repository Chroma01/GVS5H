- **Strong-connectivity criterion:** Every proper prefix cut must have at least one added edge directed from a white vertex on the right to a black vertex on the left. This is equivalent to the required strong connectivity of the graph.
- **Prefix data:** `whites[i]`, `blacks[i]`, and `balance[i] = whites[i] - blacks[i]` are computed for every cut.
- **Recurrence:** For every cut `j` with nonnegative balance, the first-return coefficient satisfies  
  `e[j] * fact(balance[j]) = fact(whites[j]) - sum(e[k] * fact(whites[j] - blacks[k]))`,  
  where the sum is over `0 < k < j`.
- **Initial-term correction:** The term `k = 0` is excluded from the subtraction. The unrestricted factorial term already counts the segment beginning at cut zero, so subtracting `e[0]` would incorrectly cancel it. Consequently, `e[0]` is initialized to zero.
- **CDQ evaluation:** Contributions from already-computed indices in the left half to indices in the right half are grouped by `blacks[k]`. The resulting sum is a convolution with the factorial sequence, allowing all cross-half contributions to be processed efficiently.
- **Complexity:** The implementation uses CDQ divide-and-conquer with NTT convolutions, requiring `O(N log^2 N)` time and `O(N log N)` temporary allocation.
- **Edge cases:** `BW` gives one valid pairing; `WB` gives zero. Strings beginning with `W` or ending with `B` correctly produce zero. `WWBB` also produces zero.
