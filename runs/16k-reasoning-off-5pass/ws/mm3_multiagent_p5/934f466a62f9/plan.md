The key observation is that for a pair `(a,b)`, the price is `max(X_a+X_b, Y_a+Y_b, Z_a+Z_b)`. If we think in terms of vectors, each cake i contributes a 3D vector (X_i, Y_i, Z_i). The pair price equals the maximum sum along any coordinate.

We can decouple the max by considering that for any pairing, the total price equals the sum of `max` per pair. There is a known trick: for problems where a value is `max` of multiple additive components, we can use a binary search on the answer and a feasibility check using bipartite matching or flow.

For each pair, price ≤ C iff for all three coordinates, the sum of the two cakes along that coordinate ≤ C? No — actually price = max of three sums, so price ≤ C iff all three sums ≤ C. That's too restrictive.

Better: use the inequality max(A,B,C) ≥ (A+B+C)/3. This gives a lower bound. For upper bound, we can binary search on a threshold C and ask: can we pair K pairs such that for each pair, max(sumX, sumY, sumZ) ≤ C? That means for each pair, we need sumX ≤ C, sumY ≤ C, and sumZ ≤ C. This is a 3-constraint bipartite matching, which is hard.

Alternative: Since X, Y, Z values are up to 1e9, and N up to 1e5, we need a clever approach.

Actually, a well-known approach for this type of problem: For each cake, consider (X_i, Y_i, Z_i). Sort cakes by one coordinate (say X). The pair price's max of three sums... 

Let me think differently. Since the answer is sum of maxes, and we want to maximize, we can think of it as: for each pair, we pick the "dominant" coordinate. This is similar to pairing problems where we optimize sum of max.

Key insight: The price of a pair (a,b) equals max over dimensions. So for any pair, the price equals the maximum of three possible "paying" values. In an optimal solution, we can categorize pairs by which dimension achieved the max (ties can be broken arbitrarily).

So total = (sum of X for pairs where X-dim dominates) + (sum of Y for pairs where Y-dim dominates) + (sum of Z for pairs where Z-dim dominates).

But this decomposition is complex. Let me think of a DP or greedy approach.

Actually, I recall a technique: sort cakes by one attribute, and use the observation that for a pair, the max of the three sums equals... hmm.

Let me think about the structure. WLOG say we want to pair cake a with cake b. The price is max(X_a+X_b, Y_a+Y_b, Z_a+Z_b).

Consider sorting cakes by (say) Y_i + Z_i - X_i or some linear combination. There's a classic result: if we define for each cake a "label" and use a flow network, we can solve it in polynomial time.

However, with N up to 1e5 and 3 dimensions, we need something efficient.

Let me reconsider. The problem is from ABC 400 (a recent contest). The constraints N ≤ 1e5 and sum of N ≤ 1e5 suggest an O(N log N) or O(N sqrt N) solution per test case.

I think the intended approach is: 
- Binary search on the answer C.
- Check if we can form K pairs with price ≤ C.
- The check: we need to find a perfect matching of size K in a graph where edge (i,j) exists iff max(X_i+X_j, Y_i+Y_j, Z_i+Z_j) ≤ C.

This graph is the intersection of three constraints: X_i+X_j ≤ C, Y_i+Y_j ≤ C, Z_i+Z_j ≤ C.

This is a "3D" constraint. In general, bipartite matching with such constraints is hard, but here the constraints are on sums of pairs.

Important property: X_i+X_j ≤ C means both X_i ≤ C and X_j ≤ C (since values are non-negative), and more restrictively, they are "complementary" in a sense.

Let me think about this differently. For two non-negative numbers a, b: a+b ≤ C iff both a ≤ C and b ≤ C, and additionally a+b ≤ C.

Consider building a graph where we connect i and j if all three sums are ≤ C. We want a maximum matching of size K.

Since all values are non-negative, X_i+X_j ≤ C implies X_i ≤ C and X_j ≤ C. Similarly for Y and Z. So any cake in a valid pair must have X_i ≤ C, Y_i ≤ C, Z_i ≤ C (since pairing with a cake with value 0 in that dimension gives sum = X_i, so X_i ≤ C, etc.). Wait, actually we need X_i + X_j ≤ C where j has some X_j ≥ 0, so X_i ≤ C. Yes.

So we can pre-filter: only cakes with X_i ≤ C, Y_i ≤ C, Z_i ≤ C can be used. Let's call these "eligible" cakes.

Now, for eligible cakes, we need to find maximum matching in graph where edge exists iff X_i+X_j ≤ C AND Y_i+Y_j ≤ C AND Z_i+Z_j ≤ C.

This is still a general graph matching problem which is hard in general, but with specific structure (sum constraints) it might be tractable.

Observation: The constraints X_i+X_j ≤ C define a graph that is a "threshold graph" on sorted X values. Specifically, sort cakes by X. Then X_i+X_j ≤ C iff the two cakes' X values sum to ≤ C. If we sort by X ascending, the constraint means for any cake at position p, it can pair with cakes in positions q where X_p + X_q ≤ C. This defines a contiguous range (from the left) of compatible partners.

Similarly for Y and Z. The overall compatibility is the intersection of three such ranges. This makes the graph a "3-sorted" intersection graph, which has special structure.

In fact, this is similar to the problem of finding maximum matching in a 3-uniform hypergraph or in a graph defined by intersection of three interval-like conditions.

For the 1D case (just one constraint), we can greedily match: sort by value, use two pointers. For 2D, it's more complex. For 3D, even more so.

Wait, let me check the constraints again. We need X_i+X_j ≤ C AND Y_i+Y_j ≤ C AND Z_i+Z_j ≤ C.

If we think of it as: cake i "allows" partners j such that j is in the intersection of three ranges defined by the constraints. 

For the 1D case (only X constraint), we can solve in O(N log N) by sorting and two pointers.

For the 3D case, we need a more sophisticated approach. 

Let me think about using Hall's theorem or max flow. With N up to 1e5, we need a near-linear algorithm.

I recall that for problems with sum constraints on pairs across multiple dimensions, we can use the following approach: sort by one dimension, and for each prefix, maintain a data structure of cakes that satisfy all constraints, and greedily match.

Actually, there's a beautiful approach: For the 1D problem of finding maximum matching where edge (i,j) exists iff a_i + a_j ≤ C, we sort by a_i and use two pointers. 

For the 3D problem, we can try: sort by one dimension, and for each cake in order, try to match it with the "best" available partner. But this might not give optimal matching.

Alternatively, since all constraints are "sum ≤ C" and we have 3 of them, and the graph is defined by intersection of three "sum" graphs, we can characterize the structure.

Let me think about the graph G where edge (i,j) exists iff all three sums ≤ C. This is the intersection of three graphs G_X, G_Y, G_Z where G_X has edge iff X_i+X_j ≤ C, etc.

Each G_X is a "co-interval graph" or "threshold graph" on the sorted order. Specifically, sort indices by X. Then in this sorted order, the neighbors of any vertex form a contiguous interval (prefix or suffix depending on sort direction). Actually, if we sort ascending by X, then for vertex i, the condition X_i + X_j ≤ C means X_j ≤ C - X_i. So the valid j's are those with X_j ≤ C - X_i, which is a prefix (if we look at the sorted array). Wait no: if we have sorted ascending, and we want X_j ≤ C - X_i, then for a given i, the valid j's are in a prefix up to some index (those with small X). But also, j could be after i if X_j is small? No, in ascending order, if j > i then X_j ≥ X_i. So X_i + X_j ≤ C requires both to be small, and the set of j's is a prefix of the sorted list (including some elements before i and some after, but the condition defines a prefix when we consider the whole array).

Actually, more precisely: let the sorted order be by X ascending. The condition X_i + X_j ≤ C defines for each i a set of j's. The adjacency is symmetric. This graph is a "interval graph" in a generalized sense: it's the comparability graph of a poset? No, it's a "cograph" or "threshold graph"?

I think the key insight is: the graph G_X (and similarly G_Y, G_Z) is a "chain graph" or has a specific structure. Specifically, if we sort by X, then for any i < j < k, if i is connected to k, then i is connected to j. This is the definition of a "threshold graph" or more specifically, the graph is "split" in a particular way.

Actually, let me think again. Sort by X ascending: x_1 ≤ x_2 ≤ ... ≤ x_n. For i < j, edge (i,j) exists iff x_i + x_j ≤ C. Note that x_i + x_j ≤ C implies x_i ≤ C and x_j ≤ C. Also, for fixed i, as j increases, x_j increases, so the condition x_i + x_j ≤ C becomes harder. So the neighbors of i (with index > i) form a contiguous block starting from the smallest index. For j < i, similar.

So the graph is: sort by X. For each i, the neighbors are in some range. Specifically, let L_i be the largest index such that x_i + x_L ≤ C. Then vertices i and j (j ≥ i) are connected iff j ≤ L_i and x_i + x_j ≤ C. But since x is sorted, x_i + x_j ≤ C for all j between i and L_i. So for j ≥ i, the neighbors are exactly the indices from i to L_i (or i to min(L_i, n)). Wait, not quite: we also need x_j to be small enough. But since x is sorted, if x_i + x_{L_i} ≤ C and j ≤ L_i, then x_j ≤ x_{L_i}, so x_i + x_j ≤ x_i + x_{L_i} ≤ C. Yes! So for j ≥ i, the neighbors are a contiguous range [i, L_i] (where L_i is the max index with x_i + x_{L_i} ≤ C).

Similarly for j < i, the neighbors form a range [R_i, i] where R_i is the min index with x_{R_i} + x_i ≤ C. Since x is sorted, R_i is the smallest index with x_{R_i} ≤ C - x_i, which means R_i is the first index in the array where x_{R_i} ≤ C - x_i, so all indices from R_i to i-1 are neighbors.

So overall, for vertex i, its neighbor set is an interval [R_i, L_i] containing i. This is an "interval graph" (on the line of sorted indices). Specifically, it's the graph where each vertex has a contiguous interval of neighbors. This is a proper interval graph or a "unit interval graph"? Not necessarily unit, but it's an interval graph in 1D.

So G_X is an interval graph. Similarly G_Y and G_Z are interval graphs (on different orderings). The intersection of three interval graphs on the same vertex set is a "3-interval graph" or has bounded complexity? In general, intersection of interval graphs is not nice, but here the intervals are defined by sums.

We want max matching in G = G_X ∩ G_Y ∩ G_Z.

Hmm, this is still complex. But note that we can choose the "ordering" for each dimension independently, and the intervals are defined by the sorted order.

Let me try a different approach. Consider the problem from a different angle.

Since the price of a pair is max of three sums, we can think of it as: the pair "uses" the maximum dimension. For each pair, exactly one dimension "wins" (or ties, but we can break ties).

Total price = sum over pairs of max(sumX, sumY, sumZ).

This equals: if we assign each pair to a "responsible" dimension (the one that achieves the max), then total = (sum of X for pairs assigned to X) + (sum of Y for pairs assigned to Y) + (sum of Z for pairs assigned to Z).

Now, for pairs assigned to X-dimension, we have X_a + X_b ≥ Y_a + Y_b and X_a + X_b ≥ Z_a + Z_b. This means (X-Y)_a + (X-Y)_b ≥ 0 and (X-Z)_a + (X-Z)_b ≥ 0.

Similarly for other dimensions.

This suggests: define three "dominance" regions. But this seems hard to optimize globally.

Let me look for a different approach. Given the problem is from a recent contest (ABC 400), the intended solution is likely clever but not overly complex.

I recall a similar problem: "Pair of values" where we have two attributes and the value of a pair is the max of two sums. The solution often involves sorting and greedy matching.

For three attributes, the solution might be: binary search the answer, and for each threshold, check if we can form K pairs with price ≤ threshold.

For the check: we need max matching of size K in graph where edge exists iff all three sums ≤ C.

Now, to check if max matching ≥ K, we can use the following observation: sort cakes by, say, X+Y+Z (or some heuristic). But we need an efficient way.

Let me think about the structure of the edge relation. Edge (i,j) exists iff:
X_i + X_j ≤ C
Y_i + Y_j ≤ C  
Z_i + Z_j ≤ C

This means each cake i has "capacity" in each dimension: it can only pair with cakes that are "small enough" in all dimensions.

Consider the following greedy algorithm: sort cakes by (X_i, Y_i, Z_i) in some order, and for each cake, try to match it with the "most constrained" available partner.

Or, use a flow network: source connects to left vertices, right vertices to sink, edges between i and j if compatible. But this is bipartite matching, which is O(V^3) or O(V^2.5), too slow for N=1e5.

We need a special property. Let me think about the "sum" constraint.

Key observation: For the 1D case (only X constraint), the graph is an interval graph as described, and max matching can be found greedily: sort by X, use two pointers. Specifically: let L = 0, R = n-1. If X[L] + X[R] ≤ C, match them, L++, R--. Else, R-- (the largest cannot match with anyone small enough, so it remains unmatched). This works.

For the 3D case, we have three constraints simultaneously. This is like finding a matching in the intersection of three "sum" graphs.

But note: the graph G is the intersection of three graphs that are each "threshold" or "sum" graphs. The intersection of such graphs is also a "sum" graph? No.

However, I recall that for the problem of "max weight matching" or "max cardinality matching" with multiple sum constraints, we can reduce it.

Alternative approach: since we binary search C, and for each C we check if matching of size K exists. The check can be done by:

- Filter cakes where X_i > C or Y_i > C or Z_i > C: these cannot be in any valid pair.
- For remaining cakes, we need to find a matching of size K in the intersection graph.

Now, here's an idea: sort cakes by X. For each i from 0 to n-1 (in sorted order), we can determine the range of j's that are compatible in X: it's [max(0, lower_i), min(n-1, upper_i)] where lower_i and upper_i are determined by the sum constraint. As argued, the X-compatible partners form an interval in the X-sorted order.

For Y and Z, if we also sort by Y and Z, the compatible partners form intervals in those orderings. But we have a single set of cakes, and we need the partners to be in the intersection of three intervals in three different orderings.

This is similar to the "3D matching" problem which is NP-hard in general. But our intervals are very special: they are defined by sum constraints.

Wait, I think I need to reconsider. Let me re-examine the constraint: for a fixed i, the set of j such that X_i + X_j ≤ C is: {j : X_j ≤ C - X_i}. When we sort by X ascending, this is {j : index(j) ≤ f(i)} for some function f, where f(i) is the largest index with X_{f(i)} ≤ C - X_i. So in the X-sorted order, the X-neighbors of i form a prefix [0, f(i)] if i is in that prefix, or more generally, for each i, the neighbors with index ≥ i are [i, f(i)], and with index < i are [g(i), i-1] where g(i) is the smallest index with X_{g(i)} ≤ C - X_i.

So the X-neighbor set of i is an interval [L_i, R_i] in the X-sorted order, where L_i ≤ i ≤ R_i.

Similarly, in the Y-sorted order, the Y-neighbors form an interval, and in Z-sorted order, the Z-neighbors form an interval.

But the three orderings are different! So the intersection of three interval constraints in three different orderings is not easy.

However, note that the Y-neighbor interval in the Y-sorted order corresponds to some subset of vertices, which when mapped back to the original indices or X-sorted indices, is a set of vertices. We need the intersection of three such sets (one from each dimension).

This is still complex. Let me think if there's a simpler structure.

Alternative idea: since the constraints are symmetric and involve sums, maybe we can transform coordinates. Let U = X+Y+Z, but that doesn't help directly.

Or: consider the projection. For the pair to be valid, we need X_i + X_j ≤ C, Y_i + Y_j ≤ C, Z_i + Z_j ≤ C. This means each cake i must have X_i, Y_i, Z_i all ≤ C (by pairing with a zero, though we may not have zeros, but the cake with smallest value in that dim... actually, if we have a cake with X=0, then X_i ≤ C. But we may not have such cake. However, if no cake has X=0, we can't directly conclude X_i ≤ C for a cake in a valid pair. Wait: if cake i pairs with cake j, then X_i + X_j ≤ C. Since X_j ≥ 0, we have X_i ≤ C. Yes! Because X_i + X_j ≤ C and X_j ≥ 0 implies X_i ≤ C. Similarly for Y and Z. So any cake in a valid pair must have all three attributes ≤ C.

So the necessary condition is: X_i ≤ C, Y_i ≤ C, Z_i ≤ C. Let's call these "C-feasible" cakes.

So we filter to cakes with all three attributes ≤ C. For these, we need to find a matching of size K where additionally X_i + X_j ≤ C, etc.

Now, for these cakes, note that X_i + X_j ≤ C and X_i, X_j ≤ C. 

Now, here's a key insight: sort the feasible cakes by X. For any pair (i,j) with i before j in X-sorted order, we have X_i ≤ X_j. The X-constraint is X_i + X_j ≤ C.

Consider the following approach: 
- Sort by X ascending.
- We will try to match cakes greedily.
- But we also need to satisfy Y and Z constraints.

Perhaps we can use a "water filling" or "flow" approach with a specific structure.

Another idea: the problem is equivalent to: find K disjoint pairs such that for each pair, the componentwise sum is bounded by C. This is like a 3-dimensional assignment.

Given the time, let me consider a different approach: maybe the answer can be found by considering all pairs and using a matching algorithm, but with a bipartite structure.

Wait, I think I have it! We can use the following:
- For a given C, define a bipartite graph? No, it's a general graph.
- But we can make it bipartite by duplicating vertices? No.

For general graphs, maximum matching is polynomial but slow for N=1e5.

However, the graph has special structure. Specifically, if we sort by X, the X-constraint means that in the X-sorted order, compatible pairs are "close" in a sense. But we have three constraints.

Let me think about small cases or relaxations.

Actually, I found a key insight: the condition X_i + X_j ≤ C AND Y_i + Y_j ≤ C AND Z_i + Z_j ≤ C is equivalent to: for each cake i, define its "type" or use a threshold.

Consider the following transformation: for each cake i, define a_i = X_i, b_i = Y_i, c_i = Z_i. We need pairs where a_i + a_j ≤ C, etc.

This is exactly the condition that the L_infinity distance or something? Not quite.

Note that a_i + a_j ≤ C means max(a_i, a_j) ≤ C - min(a_i, a_j) ≤ C. But that's not helpful.

Let me try: sort all cakes by X. Let the sorted cakes be p_1, p_2, ..., p_m (only those with X_i ≤ C, Y_i ≤ C, Z_i ≤ C). For any pair (p_i, p_j) with i < j, we need:
X_{p_i} + X_{p_j} ≤ C (automatically true if both ≤ C and their sum ≤ C, which is the condition)
Y_{p_i} + Y_{p_j} ≤ C
Z_{p_i} + Z_{p_j} ≤ C

The Y and Z conditions are independent of the X-sorted order. So for a fixed p_i, the set of p_j (j > i) that are compatible in all three dimensions is: {j : Y_{p_i} + Y_{p_j} ≤ C AND Z_{p_i} + Z_{p_j} ≤ C}.

In the X-sorted order, this set is some subset. It's the intersection of a Y-condition and Z-condition.

Now, for the Y-condition: Y_{p_i} + Y_{p_j} ≤ C. If we also know the Y-values, this defines a subset. In general, in the X-sorted order, the Y-values are in some arbitrary order, so the set of j with Y_{p_j} ≤ C - Y_{p_i} is an arbitrary subset.

This doesn't give nice structure.

Maybe the approach is: binary search C, and for each C, we need to check if a matching of size K exists in this graph. The check is the hard part.

For the check, we can try to use an augmenting path algorithm, but with N=1e5, we need it to be fast on this specific graph.

The graph is defined by: edge (i,j) exists iff for all dim d in {X,Y,Z}: d_i + d_j ≤ C.

This means: i and j are "compatible" if they are not too large together in any dimension.

Consider building the graph implicitly. We want to find if there's a matching of size K. By Hall's theorem or max-flow min-cut, we can check this.

But how to construct the flow network efficiently? The bipartite graph would be: left copy and right copy of vertices, edges between left i and right j if compatible, and also left j and right i (but that's the same). Actually, since the graph is undirected, we can make it bipartite by the standard trick: create a bipartite graph with left = vertices, right = vertices, and for each undirected edge {i,j}, add directed edges i->j and j->i? No, that's not right.

For undirected matching, we can use Edmonds' algorithm (blossom algorithm), which is O(N^3) in general, but for our graph, it might be faster, or we can use the structure.

Given the complexity, and that this is a competitive programming problem with N up to 1e5, there must be a simpler insight.

Let me reconsider the problem from the beginning. The price is max of three sums. We want to maximize the sum of prices over K pairs.

For each pair, the price is determined by the "best" dimension. So we can think: for each pair, we pay the maximum of three things.

This is similar to: we have three "currencies" and for each pair, we get the maximum value in any currency. We want to choose pairs to maximize the total.

Intuitively, we should pair cakes that are strong in the same dimension. For example, if two cakes both have high X, then their X-sum is high, likely making max large. But they might also both have high Y, so Y-sum is also high.

In fact, if two cakes have (X_i, Y_i, Z_i) and (X_j, Y_j, Z_j), the price is max(X_i+X_j, Y_i+Y_j, Z_i+Z_j). This is large if they are both large in at least one common dimension.

So the strategy is: find pairs that "align" in their large coordinates.

Specifically, if we sort cakes by X (or by any linear combination), we might be able to pair them.

But the problem is symmetric in X,Y,Z, so no single dimension is special.

I think the solution might be: 
1. For each cake, consider it as a point in 3D.
2. The pair price is the max norm of the sum: ||(X_i+X_j, Y_i+Y_j, Z_i+Z_j)||_infinity.
3. We want to choose K pairs to maximize the sum of these max-norms.

This is a hard optimization problem. But for the decision version (can we achieve at least M?), we can use binary search and check if there's a pairing with sum ≥ M.

Wait, no, the objective is to maximize, so we binary search the answer: is there a pairing with total price ≥ M? But the check is still hard.

Actually, for maximization, we binary search on the answer C: is there a pairing with total price ≥ C? For a fixed C, we need to check if max total price ≥ C. This is equivalent to: can we achieve total ≥ C? But this is not obviously easier.

Standard approach for max sum of pair values: binary search C, check if we can form pairs with total ≥ C. The check is: can we select K pairs with each pair having price ≥ some threshold? No, that's for the decision.

For "max total ≥ C", we can ask: is there a set of K pairs with total ≥ C? This is NP-hard in general, but here the structure helps.

For this problem, since each pair price is non-negative, and we want to maximize, we can use binary search on the answer C, and for each C, check if we can form a matching of size K where each edge has price ≥ ? No, that doesn't help for the total.

Alternatively: since the total is sum of max, and we want to maximize, we can use the following: sort all possible pairs by price descending, and try to select K disjoint pairs with max total. But selecting max weight matching in a general graph is hard.

Given the difficulty, let me search my memory for the problem "ABC 400 assorted cakes" or similar. This looks like a problem from AtCoder.

The problem title is "Commemorative Cake" or "Assorted Cakes" from ABC 400. I think the solution uses the following insight:

For each cake i, define its "value" as max(X_i, Y_i, Z_i)? No.

Another idea: the price of a pair is max of three sums. We can use the inequality: max(A,B,C) ≥ (A+B+C)/3. So the total is at least sum over pairs of (X_i+X_j + Y_i+Y_j + Z_i+Z_j)/3 = (2 * sum of all X + 2 * sum of all Y + 2 * sum of all Z) / 3 = 2/3 * (sum X + sum Y + sum Z). This is a lower bound, but not helpful for exact solution.

For the exact solution, I think the key is:
- The answer is determined by the K largest pair prices, and we need to check if they can be realized.
- Or: the optimal solution pairs cakes that are "extremal" in some sense.

Let me think about a simpler case: 1D. If we only had one attribute, say X, then price of pair = X_i + X_j, and we want to maximize sum of X_i+X_j over K pairs. This is equivalent to: select 2K cakes and pair them to maximize sum. The maximum is achieved by sorting by X and pairing the largest with largest: (1st with 2nd), (3rd with 4th), etc. The total is 2 * (X_1+X_3+...+X_{2K-1}) if sorted descending. Or equivalently, sum of the 2K largest X values, but paired optimally. Actually, if we sort X descending: x_1 ≥ x_2 ≥ ... ≥ x_n, then to maximize sum of sums of K pairs, we should pair (1,2), (3,4), ..., (2K-1, 2K), giving total 2*(x_1 + x_3 + ... + x_{2K-1}). Alternatively, we could pair (1,3), (2,4), but that gives x_1+x_3 + x_2+x_4 = same. So the max is 2 * sum of the 2K largest X values? No: x_1+x_2 + x_3+x_4 + ... + x_{2K-1}+x_{2K} = sum of top 2K values. Yes! Because any pairing of 2K elements gives the same sum of all values, so the sum of pair-sums is sum of the 2K values, regardless of pairing. So in 1D, any pairing of the top 2K elements gives the same total = sum of top 2K X values.

Interesting! In 1D, the total is independent of the pairing, as long as we use the 2K largest values. The max total is sum of 2K largest X values.

For 3D with max, the total depends on pairing. For example, with two elements (K=1), we have three cakes (N=3), and we pick one pair. The max of three sums depends on which pair.

So the 3D case is genuinely harder.

But notice: for a fixed set of 2K cakes, the total price is sum over pairs of max of three sums. This depends on how we pair them.

So the problem is: choose 2K cakes and pair them to maximize sum of max sums.

This is still hard.

However, there's a crucial observation: for any pairing, the total price is at least the sum of the K largest "pair potentials", but we need to find the best pairing.

Given the time I've spent, let me try to recall or derive the solution.

I think the solution involves the following:
- For each cake, consider it as having three coordinates.
- Sort cakes by X + Y + Z or some function.
- Use a greedy algorithm: for the largest cake, pair it with the "best" available cake.
- "Best" is defined as the one that maximizes the pair price.

But greedy might not be optimal.

Another thought: the pair price is max of three sums. We can think of it as: for each pair, the price is the value of the "dominating" dimension. So if we could assign each pair to a dimension and ensure that the sum in that dimension is at least some value.

Specifically, if we can partition the K pairs into three groups: X-group, Y-group, Z-group, where:
- For X-group pairs, the X-sum is at least the Y-sum and Z-sum.
- The total is (sum of X-sums for X-group) + (sum of Y-sums for Y-group) + (sum of Z-sums for Z-group).

And we want to maximize this subject to each cake used once.

This is like a maximum weight matching in a 3-partite hypergraph, hard.

But with the constraint that the price is exactly the max, we have for each pair: the price equals the max, so the price is at least the average of the three sums, and equals the max.

I think I need to look for a different characterization.

Let me consider the complement: we want to find the maximum C such that we cannot achieve total ≥ C? No, we want to find the max achievable.

Binary search on C, check if achievable total ≥ C. The check: can we find K pairs with total ≥ C? This is equivalent to: can we assign each cake to a pair or leave unpaired, such that the sum of maxes ≥ C?

This is still hard.

Wait, for the decision version "is the max total ≥ C?", we can use the fact that for any pairing, total = sum of max(X_sum, Y_sum, Z_sum). We can lower bound this by considering that each pair contributes at least the max of the three sums. To get a lower bound on the max total, we can use: max total ≥ C if there exists a pairing with sum of maxes ≥ C.

To check if there exists a pairing with sum ≥ C, we can try to construct one. But it's hard.

Alternatively, for the purpose of binary search, we need to know if the answer is ≥ C. We can try to find a lower bound by a heuristic, and an upper bound by another heuristic, and binary search is not helpful if we can't check.

Given the complexity, I suspect the problem has a simpler solution that I'm missing. Let me read the problem again.

The price is max of three sums. N up to 1e5. K up to N/2.

I think the solution is to use the following:
- For each cake i, define its "score" as max(X_i, Y_i, Z_i) or something.
- Sort cakes by this score.
- Pair them in a specific way.

But that doesn't give the exact value.

Another idea: since all attributes are non-negative, the pair price is non-negative. We want to maximize the sum.

Consider the following: the answer is at most 2 * sum of max(X_i, Y_i, Z_i) over the 2K cakes, but we can choose which 2K.

Actually, note that for any pair (a,b), max(X_a+X_b, Y_a+Y_b, Z_a+Z_b) ≤ (X_a+Y_a+Z_a) + (X_b+Y_b+Z_b) - min(X_a+X_b, Y_a+Y_b, Z_a+Z_b) ≤ sum of all attributes.

Not helpful.

Let me try to think of the problem as: we have 3 "colors" X,Y,Z. For each pair, we get the max sum in any color. We want to maximize the total.

I recall a similar problem: "Given N items with three attributes, form K pairs to maximize sum of max attribute sums." The solution is O(N log N) using sorting and a priority queue or balanced BST.

The key insight: sort the cakes by (say) X_i in descending order. Then for each cake, we want to pair it with a cake that has large Y or Z to boost the max.

Specifically, if we process cakes in order of decreasing X, then for each such cake, we should pair it with an available cake that has the maximum possible "value" in terms of Y+Z or something.

Let's formalize: when we pair cake a (with high X) with cake b, the price is max(X_a+X_b, Y_a+Y_b, Z_a+Z_b). If X_a is very large, then X_a+X_b is likely the max, so the price is approximately X_a + X_b. So to maximize, we want to pair high-X cakes with high-X cakes. But if we pair two high-X cakes, the X-sum is high, so good.

But wait, if we pair two cakes that both have high X and low Y,Z, the price is high X-sum. If we pair a high-X cake with a high-Y cake, the price is max(high + low, high + low, ...) which might be lower.

So intuitively, to maximize, we should group cakes by their "dominant" attribute and pair within groups.

Specifically:
- Group A: cakes where X is the max (or tied for max) of the three.
- Group B: cakes where Y is the max.
- Group C: cakes where Z is the max.

Then pair within groups? But we can also cross-pair.

If we pair two cakes from group A (both X-dominant), their X-sums are likely high, and the price is high. If we pair from different groups, say one X-dominant and one Y-dominant, then X_a + X_b might be medium, Y_a+Y_b might be medium, Z_a+Z_b small. The max is medium, likely lower than pairing within group.

So the optimal is to pair within dominant groups. But we might have odd numbers or want to mix.

In fact, for each pair, the price is the max of three sums. For the pair to have high price, they need to be strong in the same dimension.

This suggests: for each dimension d, we can form pairs using cakes that are strong in d, and the contribution is roughly the sum of d-values.

To maximize the total, we should assign each cake to the dimension where it is strongest, and then within each dimension, pair the assigned cakes to maximize the sum of sums in that dimension. But wait, the price is the max, so if a cake is strongest in X, but when paired with another X-strong cake, the max is X-sum, so we get the X-sum. If paired with a Y-strong cake, the max might be X_a+Y_b or X_b+Y_a, which could be lower.

So yes, the optimal is to group by dominant attribute and pair within groups.

Specifically:
1. For each cake, let d_i = argmax(X_i, Y_i, Z_i) (break ties arbitrarily).
2. Partition cakes into three groups based on d_i.
3. Within each group, pair the cakes to maximize the sum of (d_i + d_j) for the pairs, where d is the attribute.

But step 3: if we have a group with attribute X, and we want to maximize the sum of X_i + X_j over pairs in this group, then as in the 1D case, it's best to take the cakes with largest X values in this group, and any pairing gives the same total: sum of X for the paired cakes (which is 2 * sum of X of the first element of each pair, or just sum of all X of used cakes). To maximize, we use as many large X cakes as possible.

Specifically, if group X has m_X cakes, and we use 2k_X of them for k_X pairs, the contribution is sum of X_i for the 2k_X cakes used. To maximize, we should use the 2k_X cakes with largest X in this group.

Similarly for Y and Z groups.

But we have the constraint that total pairs = k_X + k_Y + k_Z = K, and for each group, the number of pairs is at most floor(m_d / 2).

So the problem reduces to: choose k_X, k_Y, k_Z ≥ 0 with k_X+k_Y+k_Z = K and 2k_X ≤ m_X, 2k_Y ≤ m_Y, 2k_Z ≤ m_Z, to maximize:
- (sum of top 2k_X X-values in X-group) + (sum of top 2k_Y Y-values in Y-group) + (sum of top 2k_Z Z-values in Z-group).

But is this optimal? We assumed that for pairs within the X-group, the price is exactly the X-sum. Is that true? For a pair (a,b) both in X-group, we have X_a ≥ Y_a, X_a ≥ Z_a, and X_b ≥ Y_b, X_b ≥ Z_b. Then X_a+X_b ≥ Y_a+Y_b and X_a+X_b ≥ Z_a+Z_b, so yes, max is X_a+X_b. So price = X_a+X_b.

Similarly for Y and Z groups.

What about pairs that cross groups? For example, a in X-group and b in Y-group. Then X_a ≥ Y_a, Z_a; Y_b ≥ X_b, Z_b. The max is max(X_a+X_b, Y_a+Y_b, Z_a+Z_b). This could be X_a+X_b or Y_a+Y_b, depending on which is larger. In general, it's not clear that crossing groups is bad, but intuitively, if we have many cakes, we can sort within groups and pair the best.

In fact, the optimal solution might involve only within-group pairs, because crossing gives at most the max of the two cross-sums, which is likely less than pairing two strong X's together.

Formally, for any cross pair (a from X-group, b from Y-group), the price is max(X_a+X_b, Y_a+Y_b, Z_a+Z_b) ≤ X_a + Y_b + something? Not sure.

But here's a key: if we can achieve the maximum by only within-group pairs, then the problem is easy: for each group, sort by the relevant attribute, and compute prefix sums, then DP to choose how many pairs to take from each group.

Is it always optimal to pair within groups? Suppose we have a cross pair. We can compare it to the best within-group pairs. By an exchange argument, if we have a cross pair and a within-X pair unused, we might swap.

Specifically, suppose we have a cross pair (a,b) with a in X, b in Y. And we have two unused cakes c,d in X-group. The contribution of (a,b) is max(X_a+X_b, Y_a+Y_b, Z_a+Z_b). The contribution of pairing c with d is X_c+X_d. If X_c+X_d is large, we prefer it.

But a and b might be "bad" in their groups, so we pair them cross to use them up.

In the optimal solution, we want to use the best possible pairs. The within-group pairs give us the X-sum, which is high. Cross pairs give at most max(X_a+X_b, Y_a+Y_b), which is at most X_a + Y_b if X_a is the max for a, but not necessarily high.

Actually, I claim that the optimal solution is to pair within groups. Here's an informal argument: for any optimal pairing, consider the pairs. If a pair is cross-group, say X and Y, then we can "improve" it by swapping. But this might not be rigorous.

However, for the purpose of the problem, this approach might be correct. Let me check with the sample.

Sample 1: 3 cakes, K=1.
Cake 1: (6,3,8) -> max is 8 (Z), so Z-group.
Cake 2: (3,5,0) -> max is 5 (Y), so Y-group.
Cake 3: (2,7,3) -> max is 7 (Y), so Y-group.

So groups: Z: [1], Y: [2,3].
Within Z: no pairs.
Within Y: pair (2,3), contribution = Y_2 + Y_3 = 5+7=12. Total 12.
Sample answer: 12. Correct.

Sample 2, first test: 5 cakes, K=2.
Cakes 1-4: (1,2,3) -> max Z=3, Z-group.
Cake 5: (100,100,200) -> max Z=200, Z-group.
So all in Z-group.
Z-values: 3,3,3,3,200.
Sort by Z desc: 200, 3,3,3,3.
For 2 pairs (4 cakes), use top 4: 200,3,3,3.
Sum of Z for these 4: 200+3+3+3=209.
Any pairing gives total 209. Sample: 209. Correct.

Second test of sample 2: 6 cakes, K=2.
Cakes:
1: (21,74,25) -> max Y=74, Y-group
2: (44,71,80) -> max Z=80, Z-group
3: (46,28,96) -> max Z=96, Z-group
4: (1,74,24) -> max Y=74, Y-group
5: (81,83,16) -> max Y=83, Y-group
6: (55,31,1) -> max X=55, X-group

Groups:
X: [6] (X=55)
Y: [1,4,5] (Y: 74,74,83)
Z: [2,3] (Z: 80,96)

We need K=2 pairs.
Within X: no pairs.
Within Y: can make 1 pair (2 cakes). Top 2 Y: 83 and 74, sum = 157.
Within Z: can make 1 pair (2 cakes). Sum = 80+96=176.
Total = 157+176=333.
Sample: 333. Correct.

So in both samples, the optimal is to pair within dominant groups, using the largest values in each group.

Therefore, the algorithm is:
1. For each cake, determine its dominant attribute: d_i = argmax(X_i, Y_i, Z_i). Break ties arbitrarily (e.g., prefer X then Y then Z).
2. Partition into three groups.
3. For each group, sort the cakes by the dominant attribute value (descending).
4. Compute prefix sums of these sorted values.
5. Use DP: dp[i][j] = max total using i pairs total, with j pairs from group 1 (or iterate groups).
   Since K ≤ N/2 ≤ 5e4, and we have 3 groups, we can do DP over the groups.
   Specifically, for each group, we have a sorted list v_1 ≥ v_2 ≥ ... ≥ v_m.
   The contribution for using 2t cakes (t pairs) from this group is sum_{k=1}^{2t} v_k, which is the prefix sum.
   So for each possible number of pairs t (0 ≤ t ≤ floor(m/2)), the max contribution from this group is prefix_sum[2t].
   Then we need to choose t1, t2, t3 with t1+t2+t3=K, to maximize sum of prefix sums.
   This is a knapsack-like DP with 3 items groups, each group has options (t, cost), and we want to maximize sum.
   Since 3 groups, we can compute all possible totals for two groups, then combine with the third.
   Or simply iterate: for t1 in 0..min(K, floor(m1/2)), for t2 in 0..min(K-t1, floor(m2/2)), t3 = K-t1-t2, check if feasible, update max.

   The complexity: for each group, the number of possible t is up to N/2. So three nested loops could be O(N^2) in the worst case. But since we have only 3 groups, we can do:
   - Precompute for group 1: for each t, value = prefix1[2t].
   - For group 2: for each t, value = prefix2[2t].
   - For group 3: for each t, value = prefix3[2t].
   - Then iterate t1 from 0 to min(K, max_t1), t2 from 0 to min(K-t1, max_t2), t3 = K-t1-t2, if t3 <= max_t3, update ans = max(ans, val1[t1] + val2[t2] + val3[t3]).
   The loops are bounded by K for t1 and t2, so O(K^2). K can be up to 5e4, so O(K^2) is 2.5e9, too slow.

   Better: precompute all possible (t, val) for groups 1 and 2, then for each t1+t2 = s, we have a set of values. But we need the max val1[t1]+val2[t2] for each s. This is a convolution-like operation, but with only addition and max, we can compute the max sum for each s in O(K * min(K, m1, m2)). Actually, since we have only two groups to combine, we can do:
   For s = 0 to K:
      best12[s] = max over t1=0..s of (val1[t1] + val2[s-t1]) where feasible.
   Then for s from 0 to K:
      ans = max over t3 of best12[K-t3] + val3[t3].
   The first part is O(K^2), still O(K^2).

   Since K can be 5e4, O(K^2) is too slow (2.5e9 operations). We need O(N log N) or O(N).

   But note: the groups are disjoint, and the total number of cakes is N. The DP over groups might be optimized because the "cost" is the number of pairs, and we are choosing how many pairs from each group. This is a 3-choice knapsack which can be solved in O(K) if we do it cleverly? Not really, with 3 groups and choices O(K), it's O(K^2).

   However, N is 1e5, K is up to 5e4. O(N log N) is fine, but O(K^2) is not.

   Can we do better? Since the value for taking t pairs from a group is the sum of top 2t values in that group, and this is a concave function? Not necessarily.

   But note: we have only 3 groups, so the number of "items" is small. However, each group has many options.

   Wait, we can observe that the value function f_d(t) = prefix_sum_d[2t] is a piecewise linear, concave function? For sorted values v_1 ≥ v_2 ≥ ... ≥ v_m, the prefix sum S_k = sum_{i=1}^k v_i. Then f(t) = S_{2t}. The marginal gain f(t+1) - f(t) = v_{2t+1} + v_{2t+2}, which is non-increasing (since v is sorted descending). So f is a concave function (increasing marginal returns decreasing).

   For concave functions, the sum f1(t1) + f2(t2) + f3(t3) with t1+t2+t3=K is maximized at extreme points? No, for concave functions, the sum is also concave, and the maximum over a simplex is at a vertex, meaning t1, t2, t3 should be as "unequal" as possible. Specifically, since f is concave, the sum is concave, so the maximum is at the boundary. That means we should put as many pairs as possible into the group with the highest marginal gain.

   But we need the exact maximum. Since f is concave, the optimal solution can be found by a greedy-like approach: we can use the fact that the derivative (marginal gain) is decreasing, so we should allocate pairs to the group with the largest marginal gain at each step. This is a water-filling or marginal allocation.

   Specifically, we can think of it as: we have 3 groups, each has a "supply" of pairs: m_d/2. We want to buy K units. The cost of buying the t-th unit in group d is the marginal gain: g_d(t) = v_{2t-1} + v_{2t} (for t≥1, with v_0=0). We want to select K units (each unit is a pair) from the groups, each group up to its capacity, to maximize the sum of values, which is sum of marginal gains for the selected units. This is exactly: select the K largest marginal gains from the union of all groups, with the constraint that from each group d, we can only take the first t marginal gains in order (i.e., g_d(1), g_d(2), ... up to capacity).

   But since the marginal gains are sorted within each group (non-increasing), the optimal is to simply take the K largest values from the multiset of all marginal gains, subject to the capacity constraint per group. Since within each group the marginal gains are sorted, and we are taking the largest overall, and we have a capacity per group, the optimal is: merge the three sorted lists of marginal gains, and take the top K, but with the constraint that from each list we take at most its capacity. This is equivalent to: we have three sorted lists, we want the top K elements from the union, with per-list limits. This can be done by merging or by a priority queue, but the per-list limit is just the length of the list.

   Wait, the capacity is the number of available marginal gains in that list, which is floor(m_d/2). So we have three sorted lists of marginal gains, each of length L_d = floor(m_d/2). We want to select K elements from the union, at most L_d from list d, to maximize the sum. This is a standard "select top K from multiple sorted lists with limits", but since we can take all elements, and we want the sum of the selected, it's simply: we want the K largest elements from the union, with the limit that we can only take what is available. But the limit is just that there are only L_d elements in list d. So the constraint is automatically satisfied if we take elements from the lists. So the problem reduces to: given three sorted arrays of marginal gains, find the sum of the K largest elements among them.

   But is that correct? Let's see. The total value for taking t_d pairs from group d is sum_{i=1}^{t_d} (v_{2i-1} + v_{2i}) = sum of the first t_d marginal gains. So yes, the total is the sum of the selected marginal gains. And we want to maximize this sum, which is equivalent to selecting the K largest marginal gains from the union of the three groups, with the constraint that from group d we can select at most L_d = floor(m_d/2) elements. But since each group has exactly L_d elements, and we want K elements total, the constraint is just that we select at most L_d from each, which is automatically satisfied as long as we don't select more than exist. So the maximum sum is simply the sum of the K largest marginal gains among all three groups.

   Is that right? We have three lists of marginal gains, each sorted descending. We want to pick K items total, at most L_d from list d, to maximize sum. Since the lists are disjoint in items, and we want the largest items, the optimal is to take the K largest items from the union, provided that we don't exceed L_d. But since L_d is the number of items in list d, and the K largest items from the union are distributed among the lists, and the number from list d in the top K is at most L_d (because there are only L_d items in list d). So the constraint is automatically satisfied! The only issue is if we want to take more than L_d from a list, but we can't, and the top K from the union won't include more than L_d from any list because there are only L_d items in that list. So yes, the answer is the sum of the K largest marginal gains from the three groups.

   Therefore, the algorithm is:
   1. For each cake, determine its dominant attribute d_i.
   2. Group by d_i.
   3. For each group, sort the cakes by the value of the dominant attribute, descending.
   4. Compute the marginal gains for this group: for pair index p from 1 to floor(m/2), the marginal gain is v_{2p-1} + v_{2p}, where v is the sorted values.
   5. Collect all marginal gains from the three groups into one big list.
   6. Sort this list in descending order.
   7. The answer is the sum of the first K elements of this sorted list.

   This is O(N log N).

   Let me verify with the samples.

   Sample 1: K=1.
   Cakes: 1:(6,3,8) max Z=8; 2:(3,5,0) max Y=5; 3:(2,7,3) max Y=7.
   Groups:
   Z: cake 1, value Z=8. m=1, L=0 (since floor(1/2)=0). No marginal gains.
   Y: cakes 2,3. Values Y: 5,7. Sort desc: 7,5. Marginal gain for first pair: 7+5=12. So one marginal gain: 12.
   X: empty.
   Big list: [12]. Top K=1: sum=12. Correct.

   Sample 2, first: K=2.
   Cakes 1-4: max Z=3, Z-group.
   Cake 5: max Z=200, Z-group.
   Z-group values: 200, 3,3,3,3. Sort: 200,3,3,3,3.
   m=5, L=2 pairs. Marginal gains: pair1: 200+3=203; pair2: 3+3=6.
   List: [203, 6]. Top K=2: 203+6=209. Correct.

   Sample 2, second: K=2.
   Groups:
   Y: cakes 1,4,5. Values Y: 74,74,83. Sort: 83,74,74. m=3, L=1. Marginal gain: 83+74=157.
   Z: cakes 2,3. Values Z: 80,96. Sort: 96,80. Marginal: 96+80=176.
   X: cake 6. Value X=55. m=1, L=0. No marginal.
   List: [157, 176]. Top 2: 157+176=333. Correct.

   So the algorithm works for the samples.

   But is it always correct? We need to verify that the optimal solution can be achieved by pairing within dominant groups, and that the marginal gain argument holds.

   First, we assumed that in the optimal solution, we only pair cakes within the same dominant group. Is this always true?

   Consider a cross pair: cake a from X-group (so X_a ≥ Y_a, X_a ≥ Z_a) and cake b from Y-group (Y_b ≥ X_b, Y_b ≥ Z_b). The price is max(X_a+X_b, Y_a+Y_b, Z_a+Z_b).

   Compare this to pairing a with another X-group cake c, and b with another Y-group cake d. The prices are X_a+X_c and Y_b+Y_d. We need to check if max(X_a+X_b, Y_a+Y_b) ≤ X_a+X_c + Y_b+Y_d, but that's sum vs max, not comparable.

   We need to show that there is an optimal solution with no cross pairs. Or that the value achieved by within-group pairs is at least as good.

   Actually, our algorithm computes the best within-group pairing. It might be that cross pairs give a higher value. But the samples work. Is there a counterexample?

   Let's construct a potential counterexample. Suppose we have two X-group cakes with X=10, Y=1, Z=1. And two Y-group cakes with X=1, Y=10, Z=1. And K=2.

   Groups:
   X: two cakes, both with X=10. Sort by X: both 10. Marginal: 10+10=20.
   Y: two cakes, both with Y=10. Marginal: 10+10=20.
   Total within: 20+20=40.

   Cross pair: pair an X and a Y. Price = max(10+1, 1+10, 1+1) = max(11,11,1)=11. Two cross pairs: 11+11=22. Or pair the two X's: 20, and two Y's: 20, total 40. So within is better.

   Another example: X-group: cake A (10,1,1). Y-group: cake B (1,10,1), cake C (1,10,1). K=1.
   Within Y: pair B and C, price Y_sum=20.
   Cross: pair A and B, price max(10+1,1+10,1+1)=11.
   So within is better.

   What if the cross pair is better? For cross pair (a from X, b from Y), the price is max(X_a+X_b, Y_a+Y_b). This is at most X_a + Y_b (if X_a ≥ Y_a and Y_b ≥ X_b, but not necessarily). Actually, max(X_a+X_b, Y_a+Y_b) ≤ X_a + Y_b? Not always. For example, if X_a=5, Y_a=5, X_b=5, Y_b=5, then max(10,10)=10, but X_a+Y_b=10. If X_a=10, Y_a=1, X_b=1, Y_b=10, max(11,11)=11, X_a+Y_b=20. So X_a+Y_b could be larger.

   In general, max(X_a+X_b, Y_a+Y_b) ≤ max(X_a, Y_a) + max(X_b, Y_b) = X_a + Y_b (since a in X-group, b in Y-group). So price ≤ X_a + Y_b.

   But X_a + Y_b is the sum of the dominant attributes. And our within-group pairing gives us X_a + X_c for some c, and Y_b + Y_d for some d. We have X_a + X_c + Y_b + Y_d ≥ X_a + Y_b (since X_c,Y_d ≥0). But that's the sum of two pairs vs one pair. For a fair comparison, we need to consider the allocation.

   In the marginal gain framework, we are effectively saying that the value of a pair in group X is X_i + X_j, and in group Y is Y_i + Y_j. The cross pair value is max(X_i+X_j, Y_i+Y_j, Z_i+Z_j) which is at most X_i + Y_j (for i in X, j in Y). But X_i + Y_j ≤ X_i + Y_j, and if we had paired i with i' in X, we get X_i + X_{i'}, and j with j' in Y, we get Y_j + Y_{j'}. We have X_i + X_{i'} + Y_j + Y_{j'} ≥ X_i + Y_j (since X_{i'}, Y_{j'} ≥ 0). But this is the sum of two pairs. To compare, we need to see if the cross pair plus another cross pair is better than two within pairs.

   Actually, the key is: for any cross pair, we can "decompose" it into contributions to the marginal gains? Not exactly.

   I think the proof is that the optimal solution is to pair within groups, and the value is the sum of the K largest marginal gains. This is because:
   - The value function is linear in the sense of marginal gains.
   - The marginal gains for a group are the values of the pairs in that group.
   - Since we can choose any number of pairs from each group, and the pairs are independent, the problem is to select K pairs from the "pool" of all possible within-group pairs, with the constraint that we use disjoint cakes.
   - But within a group, the pairs are constrained by the availability. However, as we saw, the set of achievable total values from a group is exactly the prefix sums of sorted marginal gains, which corresponds to taking the first t pairs in sorted order.
   - Since the groups are disjoint, the combined problem is to select t1,t2,t3 pairs from the three groups, which is equivalent to selecting K items from the multiset of marginal gains, with the limit that from each group we take at most the available number, but since the marginal gains are naturally ordered, the best is to take the K largest.
   - And cross pairs are not needed because any cross pair has value at most the sum of the dominant attributes, which is at most the value of within-group pairs using those cakes? Not exactly.

   However, to be rigorous, we need to ensure that no cross pair is better. But the problem is from a contest, and this is likely the intended solution: the answer is the sum of the K largest "pair scores" where a pair score is the sum of the two values of the dominant attribute, formed by pairing within groups.

   Let me check the constraints: the sum of N is 1e5, T up to 1000. O(N log N) per test case is fine.

   The algorithm:
   1. For each cake, find d = argmax(X, Y, Z). (For ties, can choose any, say the first max).
   2. Group by d.
   3. For each group, extract the value of attribute d, sort descending.
   4. For each group, compute the list of pair values: for i from 0 to len(group)//2 - 1, pair_value = v[2i] + v[2i+1].
   5. Collect all pair_values from the three groups into one list.
   6. Sort this list descending.
   7. The answer is the sum of the first K elements of this list.

   Complexity: O(N log N).

   Let's test on a custom case to see if it might fail.
   Suppose: N=4, K=2.
   Cake 1: X=100, Y=0, Z=0 -> X-group, val=100.
   Cake 2: X=0, Y=100, Z=0 -> Y-group, val=100.
   Cake 3: X=0, Y=0, Z=100 -> Z-group, val=100.
   Cake 4: X=0, Y=0, Z=0 -> say X-group, val=0.
   Groups: X: [100,0], Y: [100], Z: [100].
   Pair values: X-group: 100+0=100. Y: no pair (only 1). Z: no pair.
   List: [100]. K=2, but only one pair available? Actually, we have 4 cakes, K=2, so we need two pairs. We have only one possible within-group pair: (1,4) with value 100. The other two cakes (2 and 3) are alone, so we cannot form a second within-group pair. So the algorithm would say: only one pair value 100, cannot get two pairs, so sum is 100? But we need K=2 pairs.

   Wait, the problem says K pairs, so we must use exactly K pairs, i.e., 2K distinct cakes. In this case, N=4, K=2, so we must use all 4 cakes. We have to form two pairs. The possible pairings: (1,2) and (3,4), or (1,3) and (2,4), or (1,4) and (2,3).
   Compute:
   (1,2): max(100+0, 0+100, 0+0) = 100.
   (1,3): max(100+0, 0+0, 0+100) = 100.
   (1,4): max(100+0, 0+0, 0+0) = 100.
   (2,3): max(0+0, 100+0, 0+100) = 100.
   (2,4): max(0+0, 100+0, 0+0) = 100.
   (3,4): max(0+0, 0+0, 100+0) = 100.
   So any pairing gives 100 per pair, total 200.
   But our algorithm: groups: X: cakes 1 and 4, with X values 100 and 0. Pair value 100. Y: cake 2, alone. Z: cake 3, alone. So only one pair possible. The sum of K=2 largest pair values: only one available, so sum=100. But the correct answer is 200.

   So the algorithm fails here! Why? Because we forced pairing within dominant groups, but here we can cross-pair to use all cakes. And in this case, cross-pairing is necessary because we have only one cake in some groups.

   In this example, the dominant groups are strict, but we have isolated cakes. The algorithm only considers within-group pairs, but we can also form cross pairs. The cross pair value is 100, same as within. So we can get total 200 by two cross pairs, e.g., (1,2) and (3,4), or (1,4) and (2,3).

   So we need to consider cross pairs as well! The algorithm is incomplete.

   So the assumption that optimal pairs only within groups is false when there are leftover cakes.

   Therefore, we need a more general approach.

   The problem is: we have 3 groups. We can form within-group pairs, and also cross-group pairs. Cross-group pairs have value max(X_a+X_b, Y_a+Y_b, Z_a+Z_b) for a in group A, b in group B.

   This is complex. We need to find the maximum weight matching in the complete graph on N vertices with these specific weights.

   The graph is complete, and the weight of edge (i,j) is max(X_i+X_j, Y_i+Y_j, Z_i+Z_j). We want maximum weight matching of size K.

   This is a maximum weight K-matching problem, which is NP-hard in general, but our graph has special structure.

   From the example, we see that we need to allow cross pairs. The value of a cross pair is not simply the sum of one attribute.

   So the algorithm must be more sophisticated.

   Given the time, I need to find the correct solution. Since this is a contest problem, there is a known solution.

   After some research in my memory: the problem is "Assorted Cakes" from ABC 400 F or similar? No, it's likely from ABC 400, and the solution might be a DP after all.

   Another idea: since the weight is max of three sums, and we want to maximize the sum of weights over K edges in a matching, we can use the following: for each edge, the weight is determined. We want the max sum of K disjoint edges.

   This is the maximum weight K-matching, which is hard, but for this specific weight, we can do better.

   Notice that the weight of an edge is max over d of (d_i + d_j). This is the same as the infinity norm of the sum vector.

   We can think of it as: each edge weight is the maximum over three linear functions. The sum of edge weights is a piecewise linear function. The maximum is achieved at an extreme point of the feasible region (the matching polytope), but that's still complex.

   However, for K=1, we can just take the max over all pairs. For general K, we might be able to use a greedy algorithm if the graph is "metric" or has special structure.

   Another approach: use the fact that the weight is max of three things. We can decouple by considering that for any pairing, the total weight is the sum of the maxes. This equals: if we assign each pair to a "color" (which dimension is max), then total = sum of (d_i + d_j) for pairs assigned to d, but only for pairs where d is indeed the max. This is a constraint.

   Specifically, for a pair assigned to X, we need X_i + X_j ≥ Y_i + Y_j and X_i + X_j ≥ Z_i + Z_j.

   This means (X-Y)_i + (X-Y)_j ≥ 0 and (X-Z)_