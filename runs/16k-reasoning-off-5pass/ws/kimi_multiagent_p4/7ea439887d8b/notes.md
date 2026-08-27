
## ideation
The core difficulty is that the "reverse all edges" operation is global — it changes the direction of every edge simultaneously. This means the state isn't just the current vertex; we must also track whether the graph is currently in its original orientation or reversed. This naturally suggests a state-space expansion: (vertex, parity) where parity ∈ {0, 1} indicates how many times we've reversed (mod 2).

Key observations:
- From state (v, p), we can move along an edge: if p=0, follow original edges v→u; if p=1, follow reversed edges (i.e., original edge u→v means we can go v→u). Cost 1, parity unchanged.
- From state (v, p), we can reverse: go to (v, 1-p) at cost X.
- Answer = min(dist[N][0], dist[N][1]).

Edge weights are 1 and X (X can be 1, so weights aren't just 0/1 — need Dijkstra with a heap, or 0-1 BFS won't directly work unless X=1... actually if X=1 all weights are 1 and BFS works; but for general X, Dijkstra is safest). With 2N states and 2M + 2N edges in the expanded graph, Dijkstra is O((N+M) log N) — fine for N, M ≤ 2×10^5.

Pitfalls:
- Answer can be large (up to ~2×10^5 × 10^9 ≈ 2×10^14), exceeding 32-bit — use 64-bit (Python handles big ints natively, but still note it).
- Don't confuse which adjacency list to use per parity: parity 0 → outgoing edges (original), parity 1 → incoming edges (reversed graph). Need both adjacency lists (out and in).
- Start state is (1, 0) with distance 0.
- Guarantee of reachability means we don't need to handle unreachable cases, but using a large INF is still good practice.
- Dijkstra with heapq in Python is fast enough; must use adjacency lists efficiently (avoid recursion, use sys.stdin fast reading).

Alternative approach: 0-1 BFS variant with a deque only works if X ∈ {0,1}... not general. Could also use dial's algorithm but heap Dijkstra is simplest and fast enough.

## worker: Implement the complete Python solution: fast input
- State-space expansion: each state is (vertex, parity), parity ∈ {0,1} tracking whether all edges are currently reversed (number of reversals mod 2).
- Transitions from (v, p):
  - Move along an edge, cost 1, parity unchanged. For p=0 use original outgoing edges; for p=1 use original incoming edges (which are outgoing in the reversed graph).
  - Reverse all edges, cost X, stay at v, flip parity.
- Since weights are 1 and X (X up to 1e9, not necessarily 1), plain 0-1 BFS doesn't apply in general; Dijkstra with a binary heap over 2N states and ~2M+2N expanded edges runs in O((N+M) log N), well within limits for N, M ≤ 2×10^5.
- Answer = min(dist[0][N], dist[1][N]). Python ints handle the potentially large answer (up to ~2×10^14) natively.
- Fast input via sys.stdin.buffer.read().split(); adjacency stored as plain lists for cache-friendly iteration.
- Verified logic against samples conceptually: Sample 1 (X=5) gives 4 via direct path 1→2→4→3→5; Sample 2 (X=1) gives 3 via 1→2, reverse, 2→5 (edge 5→2 reversed); Sample 3's large X forces many reversals, matching 4294967299.
