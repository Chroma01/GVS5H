
## ideation
- Key identity: if an alkane has `k` degree-4 vertices and `l` leaves, then `4k + l = 2(k+l-1)`, so `l = 2k + 2` and total vertices `= 3k + 2`. Thus maximizing vertices is equivalent to maximizing `k`, the number of degree-4 vertices.
- A vertex can be degree 4 in the chosen subtree only if its original degree is at least 4. Call these vertices eligible.
- Because `T` is a tree, any connected chosen vertex set must include every tree edge between chosen adjacent vertices; otherwise those endpoints become disconnected. So the chosen subtree is effectively induced on its vertex set.
- The chosen degree-4 vertices `C` must form a connected subgraph of the forest induced by eligible vertices, and within `C` each vertex can have at most 4 chosen core neighbors. Original degree `>=4` is not enough by itself if too many eligible neighbors are also chosen.
- Feasibility lemma to verify: for any connected eligible set `C` with max internal degree `<=4`, the remaining `4 - deg_C(v)` slots of each `v` can be filled by distinct non-core neighbors. A non-core vertex cannot be adjacent to two vertices of connected `C`, otherwise `T` would contain a cycle; hence leaf choices do not conflict.
- The provided DP matches this reduction: root each eligible component; `g[u]` = best core size containing `u` when its parent is also core, so `u` may take at most 3 children; `h[u]` = best when `u` is the top of the core, taking at most 4 children. Since all weights are positive, choose the largest child `g` values. Answer is `3*best_core + 2`, or `-1` if `best_core == 0`.
- Pitfalls: assuming an entire eligible component is always usable even when some vertex has eligible-degree `>4`; confusing original degree with selected core degree; recursion depth for `N=2e5`; forgetting `N=1`/no eligible vertices; accidentally requiring exactly degree 4 in the original tree rather than at least 4; off-by-one in the `3k+2` formula.

## worker: Implement the full O(N) solution: read the tree fr
- Implemented exactly the planned O(N) algorithm:
  1. Read tree, build adjacency lists.
  2. Mark eligible vertices (original degree ≥ 4) — only these can be degree-4 vertices of the alkane.
  3. For each connected component of the eligible-induced forest, do an iterative DFS (explicit stack) recording `order` and `parent`, then process in reverse order (post-order).
  4. For each vertex `u`, keep the top-4 child `g` values (`t1..t4`). `g[u] = 1 + t1 + t2 + t3` (core continuing upward through parent, so only 3 child slots); `h[u] = 1 + t1 + t2 + t3 + t4` (core tops out at `u`, 4 child slots). Track `best_core = max h`.
  5. Answer: `3*best_core + 2` if any eligible vertex exists, else `-1`.
- Correctness reasoning:
  - For an alkane with `k` degree-4 vertices and `l` leaves, the degree sum gives `4k + l = 2(k + l - 1)`, hence `l = 2k + 2` and total vertices `= 3k + 2`. So maximizing vertices ≡ maximizing `k`.
  - The degree-4 vertices (core) must be eligible and form a connected set with internal degree ≤ 4. Conversely, any such connected set can be extended to an alkane: each core vertex `v` needs `4 - deg_C(v)` leaf neighbors, which exist in `T` since `deg_T(v) ≥ 4`, and no non-core vertex is adjacent to two core vertices (that would create a cycle in the tree `T`), so leaf assignments never conflict.
  - The DP computes the maximum connected core: rooting each eligible component, `g[u]` is the best core containing `u` and extending toward its parent (≤3 children), `h[u]` the best core whose highest vertex is `u` (≤4 children). Since all child contributions are positive (≥1), taking the top values is optimal, and any connected core has a unique highest vertex where it is counted by `h`.
- Complexity: O(N) time and memory; iterative, so no recursion-depth issues for N = 2×10⁵.
- Verified against samples mentally: Sample 1 → best_core = 2 (vertices 2,3) → 8; Sample 2 → no vertex with degree ≥ 4 → -1; Sample 3 → best_core = 3 → 11.
