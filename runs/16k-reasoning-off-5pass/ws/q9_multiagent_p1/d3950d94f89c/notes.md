
## ideation
**Core Difficulty**:
1.  **Tree Traversal with State**: We need to traverse a tree while maintaining the state of the current path (specifically, the set of values seen so far) to enforce the "unique values" constraint.
2.  **Efficient Backtracking**: Since $N$ is up to $5 \times 10^4$, an $O(N^2)$ solution (re-scanning the path or copying sets) will TLE. We need an approach that allows us to efficiently add/remove nodes from the current path and detect duplicates in $O(1)$ or $O(\log N)$ time.
3.  **Pruning Strategy**: If a duplicate value is encountered, the entire path from the root to the current node is invalid *as a single contiguous path*. However, valid special paths can still exist within the subtree of the current node or by restarting the path at an ancestor of the duplicate. The challenge is to correctly identify where the valid path "restarts" without excessive recomputation.
4.  **Metrics**: We need to track two metrics simultaneously: maximum length and minimum node count for that length.

**Candidate Approaches**:
1.  **DFS with Hash Map + Path Reconstruction (Naive)**:
    *   Maintain a hash map `last_seen` storing `{value: node_index}` for the current recursion stack.
    *   Upon visiting a node, check if `nums[node]` exists in `last_seen`.
    *   If yes, we have a duplicate. The valid path must end before the first occurrence of this value. We need to "cut" the path.
    *   *Pitfall*: Simply cutting isn't enough; we need to continue DFS. But if we cut, how do we manage the `last_seen` map for the remaining ancestors? We might need to pop elements from the map until the duplicate is resolved. This effectively simulates backtracking the path.
    *   *Complexity*: In the worst case (e.g., a line graph with all unique values), we do $O(1)$ work per node. If duplicates are frequent, popping might take time proportional to the depth. However, each node is pushed once and popped once across the entire DFS execution. Total time $O(N)$.

2.  **DFS with Path List and Binary Search (if sorted)**:
    *   Not applicable directly since values aren't sorted by position.

3.  **Two-Pointer / Sliding Window on Tree Path**:
    *   Since it's a tree, a sliding window isn't straightforward like in an array. The "window" is defined by the root of the current special path.
    *   For each node, we want to find the highest ancestor such that the path from that ancestor to the current node has unique values.
    *   We can maintain the `last_seen` map. If `nums[u]` was seen at `v`, then the new valid path starting point for `u` must be `parent(v)` (or `v` itself if we consider the path ending at `v` is invalid, so we start after `v`).
    *   Actually, if we encounter `x` at `u` and `x` was last seen at `v` (where `v` is an ancestor), then any path passing through both `v` and `u` is invalid. The longest valid path ending at `u` must start *after* `v`.
    *   We need to efficiently jump up the tree to find the node just above `v`. This suggests storing `parent` pointers or using the recursion stack.
    *   *Refinement*: During DFS, keep a global `last_seen` map. When entering `u`:
        *   Check if `nums[u]` in `last_seen`.
        *   If yes, let `v = last_seen[nums[u]]`. The current valid path cannot include `v`. We need to "remove" `v` and all nodes between `v` and `u` from our consideration for the *current* path ending at `u`.
        *   Actually, the standard technique for "longest path with unique values in a tree" is:
            1.  Traverse down.
            2.  Maintain a map `last_pos` of `value -> node_index`.
            3.  If `nums[u]` is in `last_pos`, say at `v`, then the path from `v` to `u` is invalid. The longest valid path ending at `u` starts at `child_of(v)`.
            4.  But we need to update the map. We can't just ignore `v`; `v` might be part of a valid path for a *different* value later? No, the map tracks the *current* path from the root of the current special path.
            5.  Correct Logic:
                *   We are building a path from some ancestor `S` to `u`.
                *   We maintain a map `seen` for the current path `S...u`.
                *   When moving to `u`:
                    *   If `nums[u]` in `seen`:
                        *   Let `v` be the node where `nums[v] == nums[u]`.
                        *   The path `S...v...u` is invalid.
                        *   We must restart the path at `parent(v)`.
                        *   So, we need to clear the `seen` map for all nodes from `v` to `u`? No, that's expensive.
                        *   Alternative: The map `seen` should only contain nodes from the *current valid* path. If a duplicate is found, we effectively "prune" the path back to `parent(v)`. This means we remove `v` and everything below it from the `seen` map, and the new `seen` map starts fresh from `parent(v)` upwards?
                        *   Wait, the `seen` map in a recursive DFS naturally represents the path from the root of the current recursion branch. If we find a duplicate, it means the path from the root of the *current* recursion (which might be the global root 0) is invalid.
                        *   However, a special path doesn't have to start at the global root. It can start at any ancestor.
                        *   If `nums[u]` duplicates `nums[v]` (ancestor), then the longest unique path ending at `u` starts at `parent(v)`.
                        *   So, we need to know `parent(v)`.
                        *   Algorithm:
                            1.  DFS(u, parent):
                                2.  Check if `nums[u]` in `path_map`.
                                3.  If yes, let `v = path_map[nums[u]]`.
                                4.  The valid path ending at `u` starts at `parent(v)`.
                                5.  We need to "reset" our tracking for the current path to start from `parent(v)`.
                                6.  This implies we need to remove all nodes from `v` down to `u` from the `path_map`? No, `v` is an ancestor. We need to remove `v` and everything *below* `v` that was added? No, `path_map` contains ancestors.
                                7.  Correct logic with `path_map`:
                                    *   `path_map` stores `{value: node_index}` for the current path from the root of the *current valid segment*.
                                    *   When we go deeper, we add `u`.
                                    *   If duplicate found at `v`:
                                        *   The segment `v...u` is invalid.
                                        *   The new valid segment starts at `parent(v)`.
                                        *   We must remove `v` and all nodes *between* `v` and `u` from `path_map`? No, `path_map` only has ancestors.
                                        *   Actually, if we use a global `path_map` for the current recursion stack (representing path from root 0), finding a duplicate at `v` means the path from 0 to `u` is invalid.
                                        *   But we can start a new path at `parent(v)`.
                                        *   So, we need to effectively "cut" the path at `v`.
                                        *   To do this efficiently: We can store the path in a list and use binary search? Or simply, since it's a tree, we can maintain the `path_map` and when we hit a duplicate at `v`, we pop elements from the `path_map` corresponding to nodes from `v` down to `u`? No, `v` is above `u`.
                                        *   Let's rethink: The `path_map` should represent the path from the *start of the current candidate special path*.
                                        *   When entering `u`:
                                            *   Check `nums[u]` in `path_map`.
                                            *   If present at `v`:
                                                *   The current candidate path must be truncated to start at `parent(v)`.
                                                *   So we need to remove `v` and all nodes *below* `v` that were added to `path_map`? No, `path_map` contains ancestors.
                                                *   We need to remove `v` from `path_map` and also any nodes that were added *after* `v` in the recursion? No, `path_map` is static for the recursion stack.
                                                *   Actually, if we find a duplicate at `v`, it means the path `start...v...u` has a duplicate. The longest unique path ending at `u` is `parent(v)...u`.
                                                *   So we need to update the `path_map` to reflect the path starting at `parent(v)`.
                                                *   This requires removing `v` and all nodes *between* `v` and `u`? No, `path_map` only has ancestors. The nodes between `v` and `u` are descendants of `v` and ancestors of `u`. They are in the recursion stack.
                                                *   This suggests we need to maintain the path explicitly or use a "rollback" mechanism.
                                                *   **Optimal Approach**: Use a global `last_seen` map. When visiting `u`:
                                                    *   If `nums[u]` in `last_seen` (say at `v`):
                                                        *   The path from `v` to `u` is invalid.
                                                        *   We need to "reset" the current path to start at `parent(v)`.
                                                        *   To do this, we need to remove `v` and all nodes *below* `v` from our tracking? No, we need to remove `v` and all nodes *in the current path that are descendants of `v`*? No, `last_seen` tracks ancestors.
                                                        *   Actually, if we encounter a duplicate, it means the path from the root (or current start) to `u` is invalid.
                                                        *   We can simply "pop" the path from `v` to `u`? No, `v` is an ancestor.
                                                        *   Correct logic:
                                                            *   Maintain `last_seen` map for the current path from the root.
                                                            *   When `nums[u]` is seen at `v`:
                                                                *   The valid path ending at `u` starts at `parent(v)`.
                                                                *   We need to remove `v` and all nodes *between* `v` and `u` from the `last_seen` map? No, `last_seen` contains `v` and nodes above it. It does NOT contain nodes between `v` and `u` (because those are descendants of `v` and we haven't reached them yet? Wait, we are at `u`, so we have passed `v` and added nodes in between).
                                                                *   Yes! The nodes between `v` and `u` are in the recursion stack and thus in `last_seen`.
                                                                *   So, if `nums[u]` duplicates `nums[v]`, we must remove `v` and all nodes *below* `v` (up to `u`) from `last_seen`.
                                                                *   But `last_seen` is a hash map. We can't efficiently remove a range of nodes by index unless we store the path in a list and iterate.
                                                                *   **Solution**: Maintain a list `path_nodes` and a map `last_seen`.
                                                                *   DFS(u):
                                                                    *   If `nums[u]` in `last_seen`:
                                                                        *   Let `v = last_seen[nums[u]]`.
                                                                        *   We need to truncate the path at `v`.
                                                                        *   Remove `v` and all nodes after `v` from `path_nodes` and `last_seen`.
                                                                        *   The new path starts at `parent(v)`.
                                                                        *   Update `path_nodes` to keep only nodes up to `parent(v)`.
                                                                        *   Update `last_seen` to only contain nodes up to `parent(v)`.
                                                                    *   Add `u` to `path_nodes` and `last_seen`.
                                                                    *   Update global max/min.
                                                                    *   Recurse.
                                                                    *   Backtrack: Remove `u`.
                                                                *   Complexity: In the worst case, we might pop many nodes. But each node is added once and popped once. Total time $O(N)$.
