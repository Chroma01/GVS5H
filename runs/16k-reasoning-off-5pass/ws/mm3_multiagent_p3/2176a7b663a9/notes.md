
## ideation
The core difficulty is answering connectivity and minimum-weight path queries on a graph where edges exist between intervals iff they are disjoint. N, Q up to 2e5, and interval endpoints are bounded by 2N. The graph is the complement of an interval graph (co-interval graph). The minimum path weight is the sum of vertex weights (all positive). Since R_i <= 2N, the coordinate range is small, enabling sweep-line techniques. The "right-neighbor" graph (linking each interval to the nearest disjoint interval to its right) preserves connectivity, but the minimum weight path is not simply the direct edge because intermediate vertices with small weights can reduce the sum. The challenge is to compute minimum path weights efficiently for many queries.

Key observations:
- The graph G is the comparability graph of the interval order "left of" (R_i < L_j).
- Connectivity in G is equivalent to connectivity in the Hasse diagram of this poset.
- A sweep line can maintain active intervals and connect each new interval to the nearest disjoint interval to its left and right, building a forest-like structure.
- For minimum weight path, since weights are positive, the path is simple and we need to find the path minimizing the sum of weights. This resembles a shortest path in a graph with vertex weights, but the special structure (interval disjointness) might allow reducing to a problem on a tree or using DSU with weight information.
- The condition R_i <= 2N suggests coordinate compression and using a segment tree or array of size 2N to find nearest disjoint intervals quickly.

## worker: Determine the exact structure of the graph G (comp
The graph G is the complement of an interval graph (co-interval graph). The key insight is that for any two connected vertices s and t, there exists a path of length at most 2. This is because if s and t are not directly connected (i.e., their intervals overlap), they must be part of a structure where either there is an interval completely to the left of both or completely to the right of both, which acts as a common neighbor. The minimum weight path is therefore either the direct edge (if disjoint) or a length-2 path through the best possible intermediate vertex k. The condition for existence of such a k is that there is some interval with right endpoint < min(L_s, L_t) or left endpoint > max(R_s, R_t). By precomputing prefix and suffix minimums of weights over the coordinate range (1..2N), we can answer each query in O(1) after O(N) preprocessing.
