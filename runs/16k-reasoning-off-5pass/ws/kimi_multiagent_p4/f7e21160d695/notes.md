
## ideation
The problem asks for a minimum-cost perfect matching between multiset A and multiset B where the cost f(x,y) is the minimax path value in the graph. Key facts and difficulties:

1. **Minimax = MST path max**: f(x,y) equals the maximum edge weight on the unique x–y path in any MST (Kruskal). So the graph reduces to a tree.

2. **K can be 2e5**, so building a K×K cost matrix and running Hungarian/assignment algorithms (O(K²) memory, O(K³) time) is impossible. We need to exploit the metric structure.

3. **Threshold structure**: f(x,y) ≤ t iff x and y are in the same connected component of the subgraph using only edges with weight ≤ t. As t increases (process Kruskal edges in increasing order), components merge. The cost of pairing a specific A with a specific B is exactly the weight of the Kruskal edge at which their components first merge (in the MST, equivalently in the incremental DSU over sorted edges).

4. **Greedy matching by processing edges in increasing weight**: Maintain DSU over all N vertices, adding MST edges in increasing weight. Each component tracks the number of unmatched A-vertices and unmatched B-vertices inside it. When a merge creates a component containing both unmatched A's and unmatched B's, match min(countA, countB) pairs at the current edge weight w, adding min*w to the answer, and reduce counts. This is optimal by an exchange argument: any pair matched later (at higher threshold) could be swapped to be matched at the earliest moment both sides coexist in a component; delaying never helps because costs are monotone in threshold and all pairs within a component have the same current "availability" cost w. More formally, the optimal total equals sum over matched pairs of their merge time, and matching greedily at each merge event minimizes the number of pairs forced to pay higher thresholds (a Hall-type argument: at threshold t, pairs with cost ≤ t must lie within components; maximizing the number matched early minimizes later costs).

   Caveat: multiple A's or B's can be on the same vertex? Constraints say A_i ≠ B_j for all i,j, but A's may repeat among themselves and B's may repeat (Sample 1 has A = (1,1,3), B = (4,4,2)). So counts per vertex, not flags. Also a vertex can hold multiple A's (count >1). A_i ≠ B_j guarantees no vertex is both an A and a B... actually it guarantees every A vertex differs from every B vertex, so the sets of vertices are disjoint. Good: each vertex is either A-side (with multiplicity), B-side (with multiplicity), or neither.

5. **Implementation**: 
   - Kruskal: sort M edges by weight, build DSU, select N-1 MST edges. Actually we don't even need to explicitly build the MST: we can process all edges in sorted order with a second DSU (or reuse), and only edges that merge two different components are MST edges; those are exactly the events. So one pass: sort edges, iterate, on successful union check counts and match.
   - DSU arrays: parent, size, cntA, cntB (int64 counts). Initialize cntA[v] = multiplicity of v in A, similarly cntB.
   - For each edge (u,v,w) in sorted order: find roots ru, rv; if same, skip. Before merging, any matching within ru or rv alone was already done. After union, newA = cntA[ru]+cntA[rv], newB = cntB[ru]+cntB[rv]; matched = min(newA, newB); but careful: matches that could have happened inside ru or rv at lower weight already happened, leaving cntA[ru], cntB[ru] with at least one of them zero (invariant: within each component, min(cntA,cntB)=0). So after merge, matched = min(newA,newB), answer += matched*w, then set: if newA>=newB: newA-=newB, newB=0 else symmetric. Maintain invariant.
   - Answer accumulates in 64-bit (weights up to 1e9, K up to 2e5 → up to 2e14, fits in int64; Python int unbounded anyway).

6. **Correctness of greedy (sketch)**: Consider thresholds. Each matched pair's cost = merge time of their vertices. Total = sum over pairs. Equivalent reformulation: sum of costs = sum over distinct edge-weight thresholds of (number of pairs whose cost ≥ that threshold)... More precisely cost = sum_{t < cost} 1 over unit thresholds, so total = Σ_t (K − pairs matched with cost ≤ t). To minimize total, at each threshold maximize the number of pairs matchable within components of edges ≤ t. Within a component at threshold t, max pairs = min(#A, #B) summed over components — and greedy achieves exactly this because it matches as many as possible at each merge, and the invariant (each component has only one side left) means the total matched so far equals Σ min over components. Since any matching's count of pairs with cost ≤ t is bounded by Σ_components min(A,B) at threshold t, greedy is optimal at every threshold simultaneously, hence minimizes the total. 

7. **Pitfalls**:
   - Multiplicities (A and B are sequences with possible repeats) — use counts.
   - Skip non-MST edges (same root) — they create no new connectivity.
   - 64-bit answer.
   - 1-indexed vertices.
   - Recursion limits — use iterative find with path compression.
   - Input size 2e5 lines — use fast IO (sys.stdin.buffer.read).

8. Complexity: O(M log M) sorting + O((M+K) α(N)). Fine.

## worker: Implement solve() in Python: fast input parsing vi
- f(x,y) is the minimax path value, equal to the max edge on the x–y path in any MST. Processing edges in increasing weight with DSU simulates Kruskal; the cost of pairing an A-vertex with a B-vertex equals the weight of the edge whose addition first connects their components.
- Greedy: each DSU component maintains unmatched counts cntA, cntB with invariant min(cntA, cntB) = 0 (all possible matches inside a component were already made at lower thresholds). On merging two components via edge weight w, match min(totalA, totalB) pairs at cost w each. Optimality: for any threshold t, the number of pairs with cost ≤ t in any matching is at most Σ over components min(#A, #B); greedy achieves this bound at every threshold, minimizing the total sum.
- Multiplicities handled via counts (A's and B's may repeat within themselves; A-vertices and B-vertices are disjoint by the constraint A_i ≠ B_j).
- Verified mentally on samples: Sample 1 → edges sorted (1:3-4, 2:1-3, 4:1-4, 5:2-4). cntA: {1:2, 3:1}, cntB: {4:2, 2:1}. Edge w=1 merges 3(A=1) and 4(B=2): match 1, ans=1, comp {3,4}: A=0,B=1. Edge w=2 merges 1(A=2): match min(2,1)=1, ans=3, comp: A=1,B=0. Edge w=4: same component, skip. Edge w=5 merges 2(B=1): match 1, ans=8. ✓ Sample 2 → edges (1:1-3, 2:2-3, 5:1-2). A={1:2}, B={2:1,3:1}. w=1 merges 1(A=2),3(B=1): match 1, ans=1, A=1,B=0. w=2 merges 2(B=1): match 1, ans=3. ✓
- Fast IO via buffer read, iterative find with path compression, union by size. Python ints handle the up-to-2e14 answer automatically.

## worker: Verify the implementation against samples and edge
**Verification against samples and edge cases:**

**Sample 1** (N=4, M=4, K=3, A=(1,1,3), B=(4,4,2)): cntA={0:2, 2:1}, cntB={3:2, 1:1}. Edges sorted: (1,3-4), (2,1-3), (4,1-4), (5,2-4).
- w=1: merge 3(A=1) & 4(B=2) → match 1, ans=1, comp: A=0,B=1.
- w=2: merge 1(A=2) → match min(2,1)=1, ans=3, comp: A=1,B=0.
- w=4: same root, skipped (non-MST edge correctly ignored).
- w=5: merge 2(B=1) → match 1, ans=8. ✓

**Sample 2** (N=3, K=2, A=(1,1), B=(2,3)): w=1 merges 1(A=2)&3(B=1) → ans=1, A=1,B=0; w=2 merges 2(B=1) → ans=3. ✓

**Edge cases checked:**
- **K=1**: single A and single B on distinct vertices; matches exactly once at their merge-time edge weight = f(A,B). ✓
- **Equal weights**: sort is stable but order among equal-weight edges doesn't matter — all matches made during any merge at weight w pay w, which equals the threshold cost regardless of tie order. ✓
- **Multiplicities**: counts (not flags) per vertex; A-vertices and B-vertices are disjoint by the constraint A_i ≠ B_j, so no vertex needs both counts. Invariant min(cntA,cntB)=0 per component is maintained after every merge. ✓
- **Non-MST edges**: `ru == rv` → skipped; they add no connectivity so no new matches. ✓
- **64-bit answer**: max K·w = 2e5·1e9 = 2e14; Python ints are unbounded. ✓
- **Performance**: O(M log M) sort + near-constant amortized DSU with path compression + union by size; fast buffer input handles 2e5 lines. ✓

**Optimality proof (sketch):** f(x,y) equals the weight of the Kruskal edge at which x,y first become connected. Writing total cost as Σ_t (K − #pairs with cost ≤ t), minimizing the sum requires maximizing pairs matched within components at every threshold t. Any matching can match at most Σ_components min(#A,#B) pairs within threshold-t components; the greedy achieves exactly this bound at every merge event (invariant: each component holds only one side), hence is simultaneously optimal at all thresholds.
