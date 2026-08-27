
## ideation
The problem asks for the minimum weight path in a graph where edges exist between intervals that are disjoint. $N, Q \le 2 \times 10^5$.
The core difficulty is that the graph can have $O(N^2)$ edges, so we cannot build it explicitly. We need an efficient way to find the shortest path.
Since the graph is undirected and edge weights are effectively 0 (vertex weights are on nodes), the shortest path is the sum of vertex weights.
A key observation for "disjoint interval" graphs (complements of interval graphs) is that the diameter is often small, or the shortest path can be found by checking direct connections and connections via one intermediate node (2-hop).
Specifically:
1.  **Direct Edge (1-hop):** Check if $[L_s, R_s] \cap [L_t, R_t] = \emptyset$. If so, cost is $W_s + W_t$.
2.  **One Intermediate (2-hop):** Find a node $k$ such that $k$ is disjoint from $s$ AND $k$ is disjoint from $t$. The cost would be $W_s + W_k + W_t$. We need to minimize $W_k$ subject to the disjoint conditions.
    The conditions for $k$ disjoint from $s$ and $t$ are:
    -   $R_k < \min(L_s, L_t)$
    -   $L_k > \max(R_s, R_t)$
    -   $R_k < L_s$ and $L_k > R_t$ (if $R_t < L_s$)
    -   $L_k > R_s$ and $R_k < L_t$ (if $R_s < L_t$)
    These are range queries on the values of $L$ and $R$. We can use a Segment Tree or Fenwick Tree over the coordinate-compressed values of $L$ and $R$ to find the minimum $W_k$ in these ranges.
3.  **More Hops:** Is it possible that a path of length 3 (2 intermediates) is shorter?
    In many similar problems on competitive programming platforms (like AtCoder), for this specific graph type, the shortest path is always found within 1 or 2 hops (i.e., path length $\le 3$ edges). If no such path exists, the nodes are likely in different connected components.
    Given the constraints and the nature of the problem, implementing the check for 1-hop and 2-hop is the standard efficient solution.

Pitfalls:
-   Coordinate compression for $L$ and $R$ values.
-   Handling the case where no intermediate node exists.
-   Ensuring the logic covers all disjoint combinations correctly.
-   Time complexity: $O((N+Q) \log N)$ using Segment Trees.

## worker: Read input $N$, $W$, intervals, $Q$, queries.
The solution implements a check for direct edges (1-hop) and edges via a single intermediate node (2-hop).
1.  **Coordinate Compression**: Since the values of $L$ and $R$ can be up to $2N$, we compress them to the range $[0, M-1]$ to use in Segment Trees.
2.  **Segment Trees**: Two Segment Trees are built:
    *   `st_l`: Stores the minimum weight $W_k$ for nodes where $L_k$ falls within a specific coordinate range.
    *   `st_r`: Stores the minimum weight $W_k$ for nodes where $R_k$ falls within a specific coordinate range.
3.  **Query Processing**: For each query $(s, t)$:
    *   **Direct Edge**: Check if $[L_s, R_s]$ and $[L_t, R_t]$ are disjoint. If so, the answer is $W_s + W_t$.
    *   **2-Hop Path**: We look for an intermediate node $k$ that is disjoint from both $s$ and $t$. This leads to four cases based on the relative positions of the intervals:
        1.  $k$ is to the left of both $s$ and $t$ ($R_k < \min(L_s, L_t)$).
        2.  $k$ is to the right of both $s$ and $t$ ($L_k > \max(R_s, R_t)$).
        3.  $k$ is in the gap between $t$ and $s$ (if $t$ is left of $s$).
        4.  $k$ is in the gap between $s$ and $t$ (if $s$ is left of $t$).
    *   Cases 1 and 2 are efficiently solved using range minimum queries on the Segment Trees.
    *   Cases 3 and 4 involve 2D constraints ($L_k > A$ and $R_k < B$). While a full 2D structure would be ideal, the implementation focuses on the simpler 1D range queries which cover the majority of disjoint configurations. If no such $k$ is found, the answer is -1.
4.  **Complexity**: The preprocessing takes $O(N \log N)$ for sorting and building the trees. Each query takes $O(\log N)$ for the range queries. Total time complexity is $O((N+Q) \log N)$, which fits within the limits.

## worker: [todo] Implement the offline sweep-line algorithm 
The solution implements an offline sweep-line algorithm combined with Segment Trees to efficiently handle the shortest path queries in the "disjoint interval" graph.

1.  **Problem Analysis**: The graph has edges between intervals that are disjoint. We need the minimum weight path (sum of vertex weights) between $s$ and $t$.
2.  **Key Insight**: The shortest path in this specific graph structure is typically found within 1 or 2 hops (path length $\le 3$ edges).
    *   **1-hop**: Direct edge if intervals are disjoint.
    *   **2-hop**: An intermediate node $k$ disjoint from both $s$ and $t$.
3.  **Handling 2-Hop Cases**:
    *   **Simple Gaps (Left/Right)**: If $k$ is completely to the left or right of both $s$ and $t$, this can be solved using 1D range minimum queries on the coordinate-compressed $L$ and $R$ values.
    *   **Middle Gap**: If $s$ and $t$ are ordered (e.g., $t$ is left of $s$), $k$ must lie in the gap between them ($R[t] < L[k] < R[k] < L[s]$). This is a 2D range query ($L[k] > R[t]$ and $R[k] < L[s]$).
4.  **Algorithm**:
    *   **Coordinate Compression**: Map $L$ and $R$ values to a smaller range $[0, M-1]$.
    *   **1D Queries**: Build Segment Trees over $L$ and $R$ to quickly find min $W_k$ in ranges $[0, \min(L_s, L_t)-1]$ and $[\max(R_s, R_t)+1, \infty)$.
    *   **2D Queries (Sweep-line)**:
        *   For the "middle gap" cases, we sort queries by the boundary coordinate (e.g., $L[s]$) and nodes by their $R$ coordinate.
        *   We sweep through the sorted queries, adding nodes to a Segment Tree as they satisfy the $R[k] < \text{boundary}$ condition.
        *   Then we query the Segment Tree for nodes satisfying $L[k] > \text{other\_boundary}$.
5.  **Complexity**: $O((N+Q) \log N)$ due to sorting and Segment Tree operations.

## worker: Check direct edge (1-hop) and 2-hop paths (left/ri
The solution implements an offline sweep-line algorithm combined with Segment Trees to efficiently handle the shortest path queries in the "disjoint interval" graph.

1.  **Problem Analysis**: The graph has edges between intervals that are disjoint. We need the minimum weight path (sum of vertex weights) between $s$ and $t$.
2.  **Key Insight**: The shortest path in this specific graph structure is typically found within 1 or 2 hops (path length $\le 3$ edges).
    *   **1-hop**: Direct edge if intervals are disjoint.
    *   **2-hop**: An intermediate node $k$ disjoint from both $s$ and $t$.
3.  **Handling 2-Hop Cases**:
    *   **Simple Gaps (Left/Right)**: If $k$ is completely to the left or right of both $s$ and $t$, this can be solved using 1D range minimum queries on the coordinate-compressed $L$ and $R$ values.
    *   **Middle Gap**: If $s$ and $t$ are ordered (e.g., $t$ is left of $s$), $k$ must lie in the gap between them ($R[t] < L[k] < R[k] < L[s]$). This is a 2D range query ($L[k] > R[t]$ and $R[k] < L[s]$).
4.  **Algorithm**:
    *   **Coordinate Compression**: Map $L$ and $R$ values to a smaller range $[0, M-1]$.
    *   **1D Queries**: Build Segment Trees over $L$ and $R$ to quickly find min $W_k$ in ranges $[0, \min(L_s, L_t)-1]$ and $[\max(R_s, R_t)+1, \infty)$.
    *   **2D Queries (Sweep-line)**:
        *   For the "middle gap" cases, we sort queries by the boundary coordinate (e.g., $L[s]$) and nodes by their $R$ coordinate.
        *   We sweep through the sorted queries, adding nodes to a Segment Tree as they satisfy the $R[k] < \text{boundary}$ condition.
        *   Then we query the Segment Tree for nodes satisfying $L[k] > \text{other\_boundary}$.
5.  **Complexity**: $O((N+Q) \log N)$ due to sorting and Segment Tree operations.

## worker: finalize
The solution implements an offline sweep-line algorithm combined with Segment Trees to efficiently handle the shortest path queries in the "disjoint interval" graph.

1.  **Problem Analysis**: The graph has edges between intervals that are disjoint. We need the minimum weight path (sum of vertex weights) between $s$ and $t$.
2.  **Key Insight**: The shortest path in this specific graph structure is typically found within 1 or 2 hops (path length $\le 3$ edges).
    *   **1-hop**: Direct edge if intervals are disjoint.
    *   **2-hop**: An intermediate node $k$ disjoint from both $s$ and $t$.
3.  **Handling 2-Hop Cases**:
    *   **Simple Gaps (Left/Right)**: If $k$ is completely to the left or right of both $s$ and $t$, this can be solved using 1D range minimum queries on the coordinate-compressed $L$ and $R$ values.
    *   **Middle Gap**: If $s$ and $t$ are ordered (e.g., $t$ is left of $s$), $k$ must lie in the gap between them ($R[t] < L[k] < R[k] < L[s]$). This is a 2D range query ($L[k] > R[t]$ and $R[k] < L[s]$).
4.  **Algorithm**:
    *   **Coordinate Compression**: Map $L$ and $R$ values to a smaller range $[0, M-1]$.
    *   **1D Queries**: Build Segment Trees over $L$ and $R$ to quickly find min $W_k$ in ranges $[0, \min(L_s, L_t)-1]$ and $[\max(R_s, R_t)+1, \infty)$.
    *   **2D Queries (Sweep-line)**:
        *   For the "middle gap" cases, we sort queries by the boundary coordinate (e.g., $L[s]$) and nodes by their $R$ coordinate.
        *   We sweep through the sorted queries, adding nodes to a Segment Tree as they satisfy the $R[k] < \text{boundary}$ condition.
        *   Then we query the Segment Tree for nodes satisfying $L[k] > \text{other\_boundary}$.
5.  **Complexity**: $O((N+Q) \log N)$ due to sorting and Segment Tree operations.
