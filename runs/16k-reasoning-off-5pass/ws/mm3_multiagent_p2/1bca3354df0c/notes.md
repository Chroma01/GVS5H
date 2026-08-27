
## ideation
The given graph $G$ is initially bipartite (no odd cycle). The only allowed move is to add a non-existing edge whose endpoints lie in different parts of the current bipartition. Adding an edge inside one part would create an odd cycle and is forbidden.

Key points:
- Starting bipartition can be obtained by BFS/DFS coloring (2‑coloring).
- The existing edges $M$ are all between the two color classes (say class 0 and class 1).
- Any new edge must also connect a vertex of class 0 with a vertex of class 1.
- The set of allowed pairs never changes: it is exactly the pairs of vertices with different colors that are not already connected.
- The game ends exactly when the graph becomes a complete bipartite graph between the two color classes.
- Total number of possible moves = $|C_0| \times |C_1| - M$ (non-edges between the two parts).
- Moves alternate; first player (Aoki) wins iff the number of moves is odd.

Pitfalls:
- The bipartition is not necessarily unique if the graph is disconnected, but the sizes of the two color classes in a connected component are fixed up to swapping. We can fix an arbitrary component, color it, and sum sizes of color 0 and color 1 across all components.
- $N, M$ up to $2\times10^5$, so counting $|C_0|\times|C_1|$ fits in 64‑bit.
- Need to use 0‑indexed or 1‑indexed consistently.
- Use recursion limit / iterative BFS because $N$ can be $2\times10^5$ (recursion may overflow).

## worker: Implement the solution in Python: parse input, BFS
The graph is initially bipartite (no odd cycle). The only allowed move is to add a non-existing edge whose endpoints lie in different parts of the current bipartition. Adding an edge inside one part would create an odd cycle and is forbidden.

Key observations:
- Starting bipartition can be obtained by BFS/DFS 2‑coloring.
- All existing edges are between the two color classes.
- Any new edge must also connect a vertex of class 0 with a vertex of class 1.
- The set of allowed pairs never changes: it is exactly the pairs of vertices with different colors that are not already connected.
- The game ends exactly when the graph becomes a complete bipartite graph between the two color classes.
- Total number of possible moves = |C0| × |C1| − M.
- Moves alternate; first player (Aoki) wins iff the number of moves is odd.

Implementation details:
- Use iterative BFS with a deque to avoid recursion depth issues for N up to 2×10⁵.
- Count vertices in each color class across all connected components.
- Compute remaining moves and check parity.
