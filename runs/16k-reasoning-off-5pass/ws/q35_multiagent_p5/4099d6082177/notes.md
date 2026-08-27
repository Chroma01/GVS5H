
## ideation
The core difficulty lies in efficiently verifying if the tree can be partitioned into disjoint paths of length K. The proposed DFS/post-order greedy strategy is sound:
1.  Root the tree arbitrarily (e.g., at node 1).
2.  Process nodes bottom-up.
3.  For each node, determine the length of the path segment ending at that node coming from its subtree.
4.  A node can extend at most one incoming path segment from its children. All other children must have completed their paths (length K).
5.  If a node extends a path of length $L$ from a child, the new length is $L+1$. If no child provides an incomplete path, the node starts a new path of length 1.
6.  If any node tries to extend more than one incomplete path, or if the final path at the root is not exactly length K, the decomposition is impossible.

Pitfalls to avoid:
-   Incorrectly handling the root node (it doesn't have a parent to extend to, so its final path length must be exactly K).
-   Not handling the case where $K=1$ correctly (every node is a path of length 1, always Yes).
-   Recursion depth issues for large trees in Python. We should use an iterative DFS or BFS to establish parent pointers and processing order, or increase recursion limit. Given $NK \le 2 \times 10^5$, recursion limit might be hit. Iterative post-order traversal is safer.

Next steps:
1.  Parse input and build adjacency list.
2.  Handle edge case $K=1$ (output Yes).
3.  Root the tree at node 1, compute parent pointers and processing order (BFS/DFS to get topological sort from leaves to root).
4.  Implement the greedy check using the computed order.
5.  Output Yes/No.

## worker: (omitted)
The solution uses a greedy bottom-up approach on a rooted tree.
1.  **Tree Rooting**: We arbitrarily root the tree at node 1 using BFS to establish parent-child relationships and a processing order.
2.  **Bottom-Up Processing**: We process nodes from leaves to the root. For each node $u$, we examine the path segments coming from its children.
3.  **Greedy Logic**:
    *   Each child $v$ provides a path segment of length $L_v$ ending at $v$.
    *   If $L_v < K$, this segment is incomplete and *must* be extended through $u$.
    *   If $L_v = K$, the segment is complete and does not need extension.
    *   A node $u$ can extend at most one incoming incomplete path (since it has only one parent).
    *   If $u$ has more than one child with an incomplete path ($L_v < K$), it's impossible to decompose, so we return "No".
    *   If $u$ has exactly one child with an incomplete path, $u$ extends it, so the new length at $u$ becomes $L_v + 1$.
    *   If $u$ has no children with incomplete paths (all are complete or $u$ is a leaf), $u$ starts a new path of length 1.
4.  **Root Check**: The root node has no parent. Therefore, the path segment ending at the root must be exactly complete (length $K$). If $dp[root] \neq K$, return "No".
5.  **Complexity**: The BFS takes $O(NK)$ time. The bottom-up processing visits each node once and checks its children. The total number of edges is $NK-1$, so the total work in the loop is proportional to the number of edges, i.e., $O(NK)$. This fits within the constraints ($NK \le 2 \times 10^5$).
