
## ideation
- **Core Difficulty**: The problem requires finding the longest path in a tree where all node values on the path are unique, with the constraint that the path must be "downward" (from ancestor to descendant). The challenge lies in efficiently managing the "unique values" constraint during traversal without resorting to an $O(N^2)$ solution (e.g., checking every node as a potential start point and traversing down).
- **Candidate Approaches**:
  1. **DFS with Backtracking (Set Maintenance)**: Perform a DFS from the root. Maintain a set of values seen on the current path from the root. When visiting a child:
     - If the child's value is not in the set, add it, update the current path's total length and node count, and recurse.
     - If the child's value is already in the set, we cannot extend the current unique path through this child *from the current ancestor*. We must backtrack (remove the current node's value from the set) and return.
     - *Correction/Refinement*: The definition says "downward path from an ancestor to a descendant". It does *not* strictly require the path to start at the root. However, any valid downward path is a sub-segment of a path starting at some ancestor. If we maintain the set of values from the root to the current node $u$, and $u$'s value is unique in that set, then any suffix of that path (starting at some ancestor $v$) is also a valid special path.
     - *Optimization*: Instead of restarting the set for every node, we can pass the set down. If we hit a duplicate, we stop extending *that specific chain*. But wait, if we stop at a duplicate, do we lose potential paths starting *below* the duplicate? No, because the path must be contiguous and downward. If $A \to B \to C$ has values $\{1, 1, 2\}$, the path $A \to B$ is invalid. The path $B \to C$ is valid. The path $A \to C$ is invalid.
     - Actually, the standard approach for "longest path with unique values in a tree" usually involves checking every node as a start. But here, the constraint is specifically "ancestor to descendant". This simplifies things: we only need to look at paths starting at some node $u$ and going down to $v$.
     - **Revised Strategy**: We can perform a DFS. For each node, we maintain the current path from the root. If the current node's value is unique in the path from root to current, then we have a set of valid paths ending at this node (starting at any ancestor). We need the one with the maximum length.
     - However, maintaining the full set and checking uniqueness for every node might be slow if not careful. But since we traverse once, we can just keep the set of values on the current recursion stack.
     - **Crucial Logic**: When at node $u$, if `nums[u]` is already in the set of values from root to parent of $u$, then no path starting at or above the parent can extend through $u$ while maintaining uniqueness. However, a path could start at $u$ itself (length 0). So, if a duplicate is found, we backtrack the set, record the max found so far, and proceed to children with an *empty* set (effectively starting a new path at $u$)?
     - Wait, if we start a new path at $u$, we just check children. If a child $v$ has a value different from $u$, we can extend.
     - **Correct Algorithm**:
       1. Build adjacency list.
       2. DFS from root. Pass `current_path_set` and `current_len`, `current_nodes`.
       3. At node $u$:
          - Check if `nums[u]` is in `current_path_set`.
          - If **Yes**: The path from any ancestor including the previous occurrence of `nums[u]` cannot be extended. We must backtrack the set (remove ancestors) until we find the node where `nums[u]` was first added? No, simpler: The current path from root is broken. We can only start a new path at $u$. So, we clear the set, add `nums[u]`, set len=0, nodes=1, and recurse. BUT, we must also consider that the path *ending* at $u$ starting at $u$ is valid.
          - If **No**: Add `nums[u]` to set. Update global max with `current_len + edge_weight`. Update global min nodes. Recurse. After returning, backtrack (remove `nums[u]`).
       - **Wait, is clearing the set correct?**
         Example: Root(1) -> A(2) -> B(1).
         Path Root->A is valid. Path Root->A->B is invalid (1 repeats).
         Path A->B is valid (values {2, 1}).
         Path B is valid.
         If we are at B, and we see 1 is in {1, 2}, we stop extending Root->A. But we can start a new path at A?
         Yes. So if we encounter a duplicate, we effectively "reset" the path start to the current node.
         However, we need to be careful: The "reset" implies we ignore the history above. But what if the duplicate was far up?
         Actually, the condition "ancestor to descendant" means the path is contiguous. If `nums[u]` exists in the path from root to parent, then any path ending at $u$ and starting above that occurrence is invalid. The only valid paths ending at $u$ are those starting at or below the node where `nums[u]` first appeared.
         Since we are doing DFS, we don't know where `nums[u]` first appeared easily without storing it.
         **Better Approach**:
         Instead of just a set, maybe we store `(value, node_index)`? No, values can repeat.
         Let's reconsider the "reset" logic.
         If `nums[u]` is in `path_set`:
           The longest valid path ending at $u$ must start at $u$ itself (length 0).
           Why? Because any path starting above $u$ would include the previous occurrence of `nums[u]`, making it invalid.
           So, if duplicate found:
             Backtrack the set to remove everything above $u$.
             Add `nums[u]`.
             Current len = 0, nodes = 1.
             Update global max/min.
         If `nums[u]` not in `path_set`:
             Add `nums[u]`.
             Current len += edge, nodes += 1.
             Update global max/min.
             Recurse.
             Backtrack.
         
         Is this sufficient?
         Case: 1 -> 2 -> 1 -> 3.
         Root(1): Set={1}, len=0. Max=0.
         Child(2): Set={1,2}, len=w1. Max=w1.
         Child(1): Duplicate! Set becomes {1} (reset to current node). Len=0. Max=max(w1, 0).
         Child(3): Set={1,3}, len=w2. Max=max(..., w2).
         This logic seems to assume that if we hit a duplicate, we *must* start at the current node. Is it possible to start at a node *between* the previous occurrence and the current one?
         Example: A(1) -> B(2) -> C(1).
         Path A->B is valid. Path B->C is valid. Path A->C is invalid.
         When at C, we see 1 is in {1, 2}. We reset to C. We lose the path B->C?
         No! If we reset to C, we treat the path as starting at C. But B->C starts at B.
         The issue is that when we are at B, we added 2 to the set. When we go to C, we see 1. We know 1 is in the set (from A).
         We cannot extend A->...->C.
         Can we extend B->C? Yes, because B has value 2, C has 1. They are unique.
         But our set contains A's value (1). We don't know if B's value is the one causing the conflict or if A's is.
         Actually, if `nums[C]` is in the set, it means there is *some* ancestor with the same value. Let that ancestor be $X$.
         Any path starting at $X$ or above is invalid.
         Any path starting below $X$ (e.g., at $X$'s child) might be valid, provided the path from $X$'s child to $C$ doesn't contain another duplicate.
         Since we are traversing top-down, if we encounter a duplicate at $C$, the "break point" is the first occurrence of that value. Let's say it was at node $P$.
         Then any path starting at $P$ is invalid. Paths starting strictly below $P$ are potentially valid.
         Since we are doing DFS, we don't naturally "jump" to $P$'s children to restart.
         **Alternative Idea**:
         For each node, we want to find the longest path ending at this node with unique values.
         Let $dp[u]$ be the length of the longest special path ending at $u$.
         To compute $dp[u]$, we look at all children $v$. But the path must come from an ancestor.
         Actually, the path is defined as Ancestor -> Descendant.
         So for a fixed descendant $u$, we want the furthest ancestor $v$ such that the path $v \to \dots \to u$ has unique values.
         This looks like we can maintain the "last seen position" of each value in the current path.
         Since $N$ is up to $50,000$, we can't afford $O(N)$ per node.
         However, we can maintain a map `last_pos[value]` which stores the depth or cumulative length from the root to the last occurrence of `value`.
         When moving from parent $p$ to child $u$:
           If `nums[u]` has been seen in the current path (i.e., in the map):
             The path cannot extend from the node where `nums[u]` was last seen.
             So the longest valid path ending at $u$ must start *after* that last seen node.
             But wait, the path must be contiguous. If the last seen node is $X$, then the path $X \to \dots \to u$ is invalid.
             The valid paths ending at $u$ must start at a node $Y$ such that $Y$ is a descendant of $X$ (or $Y=X$ if we allow starting at the duplicate? No, if we start at $X$, the path includes $X$ and $u$, both having value $V$, so invalid).
             So $Y$ must be a proper descendant of $X$.
             But we don't know the exact start node $Y$ easily without traversing down from $X$.
         
         **Wait, re-read the problem carefully**: "A special path is defined as a downward path from an ancestor node to a descendant node such that all the values of the nodes in that path are unique."
         This implies the path is a simple path in the tree.
         If we have a path $A \to B \to C \to D$ with values $1, 2, 1, 3$.
         Valid sub-paths:
         $A \to B$ (1,2) - OK
         $B \to C$ (2,1) - OK
         $C \to D$ (1,3) - OK
         $A \to C$ (1,2,1) - NO
         $B \to D$ (2,1,3) - OK
         $A \to D$ - NO
         
         So for node $D$, the valid paths ending at $D$ are $C \to D$ and $B \to D$.
         $B \to D$ has length = $w(B,C) + w(C,D)$.
         $C \to D$ has length = $w(C,D)$.
         We want the max length.
         Notice that $B \to D$ is valid because the values $\{2, 1, 3\}$ are unique. The duplicate $1$ was at $A$ and $C$. Since $A$ is not in the path $B \to D$, it's fine.
         So, if we are at $u$, and we find that `nums[u]` was last seen at ancestor $X$, then any path starting at or above $X$ is invalid.
         The longest valid path ending at $u$ must start at a node $Y$ which is a child of $X$ (or deeper), such that the path $Y \to \dots \to u$ has no duplicates.
         But wait, if $X$ is the *only* duplicate above $u$, then the path starting at the child of $X$ going down to $u$ will have unique values (assuming no other duplicates in between).
         Is it guaranteed that there are no other duplicates between $X$ and $u$?
         Not necessarily. There could be another duplicate $Z$ between $X$ and $u$.
         In that case, the "last seen" logic needs to be applied recursively.
         Actually, if we maintain the set of values on the current path from root to $u$, and we encounter a duplicate at $u$, we know the path is broken.
         BUT, we don't need to restart from $u$. We can restart from the child of the *first* occurrence of the duplicate value in the current path.
         Let's trace:
         Path: $v_0, v_1, v_2, v_3, v_4$ with values $1, 2, 3, 2, 4$.
         At $v_4$ (val 4): Unique. Path $v_0 \to v_4$ is valid.
         At $v_3$ (val 2): Duplicate of $v_1$.
           Path $v_0 \to v_3$ invalid.
           Path $v_1 \to v_3$ invalid (contains 2 twice).
           Path $v_2 \to v_3$ valid (3, 2).
           So the longest valid path ending at $v_3$ starts at $v_2$ (child of $v_1$).
         So, if we hit a duplicate at $u$ with value $V$, and $V$ was last seen at $X$, then the longest valid path ending at $u$ is the longest valid path ending at $u$ that starts at a child of $X$.
         But we don't have the answer for "child of $X$" stored globally.
         
         **Wait, is it possible to solve this by simply maintaining the set and backtracking?**
         If we hit a duplicate at $u$, we remove nodes from the set until the duplicate is gone?
         No, because the duplicate might be far up.
         Example: $1 \to 2 \to 3 \to 2 \to 4$.
         At the second 2, we see 2 is in $\{1, 2, 3\}$.
         If we remove 2, we get $\{1, 3\}$. Then we add 2 -> $\{1, 3, 2\}$.
         This corresponds to path starting at 3.
         Is path $3 \to 2 \to 4$ valid? Values $\{3, 2, 4\}$. Yes.
         Is path $2 \to 3 \to 2 \to 4$ valid? No.
         Is path $1 \to 2 \to 3 \to 2 \to 4$ valid? No.
         So effectively, when we hit a duplicate, we "cut" the path at the previous occurrence of that value.
         But we need to know *which* node was the previous occurrence.
         We can store `last_seen[value] = node_index` in the current path.
         When at $u$ with value $V$:
           If $V$ in `last_seen`:
             Let $X = last\_seen[V]$.
             The path cannot include $X$.
             So we effectively need to continue the search from the children of $X$.
             But we are currently at $u$. We can't jump back to $X$'s children easily in a simple DFS without re-traversing or storing state.
             
         **Alternative Insight**:
         Since $N$ is small ($5 \times 10^4$), maybe we can afford $O(N)$ per node? No, $O(N^2)$ is too slow.
         We need $O(N)$ or $O(N \log N)$.
         
         Let's reconsider the "reset" strategy.
         If we maintain the set of values on the current path.
         If we encounter a duplicate, we know the current path from root is invalid.
         However, the problem asks for the longest special path *anywhere*.
         Maybe we can just run DFS, and for each node, if its value is unique in the path from root, we update the global max.
         If its value is NOT unique, does that mean we stop?
         No, because a valid path could start below the duplicate.
         BUT, notice the structure:
         If we have a path $Root \to \dots \to X \to \dots \to u$ where $X$ and $u$ have same value.
         Any valid path ending at $u$ must start after $X$.
         The path starting at the child of $X$ (let's call it $Y$) and going to $u$ is a candidate.
         Is it possible that the path starting at $Y$ has a duplicate *between* $Y$ and $u$?
         Yes. In that case, the valid path would start even later.
         This suggests that for any node $u$, the longest valid path ending at $u$ is determined by the *closest* ancestor $X$ (including $u$ itself as a start) such that the path $X \to u$ is unique.
         Actually, it's the *furthest* ancestor $X$ such that $X \to u$ is unique.
         This is equivalent to: Find the nearest ancestor $X$ such that the path $X \to u$ contains no duplicates.
         This is equivalent to: Find the nearest ancestor $X$ such that for all values $v$ in path $X \to u$, count is 1.
         This is equivalent to: Find the nearest ancestor $X$ such that no value in path $X \to u$ appears twice.
         This is equivalent to: Find the nearest ancestor $X$ such that the path from $X$ to $u$ does not contain any duplicate.
         This is equivalent to: Find the nearest ancestor $X$ such that the path from $X$ to $u$ is a special path.
         Wait, this is circular.
         
         Let's simplify.
         For a fixed $u$, we want the largest $depth(X)$ such that path $X \to u$ is unique.
         This is equivalent to finding the largest $depth(X)$ such that no value in $nums[X \dots u]$ repeats.
         This is equivalent to finding the largest $depth(X)$ such that for all $v \in nums[X \dots u]$, $count(v) = 1$.
         This is equivalent to finding the largest $depth(X)$ such that the set of values in $nums[X \dots u]$ has size equal to the length of the path.
         
         How to compute this efficiently?
         We can maintain the set of values on the current path from root to $u$.
         Also maintain the cumulative length and node count from root to $u$.
         If we encounter a duplicate at $u$ (value $V$), let $X$ be the node where $V$ was last seen.
         Then any path starting at or above $X$ is invalid.
         The longest valid path ending at $u$ must start at a child of $X$.
         BUT, we don't know if the path from child of $X$ to $u$ is valid. It might have another duplicate $Z$.
         If it does, then we must start below $Z$.
         So, effectively, the start node of the longest valid path ending at $u$ is the node immediately following the *last* duplicate encountered on the path from root to $u$.
         Let's formalize:
         Traverse from root to $u$. Keep track of the "most recent duplicate break".
         Actually, simpler:
         Maintain `last_pos[val]` = depth of the last occurrence of `val`.
         Also maintain `min_depth_start` for the current path?
         No.
         Let's try a different perspective.
         We are looking for the longest path with unique values.
         This is equivalent to: For each node $u$, find the furthest ancestor $v$ such that the path $v \to u$ has unique values.
         Let $L[u]$ be the length of the longest special path ending at $u$.
         $L[u] = \max(0, L[parent] + weight)$ IF $nums[u]$ is unique in path from root to $parent$? No.
         If $nums[u]$ is unique in path from root to $parent$, then the path from root to $u$ is unique. The longest path ending at $u$ is root to $u$.
         If $nums[u]$ is NOT unique in path from root to $parent$, let $X$ be the node where $nums[u]$ was last seen.
         Then the path from $X$ to $u$ is invalid.
         The path from child of $X$ to $u$ might be valid.
         But we don't know if it's valid without checking for other duplicates.
         
         **Correct Logic with Backtracking (Set)**:
         Actually, the "reset" strategy works if we interpret it correctly.
         If we hit a duplicate at $u$, we know the path from root to $u$ is invalid.
         But we can "restart" the path at the child of the node where the duplicate first occurred.
         However, we don't know which child.
         Wait, if we use a set and backtrack:
         DFS(u, current_set, current_len, current_nodes):
           if nums[u] in current_set:
             # Duplicate found.
             # The path from root to u is invalid.
             # But we can start a new path at u?
             # Or start at the child of the previous occurrence?
             # We don't know the previous occurrence's child.
             # BUT, we can simply clear the set and start at u.
             # Why? Because any path starting above the previous occurrence is invalid.
             # Any path starting at the previous occurrence is invalid (duplicate).
             # So the only candidate start nodes are descendants of the previous occurrence.
             # But we are at u. We can't jump.
             # However, notice that if we clear the set and start at u, we are considering paths starting at u.
             # What about paths starting at the child of the previous occurrence?
             # Those paths would have been considered when we were at the child of the previous occurrence!
             # Ah!
             # When we were at the child of the previous occurrence (say $Y$), we added $nums[Y]$ to the set.
             # If $nums[Y]$ was unique, we continued.
             # If later we hit a duplicate at $u$, it means the path from $Y$ to $u$ is invalid ONLY IF $nums[u]$ appeared in $Y \to u$.
             # But $nums[u]$ appeared at $X$ (ancestor of $Y$).
             # So $nums[u]$ did NOT appear in $Y \to u$ (otherwise we would have stopped earlier at the first occurrence in that segment).
             # Therefore, the path $Y \to u$ IS valid!
             # So, if we hit a duplicate at $u$ due to $X$, then the path starting at $Y$ (child of $X$) and ending at $u$ is valid.
             # And since we want the longest, we should have tracked the path starting at $Y$.
             # But in our DFS, we didn't "save" the path starting at $Y$ separately. We saved the path starting at root.
             # So we missed it.

## worker: Implement the recursive DFS function that traverse
The solution uses a Depth-First Search (DFS) to traverse the tree. For each node, we maintain:
1. `current_len` and `current_nodes`: The cumulative length and number of nodes from the root to the current node.
2. `cut_len` and `cut_nodes`: The cumulative length and number of nodes up to the start of the valid special path segment ending at the current node. Initially, this is 0 (representing a virtual node before the root).
3. `last_pos`: A dictionary mapping a node value to the `(cumulative_len, cumulative_nodes)` of its last occurrence on the current path from the root.

When visiting a node `u` with value `val`:
- If `val` is in `last_pos`, it means `val` has appeared before on the current path. The path from the root to `u` is invalid. However, the path starting from the child of the previous occurrence of `val` to `u` is valid. We update `cut_len` and `cut_nodes` to the values stored in `last_pos[val]`.
- If `val` is not in `last_pos`, the path can be extended from the current valid segment. `cut_len` and `cut_nodes` remain unchanged.
- We update `last_pos[val]` with the current node's cumulative stats.
- The length of the longest special path ending at `u` is `current_len - cut_len`, and the number of nodes is `current_nodes - cut_nodes`. We update the global maximum length and minimum node count accordingly.
- We backtrack by removing `val` from `last_pos` after returning from the recursive calls to ensure the state is correct for other branches.

This approach ensures that we efficiently find the longest special path in $O(N)$ time and space.

## worker: finalize
The solution uses a Depth-First Search (DFS) traversal to explore all downward paths from the root. 
Key logic includes:
1.  **State Maintenance**: We maintain `current_len` and `current_nodes` representing the cumulative distance and node count from the root to the current node.
2.  **Cut Point Tracking**: We use `cut_len` and `cut_nodes` to track the start of the longest valid special path ending at the current node. Initially, this is 0 (virtual node before root).
3.  **Duplicate Handling**: We use a dictionary `last_pos` to store the cumulative stats of the last occurrence of each value on the current path. If we encounter a value `val` that is already in `last_pos`, it means the path from the root to the current node contains a duplicate. The longest valid special path ending at the current node must start immediately after the previous occurrence of `val`. Thus, we update `cut_len` and `cut_nodes` to the values stored in `last_pos[val]`.
4.  **Path Calculation**: The length of the valid special path ending at the current node is `current_len - new_cut_len`, and the number of nodes is `current_nodes - new_cut_nodes`. We update the global maximum length and minimum node count accordingly.
5.  **Backtracking**: After processing a node and its children, we remove the node's value from `last_pos` to ensure the state is correct for other branches of the tree.

This approach ensures that we efficiently find the longest special path in $O(N)$ time and space complexity, which fits within the problem constraints.
