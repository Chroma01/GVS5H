
## ideation
**Core difficulty:**  
We have a directed graph where we can either walk along edges (cost 1) or flip *all* edges at cost X. The flip operation changes reachability drastically, so we need to track the current global orientation (original or reversed) as part of the state.

**Candidate approaches:**  
- **State expansion:** Create two layers of vertices — layer 0 (original direction) and layer 1 (reversed direction).  
  - From `v0` we can go to `u0` for each original edge `v → u` (cost 1).  
  - From `v1` we can go to `u1` for each original edge `u → v` (i.e., we follow reversed edges, cost 1).  
  - Flipping the whole graph moves from `v0` to `v1` and from `v1` to `v0` (cost X).  
- This gives a graph with `2N` nodes and `2M + 2N` edges.  
- Run Dijkstra from `(1,0)` to any `(N,0)` or `(N,1)`. Answer = min(dist[N][0], dist[N][1]).  
- Complexity `O((N+M) log N)` works for `2e5`.

**Pitfalls / details to watch:**  
- Use 0-indexed vertices internally but keep 1-indexed for the model.  
- The flip transition exists for *every* vertex, so we add two edges per vertex (layer 0 ↔ layer 1).  
- Edge weights are non‑negative, so Dijkstra is safe.  
- Use a 64‑bit integer (`long long` in C++ / `int` in Python is fine) because answer can exceed 2³¹ (sample 3: ~4.3e9).  
- Distances can be up to roughly `N + X` which fits 64-bit.  
- Use adjacency list of size `2N`; store edges with `(to, weight)`.  
- Only push to priority queue if we find a better distance.  
- Return min distance to target layer(s).

## worker: Implement the solution in Python: build the 2‑laye
- Modeled the problem as a shortest path on a graph with `2N` states: each vertex `v` has two copies, `v0` (original orientation) and `v1` (reversed orientation).
- Edges in the original orientation go `u0 → v0`; in the reversed orientation they go `v1 → u1`. Moving along an edge costs 1.
- The global flip operation is represented by edges `v0 ↔ v1` with cost `X` for every vertex.
- Ran Dijkstra from `(1,0)` (node `0`) to all states; the answer is the minimum of distances to vertex `N` in either layer.
- Complexity: `O((N+M) log N)` with `2N + 2M` edges, well within limits for `N, M ≤ 2×10^5`.
- Used 64-bit arithmetic (Python ints are arbitrary precision) to handle the large answer in sample 3.
- No early termination because the minimum could be reached at the target in the other layer while the current node is still the target in its own layer.
