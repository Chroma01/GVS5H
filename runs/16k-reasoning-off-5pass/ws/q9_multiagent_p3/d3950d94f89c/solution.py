from typing import List

class Solution:
    def longestSpecialPath(self, edges: List[List[int]], nums: List[int]) -> List[int]:
        n = len(nums)
        if n == 0:
            return [0, 0]
        
        # Build adjacency list: node -> list of (neighbor, weight)
        adj = [[] for _ in range(n)]
        for u, v, w in edges:
            adj[u].append((v, w))
            adj[v].append((u, w))
            
        # To handle the tree structure rooted at 0, we need to determine children.
        # We can do a BFS/DFS to establish parent-child relationships or simply
        # pass the parent in the recursive DFS to avoid going back up.
        
        # Global variables to track the best result
        max_len = 0
        min_nodes = 1
        
        # Map to store the last seen state for each value: value -> (depth, dist_from_root, nodes_from_root)
        # depth: number of nodes from root to current node (inclusive)
        # dist_from_root: sum of edge weights from root to current node
        # nodes_from_root: number of nodes from root to current node (same as depth)
        last_seen = {}
        
        # We need to know the parent to avoid traversing back up the tree.
        # We can precompute the tree structure (children only) or pass parent in DFS.
        # Passing parent is simpler and O(N).
        
        def dfs(u: int, p: int, current_depth: int, current_dist: int, current_nodes: int):
            nonlocal max_len, min_nodes
            
            val = nums[u]
            
            # Check if this value has been seen on the current path
            if val in last_seen:
                prev_depth, prev_dist, prev_nodes = last_seen[val]
                
                # The valid path must start after the previous occurrence.
                # The path starts at the child of the node where 'val' was last seen.
                # So the length of the valid path ending at u is:
                # (dist to u) - (dist to prev node)
                valid_len = current_dist - prev_dist
                valid_nodes = current_nodes - prev_nodes
                
                # Update global maximums
                if valid_len > max_len:
                    max_len = valid_len
                    min_nodes = valid_nodes
                elif valid_len == max_len:
                    min_nodes = min(min_nodes, valid_nodes)
            
            # Update the last seen state for this value
            # We store the state *including* the current node u
            last_seen[val] = (current_depth, current_dist, current_nodes)
            
            # Explore children
            for v, w in adj[u]:
                if v != p:
                    # Recurse
                    # New depth = current_depth + 1
                    # New dist = current_dist + w
                    # New nodes = current_nodes + 1
                    dfs(v, u, current_depth + 1, current_dist + w, current_nodes + 1)
            
            # Note: We do NOT remove the entry from last_seen here because
            # the problem defines a "special path" as a downward path.
            # If we encounter the same value again deeper in the tree,
            # the path must start after the *most recent* occurrence of that value
            # on the current downward path. Since we are traversing downward,
            # the "current path" context is maintained by the recursion stack.
            # However, if we backtrack, we are leaving the subtree.
            # Does the "last_seen" map need to be cleared?
            # Actually, the logic holds: if we go down a different branch later,
            # we might encounter the same value. The "path" is defined by the recursion stack.
            # But wait, the map `last_seen` is shared across all branches.
            # If we visit node A (val X), then go to child B (val Y), then child C (val X).
            # The path A->B->C is invalid because X repeats.
            # The valid path ending at C is just C (if C's value is unique in the path).
            # But if we backtrack from C, go to another child D (val Z), then child E (val X).
            # The path from root to E might not include A.
            # The issue is that `last_seen` stores the state from the *root* of the current DFS traversal.
            # If we backtrack, we are effectively starting a new path from the parent.
            # The "path" in the problem is a downward path from *an ancestor* to a *descendant*.
            # It does NOT have to start at the root.
            # My logic: `valid_len = current_dist - prev_dist`. This calculates the length of the path
            # starting from the child of the previous occurrence of `val` up to `u`.
            # This is correct regardless of whether the path starts at the root or not.
            # The only catch is: if we backtrack, the `current_dist` and `current_nodes` passed to children
            # are based on the path from the root.
            # When we encounter a duplicate `val` at `u`, we calculate the length of the segment
            # between the previous `val` and `u`. This segment is a valid special path.
            # Is it possible that a valid special path exists that starts *before* the previous `val`?
            # No, because that would include the duplicate `val`.
            # Is it possible that a valid special path exists that starts *after* the previous `val`
            # but ends at `u`? Yes, that's what we calculated.
            # Is it possible that we need to "forget" the previous `val` when backtracking?
            # No, because the map `last_seen` is keyed by value. If we encounter `val` again in a different branch,
            # it means the path from the root to the new `u` contains `val` at the previous location.
            # Wait, if we backtrack, the path from root to the new `u` does NOT contain the previous `val`
            # if the previous `val` was in a different branch that we already finished.
            # BUT, the `last_seen` map is global.
            # Example:
            # Root(0) -> A(1) -> B(2)
            # Root(0) -> C(1) -> D(2)
            # DFS:
            # 1. Visit Root(0). last_seen[0] = (1, 0, 1)
            # 2. Visit A(1). last_seen[1] = (2, w, 2)
            # 3. Visit B(2). last_seen[2] = (3, w+w, 3)
            # Backtrack to A.
            # 4. Visit C(1). 
            #    Here, `last_seen[1]` exists (from A).
            #    But the path from Root to C does NOT include A.
            #    So treating A as an ancestor of C is WRONG.
            #
            # Correction: The `last_seen` map must only reflect values on the *current* path from the root.
            # When we backtrack, we should remove the current node's value from `last_seen`.
            # This ensures that when we explore a new branch, the map only contains values from the ancestors
            # of the current node in the new branch.
            
            # So, we need to pop from `last_seen` after returning from the recursive calls.
            # However, `last_seen` is a dict. We can't easily "pop" if multiple nodes have the same value
            # on the current path? No, on a valid path (which we maintain by pruning), values are unique.
            # But wait, we are traversing the whole tree. The path from root to current node might have duplicates?
            # No, if we encounter a duplicate, we calculate the valid segment and then... what?
            # If we encounter a duplicate at `u`, the path from root to `u` is invalid.
            # But the path from `child_of_prev` to `u` is valid.
            # Do we continue traversing from `u`? Yes.
            # Do we keep `val` in `last_seen`?
            # If we keep it, and we go deeper, say to `v`, and `v` has value `X`.
            # If `X` was seen before `u` on the path, we handle it.
            # If `X` was seen at `u` (value `val`), then we handle it.
            # The issue is the "different branch" problem.
            # If we backtrack from `u`, we go to another child of `parent`.
            # The path from root to the new child does NOT include `u`.
            # So we MUST remove `u`'s value from `last_seen` when backtracking.
            # But what if `u` had a duplicate earlier?
            # Example: Root(0) -> A(1) -> B(1).
            # At B, we see 1. We calculate valid path A->B (length w).
            # We update `last_seen[1]` to B.
            # Then we backtrack to A. We should remove A's 1?
            # If we remove A's 1, then `last_seen[1]` still has B.
            # Then we go to C(1). Path Root->C.
            # `last_seen[1]` has B. But B is not an ancestor of C.
            # So we must remove B as well?
            # Yes. When backtracking from a node `u`, we must remove `nums[u]` from `last_seen`.
            # But wait, if `nums[u]` appeared multiple times on the path?
            # On a valid path (unique values), it appears once.
            # But we are traversing the tree. The path from root to `u` might have duplicates?
            # No, if we define the "current path" as the sequence of nodes visited from root to `u`
            # without skipping, then yes, it could have duplicates if we didn't prune.
            # But the problem says "special path" must have unique values.
            # It doesn't say the path from root to `u` must be special.
            # However, for the purpose of the algorithm:
            # We are looking for ANY downward path.
            # The "current path" in the DFS is the path from root to `u`.
            # If this path has duplicates, then `last_seen` contains entries for all of them.
            # When we backtrack, we are leaving the subtree. The path from root to any node in the new subtree
            # will NOT include the nodes in the old subtree.
            # Therefore, we must remove ALL entries corresponding to the nodes in the old subtree from `last_seen`.
            # But we don't store which nodes are in the subtree.
            # Alternative approach:
            # Instead of a global map, pass the map down the recursion?
            # That would be O(N) space per recursion depth -> O(N^2) space/time. Too slow.
            #
            # Let's rethink the "different branch" issue.
            # The condition "path from root to u does not include A" is true.
            # But `last_seen` is global.
            # The solution is: `last_seen` should only store values from the *current* path from root.
            # When we backtrack, we remove the current node's value.
            # But what if the current node's value was already in `last_seen` from an ancestor?
            # That means the path from root to `u` has a duplicate.
            # In that case, the "current path" is invalid.
            # But we still need to traverse.
            # If we encounter a duplicate at `u`, say `val` was seen at `prev`.
            # The valid path ends at `u` and starts after `prev`.
            # For the purpose of extending the path further down from `u`, we should update `last_seen[val]` to `u`.
            # Why? Because if we go to a child `v` of `u`, and `v` has value `val`,
            # the path from `u` to `v` is invalid. The valid path would be just `v` (if `v`'s value is unique in the path starting after `prev`).
            # Wait, if `val` is at `u`, and we go to `v` with `val`.
            # The path `u -> v` has duplicate `val`.
            # The valid path ending at `v` must start after `u`. So just `v`.
            # So we update `last_seen[val] = u`.
            # Now, backtracking.
            # If we backtrack from `u`, we go to another child `w` of `parent`.
            # The path from root to `w` does not include `u`.
            # So we must remove `u` from `last_seen`.
            # But what if `val` was also present at `prev` (ancestor of `u`)?
            # Then `last_seen[val]` was `prev`. We updated it to `u`.
            # If we remove `u`, `last_seen[val]` becomes `prev`.
            # But `prev` is an ancestor of `w`? Yes, `prev` is an ancestor of `u`, and `u` is a child of `parent`.
            # `w` is a child of `parent`. So `prev` is an ancestor of `w`.
            # So keeping `prev` in `last_seen` is correct!
            #
            # Algorithm refinement:
            # 1. `last_seen` stores the most recent occurrence of each value on the *current path from root*.
            # 2. When visiting `u` with value `val`:
            #    a. If `val` in `last_seen`:
            #       - Let `prev` be the node where `val` was last seen.
            #       - Calculate valid path length from `child_of_prev` to `u`.
            #       - Update global max.
            #       - Update `last_seen[val] = u`. (Because for any future node in `u`'s subtree, `u` is the most recent `val`).
            #    b. If `val` not in `last_seen`:
            #       - Update `last_seen[val] = u`.
            # 3. Recurse to children.
            # 4. Backtrack:
            #    - We need to remove `u` from `last_seen` ONLY IF `u` was the *only* occurrence of `val` on the path from root to `u`?
            #    - No. We need to restore the state of `last_seen` to what it was before visiting `u`.
            #    - So we should store the previous value of `last_seen[val]` (if any) and restore it.
            #    - Let `old_val = last_seen.get(val)`.
            #    - After recursion, `last_seen[val] = old_val`.
            #
            # This handles the "different branch" case perfectly.
            # If `val` was seen at `prev` (ancestor), `old_val` is `prev`. We update to `u`.
            # After backtracking, we restore to `prev`.
            # If `val` was not seen, `old_val` is None. We update to `u`.
            # After backtracking, we restore to None.
            #
            # This logic seems sound.
            
            # Store the previous state for backtracking
            prev_state = last_seen.get(val)
            
            # Update last_seen for the current node
            last_seen[val] = (current_depth, current_dist, current_nodes)
            
            # Recurse
            for v, w in adj[u]:
                if v != p:
                    dfs(v, u, current_depth + 1, current_dist + w, current_nodes + 1)
            
            # Backtrack: restore the previous state
            if prev_state is None:
                del last_seen[val]
            else:
                last_seen[val] = prev_state

        dfs(0, -1, 1, 0, 1)
        
        return [max_len, min_nodes]