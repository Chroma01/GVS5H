
## ideation
The problem reduces to: for every root-to-node path in the tree, find the longest suffix (downward path ending at that node) with all-unique values, then take the global best by (length desc, node-count asc). Key observations and pitfalls:

- **Core mechanic**: This is "longest substring without repeating characters" along each root-to-leaf path. Maintain a window start (deepest ancestor such that path start→current node has unique values). When entering node u with value v, if v was last seen at depth d within the current window, move the window start down to depth d+1.
- **State tracking**: Need `last[value] = depth` of the most recent occurrence on the current path. On backtrack, restore the previous value (or remove if none). Since values ≤ 5·10⁴, a dict or array works; dict is safer/cleaner.
- **Window start representation**: Track `startDepth` (integer depth of window top). To compute length, we need `dist[startNode]`, but we only know its depth. Options: (a) maintain a stack of nodes in the current path so `path[startDepth]` gives the node, then `dist[u] - dist[path[startDepth]]`; (b) maintain a parallel stack of prefix distances. Option (a) is simplest: keep `path` list acting as a stack indexed by depth.
- **Answer update**: For every node u (including root, giving the trivial single-node path), candidate length = `dist[u] - dist[path[startDepth]]`, nodes = `depth[u] - startDepth + 1`. Compare: larger length wins; tie → fewer nodes wins.
- **Pitfalls**:
  - Must update `startDepth` to `max(startDepth, last[v] + 1)` — only move it downward, never up (a stale occurrence above the window shouldn't matter, but since we restore on backtrack, `last[v]` always refers to an ancestor on the current path; still, if v occurred above the window start... can't happen because when the window moved past it, that occurrence was overwritten? No — `last[v]` holds the *most recent* occurrence, which is always ≥ any earlier one; if the most recent is below window start, fine; if window start is below it, we move. Actually most-recent occurrence is always on current path and is the binding constraint. Safe.)
  - On backtrack, restore `last[v]` to its previous value (need to save it before overwriting) or delete if it didn't exist.
  - Recursion depth: n up to 5·10⁴ — Python's default recursion limit (1000) will fail. Use iterative DFS with explicit stack, or `sys.setrecursionlimit(2*10**5)` plus possibly `threading` with bigger stack. Iterative is safest.
  - Root the tree at 0: build adjacency list, DFS from 0 avoiding parent.
  - Tie-breaking direction: minimize node count among max-length paths.
  - Single-node path length 0 is always valid, so answer is at least [0,1].
- **Complexity**: O(n) time, O(n) space.

## worker: Implement the complete solution: build adjacency l
Implemented the planned O(n) sliding-window-on-root-path DFS:

- **Adjacency + rooting**: Build adjacency list from edges; DFS iteratively from node 0, tracking parent to avoid going back up.
- **Window maintenance**: `last[v]` stores the deepest depth at which value `v` appears on the current root-to-node path. On entering a node, if `last[v] >= start_depth`, the window top jumps to `last[v] + 1`, guaranteeing all values in `[start_depth, depth]` are unique. `path` (a stack indexed by depth) lets us fetch the window-top node to compute `dist[node] - dist[path[start_depth]]`.
- **Answer update**: At every node entry, candidate length and node count are computed; global best prefers larger length, then fewer nodes. Initialized to `[0, 1]` (single-node path always valid).
- **Backtracking**: A parallel `saved_stack` records `(saved_start, prev_depth, value)` per entered node; on the exit frame, `path` is popped, `last[v]` is restored (or deleted if it was absent), and `start_depth` is restored. This keeps state correct across sibling subtrees.
- **Iterative DFS** avoids Python recursion-limit issues for n = 5·10⁴ (deep skewed trees).

**Verification against examples:**
- Example 1: edges form tree 0-1(2), 1-2(3), 1-3(5), 1-4(4), 2-5(6); nums=[2,1,2,1,3,1]. Path 0→1→2→5: at node 2 (value 2, previously at depth 0), window start moves to depth 1; at node 5 (value 1, last at depth 1), start moves to depth 2 → length = dist[5]-dist[2] = 11-5 = 6, nodes = 2. Path 0→1→4: values 2,1,1 → at node 4, start = depth 2... wait: node 4 has value 1, last seen at depth 1 (node 1), so start=2, length = dist[4]-dist[4] = 0? Let me recheck: dist[4] = 2+4 = 6, path[start]=path[2]=node 4 itself → length 0. Hmm, but expected 0→1→4 has length 6 with values 2,1,1 — that's NOT unique! Re-reading the example: "0 -> 1 -> 4" with nums 2,1,1... Actually nums[4]=3? nums = [2,1,2,1,3,1]: nums[0]=2, nums[1]=1, nums[2]=2, nums[3]=1, nums[4]=3, nums[5]=1. So 0→1→4 has values 2,1,3 — unique, length 2+4=6, 3 nodes. Path 2→5: values 2,1, length 6, 2 nodes. Best length 6, min nodes 2 → [6,2]. ✓ My trace: at node 4, value 3 never seen, start stays 0 → length = 6-0 = 6, nodes 3. At node 5: value 1 last at depth 1 → start=2, length = dist[5]-dist[2] = 11-5 = 6, nodes 2. Tie at 6 → min(3,2)=2. ✓
- Example 2: edge 1-0 weight 8, nums=[2,2]. Root 0: candidate [0,1]. Node 1: value 2 seen at depth 0 → start=1, length = 8-8 = 0, nodes 1. Best stays [0,1]. ✓

**Complexity**: O(n) time, O(n) space.

## worker: Verify the implementation against Examples 1 and 2
**Fix applied**: Moved `saved_stack` from a module-level list into a local variable initialized before the DFS loop. The previous code had two bugs: (1) module-level state would leak across multiple calls to `longestSpecialPath` (LeetCode reuses the `Solution` instance and module across test cases), causing corrupted restore state; (2) the stray `__init__` and module-level declaration were dead weight. Now each call gets a fresh `saved_stack`, and enter/exit frames stay perfectly paired (one push per enter, one pop per exit).
