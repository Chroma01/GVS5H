The problem can be modeled as a shortest path problem on a state graph where each state is defined by `(vertex, edge_orientation)`. The edge orientation can be either `0` (original) or `1` (reversed). We have two types of transitions:
1. Moving along an edge in the current orientation costs 1.
   - If orientation is 0, we can traverse original edges `u -> v`.
   - If orientation is 1, we can traverse reversed edges, which corresponds to original edges `v -> u` being traversed as `u -> v` in the reversed graph.
2. Reversing all edges costs X. This transitions the state from `(u, 0)` to `(u, 1)` and from `(u, 1)` to `(u, 0)`.

We can use 0-1 BFS or Dijkstra's algorithm to find the minimum cost to reach `(N, 0)` or `(N, 1)`. Since edge weights are either 1 or X, and X can be large, Dijkstra is safer. However, since moving costs 1 and reversing costs X, we can treat this as a graph with 2N nodes and 2M + 2N edges. Specifically:
- For each original edge `u -> v`:
  - Add edge `(u, 0) -> (v, 0)` with weight 1.
  - Add edge `(v, 1) -> (u, 1)` with weight 1 (because in reversed state, the edge `u->v` becomes `v->u`, so traversing it means going from `v` to `u` in the reversed graph).
- For each vertex `u`:
  - Add edge `(u, 0) -> (u, 1)` with weight X.
  - Add edge `(u, 1) -> (u, 0)` with weight X.

Then run Dijkstra from `(1, 0)` to find the shortest distance to `(N, 0)` and `(N, 1)`, and take the minimum.