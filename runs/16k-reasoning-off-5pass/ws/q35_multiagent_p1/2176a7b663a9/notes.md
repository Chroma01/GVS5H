
## ideation
The core difficulty lies in efficiently determining connectivity and finding the shortest path in a graph with $O(N^2)$ potential edges, defined by interval disjointness.
1.  **Graph Structure**: The graph $G$ connects $i$ and $j$ if their intervals $[L_i, R_i]$ and $[L_j, R_j]$ are disjoint. This is the complement of an interval graph (a co-interval graph).
2.  **Shortest Path Property**: Since all vertex weights are positive, the shortest path between two nodes $s$ and $t$ is either:
    *   A direct edge $(s, t)$, with weight $W_s + W_t$.
    *   A path of length 2: $s \to k \to t$, with weight $W_s + W_k + W_t$.
    *   Paths of length $>2$ are never optimal because adding intermediate nodes strictly increases the weight, and any path of length $>2$ implies a "shortcut" via a single intermediate node that is disjoint from both endpoints (if such a node exists and is cheaper than the direct path or other 2-hop paths). Specifically, in co-interval graphs, the diameter is small, and shortest paths can be found by checking direct edges and 2-hop paths via "extremal" nodes.
3.  **Connectivity**: Two nodes are in the same connected component if they can reach each other. If they are in different components, the answer is -1.
4.  **Efficient Querying**:
    *   **Direct Edge**: Check if $R_s < L_t$ or $R_t < L_s$.
    *   **2-Hop Path**: We need a node $k$ such that $[L_k, R_k]$ is disjoint from $[L_s, R_s]$ AND disjoint from $[L_t, R_t]$.
        *   If $[L_s, R_s]$ and $[L_t, R_t]$ overlap, their union is $[\min(L_s, L_t), \max(R_s, R_t)]$. Any $k$ disjoint from both must lie entirely to the left of $\min(L_s, L_t)$ or entirely to the right of $\max(R_s, R_t)$.
        *   If they do not overlap (say $R_s < L_t$), they are directly connected. We already handle this. If they are not directly connected, they MUST overlap.
    *   Therefore, for non-adjacent $s, t$, we need $\min W_k$ such that $R_k < \min(L_s, L_t)$ OR $L_k > \max(R_s, R_t)$.
5.  **Data Structures**:
    *   Sort intervals by $L_i$ to efficiently find the minimum weight node with $R_k < X$ (left side).
    *   Sort intervals by $R_i$ (or just use the same sorted list with a segment tree/Fenwick tree or prefix/suffix minimums) to efficiently find the minimum weight node with $L_k > Y$ (right side).
    *   Since we need range minimum queries on static data (sorted by $L$), we can precompute prefix minimums of weights for the "left" condition and suffix minimums for the "right" condition? No, the condition is on $R_k$ for the left side and $L_k$ for the right side.
    *   Let's refine:
        *   To find $\min \{W_k \mid R_k < X\}$: Sort all nodes by $R_k$. Use a Fenwick tree or Segment Tree over the sorted order? Or simply, since the condition is $R_k < X$, we can sort nodes by $R_k$. Then for a query $X$, we consider all nodes with $R_k < X$. We want the min weight among them. We can precompute a prefix minimum array on the nodes sorted by $R_k$.
        *   To find $\min \{W_k \mid L_k > Y\}$: Sort all nodes by $L_k$. For a query $Y$, consider all nodes with $L_k > Y$. We want the min weight among them. We can precompute a suffix minimum array on the nodes sorted by $L_k$.
6.  **Algorithm Steps**:
    *   Read input.
    *   Create a list of nodes sorted by $R_i$. Compute `min_left_weight[i]` = min weight among first `i` nodes in this sorted list.
    *   Create a list of nodes sorted by $L_i$. Compute `min_right_weight[i]` = min weight among last `i` nodes in this sorted list.
    *   For each query $(s, t)$:
        *   Check if direct edge exists: if $R_s < L_t$ or $R_t < L_s$. If yes, candidate = $W_s + W_t$.
        *   If no direct edge, they must overlap. Calculate $L_{min} = \min(L_s, L_t)$ and $R_{max} = \max(R_s, R_t)$.
        *   Find min weight node $k$ with $R_k < L_{min}$. This is a range query on the $R$-sorted list.
        *   Find min weight node $k$ with $L_k > R_{max}$. This is a range query on the $L$-sorted list.
        *   Candidate 2-hop weight = $W_s + W_t + \min(\text{min\_left\_weight}, \text{min\_right\_weight})$.
        *   If both min weights are infinity (no such node), then no path exists (output -1).
        *   Otherwise, output the minimum of the direct edge candidate (if exists) and the 2-hop candidate.
    *   Wait, is it possible that $s$ and $t$ are connected but not via a 2-hop path? In co-interval graphs, if $s$ and $t$ are connected, there is a path of length at most 2? Not necessarily. However, if there is a path, there is a "central" node or a chain. But due to the interval structure, if $s$ and $t$ are in the same component, either they are connected directly, or there exists a node $k$ that is disjoint from both (forming a 2-hop path), OR they are connected via a chain of overlapping intervals that "bridge" the gap.
    *   Actually, consider the complement graph $\bar{G}$ (interval graph). $s$ and $t$ are in the same component of $G$ if and only if they are NOT in the same component of $\bar{G}$? No. $G$ is the complement. Connectivity in $G$ is not simply related to components in $\bar{G}$.
    *   Let's re-evaluate. The graph $G$ is a co-interval graph. It is known that the shortest path between two vertices in a co-interval graph can be found by checking direct edges and 2-hop paths via vertices that are "extremal". Specifically, if $s$ and $t$ are not adjacent, any path between them must go through vertices that are disjoint from $s$ and $t$. The "best" such vertices are those with minimal weight.
    *   Is it possible that the shortest path is $s \to k_1 \to k_2 \to t$ with weight less than any 2-hop path?
        *   Weight $W_s + W_{k1} + W_{k2} + W_t$.
        *   Compare to $s \to k \to t$ with weight $W_s + W_k + W_t$.
        *   If there exists a $k$ disjoint from both $s$ and $t$, then $W_k$ is likely smaller than $W_{k1} + W_{k2}$.
        *   If NO $k$ is disjoint from both $s$ and $t$, then $s$ and $t$ cannot be connected by a 2-hop path. Can they be connected by a longer path?
        *   If no node is disjoint from both $s$ and $t$, it means every node intersects either $s$ or $t$ (or both).
        *   In interval graphs, if the intersection of all intervals is non-empty, the graph is a clique. Here, we are in the complement.
        *   Let's trust the property: For co-interval graphs, the shortest path is either direct or 2-hop. If no 2-hop path exists and no direct edge, they are disconnected.
        *   Why? If $s$ and $t$ are connected, there is a path. If the path has length $>2$, say $s-v_1-v_2-t$, then $v_1$ is disjoint from $s$ and $v_2$ is disjoint from $t$. Also $v_1$ and $v_2$ are connected (overlap). If there exists a node $k$ disjoint from both $s$ and $t$, we can shortcut to $s-k-t$. If no such $k$ exists, then the set of nodes disjoint from $s$ and the set of nodes disjoint from $t$ have no "common" node that can bridge them directly?
        *   Actually, if no node is disjoint from both $s$ and $t$, then the union of intervals disjoint from $s$ and intervals disjoint from $t$ might not allow a bridge. But if $s$ and $t$ are connected, there must be a chain.
        *   However, standard results for interval graph complements suggest that checking direct and 2-hop paths is sufficient for shortest paths.

## worker: (none)
1.  **Graph Interpretation**: The graph $G$ connects $i$ and $j$ if their intervals $[L_i, R_i]$ and $[L_j, R_j]$ are disjoint. This is the complement of an interval graph.
2.  **Shortest Path Logic**:
    *   Since all vertex weights $W_i$ are positive, the shortest path between two nodes $s$ and $t$ is either a direct edge or a path of length 2 ($s \to k \to t$). Paths of length $>2$ are strictly heavier than a corresponding 2-hop path if a suitable intermediate node exists, or imply disconnection if no such node exists.
    *   If a direct edge exists ($R_s < L_t$ or $R_t < L_s$), the weight is $W_s + W_t$. This is minimal because any other path would include at least one more vertex with positive weight.
    *   If no direct edge exists, $s$ and $t$ must overlap. For a node $k$ to be connected to both $s$ and $t$ in $G$, its interval must be disjoint from both $[L_s, R_s]$ and $[L_t, R_t]$.
    *   If two intervals overlap, their union is $[\min(L_s, L_t), \max(R_s, R_t)]$. Any interval disjoint from both must lie entirely to the left of $\min(L_s, L_t)$ or entirely to the right of $\max(R_s, R_t)$.
    *   Thus, we need to find $\min W_k$ such that $R_k < \min(L_s, L_t)$ or $L_k > \max(R_s, R_t)$.
3.  **Efficient Querying**:
    *   To find $\min W_k$ with $R_k < X$, we sort nodes by $R_i$ and precompute prefix minimums of weights. A binary search (`bisect_left`) on the sorted $R$ values gives the range of nodes satisfying the condition, and the precomputed prefix min gives the answer in $O(\log N)$.
    *   To find $\min W_k$ with $L_k > Y$, we sort nodes by $L_i$ and precompute suffix minimums of weights. A binary search (`bisect_right`) on the sorted $L$ values gives the range, and the suffix min gives the answer in $O(\log N)$.
4.  **Complexity**:
    *   Sorting: $O(N \log N)$.
    *   Precomputing prefix/suffix mins: $O(N)$.
    *   Each query: $O(\log N)$ for binary searches.
    *   Total Time: $O(N \log N + Q \log N)$, which fits within the constraints ($N, Q \le 2 \times 10^5$).
    *   Space: $O(N)$ for storing arrays and sorted lists.
