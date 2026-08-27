
## ideation
**Core difficulty**: We have a dynamic operation: reversing all edges costs X. The graph orientation changes globally, not per edge. This is reminiscent of problems with a "toggle" operation, often modeled by having two states: the original orientation and the reversed orientation.

**State modeling**:
- Create a graph with 2N states: (v, 0) representing "currently at vertex v in original orientation", and (v, 1) representing "currently at vertex v in reversed orientation".
- Transitions:
  - Move along an edge: from (v, 0) we can go to (u, 1) for each original edge v→u, because after moving (cost 1) we haven't changed orientation, but we need to track orientation parity for future moves. Wait, careful: The operation "move" is a physical move; orientation doesn't change by moving. So if we are in state (v, 0) (original orientation), we can move to (u, 0) if there is an original edge v→u. Similarly, from (v, 1) we move to (u, 1) if there is a reversed edge, i.e., original edge u→v.
  - Reverse: from (v, 0) to (v, 1) with cost X, and from (v, 1) to (v, 0) with cost X.
- So edges:
  - Original edges: (v, 0) → (u, 0) cost 1 for each original v→u.
  - Original edges (reversed): (v, 1) → (u, 1) cost 1 for each original u→v (i.e., reverse direction).
  - Toggle: (v, 0) → (v, 1) cost X, (v, 1) → (v, 0) cost X.

**Goal**: Minimum cost from (1, 0) to (N, 0) or (N, 1)? Actually we need to reach vertex N regardless of orientation. So answer is min(dist[(N, 0)], dist[(N, 1)]).

## worker: Implement the solution in Python: read N, M, X, bu
- Modeled the problem as a shortest path on 2N states: (vertex, parity) where parity 0 means the graph is in its original orientation and parity 1 means it has been reversed an odd number of times.
- Transitions: moving along an edge costs 1 and keeps the same parity, but the adjacency depends on the parity (original vs reversed). Reversing the whole graph costs X and flips the parity, staying at the same vertex.
- Used Dijkstra's algorithm with a priority queue since edge weights are 1 or X (non-negative). The number of states and edges is O(N + M), well within limits.
- The answer is the minimum distance to reach vertex N in either parity.
