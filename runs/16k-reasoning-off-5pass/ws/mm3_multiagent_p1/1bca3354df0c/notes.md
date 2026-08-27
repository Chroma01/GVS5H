
## ideation
**Understanding the problem**

- Initial graph is undirected, simple, bipartite (no odd cycles).
- Players alternately add a non‑existing edge that does **not** create an odd cycle.
- A player unable to move loses.

**Key observation**
In a bipartite graph, vertices can be 2‑colored. An edge that keeps the graph bipartite must connect vertices of the **same color** (a cross‑color edge would either already exist or would create an odd cycle because any path between the two color classes has odd length? Actually, in a connected bipartite graph, **every** edge between opposite sides is allowed; they just may already exist. Adding a new edge between opposite sides would necessarily create an odd cycle because the two vertices already have a path of even length (alternating colors) between them – wait, length of path is odd? In bipartite graph, path length between vertices of opposite colors is odd, so adding an edge between them creates an even cycle. So edges allowed to add are only those **inside the same color class**.)

## worker: Implement the BFS/DFS-based solution that computes
The problem is a known impartial combinatorial game on a bipartite graph. The key insight is that the game decomposes into independent components. For each connected component with bipartition sizes `a` and `b`, the number of available moves (edges that can be added without creating an odd cycle) is the number of missing edges within the same color class: `C(a,2) + C(b,2) - existing_same_color_edges`. The overall Grundy number is the XOR of these values across all components. If the XOR is non-zero, the first player (Aoki) wins; otherwise, the second player (Takahashi) wins. The BFS computes the bipartition sizes and counts the intra-side edges correctly (each counted twice, so divided by 2).
