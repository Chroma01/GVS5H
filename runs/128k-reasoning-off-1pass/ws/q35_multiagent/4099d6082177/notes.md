
## ideation
The core difficulty lies in efficiently verifying if a tree can be partitioned into disjoint paths of length $K$. A naive simulation might be too slow or complex to implement correctly with general tree structures. The key insight is to use a greedy bottom-up approach (post-order traversal).

1.  **Leaf Processing**: We can think of "peeling" the tree from the leaves. Each leaf starts a path segment. As we move up, we extend these segments.
2.  **State at Node**: For each node $u$, we need to know the length of the path segment ending at $u$ that comes from its subtree. Let's call this `len[u]`. Initially, for leaves, `len[u] = 0` (representing a path of 1 vertex so far, or distance 0 from the leaf).
3.  **Merging**: When processing node $u$, we look at the `len` values from its children.
    *   If a child $v$ has `len[v] == K-1`, it means the path from $v$'s subtree has reached length $K$ (since it includes the edge $u-v$). This path is complete and removed.
    *   Otherwise, the path segment from child $v$ extends to $u$. The new length at $u$ from this branch is `len[v] + 1`.
    *   Node $u$ can connect at most two such segments (one from each side) to form a single continuous path passing through $u$. If $u$ has more than one child providing an active segment (i.e., `len[v] < K-1`), we must combine them.
    *   Specifically, if $u$ has multiple active segments from children, we can merge at most two. If there are more than two active segments, it's impossible because $u$ can only belong to one path and have at most 2 neighbors in that path (unless it's an endpoint, but even then, it can only start/end one path). Wait, if $u$ is an internal node of a path, it has 2 neighbors. If it's an endpoint, it has 1. So, $u$ can accept at most 2 incoming path segments from its children. If it has >2 children with pending paths, we fail.
    *   If it has 0 children with pending paths, `len[u] = 0`.
    *   If it has 1 child with pending path of length $L$, `len[u] = L + 1`.
    *   If it has 2 children with pending paths of lengths $L_1, L_2$, we can form a path through $u$ of length $L_1 + L_2 + 1$. This new path segment ends at $u$ (going upwards). So `len[u] = L_1 + L_2 + 1`. If this sum equals $K$, the path is complete and removed (so `len[u]` effectively becomes "removed", or we can treat it as -1 or similar). If it exceeds $K$, it's invalid.
    *   Actually, a simpler state: `len[u]` represents the length of the path segment ending at $u$ that is *not yet completed*. If a path completes at $u$ (length $K$), it is removed and doesn't propagate up.
    *   So, for node $u$:
        *   Collect `len[v] + 1` for all children $v$ where `len[v] != -1` (removed) and `len[v] + 1 < K`. If `len[v] + 1 == K`, the path is complete, ignore.
        *   Let the collected lengths be $S$.
        *   If $|S| > 2$, return False.
        *   If $|S| == 0$, `len[u] = 0`.
        *   If $|S| == 1$, `len[u] = S[0]`.
        *   If $|S| == 2$, let $a, b = S$. New length is $a + b + 1$? No, the segments are from different branches. The path goes from one branch, through $u$, to the other. The length of the path segment ending at $u$ (going up) is $a + b + 1$? No. The path segment *ending* at $u$ from the combined branches has length $a + b + 1$ only if we consider the whole thing. But we are tracking the length of the path *ending* at $u$ to be extended upwards. If we merge two paths of length $a$ and $b$ at $u$, the new path has length $a + b + 1$. If this equals $K$, it's complete. If it's $< K$, `len[u] = a + b + 1`. If $> K$, fail.
        *   Wait, the definition of `len[u]` is the number of edges in the path segment ending at $u$ coming from the subtree. So if a leaf has `len=0`, it's 1 vertex. If we add an edge, length becomes 1 (2 vertices).
        *   So, if child $v$ has `len[v]`, the path from $v$ to $u$ has length `len[v] + 1`.
        *   If we merge two such paths with lengths $L_1, L_2$ at $u$, the new path has length $L_1 + L_2 + 1$.
        *   If this new length is $K$, the path is complete. `len[u]` is effectively "done".
        *   If this new length is $< K$, `len[u] = L_1 + L_2 + 1`.
        *   If this new length is $> K$, fail.

4.  **Root Check**: After processing the root, if `len[root] == 0` (meaning the root is part of a completed path or is a single node path of length 0 which is valid if $K=1$), or if `len[root]` is "done", then Yes. If `len[root] > 0`, it means there's an incomplete path, so No.

5.  **Pitfalls**:
    *   $K=1$: Always Yes.
    *   Rooting the tree: Arbitrarily pick root 1.
    *   Handling the "removed" state: Use -1 or a separate flag.
    *   Degree constraints: The logic above handles it by checking if $|S| > 2$.

## worker: (omitted)
The solution uses a greedy bottom-up approach on the tree.
1.  **Rooting**: We arbitrarily root the tree at vertex 1.
2.  **Post-order Traversal**: We process nodes from leaves up to the root. This allows us to determine the state of path segments ending at each node based on its children.
3.  **State Representation**: `path_len[u]` represents the length (number of edges) of the path segment ending at `u` that extends upwards from `u`'s subtree.
    *   If `path_len[u] == -1`, the path segment ending at `u` has reached length `K` and is considered "completed/removed".
    *   If `path_len[u] == L` (where $0 \le L < K$), it means there is a path of $L+1$ vertices ending at `u`, with the last vertex being `u`. This path can be extended upwards.
4.  **Merging Logic**:
    *   For each node `u`, we look at its children.
    *   If a child `v` has a completed path (`path_len[v] == -1`), it contributes nothing.
    *   If a child `v` has an active path of length `L_v`, it contributes a segment of length `L_v + 1` to `u`.
    *   If this new length equals `K`, the path is completed at `u` and removed.
    *   If this new length is less than `K`, it's an "active segment" that needs to be handled by `u`.
    *   Node `u` can connect at most two such active segments (one from each side) to form a single continuous path passing through `u`. If there are more than two active segments, it's impossible because `u` can only belong to one path (degree constraint within the path decomposition).
    *   If there are 0 active segments, `u` starts a new path of length 0.
    *   If there is 1 active segment of length `L`, `u` extends it to length `L+1`.
    *   If there are 2 active segments of lengths `L1` and `L2`, they are merged through `u` to form a path of length `L1 + L2 + 1`. If this equals `K`, it's completed. If less, `u` now has a path of that length ending at it. If more, it's invalid.
5.  **Final Check**: After processing the root, if `path_len[root]` is not `-1`, it means there's an incomplete path, so the answer is "No". Otherwise, "Yes".
6.  **Edge Case**: If $K=1$, every vertex is a path of length 0, so the answer is always "Yes".
