
## ideation
The problem asks us to determine the winner of a game played on a bipartite graph where players add edges such that the graph remains bipartite. The game ends when the graph is a "maximal bipartite graph" (adding any edge would create an odd cycle).

Key insights:
1. A graph has no odd cycles if and only if it is bipartite.
2. The game ends when the graph becomes a maximal bipartite graph. For a connected bipartite component with partition sizes $A$ and $B$, the maximal bipartite graph is the complete bipartite graph $K_{A,B}$, which has $A \times B$ edges.
3. The total number of edges in the final maximal bipartite graph is the sum over all connected components of $A_c \times B_c$.
4. The number of moves in the game is (Total edges in final graph) - (Initial edges M).
5. If the number of moves is odd, the first player (Aoki) wins. If even, the second player (Takahashi) wins.

Algorithm:
1. Read input and build the graph.
2. Find connected components using BFS or DFS.
3. For each connected component, check if it's bipartite (it should be, given the problem statement) and determine the sizes of the two partitions.
4. Compute the total number of edges in the maximal bipartite graph: sum of $A_c \times B_c$ for all components.
5. Calculate the number of moves: total_edges_final - M.
6. If the number of moves is odd, Aoki wins; otherwise, Takahashi wins.

Pitfalls:
- Need to correctly compute bipartition sizes for each connected component.
- The graph may have multiple connected components.
- Ensure that the graph is indeed bipartite (given by problem constraints).

## worker: (None)
The solution leverages the key insight that a graph with no odd cycles is bipartite. The game ends when the graph becomes a maximal bipartite graph. For each connected component with bipartition sizes $A$ and $B$, the maximal bipartite graph is the complete bipartite graph $K_{A,B}$ with $A \times B$ edges. The total number of edges in the final graph is the sum of $A_c \times B_c$ over all connected components. The number of moves is this total minus the initial number of edges $M$. If the number of moves is odd, the first player (Aoki) wins; otherwise, the second player (Takahashi) wins.

The algorithm:
1. Reads the input and builds an adjacency list.
2. Uses BFS to find connected components and compute bipartition sizes for each component.
3. Computes the total maximum edges possible in the final maximal bipartite graph.
4. Determines the winner based on the parity of the number of moves.

Time complexity: $O(N + M)$ for BFS and processing.
Space complexity: $O(N + M)$ for the adjacency list and auxiliary arrays.
