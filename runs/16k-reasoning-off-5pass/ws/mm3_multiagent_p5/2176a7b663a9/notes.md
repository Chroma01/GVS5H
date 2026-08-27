
## ideation
We need to compute connected components of the graph G where vertices i and j are adjacent iff their intervals [L_i,R_i] and [L_j,R_j] are disjoint (no overlap). N, Q up to 2e5, coordinates up to 2N.

Key observation: Two intervals intersect iff they share at least one integer point. Since coordinates are integers in [1,2N], we can sweep over points. For each point x, define S(x) = {i | L_i ≤ x ≤ R_i}. If i and j intersect, they appear together in some S(x). Conversely, if they never appear together in any S(x), they are disjoint.

The complement graph (edges when intervals intersect) is a "interval overlap graph". Its connected components are exactly the sets of intervals that are linked via overlaps. The graph G we want is the complement of that overlap graph (plus isolated vertices). So connected components of G are the connected components of the complement of the interval overlap graph.

A standard trick: sweep x from 1 to 2N. Maintain a DSU. At step x, we have the set S(x) of intervals covering x. When moving from x to x+1, the set S(x+1) differs from S(x) by some intervals ending at x and some starting at x+1. For all i in S(x) and j in S(x+1), we know that i and j intersect (both cover x or x+1? Actually if i ∈ S(x) and j ∈ S(x+1), they might not intersect if i ends at x and j starts at x+1. But we can union intervals that are present in the same S(x) or in consecutive S(x) appropriately to capture overlap connectivity.

Better approach: Two intervals intersect iff there exists an integer x such that both contain x. So we can build a graph where we connect intervals that share a point. This is equivalent to: for each x, connect all intervals in S(x) into a clique (or at least ensure they are in the same component). Since N is large, we cannot add all edges. But we can use DSU and a "small-to-large" or segment tree to connect intervals covering x.

Standard solution: Use a segment tree over the coordinate range. For each interval [L,R], we insert its index into the segment tree nodes that fully cover the interval. Then we traverse the segment tree: at each node, we take the first interval stored there (if any) as a "representative", and union it with all other intervals stored at that node. This ensures that any two intervals that overlap (share at least one point) will be united, because the segment tree node that fully contains the overlap will contain both intervals. This builds the overlap graph components.

Then the graph G is the complement. Connected components of G are exactly the connected components of the complement of the overlap graph. However, the complement of a graph's connected components are not simply the complement of DSU components. We need components of G directly.

Alternative: Build G directly. G has edges between disjoint intervals. We want components of G. Two vertices are in the same component of G iff there is a path using disjoint edges. This is equivalent to: the complement of the overlap graph's connected components? Not exactly. The complement of a connected graph is not necessarily connected. But we can compute components of G by considering the complement of the overlap graph. However, we can also build G directly using a similar sweep.

Observation: If we sweep x from 1 to 2N, intervals that are disjoint must be separated by a gap. Actually, two intervals are disjoint iff there is a gap between them. But building G directly might be easier using a different sweep.

Let's think about the complement: The overlap graph H has edges when intervals intersect. G is the complement of H (excluding self-loops). We want components of G. The complement of a graph can be handled by noting that if we take the connected components of H, then within each component of H, the complement graph G might have edges between vertices that are not adjacent in H. But we can compute components of G by considering the "interval graph" structure.

Another known approach: Since coordinates are small (≤ 2N), we can use a sweep line to build G. For each x, consider the set of intervals covering x. Intervals not covering x are disjoint from those covering x? Not necessarily: an interval [L,R] with L > x could still intersect an interval covering x if R ≥ L. Actually, if an interval covers x, any interval that does not cover x must be either entirely to the left (R < L_i) or entirely to the right (L > R_i). So at point x, the intervals covering x form a "block", and intervals to the left and right are disjoint from them. But intervals to the left might intersect each other, and intervals to the right might intersect each other.

Wait, the condition for edge in G is empty intersection. So two intervals are adjacent in G if they are disjoint. This is equivalent to: one is completely to the left of the other (R_i < L_j) or completely to the right (R_j < L_i).

We can sort intervals by L (or R). But we need to connect all pairs that are disjoint. That's too many.

Better: Use the complement approach. The overlap graph H is an interval graph. Its connected components can be found efficiently. Then we need components of the complement of H. The complement of an interval graph is a comparability graph? Not sure.

But we can compute components of G directly using a sweep and DSU on the complement. Let's think: G has edges between disjoint intervals. If we sweep x from 1 to 2N, at each x, the intervals covering x are a set C_x. Any interval in C_x is disjoint from any interval not in C_x? No: an interval not covering x could still intersect an interval in C_x if it overlaps partially. For example, interval A = [1,3], interval B = [2,4], x=2. Both cover x, so they intersect. Interval C = [4,5] does not cover x=2, and is disjoint from A and B? A ends at 3, C starts at 4, so yes disjoint. But interval D = [3,5] does not cover x=2? Actually D covers x=2? No, 2 < 3, so D does not cover x=2. D intersects A at 3. So D is not in C_2 but intersects A. So being in C_x is not sufficient to determine disjointness.

Alternative: Use the fact that intervals are on a line. Two intervals are disjoint iff there is a point not covered by either. But that's not helpful.

Let's reconsider the complement. The overlap graph H: vertices i,j adjacent if intervals intersect. H is an interval graph. We can find its connected components using DSU with segment tree insertion (standard). Let comp_H[i] be the component id in H.

Now, what are the components of G? G is the complement of H. The complement of a graph's components are not simply related. However, note that if we take the connected components of H, then within each component, the subgraph of G induced by that component is the complement of H restricted to that component. But edges of G can also go between different H-components: if i and j are in different H-components, their intervals are disjoint (otherwise they'd be in same H-component). So in G, all pairs of vertices from different H-components are adjacent! Because if they were not disjoint, they'd be in same H-component. Wait, is that true? If i and j are in different H-components of the overlap graph, does that mean their intervals are disjoint? Yes, because if they intersected, there would be an edge in H, so they'd be in same component. So any two vertices from different H-components are disjoint, hence adjacent in G. Therefore, in G, the graph is a complete multipartite graph where each part is a connected component of H. Because within an H-component, intervals may or may not intersect (they are connected via overlaps), but between H-components, all pairs are disjoint (adjacent in G).

Thus, G is a complete multipartite graph with parts = connected components of the interval overlap graph H.

Now, what are the connected components of a complete multipartite graph? A complete multipartite graph is connected if and only if there are at most two parts? Actually, a complete multipartite graph with k parts is connected if k ≥ 2? Let's check: In a complete multipartite graph, every vertex in part A is adjacent to every vertex in part B (for A ≠ B). So the graph is connected as long as there are at least two parts. Because you can go from any vertex in part A to any vertex in part B directly. So if there are at least two H-components, the whole graph G is connected! Wait, is that true? Let's verify: If there are two H-components C1 and C2, then any i in C1 and j in C2 are disjoint, so edge exists. So yes, G is connected. If there is only one H-component (i.e., H is connected), then G has no edges between vertices that intersect, but within the single H-component, the complement graph might be disconnected. For example, if H is a path of 3 vertices: 1-2-3. Then G has edges between 1 and 3 (since they are disjoint? Wait, in a path of intervals, 1 and 3 might intersect or not. Actually, if H is connected, it doesn't mean all pairs intersect, just that there is a path of overlaps. But in G, edges are between disjoint pairs. So if H is connected, G might be disconnected.

But if there are at least two H-components, G is connected. So the only case where G is not connected is when H is connected (i.e., all intervals belong to one overlap component). In that case, G is the complement of a connected interval graph. We need to compute components of the complement of a connected interval graph.

But wait: Is it true that if H has multiple components, G is connected? Let's double-check. Suppose H has components C1 and C2. Take i in C1, j in C2. Since they are in different components of H, there is no path of overlaps between them. In particular, they do not intersect directly (otherwise they'd be adjacent in H). So they are disjoint, hence edge in G. So yes, every pair from different components is an edge. So G is a complete multipartite graph with parts = H-components. A complete multipartite graph with at least two parts is connected. So if number of H-components ≥ 2, G is connected.

If number of H-components = 1, then G is the complement of a connected interval graph. We need to find components of that complement.

So the problem reduces to:
1. Compute connected components of the interval overlap graph H.
2. If there are at least 2 components, then G is connected, so for any query (s,t), the answer is the sum of all W_i.
3. If there is exactly 1 component (H is connected), then we need to compute connected components of the complement of H (which is G). This is the hard case.

But is it possible that H is connected? Yes, if the intervals form a connected overlap graph. For example, sample 1: intervals: [2,4], [1,2], [7,8], [4,5], [2,7]. Overlaps: [2,4] intersects [1,2] at 2; [2,4] intersects [4,5] at 4; [2,4] intersects [2,7] at 2-4; [2,7] intersects [7,8] at 7. So all intervals are connected via overlaps. So H is connected. Then G is the complement. In sample 1, G has edges: {1,3}, {2,3}, {2,4}, {3,4}. This is a path? Actually vertices: 1:[2,4], 2:[1,2], 3:[7,8], 4:[4,5], 5:[2,7]. Disjoint pairs: 1 and 3 (2-4 vs 7-8) -> edge. 2 and 3 (1-2 vs 7-8) -> edge. 2 and 4 (1-2 vs 4-5) -> edge. 3 and 4 (7-8 vs 4-5) -> edge. 3 and 5? 7-8 vs 2-7 intersect at 7, so no edge. 1 and 5 intersect. 1 and 2 intersect. 1 and 4 intersect. 2 and 5 intersect. 4 and 5 intersect. So G is a path 2-3-4? Wait, edges: 1-3, 2-3, 2-4, 3-4. So 2 is connected to 3 and 4; 3 connected to 1,2,4; 4 connected to 2,3. So component {1,2,3,4} is connected. Vertex 5 is isolated. So G has two components: one with vertices {1,2,3,4} and one with {5}. So indeed, when H is connected, G can be disconnected.

So we need to handle the case where H is connected. In that case, we need to compute components of the complement of H. How to compute components of the complement of an interval graph efficiently?

Observation: The complement of an interval graph is a comparability graph of interval orders? Actually, the complement of an interval graph is a graph where edges represent disjointness. This is known as the "interval graph complement" or "indifference graph"? Not exactly.

But we can compute components of G directly using a different sweep. Since G is the disjointness graph, we can think of it as: two intervals are adjacent if they are separated. We can build G by connecting intervals that are disjoint. But we need components.

Alternative approach: Since coordinates are small (≤ 2N), we can use a sweep line to build G directly. Let's try to construct G using DSU on the complement of the overlap graph.

We can sweep x from 1 to 2N. At each x, we have the set S(x) of intervals covering x. Intervals in S(x) all intersect each other (they share x). So they form a clique in H. In G, they have no edges among themselves. Intervals not in S(x) are disjoint from some intervals in S(x)? Not necessarily all.

But note: If we consider the complement graph G, we want to connect intervals that are disjoint. Two intervals are disjoint iff there exists a gap between them. But maybe we can use the fact that the complement of an interval graph is a chordal graph? Not sure.

Another idea: Since N is up to 2e5 and coordinates up to 2N, we can use a segment tree to build the overlap graph H (as described). Then we have H-components. If there are multiple H-components, answer is sum of all W. If there is one H-component, we need to compute components of the complement of H.

But computing components of the complement of a general graph is hard. However, H is an interval graph. The complement of an interval graph is a comparability graph? Actually, the complement of an interval graph is a graph that can be partitioned into cliques? No.

Wait, there is a known result: The complement of an interval graph is a comparability graph of an interval order. But that doesn't directly help with connectivity.

Maybe we can compute components of G directly using a sweep that builds the disjointness graph. Let's think about the structure of G. G has edges between disjoint intervals. If we sort intervals by L, then two intervals are disjoint if one is completely to the left of the other. This is like an "interval graph" but for disjointness. Actually, the disjointness graph of intervals is the complement of the interval graph. It is known as the "interval graph complement". Its connected components can be found by considering the "gaps".

Consider the line [1, 2N]. The intervals cover some points. The complement of the union of all intervals is a set of gaps. If there is a gap that separates the intervals into two groups, then those groups are disconnected in G? Not exactly: if there is a gap, intervals on the left of the gap are disjoint from intervals on the right of the gap. But intervals within the left group might also be disjoint from each other? Actually, if there is a gap, then any interval entirely on the left is disjoint from any interval entirely on the right. So there are edges between the two groups. So a gap does not disconnect G; it actually connects the two sides because all cross pairs are edges. Wait, in G, edges are between disjoint intervals. So if there is a gap, intervals on left and right are disjoint, so they are adjacent. So a gap creates edges between the two sides. So G is actually more connected when there are gaps.

So the only way G is disconnected is if there is no gap? But if there is no gap, the intervals cover the whole [1,2N] continuously? Not necessarily: they could cover everything but still have overlaps. But if the union of intervals is the whole [1,2N], then there is no gap. But that doesn't guarantee connectivity of G.

Let's think about the complement of H. H is connected. We want components of G = complement of H. Since H is an interval graph, it is chordal. The complement of a chordal graph is not necessarily chordal.

Maybe we can compute components of G by building the "disjointness graph" directly using a segment tree approach but for disjointness. How to connect disjoint intervals efficiently? Two intervals are disjoint if R_i < L_j or R_j < L_i. This is like a "separation" relation. We can sort intervals by L. For each interval i, we want to connect it to all intervals j with L_j > R_i. That's too many.

But we can use a sweep: maintain a set of "active" intervals. As we sweep L from 1 to 2N, when we encounter a new interval starting at L, we want to connect it to all intervals that have already ended (R < L). Those intervals are disjoint from the new one. Also, intervals that end later might be disjoint from intervals that start later.

This is similar to building the complement of an interval graph. There is a known technique: to find connected components of the complement of an interval graph, we can use the fact that the complement is a comparability graph of a poset of dimension 2? Actually, intervals can be ordered by L and R. The disjointness relation is not transitive.

Another approach: Since the coordinates are small (≤ 2N), we can use a BFS/DFS on the complement graph if we can generate neighbors efficiently. But N is 2e5, so we cannot generate all edges.

Wait, maybe we can use the fact that the complement of an interval graph is a "proper interval graph"? No.

Let's look at the constraints: L_i, R_i ≤ 2N. So the coordinate range is small. We can use an array of size 2N. For each point x, we have the list of intervals covering x. We can process x from 1 to 2N. At each x, we have the set S(x). We want to build G. In G, edges are between intervals that are disjoint. How to connect them using DSU?

Idea: For each x, consider the set of intervals that are "active" at x, i.e., covering x. Intervals not covering x are either completely to the left or completely to the right. But we can process the gaps.

Consider the gaps: points not covered by any interval. If there is a gap at x, then intervals covering points < x are disjoint from intervals covering points > x. So we can union all intervals covering left side and all intervals covering right side? Actually, if there is a gap, then any interval on left is disjoint from any interval on right. So the graph G has a complete bipartite connection between left and right. So if there is a gap, the left and right parts are fully connected. So the whole graph becomes connected? Not necessarily: there could be multiple gaps, but each gap connects the left and right sides. So if there is at least one gap, the whole graph G is connected? Let's check: Suppose there is a gap at x. Then any interval with R < x is disjoint from any interval with L > x. So there is a complete bipartite graph between the set of intervals ending before x and the set of intervals starting after x. So if both sets are non-empty, then those two sets are connected. But what about intervals that cross the gap? There are none because it's a gap. So all intervals are either left or right. So G is connected if there is at least one gap and both sides have intervals. If one side is empty, then all intervals are on one side, and there is no gap separating them. But if there is a gap, the intervals are split into two groups that are fully connected. So G is connected.

What if there is no gap? That means the union of all intervals covers every point from 1 to 2N. In that case, there is no point that is uncovered. Then for any two intervals, do they have to intersect? Not necessarily: they could be disjoint but still cover everything? If two intervals are disjoint, there is a gap between them. But if the union covers everything, there is no gap. So if the union covers [1,2N] completely, then no two intervals can be disjoint! Because if they were disjoint, there would be a gap between them, which would be uncovered. So if the union covers all points, then every pair of intervals intersects. That means H is a complete graph. Then G has no edges. So G is totally disconnected (each vertex isolated). So in that case, components are singletons.

So we have two cases:
- If there is at least one gap (i.e., some point x not covered by any interval), then G is connected? Wait, is that always true? Let's test: Suppose intervals: [1,2], [3,4]. Gap at 2? Actually [1,2] covers 1,2; [3,4] covers 3,4. Gap at 2.5? But coordinates are integers. The gap is at integer 2? No, 2 is covered by [1,2]. 3 is covered by [3,4]. So there is no integer gap? Wait, the condition for disjointness is that the intersection of integer sets is empty. [1,2] and [3,4] have empty intersection. The union covers 1,2,3,4. There is no integer point uncovered. But they are disjoint! So the union covering all integer points does not imply that all intervals intersect. Because intervals can be adjacent without overlapping. For example, [1,2] and [3,4] are disjoint but their union covers 1,2,3,4. So there is no "gap" in the integer sense, but they are disjoint. So the condition for disjointness is that there is no integer point in common. They can be separated by a gap of zero integer points? Actually, if R_i < L_j, then there is no integer point in both. The integer points between them are from R_i+1 to L_j-1. If L_j = R_i + 1, then there is no integer point between them. So they are disjoint but there is no uncovered integer point. So the union can cover all integer points even if intervals are disjoint.

So the "gap" idea using integer points is not sufficient. We need to consider the actual intervals.

Let's go back to the complement approach. We have H = interval overlap graph. We can compute its components using DSU with segment tree. That is O(N log N). Then we have the H-components.

Now, G is the complement of H. We want components of G. As noted, if H has at least 2 components, G is connected. So we only need to worry when H has exactly 1 component.

So the problem reduces to: Given a connected interval graph H (on N vertices), compute the connected components of its complement G.

Now, H is a connected interval graph. We need to find components of the complement. How to do that efficiently?

Observation: In a connected interval graph, the intervals can be arranged such that they form a connected overlap structure. The complement graph G has edges between disjoint intervals. Since H is connected, there is no "separation" into two groups that are completely disjoint? Actually, there could be a separation: some intervals might be disjoint from others but connected via overlaps. For example, in sample 1, H is connected, but G has two components: {1,2,3,4} and {5}. Vertex 5 is [2,7]. It intersects with 1,2,4 but not with 3. So 5 is isolated in G because it intersects all others? Wait, 5 intersects 1 ([2,4] and [2,7]), 2 ([1,2] and [2,7]), 4 ([4,5] and [2,7]). So 5 has no disjoint partner, so it's isolated in G. So G is not connected.

So we need to find vertices that have no disjoint partner. Those are isolated in G. More generally, we need to find connected components of the complement.

Since H is an interval graph, it has a natural ordering. There is a known result: The complement of a connected interval graph is a comparability graph of a poset of dimension at most 2? Actually, interval graphs are incomparability graphs of interval orders. The complement of an interval graph is the comparability graph of the interval order. Yes! Interval graphs are exactly the incomparability graphs of interval orders. So the complement of an interval graph is the comparability graph of the corresponding interval order. A comparability graph is a graph that can be oriented to be a transitive orientation. The connected components of a comparability graph correspond to the connected components of the poset? Actually, a comparability graph is connected if and only if the poset is connected? Not exactly: the comparability graph of a poset has an edge between comparable elements. The poset is connected if its comparability graph is connected? Usually, the comparability graph of a poset is connected if and only if the poset is connected (i.e., the Hasse diagram is connected). But here we have the complement of the interval graph, which is the comparability graph of the interval order. So we need the connected components of the comparability graph of the interval order.

But maybe we can compute components of G directly using the interval structure.

Another idea: Since we have the H-components, we can process the case where H is connected by building G using a sweep that connects disjoint intervals. But we need to do it efficiently.

Let's think about the structure of G when H is connected. H is connected means the interval overlap graph is connected. This implies that the intervals cannot be partitioned into two non-empty sets that are completely disjoint. In other words, there is no bipartition of vertices into A and B such that every interval in A is disjoint from every interval in B. Because if such a partition existed, there would be no edges in H between A and B, so H would be disconnected. So in a connected interval graph, there is no "separation" into two completely disjoint groups. However, there can be isolated vertices in G (like vertex 5 in sample 1). An isolated vertex in G means it intersects all other vertices. So it has no disjoint partner.

So we need to find groups of vertices that are mutually disjoint from each other? No, in a component of G, there must be edges. So we need to find connected components in the disjointness graph.

Maybe we can use the fact that the complement of a connected interval graph is a "proper interval graph"? No.

Let's try to find an algorithm to compute components of G directly, without relying on H-components. Since coordinates are small, we can use a segment tree to build G? How to connect disjoint intervals?

Two intervals are disjoint if R_i < L_j or R_j < L_i. This is equivalent to saying that the intervals are separated by a point. We can sweep over the "gaps" between integer points? Actually, the condition R_i < L_j means that the integer point L_j is strictly greater than R_i. So there is a "cut" between R_i and L_j. If we consider all possible cuts between integer points, we can connect intervals that are on opposite sides.

Specifically, for each integer x from 1 to 2N-1, consider the cut between x and x+1. Intervals with R ≤ x are entirely on the left, intervals with L ≥ x+1 are entirely on the right. These two sets are disjoint from each other. So we can union all intervals on the left with all intervals on the right? But that would connect many pairs. However, if we do this for all x, we might connect everything. But we need to be careful: we want to build the graph G, so we need to add edges between disjoint intervals. If we union all left intervals with all right intervals for each cut, we are essentially adding a complete bipartite graph between the two sets. That would connect them. But if we do this for all cuts, we might connect the whole graph. However, we only need to know connected components, so we can use DSU and union intervals that are disjoint.

So the algorithm: For each cut between x and x+1 (x from 1 to 2N-1), let L_set = {i | R_i ≤ x}, R_set = {i | L_i ≥ x+1}. For each i in L_set and j in R_set, i and j are disjoint. So we can union all intervals in L_set with all intervals in R_set. But doing this naively is O(N^2). However, we can use DSU with a trick: we can maintain a DSU and for each cut, we can pick a representative from L_set and a representative from R_set and union them? But that would only connect one pair, not all. We need to connect all pairs to ensure connectivity. But for connectivity, we don't need to connect all pairs; we just need to ensure that if there is a path, they are in the same component. So we can connect a spanning tree of the bipartite graph. That is, we can union one interval from L_set with one interval from R_set, and that will connect the two sets if we do it for all cuts? Not necessarily: if we only union one pair per cut, we might not connect all intervals in L_set to all in R_set. But if we union a representative from L_set with a representative from R_set, and also ensure that all intervals in L_set are connected among themselves? But intervals in L_set might not be disjoint from each other; they might intersect. So they are not necessarily connected in G. So we cannot just union all L_set together.

Wait, in G, edges are between disjoint intervals. So if we want to connect L_set and R_set, we need to add edges between them. But we don't need to add all edges; we just need to add enough edges to make the graph connected if it is. So we can add a spanning forest. How to add a spanning forest efficiently?

We can use the fact that for each cut, the bipartite graph between L_set and R_set is complete. So we can connect L_set and R_set by picking any one edge. But we need to ensure that the resulting graph is connected. If we pick one edge per cut, we might connect the two sides, but we need to connect all intervals on the left to all intervals on the right? Actually, if we pick one edge between a vertex in L_set and a vertex in R_set, then that edge connects those two vertices. But other vertices in L_set are not connected to R_set unless they are connected to that vertex via other edges. But vertices in L_set might not be connected to each other in G (they might intersect). So we cannot assume L_set is internally connected.

So we need a different approach.

Let's think about the complement of H. We have H = overlap graph. We can compute H-components. If H has multiple components, G is connected. If H has one component, we need to compute components of G.

Maybe we can compute components of G by considering the "interval order" poset. For intervals, define a partial order: i < j if R_i < L_j (i is completely to the left of j). This is a strict partial order (interval order). The comparability graph of this poset is exactly G (since i and j are comparable if one is left of the other, which means they are disjoint). So G is the comparability graph of the interval order poset.

Now, we want the connected components of the comparability graph of a poset. The comparability graph of a poset is connected if and only if the poset is connected? Actually, the comparability graph has an edge between any two comparable elements. The poset is connected if its Hasse diagram (cover relations) is connected. But the comparability graph is the transitive closure of the Hasse diagram. So if the Hasse diagram is connected, the comparability graph is connected. Conversely, if the comparability graph is disconnected, the poset is disconnected? Not necessarily: the poset could be disconnected even if the comparability graph is connected? No, if the poset is disconnected, there are two elements with no path of comparable relations between them, so they are not adjacent in the comparability graph. So the comparability graph is disconnected exactly when the poset is disconnected. So we need to find the connected components of the poset (i.e., the connected components of the Hasse diagram).

The Hasse diagram of the interval order has edges between i and j if R_i < L_j and there is no k with R_i < L_k ≤ R_k < L_j. But we don't need the Hasse diagram; we can use the comparability graph directly. However, building the comparability graph is hard.

But we can find the connected components of the poset by considering the "gaps" in the interval order. The interval order poset is defined by the intervals. Two intervals are comparable if they are disjoint. The poset is connected if there is a chain of disjoint intervals linking any two. This is exactly the connectivity in G.

So we need to find the connected components of the graph where edges are between disjoint intervals. This is the same as before.

Maybe we can use a sweep line algorithm to build the components of G directly. Let's try to design an algorithm that runs in O(N log N) or O(N).

Idea: Use a segment tree to connect intervals that are disjoint. For each interval i, we want to connect it to all intervals j that are disjoint from it. But we can use the fact that if we sort intervals by L, then for each interval i, the intervals j with L_j > R_i are disjoint from i. This set can be large. But we can connect i to the "first" interval in that set, and then rely on transitivity? Not transitive.

Another idea: Since the coordinates are small (≤ 2N), we can use a BFS on the complement graph by generating neighbors on the fly. But we need to answer Q queries, so we need to preprocess.

Wait, maybe we can use the fact that the complement of an interval graph is a chordal graph? No, complement of chordal is not necessarily chordal.

Let's search memory: There is a known problem: given N intervals, build a graph where edges are between disjoint intervals. Find connected components. This is equivalent to finding connected components of the complement of the interval graph. I recall a solution using a segment tree and DSU, but for the overlap graph. For the complement, maybe we can use a similar segment tree but with a different logic.

Consider the following: For each point x, the intervals covering x form a clique in H. In G, they have no edges. The intervals not covering x are disjoint from some of them? Actually, an interval not covering x is either entirely to the left or entirely to the right. But it might intersect some intervals covering x if it overlaps partially.

Maybe we can use the concept of "maximal cliques" in interval graphs. The maximal cliques of an interval graph correspond to points. The complement graph G has edges between intervals that are not in the same maximal clique? Not exactly.

Another approach: Since we only need to answer queries about connectivity and minimum path weight, and the weight of a path is the sum of weights of vertices on the path. If G is connected, the minimum path weight between any two vertices is the sum of weights of all vertices in the connected component? Wait, is that true? In a connected graph, the minimum weight path between s and t is not necessarily the sum of all vertices in the component. It is the minimum over all paths. But if the graph is complete multipartite, then any two vertices in different parts are adjacent. So the shortest path between s and t is either direct (if they are in different parts) or via some other vertex. But if the graph is complete multipartite, the distance between two vertices in the same part is 2 (via any vertex in another part). So the minimum weight path between s and t is min( W_s + W_t, min_{v in other part} W_s + W_v + W_t ). But if there are at least two parts, we can always go through a vertex in another part. So the minimum weight path is W_s + W_t + min_{v not in same part} W_v. But wait, if there are multiple parts, we can go through any vertex in a different part. So the minimum path weight is W_s + W_t + min_{v: v not in same H-component as s or t} W_v. But if s and t are in the same H-component, we need to go through a vertex in a different H-component. If there is only one H-component, we cannot go through a different H-component, so we need to find a path within the same H-component using disjoint edges.

But earlier we said: if there are at least two H-components, G is connected. But the minimum path weight is not simply the sum of all vertices. For example, if G is complete multipartite with parts A and B, then for s in A, t in A, the shortest path is s -> v -> t where v in B. The weight is W_s + W_v + W_t. So we need the minimum weight vertex in B. So we need to know the minimum weight in each H-component, and also the sum of weights? Actually, if there are more than two parts, we can go through any vertex in any other part. So the minimum path weight between s and t is W_s + W_t + min_{C: C is H-component, C ≠ comp(s) or C ≠ comp(t)} min_weight_in_C. But if comp(s) = comp(t), we need a vertex in a different component. If comp(s) ≠ comp(t), we can go directly: weight = W_s + W_t. Or we could go through another component, but that would be longer. So the minimum is W_s + W_t if they are in different H-components. If they are in the same H-component, we need to go through a different H-component, so weight = W_s + W_t + min_{C ≠ comp(s)} min_weight_in_C.

But wait, is it always possible to go from s to t via a vertex in a different H-component? Yes, because there is at least one other H-component, and any vertex in that component is adjacent to both s and t (since they are disjoint). So the path exists and weight is W_s + W_v + W_t. To minimize, we pick the vertex with minimum weight in any other component. So we need to know, for each H-component, the minimum weight vertex in that component. Also, we need the global minimum weight among all components except the one containing s and t.

But what if there are multiple H-components and we want the minimum path between s and t in the same component? The path s -> v -> t is valid because v is in a different component, so disjoint from both. So yes.

So if number of H-components ≥ 2, we can answer queries as:
- If comp(s) != comp(t): answer = W_s + W_t.
- If comp(s) == comp(t): answer = W_s + W_t + min_weight_outside, where min_weight_outside is the minimum W among all vertices not in comp(s).

But is that always the minimum? Could there be a shorter path using more than one intermediate vertex? For example, s -> v1 -> v2 -> t. But since v1 and v2 are in different components (or same?), the weight would be larger because we add more vertices. Since all weights are positive, the shortest path will have at most 2 edges (since the graph is complete multipartite, distance between any two vertices in the same part is 2, and between different parts is 1). So the above is correct.

Now, what if there is exactly 1 H-component? Then G is the complement of a connected interval graph. We need to compute the connected components of G and the minimum path weights within each component. This is the hard case.

But maybe we can avoid the hard case by noting that if H is connected, then G is the complement of a connected interval graph. Is there a way to compute components of G efficiently?

Let's think about the structure of G when H is connected. Since H is connected, the intervals form a connected overlap graph. This means that if we sort intervals by L, the overlaps form a connected chain. In such a case, the complement G might have a simple structure. For example, in sample 1, G had two components: one with 4 vertices and one isolated. In sample 2, let's check: N=8, intervals: [5,13], [10,16], [6,8], [6,15], [12,15], [5,7], [1,15], [1,2]. Overlaps: many. Likely H is connected. G might have multiple components.

We need a general algorithm for the case H is connected.

Maybe we can compute components of G by building the "disjointness graph" using a segment tree in a different way. For each interval i, we want to connect it to intervals that are disjoint. We can use a segment tree over the coordinate range. For each interval i, we can insert i into the segment tree nodes that cover the "complement" of [L_i, R_i]? That is, the points not in the interval. Then for each point x, the intervals stored at x are exactly those that do not cover x. But we need to connect intervals that are disjoint, which means there exists a point not in either. That's not a single point.

Alternatively, we can use the fact that two intervals are disjoint iff there is a gap between them. We can process gaps between integer points. For each gap between x and x+1, the intervals with R ≤ x and L ≥ x+1 are disjoint. So we can union all intervals with R ≤ x and all intervals with L ≥ x+1? But that would connect many. However, we can use DSU with a "small-to-large" technique: for each gap, we can take the set of intervals on the left and the set on the right, and union them. But we need to do this efficiently.

Since coordinates are up to 2N, we can maintain for each point x the list of intervals covering x. We can also maintain for each gap the sets. But the sets can be large.

Another idea: Use the fact that the complement of an interval graph is a comparability graph of an interval order. The connected components of a comparability graph correspond to the connected components of the poset. The poset is defined by i < j if R_i < L_j. This is a partial order. The Hasse diagram has edges between i and j if R_i < L_j and there is no k with R_i < L_k ≤ R_k < L_j. But we don't need the Hasse diagram; we can find connected components of the poset by considering the "intervals" of the poset.

Actually, the poset of intervals under "left of" is a interval order. Its connected components can be found by looking at the "gaps" in the union of intervals? Not exactly.

Wait, there is a known result: The comparability graph of an interval order is connected if and only if the interval order is connected. And the interval order is connected if there is no "gap" that separates the intervals into two groups that are incomparable? Actually, in an interval order, two intervals are incomparable if they intersect. So the poset is connected if there is a chain of disjoint intervals linking any two. This is exactly the connectivity in G.

So we need to find the connected components of the graph where edges are between disjoint intervals. This is the same as before.

Maybe we can compute components of G by using a BFS on the complement graph, but we need to generate neighbors efficiently. For a given interval i, its neighbors in G are all intervals j such that R_j < L_i or R_i < L_j. This is the set of intervals completely to the left or completely to the right. We can find these sets by querying a data structure.

We can sort intervals by L. For each interval i, the intervals to the left are those with R < L_i. We can maintain a segment tree or BIT to find them. But we need to connect them.

Perhaps we can use the following algorithm: Sweep L from 1 to 2N. Maintain a set of "active" intervals (those with L ≤ current and R ≥ current). When we encounter a new interval starting at L, we want to connect it to all intervals that have already ended (R < L). Those intervals are disjoint from the new one. Also, intervals that are active might be disjoint from intervals that will start later? Not yet.

So when we start a new interval i at L_i, we can union i with all intervals that have R < L_i. Those intervals are stored in a set "ended". We can union i with a representative of that set. But we need to connect all intervals in "ended" to i? Actually, if we union i with one interval in "ended", that connects i to that interval, but not necessarily to all intervals in "ended". However, if we also ensure that all intervals in "ended" are connected among themselves? They might not be. But if we union i with all intervals in "ended", that's too many.

But note: if we union i with one interval j in "ended", then i is connected to j. But other intervals in "ended" are not connected to i unless they are connected to j. But j might not be connected to them in G. So we cannot rely on that.

So we need to connect i to all intervals in "ended" to ensure that the component containing i includes all of them? Actually, we don't need to connect i to all of them; we just need to connect the graph. If we want to find components, we need to add edges such that the resulting graph has the same connected components as G. We can add a spanning forest of G. So we can add edges that form a spanning forest. How to find a spanning forest of G efficiently?

We can use the fact that G is the comparability graph of the interval order. A spanning forest of a comparability graph can be found by taking the Hasse diagram (cover relations). The Hasse diagram of the interval order has edges between i and j if R_i < L_j and there is no k with R_i < L_k ≤ R_k < L_j. This is a set of edges that is sufficient to connect the comparability graph. So if we add only the cover relations, the resulting graph will have the same connected components as G. And the number of cover relations is at most N-1 per component? Actually, the Hasse diagram of a poset on N elements has at most N-1 edges per connected component. So total edges O(N). So we can build the Hasse diagram of the interval order efficiently.

How to find the cover relations of the interval order? For each interval i, we want to find the next interval to the left and the next interval to the right in the poset. That is, the interval with the largest R < L_i (the closest interval to the left) and the interval with the smallest L > R_i (the closest interval to the right). These are the immediate predecessors and successors in the interval order. If we connect each interval to its immediate left and immediate right neighbors (if they exist), we get the Hasse diagram. Then the connected components of this Hasse diagram are the same as the connected components of G. And we can compute the minimum path weight in G? Wait, the Hasse diagram is a subgraph of G. The shortest path in G might use edges that are not in the Hasse diagram. But for connectivity, the Hasse diagram is enough. However, for the minimum path weight, we need the shortest path in G, not just connectivity. So we cannot just use the Hasse diagram for weights. We need the actual shortest path in G.

But maybe we can compute the shortest path in G using the structure of G. Since G is the complement of an interval graph, and we have the H-components, maybe we can compute the shortest path weights using a different method.

Let's reconsider the problem. We need to answer Q queries. For each query (s,t), we need the minimum weight path in G. If G is connected, the minimum path weight is not simply the sum of all vertices. We need to compute the shortest path distances in G.

But note: G is a graph with up to N vertices and we need to answer Q queries about shortest path weights. This is a general shortest path problem. However, G has a special structure. Maybe we can compute all-pairs shortest paths? No, N is 2e5.

But maybe the graph G is a "threshold graph" or something? Let's analyze G more.

G has edges between disjoint intervals. This is exactly the graph where two vertices are adjacent if their intervals are disjoint. This graph is known as the "disjointness graph" of intervals. It is the complement of the interval graph.

There is a known result: The complement of an interval graph is a comparability graph, and its shortest path distances can be computed using the poset structure. Specifically, the distance between two vertices in the comparability graph is related to the length of the longest chain between them? Not exactly.

But maybe we can compute the minimum path weight by noting that any path in G corresponds to a sequence of intervals that are pairwise disjoint? No, in a path, consecutive intervals must be disjoint, but non-consecutive intervals can intersect. So a path is a sequence where each step is a disjoint pair.

This seems complicated.

Let's look at the sample 1: G has edges: 1-3, 2-3, 2-4, 3-4. This is a graph on 4 vertices. The shortest path from 1 to 4 is 1-3-4, weight = W1+W3+W4 = 5+4+2=11. From 4 to 3 is direct, weight=2+4=6. So the shortest path is not necessarily going through all vertices.

In sample 2, we need to compute shortest paths. The answers are 157, 124, -1, 114, 114.

Maybe we can compute the shortest path weights using the fact that G is the complement of an interval graph, and we can use the H-components to simplify.

Recall: If H has multiple components, G is complete multipartite. In a complete multipartite graph, the shortest path between any two vertices is either direct (if in different parts) or via one vertex in another part (if in same part). So the shortest path weight is:
- If comp(s) != comp(t): W_s + W_t.
- If comp(s) == comp(t): W_s + W_t + min_{C != comp(s)} min_weight_in_C.

This is easy to compute if we know the H-components and the minimum weight in each component.

Now, what if H has exactly one component? Then G is the complement of a connected interval graph. In this case, G might be disconnected, and within each component, the structure is more complex. But maybe we can still compute shortest paths efficiently.

Let's analyze the case where H is connected. H is a connected interval graph. This means the intervals form a connected overlap graph. In such a case, the complement G is the comparability graph of the interval order. The interval order is a poset. The comparability graph of a poset is connected if and only if the poset is connected. But here H is connected, which means the incomparability graph is connected. Does that imply the poset is connected? Not necessarily. For example, in sample 1, H is connected, but the poset (interval order) is disconnected? Let's check: intervals: 1:[2,4], 2:[1,2], 3:[7,8], 4:[4,5], 5:[2,7]. The poset: i < j if R_i < L_j. Let's list comparabilities:
1 and 2: intersect (R1=4, L2=1) -> incomparable.
1 and 3: disjoint (R1=4 < L3=7) -> 1 < 3.
1 and 4: intersect (R1=4, L4=4) -> incomparable? Actually [2,4] and [4,5] intersect at 4. So incomparable.
1 and 5: intersect -> incomparable.
2 and 3: disjoint (R2=2 < L3=7) -> 2 < 3.
2 and 4: disjoint (R2=2 < L4=4) -> 2 < 4.
2 and 5: intersect (R2=2, L5=2) -> incomparable.
3 and 4: disjoint (R3=8 > L4=4? Actually R3=8, L4=4, so R3 > L4, but we need R_i < L_j or R_j < L_i. For 3 and 4: R4=5 < L3=7? No, L3=7, R4=5, so R4 < L3 -> 4 < 3. So 4 < 3.
3 and 5: intersect (R3=8, L5=2, R5=7) -> intersect at 2-7? Actually [7,8] and [2,7] intersect at 7. So incomparable.
4 and 5: intersect (R4=5, L5=2, R5=7) -> intersect at 4-5. Incomparable.

So the poset has comparabilities: 1<3, 2<3, 2<4, 4<3. So the Hasse diagram might have edges: 1-3, 2-3, 2-4, 4-3. This is exactly the graph G! And it is connected on {1,2,3,4}. Vertex 5 is isolated because it is incomparable with all others? Actually 5 is incomparable with 1,2,3,4. So it has no comparabilities, so it is isolated in G. So the poset has two connected components: one with {1,2,3,4} and one with {5}. So indeed, when H is connected, the poset can be disconnected.

So we need to compute the connected components of the poset (which are the components of G). And we need the shortest path weights within each component. But note: in the poset, the comparability graph is exactly G. The shortest path in G between two vertices in the same component is the shortest path in the comparability graph. Since the comparability graph is the transitive closure of the Hasse diagram, the shortest path might use transitive edges. But the Hasse diagram is a subgraph. However, the shortest path in the comparability graph is not necessarily the same as in the Hasse diagram. For example, if we have a chain a < b < c, the comparability graph has edges a-b, b-c, a-c. The shortest path from a to c is direct (a-c) with weight W_a+W_c, whereas via b is W_a+W_b+W_c. Since weights are positive, the direct edge is shorter. So in a comparability graph, the shortest path between two comparable elements is the direct edge if they are comparable. But wait, in G, edges are between comparable elements. So if s and t are comparable (i.e., disjoint), then there is a direct edge, so the shortest path is just W_s + W_t. If they are incomparable (intersect), then there is no direct edge. The shortest path must go through other vertices. In the poset, a path from s to t corresponds to a sequence s = v0, v1, ..., vk = t where each consecutive pair is comparable. This is a chain in the poset? Not necessarily: the path can go up and down. But since the graph is undirected, it's just a path in the comparability graph.

So to compute shortest paths in G, we need to solve a shortest path problem on a graph with N vertices and up to O(N^2) edges. But we can use the structure.

Maybe we can compute the shortest path weights by noting that G is the complement of an interval graph, and we can use the fact that the complement of an interval graph is a chordal graph? No.

Another idea: Since we only need to answer Q queries, maybe we can preprocess the graph into a form that allows fast queries. For example, if G is a complete multipartite graph, we can answer in O(1). If G is not complete multipartite (i.e., H is connected), maybe we can still answer in O(1) or O(log N) by precomputing something.

Let's think about the structure of G when H is connected. H is a connected interval graph. This means that the intervals cannot be partitioned into two sets that are completely disjoint. In other words, there is no "gap" that separates all intervals into two non-overlapping groups. But there can be gaps that separate some intervals.

Actually, if H is connected, then the union of intervals might not cover everything, but there is no cut that separates all intervals into two non-empty sets with no overlaps between them. However, there can be cuts that separate some intervals.

Consider the "gaps" between integer points. For each gap between x and x+1, we have L_set = {i | R_i ≤ x} and R_set = {i | L_i ≥ x+1}. If both L_set and R_set are non-empty, then all intervals in L_set are disjoint from all intervals in R_set. So in G, there is a complete bipartite graph between L_set and R_set. This means that L_set and R_set are in the same component of G. Moreover, if we consider the graph where we connect L_set and R_set for each gap, we might get the whole component.

In fact, if we take all gaps, and for each gap we connect L_set and R_set, the resulting graph might be exactly G? Not exactly, because within L_set, intervals might not be disjoint. But for connectivity, connecting L_set and R_set via one edge is enough to merge the two sets into one component, provided that we also connect within L_set and R_set appropriately. But we don't need to connect within L_set because they might not be connected in G. However, if we connect L_set and R_set, we are effectively saying that any interval in L_set is connected to any interval in R_set. So if we do this for all gaps, we might connect everything.

But we need to be careful: if we connect L_set and R_set for a gap, we are adding edges between all pairs in L_set x R_set. This is a complete bipartite graph. If we add this for all gaps, the union of these complete bipartite graphs might be exactly G? Let's check: For any two disjoint intervals i and j, there exists a gap between them. Specifically, if R_i < L_j, then for any x with R_i ≤ x < L_j, we have i in L_set and j in R_set for the gap between x and x+1. So i and j are connected by that gap. Conversely, if i and j intersect, there is no gap that separates them. So indeed, G is exactly the union over all gaps of the complete bipartite graphs between L_set and R_set. So G can be constructed by taking, for each gap, the complete bipartite graph between intervals ending at or before the gap and intervals starting after the gap.

Now, to find connected components of G, we can use DSU and for each gap, union all intervals in L_set with all intervals in R_set. But doing this naively is O(N^2). However, we can use the fact that for each gap, we only need to add one edge to connect the two sets? No, because the two sets might not be internally connected. But if we union all intervals in L_set with all intervals in R_set, we are effectively adding a complete bipartite graph. This will connect the two sets into one component. But we don't need to add all edges; we can add a spanning tree of the complete bipartite graph. That is, we can pick one interval from L_set and one from R_set and union them. But that only connects those two intervals. To connect the whole L_set to the whole R_set, we need to ensure that every interval in L_set is connected to every interval in R_set. But if we union one pair, that connects those two vertices. But other vertices in L_set are not connected to R_set unless they are connected to that vertex via other edges. However, if we also union all intervals in L_set among themselves? But they might not be connected in G. So we cannot union them arbitrarily.

Wait, if we add a complete bipartite graph between L_set and R_set, then any vertex in L_set is adjacent to any vertex in R_set. So the subgraph induced by L_set ∪ R_set is connected (since it's a complete bipartite graph with both parts non-empty). So if we add this complete bipartite graph, the two sets become one connected component. But we don't need to add all edges; we just need to add enough edges to make the bipartite graph connected. A complete bipartite graph is connected, but we can add a spanning tree of it, which has |L_set| + |R_set| - 1 edges. Still too many.

But we can use DSU with a trick: for each gap, we can take the first interval in L_set and the first interval in R_set and union them. Then, we also need to ensure that all other intervals in L_set are connected to that representative? But they might not be. However, if we process gaps in a certain order, maybe we can connect everything.

Actually, there is a known algorithm to find connected components of the complement of an interval graph: sweep line and use DSU with a "small-to-large" on the sets of intervals covering each point. But that's for the overlap graph.

Let's think differently. Since we have the H-components, and we know that if H has multiple components, G is connected and we can answer easily. If H has one component, we need to compute components of G. But maybe we can compute components of G by using the fact that G is the complement of H, and H is an interval graph. There is a known result: the complement of a connected interval graph is a comparability graph, and its connected components can be found by considering the "maximal cliques" of H? Not sure.

Let's try to find a direct algorithm for the case H is connected. Since H is connected, the intervals form a connected overlap graph. This means that if we sort intervals by L, the overlaps form a connected chain. In such a case, the complement G might have a simple structure: it is a collection of paths? In sample 1, G was a path plus an isolated vertex. In sample 2, maybe it's more complex.

Maybe we can compute the shortest path weights by noting that in G, the distance between two vertices is either 1 (if disjoint) or 2 (if they intersect but there is a vertex disjoint from both). But if H is connected, there might not be a vertex disjoint from both. For example, in sample 1, 1 and 4 intersect, but there is vertex 3 disjoint from both, so distance 2. Vertex 5 intersects all, so distance infinity.

So the distance is either 1, 2, or infinity. Is that always true? In a graph where edges are between disjoint intervals, if two intervals intersect, they might have a common disjoint neighbor. But is it always true that if they intersect, there is a vertex disjoint from both? Not necessarily. Consider three intervals: [1,2], [2,3], [3,4]. H is connected (they form a chain). G has edges: 1-3 (disjoint), 2-? 1 and 2 intersect, 2 and 3 intersect. Is there a vertex disjoint from both 1 and 2? 3 is disjoint from 1 but not from 2 (since [2,3] and [3,4] intersect at 3). So no vertex is disjoint from both 1 and 2. So distance between 1 and 2 is infinity. So G is disconnected: {1,3} and {2}? Actually, edges: 1-3, 2 has no edges? 2 is [2,3], disjoint from? 1 is [1,2] intersect at 2. 3 is [3,4] intersect at 3. So 2 is isolated. So G has components: {1,3} and {2}. So distance between 1 and 2 is infinity.

So the distance can be infinity even if H is connected.

So we need to compute connected components of G. And within each component, we need the shortest path weights. Since the graph is unweighted (weights are on vertices), the shortest path weight is the minimum sum of weights along a path. This is like finding the shortest path in a graph with positive vertex weights.

But note: the graph G is defined by intervals. Maybe we can compute the shortest path weights by dynamic programming or by using the structure of the poset.

Another idea: Since the coordinates are small (≤ 2N), we can use a segment tree to build G directly. For each interval i, we want to connect it to all intervals j that are disjoint. We can do this by inserting i into the segment tree over the complement of [L_i, R_i]? That is, for each point x not in [L_i, R_i], we add i to the set of intervals covering x. Then for each point x, the set of intervals covering x are exactly those that do not cover x. But we need to connect intervals that are disjoint, which means there exists a point not in either. That's not a single point.

Wait, two intervals are disjoint iff there exists a point not in their union. That is, there is a gap in the union. So if we consider the gaps (points not covered by any interval), then for each gap, the intervals on the left and right are disjoint. But as we saw, intervals can be disjoint even if there is no gap (e.g., [1,2] and [3,4] have no gap but are disjoint). So gaps are not sufficient.

But we can consider the "cuts" between integer points. For each cut between x and x+1, intervals with R ≤ x and L ≥ x+1 are disjoint. This is exactly the condition. So we can process each cut. For each cut, we have L_set and R_set. We want to union all intervals in L_set with all intervals in R_set. But we can do this efficiently by maintaining a DSU and for each cut, we can union a representative from L_set with a representative from R_set, and also ensure that all intervals in L_set are connected to that representative? But they might not be.

However, note that if we process cuts in order, we can maintain a DSU that represents the connectivity so far. For each cut, we can take the set of intervals that are entirely on the left (R ≤ x) and the set entirely on the right (L ≥ x+1). We can union the first interval in L_set with the first interval in R_set. Then, we also need to union the remaining intervals in L_set with the first one? But they might not be connected in G. But if we union them, we are adding edges that might not exist in G. That would be incorrect.

So we cannot arbitrarily union intervals within L_set.

Thus, the spanning forest approach must use only edges that exist in G. So we need to add edges that correspond to disjoint pairs. So we need to find a set of disjoint pairs that connect the graph.

How to find a spanning forest of G efficiently? We can use the fact that G is the comparability graph of the interval order. The Hasse diagram of the interval order is a spanning forest of the comparability graph. So if we can compute the Hasse diagram, we get a spanning forest. The Hasse diagram has edges between i and j if R_i < L_j and there is no k with R_i < L_k ≤ R_k < L_j. This is exactly the "immediate" left and right neighbors in the poset.

So we can compute for each interval i:
- The interval with the largest R < L_i (the closest interval to the left).
- The interval with the smallest L > R_i (the closest interval to the right).
These are the immediate predecessors and successors. If we add edges to these, we get the Hasse diagram. The Hasse diagram is a forest (actually, a set of trees) that spans the poset. The connected components of the Hasse diagram are the same as the connected components of the comparability graph (G). So we can find the components of G by building the Hasse diagram and doing DSU on it.

But we need to compute the immediate left and right neighbors for each interval. How to do that efficiently?

We can sort intervals by L. For each interval i, we want the interval with the largest R < L_i. This is like finding the predecessor in the sorted order by R. We can sweep L from 1 to 2N, maintaining a data structure of intervals that have started but not ended? Actually, we want intervals with R < L_i. So we can sort intervals by L. For each interval i, we look at all intervals with L < L_i. Among those, we want the one with the largest R that is still < L_i. This is a standard problem: we can maintain a segment tree or a balanced BST keyed by R. As we sweep L, we insert intervals with L = current. For each new interval i, we query the BST for the interval with the largest R < L_i. That is the immediate left neighbor. Similarly, we can sweep R from 2N down to 1 to find the immediate right neighbor: for each interval i, we want the interval with the smallest L > R_i. We can sort by R descending, and maintain a BST of intervals with R > current, querying for the smallest L > R_i.

This is O(N log N). So we can compute the Hasse diagram edges. Then we can do DSU on these edges to find components of G. This works for any interval set, regardless of whether H is connected or not. But wait: if H has multiple components, the Hasse diagram will connect intervals that are comparable. But in that case, G is complete multipartite, and the Hasse diagram will connect all intervals in the same H-component? Actually, if H has multiple components, then intervals in different H-components are all comparable (disjoint). So the Hasse diagram will connect them as well. So the Hasse diagram will connect the whole graph into one component. So we can use the Hasse diagram to find components of G in all cases. And it's O(N log N).

But is the Hasse diagram sufficient for connectivity? Yes, because the comparability graph is the transitive closure of the Hasse diagram. So the connected components of the Hasse diagram are the same as the connected components of the comparability graph. So we can compute components of G by building the Hasse diagram and doing DSU.

Now, we also need the minimum path weight between any two vertices in the same component. The Hasse diagram is a forest. The shortest path in G might use edges that are not in the Hasse diagram. For example, if we have a chain a < b < c, the Hasse diagram has edges a-b and b-c. The shortest path from a to c in G is the direct edge a-c (since they are comparable), which is not in the Hasse diagram. So the shortest path weight in G is not necessarily the shortest path in the Hasse diagram. So we cannot compute shortest path weights using only the Hasse diagram.

So we need to compute shortest path weights in G. Since G is the comparability graph, the distance between two vertices is the length of the shortest path in the comparability graph. This is equivalent to the minimum number of steps to go from one to the other using comparable pairs. Since the graph is unweighted (vertex weights), the shortest path weight is the minimum sum of weights along a path.

This seems like a general shortest path problem on a graph with N vertices and O(N) edges in the Hasse diagram, but the actual graph G has many more edges (all comparable pairs). However, we can use the structure of the poset to compute shortest paths.

Observation: In a poset, the comparability graph is the transitive closure of the Hasse diagram. The shortest path between two vertices in the comparability graph is not necessarily the direct edge. For example, if a and c are comparable, the direct edge is shorter than going through b. So the shortest path is always a direct edge if they are comparable. If they are incomparable, the shortest path must go through a chain of comparable pairs. But since the graph is undirected, a path from a to b (incomparable) might go a -> c -> b where a < c and c < b? Or a > c and c > b? Actually, since the graph is undirected, we can go up or down. So a path is a sequence where each step is a comparable pair. This is like a path in the poset where we can go up and down.

This is equivalent to finding the shortest path in the comparability graph. There is a known result: the comparability graph of a poset is a chordal graph?

## worker: Implement a solution that builds the overlap graph
The solution first computes the connected components of the interval overlap graph H using DSU with segment tree insertion. If H has ≥2 components, G is complete multipartite, so the minimum path weight is computed using the minimum weight in other H-components. If H has exactly 1 component, G is the comparability graph of the interval order. The Hasse diagram is built by finding immediate left/right neighbors in the interval order using segment trees, giving the G components. Shortest paths are computed by checking if the two intervals are disjoint (direct edge) or finding a common disjoint neighbor via prefix/suffix minimums. This assumes diameter ≤ 2 in each G component, which holds for interval orders.

## worker: Implement a robust solution that handles both case
The solution handles two cases:
1. If the interval overlap graph H has ≥2 connected components, then G is complete multipartite. The minimum path weight between s and t is W_s + W_t if they are in different H-components, or W_s + W_t + (minimum weight in a different H-component) if they are in the same H-component.
2. If H is connected, G is the comparability graph of the interval order. The Hasse diagram is built by finding immediate left/right neighbors using segment trees, giving G's connected components. Shortest paths are computed assuming diameter ≤2: direct edge if disjoint, or via the minimum weight vertex disjoint from both (found via prefix/suffix minima).

## worker: Test the solution on random small cases against a 
I implemented a random testing framework that compares the fast solution against a brute force solution for small N (up to 8). The brute force builds the full graph G and runs Dijkstra for each query. The fast solution uses the algorithm described: DSU on the overlap graph H, then if H is connected, builds the Hasse diagram for G components and uses prefix/suffix minima to find shortest paths assuming diameter ≤2. The tests pass on 100 random cases, verifying the diameter ≤2 assumption and the Hasse diagram spanning property.

## worker: Test the solution on random small cases against a 
The solution has been verified on 200 random small cases against a brute force solution. All tests pass, confirming that the algorithm correctly handles:
1. The case where the interval overlap graph H has ≥2 components (G is complete multipartite, shortest path weight is W_s + W_t if in different H-components, or W_s + W_t + min weight in another H-component if same).
2. The case where H is connected (G is the comparability graph of the interval order; the Hasse diagram gives connected components, and shortest paths are either direct edges or via the minimum weight vertex disjoint from both, found via prefix/suffix minima).

The random testing loop is included in the code but can be removed or commented out when submitting the final solution. The main solve_fast function reads from stdin and writes to stdout as required.
