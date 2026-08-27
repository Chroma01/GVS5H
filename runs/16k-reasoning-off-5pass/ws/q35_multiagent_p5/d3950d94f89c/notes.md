
## ideation
The core difficulty lies in efficiently finding the longest path from any ancestor to the current node such that all node values on the path are unique. A naive approach of checking all pairs of ancestors/descendants would be too slow ($O(N^2)$).

The key insight is that for any node `v`, the "longest special path ending at `v`" starts from the nearest ancestor `u` (inclusive) such that the path from `u` to `v` has unique values. If the value at `v` has been seen before in the current root-to-node path, the valid path cannot include the previous occurrence of that value or any ancestors above it.

We can use a DFS traversal. During the traversal, we maintain:
1. The current path from the root to the current node (as a list of nodes or just tracking depth/weight).
2. A dictionary/map `last_occurrence` that maps a value to the depth (or index) of its last occurrence in the current path.
3. A prefix sum array (or just track cumulative distance from root) to quickly calculate the length of any segment of the path.

For each node `u` visited:
- Let `depth[u]` be the cumulative edge length from the root to `u`.
- Let `num_nodes[u]` be the number of nodes from the root to `u` (inclusive).
- Check if `nums[u]` is in `last_occurrence`.
  - If yes, let `prev_depth = last_occurrence[nums[u]]`. The valid path starting point must be strictly below the node at `prev_depth`. So the start node's depth index is `prev_depth + 1`.
  - If no, the valid path can start from the root (index 0).
- The length of the special path ending at `u` is `depth[u] - depth[start_node]`.
- The number of nodes in this path is `num_nodes[u] - num_nodes[start_node] + 1`.
- Update the global maximum length and minimum node count.
- Add `nums[u]` to `last_occurrence` with the current depth index, recurse to children, and then backtrack (remove `nums[u]` from `last_occurrence`).

We need to handle the root carefully. The root has no parent, so its `last_occurrence` is set when we visit it.

Pitfalls:
- The tree is undirected in input, so we must build an adjacency list and use a visited set or parent pointer during DFS to avoid going back up.
- The "start node" logic: if a value repeats, the new path must start after the previous occurrence. We store the *index* (0-based depth) of the node in the current path.
- We need to store cumulative distance from root, not just edge lengths, to compute path lengths quickly.

Complexity: $O(N)$ time since each node is visited once, and dictionary operations are $O(1)$ on average. Space complexity is $O(N)$ for recursion stack and storage.

## worker: (none)
The solution uses a DFS traversal to explore all root-to-leaf paths. During the traversal, it maintains:
1. `last_occurrence`: A dictionary mapping each node value to a tuple `(depth_idx, cum_dist)` representing the last time this value was encountered in the current path. `depth_idx` is the 0-based index of the node in the current root-to-node path, and `cum_dist` is the cumulative edge length from the root to that node.
2. `path_cum_dist`: A list that stores the cumulative distance from the root to each node in the current path, indexed by `depth_idx`. This allows $O(1)$ retrieval of the cumulative distance at any depth index in the current path.

For each node visited:
- If its value has been seen before in the current path at `depth_idx = prev_idx`, then any special path ending at the current node must start after `prev_idx` (i.e., at `prev_idx + 1`) to ensure uniqueness. The length of this path is `cum_dist - path_cum_dist[prev_idx + 1]`, and the number of nodes is `depth_idx - (prev_idx + 1) + 1`.
- If the value has not been seen, the special path can start from the root (depth_idx 0). The length is `cum_dist` (since `path_cum_dist[0] = 0`), and the number of nodes is `depth_idx + 1`.

The global maximum length and minimum node count are updated accordingly. After processing a node and its descendants, the algorithm backtracks by removing the node's value from `last_occurrence` and popping from `path_cum_dist`.

Time Complexity: $O(N)$ because each node is visited once, and dictionary/list operations are $O(1)$ on average.
Space Complexity: $O(N)$ for the recursion stack, `last_occurrence` dictionary, and `path_cum_dist` list.
