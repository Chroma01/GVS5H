
## ideation
The core difficulty lies in recognizing that the game is equivalent to filling a bipartite graph to its maximal state (a complete bipartite graph on each connected component's partition).
1.  **Bipartite Property**: The condition "adding an edge does not create an odd cycle" is equivalent to maintaining the bipartite property. A graph has no odd cycles if and only if it is bipartite.
2.  **Maximal Bipartite Graph**: For a connected bipartite component with partition sets of size $A$ and $B$, the maximum number of edges is $A \times B$. Any edge within a partition set would create an odd cycle (specifically, a cycle of length 3 if connected directly, or generally an odd cycle). Any edge between the two sets is allowed.
3.  **Game Length**: The game ends when every possible edge between the two partitions of each connected component has been added. The total number of moves possible is the sum over all components of $(A_k \times B_k)$ minus the initial number of edges $M$.
4.  **Winning Condition**: This is a normal play game. The total number of moves is fixed regardless of the order in which edges are added (as long as they are valid). Therefore, the winner is determined solely by the parity of the total number of moves. If the total moves is odd, the first player (Aoki) makes the last move and wins. If even, the second player (Takahashi) wins.
5.  **Algorithm**:
    -   Read input.
    -   Build adjacency list.
    -   Use BFS or DFS to find connected components and perform bipartite coloring (2-coloring).
    -   For each component, count the number of nodes in color 0 ($A_k$) and color 1 ($B_k$).
    -   Calculate `total_max_edges = sum(A_k * B_k for all components)`.
    -   Calculate `moves = total_max_edges - M`.
    -   If `moves % 2 == 1`, Aoki wins. Else, Takahashi wins.

Pitfalls to avoid:
-   Incorrectly handling disconnected components.
-   Forgetting to subtract the initial edges $M$.
-   Integer overflow for $N \times N$? $N \le 2 \cdot 10^5$, so $A_k B_k$ can be up to $\approx 10^{10}$, which fits in a 64-bit integer. Python handles large integers automatically.
-   Stack overflow with DFS for deep graphs? BFS is safer for large $N$.

## worker: Implement the solution based on the ideation.
The problem describes a game played on a graph where players add edges as long as the graph remains bipartite (no odd cycles). This is equivalent to filling a bipartite graph to its maximal state.
1.  **Bipartite Components**: The graph is initially bipartite. Each connected component is a bipartite graph with two partition sets. Let the sizes of these sets for component $k$ be $A_k$ and $B_k$.
2.  **Maximal Edges**: In a bipartite component with partitions $A_k$ and $B_k$, the maximum number of edges is $A_k \times B_k$. This is achieved when every node in $A_k$ is connected to every node in $B_k$.
3.  **Total Moves**: The game ends when all possible edges between the partitions of each component have been added. The total number of moves possible is the sum of $(A_k \times B_k)$ for all components minus the initial number of edges $M$.
4.  **Parity Argument**: Since the total number of moves is fixed regardless of the order of play (any valid move reduces the number of available moves by exactly 1, and the game must end at the maximal bipartite graph), the winner is determined by the parity of the total number of moves.
    -   If total moves is odd, the first player (Aoki) makes the 1st, 3rd, ..., last move and wins.
    -   If total moves is even, the second player (Takahashi) makes the last move and wins.
5.  **Implementation**: We use BFS to traverse each connected component, count the nodes in each partition (using 2-coloring), and accumulate the product of partition sizes. Finally, we subtract $M$ and check the parity.
