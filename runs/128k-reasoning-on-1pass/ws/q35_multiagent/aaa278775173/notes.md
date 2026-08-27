
## ideation
The core difficulty lies in correctly tracking the sequence parity (`1, 2, 0, 2, 0...`) across diagonal directions and handling the 90-degree clockwise turn while ensuring the sequence remains continuous. A naive DFS/BFS would be too slow due to overlapping subproblems and branching. Dynamic Programming is ideal here.

We need two DP tables:
1. `back[d][r][c]`: Length of the valid sequence ending at `(r, c)` coming from direction `d`. This captures the first leg of the V-shape (or a straight line).
2. `fwd[d][r][c][p]`: Length of the valid continuation starting at `(r, c)` in direction `d`, given the parity `p` of the index at `(r, c)` (0 for even, 1 for odd). This captures the second leg after the turn.

The sequence rules dictate:
- Index 0: `1`
- Index `k >= 1`: `2` if `k` is odd, `0` if `k` is even.
- `back` computes forward along diagonals, checking if the current cell matches the expected value based on the previous length.
- `fwd` computes backward along diagonals, storing lengths for both parities. `p=0` expects `1` or `0`, `p=1` expects `2`.
- A clockwise turn occurs in the order: TL-BR → TR-BL → BR-TL → BL-TR → TL-BR.
- For each cell, we combine `back` from a direction `d1` with `fwd` from the clockwise-turn direction `d2`. The parity `p` is derived from the length of the first leg: `p = (L1 - 1) % 2`. The total length is `L1 + L2 - 1` (subtracting 1 because the turn cell is counted in both).
- Time Complexity: $O(NM)$, Space Complexity: $O(NM)$. Given $N, M \le 500$, this is well within limits.
