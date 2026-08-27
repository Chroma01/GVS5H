- **Edge variables:** Let each horizontal and vertical torus edge have a binary variable indicating whether a segment reaches that edge.
- **Type A condition:** Its left/right edge values differ, and its top/bottom edge values differ.
- **Type B condition:** Its left/right values are equal, its top/bottom values are equal, and the horizontal and vertical values differ.
- **Prefix representation:** Choose one horizontal seed variable per row and one vertical seed variable per column. Scanning from column 0 and row 0, edge values are determined by the XOR prefix of Type-A cells.
- **Parity requirements:** The XOR of Type-A indicators must be zero in every row and every column, because prefixes must close consistently around the torus. Any failed row or column parity immediately gives answer zero.
- **Type-B constraints:** For a Type-B cell `(i,j)`, the local opposite-edge condition becomes one XOR equation between row seed `i` and column seed `j`:
  `row_seed[i] XOR column_seed[j] = 1 XOR row_prefix_before_j XOR column_prefix_before_i`.
- **Weighted DSU:** Store the XOR relation from each node to its parent. Every Type-B equation is added to the DSU; contradictions give zero. If consistent, each connected component contributes one free binary seed, so the answer is `2^components mod 998244353`.
- **Complexity:** Each cell is processed once. DSU operations are effectively linear, with `O(HW α(H+W))` time and `O(H+W+W)` additional memory.
