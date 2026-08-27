
## ideation
**Core difficulty:** The twist is that we can globally *reverse all edges* at cost X, possibly multiple times. A naive BFS that explores paths with flips would blow up because flips affect all edges. We need a state representation that captures “which orientation are we currently in?” and integrates that with per-edge moves.

**Key insight:** A flip is global, so for the purpose of the current orientation, we only need to know whether the graph is in its original orientation or its reversed orientation. That is a binary state per vertex.

**State graph (2N nodes):**
- For each vertex `v` we have two states: `v0` (original orientation) and `v1` (reversed orientation).
- From `v0`:
  - For every original outgoing edge `v -> u`, we can go to `u0` with cost 1.
  - Pay X to flip everything: go to `v1` with cost X.
- From `v1`:
  - The “available” edges are the original incoming edges (which become outgoing after reversal). So for every original edge `u -> v`, we can go to `u1` with cost 1.
  - Pay X to flip back: go to `v0` with cost X.

Thus each move along an edge costs 1; each flip costs X. Edge weights are 0/1, perfect for 0‑1 BFS.

**Start state:** `1_0` (graph initially in original orientation, at vertex 1).  
**Goal:** minimum of `dist[N_0]` and `dist[N_1]`.

**Why 0‑1 BFS works:** All transition costs are 0 or 1. We push flips (cost X) to the front/back of deque based on whether X is treated as 0 or 1? Wait — X can be up to 1e9, not 0 or 1. So 0‑1 BFS as stated in the plan is **wrong** unless we reweight.

**Reweighting / trick:** Since we can take many cheap edge moves (cost 1) between flips, we need Dijkstra. But the graph has 2N states and 2M transitions, so Dijkstra is O((N+M) log N) — acceptable for 2e5.

Alternative: since only two possible transition weights (1 and X), we can use 0‑1 BFS *only if* we model each move as 0/1. But cost X is not binary. However, we can transform: treat each flip as a “port” of weight X, but X can be large. So Dijkstra (or a two-layer BFS with deque using small/large cost) is the safe approach.

**Edge cases / pitfalls:**
- `N` up to 2e5, `M` up to 2e5 → `dist` array of size `2N` with int64.
- Answer can exceed 32‑bit (sample 3 shows ~4.3e9 > 2^31) — must use 64‑bit (Python int is fine).
- The guarantee “you can reach N” ensures the target is reachable; still handle unreachable theoretically by keeping `INF`.
- Build adjacency list both for outgoing (used when in state 0) and incoming (used when in state 1). To avoid building two separate lists, we can store edges and, for state 1, traverse all incoming edges of `v` (i.e., for each edge `u -> v`, we can go to `u1`). Building an incoming adjacency list (or storing edges in both lists) keeps total memory O(N+M).
- Multi-edges? Not forbidden; store as separate edges. Self-loops allowed? Yes, but harmless.

**Correctness sketch:**
- Any sequence of operations corresponds to a walk in the 2N state graph: each edge traversal follows the current orientation, each flip switches the orientation label. Costs match (1 for edge, X for flip). Shortest path in this state graph equals minimum cost. Dijkstra computes it. 2N states, 2M edges, so O((N+M) log(N)).

**Alternative ideas considered:**
- Unweighted layers + Dijkstra with virtual “flip nodes” — same complexity.
- BFS in original graph with “distance” measured as #flips and #edges separately → 2D cost, no good.
- 0‑1 BFS only works if X ∈ {0,1}, which is not guaranteed.

**Conclusion:** Use Dijkstra on a graph of 2N vertices (split each vertex into `v0` and `v1`), with edges:
- `v0 -> u0` for each original `v->u` (weight 1)
- `v0 -> v1` (weight X)
- `v1 -> u1` for each original `u->v` (weight 1)  ← incoming edges of v in original graph
- `v1 -> v0` (weight X)

Start `1_0`. Answer = `min(dist[N_0], dist[N_1])`.

## worker: Implement the Dijkstra solution in Python: parse i
The solution uses a 2N-state graph where each vertex `v` is split into two states:
- `v0` (index `2*(v-1)`): graph is in its original orientation.
- `v1` (index `2*(v-1)+1`): graph has been reversed an odd number of times.

Transitions:
- From `v0`: follow each original outgoing edge `v→u` to `u0` (cost 1), or pay `X` to go to `v1`.
- From `v1`: follow each original incoming edge `u→v` (which becomes outgoing after reversal) to `u1` (cost 1), or pay `X` to go back to `v0`.

Dijkstra's algorithm with a priority queue runs in `O((N+M) log N)` time, which is easily within limits for `N, M ≤ 2×10^5`. All distances are stored as Python integers (unbounded precision), so the answer can exceed 32-bit ranges safely.

The answer is the minimum of distances to `N0` and `N1`.
