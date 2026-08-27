
## ideation
- **Core Difficulty**: The problem requires finding the longest downward path with unique node values in a tree. A naive DFS that checks all ancestors for each node would be $O(N^2)$ in the worst case (e.g., a line), which is too slow for $N \le 50,000$. We need an efficient way to handle the "backtracking" or "resetting" of the unique value set when a duplicate is encountered.
- **Candidate Approaches**:
  1. **DFS with Path Set + Backtracking**: Maintain a set of values on the current recursion stack. When visiting a child, check if its value exists in the set. If it does, we must "pop" nodes from the current path until the duplicate is removed. Since we are moving down the tree, we can maintain the current path's length and the set. When a duplicate is found at depth $d$ with value $v$, we need to find the nearest ancestor with value $v$ and reset the path state to just below that ancestor.
  2. **Optimized State Management**: Instead of rebuilding the set every time, pass the current set and length down. If a duplicate is found, we need to efficiently find the depth of the previous occurrence. We can store `(value -> depth)` in a dictionary for the current path. If `nums[child]` is in the dict, say at `prev_depth`, the new valid path starts from `prev_depth + 1`. We then pop elements from our path tracking structures from `prev_depth` down to the current node.
  3. **Complexity Analysis**: With proper backtracking (popping from the path set and length counters), each node is added and removed from the path set at most once per branch traversal. The total time complexity would be $O(N)$ because the "work" of popping corresponds to the edges traversed in the recursion stack.
- **Pitfalls**:
  - **Incorrect Backtracking Logic**: Simply breaking the loop and returning 0 is insufficient; we must correctly update the global maximums and ensure the recursion continues correctly for other branches.
  - **Global State Contamination**: If we use a global set, we must ensure it is perfectly restored after visiting a subtree. Using recursion with passed sets or explicit popping is safer.
  - **Edge Cases**: Single node trees, paths where the duplicate is the immediate parent, or duplicates deep in the tree.
  - **Data Structures**: Using a list for the path and a dict for value-to-index mapping allows $O(1)$ lookups and $O(1)$ pops if we manage indices carefully.

## worker: Build the adjacency list representation of the tre
- **Tree Construction**: Built an adjacency list from `edges`. Since the input is an undirected tree, we perform a BFS starting from node 0 to establish parent-child relationships and avoid traversing back to the parent.
- **DFS with Backtracking**: 
  - Maintains a `stack_vals` (list of node values on the current path) and `stack_lens` (list of cumulative lengths from root).
  - Uses a `seen_map` dictionary to store the index of each value in the current path for O(1) lookup.
  - When visiting a node, if its value is already in `seen_map`, it calculates the length and node count of the special path starting immediately after the previous occurrence of the same value.
  - If no duplicate is found, it considers the path from the root.
  - Updates global `max_len` and `min_nodes` accordingly.
  - Backtracks by popping from `stack_vals`, `stack_lens`, and removing from `seen_map` to restore state for other branches.
- **Complexity**: Each node is added and removed from the stack exactly once. Dictionary operations are O(1) on average. Total time complexity is O(N). Space complexity is O(N) for the recursion stack and auxiliary data structures.
- **Edge Cases**: Handled naturally (e.g., single node, duplicates at root, duplicates deep in the tree).

## worker: Run the solution against the provided examples to 
1.  **Tree Construction**: The input `edges` represents an undirected tree. I first perform a BFS starting from node 0 to establish parent-child relationships and populate a `children` adjacency list. This ensures the DFS only traverses downwards, respecting the rooted structure.
2.  **DFS with Backtracking**:
    -   I maintain `stack_vals` (node values on the current path) and `stack_lens` (cumulative edge lengths from root to each node in the stack).
    -   `seen_map` stores the index of each value in `stack_vals` for O(1) lookup.
    -   When visiting a node `u` with value `val`:
        -   If `val` is in `seen_map`, it means there's a duplicate ancestor. The longest special path ending at `u` starts immediately after the previous occurrence of `val`. The length is calculated as `curr_len - stack_lens[prev_idx]`, and the node count is `depth - prev_idx`.
        -   If `val` is not in `seen_map`, the path from the root to `u` is valid. The length is `curr_len`, and node count is `depth + 1`.
    -   After processing, the node is added to the stack, children are visited, and then the node is removed (backtracked) to restore state for other branches.
3.  **Complexity**:
    -   Time Complexity: $O(N)$ because each node is visited once, and stack operations (append/pop/dict update/delete) are $O(1)$ on average.
    -   Space Complexity: $O(N)$ for the adjacency list, recursion stack, and path tracking structures.
4.  **Edge Cases**:
    -   Single node: Handled correctly (loop doesn't run, returns `[0, 1]`).
    -   Duplicates: The logic correctly identifies the nearest ancestor with the same value and calculates the path length starting after it.
    -   Constraints: $N \le 50,000$ is handled efficiently. Recursion limit is increased to prevent stack overflow.

## worker: [B, C, B] -> No.
- **Tree Construction**: The input `edges` is an undirected tree. I first perform a BFS starting from node 0 to establish parent-child relationships and populate a `children` adjacency list. This ensures the DFS only traverses downwards, respecting the rooted structure.
- **DFS with Backtracking**:
    - I maintain `stack_vals` (node values on the current path) and `stack_lens` (cumulative edge lengths from root to each node in the stack).
    - `seen_map` stores the index of each value in `stack_vals` for O(1) lookup.
    - When visiting a node `u` with value `val`:
        - If `val` is in `seen_map`, it means there's a duplicate ancestor. The longest special path ending at `u` starts immediately after the previous occurrence of `val`. The length is calculated as `curr_len - stack_lens[prev_idx]`, and the node count is `depth - prev_idx`.
        - If `val` is not in `seen_map`, the path from the root to `u` is valid. The length is `curr_len`, and node count is `depth + 1`.
    - After processing, the node is added to the stack, children are visited, and then the node is removed (backtracked) to restore state for other branches.
- **Complexity**:
    - Time Complexity: $O(N)$ because each node is visited once, and stack operations (append/pop/dict update/delete) are $O(1)$ on average.
    - Space Complexity: $O(N)$ for the adjacency list, recursion stack, and path tracking structures.
- **Edge Cases**:
    - Single node: Handled correctly (loop doesn't run, returns `[0, 1]`).
    - Duplicates: The logic correctly identifies the nearest ancestor with the same value and calculates the path length starting after it.
    - Constraints: $N \le 50,000$ is handled efficiently. Recursion limit is increased to prevent stack overflow.
