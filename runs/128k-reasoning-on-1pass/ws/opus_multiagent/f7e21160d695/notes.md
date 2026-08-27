
## ideation
**Core reduction.** f(x,y) is the bottleneck (minimax) path weight, which equals the maximum edge weight on the x–y path in any MST. Equivalently, in Kruskal order, f(x,y) = the weight of the edge that first merges x and y into the same DSU component. This makes the distance an **ultrametric**: d(x,y) ≤ max(d(x,z), d(z,y)), and the "components at threshold t" form a laminar (hierarchical) family.

**Matching under an ultrametric.** We need a minimum-cost perfect matching between multiset A and multiset B (both size K) where cost = bottleneck distance. Key fact: for a hierarchy, the optimal matching is obtained greedily bottom-up — match as many A's with B's as possible as soon as they land in the same component.

*Lower bound argument:* Consider any component C formed strictly before weight w (i.e., any node of the Kruskal merge tree). Any pair (A_i, B_j) with exactly one endpoint inside C must cost ≥ (weight at which C stops being maximal). Summing |cntA(C) − cntB(C)| type quantities over the hierarchy gives a lower bound matched exactly by greedy. Concretely: total cost = Σ over merge events of (#pairs newly matched) × w, and greedy achieves the minimum # of "carried-over" surplus at each level.

**Algorithm.**
1. Sort edges by weight ascending.
2. surplus[v] = cntA[v] − cntB[v]. (Since A_i ≠ B_j for all i,j, no vertex has both A's and B's, so surplus[v] is already "pure": no zero-cost matches possible, and none needed.)
3. Process edges in order with DSU. If endpoints already connected → skip (non-MST edge, contributes nothing). Otherwise, let s1, s2 be surpluses of the two roots. Newly matched pairs = (|s1| + |s2| − |s1+s2|)/2, i.e. min(s1, −s2) if signs differ, else 0. Add pairs × w to answer; merged surplus = s1 + s2.
4. Graph is connected ⇒ after all merges the single component has surplus 0 ⇒ all K pairs matched.

**Pitfalls / details.**
- Duplicates: A can contain repeated vertices, likewise B — must use *counts*, not booleans.
- The guarantee A_i ≠ B_j means no vertex is simultaneously an A-vertex and B-vertex, so no cost-0 pairs; but the count-based formula handles it uniformly anyway.
- Overflow: none in Python (answer up to ~2e5 × 1e9 = 2e14).
- DSU must be iterative (path compression + union by size/rank) to avoid recursion limit with N = 2e5.
- Sorting: only need ascending by w; ties don't matter (any tie order gives the same ultrametric costs — careful: with equal weights, different Kruskal orders give the same f values, so it's safe).
- Performance in Python: read all input with sys.stdin.buffer.read().split() or numpy; consider numpy argsort on the weight array to sort edges quickly; keep DSU arrays as plain lists (often faster than numpy for scalar ops) or use array module.
- Don't compute the MST explicitly and then do LCA/tree-DP — unnecessary; the DSU sweep is enough.
- Careful with the pairs formula sign convention (positive = surplus of A's, negative = surplus of B's).

**Alternative approaches (fallbacks / cross-checks).**
- Build MST, then do a DFS/merge-tree (Kruskal reconstruction tree) and small-to-large; equivalent but heavier.
- Brute force for testing: compute all-pairs bottleneck distances (Floyd–Warshall variant with max) and Hungarian algorithm for small N, K — good for randomized validation against the greedy DSU solution.

## worker: Write the complete Python solution: fast stdin par
- f(x,y) is the bottleneck (minimax) path weight = weight of the edge that first unites x and y in Kruskal order. This yields an ultrametric with a laminar hierarchy of components.
- Optimal matching of multiset A to multiset B under an ultrametric is achieved greedily: match A's with B's as soon as they become co-located in a component. Lower bound: for any component C existing just before threshold w, the number of pairs that must cross out of C is at least |cntA(C) − cntB(C)|, each costing ≥ w; greedy attains exactly this at every hierarchy node.
- Implementation: sort edges ascending by weight; DSU (iterative find with path compression, union by size); each root carries a signed surplus (positive = unmatched A's, negative = unmatched B's). On a real merge at weight w, newly matched pairs = (|s1|+|s2|−|s1+s2|)/2, contributing pairs*w; merged surplus = s1+s2.
- Since A_i ≠ B_j, no vertex holds both A and B tokens, so no zero-cost matches are missed; connectivity guarantees final surplus 0, i.e., all K pairs matched.
- Non-MST edges (endpoints already merged) are skipped; tie-breaking among equal weights doesn't affect the resulting f values.
- Complexity: O(M log M + (N+M)α). Answer fits easily in Python ints (≤ ~2e14).
