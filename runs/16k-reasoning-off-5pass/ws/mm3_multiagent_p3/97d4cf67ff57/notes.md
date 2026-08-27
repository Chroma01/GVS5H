
## ideation
**Core difficulty:** Find a connected subgraph (tree) of the given tree T where every node has degree 1 or 4, with at least one degree-4 node, maximizing vertex count.

**Key observations:**
- Alkane structure: each degree-4 node has 4 branches ending in leaves; a leaf is a degree-1 node.
- We can pick any connected subset, so we can "prune" branches not used.
- Tree DP on a rooted tree is natural: for each node, decide how many of its child-edges are kept in the subgraph.

**DP states per node u (parent p, children c1..ck):**
- `dp0[u]`: max vertices in a valid subgraph within u's subtree, with NO edge to parent used (u may be absent or present as a hub connecting only its children).
- `dp1[u]`: max vertices where the edge to parent IS used, so u is present, and within its subtree u acts as a leaf or a hub with exactly 3 used child-edges (0 or 3 children used).
- `dp2[u]`: max vertices where u is present, parent edge used, and u is an internal degree-4 node (exactly 3 child-edges used).

Base: leaf → `dp0=0, dp1=1, dp2=-inf` (since degree-4 requires ≥4 children, impossible at leaf).

**Transitions:**
- Collect `cand = [dp1[ci] + 1 for each child ci]` (adding the child vertex and the edge to u).
- `best4 = sum of top 4 values` (with -inf for missing). `best3 = sum of top 3`, `best1 = max`, `best0 = 0`.
- `dp0[u] = max( best4, best1 )` — u can be a hub using 4 child edges, or only 1 (leaf) but that gives 1 vertex, but since we don't require u→parent, we allow it.
  Actually: `dp0[u] = best4` (u is a hub) — wait, also could be `0` if we exclude u.
- `dp1[u] = max( best0, best3 )` — u connects to parent, either as leaf (0 child edges) or as degree-4 hub (3 child edges).
- `dp2[u] = best3` — u is hub, needs 3 children, parent edge present.

**Alkane validity:** Need at least one degree-4 node and total vertices ≥ 5. A hub exists when we use exactly 4 children at some node, or 3 children when parent edge is present. So we must ensure the chosen configuration has ≥1 hub.

Tricky part: in `dp0`, if we pick 4 children but u is the root (no parent), u becomes a hub → valid. If u has a parent but edge to parent not used, using 4 children still makes u a hub → valid (since alkane is a standalone tree, u's branch is the alkane).

For `dp1` and `dp2`, the alkane is a subtree continuing upward; we just propagate sizes.

**Final answer:** 
- For the root r, `dp0[r]` already represents a valid alkane if it has a hub. If root has no parent, `dp1[r]` means root connects "up" to nothing — but that edge doesn't exist, so we should consider `max(dp0[r], dp1[r])` with the condition that the chosen configuration actually contains a degree-4 node.
- Use a separate flag `has_hub` tracked in DP, or equivalently, accept `dp0[u]` only if `best4 > 0` and the number of valid children is 4, or `dp1`/`dp2` only if 3 child edges used.

Cleaner approach: track two values per state: (max_size, has_hub_bool). Compare by size, tiebreak by has_hub. A solution is valid iff `has_hub == True`.

**Complexity:** O(N log N) due to sorting per node (sum of k log k = N log N overall, or use nth_element/insertion since total children = N-1 → O(N log N) fine, or O(N) with careful merging).

**Pitfalls:**
- Must output -1 if no valid alkane exists.
- Minimum alkane: 1 degree-4 node + 4 leaves = 5 vertices.
- State `dp2` may be -inf; be careful with comparisons.
- When root is the hub, it has no parent, so we can't use `dp1[root]` directly unless we interpret it as "root connects to nothing" which is just `dp0` essentially. Actually, `dp1[r]` = max size where parent edge used, but root has no parent, so treat root specially: answer = `dp0[r]` with has_hub check. Or include both since if root has no parent, `dp1` means edge to nonexistent parent, invalid — skip `dp1` for root.
- Need to ensure "at least one degree-4" globally: hub can be any node in the subgraph, not necessarily root.

**Final answer formula for root r:**
- ans = max size among valid (size, True) configurations. For root, this is `dp0[r]` with hub flag.

## worker: Root the tree at node 1 with an iterative DFS (sta
The solution uses a tree DP with three states per node (`dp0`, `dp1`, `dp2`) tracking `(size, has_hub)`. The tree is rooted at node 1 using an iterative DFS to avoid recursion depth issues. For each node, we greedily select the best children to form degree-4 hubs (using exactly 4 children in `dp0` or exactly 3 children in `dp1`/`dp2`). The final answer is the maximum valid alkane size over the root's `dp0` and all children's `dp0` (to capture alkanes entirely within subtrees), requiring `has_hub=True` and size ≥ 5 (minimum 1 hub + 4 leaves).

## worker: Implement a corrected Python solution for the alka
The solution uses tree DP with states `(size, has_hub)` per node. After rooting at node 1 and processing in postorder, each node considers which children to keep (using `dp1[child]+1` as the cost of including that child via the connecting edge). 

Key states:
- `dp0[u]`: best alkane in u's subtree where the edge to u's parent is NOT used. u is either absent or is a hub with 4 child-edges.
- `dp1[u]`: edge to parent IS used; u is present as a leaf (0 child-edges) or a hub (3 child-edges).
- `dp2[u]`: same as dp1 but u MUST be a hub (for cleaner propagation).

The greedy selection picks the top-k children by their `dp1+1` values. The final answer scans all nodes' `dp0` values (since an alkane could live in any subtree, not just the one containing the root) and picks the maximum with `has_hub=True` and `size >= 5`. Time complexity is O(N log N) due to sorting children at each node (total children = N-1).

## worker: Validate the current solution against all three sa
I validated the solution against all three sample inputs:

**Sample 1** (9 nodes, star-like):
```
9
1 2
2 3
3 4
4 5
2 6
2 7
3 8
3 9
```
Output: `8` ✓ (matches expected)

**Sample 2** (7 nodes, binary tree):
```
7
1 2
1 3
2 4
2 5
3 6
3 7
```
Output: `-1` ✓ (no degree-4 node possible, max degree is 3)

**Sample 3** (15 nodes):
Output: `11` ✓ (matches expected)

**Key correctness points verified:**
- `topk(k)` properly propagates `has_hub` via bitwise OR of the children's hub flags, so any subtree containing a degree-4 node correctly marks the parent path as having a hub.
- `dp1` for a node with no children correctly gives `(1, 0)` — the node is a leaf (size 1, no hub), which allows it to serve as a leaf branch of a parent hub.
- `dp2` is `(NEG, 0)` for leaves, correctly preventing a leaf from being a hub.
- The final scan over all `dp0[u]` values correctly captures alkanes in any subtree, not just the one rooted at node 1.
- The constraint `size >= 5` (minimum 1 hub + 4 leaves) and `has_hub == 1` together ensure alkane validity.

The `has_hub` propagation in `topk` was the critical fix: it must OR (not just AND) the children's hub flags since a hub can exist in any selected child branch. The final selection logic scans all nodes' `dp0` to find the globally maximum valid alkane.
