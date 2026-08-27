
## ideation
**Core difficulty:** Determine the winner of a combinatorial game on a bipartite graph where players add missing cross-edges between the two color classes, and the graph initially has no odd cycles.

**Key insight:** Because the initial graph is bipartite, we can 2-color each connected component uniquely (up to swapping colors). Adding any edge between vertices of different colors preserves bipartiteness, so the only constraint is that the edge must not already exist. Thus a move is equivalent to removing a missing edge from the complete bipartite graph $K_{A,B}$ for that component (where $A$ and $B$ are the sizes of the two color classes). Once a component becomes $K_{A,B}$, no further moves are possible there.

**Impartial game decomposition:** The game splits into independent subgames on each connected component. For a component with $A$ vertices in one color class and $B$ in the other, the number of possible moves (i.e., missing cross-edges) is $A \times B - E_{\text{component}}$. Each move reduces this count by exactly one, and any move is legal. This is precisely a Nim heap of size equal to the number of missing edges. The overall winner is determined by the XOR (nim-sum) of all heap sizes; Aoki (first player) wins iff the XOR is non-zero.

**Pitfalls / checks:**
- Need to handle isolated vertices (size 1 components) correctly: $A=1, B=0$ gives $A \times B = 0$, heap size 0.
- Graph is initially bipartite; must verify this or use it directly.
- Constraints are up to $2\times10^5$, so we need $O(N+M)$ or $O((N+M)\alpha)$ time.
- Use DSU/Union-Find to find components and compute sizes, or DFS.

## worker: Implement the solution: read N, M, build graph; us
- Built adjacency list for an undirected graph with N vertices and M edges.
- For each connected component, performed BFS to 2-color it (possible because the graph is given to be bipartite). Counted vertices in each color class (A, B) and the number of edges in the component.
- The number of moves available in a component is the number of missing cross-edges: `A * B - e`. Each move adds one such edge, reducing the missing count by 1; any missing cross-edge is legal because it keeps the graph bipartite.
- The game splits into independent impartial subgames (one Nim heap per component) of size equal to the missing edge count. The XOR of these heap sizes determines the winner: Aoki (first player) wins iff the XOR is non-zero.
- Edge counting: each edge is encountered twice during BFS (from both endpoints), so divide by 2.
- Complexity: O(N + M) time and O(N + M) memory, suitable for N, M up to 2×10⁵.
