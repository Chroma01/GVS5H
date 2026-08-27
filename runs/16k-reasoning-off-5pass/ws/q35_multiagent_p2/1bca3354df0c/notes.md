
## ideation
The problem describes a game played on a bipartite graph where players add edges between vertices in different partitions of the same connected component, provided the edge doesn't already exist. Since adding an edge within the same partition creates an odd cycle (forbidden), the game is equivalent to filling in all missing edges between the two sets of each connected component's bipartition.

Key insights:
1. The initial graph is bipartite (no odd cycles).
2. Each connected component can be split into two sets, say $A_i$ and $B_i$.
3. A valid move is to add an edge between a vertex in $A_i$ and a vertex in $B_i$ that isn't already present.
4. The game ends when every possible edge between $A_i$ and $B_i$ exists for all components $i$. This is because no more edges can be added without creating an odd cycle or duplicating an edge.
5. The total number of moves possible in the entire game is fixed: it's the sum over all components of $(|A_i| \times |B_i|)$ minus the initial number of edges $M$.
6. This is a normal play game with a fixed total number of moves. The first player (Aoki) wins if the total number of moves is odd, and the second player (Takahashi) wins if it is even.

Algorithm:
1. Build the graph from input.
2. Use BFS/DFS to find connected components and determine the bipartition sizes ($|A_i|, |B_i|$) for each component.
3. Calculate total possible edges: $\sum (|A_i| \times |B_i|)$.
4. Total moves = total possible edges - M.
5. If total moves is odd, Aoki wins; else Takahashi wins.

Pitfalls:
- Need to handle disconnected components correctly.
- Ensure bipartition is done correctly using BFS/DFS with two-coloring.
- Large N and M require efficient graph traversal (BFS/DFS with adjacency list).

## worker: (omit)
The problem is a combinatorial game on a bipartite graph. Since the initial graph has no odd cycles, it is bipartite. The constraint that adding an edge must not create an odd cycle means we can only add edges between vertices in different partitions of the same connected component. The game ends when the graph becomes a disjoint union of complete bipartite graphs (one for each connected component).

The total number of edges in the final state for a connected component with partition sizes $A$ and $B$ is $A \times B$. The number of moves possible in the entire game is the sum of $(A_i \times B_i)$ for all components $i$, minus the initial number of edges $M$.

Since this is a normal play game with a fixed total number of moves (no branching choices affect the total count of moves available, only their order), the winner is determined solely by the parity of the total number of moves. If the total number of moves is odd, the first player (Aoki) wins. If even, the second player (Takahashi) wins.

We use DFS to find connected components and compute the bipartition sizes. The time complexity is $O(N + M)$ which is efficient for the given constraints.
