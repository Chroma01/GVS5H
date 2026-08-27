
## ideation
The core difficulty lies in recognizing that the game is equivalent to filling a bipartite graph. Since the initial graph is bipartite (no odd cycles), any valid move must connect two vertices from different partitions of the same connected component. Adding an edge within the same partition would create an odd cycle, which is forbidden. The game ends when each connected component becomes a complete bipartite graph. The total number of moves possible is the sum over all connected components of (|A| * |B| - existing_edges_in_component), where |A| and |B| are the sizes of the two partitions. The winner is determined by the parity of this total: if odd, the first player (Aoki) wins; if even, the second player (Takahashi) wins.

Key steps:
1. Use BFS/DFS to find connected components and determine the bipartite partitions for each component.
2. For each component, calculate the maximum number of edges possible in a complete bipartite graph with partition sizes |A| and |B|, which is |A| * |B|.
3. Subtract the number of existing edges in the component to get the number of available moves for that component.
4. Sum the available moves across all components.
5. If the total is odd, Aoki wins; otherwise, Takahashi wins.

Pitfalls:
- Incorrectly counting edges: need to ensure we only count edges within each component.
- Large N and M: need efficient graph traversal (BFS/DFS) and careful handling of large numbers (though parity check avoids overflow issues).
- Ensuring the graph is properly bipartitioned: use BFS with coloring to verify and compute partition sizes.

## worker: <none>
The problem is a game on a bipartite graph where players add edges without creating odd cycles. Since the initial graph is bipartite (no odd cycles), valid moves are only between vertices in different partitions of the same connected component. The game ends when each connected component becomes a complete bipartite graph.

The total number of moves possible is:
- For each connected component with partition sizes |A| and |B|, the maximum edges in a complete bipartite graph is |A| * |B|.
- Subtract the number of existing edges in that component.
- Sum over all components.

The winner is determined by the parity of the total moves: odd means first player (Aoki) wins, even means second player (Takahashi) wins.

We use BFS to find connected components and compute bipartite partitions. Then we count edges per component and compute the total available moves.
