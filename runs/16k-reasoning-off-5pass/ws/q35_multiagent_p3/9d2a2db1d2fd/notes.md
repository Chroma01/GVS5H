
## ideation
The core difficulty lies in efficiently answering $2 \times 10^5$ queries on a $500 \times 500$ grid. A direct simulation or Dijkstra per query is too slow due to the large state space (floors up to $10^6$).

The key insight is to decompose the problem:
1.  **Horizontal Movement**: Moving between adjacent blocks at the same floor $h$ is free (0 stairs) if both buildings have height $\ge h$. This implies that for a fixed floor $h$, all blocks with height $\ge h$ that are connected form a component where movement is free.
2.  **Vertical Movement**: Changing floors within a building costs 1 stair per floor.
3.  **Optimization**: To go from $(A, B, Y)$ to $(C, D, Z)$, we can change floors in the starting building to some height $h$, travel via walkways to the destination building (staying at height $h$), and then change floors to $Z$. The cost is $|Y - h| + |Z - h|$.
4.  **Constraint**: We can only use height $h$ for the walkway path if there exists a path of blocks from $(A, B)$ to $(C, D)$ such that every block on the path has height $\ge h$.
5.  **Bottleneck Path**: We want to maximize the "bottleneck" height $H_{max}$ of the path from $(A, B)$ to $(C, D)$. $H_{max}$ is the maximum value $h$ such that a path exists where all blocks have height $\ge h$. This is equivalent to finding the path that maximizes the minimum edge weight, where the weight of an edge between adjacent blocks $(i,j)$ and $(i',j')$ is $\min(F_{i,j}, F_{i',j'})$.
6.  **Cost Calculation**:
    -   If $H_{max} \ge \min(Y, Z)$, we can choose an intermediate height $h$ between $Y$ and $Z$ (specifically, any $h \in [\min(Y,Z), \max(Y,Z)]$ that is $\le H_{max}$ works, and since $H_{max} \ge \min(Y,Z)$, we can always pick $h$ in the interval $[Y, Z]$ or $[Z, Y]$). The cost is simply $|Y - Z|$.
    -   If $H_{max} < \min(Y, Z)$, the best we can do is use the highest possible height $H_{max}$. The cost is $(Y - H_{max}) + (Z - H_{max}) = Y + Z - 2 H_{max}$.

Thus, the problem reduces to:
1.  Construct a Maximum Spanning Tree (MST) of the grid graph where edge weights are $\min(F_{u}, F_{v})$.
2.  For each query, find the minimum edge weight on the unique path between $(A, B)$ and $(C, D)$ in the MST. This value is $H_{max}$.
3.  Compute the answer using the formula derived above.

We can use LCA with binary lifting to answer the "min edge on path" queries in $O(\log(HW))$ time after $O(HW \log(HW))$ preprocessing.

Pitfalls:
-   The grid is large ($500 \times 500 = 250,000$ nodes), so $O(HW \log(HW))$ is acceptable.
-   Edge weights are $\min(F_{i,j}, F_{i',j'})$.
-   Need to handle 1-based indexing carefully.
-   The case where start and end are the same block is excluded by constraints, but if $A_i=C_i$ and $B_i=D_i$, the path is just vertical, cost $|Y-Z|$. The bottleneck logic still holds (path of length 0, bottleneck is effectively infinity or the building's own height, but since we don't move horizontally, we just go $Y \to Z$). However, the problem states $(A_i,B_i,Y_i) \neq (C_i,D_i,Z_i)$, so start and end positions might be same block but different floors. In that case, $H_{max}$ is effectively $\infty$ (or at least $\max(Y,Z)$), so cost is $|Y-Z|$. The MST path between a node and itself has no edges, so we need to handle this or ensure the logic holds. Actually, if start==end, we don't need walkways. The formula $|Y-Z|$ works. If we use LCA, the path length is 0, min edge is undefined. We should handle start==end separately or define min edge on empty path as $\infty$.

Implementation details:
-   Flatten 2D grid to 1D index: $idx = (i-1)*W + (j-1)$.
-   Kruskal's algorithm for MST: Sort all edges by weight descending. Use Union-Find.
-   Build adjacency list for the MST.
-   Preprocess LCA: `up[u][k]` is $2^k$-th ancestor, `min_edge[u][k]` is min edge weight on path to that ancestor.
-   For each query, if $u=v$, answer $|Y-Z|$. Else, find LCA, compute min edge on path $u \to lca$ and $v \to lca$, take minimum of these two values as $H_{max}$.
-   Apply formula.

## worker: Implement Union-Find data structure.
1.  **Problem Decomposition**: The problem was reduced to finding the "bottleneck capacity" $H_{max}$ between two blocks, which is the maximum height $h$ such that a path exists where all blocks have height $\ge h$. This is a classic "bottleneck path" problem.
2.  **Maximum Spanning Tree (MST)**: The bottleneck capacity between any two nodes in a graph is equal to the minimum edge weight on the unique path between them in the Maximum Spanning Tree. We constructed the MST using Kruskal's algorithm with edges sorted by weight descending. Edge weights were defined as $\min(F_{u}, F_{v})$.
3.  **LCA with Binary Lifting**: To answer queries efficiently, we preprocessed the MST using binary lifting. For each node, we stored its $2^k$-th ancestor and the minimum edge weight on the path to that ancestor. This allows us to find the minimum edge weight on the path between any two nodes in $O(\log(HW))$ time.
4.  **Cost Calculation**:
    -   If $H_{max} \ge \min(Y, Z)$, the optimal intermediate floor can be chosen between $Y$ and $Z$, resulting in a cost of $|Y - Z|$.
    -   If $H_{max} < \min(Y, Z)$, the best intermediate floor is $H_{max}$, resulting in a cost of $Y + Z - 2 H_{max}$.
5.  **Edge Cases**:
    -   If start and end blocks are the same, the cost is simply $|Y - Z|$ as no walkways are needed.
    -   The grid size is up to $500 \times 500 = 250,000$ nodes, and $Q$ is up to $200,000$. The $O(HW \log(HW))$ preprocessing and $O(Q \log(HW))$ query time fit within the limits.
    -   Recursion limit was increased to handle deep trees in DFS/BFS if necessary, though an iterative BFS was used for depth calculation.
