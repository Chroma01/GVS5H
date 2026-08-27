
## ideation
The core difficulty lies in efficiently tracking the "valid" downward paths from any ancestor to the current node such that all node values on the path are unique. A naive approach of checking all ancestors for each node would be $O(N^2)$, which is too slow for $N=5 \times 10^4$.

The key insight is that for a fixed current node, the longest special path ending at this node starts from the deepest ancestor such that the path from that ancestor to the current node has unique values. This is equivalent to finding the nearest ancestor (closest to the current node) that has the same value as the current node. Let's call this ancestor `dup_ancestor`. Then the valid path starts from the child of `dup_ancestor` that is on the path to the current node. If no such duplicate exists, the path starts from the root.

To implement this efficiently during a DFS:
1. Maintain a global dictionary `last_seen` that maps a value to the depth (or node index) of the most recent occurrence of that value on the current root-to-node path.
2. Maintain the current distance from the root to the current node (`curr_dist`).
3. When visiting a node `u` with value `val`:
   - Record the previous depth of `val` (if any) in `last_seen`. Let this be `prev_depth`.
   - Update `last_seen[val]` to the current depth.
   - The start of the valid special path ending at `u` is determined by `prev_depth`. Specifically, the path starts from the node at depth `prev_depth + 1` (if `prev_depth` exists) or from the root (depth 0) if `prev_depth` does not exist.
   - The length of the special path ending at `u` is `curr_dist - dist_to_start_node`. Note: `dist_to_start_node` is the distance from root to the start node. If the start node is the child of `dup_ancestor`, then `dist_to_start_node = dist_to_dup_ancestor + edge_length_to_child`. But it's easier to think in terms of depths and cumulative distances.
   
Actually, a simpler way:
- Keep track of the cumulative distance from the root to the current node: `dist[u]`.
- For each value `v`, store the cumulative distance to the last seen node with value `v` on the current path: `last_dist[v]`.
- When at node `u` with value `val`:
  - The nearest ancestor with value `val` is stored in `last_dist[val]` (if it exists). Let this distance be `d_prev`.
  - The special path ending at `u` must start after that ancestor. So the length of the path is `dist[u] - d_prev` if `d_prev` exists, otherwise `dist[u]` (path from root).
  - But wait: the path must include the start node. The start node is the child of the duplicate ancestor. So the length is `dist[u] - dist[child_of_dup]`. And `dist[child_of_dup] = d_prev + edge_length_from_dup_to_child`.
  - Actually, we can store the depth (number of edges from root) and the cumulative distance separately. Or just store the cumulative distance to the node itself.
  
Let's refine:
- `dist[u]`: cumulative distance from root to `u`.
- `last_dist[val]`: cumulative distance to the last node with value `val` on the current path.
- When processing `u`:
  - Save `old_dist = last_dist.get(val, -1)`
  - `last_dist[val] = dist[u]`
  - If `old_dist == -1`, the path starts at root, so path length = `dist[u]`, node count = depth[u] + 1.
  - Else, the path starts from the child of the node at `old_dist`. But we don't have the edge length from that node to its child directly in `last_dist`. 
  - Instead, store the depth (index in the path from root) of the last occurrence. Let `last_depth[val]` be the depth (0-indexed, root at 0) of the last node with value `val`.
  - Then the start node is at depth `last_depth[val] + 1`. The cumulative distance to the start node is not directly available unless we store it.
  
Alternative: Store the cumulative distance to the node at the time it was last seen. But when we backtrack, we need to restore the previous value.
  
Better approach:
- During DFS, maintain `last_pos[val]` = the depth (integer, root=0) of the last occurrence of `val` on the current path.
- Also maintain `depth_dist[d]` = cumulative distance from root to the node at depth `d` on the current path. But this is tricky because different branches have different distances.
  
Actually, we can compute the path length as:
`path_length = dist[u] - dist[start_node]`
where `start_node` is the child of the duplicate ancestor.
We can store `last_node[val]` = the node index of the last occurrence of `val` on the current path.
Then, when at `u`, if `val` was seen before at `prev_node`, then the start node is the child of `prev_node` on the path to `u`. We don't know which child it is without storing parent pointers or edge weights.

Revised plan:
- Do DFS from root.
- Maintain `last_seen[val]` = the depth (0-indexed) of the last node with value `val` on the current root-to-node path.
- Maintain `cum_dist` as the cumulative distance from root to current node.
- Also, maintain an array `dist_from_root` for the current path? No, because it's a tree, not a line.
- Instead, for each node, we can store its depth and cumulative distance from root in the DFS state.
- When we enter a node `u` with value `val`:
  - `prev_depth = last_seen.get(val, -1)`
  - `last_seen[val] = current_depth`
  - If `prev_depth == -1`, the special path starts at root. Length = `cum_dist`, nodes = `current_depth + 1`.
  - Else, the special path starts at the child of the node at `prev_depth` that is an ancestor of `u`. The length of the path is `cum_dist - dist_to_start_node`. We need `dist_to_start_node`.
  
To get `dist_to_start_node`, we can store `node_dist[node_index]` = cumulative distance from root to `node_index`. This can be computed during DFS.
Then, if `prev_depth` exists, let `prev_node` be the node at `prev_depth` on the current path. But we don't have a direct mapping from depth to node index in the current path easily without storing it.

Actually, we can store `path_nodes` as a list during DFS. Then `path_nodes[prev_depth]` is the duplicate ancestor. Then the start node is the child of `path_nodes[prev_depth]` that is on the path to `u`. But we don't know which child it is.

Simpler: The length of the special path ending at `u` is `cum_dist[u] - cum_dist[prev_node] - edge_length(prev_node, start_node)`. This is messy.

Best approach:
- For each node, the longest special path ending at that node is determined by the nearest ancestor with the same value.
- Let `dup_node` be the nearest ancestor of `u` (including `u` itself? No, excluding `u` for the start) with the same value as `u`. Actually, the path can start at `u` (length 0).
- The path starts from the child of `dup_node` that is on the path to `u`. Let this child be `s`.
- Then length = `dist[u] - dist[s]`.
- We can find `s` if we store the parent and the edge weight from parent to child for each node. But we need the nearest ancestor with duplicate value.

We can use a stack for each value: `stack[val]` stores the nodes with value `val` on the current path, in order from root to current.
When at `u` with value `val`:
- If `stack[val]` is not empty, the top is the nearest ancestor with value `val`. Let this be `dup_node`.
- The start node `s` is the child of `dup_node` on the path to `u`. We can find `s` by storing the parent pointer and then traversing up? No, that's slow.

Actually, we can store for each node, the cumulative distance from root. And we can store the parent of each node.
But to find the child of `dup_node` that is on the path to `u`, we can note that this child is the next node after `dup_node` on the path. We can store the path as a list of nodes during DFS. Then `path[depth_of_dup_node + 1]` is the start node.

So:
- Maintain `path` as a list of nodes from root to current.
- Maintain `last_seen[val]` = the index in `path` where `val` was last seen.
- When at `u` (at index `k` in `path`):
  - `prev_idx = last_seen.get(val, -1)`
  - `last_seen[val] = k`
  - If `prev_idx == -1`, start node is `path[0]`, length = `dist[u]`, nodes = `k+1`.
  - Else, start node is `path[prev_idx + 1]`, length = `dist[u] - dist[start_node]`, nodes = `k - prev_idx`.
  - Update global max length and min nodes.
- Backtrack: remove `val` from `last_seen`? No, because there might be multiple occurrences. We need to restore the previous value. So store `old_val = last_seen.get(val, -1)` and after DFS, set `last_seen[val] = old_val`.

This approach is $O(N)$ because each node is processed once and dictionary operations are $O(1)$.

Pitfalls:
- Need to handle the case where the path starts at the current node (length 0). This is covered when `prev_idx == k-1`? No, if the parent has the same value, then `prev_idx = k-1`, start node is `path[k]`, which is `u`, length 0, nodes 1. Correct.
- Need to compute cumulative distances from root. Can do this during DFS.

Steps:
1. Build adjacency list from edges. Since it's a tree rooted at 0, we can do BFS/DFS to build parent pointers and cumulative distances, or do it during the main DFS.
2. In DFS, maintain `path` list, `last_seen` dict, `global_max_len`, `global_min_nodes`.
3. For each node, compute `dist` from root.
4. Update results.

Let's implement this.

## worker: Build an adjacency list representation of the tree
The solution uses a DFS traversal from the root (node 0). During the traversal, it maintains:
1. `path`: a list of nodes from the root to the current node.
2. `path_cum_dist`: a list of cumulative distances from the root to each node in `path`.
3. `last_seen`: a dictionary mapping each value to the depth (index in `path`) of its last occurrence on the current root-to-node path.

For each node `u` with value `val`:
- The nearest ancestor with the same value is found at `last_seen[val]` (if it exists).
- If no duplicate exists (`prev_idx == -1`), the special path starts at the root, so the length is the cumulative distance to `u` and the node count is `depth + 1`.
- If a duplicate exists at `prev_idx`, the special path starts at the child of the duplicate ancestor, which is at index `prev_idx + 1` in `path`. The length is `cum_dist[u] - cum_dist[start_node]` and the node count is `depth - prev_idx`.

The global maximum length and minimum node count are updated accordingly. Backtracking restores the state of `last_seen`, `path`, and `path_cum_dist`.

Time Complexity: $O(N)$ where $N$ is the number of nodes, as each node is visited once and dictionary operations are $O(1)$ on average.
Space Complexity: $O(N)$ for the recursion stack and auxiliary data structures.
