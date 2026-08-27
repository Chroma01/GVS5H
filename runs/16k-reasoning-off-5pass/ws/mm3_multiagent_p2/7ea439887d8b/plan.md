We can model the problem as a 0-1 BFS on a graph with 2N states. For each vertex `v`, we keep two states: `v0` (edges in original direction) and `v1` (edges reversed). From `v0` you can either:
- Move along an original outgoing edge `v -> u` to state `u0` with cost 1.
- Pay X to flip the whole graph: from `v0` you go to `v1` with cost X.
Symmetrically, from `v1` you can move along original incoming edges (i.e., reverse edges) with cost 1, or flip back to `v0` with cost X.

Since all edge moves cost 1 and flip costs X, the edge weights are 0/1, so 0-1 BFS (deque) gives O(N+M) shortest path. Start from state `1_0`; answer is `min(dist[N_0], dist[N_1])`. Use 64-bit integers because X and distances can be up to ~1e14.