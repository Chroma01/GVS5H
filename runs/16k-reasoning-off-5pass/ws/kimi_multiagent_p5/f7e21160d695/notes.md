
## ideation
The core of the problem: f(x,y) is the minimax distance (minimize the maximum edge weight along a path). A classical result: f(x,y) equals the maximum edge weight on the unique path between x and y in any Minimum Spanning Tree (Kruskal tree). So step one is Kruskal → MST (O(M log M)), then answer max-edge-on-path queries via binary lifting (O((N+Q) log N)).

The second part: we have K "left" nodes (A_i, with repetition allowed) and K "right" nodes (B_j, with repetition allowed), cost matrix C[i][j] = f(A_i, B_j), and we need a minimum-cost perfect matching (assignment problem). The guarantee A_i ≠ B_j means no trivial zero-cost diagonal traps.

Key difficulty: K can be up to N = 2×10⁵. Hungarian algorithm is O(K³) — utterly infeasible for large K. Even building the K×K cost matrix is O(K² log N), infeasible for K ~ 2×10⁵. So the crux is exploiting the special structure of minimax distances:

- f values are ultrametric-like: f(x,y) ≤ W means x and y lie in the same connected component of the subgraph formed by MST edges with weight ≤ W. Equivalently, consider the Kruskal reconstruction tree (DSU tree): f(x,y) = weight of the LCA of x and y in the reconstruction tree. This is an ultrametric.
- Assignment with ultrametric costs likely admits a greedy: process reconstruction-tree nodes bottom-up (increasing weight); within each component, match as many A's and B's as possible internally at that node's weight, passing unmatched counts upward. Since all pairs within a component merged at weight W have cost ≤ W (exactly W if their LCAs are this node), an optimal strategy: at each DSU-tree node, match leftover A's with leftover B's from its child subtrees at cost = node weight. Because any cross-component pair costs at least this node's weight, matching internally as much as possible is optimal (exchange argument). The total cost = sum over reconstruction-tree nodes of (number of pairs matched at that node) × node weight.
- This works even with duplicate vertices in A or B (multiset counts per leaf). The condition A_i ≠ B_j doesn't even seem necessary for this greedy, but it may simplify edge cases (e.g., it prevents pairing identical indices? No — pairing is by position, and A_i = B_j as vertex values is disallowed, so every pair has positive cost; but greedy doesn't need it).

Pitfalls:
- A and B are multisets (sample 1 has A = [1,1,3], B = [4,4,2]). Count multiplicities per vertex.
- Reconstruction tree: N leaves (original vertices), N-1 internal nodes each with weight = edge weight that merged components. LCA weight = f value. Tree has 2N-1 nodes; build with DSU during Kruskal.
- Greedy at internal node v with children c1..ck: each child passes up (a_c, b_c) = unmatched A-count and B-count. Within node v, total A = sum a_c, total B = sum b_c; matched here = min(totalA, totalB) at cost w_v; pass up (totalA - m, totalB - m). Wait — but matching within the node across children all costs w_v, so just min of sums. Pass up leftovers. At the root, totals must match (both K), so everything gets matched. Sum of m_v × w_v is the answer.
- Proof sketch: any matching must match the A's inside a subtree; if subtree has more A's than B's, at least (a−b) A's must be matched outside at cost ≥ w_v... standard min-cost flow on a tree argument. This is equivalent to earth-mover/min-cost matching on tree metric with costs at LCA — greedy bottom-up is optimal.
- Actually careful: cost of matching across children of v is exactly w_v only if the two leaves' LCA is v; if both leftovers come from the same child they'd have been matched deeper. Since each child passes up only the excess of one side (a child can't pass up both A-excess and B-excess), any cross matching at v pairs items from different children whose LCA is exactly v. Good.
- Answer can be large: K × 10⁹ up to 2×10¹⁴ — use 64-bit.

Alternative approach if the tree-greedy proof is doubted: min-cost flow on the reconstruction tree (same thing). Hungarian only viable for K ≤ ~300; not the intended solution given constraints.

## worker: Implement the full solution in Python: Kruskal rec
- f(x,y) is the minimax distance = max edge weight on the unique MST path = weight of LCA of x and y in the Kruskal reconstruction tree (DSU tree). Built during Kruskal: each successful union creates a new internal node with that edge's weight, whose children are the two component roots.
- Greedy bottom-up: at each internal node v, all unmatched A's and B's passed up from its children can be paired at cost exactly w_v (their LCA is v since each child passes up only one-sided excess). Match as many as possible: m = min(totalA, totalB), add m·w_v to the answer, pass the one-sided remainder upward. This is optimal by the standard exchange argument: any pair matched across node v's subtree boundary costs ≥ w_v, and matching internally never hurts since all internal cross-child pairs cost exactly w_v.
- Handles multisets (duplicate vertices in A or B) via per-leaf counts. Answer fits in Python int (no overflow concern).
- Complexity: O(M log M + N α(N) + total tree size) ≈ O(M log M + N). Memory O(N). Works for K up to 2·10⁵.
- Verified mentally on samples: Sample 1 → MST edges weights 1 (3-4), 2 (1-3), 5 (2-4). Reconstruction: node4 (w=1, children 3,4... wait children vertices 3 and 4 i.e. 0-indexed 2,3), node5 (w=2, children vertex1(0) and node4), node6 (w=5, children vertex2(1) and node5). A counts: vertex1:2, vertex3:1. B counts: vertex4:2, vertex2:1. Node4: a=1,b=1 → m=1, ans+=1, pass (0,0). Node5: a=2,b=0 → m=0, pass (2,0). Node6: a=2, b=1(from leaf vertex2)+0=1 → m=1, ans+=5, pass (1,0)... wait that leaves 1 A unmatched. Hmm — recount: B = [4,4,2] → vertex4:2, vertex2:1. Node4 (children vertices 3,4): a=1 (A has one 3), b=2 → m=1, ans=1, pass (0,1). Node5 (children vertex1, node4): a=2, b=1 → m=1, ans=1+2=3, pass (1,0). Node6 (children vertex2, node5): a=1, b=1 → m=1, ans=3+5=8. ✓ matches sample output 8.
- Sample 2: MST edges 1 (1-3), 2 (2-3). Node3 (w=1, children v1,v3), node4 (w=2, children v2, node3). A=[1,1] → v1:2. B=[2,3] → v2:1, v3:1. Node3: a=2,b=1 → m=1, ans=1, pass (1,0). Node4: a=1, b=1 → m=1, ans=1+2=3. ✓ matches sample output 3.

## worker: Verify the ultrametric/LCA property and greedy opt
**Verification of the ultrametric/LCA property:**
- f(x,y) = min over paths of (max edge weight on path) is the minimax distance. Classic result: f(x,y) equals the max edge weight on the unique x–y path in any MST. Proof: the MST path's max edge W gives a path with max ≤ W; conversely, if a path with max < W existed, the heaviest MST-path edge could be swapped out to get a lighter spanning tree — contradiction (cut property).
- In the Kruskal reconstruction tree (each union at weight w creates an internal node of weight w whose children are the two merged component roots), two leaves x, y first become connected exactly when the internal node LCA(x,y) is created, so f(x,y) = weight[LCA(x,y)]. Weights are nondecreasing along any rootward path (Kruskal processes edges in sorted order).

**Greedy optimality (cut argument):**
- For each internal node v with subtree S: any perfect matching must match at least |A(S) − B(S)| items across the cut (S, V\S). Every cross-cut pair has LCA at v or above, hence cost ≥ w_v. Summing these per-node lower bounds (each pair is charged exactly at its LCA, since a pair with LCA u crosses the cut of u but of no descendant) gives: answer ≥ Σ_v m_v · w_v where m_v is the number of pairs whose LCA is v, and the cut constraints force Σ over the appropriate nodes to be at least the greedy's matching counts.
- Greedy achieves all bounds simultaneously: process nodes bottom-up. Each child passes up only a one-sided excess (it matched min(a,b) internally). At node v, all leftover A's and B's come from *different* children, so any pairing among them has LCA exactly v and cost exactly w_v. Matching m = min(totalA, totalB) pairs at w_v is therefore optimal — any pair left unmatched at v would cost ≥ w_parent(v) ≥ w_v later, never less. Induction over the tree gives global optimality; at the root, totalA = totalB = K so everything is matched.

**Sample checks (by hand):**
- Sample 1: MST edges 1(3-4), 2(1-3), 5(2-4). Reconstruction: n4(w=1; v3,v4), n5(w=2; v1,n4), n6(w=5; v2,n5). A={v1:2, v3:1}, B={v4:2, v2:1}. n4: m=1, ans=1, pass (0,1). n5: m=1, ans=3, pass (1,0). n6: m=1, ans=8. ✓
- Sample 2: MST edges 1(1-3), 2(2-3). n3(w=1; v1,v3), n4(w=2; v2,n3). A={v1:2}, B={v2:1, v3:1}. n3: m=1, ans=1, pass (1,0). n4: m=1, ans=3. ✓

**Edge cases:**
- K=1: single pair, greedy matches at the LCA of the two vertices — correct.
- Equal weights: multiple internal nodes with same w; matching at any of them costs the same, greedy remains valid (weights nondecreasing upward suffices).
- Duplicates in A/B: handled via per-leaf multiplicity counts (sample 1 exercises this).
- Magnitude: answer ≤ K·10⁹ ≤ 2·10¹⁴; Python ints unbounded, no overflow.
- A_i ≠ B_j guarantee is not even needed by the algorithm (a zero-cost self-pair would just be matched at leaf level for free), so no special handling required.
- Complexity: O(M log M + N) time, O(N) memory; recursion avoided (iterative post-order), safe for N = 2·10⁵.
