
## ideation
The problem describes an impartial game played on a bipartite graph (since no odd cycles exist initially). The key insight is that adding an edge $(i, j)$ is valid if and only if it does not create an odd cycle. In a bipartite graph, an odd cycle is created if and only if we add an edge between two vertices that are in the *same* partition set of the bipartition. Therefore, valid moves are exactly those that add an edge between two vertices in *different* partition sets of the connected component's bipartition.

For each connected component $C$, let the two parts of the bipartition have sizes $A_C$ and $B_C$. The total number of possible edges between the two parts is $A_C \times B_C$. The number of existing edges in the component is $M_C$ (all of which are between the two parts, since the graph is bipartite). Thus, the number of available moves (non-existing edges between the two parts) in component $C$ is $A_C \times B_C - M_C$.

The game is equivalent to a single pile of size equal to the sum of available moves across all connected components. Since each move reduces the total number of available edges by exactly 1, and the set of valid moves is fixed (adding an edge doesn't change the bipartition or the validity of other edges), the total number of moves in the game is fixed. The first player (Aoki) wins if the total number of moves is odd, and the second player (Takahashi) wins if it is even.

The algorithm is:
1. Find connected components and their bipartitions using BFS/DFS.
2. For each component, compute the sizes of the two parts ($A_C, B_C$) and the number of edges $M_C$.
3. Compute total moves = $\sum (A_C \times B_C - M_C)$.
4. If total moves is odd, Aoki wins; otherwise, Takahashi wins.

Pitfalls:
- Ensure the graph is processed correctly for multiple connected components.
- The bipartition is unique up to swapping the two sets, so the product $A_C \times B_C$ is invariant.
- The number of edges $M_C$ is simply the count of edges in the component.

## worker: <none>
The problem is an impartial game on a bipartite graph. Since the graph has no odd cycles initially, it is bipartite. Adding an edge $(i, j)$ is valid if and only if it doesn't create an odd cycle, which means $i$ and $j$ must be in different partition sets of their connected component's bipartition.

For each connected component with bipartition sizes $A$ and $B$, the maximum number of edges possible between the two sets is $A \times B$. The number of existing edges in the component is $M_C$. The number of available moves (non-existing edges between the two sets) is $A \times B - M_C$.

The total number of moves in the game is the sum of available moves across all connected components. Since each move reduces the total available moves by exactly 1, and the set of valid moves is fixed (adding an edge doesn't change the bipartition or the validity of other edges), the game length is fixed. The first player (Aoki) wins if the total number of moves is odd, and the second player (Takahashi) wins if it is even.

The algorithm:
1. Find connected components and their bipartitions using BFS.
2. For each component, compute the sizes of the two parts ($A_C, B_C$) and the number of edges $M_C$.
3. Compute total moves = $\sum (A_C \times B_C - M_C)$.
4. If total moves is odd, Aoki wins; otherwise, Takahashi wins.

Time complexity: $O(N + M)$ for BFS and edge counting.
Space complexity: $O(N + M)$ for adjacency list and other data structures.
