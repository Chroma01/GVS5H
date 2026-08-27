
## ideation
- Core difficulty: this is a global exact-cover/partition problem on a tree, but tree structure makes edge decisions locally forced by subtree sizes modulo `K`.
- Interpretation pitfall: statement says “length K” but the matrix has `K` vertices per row and `K-1` adjacency constraints, so each part is a path on exactly `K` vertices.
- Key equivalence: choose edges to delete so every remaining connected component is a path with exactly `K` vertices. A kept component must have max degree ≤ 2 and size `K`.
- Forced-edge insight after rooting: for edge `parent-child` with child subtree size `s`, all fully contained components inside the child subtree contribute multiples of `K`. If `s % K == 0`, the edge must be cut; otherwise exactly one path must cross the edge, contributing `s % K` vertices on the child side, so the edge is forced to be kept.
- After keeping exactly forced edges, validation is still needed: kept components could have degree ≥ 3 or size not equal to `K` despite modular consistency. Check each kept component has size `K` and max degree ≤ 2.
- Edge cases: `K=1` cuts every edge and requires all singleton components; `N=1` requires the whole tree itself to be one path; deep trees require iterative DFS or increased recursion limits.
- Complexity target is `O(NK)`; DP over subsets/matchings is infeasible.

## worker: Implement the complete Python solution: parse inpu
- **Parsing**: reads all of stdin at once with `sys.stdin.buffer.read().split()` for speed; `total = N*K` vertices and `total-1` edges.
- **Rooting & subtree sizes**: iterative DFS from vertex 1 produces `parent[]` and a traversal `order`; accumulating `size[parent] += size[child]` over `reversed(order)` gives all subtree sizes in O(NK), avoiding recursion-depth issues on deep trees.
- **Forced edges**: for each non-root node, the edge to its parent is kept iff `size[node] % K != 0`. Rationale: inside the child subtree, all completed K-vertex paths contribute multiples of K; if the subtree size is a multiple of K the edge must be cut, otherwise exactly one path must cross it (carrying `size % K` vertices from the child side), so it is forced to be kept.
- **Validation**: kept edges are unioned in a DSU with component-size tracking, and `kept_deg` counts kept edges per vertex. The decomposition is valid iff every vertex has kept-degree ≤ 2 (each kept component is a path, not a branch) and every DSU component has exactly K vertices. Modular consistency alone is not sufficient (a vertex could be incident to 3 forced edges), so both checks are required.
- **Edge cases**: `K=1` cuts all edges → all singleton components of size 1 → always Yes. `N=1` keeps all edges → Yes iff the whole tree is a path (degree check). Single-vertex tree works trivially.
- **Complexity**: O(NK · α(NK)) time, O(NK) memory.
