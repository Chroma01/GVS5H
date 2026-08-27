
## ideation
- **Core difficulty:**  
  Find, in a rooted weighted tree, the downward (ancestor → descendant) path that maximizes the total edge length while containing no repeated node values. Among those maximal‑length paths we also need the smallest number of nodes.  
  The difficulty is the combination of *uniqueness of values* (a set constraint) and *weight sum* (a numeric constraint) on paths that are not linear but tree‑structured.

- **Key observation:**  
  While walking from the root downwards the current path is a simple linear list of nodes (the recursion stack). The condition “all values are different” on that list is exactly the classic “longest sub‑array with distinct elements”. A sliding‑window (two‑pointer) technique can be applied online: keep a left border `L` such that the sub‑path `nodes[L … current]` has all distinct values. When a duplicate value appears at depth `prev`, the left border must move to `max(L, prev+1)`.

- **Data needed for each node:**  
  1. `curDist` – total edge length from the root.  
  2. `curDepth` – number of edges from the root (also the index in the path).  
  3. For every value, the most recent depth where it occurred on the current path (`lastPos[value]`).  
  4. `dist[depth]` – distance from the root to the node at that depth, to obtain the length of a window as `curDist - dist[L]`.  
  5. `startDepth` – current left border `L`.

- **Candidate path ending at the current node:**  
  - Length = `curDist - dist[startDepth]`.  
  - Number of nodes = `curDepth - startDepth + 1`.  
  This pair is compared with the global best (longer length, or same length with fewer nodes).

- **Backtracking:**  
  After processing a child we must restore `startDepth` and the entry for the current value in `lastPos` to the state they had before the child was visited, otherwise the sliding window would be corrupted for sibling sub‑trees.

- **Pitfalls / corner cases:**  
  - Recursion depth for `n = 5·10⁴` can exceed Python’s default limit → raise recursion limit.  
  - Values can be as large as `5·10⁴`; a dictionary (`hash map`) is needed for `lastPos`.  
  - When a value is seen for the first time on a path we must **delete** its entry on backtrack; otherwise it would incorrectly block later branches.  
  - Path length may be `0` (single node). Ensure node count is counted correctly (the starting node itself).  
  - If multiple longest paths have the same length, we need the *minimum* node count, not the maximum.  
  - The tree is undirected; we must build an adjacency list and ignore the parent edge during DFS.

- **Complexity expectation:**  
  Each node is entered and left once, all operations are `O(1)`. Overall time `O(n)`, extra memory `O(n)` for adjacency list, `dist` array, and the dictionary.

## worker: finalize
- The problem asks for the longest *downward* path (ancestor → descendant) whose node values are all distinct.  
- While walking from the root, the current path is a simple list (the recursion stack). The distinct‑value condition on this list is exactly the classic “longest sub‑array with distinct elements”.  
- A sliding‑window (two‑pointer) technique works online: keep a left border `start_depth` such that the sub‑path `nodes[start_depth … cur_depth]` has all distinct values. When a duplicate value appears at depth `prev`, we move the left border to `max(start_depth, prev+1)`.  
- For each node we know:
  * `cur_dist` – total edge length from the root,
  * `cur_depth` – depth (index) of the node,
  * `depth_dist[d]` – distance from the root to the node at depth `d`,
  * `last_pos[value]` – most recent depth where that value occurs on the current path.
- The longest special path ending at the current node has length `cur_dist - depth_dist[start_depth]` and node count `cur_depth - start_depth + 1`.  
- We keep a global best pair `(best_len, best_cnt)`, updating when a longer path is found, or when a path of the same length has fewer nodes.  
- Backtracking restores `start_depth` and the entry for the current value in `last_pos` so that sibling sub‑trees are processed correctly.  
- Complexity: each node is visited once, all operations are `O(1)`. Total time `O(n)`, extra memory `O(n)` (adjacency list, `depth_dist`, `last_pos`, recursion stack).  
- The implementation raises the recursion limit to safely handle a chain of up to `5·10⁴` nodes.
