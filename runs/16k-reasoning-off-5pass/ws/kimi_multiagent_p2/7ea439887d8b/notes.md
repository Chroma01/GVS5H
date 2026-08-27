
## ideation
The core difficulty is that the graph's orientation is a global state that can be toggled at cost X, so plain BFS/Dijkstra on vertices is insufficient. The natural fix is a state-space expansion: each state is (vertex, parity), where parity indicates whether edges are currently reversed. Moves along edges cost 1 (using forward adjacency in parity 0, reverse adjacency in parity 1), and toggling costs X while staying at the same vertex. Since edge weights are 1 and X (X up to 1e9, not 0/1 in general), we need Dijkstra with a binary heap rather than 0-1 BFS. The graph has up to 2e5 vertices/edges, so 2N states and 2M directed arcs are fine. Distances can exceed 32-bit (sample 3 answer ~4.3e9), so use 64-bit integers (Python ints are fine). The answer is min(dist[N][0], dist[N][1]). Guarantee of reachability means we don't need to handle unreachable cases, though min() over the two parities handles it anyway.

Pitfalls:
- Building both adjacency lists (original and reversed) — memory 2*(M) ints, fine.
- Using 0-1 BFS incorrectly when X > 1 — must use heapq Dijkstra.
- Answer may exceed 2^31 — Python handles big ints natively.
- 1-indexed vertices; allocate arrays of size N+1.
- Efficiency: use sys.stdin.buffer.read and fast parsing.

## worker: Implement the full solution: parse input with fast
- State space: (vertex, parity) with parity 0 = original orientation, 1 = reversed. This fully captures the global flip state since flipping affects all edges simultaneously.
- Transitions: move along an edge in the current orientation (cost 1, using `adj` for parity 0 and `radj` for parity 1), or flip all edges (cost X, same vertex, parity toggles).
- Dijkstra with a binary heap is used because edge weights are 1 and X (X up to 1e9), so 0-1 BFS is not applicable in general.
- Complexity: O((N + M) log N) time, O(N + M) memory — well within limits for N, M ≤ 2e5.
- Python's arbitrary-precision integers handle answers exceeding 32 bits (e.g., sample 3's ~4.3e9).
- Answer is min(dist[0][N], dist[1][N]); reachability is guaranteed by the problem statement.
