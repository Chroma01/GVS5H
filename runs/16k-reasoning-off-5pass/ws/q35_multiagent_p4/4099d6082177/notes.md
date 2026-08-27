
## ideation
The problem asks for a decomposition of a tree with $NK$ vertices into $N$ disjoint paths, each of length $K$ (containing $K$ vertices). This is a "perfect K-path packing" problem.

Key insights:
1.  **Greedy Strategy from Leaves**: We can root the tree arbitrarily (e.g., at vertex 1) and process it in post-order (bottom-up). For each subtree, we determine if it can be fully decomposed into complete paths of length $K$, and if not, what is the length of the "pending" path segment that ends at the root of the subtree and needs to be extended upwards.
2.  **State Representation**: For a node $u$, the DFS returns an integer $r$.
    *   $r \in [0, K-1]$: There is a pending path segment of length $r$ ending at $u$. If $r=0$, it means the subtree is perfectly decomposed (no pending segment, or a segment of length $K$ was just completed and removed). Note: Returning 0 is slightly ambiguous if we consider "no pending path" vs "pending path of length 0". It's better to return the length of the pending path. If the subtree is fully decomposed, we can conceptually say the pending length is 0, but we must distinguish between "no path exists" and "path of length 0". However, since every vertex must be covered, a "pending path" always includes the current node. So a valid return value is the number of vertices in the partial path ending at $u$. If the subtree is fully covered by complete paths, we return 0 to indicate "no pending path extending to parent".
    *   $-1$: Impossible to decompose the subtree.
3.  **Merging at Node $u$**:
    *   Collect pending lengths $r_v$ from all children $v$.
    *   Each child's pending path of length $r_v$ can be extended to $u$, becoming a path of length $r_v + 1$ ending at $u$.
    *   If any child returns a value that results in length $K$ (i.e., $r_v + 1 == K$), that path is complete and removed from consideration.
    *   Let $P$ be the list of lengths of pending paths from children after extension (i.e., $r_v + 1$ for all $v$ where $r_v + 1 < K$).
    *   **Constraint**: In a path decomposition, any internal node has degree at most 2 in the union of paths. This means node $u$ can be part of at most 2 path segments coming from its children.
        *   If $|P| > 2$, it's impossible to merge them all into a single path passing through $u$ or completing paths, because $u$ can only connect to 2 neighbors in the path structure. Thus, return -1.
        *   If $|P| == 2$, we must merge these two segments at $u$. The new length is $p_1 + p_2$.
            *   If $p_1 + p_2 == K$, the path is complete. Return 0.
            *   If $p_1 + p_2 < K$, we have a pending path of length $p_1 + p_2$. Return $p_1 + p_2$.
            *   If $p_1 + p_2 > K$, it's impossible. Return -1.
        *   If $|P| == 1$, we have one pending path of length $p_1$. We can extend it to the parent. Return $p_1$.
        *   If $|P| == 0$, there are no pending paths from children. Node $u$ must start a new path segment of length 1. Return 1.
4.  **Final Check**: After processing the root, if the returned value is 0, it means all paths are complete and the decomposition is valid. If it returns any $L > 0$, there is an incomplete path, so return No. If it returns -1, return No.

Pitfalls:
*   Handling $K=1$ correctly.
*   Ensuring the root's final state is checked properly.
*   The condition $|P| > 2$ is critical. Some might think we can merge more, but topological constraints of paths (degree $\le 2$) forbid it.

## worker: Implement the DFS function as described.
The solution uses a greedy bottom-up approach (post-order traversal) to determine if the tree can be decomposed into paths of length $K$.
1.  **Tree Traversal**: We first establish a parent-child relationship by rooting the tree at vertex 1 using a simple DFS/BFS. This gives us a processing order where children are processed before their parents.
2.  **State Propagation**: For each node $u$, we calculate a `pending` value. This value represents the length of a path segment ending at $u$ that is not yet complete (length $< K$). If the subtree rooted at $u$ is perfectly decomposed into complete paths, the pending value is 0. If it's impossible, the value is -1.
3.  **Merging Logic**:
    *   For each child $v$, if it returns a pending length $r_v$, we extend it to $u$, resulting in length $r_v + 1$.
    *   If this new length equals $K$, the path is complete and discarded.
    *   If it's less than $K$, it becomes a candidate pending path at $u$.
    *   **Degree Constraint**: A node in a path decomposition can have at most 2 incident edges belonging to the paths. Thus, at node $u$, we can accept pending paths from at most 2 children. If more than 2 children provide pending paths, it's impossible (`pending[u] = -1`).
    *   If 2 children provide pending paths, we merge them. The new length is the sum. If the sum is $K$, it's complete (0). If $< K$, it's the new pending length. If $> K$, it's impossible.
    *   If 1 child provides a pending path, it becomes the pending path at $u$.
    *   If 0 children provide pending paths, $u$ starts a new path of length 1.
4.  **Final Check**: After processing the root, if `pending[1]` is 0, the decomposition is valid. Otherwise, it's invalid.

Complexity: $O(NK)$ time and space, which fits within the constraints ($NK \le 2 \cdot 10^5$).
