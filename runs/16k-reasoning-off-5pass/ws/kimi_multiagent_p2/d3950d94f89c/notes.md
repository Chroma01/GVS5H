
## ideation
The core difficulty is enforcing the "all values unique" constraint along ancestor-to-descendant paths efficiently. Since paths must be downward, a single DFS from the root naturally enumerates every candidate endpoint; the challenge is finding, for each node, the highest valid starting ancestor such that the path to it has all unique values. This is essentially a sliding window over the current root-to-node path: the window's top boundary is just below the deepest occurrence of any value that appears again at the current node. A dict mapping value → deepest depth index where it currently appears on the path gives O(1) updates; on entering a node with value v, the new window top is max(current top, lastDepth[v] + 1). Prefix sums of edge weights let us compute path length in O(1). Answer comparison is lexicographic: maximize length, then minimize node count (nodes = depth difference + 1). Pitfalls: (1) correctly restoring dict state on backtrack — when a value was already present deeper up, we must restore the old depth, not delete; (2) the window top must be monotonic within a single DFS branch but restored on backtrack; (3) single-node paths (length 0, 1 node) must be considered, e.g., Example 2 where all values duplicate; (4) recursion depth up to 5·10^4 — need sys.setrecursionlimit or iterative DFS; (5) depth index vs weighted length must not be confused — node count uses unweighted depth, length uses weighted prefix sum.

## worker: Implement the full solution: build adjacency list,
Implemented an iterative DFS from root 0 maintaining:
- `path[d]`: node id at depth `d` on the current root-to-node path (used to identify the parent edge and for window start node lookup).
- `pref[d]`: weighted prefix distance from root to depth `d`.
- `last_depth`: dict mapping value → deepest depth index on the current path, with save/restore on backtrack (restore old depth if the value existed above, delete otherwise).
- `start`: the current sliding-window top depth; on entering a node with value `v`, `start = max(start, last_depth.get(v, -1) + 1)`. On backtrack, `start` is restored from the parent frame's stored value.

At each node, the candidate special path is from depth `start` to the current depth: length `pref[nd] - pref[start]`, node count `nd - start + 1`. The best answer is tracked lexicographically (maximize length, then minimize nodes). Root's single-node path (length 0, 1 node) initializes the best, covering cases like Example 2.

Complexity: O(n) time, O(n) space. Iterative DFS avoids recursion-limit concerns.

One subtlety handled: `start` restoration on pop uses the parent frame's stored post-entry `start` value (5th tuple element), which equals the window top while the parent is the deepest node — exactly the correct state to resume iterating the parent's other children.

## worker: Verify against Example 1 (expect [6,2]) and Exampl
Verified the implementation mentally against the required cases:

**Example 1**: edges=[[0,1,2],[1,2,3],[1,3,5],[1,4,4],[2,5,6]], nums=[2,1,2,1,3,1]
- DFS from 0: node 0 (val 2, depth 0, pref 0), start=0, candidate (0,1).
- Node 1 (val 1, depth 1, pref 2): start=0, candidate len 2, nodes 2 → best (2,2).
- Node 2 (val 2, depth 2, pref 5): last_depth[2]=0 → start=1, candidate len 4, nodes 2 → best (4,2).
- Node 5 (val 1, depth 3, pref 11): last_depth[1]=1 → start=2, candidate len 6, nodes 2 → best (6,2). ✓ (path 2→5)
- Backtrack to 1, node 4 (val 3, depth 2, pref 6): start restored to 0 (frame of node 1 stored start_entry=0), candidate len 6, nodes 3 → tie length, nodes 3 > 2, best stays (6,2). ✓ (path 0→1→4 has length 6 but 3 nodes; min nodes = 2)
- Result: [6,2] ✓

**Example 2**: edges=[[1,0,8]], nums=[2,2]
- Root 0 (val 2): best (0,1). Node 1 (val 2, depth 1, pref 8): last_depth[2]=0 → start=1, candidate len 0, nodes 1 → tie, best stays (0,1). Result: [0,1] ✓

**Chain all-same values** (e.g., 0-1-2-3, all val 5): each node forces start = its own depth, so all candidates are (0,1) → [0,1] ✓

**Star tree**: each leaf processed with start=0 (assuming distinct values), candidate = edge weight, 2 nodes; best = max edge weight ✓

**Deep chain (5·10⁴)**: iterative DFS with explicit stack — no recursion limit issues; path/pref arrays sized n ✓

State restoration on backtrack is correct: `last_depth` restored to previous depth (or deleted), and `start` restored from parent frame's stored `start_after_entry`, which is exactly the window top while the parent is deepest.

Complexity: O(n) time, O(n) space.
