
## ideation
The problem asks for the largest subgraph of a given tree $T$ that satisfies the "alkane" property: it is a tree where every vertex has degree 1 or 4, and at least one vertex has degree 4.

Key observations:
1.  **Subgraph Structure**: Since the original graph is a tree, any subgraph is also a forest. We are looking for a connected subgraph (a tree) that is an alkane.
2.  **Degree Constraints**: In the alkane subgraph, every node has degree 1 or 4.
    *   Leaves of the alkane have degree 1.
    *   Internal nodes have degree 4.
3.  **Rooted DP Approach**: We can root the original tree arbitrarily (e.g., at vertex 1) and use dynamic programming on the tree structure. For each node $u$, we want to compute the maximum size of valid structures in its subtree.
4.  **State Definition**:
    *   `dp1[u]`: The maximum number of vertices in a valid "branch" ending at $u$ within the subtree of $u$. In this branch, $u$ has degree 1 (it connects to its parent in the full tree context, so within the subtree, it acts as the root of this branch). This branch consists of $u$ and a valid structure attached to one of its children. The child $v$ can either be a leaf in the alkane (degree 1 in alkane, so `dp1[v]` represents the branch from $v$ downwards) or a center (degree 4 in alkane, so `dp4[v]` represents the center $v$ with 4 branches). Note: If $v$ is a center, the edge $(u,v)$ is one of the 4 edges for $v$. So `dp4[v]` already accounts for $v$ having degree 4. If $v$ is a leaf in the alkane, the edge $(u,v)$ is its only edge, so `dp1[v]` accounts for $v$ having degree 1. Thus, the contribution from child $v$ is `max(dp1[v], dp4[v])`.
    *   `dp4[u]`: The maximum number of vertices in a valid alkane structure where $u$ is a center (degree 4). This requires $u$ to connect to exactly 4 distinct children $v_1, v_2, v_3, v_4$. Each child $v_i$ will be the root of a valid branch (either a leaf branch or a center branch). The size is $1 + \sum_{i=1}^4 \max(dp1[v_i], dp4[v_i])$. We pick the 4 children that maximize this sum.

5.  **Transitions**:
    *   For a leaf $u$: `dp1[u] = 1`, `dp4[u] = -infinity` (cannot have degree 4).
    *   For internal node $u$:
        *   `dp1[u] = 1 + max(max(dp1[v], dp4[v]) for v in children)`. If $u$ has no children, it's a leaf, handled above. If it has children, we take the best one.
        *   `dp4[u]`: Collect `val[v] = max(dp1[v], dp4[v])` for all children $v$. If there are fewer than 4 children, `dp4[u] = -infinity`. Otherwise, sum the largest 4 `val[v]` and add 1.

6.  **Answer**: The answer is the maximum `dp4[u]` over all nodes $u$. If no node can form a degree-4 center (i.e., all `dp4[u]` are $-\infty$), output -1.

7.  **Pitfalls**:
    *   Handling $-\infty$ correctly to avoid invalid structures.
    *   Ensuring that `dp1[u]` is always valid (at least 1) because a single node can be a branch of length 1 (degree 0 in subtree, degree 1 when connected to parent).
    *   The definition of `dp1` and `dp4` must be consistent. `dp1[u]` means $u$ has degree 1 in the final alkane subgraph. In the subtree, it connects to one child. That child's degree in the alkane is determined by its own state. If the child is a leaf in the alkane, it has degree 1 (edge to $u$). If the child is a center, it has degree 4 (edge to $u$ plus 3 others). Both are valid.

Let's refine the base case and transitions.
- `dp1[u]`: Max size of a tree rooted at $u$ (in the DP sense, meaning $u$ is the highest node in the subtree) where $u$ has degree 1 in the alkane. This tree is formed by $u$ and one valid component attached to a child. The child $v$ can be the root of a component where $v$ has degree 1 (`dp1[v]`) or degree 4 (`dp4[v]`). So `dp1[u] = 1 + max_{v \in children(u)} (max(dp1[v], dp4[v]))`. If $u$ is a leaf in the original tree, `dp1[u] = 1`.
- `dp4[u]`: Max size of a tree rooted at $u$ where $u$ has degree 4. This requires 4 children. `dp4[u] = 1 + sum of largest 4 (max(dp1[v], dp4[v]))`. If fewer than 4 children, `dp4[u] = -inf`.

The global answer is `max_{u} dp4[u]`.

## worker: (None)
The solution uses dynamic programming on trees. We root the tree arbitrarily at vertex 1. For each node `u`, we compute two values:
1. `dp1[u]`: The maximum size of a valid "branch" in the subtree of `u` where `u` has degree 1 in the alkane subgraph. This branch consists of `u` and exactly one valid component attached to one of its children. The child `v` can either be a leaf in the alkane (`dp1[v]`) or a center (`dp4[v]`). The value is `1 + max(max(dp1[v], dp4[v]))` over all children `v`.
2. `dp4[u]`: The maximum size of a valid alkane component in the subtree of `u` where `u` has degree 4. This requires `u` to connect to exactly 4 distinct children. We take the sum of the largest 4 values of `max(dp1[v], dp4[v])` from its children and add 1 for `u` itself.

The base case for a leaf node `u` is `dp1[u] = 1` and `dp4[u] = -infinity`.
The final answer is the maximum `dp4[u]` over all nodes `u`. If no node can form a degree-4 center, the answer is -1.

The algorithm runs in $O(N \log N)$ due to sorting the child values for each node, but since each node has a bounded number of children in the context of picking the top 4, we can optimize the sorting to $O(\text{degree}(u))$ or even $O(1)$ if we only keep the top 4. However, sorting a small list is efficient enough. The overall complexity is $O(N)$ if we use a linear selection or just sort small lists. Given $N \le 2 \times 10^5$, this approach is efficient.
