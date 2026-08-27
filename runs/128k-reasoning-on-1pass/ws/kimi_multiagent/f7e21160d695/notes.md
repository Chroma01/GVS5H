
## ideation
Core difficulty: K can be Θ(N), so computing all K^2 costs f(A_i,B_j) or running generic assignment is impossible. The cost f(x,y) is a minimax/bottleneck distance: in an undirected graph it equals the maximum edge on the unique x-y path in any MST, equivalently the Kruskal time when x and y first become connected. Thus the problem becomes minimum-cost bipartite matching between two multisets under an ultrametric/hierarchical clustering induced by Kruskal.

Key greedy invariant: process MST edges in nondecreasing weight with DSU. For each component store only signed surplus diff = #unmatched A - #unmatched B; a component should never need to keep both types because internal A-B pairs would already have been matched no later than when they became connected. When unioning two components by an edge of weight w, if diffs have opposite signs, match min(abs(diff1), abs(diff2)) pairs across the cut and add matched*w; new diff is diff1+diff2. Matching as many opposite surpluses as possible at the current cheapest threshold is optimal because all cross-component pairs now have the same bottleneck cost w, and leaving them unmatched only forces later cost ≥ w.

Correctness support: MST gives minimum bottleneck paths by cut/cycle exchange. Kruskal components define an ultrametric; in an ultrametric, an optimal assignment can be transformed so no pair is matched later than necessary while an opposite-type surplus exists in another merging component.

Pitfalls: duplicate vertices in A/B require multiplicity counts, not sets. The guarantee A_i != B_j only means the value sets are disjoint; A and B may each contain repeats. Use 64-bit/Python arbitrary precision for answer. Equal-weight edges are safe if processed with the same current weight, but batching equal weights can simplify reasoning. Do not output a permutation. Beware recursion depth if implementing tree DP; DSU avoids it. Graph is connected, so final surplus must be zero.

Complexity target: O(M log M + (N+M) α(N) + K), memory O(N+M).

## worker: Implement the complete Python solution: fast parsi
- **Minimax property**: For an undirected graph, f(x,y) equals the maximum edge weight on the unique x–y path in any MST, i.e., the Kruskal threshold at which x and y first become connected. So only MST structure matters.
- **Algorithm**: Sort edges by weight (Kruskal). Maintain DSU where each component root stores its *signed surplus* `diff = (#unmatched A) − (#unmatched B)`. The invariant is that a component never holds both unmatched A's and B's, because any such pair would already have been matched at the cheapest threshold when they became connected.
- When merging two components via an edge of weight `w`, every cross-component pair has bottleneck cost exactly `w` (all intra-component MST edges have weight ≤ w). If the two surpluses have opposite signs, match `min(|d1|,|d2|)` pairs and add `matched * w` to the answer; the new surplus is `d1 + d2`. Matching greedily at the earliest (cheapest) possible threshold is optimal for this ultrametric cost, since deferring a match can only cost ≥ w.
- Duplicates in A and B are handled naturally via multiplicity counts. The guarantee `A_i ≠ B_j` isn't even needed for correctness of the surplus method.
- Verified against both samples: Sample 1 → 1 + 2 + 5 = 8; Sample 2 → 1 + 2 = 3.
- **Complexity**: O(M log M) for sorting, O((N+M) α(N)) for DSU, O(K) for counting; memory O(N+M). Python ints handle the large answer (up to ~2·10⁵ · 10⁹).

## worker: Validate against brute force on small random graph
- Uses the minimax/MST property: `f(x,y)` is the Kruskal threshold when `x` and `y` first become connected, equivalently the max edge on the MST path.
- DSU processes edges in increasing weight. Each component keeps only net surplus `diff = #A - #B`; opposite signs across a merge are matched immediately at the current cheapest possible cost.
- Validation against brute force: for small `N <= 8`, connected random graphs, `K <= 5`, compute all-pairs `f` by threshold DSU/minimax and enumerate all `K!` assignments of `B`; compare with the greedy surplus total. Covered duplicates in `A`/`B`, disjoint value sets, equal edge weights, path/star MST shapes, `K=1`, disconnected-before-threshold cases, and weights up to `1e9`. The greedy earliest-matching invariant agrees with exhaustive optimum; samples give `8` and `3`.
- Complexity: `O(M log M)` sorting, `O((N+M) α(N) + K)` DSU/counting, `O(N+M)` memory. Python integers handle the maximum answer safely.
