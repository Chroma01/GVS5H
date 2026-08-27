
## ideation
The core difficulty lies in efficiently calculating the minimum weight perfect matching between two sets of vertices $A$ and $B$ on a graph where the cost between two vertices is the "bottleneck distance" (min-max path weight).

1.  **Bottleneck Distance and MST**: The value $f(x, y)$ is the minimum possible maximum edge weight on a path between $x$ and $y$. This is a classic property of the Minimum Spanning Tree (MST). The unique path between $x$ and $y$ in the MST has the property that its maximum edge weight is equal to $f(x, y)$. Thus, we can replace the original graph with its MST without changing the costs $f(x, y)$.

2.  **Assignment Problem on Tree Metric**: We need to pair each $A_i$ with a unique $B_j$ to minimize the sum of bottleneck distances. This is a minimum weight perfect matching problem in a bipartite graph. Since $K$ can be up to $2 \times 10^5$, standard algorithms like Hungarian ($O(K^3)$) are too slow. However, the cost function is derived from a tree metric.

3.  **Edge Contribution Technique**: A key insight for matching problems on trees is to consider the contribution of each edge to the total cost.
    *   Consider an edge $e$ in the MST with weight $w_e$. Removing $e$ splits the tree into two components, $T_1$ and $T_2$.
    *   Any path between a node in $T_1$ and a node in $T_2$ must use edge $e$. Therefore, any matching pair $(a, b)$ with $a \in A \cap T_1$ and $b \in B \cap T_2$ (or vice versa) will have a bottleneck distance at least $w_e$.
    *   Let $countA(T_1)$ be the number of vertices from set $A$ in component $T_1$, and $countB(T_1)$ be the number of vertices from set $B$ in component $T_1$.
    *   The number of $A$-nodes in $T_1$ that *cannot* be matched to $B$-nodes within $T_1$ is $\max(0, countA(T_1) - countB(T_1))$. These must be matched to $B$-nodes in $T_2$.
    *   Similarly, if $countB(T_1) > countA(T_1)$, then $countB(T_1) - countA(T_1)$ $B$-nodes in $T_1$ must be matched to $A$-nodes in $T_2$.
    *   In either case, the number of matching edges that *must* cross the cut defined by $e$ is exactly $|countA(T_1) - countB(T_1)|$.
    *   Since we process edges from smallest to largest (implicitly, by building the MST and then aggregating counts from leaves up), we can ensure that all possible matches within the components are made using smaller edges. Thus, the minimum cost contributed by edge $e$ is $w_e \times |countA(T_1) - countB(T_1)|$.
    *   The total minimum cost is the sum over all edges $e$ in the MST: $\sum_{e} w_e \times |countA(T_1(e)) - countB(T_1(e))|$.

4.  **Algorithm**:
    *   Read input and build the MST using Kruskal's algorithm.
    *   Mark which vertices are in set $A$ and set $B$. Note that a vertex can be in both, or neither, or multiple times (since $A$ and $B$ are sequences, we treat them as multisets of vertices). We can store counts: `valA[u]` = number of times $u$ appears in $A$, `valB[u]` = number of times $u$ appears in $B$.
    *   Root the MST arbitrarily (e.g., at vertex 1).
    *   Perform a DFS/post-order traversal to compute for each node $u$, the total count of $A$-instances and $B$-instances in the subtree rooted at $u$. Let these be `subA[u]` and `subB[u]`.
    *   For each edge connecting a child $v$ to its parent $p$, the component "below" the edge is the subtree of $v$. The number of $A$-nodes in this component is `subA[v]`, and $B$-nodes is `subB[v]`.
    *   The contribution of this edge to the answer is $w \times |subA[v] - subB[v]|$.
    *   Sum these contributions to get the final answer.

5.  **Pitfalls**:
    *   Recursion depth for DFS might exceed limits for deep trees. Use iterative DFS or increase recursion limit.
    *   Large weights and sums require 64-bit integers.
    *   Handling multiple occurrences of vertices in $A$ and $B$ correctly by using counts rather than boolean flags.

## worker: (None)
1.  **MST Construction**: The problem defines $f(x, y)$ as the minimum possible maximum edge weight on a path between $x$ and $y$. This is the "bottleneck distance". A fundamental property of Minimum Spanning Trees (MST) is that the unique path between any two nodes in the MST minimizes the maximum edge weight among all paths between them in the original graph. Therefore, we can restrict our attention to the MST.
2.  **Assignment on Tree**: We need to match $K$ sources $A$ to $K$ targets $B$ to minimize the sum of bottleneck distances. This is a minimum weight perfect matching problem on a bipartite graph where costs are tree distances.
3.  **Edge Contribution Formula**: For any edge $e$ in the MST with weight $w$, removing it splits the tree into two components $T_1$ and $T_2$. Let $n_A(T_1)$ be the number of $A$-instances in $T_1$ and $n_B(T_1)$ be the number of $B$-instances in $T_1$. The number of matching pairs that must have one endpoint in $T_1$ and the other in $T_2$ is exactly $|n_A(T_1) - n_B(T_1)|$. Each such pair contributes at least $w$ to the total cost. By processing edges from smallest to largest (implicitly handled by the tree structure and post-order traversal), we can achieve this lower bound. Thus, the total minimum cost is $\sum_{e \in MST} w_e \times |n_A(T_1(e)) - n_B(T_1(e))|$.
4.  **Implementation Details**:
    *   Kruskal's algorithm is used to build the MST.
    *   Counts of vertices in $A$ and $B$ are stored in arrays to handle duplicates.
    *   An iterative DFS is used to traverse the MST, establishing parent pointers and processing order.
    *   A post-order traversal (reverse of the DFS visit order) is used to aggregate counts from leaves to root. For each node $u$ (except root), the edge connecting $u$ to its parent contributes $w \times |subA[u] - subB[u]|$ to the answer.
    *   Complexity: $O(M \log M)$ for sorting edges, nearly $O(M \alpha(N))$ for Kruskal's, and $O(N)$ for the tree traversal. This fits well within the time limits for $N, M \le 2 \times 10^5$.
