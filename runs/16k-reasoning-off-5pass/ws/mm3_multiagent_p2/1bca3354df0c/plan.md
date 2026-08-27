The graph is bipartite (no odd cycle initially). Adding edges that keep it bipartite means we can only add edges between vertices in opposite sides of the current bipartition. The key observation: in a bipartite graph, the available moves are exactly the non-edges crossing the two parts. Adding an edge between two vertices in the same part would create an odd cycle, which is forbidden. The game ends when the graph becomes a complete bipartite graph.

So we just need to count the number of valid moves: (size of part A) * (size of part B) - M, and the players alternate adding these edges. The first player wins iff this count is odd.

We must be careful: as edges are added, the bipartition may change? Actually, no. Starting from a bipartite graph, adding any edge between the two parts keeps it bipartite, and the existing partition remains valid (each new edge connects opposite sides). So the set of allowed moves only shrinks, and total moves equals the count of cross-pairs minus existing edges.

Thus the winner is determined by parity of (count_cross - M).