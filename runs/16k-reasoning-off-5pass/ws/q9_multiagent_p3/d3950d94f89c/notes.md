
## ideation
**Core Difficulty**:
The problem requires finding the longest "special path" (downward, unique values) in a tree. The constraints are $N \le 5 \times 10^4$, which suggests an $O(N \log N)$ or $O(N)$ solution. A naive DFS that checks every path would be $O(N^2)$ in the worst case (e.g., a line graph), which will TLE. The key challenge is efficiently handling the "unique values" constraint and pruning invalid paths without re-scanning from the root every time a duplicate is found.

**Candidate Approaches**:
1.  **DFS with Backtracking + Set**:
    *   Traverse down the tree. Maintain a set of values on the current path.
    *   If `nums[child]` is in the set, we must remove nodes from the current path until the duplicate is gone.
    *   *Optimization*: Instead of a raw set, use a list or a hash map to store the *depth* (or index) of each value. When a duplicate `val` is found at current depth `d`, we know the previous occurrence was at depth `prev_d`. The valid path must start *after* `prev_d`. We can "jump" our recursion state to `prev_d + 1` effectively.
    *   Since we need to calculate lengths and node counts, we can pass the accumulated length and node count from the parent. If we jump, we reset the accumulator based on the stored state at `prev_d`.

2.  **Heavy-Light Decomposition (HLD) / LCA**:
    *   Overkill for this specific "downward path" constraint. HLD is great for arbitrary paths, but here the path direction is fixed (ancestor to descendant). Simple DFS with state jumping is more direct.

3.  **Map-based State Jumping (Selected Approach)**:
    *   Use a global (or thread-local) map `last_seen[value]` storing the `(depth, accumulated_length, node_count)` of the most recent occurrence of `value` on the current path.
    *   DFS function `dfs(u, current_depth, current_len, current_nodes)`:
        *   Check if `nums[u]` exists in `last_seen`.
        *   If yes, let `(prev_depth, prev_len, prev_nodes) = last_seen[nums[u]]`.
        *   The new state for `u` becomes:
            *   `new_depth = prev_depth + 1`
            *   `new_len = prev_len + edge_weight_to_u` (Wait, if we jump, we treat the path as starting from the child of the previous occurrence. So the length accumulated so far is `prev_len` + weight to `u`? No. The path *ends* at `u`. The path starts at `prev_depth + 1`. The length of the path from `prev_depth+1` to `u` is `current_len - prev_len`? No, `current_len` includes the path from root to `u`. If we truncate the path to start after `prev_depth`, the new length is `current_len - (distance from root to node at prev_depth)`. But we don't store distance from root easily if we just store accumulated length of the *current* path.
        *   *Refinement*: Let's store `(depth, path_length_from_root, node_count_from_root)` for each value.
        *   When visiting `u` with `val`:
            *   If `val` seen at `prev_depth`:
                *   The valid path ending at `u` must start at `prev_depth + 1`.
                *   `new_path_len = path_len_from_root[u] - path_len_from_root[prev_node]`? No, `path_len_from_root` is sum of edge weights.
                *   Actually, simpler: Just store the state `(depth, accumulated_len, node_count)` for the path *ending* at the previous occurrence.
                *   If duplicate found: The longest valid path ending at `u` that respects uniqueness is the path starting from `prev_node`'s child to `u`.
                *   `current_len = stored_len + weight(u)`. Wait, `stored_len` is the length of the path from root to `prev_node`. The path from `prev_node`'s child to `u` has length `stored_len + weight(u) - (length to prev_node)`. This is getting confusing.
    *   *Simpler State Logic*:
        *   Pass `current_len` and `current_nodes` down the recursion.
        *   If duplicate `val` found at `prev_depth`:
            *   We discard everything from root to `prev_depth`.
            *   The new `current_len` becomes `stored_len_at_prev + weight(u)`. (Where `stored_len_at_prev` is the length of the path from root to `prev_node`).
            *   The new `current_nodes` becomes `stored_nodes_at_prev + 1`.
            *   Update `last_seen[val] = (current_depth, current_len, current_nodes)`.
        *   If no duplicate:
            *   `current_len += weight(u)`
            *   `current_nodes += 1`
            *   Update `last_seen[val]`.
        *   *Correction*: The `stored_len` in the map should represent the length of the path from the root to the node where the value was last seen.
        *   When we encounter `val` again at `u`:
            *   The valid path starts at `child_of_prev_node`.
            *   Length of path from `child_of_prev_node` to `u` = `(Length to u) - (Length to prev_node)`.
            *   But we are building the path incrementally.
            *   Let's store `(depth, length_from_root, node_count_from_root)` for each value.
            *   At `u` (value `v`):
                *   If `v` in map at `prev_depth`:
                    *   `effective_len = length_from_root[u] - length_from_root[prev_node]`
                    *   `effective_nodes = (depth[u] - depth[prev_node])`
                    *   Update global max with `effective_len`.
                *   Update map: `map[v] = (depth[u], length_from_root[u], node_count_from_root[u])`.
    *   This approach is $O(N)$ because each node is visited once, and map operations are $O(1)$ (or $O(\log N)$ with tree map, but values are integers up to $5 \times 10^4$, so array/hash map is fine).

## worker: finalize
The solution uses a Depth-First Search (DFS) to traverse the tree. To efficiently handle the "unique values" constraint and avoid $O(N^2)$ complexity, we maintain a global dictionary `last_seen` that maps each node value to its state (depth, distance from root, node count from root) on the *current* path from the root.

Key optimizations:
1.  **State Jumping**: When a duplicate value is encountered at node `u` (value `v`), we check `last_seen[v]`. If it exists, it points to the most recent ancestor `prev` with the same value. The longest valid special path ending at `u` must start immediately after `prev`. The length of this path is calculated as `dist[u] - dist[prev]`, and the node count is `depth[u] - depth[prev]`.
2.  **Backtracking**: Since the `last_seen` dictionary is shared across all branches, we must ensure that when we backtrack from a node `u`, the dictionary reflects the state of the path *before* visiting `u`. We do this by storing the previous state of `last_seen[v]` before updating it with `u`, and then restoring it after the recursive calls return. This ensures that if we move to a different branch, the `last_seen` map only contains values from the ancestors common to that new branch.
3.  **Complexity**: Each node is visited once. Dictionary operations are $O(1)$ on average. Thus, the time complexity is $O(N)$ and space complexity is $O(N)$ for the recursion stack and the dictionary.
