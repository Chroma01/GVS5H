
## ideation
The core difficulty lies in efficiently tracking the "valid" start node for a special path ending at each node during a DFS traversal. A special path requires all node values on the path to be unique. As we traverse down the tree from the root, we maintain the current path from the root to the current node. For any node `v` in this path, the longest special path ending at `v` starts at the deepest ancestor `u` such that all nodes on the path from `u` to `v` have unique values.

To solve this:
1.  **Tree Construction & Rooting**: Build an adjacency list. Since the input is an undirected tree but rooted at 0, we need to establish parent-child relationships. We can do this with a BFS or DFS starting from node 0 to build a directed tree structure (or simply use the adjacency list and avoid going back to the parent during DFS).
2.  **Distance Calculation**: Precompute or compute on-the-fly the distance from the root to each node. Let `dist[v]` be the sum of edge lengths from root to `v`. The length of a path from ancestor `u` to descendant `v` is `dist[v] - dist[u]`.
3.  **Tracking Unique Values**: During DFS, maintain a dictionary `last_occurrence` that maps each number value to the depth (or node index in the current root-to-node path) where it was last seen. Also, maintain a list `path_nodes` to store the nodes on the current path from root to current node, which allows us to retrieve the actual node at a given depth if needed (though we mainly need the depth to calculate the number of nodes).
4.  **Finding Valid Start**: For the current node `v` at depth `d` with value `val = nums[v]`:
    -   The previous occurrence of `val` is at depth `prev_depth = last_occurrence.get(val, -1)`.
    -   The earliest valid start depth for a special path ending at `v` is `start_depth = prev_depth + 1`. If `start_depth < 0`, it means `val` hasn't been seen, so `start_depth = 0`.
    -   The node at `start_depth` is the start of the longest special path ending at `v`.
    -   The length of this path is `dist[v] - dist[node_at_start_depth]`.
    -   The number of nodes in this path is `d - start_depth + 1`.
5.  **Backtracking**: After visiting all children of the current node, we must remove the current node's value from `last_occurrence` (or restore its previous value) to backtrack correctly for other branches. This is crucial because the `last_occurrence` map is specific to the current root-to-node path.

Pitfalls to avoid:
-   Not properly backtracking the `last_occurrence` dictionary, which would lead to incorrect results for sibling subtrees.
-   Confusing edge length with number of nodes. The problem asks for the longest path by edge length, but the second result is the minimum number of nodes among those longest paths.
-   Incorrectly calculating the start depth. The start node must be an ancestor, and the path from start to current must have unique values. The condition `start_depth = last_occurrence.get(val, -1) + 1` ensures that the value at `start_depth` is not the same as the current value (if it exists), and all values between `start_depth` and current are unique because we are traversing a single path from root and only the most recent occurrence matters for uniqueness constraint relative to the current node.

## worker: (none)
The solution uses a recursive DFS traversal from the root (node 0). During the traversal, it maintains:
1. `dist`: The cumulative distance from the root to the current node.
2. `path_nodes`: A list representing the current path from the root to the current node.
3. `last_occurrence`: A dictionary mapping each number value to the depth index in `path_nodes` where it was last seen.

For each node visited:
- The earliest valid start depth for a special path ending at the current node is determined by `last_occurrence.get(nums[node], -1) + 1`. This ensures that all values from the start node to the current node are unique.
- The length of the special path is `dist[current] - dist[start_node]`.
- The number of nodes in the path is `current_depth - start_depth + 1`.
- We update the global maximum length and minimum node count accordingly.
- Before recursing into children, we update `last_occurrence` and `path_nodes`. After returning from children, we backtrack by restoring `last_occurrence` to its previous state and removing the current node from `path_nodes`.

This approach efficiently tracks the longest special path ending at each node in O(1) per node (amortized) with O(n) space for the recursion stack and auxiliary data structures.
