
## ideation
The problem is a classic state-expanded shortest path: the "reverse all edges" operation is global, so the only extra state needed is a parity bit (0 = original orientation, 1 = reversed). From (v, p), moving costs 1 along edges in the current orientation (out-edges if p=0, in-edges if p=1), and flipping costs X while staying at v. Dijkstra over 2N states with both adjacency lists gives O((N+M) log N), well within limits (N, M ≤ 2e5). Answer is min(dist[N][0], dist[N][1]).

Core difficulties / pitfalls:
- Must build both forward and reverse adjacency lists (memory 2M entries, fine).
- Edge weights differ (1 vs X), so BFS alone is insufficient unless using 0-1 BFS tricks — but X can be huge, so Dijkstra is the safe general choice.
- Answer can exceed 32-bit (sample 3: ~4.3e9), so use 64-bit / Python ints.
- Guarantee of reachability means we don't need to handle unreachable cases, but min over both parities at N is still required.
- Standard Dijkstra with lazy deletion (skip stale heap entries) is simplest and fast enough.

## worker: Implement the complete solution: read N, M, X and 
- Built a state-expanded graph with 2N states: (vertex, parity), where parity 0 = original edge orientation, 1 = reversed.
- Transitions: from (v, p), move along out-edges (p=0) or in-edges (p=1) with cost 1; flip parity at same vertex with cost X.
- Ran Dijkstra with lazy deletion from (1, 0). Answer is min(dist[0][N], dist[1][N]).
- Complexity: O((N + M) log N) time, O(N + M) memory. Python ints handle answers beyond 32-bit (e.g., sample 3).
- Verified logic against samples: sample 1 → 4 (direct path 1→2→4→3→5), sample 2 → 3 (move, flip, move), sample 3 → 4294967299 (7 flips of 613566756 + 7 moves = 7*613566756 + 7 = 4294967299).
