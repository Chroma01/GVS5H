
## ideation
The problem describes a game played on a bipartite graph where players add edges without creating odd cycles. This implies the graph remains bipartite throughout the game.
The core difficulty is determining the winner based on the initial configuration.
Key observations:
1.  **Bipartite Property**: Since no odd cycles are allowed, the graph is always bipartite.
2.  **Game Termination**: The game ends when no more edges can be added. An edge $(u, v)$ can be added if $u$ and $v$ are in different connected components OR if they are in the same component but belong to different partitions (colors).
3.  **Final State**: The game continues as long as there are edges that can be added. Can the game end with multiple connected components?
    *   If there are two components $C_1$ and $C_2$, can we always add an edge between them?
    *   Let $C_1$ have partitions $(A_1, B_1)$ and $C_2$ have $(A_2, B_2)$.
    *   We can add an edge between $u \in A_1$ and $v \in A_2$ (or $B_1, B_2$). This merges the components.
    *   The only way we *cannot* add an edge between two components is if one of them is empty, which is impossible.
    *   Therefore, players can always choose to merge components until the graph becomes a single connected component.
    *   Once the graph is a single connected bipartite graph, can we still add edges? Yes, unless it is a complete bipartite graph.
    *   Since players play optimally to win, and the game is finite, we need to know if the total number of moves is fixed.
4.  **Fixed Number of Moves**:
    *   The maximum number of edges in a bipartite graph with $N$ vertices is $\lfloor N^2/4 \rfloor$ (Turán's theorem for bipartite graphs, achieved by $K_{\lfloor N/2 \rfloor, \lceil N/2 \rceil}$).
    *   Does the game *force* the graph to become a single complete bipartite component?
    *   Suppose the current state is a union of complete bipartite components. A player *must* merge two components to make a move. Merging two complete bipartite components results in a larger bipartite component which is *not* necessarily complete (unless the sizes align perfectly to form a complete bipartite graph immediately, but generally it creates "missing edges" between the new partitions).
    *   Actually, consider the potential function $P = \lfloor N^2/4 \rfloor - (\text{current edges})$.
    *   Every move adds 1 edge.
    *   Is it possible to reach a state where the graph is not a single component but no moves are possible? No, because we can always merge components.
    *   Is it possible to reach a state where the graph is a single component but not complete bipartite, and no moves are possible? No, because if it's not complete bipartite, there exist non-adjacent vertices in different partitions that can be connected.
    *   Therefore, the game *must* end when the graph is a single connected component that is a complete bipartite graph.
    *   The number of edges in this final state is exactly $\lfloor N^2/4 \rfloor$.
    *   Since the initial number of edges is $M$, and each move adds exactly 1 edge, the total number of moves in the game is exactly $\lfloor N^2/4 \rfloor - M$.
    *   This number is independent of the players' choices.
5.  **Winning Condition**:
    *   If the total number of moves $K = \lfloor N^2/4 \rfloor - M$ is odd, the first player (Aoki) makes the 1st, 3rd, ..., last move. Aoki wins.
    *   If $K$ is even, the second player (Takahashi) makes the last move. Takahashi wins.

Pitfalls:
*   Assuming the game could end with multiple components. (Proven impossible as components can always be merged).
*   Assuming the final component size isn't fixed. (The max edges for $N$ vertices in a bipartite graph is unique).
*   Implementation details: Calculating $\lfloor N^2/4 \rfloor$ correctly for large $N$ (use integer division).

Next:
*   Read $N$ and $M$.
*   Read the $M$ edges (we don't actually need to process the edges to determine the parity, just $M$).
*   Calculate $K = (N * N) // 4 - M$.
*   Check parity of $K$.
*   Print "Aoki" if odd, "Takahashi" if even.

## worker: Implement the solution in Python: read N and M, ca
The problem asks for the winner of a game played on a bipartite graph where players add edges without creating odd cycles.
1.  **Game Structure**: The graph remains bipartite throughout the game.
2.  **Termination**: The game ends when no more edges can be added. A move is possible if we can connect two vertices $u, v$ such that they are in different partitions (colors) of the bipartite graph.
3.  **Merging Components**: If the graph has multiple connected components, say $C_1$ and $C_2$, we can always add an edge between a vertex in $C_1$ and a vertex in $C_2$ (specifically, choosing vertices from the same partition set in their respective components) to merge them into a larger bipartite component. Thus, the game cannot end with multiple components unless no such merge is possible, but since we can always merge, the game proceeds until there is only one connected component.
4.  **Final State**: The game ends when the single connected component is a complete bipartite graph. The maximum number of edges in a bipartite graph with $N$ vertices is $\lfloor N^2/4 \rfloor$.
5.  **Total Moves**: Since the initial number of edges is $M$ and the final number of edges is $\lfloor N^2/4 \rfloor$, and each move adds exactly 1 edge, the total number of moves in the game is exactly $\lfloor N^2/4 \rfloor - M$.
6.  **Winning Condition**: This is a game of fixed length. If the total number of moves is odd, the first player (Aoki) makes the last move and wins. If even, the second player (Takahashi) makes the last move and wins.

The solution simply calculates this difference and checks its parity. The specific edges and graph structure do not affect the winner, only $N$ and $M$ matter.
