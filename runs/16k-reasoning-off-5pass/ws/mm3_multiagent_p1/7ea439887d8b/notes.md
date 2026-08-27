
## ideation
We have a directed graph with N vertices and M edges. We can either traverse an edge (cost 1) following its current direction, or reverse all edges globally (cost X). Reversing toggles which direction each edge is traversable.

The state is naturally represented by `(v, p)` where `p` is the parity of edge orientations: `p=0` for the original orientation, `p=1` for reversed. From a state `(v, p)`, the reachable neighbors in the same parity are the vertices `u` such that there is a directed edge from `v` to `u` in orientation `p`. In the original orientation (`p=0`), that is the original edge set; in reversed orientation (`p=1`), that corresponds to the original edge set reversed, i.e., the original edges `u -> v` become traversable `v -> u`.

Thus we can build a graph with `2 * N` nodes. Each original edge `a -> b` contributes:
- From `(a, 0)` to `(b, 0)` cost 1.
- From `(b, 1)` to `(a, 1)` cost 1.
Additionally, there is a flip edge from `(v, 0)` to `(v, 1)` with cost X, and from `(v, 1)` to `(v, 0)` with cost X (but the latter is not needed if we only need to reach parity 0 or 1 from start parity 0; we should consider both target parities since the optimal answer might end after a flip).

Run Dijkstra from `(1, 0)` on this graph of `2N` nodes and `2M + 2N` edges. The answer is `min(dist[N][0], dist[N][1])`.

Complexity: `O((N + M) log N)` time, `O(N + M)` memory. Since N, M ≤ 2e5, this is fine. Use 64-bit integers because cost can be up to ~1e9 * 2e5 = 2e14 (or larger per sample).

Edge cases:
- N=2, maybe trivial path.
- X=0: then we can flip freely; but that's still handled.
- The graph is guaranteed to have a path using these operations.
- Self-loops and multiple edges are allowed; we must not deduplicate the flip edges but they are N each so it's fine.

Implementation details:
- Use adjacency list: `adj = [[] for _ in range(2*N)]` where node `i` is `(i, 0)` and `i+N` is `(i, 1)` (0-indexed vertices).
- For each edge `a, b` (1-indexed): convert to 0-indexed.
  - `adj[a].append((b, 1))` for state 0.
  - `adj[b + N].append((a + N, 1))` for state 1.
- For each vertex `v` in 0..N-1:
  - `adj[v].append((v + N, X))` flip.
  - `adj[v + N].append((v, X))` flip back (to allow paths that end after odd flips or to return to parity 0 if needed).
- Run Dijkstra from source `0` (vertex 1, parity 0).
- Answer: `min(dist[N-1], dist[N-1 + N])`.

Dijkstra with heap of `(dist, node)`.

Pitfalls:
- Remember to use large integer type (Python int is unbounded, OK).
- Don't forget to add reverse flip edges; otherwise paths that flip an even number of times would be impossible.
- The state space is 2N, edges ~2M + 2N, so up to 6e5, manageable.

## worker: Implement `solve()`: read N, M, X, build the 2N st
- Modeled the problem as a shortest path on an expanded graph with `2N` states, one per vertex per edge-orientation parity.
- Each original edge `a -> b` creates two traversal edges: in state 0 `a -> b` and in state 1 `b -> a`, each with cost 1.
- The global "reverse all edges" operation corresponds to a flip between parity states with cost `X`, added for every vertex in both directions.
- Dijkstra from source `(1, 0)` (index 0) finds the minimum cost to any state for vertex `N`; the answer is the minimum of reaching `N` in either parity.
- Complexity: `O((N + M) log N)` time, `O(N + M)` memory, well within limits. Python ints handle the large costs (up to ~1e9 * 2e5 + path length).
