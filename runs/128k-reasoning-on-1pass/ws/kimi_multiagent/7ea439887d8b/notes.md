
## ideation
The key observation is that the graph direction is global and depends only on how many times the reverse operation has been performed modulo 2. Thus the natural state is `(vertex, parity)`, where `parity=0` means original orientation and `parity=1` means all edges reversed. A move has cost `1` and follows outgoing edges in the current parity; a reverse has cost `X` and changes `(v,p)` to `(v,1-p)` without moving.

Core difficulty: avoid materializing an unnecessarily large graph while still supporting both orientations. The expanded graph has `2N` vertices and about `2M + 2N` edges if represented explicitly, which is still fine, but adjacency can be implicit: store original outgoing edges and original incoming edges; in parity `0` use outgoing, in parity `1` use incoming. Edge weights are positive but not uniform because `X` can differ from `1`, so plain BFS is invalid; Dijkstra is the standard fit.

Reachability is guaranteed in the original process, which implies reachability in the two-layer state graph. The answer is `min(dist[N][0], dist[N][1])` because it does not matter whether edges end reversed once vertex `N` is reached.

Pitfalls:
- Using BFS/0-1 BFS incorrectly; `X` may be neither `0` nor `1`.
- Integer overflow: costs can exceed 32-bit, as in Sample 3; use 64-bit distances.
- Building both orientations as separate full adjacency lists can double memory unnecessarily; store `out` and `in` once.
- Forgetting that reversing at the same vertex is allowed repeatedly and may be useful even if it seems wasteful.
- Self-loops and parallel edges are harmless for Dijkstra but should not break adjacency construction.
- Need fast input/output for `N,M <= 2e5`.

## worker: Write the complete Python solution: parse input, b
- State is `(vertex, parity)`, where `parity=0` means original edge directions and `parity=1` means all edges are reversed.
- Moving costs `1`: in parity `0` use `out_adj`, in parity `1` use `in_adj`.
- Reversing costs `X` and keeps the same vertex while flipping parity.
- Dijkstra over these `2N` states gives the minimum cost; answer is `min(dist0[N], dist1[N])`.
- Complexity is `O((N + M) log N)` time and `O(N + M)` memory. Python integers avoid overflow.
