
## ideation
The core difficulty is maintaining a sliding window of unique values along the current DFS root-to-node path. Since a special path must be a downward path (ancestor to descendant) with all unique values, it corresponds exactly to a contiguous suffix of the current root-to-node path where all values are distinct.

Key observations:
1. Root the tree at node 0 and perform DFS.
2. Maintain the current path as a sequence of nodes with their values and prefix distances from root.
3. For each node, the longest valid special path ending at that node starts after the most recent occurrence of any duplicate value in the current path.
4. Use a dictionary to track the last occurrence (position/index in current path) of each value.
5. When entering a node, check if its value was seen before in the current path; if so, the window start must move past that previous occurrence.
6. Track the best answer: maximize length (distance), then minimize node count.

Pitfalls to avoid:
- The window start can only move forward (monotonic), so when backtracking, we need to restore the previous state of the window start and last occurrence map.
- Need to handle the case where a node's value duplicates an ancestor's value correctly.
- Node count = current depth - window start depth + 1 (or similar calculation based on indices).
- Distance = prefix_dist[current] - prefix_dist[start_node].

Approach: Iterative or recursive DFS with explicit state tracking. For each node, before processing children, compute the valid window and update answer. When backtracking, undo changes to last occurrence map and window start.

## worker: Implement the complete Python solution: build adja
I started with an iterative approach but realized state restoration during backtracking is cleaner with recursion. The key insight is maintaining a sliding window over the current root-to-node path where all values are unique. For each node, the longest valid special path ending there starts after the most recent duplicate value in the current path.

The recursive approach:
1. Track `path_dists` (prefix distances from root) and `last_occ` (last occurrence index of each value)
2. When entering a node, if its value was seen at position >= current window start, move window start past that occurrence
3. Update answer with current window: length = current_dist - path_dists[left], nodes = depth - left + 1
4. On backtrack, restore `last_occ` to previous state and pop path arrays

Time: O(n), Space: O(n) for recursion stack and path storage.

## worker: Verify against Example 1 (expect [6,2]) and Exampl
**Algorithm Verification:**

**Example 1:** `edges = [[0,1,2],[1,2,3],[1,3,5],[1,4,4],[2,5,6]]`, `nums = [2,1,2,1,3,1]`
- DFS from 0: Path 0(2)→1(1)→2(2)→5(1)
  - At node 2: value 2 seen at index 0, left becomes 1. Path 1→2: length 3, nodes 2
  - At node 5: value 1 seen at index 1, left becomes 2. Path 2→5: length 6, nodes 2 ✓
- Branch 1→4: value 1 at node 4 seen at index 1, left becomes 2. Path 1→4 invalid (duplicate), actually left=2 means path starts at node 2... wait, let me trace again:
  - At node 1: left=0, path 0→1: length 2, nodes 2
  - At node 4: value 1 seen at index 1 (node 1), left becomes 2. Path from index 2 (node 2) to 4... but node 4 is not descendant of 2. 
  - **Correction:** The path is 0→1→4. At node 4, value 1 was last seen at index 1 (node 1). So left=2. But depth of node 4 is 2. curr_nodes = 2-2+1 = 1, curr_len = dist[4] - path_dists[2] = 6 - 3 = 3. This gives length 3, not 6.
  
**Wait, there's an issue!** The path 0→1→4 has values [2,1,1] which are NOT unique. So it's not special. The valid path is just node 4 itself (length 0) or node 1→4 is invalid.

Let me re-trace: The longest valid paths are:
- 2→5: values [2,1], length 6, nodes 2 ✓
- 0→1: values [2,1], length 2, nodes 2
- 1→3: values [1,1] invalid
- 1→4: values [1,1] invalid

So [6,2] is correct! The algorithm finds 2→5.

**Example 2:** `edges = [[1,0,8]]`, `nums = [2,2]`
- Root 0: path [0], length 0, nodes 1
- Node 1: value 2 seen at index 0, left becomes 1. Path [1], length 0, nodes 1
- Result: [0,1] ✓

**Edge Cases Handled:**
1. **Single-edge duplicates:** Example 2 verifies this
2. **Deep chains:** `sys.setrecursionlimit(10**6)` handles n ≤ 5×10⁴
3. **All-same values:** Each node forms its own path, left always moves to current depth, result [0,1]
4. **All-unique values:** left stays 0, longest path is root to deepest leaf

**Complexity:** O(n) time, O(n) space for recursion stack and path storage.
