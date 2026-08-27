
## ideation
The core insight is that the "reverse all edges" operation is global, so the state must include the current orientation of the graph (original or reversed). This creates a state space of 2N vertices: (v, 0) for normal orientation and (v, 1) for reversed orientation. From (v, 0), we can move along original outgoing edges (cost 1) or flip to (v, 1) (cost X). From (v, 1), we move along reversed edges (i.e., original incoming edges) or flip back to (v, 0). Since all costs are non-negative, Dijkstra's algorithm works. The answer is min(dist[N][0], dist[N][1]) because we can stop at N regardless of orientation.

Key pitfalls:
- Need both forward and reverse adjacency lists (2M storage total).
- Must use 64-bit integers (Python handles this naturally).
- The graph may have multiple edges or self-loops; Dijkstra handles these fine.
- Guarantee of reachability ensures we don't need to handle infinity output.

## worker: Implement the complete Python solution: parse inpu
- Built a 2-layer state graph: state (v, o) where o=0 means edges are in original orientation, o=1 means all edges reversed.
- Transitions: move along an edge valid in the current orientation (cost 1), or flip orientation at the same vertex (cost X).
- Ran Dijkstra from (1, 0) since all edge weights are non-negative. Used both forward and reverse adjacency lists so each orientation's moves are O(degree).
- Answer is min(dist[0][N], dist[1][N]) since we may arrive at N in either orientation.
- Python ints are unbounded, so large answers (like sample 3) are handled automatically.
- Complexity: O((N + M) log N) time, O(N + M) memory.
