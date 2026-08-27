
## ideation
**Core difficulty** – The operation "reverse all edges" changes the entire edge set, so the graph isn’t static.  
We have to incorporate the fact that the current orientation of the graph depends on the parity of how many times we have reversed.

**Modeling** –  
Define two states for each vertex `v`:
- `v0` : we are in the original graph (parity of reversals = 0)
- `v1` : we are in the reversed graph (parity = 1)

Transitions:
1. **Move along an edge** – From `v0` we may go to any `u` such that `(v,u)` is an original edge; cost 1.  
   From `v1` we may go to any `u` such that `(v,u)` is a reversed edge, i.e. original edge `(u,v)`. Cost 1.
2. **Reverse all edges** – From any `v0` we can go to `v1` paying `X`, and from any `v1` to `v0` paying `X`. No movement.

The start state is `(1,0)`. The goal states are `(N,0)` or `(N,1)` (we can stop after any number of reversals). We need the minimum total cost.

**Solution** – Build a graph with `2N` nodes and at most `2M + 2N` edges, then run Dijkstra from the start node. The distance can be up to `~ 1e9 * number_of_reversals` (worst‑case may need many reversals but overall answer fits in 64‑bit), so use `int64`.

**Why Dijkstra works** – All edge costs are non‑negative (1 or X ≥ 1). Number of nodes ≤ 4·10⁵, edges ≤ 4·10⁵, feasible.

**Pitfalls** –
- Remember to build edges for both orientations: for each input edge `u→v`, add a move edge `u0→v0` (cost 1) and `v1→u1` (cost 1) (since in reversed mode direction flips).
- Add the reversal edges: for every `v` add `v0→v1` and `v1→v0` with cost `X`.
- Use 0‑based or 1‑based indexing consistently.
- Answer could exceed 32‑bit signed int; use `int64` in Go (`int64` is 64‑bit) or Python `int` (unbounded).
- Use a priority queue (min‑heap) for Dijkstra.

**Edge case considerations** – The graph may not be connected, but the problem guarantees reachability. Reversals may be needed even if no edges exist from current vertex (e.g., dead end). Reversing allows us to use the incoming edges.

**Complexity** – Building adjacency: `O(M)`. Dijkstra: `O((N+M) log (N+M))`, which is fine for 2·10⁵.

**Alternative viewpoint (not required)** – Could also use 0‑1 BFS if `X = 1`, but Dijkstra is general.

## worker: Implement the solution in Python: read inputs, bui
The solution models the dynamic graph by creating two states per vertex: mode 0 (original orientation) and mode 1 (all edges reversed). Each original edge `(u, v)` contributes a move edge `u0 → v0` and `v1 → u1` (cost 1). Reversing the whole graph is captured by zero-length movement edges `v0 ↔ v1` with cost `X`. Running Dijkstra on this 2N-node, ~2M+2N-edge graph yields the minimum cost to reach vertex `N` in either mode.
