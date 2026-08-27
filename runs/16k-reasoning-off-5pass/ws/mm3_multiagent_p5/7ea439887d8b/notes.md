
## ideation
The problem is a shortest path problem with a global toggle operation. Since reversing the whole graph either toggles between the original and fully reversed graph, we can model the state of the system as a pair `(v, p)` where `v` is the current vertex and `p ∈ {0,1}` indicates whether edges are in the original orientation (p=0) or the reversed orientation (p=1). Moving along a directed edge costs 1 and does not change `p`. Reversing all edges costs `X` and toggles `p` without moving.

This yields a graph with `2N` states. From each state `(v, p)`:
- For every original edge `v → to`, we can move to `(to, p)` with cost 1.
- We can move to `(v, 1-p)` with cost `X`.

All edge weights are non-negative, so Dijkstra's algorithm works in `O((N+M) log N)`. The answer is `min(dist[N][0], dist[N][1])`. Edge weights are 1 and X (X up to 1e9), and distances may exceed 32-bit, so use 64-bit integers.

Pitfalls:
- Do not forget to build adjacency for both orientations.
- Use a fast adjacency list; scanning all outgoing edges for each pop of Dijkstra is required.
- For reversed orientation, edges go opposite of original.
- The graph is guaranteed to allow reaching N, but distances must be properly initialized to infinity.

## worker: Implement Dijkstra over 2N states in Python: read 
The solution models the problem as a shortest path on a graph with 2N states representing `(vertex, parity)` where parity indicates whether the current edge orientation is original (0) or reversed (1). 

- From state `(v, 0)`: can traverse original edges `v → to` with cost 1, staying in parity 0; or pay cost `X` to flip to `(v, 1)`.
- From state `(v, 1)`: can traverse reversed edges (which correspond to original edges going *into* `v`, i.e., `u → v` becomes `v → u`), with cost 1, staying in parity 1; or pay `X` to flip back to parity 0.

Dijkstra's algorithm handles non-negative weights (1 and X up to 10^9). Complexity is O((N+M) log N) with 2N nodes and O(N+M) edges per parity. Distances use 64-bit-safe large values (10^30) since the answer can exceed 32-bit range (e.g., sample 3).
