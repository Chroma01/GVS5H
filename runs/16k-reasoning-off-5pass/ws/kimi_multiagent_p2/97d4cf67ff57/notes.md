
## ideation
The core difficulty: an alkane is a connected subtree where internal vertices have degree exactly 4 and boundary vertices degree 1. So we need the largest connected subgraph where every included vertex keeps either 0 or 3 of its children (when rooted, with parent edge counting toward degree), except the "topmost" vertex which keeps exactly 4 children (degree 4 without a parent). Key observations:

- Any alkane has a unique structure: pick any degree-4 vertex as the "root" of the alkane; then every other vertex is either a leaf (keeps 0 children) or degree-4 (keeps 3 children + parent edge).
- So DP: root T at vertex 1. For each node v, compute g[v] = max number of vertices in a valid partial alkane within v's subtree where v is included and v's parent edge is used (so v must keep exactly 3 children, each of which also uses their parent edge). g[v] = 1 + sum of g[c] over the 3 chosen children with largest g[c] (only children with g[c] defined/positive count; a child could also be excluded entirely).
- Wait — children kept must themselves be valid: a kept child c uses edge (v,c), so c needs exactly 3 kept children too. So g[c] = 1 + sum of top-3 g-values among c's children. If c has fewer than 3 children, g[c] is invalid (-inf).
- Then the answer: for each node v as the alkane's top vertex (degree 4, no parent), value = 1 + sum of top-4 g-values among v's children (need at least 4 children with valid g). Take max over all v. If none, -1.
- Also leaves of the alkane: a kept child that keeps 0 children is a leaf — but wait, if child c is kept, c's degree in subgraph = 1 (edge to v) + kept children. For c to be a leaf, it keeps 0 children, degree 1 — that's valid! So actually a kept child can be in two modes: leaf (keep 0 children, contributes 1 vertex) or internal (keep exactly 3 children, contributes g[c]). So g[v] = 1 + sum over exactly 3 chosen children of best[c], where best[c] = max(1, g[c]) — i.e., child as a leaf contributes 1, or as internal contributes g[c] if valid.
- Similarly the top vertex: 1 + sum over exactly 4 chosen children of best[c].
- Edge cases: N small (need at least 5 vertices: 1 internal + 4 leaves). Single vertex, paths, etc. naturally yield -1. Also note the alkane's top vertex must have degree ≥ 4 in T... not exactly — it needs 4 children in the rooted tree, meaning degree ≥ 4 if v is not root of T, or degree ≥ 4 as root (root has no parent so needs 4 children = degree ≥ 4). Hmm, but the alkane's top vertex could also use its parent edge in T? No — the top vertex is defined as having no parent in the subgraph. But any alkane rooted at any of its degree-4 vertices works; when we root T at vertex 1, the alkane's highest vertex (closest to T's root) has no parent in the subgraph, so it needs 4 children in T. That's fine — every alkane has a unique highest vertex, and we enumerate it. But careful: the highest vertex's parent edge in T is simply unused. Good.
- Pitfall: g[c] could be invalid (fewer than 3 children); best[c] = max(1, g[c]) handles it since leaf mode always available. Also choosing "exactly 3 children" — we pick the 3 largest best[c] values; all are ≥ 1 so always pick top 3 if ≥ 3 children exist.
- Complexity O(N) after computing for each node the top-4 best values among children.

## worker: Write the final Python solution: parse input, root
- Root T at vertex 1. For a node v included in the alkane:
  - If v uses its parent edge, it needs total degree 4 (internal) → keep exactly 3 children, or degree 1 (leaf) → keep 0 children. So a kept child c contributes `best[c] = max(1, g[c])` where `g[c]` is the value when c is internal (keeps exactly 3 children).
  - `g[v] = 1 + sum of top-3 best[c]` over children, valid only if v has ≥ 3 children.
  - The alkane's highest vertex (no parent in subgraph) must keep exactly 4 children: candidate `= 1 + sum of top-4 best[c]`, valid if ≥ 4 children.
- Every alkane has a unique highest vertex relative to the rooting, so enumerating all v as that top vertex covers all alkanes. Answer is the max candidate, or -1 if none exists.
- Verified against samples:
  - Sample 1: node 2 as top keeps children 1 (leaf), 3 (internal with children 4,8,9), 6, 7 → 1 + 1 + 4 + 1 + 1 = 8. ✓
  - Sample 2: no node has ≥ 4 children with valid values → -1. ✓
  - Sample 3: yields 11. ✓
- Complexity: O(N) time (each node keeps only top-4 child values), O(N) memory. Iterative DFS avoids recursion limits.

## worker: Verify the solution against samples and edge cases
**Verification of the algorithm:**

An alkane is a connected subtree where every vertex has degree 1 (leaf) or 4 (internal), with ≥ 1 internal vertex. Root T at vertex 1. Any alkane has a unique *highest* vertex (closest to T's root), which uses no parent edge and must keep exactly 4 children. Every other included vertex uses its parent edge, so it either keeps 0 children (leaf, degree 1) or exactly 3 children (internal, degree 4).

- `best[c] = max(1, g[c])`: a kept child contributes 1 as a leaf, or `g[c]` as an internal node. Since `g[c] ≥ 4` when valid (1 + three children each ≥ 1), `max(1, g[c])` never wrongly prefers leaf mode for a valid internal child, and `g[c] = NEG` (invalid, < 3 children) safely degrades to 1.
- `g[v] = 1 + top-3 best values` (requires ≥ 3 children).
- Answer candidate at v: `1 + top-4 best values` (requires ≥ 4 children). Max over all v, else -1.

**Sample traces:**
- **Sample 1** (answer 8): Node 3 has children 4, 8, 9 → g[3] = 1+1+1+1 = 4. Node 2 has children 1, 3, 6, 7 → best = 1, 4, 1, 1 → candidate = 1+4+1+1+1 = 8. ✓
- **Sample 2** (answer -1): Root 1 has only 2 children; nodes 2 and 3 have 2 children each. No node has ≥ 4 children → ans stays -1. ✓
- **Sample 3** (answer 11): Tree edges give node 1 children {12, 9, 5} (parent 0, rooted at 1): adjacency — 1 connects to 12, 15, 5, 9. Rooting at 1: children of 1 are 12, 15, 5, 9 (4 children). Node 5's children: 8, 10, 4 → g[5] = 4. Node 9's children: 2, 3, 6 → g[9] = 1+1+1+ g[6]... node 6's children: 11, 14 → only 2 children, g[6] invalid → best[6] = 1. So g[9] = 1+1+1+1 = 4. Node 12's children: 7 → g invalid. Candidate at 1: 1 + best[12]=1 + best[15]=1 + best[5]=4 + best[9]=4 = 11. ✓

**Edge cases:**
- **N < 5** (e.g., N=1, single edge, path of 4): no node has ≥ 4 children → -1. Correct, since minimum alkane has 5 vertices.
- **Star graph K₁,₄** (center + 4 leaves): center has 4 children, all leaves → candidate = 5. Correct (smallest alkane).
- **Star K₁,₃**: center has 3 children → g[center] = 4 but no candidate → -1. Correct.
- **Deep chain (path)**: every node has ≤ 1 child → -1. Correct.
- **Root with exactly 4 children**: handled since root's parent is 0 and all 4 neighbors are counted as children.
- **Invalid g values**: `val = g[u] if g[u] > 1 else 1` maps NEG → 1 (leaf mode), so invalid internal states never pollute sums.
- **Non-root internal alkane vertex with parent in T**: the highest alkane vertex never uses its T-parent edge; all lower vertices do. Enumeration over all v covers every alkane exactly once. ✓

**Complexity:** O(N) time (top-4 selection is O(1) per edge), O(N) memory. Iterative DFS avoids recursion limits for N = 2×10⁵.
