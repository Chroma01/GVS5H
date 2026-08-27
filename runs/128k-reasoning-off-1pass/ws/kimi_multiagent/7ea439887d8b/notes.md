
## ideation
The core difficulty is that the "reverse all edges" operation is a global state change, not a local move. The natural way to handle this is to expand the state space: the state is (current vertex, parity of number of reversals so far). Orientation 0 = edges as given; orientation 1 = all edges reversed. Transitions:
- Move along an edge: in orientation 0, follow original adjacency; in orientation 1, follow reversed adjacency. Cost 1, orientation unchanged.
- Reverse: stay at same vertex, flip orientation, cost X.

This gives 2N states and 2M + 2N edges, all weights non-negative (1 and X), so Dijkstra from (1, 0) works. Answer = min(dist[N][0], dist[N][1]).

Pitfalls:
- Costs can be huge: up to ~2e5 moves plus reversals at 1e9 each; sample 3 answer is ~4.3e9 > 2^32, so use 64-bit (Python ints are fine natively).
- N, M up to 2e5, so need efficient I/O and adjacency lists; a naive O((N+M)^2) approach fails.
- Don't mistakenly allow reversing to be "free" or model it per-edge; it's a global flip.
- Guarantee of reachability means we don't need to handle unreachable cases, but min over both orientations at N is still required.
- Dijkstra with a binary heap is O((N+M) log N), fine. Alternatively 0-1 BFS doesn't directly apply since X can be > 1, so Dijkstra (or dial/bucket) is the safe choice.

## worker: Implement the full Python solution: fast input par
- State = (vertex, orientation parity). Orientation 0: edges as given; orientation 1: all edges reversed.
- Transitions: move along an edge (cost 1, same orientation, using `adj` or `radj` depending on orientation); flip (cost X, same vertex, orientation toggled).
- Dijkstra over 2N states with 2M + 2N implicit edges: O((N + M) log N), well within limits for N, M ≤ 2×10^5.
- Python ints handle answers exceeding 2^32 (e.g., sample 3's 4294967299) natively.
- Answer is min(dist[0][N], dist[1][N]) since we may arrive at N in either orientation.
- Fast input via reading all of stdin at once; adjacency lists built for both directions.
