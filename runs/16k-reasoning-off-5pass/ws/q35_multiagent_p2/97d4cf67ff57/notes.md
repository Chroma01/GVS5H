
## ideation
The core difficulty lies in correctly identifying what constitutes a valid "branch" extending from a potential degree-4 node in the alkane subgraph.

1.  **Alkane Structure**: An alkane is a tree where internal nodes have degree 4 and leaves have degree 1. This implies that if we root the alkane at a degree-4 node, it consists of exactly 4 disjoint paths (branches) emanating from the root. Each path must end in a leaf of the alkane (degree 1). The nodes along these paths (excluding the root) have degree 2 within the alkane.
2.  **Subgraph Constraint**: Since we are looking for a *subgraph* of the original tree $T$, the branches must be simple paths in $T$. We cannot merge branches or reuse nodes.
3.  **Key Insight**: For any node $u$ in $T$ that serves as the "center" (degree 4 node) of an alkane, we need to find 4 disjoint paths starting at $u$ and going into 4 different subtrees (or neighbors) such that each path is as long as possible. The total size of the alkane centered at $u$ would be $1 + \sum_{i=1}^4 L_i$, where $L_i$ is the number of edges in the $i$-th branch (so the number of vertices in that branch is $L_i$). Wait, if the branch has $L_i$ edges, it has $L_i$ vertices excluding the root? No, if the branch is a path of length $k$ (edges), it has $k$ vertices attached to the root? Let's trace: Root $u$. Branch 1: $u-v_1$. Length 1 edge, 1 vertex $v_1$. Total vertices $1+1=2$. Branch 2: $u-v_2-w_2$. Length 2 edges, 2 vertices $v_2, w_2$. Total vertices $1+1+2=4$. So if a branch has $k$ edges, it contributes $k$ vertices to the total count (excluding the root). Thus, Total Vertices = $1 + \sum_{i=1}^4 \text{length}_i$.
4.  **DP State**: For each node $u$, we want to compute the maximum length of a path starting at $u$ and going downwards into its subtree. Let this be `max_path[u]`.
    -   `max_path[u]` = $1 + \max(\{max\_path[v] \mid v \in children(u)\} \cup \{0\})$.
    -   Actually, this is just the height of the subtree if we consider the longest path. But we need to be careful: the path must be valid. In a tree, any path from $u$ down to a leaf is valid. The "length" is the number of edges.
5.  **Algorithm**:
    -   Root the tree at vertex 1.
    -   Perform a DFS to compute `dp[u]`, the maximum length of a path starting at $u$ and going down into its subtree.
        -   `dp[u] = 1 + max([dp[v] for v in children(u)] + [0])`
        -   Wait, if a child $v$ has `dp[v]=0` (leaf), then the path $u-v$ has length 1. So `dp[u] = 1 + max(...)`. If no children, `dp[u]=0`? No, a single node has path length 0. A node with a leaf child has path length 1.
        -   Let's redefine: `dp[u]` is the maximum number of edges in a path starting at $u$ and going down.
        -   Leaf: `dp[u] = 0`.
        -   Node with children: `dp[u] = 1 + max(dp[v] for v in children)`.
    -   For each node $u$, collect the `dp[v]` values from all its neighbors (children and parent).
        -   Note: For the parent, we need the max path length going *up* from $u$. This requires a second DFS (rerooting) or careful handling.
    -   Actually, we can do this in two passes:
        1.  **Downward Pass**: Compute `down[u]` = max path length from $u$ into its subtree.
        2.  **Upward Pass**: Compute `up[u]` = max path length from $u$ going through its parent.
            -   For the root, `up[root] = 0` (or -infinity if we consider no path, but effectively 0 edges).
            -   For a child $v$ of $u$, `up[v]` depends on `up[u]` and `down` values of $u$'s other children.
            -   Specifically, `up[v] = 1 + max(up[u], max(down[w] for w in children(u) if w != v))`.
    -   After computing `down[u]` and `up[u]` for all $u$, for each node $u$, we have a set of branch lengths:
        -   From children: `down[v]` for each child $v$.
        -   From parent: `up[u]`.
    -   If $u$ has at least 4 branches with length $\ge 0$ (actually, we need to check if we can form a valid alkane. The problem says degree 1 or 4. A branch of length 0 means the neighbor is just $u$ itself? No, a branch of length 0 corresponds to a leaf attached to $u$. In our definition, `down[v]=0` means $v$ is a leaf. The edge $u-v$ has length 1. So the contribution to the vertex count is 1.
    -   Let's stick to edge lengths.
        -   Branch length $L$ means $L$ edges.
        -   Number of vertices in branch = $L$.
        -   Total vertices = $1 + \sum L_i$.
    -   We need to pick the 4 largest branch lengths from the available branches at $u$.
    -   Available branches at $u$:
        -   For each child $v$: length `down[v] + 1`? No.
        -   Let's re-verify `dp` definition.
        -   If `dp[u]` is max edges in path down from $u$:
            -   Leaf: `dp[u] = 0`.
            -   Child $v$ has `dp[v]`. Path $u \to v \to \dots$ has length $1 + dp[v]$.
            -   So `dp[u] = 1 + max(dp[v])`.
        -   So the branch length from $u$ to child $v$ is `1 + dp[v]`.
        -   The branch length from $u$ to parent is `up[u]`.
    -   So for each node $u$, we collect:
        -   `up[u]` (if parent exists, else ignore or 0? If no parent, no upward branch).
        -   `1 + dp[v]` for each child $v$.
    -   Sort these lengths in descending order.
    -   If there are at least 4 branches, take the top 4.
    -   Candidate answer: $1 + \sum_{i=1}^4 \text{top\_4\_lengths}$.
    -   We must ensure that the alkane has at least one degree-4 node. By definition, the center $u$ is degree 4. The leaves of the alkane are the ends of these 4 branches. Are they degree 1? Yes, because we stop the branch there. The internal nodes of the branches have degree 2 in the alkane (connected to previous and next node in path).
    -   Is it possible that a branch ends at a node that already has other connections in the alkane? No, because we are picking disjoint paths from $u$ into different subtrees/neighbors. The only shared node is $u$.
    -   Pitfall: What if the "leaf" of a branch is actually a node with degree > 1 in the original tree? It doesn't matter. In the *subgraph*, that node will have degree 1 (only connected to its predecessor in the path). The subgraph doesn't include the other edges.
    -   So, the strategy is sound.

6.  **Implementation Details**:
    -   Adjacency list.
    -   DFS 1: Compute `down[u]`.
    -   DFS 2: Compute `up[u]`.
    -   Iterate all nodes, collect branch lengths, compute max alkane size.
    -   If no node has $\ge 4$ branches, output -1.

## worker: Implement the solution: Read input, build adjacenc
1.  **Problem Analysis**: An alkane subgraph is a tree where internal nodes have degree 4 and leaves have degree 1. Since it's a subgraph of a tree $T$, it must also be a tree. Any such alkane must have at least one node of degree 4. If we root the alkane at one of its degree-4 nodes, it consists of exactly 4 disjoint paths (branches) emanating from the root. The total number of vertices is $1 + \sum_{i=1}^4 L_i$, where $L_i$ is the number of edges in the $i$-th branch (which equals the number of vertices in that branch excluding the root).

2.  **Algorithm**:
    *   **Rooting**: Root the original tree $T$ at vertex 1.
    *   **Down DP**: Compute `down[u]`, the maximum length (in edges) of a path starting at $u$ and going down into its subtree. This is done via a post-order traversal (leaves to root).
        *   `down[u] = 1 + max(down[v] for v in children(u))`, or 0 if leaf.
    *   **Up DP**: Compute `up[u]`, the maximum length (in edges) of a path starting at $u$ and going up through its parent. This is done via a pre-order traversal (root to leaves).
        *   For a child $v$ of $u$, `up[v] = 1 + max(up[u], max(down[w] for w in children(u) if w != v))`.
    *   **Branch Collection**: For each node $u$, the available branches are:
        *   To each child $v$: length `1 + down[v]`.
        *   To parent: length `up[u]` (if parent exists).
    *   **Maximization**: For each node $u$ with at least 4 branches, sort the branch lengths in descending order, take the top 4, and calculate the candidate alkane size: $1 + \sum_{i=1}^4 \text{top\_4\_lengths}$. The maximum over all such nodes is the answer.

3.  **Complexity**:
    *   Building adjacency list: $O(N)$.
    *   DFS/BFS for order and parent pointers: $O(N)$.
    *   Down DP: $O(N)$.
    *   Up DP: For each node, we iterate over its children. The total work across all nodes is proportional to the sum of degrees, which is $O(N)$. Finding the max alternative for each child can be optimized by precomputing the top 2 down values among children, but even the naive iteration over siblings for each child sums to $O(\sum \text{deg}(u)^2)$ in worst case? No, we iterate `adj[u]` for each child `v` of `u`. This is $O(\text{deg}(u)^2)$. Sum of squares of degrees can be $O(N^2)$ in star graph.
    *   **Optimization for Up DP**: To avoid $O(\text{deg}(u)^2)$, for each node $u$, we can find the largest and second largest `down` values among its children. Then for each child $v$, if `down[v]` is the largest, we use the second largest; otherwise, we use the largest. This makes the Up DP pass $O(N)$.
    *   **Final Pass**: Iterating all nodes and sorting up to 4 branches is $O(N \log 4) = O(N)$.
    *   Total Time Complexity: $O(N)$.
    *   Space Complexity: $O(N)$ for arrays and recursion stack.

4.  **Edge Cases**:
    *   $N < 5$: Impossible to have a degree-4 node with 4 branches. Output -1.
    *   Star graph: Center has $N-1$ branches. We pick top 4.
    *   Line graph: No node has degree $\ge 4$. Output -1.

5.  **Correction in Code**: The initial Up DP implementation inside the loop iterates over siblings for each child, which is $O(\text{deg}(u)^2)$. I will optimize this in the final code by precomputing the top 2 down values for each node's children.
