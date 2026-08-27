We need to minimize sum of f(A_i, B_{π(i)}) where f(x,y) is the minimax edge weight (minimum possible maximum edge weight on a path). This f can be computed by MST: f(x,y) equals the maximum edge weight on the unique path between x and y in the Minimum Spanning Forest (here a tree). So we build an MST of the graph (Kruskal), then answer queries for max edge on path between any two vertices using LCA with binary lifting (storing max on the way up). After we have all K×K f values, we need to assign B vertices to A vertices minimizing total sum. This is a minimum weight perfect matching on a bipartite graph with K up to 2e5, so a special structure is needed. Observation: since A_i and B_i are both vertices, we can consider for each A_i we compute distances to all B's. We need min sum pairing = assignment problem, but K can be large. The constraint "A_i ≠ B_j" only removes self matches but does not give structure. However, looking at typical solutions for similar problems (AtCoder ABC 287 F or similar?), the assignment can be done greedily if we sort by some value? Actually the cost f(A_i, B_j) depends only on max edge on path, which is a tree metric. There may be a property allowing a simple matching: sort A and B by Euler tour order on the tree, then optimal pairing is to match in order. Let's analyze: For a tree metric where cost is the maximum edge weight on path, the distance matrix is a "bottleneck" distance. Is the assignment problem solved by matching sorted by dfs order? I recall a known result: for a tree, the minimum weight perfect matching of pairs (Ai, Bπ(i)) where cost is sum of distances can be solved via Hungarian but here cost is max edge. However there is known problem "Minimize sum of minmax path weight" which is exactly this AtCoder problem (ABC 287 Ex? No). Let me search memory: I think this is AtCoder ABC 287 F? No. Actually I recall a problem "Minimum Sum of Max Edge on Path" from AtCoder typical tasks. The solution: build MST, then sort A and B by their depth-first in-time (Euler tour order), then pairing greedily yields optimal. This is due to the property that for any two pairs (a,b) and (c,d) with a<c and b<d in Euler order, swapping yields no better total cost? Let's verify with counterexample: tree is a line with weights increasing, vertices 1-2-3-4 with weights: 1-2 weight 1, 2-3 weight 10, 3-4 weight 1. So f(x,y) = max edge on path. Consider A = [1,4], B = [2,3]. Euler order: 1,2,3,4. Sorted A: 1,4; sorted B: 2,3. Pairing yields f(1,2)=1, f(4,3)=1, sum=2. Alternative pairing f(1,3)=10, f(4,2)=10 sum=20. So sorted works.

But is there a case where sorted pairing is not optimal? Let's think: the cost matrix is a "Kalmanson" matrix? For max edge weight, the matrix satisfies the four-point condition? Possibly leads to optimal matching being monotone in some ordering. I think the known solution: sort A and B by the time of first appearance in DFS order (i.e., tin) of the MST, then pair in that order. Because for any i<j and p<q, swapping the pairs does not improve total cost. Let's try to prove or find counterexample.

We need to show that for any four vertices a<b<c<d (in tin order), and two pairs (a,c) and (b,d), we have f(a,c)+f(b,d) ≤ f(a,b)+f(c,d) (or the opposite depending on monotonicity). This is similar to the property that max edge path cost satisfies the quadrangle inequality: f(a,c)+f(b,d) ≤ max(f(a,b),f(b,c))+max(f(b,c),f(c,d))? Not clear.

But many editorial solutions for this exact problem (I think from AtCoder ABC 287 Ex? Actually I recall "ABC 270 F" is about transportation. Let me search memory: The problem "Permute B" with f defined as min max edge appears in AtCoder "ABC 269 F"? Not sure. I will search mental repository: The problem might be "AtCoder Grand Contest 029 - F" no. Let me just recall: There's an AtCoder problem "ABC 245 F" about pair matching. Not.

Let's step back: the assignment is a classic problem: "minimum sum of distances on a tree" can be solved by sorting by Euler tour order (for sum of distances, it's known that optimal matching pairs i-th in one set with i-th in other set when both sets are sorted by Euler order). Indeed, for sum of distances (edge weight sum) the matrix of distances on a tree is "Kalmanson" which satisfies the Monge property, and the assignment problem with Monge cost matrix can be solved greedily (matching sorted order). For max edge weight, the cost might also be Monge? Let's test. Monge property: for all i<k and j<l, C[i][j] + C[k][l] ≤ C[i][l] + C[k][j]. For max edge path cost, does this hold? Example line 1-2 (weight 5), 2-3 (weight 1). Vertices 1,2,3. Compute matrix (i from A set, j from B set). Let A = {1,3}, B={2,3}. Then C[1][2] = max(5)=5, C[3][3] = 0? Actually f(3,3) = 0? But f(x,x) is 0? However constraint A_i ≠ B_j so we don't need self matches. But matrix includes self zeros. Let's test Monge: i=1,k=2 (A indices 1 and 3), j=1,l=2 (B indices 2 and 3). C[1][1] = f(1,2)=5, C[2][2] = f(3,3)=0 (if self allowed). C[1][2] = f(1,3)=5 (max of 5 and 1). C[2][1] = f(3,2)=1. Then C[1][1]+C[2][2] =5+0=5, C[1][2]+C[2][1] =5+1=6. So 5 ≤ 6 holds. Another test: i=1 (A=1), k=2 (A=3), j=2 (B=3), l=1 (B=2) but j<l required, so not.

I suspect the cost matrix is Monge for max edge path on a tree. If so, optimal assignment is to sort both sets and pair them. The problem constraints are large K up to N (2e5), so we need O((N+M) log N) or similar.

Thus solution steps:

1. Build MST using Kruskal: sort edges by weight ascending, union-find. Complexity O(M log M).
2. Build adjacency list of MST (N-1 edges).
3. Preprocess LCA with binary lifting (maxEdge up to logN ~ 18). We need function maxOnPath(u, v) = max edge weight on path between u and v in MST.
4. For each i compute f(A_i, B_j) for all j? That's K^2 up to 4e10 impossible. Instead, we need to sort A and B by Euler order, then match correspondingly: total sum = sum_i maxOnPath(sortedA[i], sortedB[i]).

Thus we need to prove that pairing in Euler order yields minimum sum. I recall the editorial for this exact problem indeed uses sorting by Euler tour order. So implement that.

Let's confirm with sample 1: MST edges sorted: (3-4,1), (1-3,2), (1-4,4) or (2-4,5) whichever. Build MST: edges with smallest weights: (3-4,1), (1-3,2), (1-4,4) (connects 1-4 via 1-3-4 but that would create cycle? Actually 1-3-4 already connects 1 to 4 via 1-3 (2) + 3-4 (1) so adding 1-4 (4) would create cycle, so MST edges: (3-4,1), (1-3,2), (2-4,5) maybe. Let's run Kruskal: edges sorted: (3-4,1) add, (1-3,2) add, (1-4,4) would create cycle (1-3-4-1) skip, (2-4,5) add connecting component 2. So MST edges: weights 1,2,5. Compute tin: root at 1 maybe. Tree structure: 1-3 weight2, 3-4 weight1, 4-2 weight5. Euler order (DFS) from 1: order: 1,3,4,2. So tin: 1->1,3->2,4->3,2->4. A: [1,1,3] -> sorted tin order: vertices 1(tin1),1(tin1),3(tin2) => list = [1,1,3] (same). B: [4,4,2] -> sorted tin: 4(tin3),4(tin3),2(tin4) => list = [4,4,2]. Pair: f(1,4)=2, f(1,4)=2, f(3,2)=? Path 3-4-2: edges 1 and 5, max =5. Sum =2+2+5=9? But sample answer is 8 with pairing (1,2), (1,4), (3,4). That's not sorted order. Let's compute sorted pairing sum: 2+2+5=9 > 8. So sorting by Euler order does NOT give optimal for this case. So our assumption is wrong. Let's verify my calculation: Actually we need to sort A and B by their tin values, but the MST may have a different structure leading to different order. Let's compute f values exactly from MST: MST edges: 3-4 weight1, 1-3 weight2, 2-4 weight5. Compute f using max edge on path:
- f(1,2): path 1-3-4-2: max(2,1,5)=5.
- f(1,4): path 1-3-4: max(2,1)=2.
- f(3,4): path 3-4: max(1)=1.
- f(1,1): 0.
- f(3,2): path 3-4-2: max(1,5)=5.
Sorted order gave 2+2+5=9. But optimal is 8 as sample: pair 1-2 (5), 1-4 (2), 3-4 (1). This pairs sorted A[0]=1 with B[0]=2, sorted A[1]=1 with B[1]=4, sorted A[2]=3 with B[2]=4. That is exactly sorted by tin of B? B's sorted tin: 4(tin3),4(tin3),2(tin4). But they paired 1 with 2 (tin4) first, then 1 with 4, then 3 with 4. So pairing is not in order of sorted A vs sorted B, but they matched each A with some B. Let's try pairing in order of sorted A and sorted B but maybe they use some other ordering like sort by depth or something else? Let's try sort B by descending tin: 2(tin4),4(tin3),4(tin3) => pairing 1-2 (5),1-4 (2),3-4 (1) sum=8. So using reversed order yields optimum. Interesting.

What is reversed order? It corresponds to pairing smallest A with largest B, etc. This is like minimizing sum of bottleneck distances; it's like assignment problem on a line metric (max edge path) where the cost matrix might be anti-Monge (i.e., C[i][j] + C[k][l] ≥ C[i][l] + C[k][j] for i<k, j<l). Let's test: earlier we computed 5 ≤ 6, not anti-Monge. But maybe with self zeros removed? Let's check property for the actual assignment. It seems we need to consider sorting A by tin ascending, and B by tin descending (or vice versa). But not sure.

Let's test with sample 2: N=3, edges: (1-2,5), (2-3,2), (1-3,1). MST: choose smallest edges: (1-3,1), (2-3,2). MST edges: 1-3 (1), 2-3 (2). Tree: root at 1. DFS: 1(tin1),3(tin2),2(tin3). A: [1,1] (both 1) -> sorted A: [1,1]. B: [2,3] -> sorted B: [2(tin3),3(tin2)] = [2,3] ascending tin gives [3,2]? Wait B sorted ascending tin: 3(tin2),2(tin3) => [3,2]. Pairing A sorted ascending with B sorted ascending yields f(1,3)=1, f(1,2)=max(1,2)=2, sum=3 (optimal). Pairing A ascending with B descending yields f(1,2)=2, f(1,3)=1 sum=3 also same. So both give optimal.

Thus we need a more robust solution: compute f values for each A with each B, but K can be up to 2e5, impossible to compute all pairs. However note that we can treat the problem as assignment where cost is max edge path weight; there is known solution: sort A and B by some order and pair them directly; the order is the order of vertices in Euler tour of MST (maybe inorder) but we saw sample1 needed reversed B. Let's examine more.

Maybe the correct ordering is sort A by tin, and sort B by tin, then match the smallest A with the smallest B, but that gave 9 > 8. So maybe we need to sort B by tin of the vertex in MST that is farthest from A? Not.

Let's re-evaluate the problem: f(x,y) = min possible max edge weight path = max edge weight on the MST path. The assignment problem: min sum of f(A_i, B_{π(i)}). Since f is symmetric and 0 on same vertices, but A_i != B_j always. We need to find a min cost perfect matching between sets A and B. The graph of costs is defined on vertices of the MST, we need to find min sum. This is a classic problem: "minimum weight perfect matching in a tree metric where weight is max edge" - can be solved by sorting by some order, maybe by the "centroid"? Let's think.

Consider constructing an auxiliary structure: For each A, we can consider distances (max edge) to all B, but we need to pick assignment. This is essentially a minimum cost bipartite matching where each A is matched to a distinct B. Since K can be up to N, O(K^2) is too big. The cost matrix has a special structure: it depends only on max edge on path. Is there an algorithm like Hungarian in O(K log N) for this matrix? Possibly using min-cost max-flow on a tree? Might be reducible to assignment of intervals.

I recall a known problem: AtCoder ABC 210 F? Not.

Let's search memory: There is a problem "Maximum matching on a tree" where cost is maximum edge weight, and you need to match K pairs to minimize sum. I think the solution is to sort A and B by depth, or by Euler tour order, then match accordingly, but the direction may depend on whether the tree is rooted and you sort by entry time, and the optimal is to match A's sorted by tin with B's sorted by tin in the same order. However sample1 contradicts. Did we compute tin correctly? Let's recompute MST for sample1 again more carefully.

Edges:
1: 1-3 weight2
2: 3-4 weight1
3: 2-4 weight5
4: 1-4 weight4

Kruskal:
- weight1: (3-4) add.
- weight2: (1-3) add (connects 1 with component of 3-4).
- weight4: (1-4) would create cycle 1-3-4-1, skip.
- weight5: (2-4) add (connects 2).

Thus MST edges: (3-4,1), (1-3,2), (2-4,5). Yes.

Now we need to root the tree arbitrarily. Choose root = 1. Then adjacency:
1-3 (2)
3-4 (1)
4-2 (5)

DFS order (preorder) from root 1: stack: 1 visited, then neighbor 3, then neighbor 4, then neighbor 2. So order: 1,3,4,2. So tin: 1->1, 3->2, 4->3, 2->4.

Now A list: [1,1,3]; B list: [4,4,2].

Sorted A by tin: [1(t1),1(t1),3(t2)] -> same list.
Sorted B by tin: vertices sorted by tin: 4(t3), 4(t3), 2(t4). So B sorted ascending = [4,4,2] as we used.

Now sum f(A_i,B_i) = f(1,4)+f(1,4)+f(3,2) = 2+2+5 = 9.

But sample answer is 8 with pairing: (1,2), (1,4), (3,4). That's B list permuted to [2,4,4] which in tin order is 2(t4),4(t3),4(t3) descending. So they sorted B descending tin: [2,4,4] yields sum = f(1,2)=5, f(1,4)=2, f(3,4)=1 =8.

So pairing A sorted ascending tin with B sorted descending tin gives optimal for this case. But is that always true? Let's test sample2: A: [1,1] (both 1). B: [2,3] with tin: 2->3, 3->2. Descending B = [2,3]; sum = f(1,2)+f(1,3) = 2+1=3 optimal. Ascending B = [3,2] sum = 1+2=3 same.

What about other cases? Let's try a small tree where optimal is not monotone. Suppose tree is a star: center 0 with leaves a,b,c with edge weights w_a, w_b, w_c. A set = leaves a,b; B set = leaves b,c. Then f(x,y) = weight of edge connecting x if they are different leaves (since path x-0-y has max of the two edge weights). Let's set weights: a=1, b=10, c=2. So f(a,b)=max(1,10)=10, f(a,c)=max(1,2)=2, f(b,c)=max(10,2)=10. Assignment:
- Pair a with b (10), b with c (10) sum=20.
- Pair a with c (2), b with b (0 but not allowed) - but b is in B, so we need match A's both to B's distinct: A={a,b}, B={b,c}. If we match a-c (2) and b-b (0) not allowed (A_i != B_j, but b matched to itself is not allowed). So we must match b to c (10) sum=12. That's optimal: 12.

Now sort A by some order: maybe by weight of edge? If we sort by tin (Euler) on star: root 0, preorder visits children in some order (say a,b,c). Then tin: a=1,b=2,c=3. So A sorted: a,b. B sorted ascending: b,c. Pair a-b =10, b-c=10 sum=20 not optimal. Sorted descending B: c,b => a-c=2, b-b (0) not allowed. Actually a-c=2, b-b (0) not allowed. So that fails.

Thus the simple sorting by tin (either direction) fails for star case. Let's compute actual f values: A = {a,b}, B = {b,c}. f matrix:
- f(a,b)=10
- f(a,c)=2
- f(b,b)=0 (invalid)
- f(b,c)=10

We need to choose one assignment (matching) that pairs a to either b or c, b to the other. Since a cannot be paired with itself, a must be paired with either b or c. The best is pair a with c (2) and b with b? Not allowed. So b must be paired with c (10). Thus assignment a-c (2), b-c? but b can't be paired with c because c already used. So we need to match a-c, b-b? Not allowed. Actually we have two A's: a and b. Two B's: b and c. Matching must be bijection. So we must match a to b and b to c (since a cannot be matched to itself). That gives sum 10+10=20. Wait earlier I thought we could match a-c and b-b, but b-b is not allowed. So we must match a to b (10) and b to c (10) sum=20. So optimal sum is 20. Let's compute if any other matching yields lower: a-c (2) and b-b (0) not allowed. So only possible is a-b, b-c or a-c, b-b (invalid). So only one feasible matching sum=20. So any algorithm must produce 20. Sorting ascending tin gave 20 (a-b=10,b-c=10). Sorting descending B gave a-c=2, b-b (0) invalid; but we need to match both. Actually descending B list: [c,b] but then pairing A ascending [a,b] yields pairs (a,c) and (b,b). Since b-b invalid, we cannot use that. So descending B is not a solution for that case because we can't pair b to itself. So the algorithm must avoid self matches? But the problem guarantees A_i != B_j for all i,j, but specific pairs could be equal for some i=j? It says A_i != B_j (1 ≤ i,j ≤ K). Means for all i and j, A_i != B_j. So any vertex cannot appear in both A and B sets. That's important: The sets A and B are disjoint! Indeed guarantee: For any i, j, A_i != B_j. So there is no vertex that appears both in A and B. So we can't have a situation where a vertex appears in both sets. In star example, we had a,b in A and b,c in B which violates guarantee (b appears in both). So not allowed. Good. So the scenario where a leaf appears in both sets is impossible.

Thus the domain is that A and B are disjoint sets of vertices. Good. So for sample1, sets A = {1,3}, B = {4,2} with 1 appears in A (1 appears twice but only one vertex; duplicates allowed). B includes 4 and 2 only. So indeed A and B are disjoint. So we can assume that.

Now the problem reduces to matching K vertices from set A to K distinct vertices from set B, all disjoint. Since they are disjoint, the graph formed by edges between any A and B doesn't have self loops. That may simplify.

We need to find min sum of max edge path. This is reminiscent of assignment problem with cost defined by tree bottleneck distance. Perhaps there is a greedy algorithm: sort A and B by the time they appear in Euler tour of MST, and then match them in order (or reverse). Because the cost matrix is Monge, the optimal assignment is to match sorted A with sorted B (or reverse sorted B) but we need to decide direction. Actually Monge property yields that optimal assignment is to match in the same order (i.e., identity permutation after sorting). But earlier we saw that fails for sample1. But maybe the correct ordering is not Euler order but "time when you encounter the vertex in a depth-first traversal of the tree after rooting at some arbitrary node"? But we already used that. However sample1 suggests that matching A in increasing tin with B in decreasing tin yields optimal. That is reverse order. So maybe the property is that the matrix is anti-Monge (or Monge) and we need to match A sorted with B sorted in opposite order. Let's test with star case where A and B are disjoint. For star, vertices A: leaves a,b (disjoint from B). B: leaves c,d maybe. Let's compute tin order: root 0, children visited in some order, say a,b,c,d. Then tin: a=1,b=2,c=3,d=4. A sorted ascending: a,b. B sorted ascending: c,d. Pair a-c: max weight w_a vs w_c = max(w_a,w_c), b-d = max(w_b,w_d). Reverse B: d,c => a-d = max(w_a,w_d), b-c = max(w_b,w_c). Is either guaranteed to be optimal? Let's test with weights: a=1, b=100, c=2, d=3. So costs:
- a-c = max(1,2)=2
- b-d = max(100,3)=100
- sum ascending = 102

- a-d = max(1,3)=3
- b-c = max(100,2)=100
- sum descending = 103

Thus ascending is better. So for star, ascending B works.

Thus the direction (ascending vs descending) may depend on the specific tree shape and maybe can be decided by trying both possibilities? Since K up to 2e5, we could compute both sums (A sorted ascending with B sorted ascending, and with B sorted descending) and take minimum. Is it always optimal to either match in same order or reverse order? Possibly yes for Monge matrices, the optimal assignment is either identity or reverse identity (the assignment problem on a Monge matrix has optimal solution that is either the identity or reverse, but not in general for arbitrary Monge? Actually the assignment problem with Monge property can be solved in O(n) by the "Monge DP" which yields a certain structure but not necessarily monotone. However for a matrix that is also a "Kalmanson" matrix (tree metric), I recall that the optimal matching between two subsets of vertices is to match them in order of Euler tour (i.e., the "circular" order) - basically the assignment reduces to matching intervals. Let's explore.

Consider a tree. For any two vertices x,y, define f(x,y) = max edge weight on path. This is a "bottleneck" distance. It satisfies the four-point condition: for any a,b,c,d, the two largest among f(a,b), f(a,c), f(a,d), f(b,c), f(b,d), f(c,d) are opposite sides? Not sure. But the distance is an ultrametric? Actually it's not an ultrametric because triangle inequality: f(x,y) <= max(f(x,z), f(z,y)). That's exactly the ultrametric inequality. Yes! The bottleneck distance is an ultrametric. In an ultrametric, the distance is the maximum edge weight on the minimal spanning tree path. It is indeed a metric with stronger property: for any three points, the two largest distances are equal. This is ultrametric. For ultrametrics, the optimal assignment (minimum sum) between two sets of equal size is to match in order of a hierarchical clustering? There is known result: For an ultrametric, the sum of distances in optimal matching equals sum of distances of matching according to the "leaf order" given by the dendrogram. Maybe the optimal matching is to match the leaves in the order they appear in a sorted list by the time they join clusters.

But we need a constructive algorithm for up to 2e5 vertices. The MST yields a hierarchical clustering (by removing edges in decreasing order). If we sort edges of MST by weight descending, we gradually merge components. At each step, we can maintain for each component the number of As and Bs inside. The matching cost for a pair (A in component X, B in component Y) that become connected at weight w is w (since the path's max edge weight is w). The total sum of f(A_i, B_{π(i)}) can be expressed as sum over all merges of weight w * number_of_pairs_connected_by_this_merge where each pair counted exactly once in the final matching. Actually we can think: For each pair (a,b) matched, the bottleneck edge weight on their path is the weight of the deepest common ancestor edge that separates them in the MST. The total sum across matched pairs equals sum_{edges e} w(e) * cnt(e) where cnt(e) is the number of matched pairs whose path uses edge e as the maximum (i.e., whose LCA is just above e). In MST, each pair's max edge is the maximum weight edge on the unique path; that is the edge with maximum weight among edges on the path. So we can think of the tree edges sorted decreasing; the pair's max is the highest weight edge connecting their components after removing edges heavier than that. So if we do a DSU merging from smallest to largest weight (i.e., building MST), when we add an edge of weight w, we connect two components. The pairs (a,b) that become connected for the first time at this edge will have f = w. But we need to count only pairs that are matched, not all pairs.

Thus the matching cost is sum over edges e of w(e) * m(e) where m(e) is number of matched pairs whose LCA is the endpoint of e (i.e., whose path includes e as the maximum). Equivalent to: In the tree, for each edge e, consider the two components after cutting e. The number of matched pairs crossing this cut (i.e., one endpoint in each component) is some number. However, for a pair to have max edge weight w(e) exactly, they must be in different components when we cut e, but not separated by any heavier edge. The set of pairs whose max is exactly w(e) are those that become connected for the first time when we add e. That's like the DSU process: start with each vertex as its own component, process edges in increasing weight order, and when we union two components using edge of weight w, any pair (a,b) where a is in one component and b in the other will have f(a,b) = w. However, those pairs that were already connected earlier via a lighter edge are not affected. So each edge's weight contributes to the sum for all pairs (a,b) that are separated before union and become connected after union. Among all possible pairs across the cut, only some are actually matched in the assignment. So the total sum = sum_{edges} w(e) * X(e) where X(e) is number of matched pairs crossing the cut defined by e.

Now the assignment problem reduces to: we need to choose a matching between As and Bs, and we want to minimize sum over edges w(e) * X(e). Since each matched pair contributes to X(e) for each edge on the path between its vertices (specifically for the edge of maximum weight, which is the lightest edge on the path? Actually max weight is the heaviest edge on the path. In the DSU process of adding edges in increasing order, the first time the two vertices become connected is when we add the edge with the smallest weight that connects them? Wait, the path may contain edges of varying weights; the maximum weight is the largest weight along the path. In DSU union by weight (Kruskal), edges are added from smallest to largest. When we add an edge of weight w, we connect two components. If two vertices a and b are in different components before adding e, then any path between them will include e (since e is the only edge connecting the two components). But the path might also contain heavier edges (added later) that lie within each component? Actually after adding e, a and b become connected via a path that includes e and other edges within each component that have weight <= w (since they were added earlier). However, the maximum edge weight on that path might be larger than w if there is a heavier edge within one of the components (but those edges would have weight > w and would not have been added yet). Since DSU processes edges in increasing order, any edge within a component has weight <= w. So the max weight on the path a-b is exactly w (the weight of the edge that just connected them). Thus the DSU view gives that for each edge e, when we union components, the pairs (a,b) that become connected at that step have max = w(e). And later heavier edges won't affect them because they are already connected; but the path may later include heavier edges, but those edges are within the same component after previous unions? Actually if later we add a heavier edge that connects two vertices that are already in the same component, that won't create a new path. So the max weight for a pair is determined by the moment they become connected in Kruskal: the weight of the edge that connected their components. Good.

Thus the problem becomes: we have K As and K Bs (disjoint). Process MST edges in increasing weight; initially each vertex is its own component. Maintain for each component: count of A's in it, count of B's in it. When we union two components via edge weight w, the pairs that become newly connected are those where one vertex is an A in one component and a B in the other component (or vice versa). However, there may be multiple As in one component and multiple Bs in the other, and any pair across components will have max weight w. But only some of those cross pairs will be actually matched in the final assignment; we need to decide a matching that minimizes sum of w times matched cross pairs. Since the total contribution of a union step is w * (number of matched A-B pairs that cross between the two components at that step). If we have X As in left component, Y Bs in left component, similarly for right component: As right, Bs right. The total possible cross A-B pairs across the cut is X_left * Y_right + X_right * Y_left. We need to match some number of them, but not necessarily all, because we have exactly K As and K Bs overall and we need to match all As to distinct Bs. As we union components, eventually all As will be matched to some Bs (global matching). The matching must be a bijection between As and Bs. The number of matched pairs crossing a cut is equal to the number of As in one side that are matched to Bs on the other side. The total across all cuts must be exactly K (since each pair is counted exactly for the cut where its endpoints become connected). But we need to allocate the matching across edges to minimize total cost: we prefer to match As and Bs that become connected later (i.e., via heavier edges) as little as possible, because heavier edges add higher cost. The greedy solution is to match as many As with Bs as possible using lighter edges (i.e., earlier unions). So we can decide a matching that, for each union step, matches as many cross pairs as possible, i.e., match min(X_left, Y_right) + min(X_right, Y_left) ??? Actually we can match some pairs across this edge; the maximum number we can match at this step is limited by the remaining unmatched As and Bs. To minimize total cost, we would like to match as many As with Bs that become connected at the smallest possible weight. That is, we want to greedily match pairs at each union step as much as possible. This is reminiscent of a flow or matching problem: at each union, we can match any As from left with any Bs from right (or As right with Bs left). Since we have global counts, we can match up to the minimum of total As on one side and total Bs on the other side across the cut. So the optimal total cost would be sum over edges w(e) * match(e), where match(e) is the number of pairs matched across the edge e, defined as the amount of "excess" As on one side matched to Bs on the other side at that union. We need to compute the minimal possible total sum, which is basically: for each edge, the number of matched pairs that have to be matched at that edge is determined by the net imbalance of As and Bs in each component as we merge.

More concretely, consider the tree as rooted arbitrarily. For each vertex, define a "balance" = (#As in subtree) - (#Bs in subtree). Then for each edge connecting parent to child, the number of pairs matched across that edge is the absolute value of the sum of balances of the child's subtree? Something like that. Let's think.

We have a tree, each leaf may be an A or a B (or neither). We need to match each A to a B, forming K edges (matching). The total cost is sum over edges of weight * (number of matched pairs that cross that edge). The total number of pairs that cross an edge equals the number of As in one side matched to Bs in the other side. Suppose we root the tree arbitrarily, and orient edges from parent to child. For each edge e (parent u, child v), let A_sub = number of As in subtree of v, B_sub = number of Bs in subtree of v. The rest of the tree (outside subtree) has A_out = total A - A_sub, B_out = total B - B_sub. For a given matching, the number of matched pairs crossing edge e is at most min(A_sub, B_out) + min(A_out, B_sub) (since a pair crossing e must have one endpoint in subtree v and the other outside). But also the total number of matched pairs crossing e equals the number of As in subtree that are matched to Bs outside, plus As outside matched to Bs inside. But the matching pairs are disjoint: each A and B appear exactly once. So for the edge, the number of As in subtree that are matched to Bs outside must be exactly the number of As in subtree minus the number of As in subtree matched to Bs inside the subtree. Similarly for Bs.

But perhaps the total cost can be expressed as sum over edges of w(e) * |balance_subtree|? Let's test on simple examples.

Consider a simple path: A at vertex 1, B at vertex 2. There is only one edge weight w. The sum of balances: subtree of vertex 1 (leaf) contains A but not B => balance = 1 - 0 = 1. The total cost = w * 1. The formula sum w*|balance| would be w*1 = w. That matches f(A,B) = w (since path edge weight is w). Good.

Consider a path with A at 1, B at 3, middle vertex 2 not in sets. Edge weights w1 between 1-2, w2 between 2-3. The path's max edge weight is max(w1,w2). The balances: Subtree of node 1 contains A (balance=1). Subtree of node 3 contains B (balance=-1). For edge (1,2), the subtree of child 1 has A_sub=1,B_sub=0 => balance=1. For edge (2,3), subtree of child 3 has A_sub=0,B_sub=1 => balance=-1 => |balance|=1. So sum w*|balance| = w1*1 + w2*1 = w1 + w2, not max(w1,w2). So that formula not correct.

Maybe the cost is sum over edges w(e) * (|balance| of one side after matching). Not that.

Alternatively, think in terms of DSU merging in increasing weight order. The total cost is sum_{edges e} w(e) * m(e) where m(e) is number of matched A-B pairs that become connected at edge e. Since the DSU merges two components C1 and C2, suppose component C1 has a1 As and b1 Bs; component C2 has a2 As and b2 Bs. After merging, the As and Bs that are now in same component may be matched later, but pairs that are matched now (i.e., at this edge) can be any cross pairs between the two components: they can be from A in C1 to B in C2, or A in C2 to B in C1. The number of such pairs matched at this step is at most min(a1, b2) + min(a2, b1). To minimize total cost, we want to match as many as possible at this step (since this weight is the smallest weight that will be assigned to those pairs). So the optimal greedy is: at each union, match as many cross pairs as possible. This will produce a matching that is optimal (similar to the classic problem of minimizing sum of edge weights used in matching As to Bs on a tree). Indeed, we can think of it as a flow: each A and B need to be matched; we push flow across the tree; each time we cross an edge, we incur cost equal to weight times flow across it. Minimizing total cost is a min-cost flow problem on a tree where each A is a unit supply, each B is unit demand, and cost per unit on edge e is weight w(e). This is a classic min-cost flow on tree with convex cost (linear). The optimal solution is to send flow along paths, which is equivalent to greedily matching across edges as we ascend in Kruskal.

Specifically, treat each vertex as node, each A vertex has supply +1, each B vertex has demand -1, others 0. Edge costs per unit = w(e). This is a min-cost flow on a tree. The optimal flow can be found by a simple greedy algorithm: process edges in increasing order of w, using DSU to aggregate supplies and demands. When we connect two components, we can match supply in left with demand in right as much as possible, incurring cost w per unit. This yields the min total cost. This is analogous to the classic "minimum cost to pair points on a line with distances" where you sort and match adjacent. For tree, you do union-find by increasing weight, and match supplies.

Thus the minimal sum of f(A_i, B_{π(i)}) is exactly the cost of min-cost flow: sum over edges w(e) * flow(e), where flow(e) is the amount of supply crossing that edge. The DSU greedy algorithm yields that total cost.

So we need to implement: Build MST, get its edges with weights. Then run DSU merging in order of increasing weight, maintaining for each component: countA (number of A vertices in component), countB (number of B vertices). Initially each vertex is its own component, with countA=1 if vertex in A list (i.e., appears in A), countB=1 if vertex in B list. But note that A and B may have duplicates (multiple entries). Since we need to match each occurrence (K pairs). So countA for a vertex should be the multiplicity of that vertex in A (0,1,2,...). Similarly for B. Since sets are disjoint, a vertex can be in A or B but not both; but may appear multiple times in its own set.

At each union of components c1 and c2 with edge weight w, we can match pairs between them: let match1 = min(c1.countA, c2.countB); let match2 = min(c2.countA, c1.countB). These are the numbers of A-B pairs that we can match across the union (i.e., As from one side to Bs from the other side). The total matched at this step is match1+match2. Each such pair will incur cost w. So add w * (match1+match2) to total answer. Then update component counts: newCountA = c1.countA + c2.countA - (match1+match2) ??? Wait we matched some As with Bs, those As and Bs are now used (matched) and should be removed from counts for future matches. So after matching, we need to subtract matched As and matched Bs from the component. More precisely, for each match we use one A and one B. So the remaining A count in component after matching is: c1.countA + c2.countA - (match1+match2)??? Not exactly because match1 uses As from component1 and Bs from component2, match2 uses As from component2 and Bs from component1. So the total As used = match1 + match2. Similarly total Bs used = match1 + match2. So after matching, the remaining As in combined component is c1.countA + c2.countA - (match1+match2). Similarly remaining Bs = c1.countB + c2.countB - (match1+match2). But also there may be leftover As and Bs that are unmatched within combined component, to be matched later via heavier edges.

We need to maintain counts of unmatched As and Bs in each component. Let's define for each component: a = number of unmatched As in the component, b = number of unmatched Bs. Initially a = multiplicity in A, b = multiplicity in B. For leaf not in either, a=b=0.

When merging components X and Y with edge weight w:
- We can match some As in X with some Bs in Y: t1 = min(a_X, b_Y)
- And As in Y with Bs in X: t2 = min(a_Y, b_X)
- Total matches m = t1 + t2.
- Add w * m to answer.
- Update new a = a_X + a_Y - m (since each match consumes one A and one B)
- New b = b_X + b_Y - m

That's correct: each match consumes one A and one B. The remaining unmatched As and Bs are simply the sum minus those used.

At the end of all merges, we should have a=b=0 (since total A = total B = K). The answer will be sum of w * matched at each union.

Thus the answer is computed by union-find on MST edges sorted ascending, maintaining a and b counts, and accumulating cost as described.

Let's test this algorithm on sample1.

MST edges sorted ascending: weight 1: edge (3,4); weight 2: edge (1,3); weight 5: edge (2,4).

Initialize counts:
Vertex1: a=2 (since A list has 1 twice), b=0
Vertex2: a=0, b=1 (B has 2 once)
Vertex3: a=1, b=0
Vertex4: a=0, b=2 (B has 4 twice)

Now DSU merges:

Edge weight 1: merge component of 3 (a=1,b=0) and 4 (a=0,b=2).
t1 = min(a3=1, b4=2) = 1
t2 = min(a4=0, b3=0) = 0
m = 1
cost += 1*1 =1
New a = 1+0-1=0
New b = 0+2-1=1

Now component (3-4) has a=0,b=1 (one unmatched B at vertex4). Actually B count left is 1.

Edge weight 2: merge component of 1 (a=2,b=0) with component (3-4) (a=0,b=1).
t1 = min(a1=2, b34=1) =1
t2 = min(a34=0, b1=0) =0
m=1
cost += 2*1 =2 => total=3
New a = 2+0-1=1
New b = 0+1-1=0

Now component (1-3-4) has a=1,b=0.

Edge weight 5: merge component (1-3-4) (a=1,b=0) with component 2 (a=0,b=1).
t1 = min(a1234=1, b2=1)=1
t2 = min(a2=0, b1234=0)=0
m=1
cost+=5*1=5 => total=8.

Matches:
- At weight 1, matched A from vertex3 to B at vertex4 (makes sense f(3,4)=1).
- At weight 2, matched one of the A at vertex1 to B at vertex4 (the other B at vertex4 is already matched? Actually B count left was 1; matched to A1). So f(1,4)=2.
- At weight 5, matched remaining A (the second A at vertex1) to B at vertex2 => f(1,2)=5.
Total cost =1+2+5=8. Works!

Thus the algorithm yields the optimal answer.

Now test sample2.

MST edges sorted: weight1: (1-3,1); weight2: (2-3,2).

Counts:
v1: a=2 (A has 1 twice), b=0.
v2: a=0, b=1.
v3: a=0, b=1.

Edge weight 1: merge 1 (a=2,b=0) and 3 (a=0,b=1):
t1 = min(2,1)=1
t2 = min(0,0)=0
m=1
cost+=1*1=1
new a=2+0-1=1
new b=0+1-1=0
Component (1-3) a=1,b=0.

Edge weight 2: merge component (1-3) (a=1,b=0) with 2 (a=0,b=1):
t1 = min(1,1)=1
m=1
cost+=2*1=2 => total=3.
new a=0, new b=0. Done.

Matches: A at 1 to B at 3 (f=1), A at 1 to B at 2 (f=2). Sum=3. Works.

Thus DSU matching on MST works for both samples.

Now we need to prove correctness: The DSU matching algorithm yields min total sum because it's equivalent to min-cost flow on a tree with linear costs, which can be solved greedily by processing edges in increasing order, matching as much flow as possible across each edge.

Hence the solution:

Algorithm:
1. Read N, M, K.
2. Read edges. Build MST using Kruskal: sort edges by weight, union them if they connect different components. Store MST edges.
3. Count for each vertex:
   cntA[v] = number of times v appears in A list.
   cntB[v] = number of times v appears in B list.
   (Since A_i and B_j are disjoint, no vertex has both >0, but we can still allow.)
4. Initialize DSU for MST (size N). For each root, store a = cntA[v], b = cntB[v].
5. Sort MST edges by weight ascending (though we can process in order we already have after building MST; we can store them in a list).
6. For each edge (u,v,w) in ascending order:
   - Find root of u and v; if same, skip (shouldn't happen as MST has no cycles).
   - Let ra, rb be the DSU components.
   - Compute t1 = min(a[ra], b[rb]) (match A from ra with B from rb)
   - t2 = min(a[rb], b[ra]) (match A from rb with B from ra)
   - matched = t1 + t2
   - ans += matched * w
   - New a = a[ra] + a[rb] - matched
   - New b = b[ra] + b[rb] - matched
   - Union ra, rb: store new a,b in the root.
7. After processing all edges, ans is the minimal sum.

Time complexity: O(M log M) for Kruskal, O(N log N) for DSU union operations on N-1 edges. N up to 2e5, M up to 2e5, fine.

Now we need to ensure that this algorithm indeed matches each A to exactly one B, i.e., at the end a and b should be zero. Since total sum of a across all vertices = K, same for b. At each union we match as many as possible, leaving leftover As and Bs. The DSU ensures that eventually all matched.

Edge Cases: Graph may have parallel edges? Input is simple, no parallel edges. MST will have N-1 edges, unique if all weights distinct? Not necessarily unique but any MST works because f(x,y) defined via min max path is independent of which MST? Actually f(x,y) = min possible max edge weight path, which equals the maximum edge weight on the path between x and y in any MST (specifically any minimum spanning tree). However if there are multiple MSTs, the f values are the same because the max edge weight on the min possible path is unique (the value of the min bottleneck path). In any MST, the max edge weight on the unique path equals f(x,y). Indeed, the property: The minimax path value between any two vertices equals the max edge weight on the path between them in any MST (i.e., the minimax path is the same for all MSTs). This is known: The MST is a minimum bottleneck spanning tree; for any pair, the minimax path weight equals the max edge weight on the path in any MST. So we can pick any MST.

Thus algorithm correct.

Now we must implement with careful handling of large K (up to 2e5). DSU arrays: parent, size, a, b. Since we only need to union components, we can maintain a and b per root.

Potential issues: Multi-set A may contain duplicate vertices (like vertex 1 appears twice in sample). Our cntA counts that. DSU merging uses counts, fine.

Now verify correctness on more test cases, including random small graphs, by brute force matching (K <= 8). Let's test with code later.

Potential pitfalls: The DSU algorithm matches as many as possible at each edge, but is it always optimal? Yes, because min-cost flow on a tree with linear edge costs is solved by this greedy: at each edge, you can push as much flow as possible (i.e., match as many units) because any flow across that edge will incur the same cost w, and you want to satisfy demands/supplies with minimal total cost. Since edges are processed in increasing order, earlier edges cheaper, so we want to use them as much as possible. This is analogous to the classic "minimum cost to connect supply and demand on a tree" where the optimal solution is to push flow along cheapest edges first.

Proof: Consider min-cost flow. The cost is sum over edges w(e) * flow(e). Since edges have nonnegative costs, there is an optimal solution where flow is routed along paths that are monotone with respect to edge weight order; basically, you can always rearrange flows to not use more expensive edges than necessary. Equivalent to the "greedy matching" algorithm.

Thus algorithm stands.

Now we need to produce a final answer: print ans.

Now we need to think about memory: DSU arrays size N+1 (1-indexed). Edge list for MST: up to N-1 edges.

Implementation steps:
- Input.
- edges = list of (w,u,v)
- sort edges by w.
- Initialize DSU for building MST: parent = list(range(N+1)). Keep mst_edges = [].
- For each (w,u,v) in sorted edges:
   if find(u) != find(v):
        union(u,v)
        mst_edges.append((u,v,w))
   if len(mst_edges) == N-1: break
- Now DSU reset (or reuse separate arrays) for processing MST.
   - We can reuse same DSU arrays but reinitialize parent to identity for new DSU used in matching step.
- Prepare cntA and cntB arrays of size N+1, initially zero.
- For each A_i: cntA[A_i] += 1
- For each B_i: cntB[B_i] += 1
- Initialize DSU2: parent2, a = cntA, b = cntB.
- Process mst_edges sorted by weight ascending (they may already be sorted because we inserted in sorted order, but ensure).
- For each (u,v,w):
    ru = find2(u); rv = find2(v)
    if ru == rv: continue (should not happen)
    t1 = min(a[ru], b[rv])
    t2 = min(a[rv], b[ru])
    matched = t1 + t2
    ans += matched * w
    new_a = a[ru] + a[rv] - matched
    new_b = b[ru] + b[rv] - matched
    # union ru, rv (by size)
    if size[ru] < size[rv]: swap
    parent2[rv] = ru
    a[ru] = new_a
    b[ru] = new_b
    size[ru] += size[rv]
- Print ans.

Check that ans fits in 64-bit: each w up to 1e9, matched up to K up to 2e5, ans up to 2e5*1e9 = 2e14, fits in 64-bit (less than 9e18). So use Python int fine.

Now test with sample1 and sample2.

Now we need to test more random cases. We'll implement a brute solver for small N (N <= 8, K <= 4) enumerating all permutations of B to compute min sum, then compare with DSU algorithm.

Potential issues: The DSU algorithm implicitly assumes that we can match As and Bs arbitrarily; but there is a hidden assumption that there exists a perfect matching (i.e., total counts equal). Since A_i and B_i have same length K, and they are disjoint, there is always a perfect matching (any bijection). The DSU algorithm will find a matching but we need to ensure that we don't get stuck with unmatched As or Bs that cannot be matched due to tree structure? However due to the connectivity of the MST, there is always a path between any A and any B, so we can match them arbitrarily; the DSU algorithm matches as many as possible at each step, but might leave some As and Bs unmatched until later merges; but eventually all will be matched as we process all edges, because eventually all vertices are merged into one component, at which point a and b must be zero. Since total a and b both equal K, and each union reduces total a+b by 2*matched, eventually zero.

Thus DSU algorithm is correct.

Now, complexity wise: O(N log N) for DSU union-find with path compression, plus O(N) for processing. Good.

Edge Cases: K may be 0? Not per constraints (K >=1). A_i and B_i sets may be empty? No. But handle generic.

Now we need to produce final solution with code.

Let's produce final answer in required format.

But before final, we need to ensure we didn't miss any nuance: the DSU algorithm matches greedily across each edge, but does it guarantee that each A is matched to exactly one B (i.e., no A matched twice)? Yes, because each match consumes one A and one B, and we never reuse an A or B.

Now we should prove that greedy matching yields optimal min total cost. Formal proof: Since the cost for a pair is the weight of the maximum edge on the path, which corresponds to the edge weight when the pair's components first become connected in Kruskal, the total cost is sum over edges weight * number_of_pairs_using_this_edge_as_max. The number of pairs using a particular edge is determined by the distribution of unmatched As and Bs in the two components at the moment of union. The optimal solution chooses a matching that minimizes sum_{edges} w(e) * x(e), where x(e) is the number of pairs crossing edge e, subject to flow constraints. This is exactly a min-cost flow on a tree, which can be solved greedily by processing edges in increasing order and sending as much flow as possible across each edge, because sending flow earlier (cheaper) cannot increase the need for flow later (heavier). A simple exchange argument shows that any optimal solution can be transformed to match as many pairs as possible across each edge in order, without increasing cost.

Alternatively, we can think of the problem as: we have K As (supply) and K Bs (demand). The cost of sending one unit of flow along a path is the maximum edge weight along that path. In a tree, each path's cost equals the maximum weight among edges on it. This is equivalent to a min-cost flow where each edge has cost w(e) per unit flow (i.e., linear). Since costs are nonnegative and the graph is a tree, the min-cost flow can be found by a "southward" algorithm: push flow from supplies to demands using cheapest edges first. This is analogous to the classic problem of connecting terminals on a tree with minimum total edge weight times number of terminals using that edge.

Thus DSU algorithm is correct.

Now confirm on random small graphs via brute force: Let's do mental test.

Example: N=4, edges: (1-2,w=1), (2-3,w=10), (3-4,w=1). MST: edges (1-2,1) and (3-4,1) and (2-3,10). Suppose A = {1,4} (both in A), B = {2,3}. So K=2.

Our DSU algorithm:
- Build MST edges: (1-2,1), (3-4,1), (2-3,10)
- cntA: 1->1,4->1, others 0. cntB: 2->1,3->1.
- Process edges ascending:
  weight 1: edge (1-2):
    comp1: a=1,b=0; comp2: a=0,b=1.
    t1 = min(1,1)=1, t2 = min(0,0)=0 => m=1 => ans +=1*1=1.
    new a =1+0-1=0; new b =0+1-1=0. So component (1-2) has a=b=0.
  weight 1: edge (3-4):
    comp3: a=0,b=0; comp4: a=1,b=0.
    t1 = min(0,0)=0, t2 = min(1,0)=0 => m=0. ans unchanged.
    new a =0+1-0=1; new b =0+0-0=0. Component (3-4) a=1,b=0.
  weight 10: edge (2-3):
    root of 2 is component (1-2) with a=0,b=0.
    root of 3 is component (3-4) with a=1,b=0.
    t1 = min(0,0)=0, t2 = min(1,0)=0 => m=0.
    ans stays 1.
    new a = 0+1-0=1, new b=0+0-0=0. So after merging all, a=1,b=0 (unmatched A). Something wrong: total A=K=2, B=2, we matched only 1 pair? Let's track correctly: At start, As: vertices 1 and 4 each have a=1. Bs: vertices 2 and 3 each have b=1. After first union (1-2) we matched A1 to B2 using weight 1, leaving A at vertex4 unmatched and B at vertex3 unmatched. After second union (3-4) we have component (3-4) a=1 (A at 4), b=0. At final union weight 10 merges (1-2) component (a=0,b=0) with (3-4) component (a=1,b=0). Wait B3 is still unmatched. But we have B at vertex3 which is now part of (3-4) component, but b count is 0? That seems wrong. Actually we missed B at vertex3: at the start cntB[3]=1. In component (3-4) we initially had a=0,b=1? Wait B at vertex3 should be counted. Let's re-evaluate: cntB[3]=1, cntB[2]=1. So after initial processing of edges, we should have:

Initialize:
v1: a=1,b=0
v2: a=0,b=1
v3: a=0,b=1
v4: a=1,b=0

Edge (1-2) w=1: merge v1 (a=1,b=0) and v2 (a=0,b=1). t1 = min(1,1)=1; t2=0; m=1; ans=1; new a=1+0-1=0; new b=0+1-1=0. So component (1-2) a=0,b=0.

Edge (3-4) w=1: merge v3 (a=0,b=1) and v4 (a=1,b=0). t1 = min(0,0)=0; t2 = min(1,1)=1? Wait a3=0, b3=1; a4=1, b4=0. So t1 = min(a3=0, b4=0) = 0. t2 = min(a4=1, b3=1) = 1. So m = 1, ans += 1*1 = 2. new a = 0+1-1 = 0; new b = 1+0-1 = 0. So component (3-4) a=0,b=0. Great! Then final edge weight 10 merging components both a=0,b=0 => m=0, ans stays 2. So total cost = 2.

Now compute actual f values: The MST path between 1 and 2: max weight =1. Between 4 and 3: path 4-3 weight =1. So sum of these two pairs =2. So DSU algorithm yields 2, which is optimal. So earlier we misapplied t1/t2.

Thus algorithm is consistent.

Now consider more complex scenario: A and B sets are larger and spread.

Edge Cases: The DSU algorithm matches as many as possible across each edge in order. It's essentially the min-cost flow solution.

Let's also test a case where there are multiple As and Bs in same component before union: Suppose component X has a_X=3, b_X=0 (only As). Component Y has a_Y=0, b_Y=5 (only Bs). Edge weight w. Then t1 = min(3,5) = 3, t2 = min(0,0) = 0, m=3. So we match all As with some Bs at weight w. That's correct: the best we can do is match all As with Bs across this edge, because any As matched to Bs inside component X or Y would have to be matched later across other edges with higher weight (since all other edges are heavier). So matching all possible now is optimal.

Now test case where both sides have As and Bs: X: a_X=2,b_X=2; Y: a_Y=2,b_Y=2. Then t1 = min(2,2) = 2, t2 = min(2,2) = 2, m=4. So all pairs matched now, leaving a=0,b=0. That's optimal: we can match all cross pairs across this edge, avoiding any heavier edges.

Thus algorithm seems correct.

Now we need to implement DSU with union by size/rank and path compression.

Potential issues: Because we need to keep a and b per root, we need arrays a and b of length N+1. When we union, we should combine them appropriately.

Implementation details:

```
parent = list(range(N+1))
size = [1]*(N+1)
cntA = [0]*(N+1)
cntB = [0]*(N+1)
for each a_i: cntA[a_i] += 1
for each b_i: cntB[b_i] += 1
a = cntA[:] # copy
b = cntB[:]
def find(x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x
ans = 0
for u,v,w in mst_edges:
    ru = find(u)
    rv = find(v)
    if ru == rv: continue