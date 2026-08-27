
## ideation
The core difficulty lies in correctly modeling the constraints of an "alkane" subgraph within a tree using dynamic programming. An alkane is a tree where every vertex has degree 1 or 4, with at least one vertex of degree 4. Since we are looking for a subgraph of the original tree $T$, the subgraph must be connected and a tree.

Key insights:
1.  **Rooting the Alkane**: Any alkane has at least one node of degree 4. We can view the alkane as rooted at one of its degree-4 nodes (or any node if we consider the structure). In a rooted alkane:
    *   The root has degree 4 in the alkane. Since it's the root, it has 4 children in the alkane structure.
    *   Any other internal node has degree 4 in the alkane. One edge connects to its parent, so it must have exactly 3 children in the alkane structure.
    *   Leaves have degree 1 in the alkane, meaning they have 0 children in the alkane structure.

2.  **DP State Definition**:
    Let's root the original tree $T$ at an arbitrary node (e.g., node 1). For each node $u$, we compute:
    *   `dp[u][0]`: The maximum number of vertices in a valid alkane subtree rooted at $u$ where $u$ is a **leaf** in the alkane. This means $u$ is not connected to any of its children in the alkane. The size is simply 1 (just $u$). However, this state is only useful if $u$ is connected to its parent in the alkane.
    *   `dp[u][3]`: The maximum number of vertices in a valid alkane subtree rooted at $u$ where $u$ is an **internal node** with exactly **3 children** in the alkane. This implies $u$ will be connected to its parent in the alkane (making its total degree 4). To form this, we select 3 children $v_1, v_2, v_3$ and for each child, we take the best alkane subtree rooted at that child where the child is either a leaf (`dp[v][0]`) or an internal node with 3 children (`dp[v][3]`). Note: A child cannot be an internal node with 4 children if it's connected to $u$, because that would make the child's degree 5 (1 parent + 4 children). So for a child $v$ connected to $u$, the max size is `max(dp[v][0], dp[v][3])`.
    *   `dp[u][4]`: The maximum number of vertices in a valid alkane subtree rooted at $u$ where $u$ is the **root** of the alkane with exactly **4 children** in the alkane. This is a candidate for the final answer. We select 4 children and sum `max(dp[v][0], dp[v][3])` for them, plus 1 for $u$.

3.  **Transitions**:
    *   `dp[u][0] = 1` (u is a leaf in the alkane, no children included).
    *   For `dp[u][3]`: Collect values `val[v] = max(dp[v][0], dp[v][3])` for all children $v$. If there are at least 3 children, pick the largest 3 values and sum them, then add 1 for $u$. If fewer than 3 children, this state is invalid (set to $-\infty$).
    *   For `dp[u][4]`: Collect values `val[v]` for all children $v$. If there are at least 4 children, pick the largest 4 values and sum them, then add 1 for $u$. If fewer than 4 children, this state is invalid.

4.  **Answer**: The answer is the maximum value of `dp[u][4]` over all nodes $u$. If no such `dp[u][4]` exists (i.e., no node has 4 children in the original tree that can form valid structures), output -1.

5.  **Pitfalls**:
    *   Forgetting that a child connected to an internal node $u$ can be either a leaf or an internal node with 3 children, but NOT an internal node with 4 children.
    *   Incorrectly handling nodes with fewer than 3 or 4 children.
    *   The global maximum must be a root of an alkane (degree 4), so we only consider `dp[u][4]` for the final answer.

## worker: (None)
The problem asks for the maximum size of a subgraph of a given tree $T$ that forms an "alkane". An alkane is defined as a tree where every vertex has degree 1 or 4, and there is at least one vertex of degree 4.

1.  **Structure Analysis**:
    *   Since the subgraph must be a tree and a subgraph of $T$, it must be connected.
    *   In any such alkane, if we root it at a vertex of degree 4, the root has 4 children in the alkane structure.
    *   Any other internal vertex (degree 4 in alkane) has 1 parent and 3 children in the alkane structure.
    *   Leaves have degree 1 in the alkane, so they have 0 children in the alkane structure.

2.  **Dynamic Programming Approach**:
    *   We root the original tree $T$ at an arbitrary node (node 1).
    *   For each node $u$, we compute three DP states based on the role $u$ plays in the alkane subgraph within its subtree:
        *   `dp0[u]`: $u$ is a leaf in the alkane. This means $u$ is not connected to any of its children in the alkane. The size is simply 1.
        *   `dp3[u]`: $u$ is an internal node in the alkane with exactly 3 children in the alkane. This implies $u$ is connected to its parent in the alkane (making its total degree 4). To form this, we select 3 children $v$ and for each, we take the best alkane structure rooted at $v$ where $v$ is either a leaf (`dp0[v]`) or an internal node with 3 children (`dp3[v]`). A child cannot be an internal node with 4 children if it's connected to $u$ because that would violate the degree constraint for the child (degree would be 5).
        *   `dp4[u]`: $u$ is the root of the alkane with exactly 4 children in the alkane. This is a candidate for the final answer. We select 4 children and sum their best contributions (`max(dp0[v], dp3[v])`), plus 1 for $u$.

3.  **Transitions**:
    *   `dp0[u] = 1` for all $u$.
    *   For `dp3[u]`: Collect `val[v] = max(dp0[v], dp3[v])` for all children $v$. If there are at least 3 children, `dp3[u] = 1 + sum(top 3 val[v])`. Otherwise, `dp3[u] = -inf`.
    *   For `dp4[u]`: Similarly, if there are at least 4 children, `dp4[u] = 1 + sum(top 4 val[v])`. Otherwise, `dp4[u] = -inf`. Update the global maximum with `dp4[u]`.

4.  **Complexity**:
    *   Sorting children's values for each node takes $O(d_u \log d_u)$ where $d_u$ is the degree of $u$. Summing over all nodes, this is bounded by $O(N \log N)$ in the worst case (star graph), but typically much faster. Given $N \le 2 \times 10^5$, this is efficient.
    *   Space complexity is $O(N)$ for the DP arrays and recursion stack.

5.  **Edge Cases**:
    *   If $N < 5$, it's impossible to have a degree 4 node, so output -1.
    *   If no node can form a valid `dp4` structure, output -1.
