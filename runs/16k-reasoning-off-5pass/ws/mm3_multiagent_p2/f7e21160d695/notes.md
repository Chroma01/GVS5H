
## ideation
**Core difficulty:**
We need the minimum total minimax-path-weight sum when matching the multiset of A-vertices with the multiset of B-vertices. The key insight: in any graph, the minimax path weight f(x,y) equals the maximum edge weight on the unique path between x and y in *any* Minimum Spanning Tree (MST). So building an MST reduces the problem to a tree.

**Candidate approaches:**

1. **MST + path-max queries:** Build an MST (Kruskal on M ≤ 2e5). Preprocess with binary lifting to answer max-on-path queries in O(log N). Then for each pair (a_i, b_j) compute f(a_i, b_j) and do optimal matching.

2. **Optimal matching on a metric matrix:** When minimizing sum over a bipartite matching with a symmetric "ultrametric" cost (cost depends only on sorted order, satisfies the rearrangement inequality), the optimal is to sort both lists and pair index-wise. For a tree MST, the cost matrix satisfies the required monotonicity property. So: compute all K values f(A_i, b) for each fixed b, gather as a list, sort, and sum pairwise with a sorted copy of the other side.

3. **Kruskal-like DSU sweeping:** Alternative — sweep edges by weight, union A-vertices and B-vertices in the same component; the first time a component containing an A meets a component containing a B, the current edge weight is the f value. This naturally gives all required f values, and we can sort & pair the resulting lists.

4. **Sorting feasibility check:** Sorting A-values and B-values independently and pairing is optimal because the minimax-on-MST function satisfies the property that f(x,y) only depends on the LCA's max-edge, and for any threshold, the connectivity is a partition — the resulting values form "ultrametric-like" structures where larger values are unavoidable. Standard result: the optimal min-cost perfect matching on a bipartite metric matrix where all row/column multisets are equal can be solved by sorting both sides.

**Pitfalls:**

- MST is not unique but the path-max value is invariant across all MSTs.
- Must use 64-bit integers (weights up to 1e9, K up to 2e5, sum up to 2e14).
- BFS/DFS from each A would be O(NK) — too slow.
- Floyd–Warshall is O(N^3) — too slow.
- Need binary lifting tables sized N×logN.
- K can be up to N (2e5), so storing all K×K f values is too big if we did it naively. We only need f(A_i, B_j) for the sorted-pair approach. We need K values per A_i, which is O(K^2) if we do all pairs. We can instead do: compute the multiset of f-values by processing each A-vertex, and for each B-vertex, query f(A_i, B_j) using binary lifting — that's still O(K^2 log N) which may be 4e10. Need smarter.

**Better plan:**

- For each vertex v in the MST, the function g_v(x) = f(v, x) for varying x is determined by tree structure. We can compute distances from each A-vertex using BFS/DFS in O(N) each — too slow if K is large.
- **Kruskal sweep approach is the right one:** Sort MST edges by weight ascending. Maintain a DSU over N vertices. Also track for each DSU component:
  - count of A-vertices inside (cA)
  - count of B-vertices inside (cB)
  When processing an edge (u,v) of weight w connecting components C1, C2:
    - new cA = cA1 + cA2, new cB = cB1 + cB2
    - pairs newly formed = cA1 * cB2 + cA2 * cB1 (each A in one side paired with each B in the other)
    - total_cost += w * pairs_newly_formed
  This directly computes the sum over ALL K×K pairings. But we need optimal matching, not sum over all pairs!

**Revised approach for optimal matching:**

The optimal matching minimizes sum of f(A_i, B_{π(i)}). Since f is a minimax metric (specifically, for any threshold t, f(x,y) ≤ t iff x and y are connected in the subgraph of edges with weight ≤ t — this is equivalent to saying the graph formed by edges with weight ≤ t is an equivalence relation on vertices, and connectivity defines components).

This property (f is a "bottleneck distance" in an MST) means the function satisfies: for any two thresholds t1 < t2, the partition at t2 is a refinement of the partition at t1. This is exactly the structure of an **ultrametric** restricted to A∪B.

**Key theorem:** For such a function, the minimum cost matching of multiset A to multiset B (with |A| = |B| = K) is achieved by sorting the vertices in A∪B in an order consistent with the refinement hierarchy, and pairing A-vertices and B-vertices in sorted order. More concretely:

- When we do Kruskal-sweep on the MST, at each threshold t, the components partition the graph. The function f restricted to the A and B vertices is the level of their first common ancestor in the Kruskal merge tree.
- The optimal matching can be computed with a **greedy DSU approach on A and B separately**:
  - Process MST edges in increasing order of weight.
  - Maintain two DSUs: one for A-vertices, one for B-vertices (or one DSU on all vertices with separate counts).
  - At each step, when merging components, if any A-vertex becomes connected to any B-vertex (across the components), they "lock in" a pairing at cost = current weight.
  - This is essentially: build a forest on A∪B induced by the MST merge order, then the answer is sum of max-edge-on-path summed over the optimal matching.

**Cleaner formulation (the working solution):**

For each A-vertex a, do a DFS from a over the MST, tracking the current path max. As we reach each B-vertex b, record f(a,b). Do this for all A-vertices. This is O(K * (N + M)) — too slow.

**The real efficient approach (verified technique for this problem type):**

Use the Kruskal reconstruction tree (KRT):
- Build MST via Kruskal. Each time we union two components with edge weight w, create a new node with weight w, and make it the parent of the two component roots.
- The KRT has N + (N-1) = 2N-1 nodes, is a binary tree with original vertices as leaves.
- For any two original vertices x, y, f(x,y) = weight(LCA_KRT(x,y)).

Now, the problem becomes: given K A-leaves and K B-leaves in a tree with weights on internal nodes, pair them to minimize sum of LCA weights.

This is a known problem solvable with the Kruskal-sweep on the KRT with a DSU that tracks A-count and B-count per KRT node, and uses the same "newly paired = cA_left * cB_right + cA_right * cB_left" formula. The result is exactly the sum of LCA weights over the optimal matching, computed in O(N log N) or O(N α(N)).

**Why this greedy works:** The "first time A and B become connected" interpretation, combined with the fact that within a KRT component at the moment of merging, the optimal matching can be determined greedily because the ultrametric property implies that swapping pairings within already-merged components cannot decrease cost. (This is the standard result for this problem.)

**Algorithm:**

1. Build MST using Kruskal: sort edges by weight, union components.
2. Build Kruskal reconstruction tree: for each successful union of edge weight w, create a new node id = ++curr, with weight w, and set parent of the two roots to this new node. New root = curr.
3. After processing all MST edges, the final root has all vertices under it. Total nodes = 2N-1, all leaves are original vertices.
4. DSU pass on KRT (post-order from leaves up):
   - At each internal node, sum cA and cB from its two children.
   - cost += w_node * (cA_left * cB_right + cA_right * cB_left).
5. Output cost.

**Time complexity:** O(M log M) for sorting edges (Kruskal), O(N) for KRT, O(N) for the final DSU sweep. All within limits.

**Verification with sample 1:**
- MST edges: (3,4,1), (1,3,2), (1,4,4), (2,4,5) — wait need to verify: 4 vertices, 4 edges, MST of 3 edges: edges (3,4,1), (1,3,2), (2,4,5). The edge (1,4,4) is excluded.
- KRT: union (3,4) w=1 → node 5, parent of 3,4; union (1,3) w=2 → node 6, parent of 1,5; union (2,5_root=4) w=5 → node 7, parent of 2,6.
- A-vertices (multiset): 1,1,3. B-vertices: 4,4,2.
- At node 5 (w=1): cA=1 (vertex 3), cB=1 (vertex 4). cost += 1 * (1*1 + 0) = 1.
- At node 6 (w=2): children 1 (cA=1, cB=0) and 5 (cA=1, cB=1). cost += 2 * (1*1 + 1*0) = 2.
- At node 7 (w=5): children 2 (cA=0, cB=1) and 6 (cA=2, cB=1). cost += 5 * (0*1 + 2*1) = 10.
- Total: 1+2+10 = 13. But expected answer is 8. Discrepancy!

**Reconsider:** The KRT pairing approach gave 13, but the sample answer is 8. So the "sum of LCA weights over all pairs" is NOT the right formula. We need the OPTIMAL matching, which is the minimum, not the sum over all pairs.

**Correct formula:** At each internal node, the new pairings formed are min(cA_left, cB_right) paired with min(cA_right, cB_left)? No, that's the assignment problem.

Wait, let me reconsider. When two components merge at weight w, we have cA_L A's and cB_L B's on the left, cA_R A's and cB_R B's on the right. The number of new "connections" formed is min(total_A_connected, total_B_connected)? No...

Actually, the number of pairs that "lock in" at weight w is: the number of A-B pairs whose LCA is exactly this node. That is cA_L * cB_R + cA_R * cB_L (all A's on left with all B's on right, and vice versa). This is fixed — it's determined by the tree structure, not by matching.

But in the optimal matching, we might not pair all of them at this LCA! Wait, no. If the LCA of A-vertex a and B-vertex b is node v, then in the optimal matching, the pair (a,b) contributes weight w_v. The sum of weights over all matched pairs is sum over matched (a,b) of weight(LCA(a,b)). 

The key insight: at each internal node v with weight w, among the A's and B's in its subtree, we need to form pairings. The pairings that "leave" this subtree (going to ancestors) are determined by the surplus. The pairings that are "internal" (both A and B are in the same child subtree) contribute to the answer only via deeper nodes.

**The correct greedy (the standard one for this problem):**

At each internal node v with weight w:
- Let (aL, bL) and (aR, bR) be A/B counts in left and right children.
- After processing children, the number of "extra" A's in left = aL - bL (if positive) or extra B's (if aL < bL). Similarly for right.
- These extras must be paired with A's/B's from the other side at this node, contributing w per such pair.
- Number of pairs locked at this node = min(aL, bR) + min(aR, bL) ... no, it's:
  - excess_A_left = max(0, aL - bL), excess_B_left = max(0, bL - aL)
  - excess_A_right = max(0, aR - bR), excess_B_right = max(0, bR - aR)
  - pairs_locked = min(excess_A_left, excess_B_right) + min(excess_A_right, excess_B_left)
  - cost += w * pairs_locked

Let me verify with sample 1:
- Node 5 (w=1): L=3 (a=1,b=0), R=4 (a=0,b=1). excess_A_L=1, excess_B_L=0; excess_A_R=0, excess_B_R=1. pairs = min(1,1)+min(0,0)=1. cost += 1.
- Node 6 (w=2): L=1 (a=1,b=0), R=5 (a=1,b=1). excess_A_L=1, excess_B_L=0; excess_A_R=0, excess_B_R=0. pairs = min(1,0)+min(0,0)=0. cost += 0.
- Node 7 (w=5): L=2 (a=0,b=1), R=6 (a=2,b=1). excess_A_L=0, excess_B_L=1; excess_A_R=1, excess_B_R=0. pairs = min(0,0)+min(1,1)=1. cost += 5.
- Total: 1+0+5 = 6. Still not 8!

Hmm, that's not matching either. Let me reconsider the tree structure.

Sample 1 edges: (1,3,2), (3,4,1), (2,4,5), (1,4,4).
MST (3 edges): (3,4,1), (1,3,2), (2,4,5). Edge (1,4,4) excluded.

A multiset: {1,1,3}, B multiset: {4,4,2}.

f(1,4)=2, f(1,2)=5, f(3,4)=1. Optimal: pair A=1 with B=2 (cost 5), A=1 with B=4 (cost 2), A=3 with B=4 (cost 1). Sum = 8. ✓

f(1,4)=2, f(1,2)=5, f(3,4)=1, f(1,4)=2, f(1,2)=5, f(3,4)=1 (if we look at all 9 pairs). Sort A-values of f: for each b, compute f(a,b):
- b=4: f(1,4)=2, f(1,4)=2, f(3,4)=1 → sorted: [1,2,2]
- b=2: f(1,2)=5, f(1,2)=5, f(3,2)=? 

What's f(3,2)? Path in MST: 3-4-2, max edge = max(1,5) = 5. So f(3,2)=5.
- b=2: [5,5,5]
- b=4: [1,2,2]

So for each A_i, the f values to the 3 B's are:
- A=1: [2,2,5]
- A=1: [2,2,5]
- A=3: [1,5,5]

If we sort each A's B-values and pair... that's for a different matching.

Actually the rearrangement inequality says: for matrices, if we sort each row, then sort the resulting list, we get the minimum sum matching. The resulting sorted list of all f(A_i, B_j) values is the multiset we need to pair with itself? No.

**The correct rearrangement inequality application:**
- Form a K×K matrix M[i][j] = f(A_i, B_j).
- We need min over permutations π of sum_i M[i][π(i)].
- For "ultrametric" matrices, the optimal is achieved by sorting both row-indices and column-indices by the same hierarchical clustering, and pairing correspondingly.

Specifically, if we sort the A-vertices and B-vertices by their position in the Kruskal tree (e.g., the order they get merged), and pair correspondingly, we get the optimal.

In sample 1, sort A by merge order: A={1,1,3}. The leaves merge as: 3 and 4 merge first (at w=1), then 1 joins (at w=2), then 2 joins (at w=5). So order in KRT: leaves [3,4,1,2] in some traversal. 

Let's do the KRT post-order: node 7 (root), children node 2 and node 6. Node 6 children: 1 and node 5. Node 5 children: 3 and 4. Post-order leaves: 3, 4, 1, 2.

A in this order: A leaves are 3, 1, 1. B leaves are 4, 4, 2.
Pair in order: (3,4), (1,4), (1,2). Costs: f(3,4)=1, f(1,4)=2, f(1,2)=5. Sum=8. ✓

So the algorithm is: pair A and B in the order they appear in a post-order (or any consistent) traversal of the KRT leaves.

**The correct greedy for cost calculation:**

Process KRT nodes in post-order. At each internal node v with weight w:
- It has two children L, R. After processing children, L has some A's and B's that are "unmatched within L", R has some that are "unmatched within R".
- The unmatched must be paired across L and R at cost w.
- The number of such cross-pairings = unmatched count from L + unmatched count from R? No...

Let's define: after processing child L, let net_L = cA_L - cB_L (positive means extra A's, negative means extra B's). Similarly net_R.
- The number of cross-pairings at node v = |net_L| + |net_R| - |net_L + net_R|? No, simpler: the cross pairings consume the surplus on each side.
- The total "items" (A's + B's) in subtree v = cA_v + cB_v = total items.
- The number of pairs that can be formed within v is min(cA_v, cB_v).
- The number of cross-pairings at v = (min(cA_L, cB_L) + min(cA_R, cB_R)) + (items paired across) = min(cA_v, cB_v).
- So cross pairings at v = min(cA_v, cB_v) - min(cA_L, cB_L) - min(cA_R, cB_R).
- And cost += w * cross_pairings.

Let me verify:
- Node 5 (w=1): cA=1, cB=1. min=1. Children: L (vertex 3) cA=1,cB=0, min=0. R (vertex 4) cA=0,cB=1, min=0. Cross = 1-0-0=1. cost += 1*1=1.
- Node 6 (w=2): cA=2 (1+1), cB=1 (0+1). min=1. Children: L (v1) min(1,0)=0. R (node5) min(1,1)=1. Cross = 1-0-1=0. cost += 0.
- Node 7 (w=5): cA=2 (0+2), cB=2 (1+1). min=2. Children: L (v2) min(0,1)=0. R (node6) min(2,1)=1. Cross = 2-0-1=1. cost += 5*1=5.
- Total: 1+0+5=6. Still wrong!

Hmm. The issue is that node 6 doesn't pair anything, so the "1" from node 5 (pairing 3 with 4) propagates up. Then at node 7, we need to pair 2 more A's (the two 1's) with 1 more B (the 2). But there's only 1 B, so only 1 cross-pairing at node 7, giving cost 5. Total 1+5=6. But the answer is 8.

I think the issue is that I was computing min(cA_v, cB_v) at each node, but the cross-pairings at v are only those A-B pairs whose LCA is exactly v. The total number of such pairs is cA_L * cB_R + cA_R * cB_L, not based on min.

In sample 1:
- Node 5: cross = 1*1 + 0*0 = 1. ✓ (pair 3 with 4)
- Node 6: cross = 1*1 + 1*0 = 1. (pair A=1 with B=4 from node 5's side, but B=4 is already paired at node 5!)

Ah, so the formula cA_L * cB_R + cA_R * cB_L counts all A-B pairs whose LCA is v, but in an optimal matching, we don't pair all of them — we only pair the ones that "need to be" paired at this level.

The correct formula: at each internal node, the number of pairings whose LCA is v is determined by the matching. Specifically, if we denote p_v = number of pairings fully contained in subtree v, then p_v = p_L + p_R + cross_v, where cross_v is the number of A-B pairs matched across L and R. And cross_v is constrained by: it can't exceed the available A's in L and B's in R, etc.

The minimum total cost matching, by the ultrametric property, is achieved by a "greedy bottom-up" matching where at each node, we match as many as possible across the two children, and the unmatched propagate up.

Specifically:
- At node v, after matching within children, we have unmatched_A_L, unmatched_B_L, unmatched_A_R, unmatched_B_R.
- We match min(unmatched_A_L, unmatched_B_R) + min(unmatched_A_R, unmatched_B_L) across.
- cost += w * (these cross matchings).
- New unmatched: 
  - unmatched_A = (unmatched_A_L - min(unmatched_A_L, unmatched_B_R)) + (unmatched_A_R - min(unmatched_A_R, unmatched_B_L))
  - similarly for B.

For sample 1:
- Node 5 (w=1): L=v3 (unmatched_A=1, unmatched_B=0), R=v4 (0,1). cross = min(1,1)+min(0,0)=1. cost+=1. new: A=(1-1)+(0-0)=0, B=(0-0)+(1-0)=1.
- Node 6 (w=2): L=v1 (1,0), R=node5 (0,1). cross = min(1,1)+min(0,0)=1. cost+=2. new: A=0, B=0.
- Node 7 (w=5): L=v2 (0,1), R=node6 (2,1)... wait, after node 6, unmatched are (0,0), but we still have the A's and B's that were "absorbed" into pairings. 

Hmm, I need to track: within a subtree, some A's and B's are paired (and contribute to cost at their LCA), and the "unmatched" ones are the ones whose partner is outside the subtree.

After node 6: within node 6's subtree, we have 2 A's and 1 B. We paired 1 A with 1 B (at node 6, cost 2). So 1 A is unmatched, 0 B unmatched. Net = +1 A.

At node 7: L=v2 (1 B), R=node6 (1 A, 0 B unmatched). cross = min(0,0)+min(1,1)=1. cost += 5. Total: 1+2+5=8. ✓

So the algorithm is:
1. Build KRT from MST.
2. Post-order traversal. At each leaf (original vertex), set unmatched_A = 1 if vertex in A-multiset, unmatched_B = 1 if in B-multiset (using multiset counts, can have >1).
3. At each internal node v with weight w:
   - cross = min(unmatched_A_L, unmatched_B_R) + min(unmatched_A_R, unmatched_B_L)
   - cost += w * cross
   - unmatched_A_v = unmatched_A_L + unmatched_A_R - cross_with_B
     where cross_with_B = min(unmatched_A_L, unmatched_B_R) + min(unmatched_A_R, unmatched_B_L)
     Actually: unmatched_A_v = (unmatched_A_L - min(unmatched_A_L, unmatched_B_R)) + (unmatched_A_R - min(unmatched_A_R, unmatched_B_L))
   - similarly for B.

This works! And it's O(N).

**Implementation details:**

- Vertices 1..N are original. KRT nodes are N+1 .. 2N-1.
- When unioning in Kruskal (building MST), we maintain DSU. Each union creates a new node with weight = edge weight, and the two roots become its children.
- Actually, for KRT, we typically have: when we union two components, create a new node. But we only do this for MST edges, not all edges.
- Use DSU to track components. When processing an MST edge (u,v,w) and u,v are in different components, create a new node `new_id` with weight w, and union the DSU sets, setting the new root to new_id.
- For the unmatched_A and unmatched_B at leaves, use the multiset counts. Since vertices can appear multiple times, we need counts.

Let me double-check the KRT building for the "not all nodes" case: we have N leaves and N-1 internal nodes (for a tree). Total 2N-1 nodes.

For the post-order, we need to know the tree structure of the KRT. Each internal node has two children (the roots of the two components being merged). So we can build a tree with parent pointers.

After all unions, the final root is the root of the KRT. We do a recursive post-order DFS from the root to compute the unmatched counts and cost.

**Edge case:** What if all A's and B's are matched within subtrees and no cross-matchings are needed at the root? The total should be 0 for the "leftover" unmatched at root, which should be 0 (since |multiset A| = |multiset B| = K).

Let me verify with sample 2:
- 3 vertices, edges: (1,2,5), (2,3,2), (1,3,1).
- MST: (1,3,1), (2,3,2). (1,2,5) excluded.
- A: {1,1}, B: {2,3}.
- KRT: 
  - Union (1,3) w=1 → node 4, children 1, 3.
  - Union (2, 4) w=2 → node 5, children 2, 4.
- Post-order:
  - Leaf 1: unmatched_A=2 (since A has two 1's), unmatched_B=0.
  - Leaf 2: unmatched_A=0, unmatched_B=1.
  - Leaf 3: unmatched_A=0, unmatched_B=1.
  - Node 4 (w=1): L=(2,0), R=(0,1). cross = min(2,1)+min(0,0)=1. cost += 1*1=1. new: A=(2-1)+(0-0)=1, B=(0-0)+(1-0)=1.
  - Node 5 (w=2): L=(0,1), R=(1,1). cross = min(0,1)+min(1,1)=1. cost += 2*1=2. new: A=(0-0)+(1-1)=0, B=(1-1)+(1-1)=0.
- Total: 1+2=3. ✓

The algorithm works.

**Final algorithm summary:**

1. Read N, M, K.
2. Read M edges.
3. Read A list (length K) and B list (length K).
4. Build MST using Kruskal: sort edges by weight, union with DSU. But we also build the KRT:
   - When we union two components with edge weight w, create a new node id = N + (++counter), set its weight = w, and its left/right children = the two component roots.
   - The new component's representative = new_id.
5. After Kruskal, we have 2N-1 nodes. The final representative is the root of the KRT.
6. Post-order DFS from the KRT root:
   - At each node, return (unmatched_A, unmatched_B, accumulated_cost).
   - If leaf (id <= N): unmatched_A = count of id in A multiset, unmatched_B = count of id in B multiset.
   - Else: recursively process children, then compute cross and new unmatched as above.
7. Print total cost.

**Data structures:**
- Edges: list of (w, u, v). Sort by w.
- DSU with parent array.
- KRT children: left[N+1..2N-1], right[N+1..2N-1], weight[N+1..2N-1].
- Count arrays: cntA[1..N], cntB[1..N].

**Potential issues:**
- The KRT has N-1 internal nodes. We need to map DSU root to the KRT node. Use an array `dsu_node[1..2N-1]` where dsu_node[representative] = the KRT node id.
- When we union two components, the new KRT node becomes the new representative, and dsu_node[new_rep] = new_krt_id.

**Time:** O(M log M) for Kruskal, O(N) for DFS. Total O((N+M) log M) which is fine for 2e5.

**Space:** O(N + M) for edges and KRT.

I'm confident this is the correct approach. Let me code it up.

One more verification: what if K=0? The problem says K >= 1, so no issue.

What if some A_i == A_j (repeated)? Handled by cntA (can be > 1).

What if the graph is already a tree (M = N-1)? MST is the graph itself, KRT is the tree, algorithm works.

What if multiple edges have the same weight? Kruskal handles ties by processing in any order; the MST property is maintained.

Alright, ready to implement.</mm:think>### NOTES

**Core difficulty:** We need to minimize the sum of minimax path weights when matching two multisets A and B of size K. The minimax path weight f(x,y) equals the max edge weight on the path between x and y in *any* MST.

**Key insight (Kruskal Reconstruction Tree):** When we run Kruskal on the MST and create a new node for each successful union (with weight = edge weight), we get a binary tree where:
- Leaves = original vertices
- Internal node weight = the edge weight that merged its two subtrees
- f(x,y) = weight of LCA(x,y) in this tree

The optimal matching can be computed greedily bottom-up: at each internal node of weight w, match the "surplus" A's on one side with surplus B's on the other side, at cost w per such cross-pairing.

**Algorithm verified against samples:**
- Sample 1 → 8 ✓
- Sample 2 → 3 ✓

**Pitfalls:**
- Must use 64-bit arithmetic (sum can be up to 2e14)
- Multiset vertices (same vertex can appear multiple times) → use count arrays
- KRT has 2N-1 nodes, need to track which DSU representative maps to which KRT node
- DFS post-order must handle both children correctly

## worker: Implement the solution: read input, build MST with
Implemented the Kruskal Reconstruction Tree approach:

1. **Build MST + KRT via Kruskal:** Sort edges by weight. For each edge that connects two different DSU components, create a new KRT node with weight = edge weight and children = the two component roots. The new node becomes the DSU component's representative in the KRT.

2. **Post-order DFS with surplus matching:** For each internal KRT node with weight w, after processing children, match the "surplus" A vertices on one side with surplus B vertices on the other side: `cross = min(aL, bR) + min(aR, bL)`. Add `w * cross` to the answer. Propagate the remaining unmatched counts up the tree.

3. **Leaf handling:** Use count arrays `cntA` and `cntB` to handle multiset entries (vertices can appear multiple times).

4. **Verification:** Tested against both samples — Sample 1 gives 8, Sample 2 gives 3.

The algorithm is O(M log M + N α(N)) and handles N, M ≤ 2×10⁵ efficiently. Uses 64-bit integers via Python's arbitrary precision.
