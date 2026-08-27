Model the graph complement: two vertices i and j are connected iff their intervals [L_i, R_i] and [L_j, R_j] are disjoint. We need shortest path by vertex-weight sum (i.e., minimizing sum of W along path, where each vertex cost is counted once). This is equivalent to finding the minimum weight path in the "interval graph complement" which is an interval-overlap graph.

Key observation: If intervals i and j overlap, they are *not* directly connected. They are only connected through vertices whose intervals are disjoint from both. But we can think differently: The graph is exactly the complement of an interval graph (intersection graph). For interval graphs, the complement's connected components correspond to intervals that can be "chained" by disjoint overlaps. In fact, a known characterization: vertices i and j are in the same connected component of the complement graph if and only if there is no interval that "covers" both in a way that separates them. More precisely, for intervals on a line, the complement graph's components are determined by: i and j are in the same component iff there exists no point covered by all intervals of some "separator set"... Actually let me think again.

Alternative approach: For each point p on the line, consider the set of intervals that *do not* cover p. These intervals can all be directly connected to each other (they are pairwise disjoint only if they don't overlap). Wait no: intervals that don't cover p might still overlap each other.

Let me think more carefully. Two intervals are connected if they are disjoint. So the graph's edges are pairs of non-overlapping intervals. This is the *interval graph complement*, also known as the *co-interval graph*.

A known fact: the co-interval graph's connected components can be characterized. Two intervals are in the same component iff their union is "not properly covered" by another interval... Hmm.

Actually, simpler characterization: Consider the interval graph H where edges = overlapping pairs. The complement graph G = complement of H. Connected components of G: two vertices are in the same component of G iff there's a path of non-overlapping intervals between them.

Claim: vertices i and j are in the same component of G iff there is no interval that "separates" them, meaning an interval [L_k, R_k] such that L_k < L_i and R_k < L_j (or symmetrically), i.e., an interval whose right endpoint is before L_j and whose left endpoint is before... hmm.

Let me think differently. The complement of an interval graph - the connected components. Here's a known result: sort intervals by left endpoint. Two consecutive intervals in this sort that overlap form a "clique" in interval graph, hence non-edges in G. The components of G correspond to "gaps" in the interval structure.

Actually here's a cleaner characterization: Consider the line [1, 2N]. Each interval [L_i, R_i] is a subset. The intervals partition (with overlaps) the line. Two intervals are "linked" in G if they don't overlap. The components of G are formed by intervals that can be connected via non-overlapping pairs.

A useful perspective: Build the interval graph (overlap = edge). Its connected components are formed by intervals that overlap transitively. The complement's components: think about it as a graph where you connect non-overlapping intervals. This is related to "interval catch graph" or "co-interval graph".

Let me think about a direct algorithm. We need shortest path in co-interval graph. The number of vertices is up to 2*10^5, edges could be huge, so we need to be clever.

Observation: The path weight sums vertex weights. This is the same as: for path s = v_0, v_1, ..., v_k = t, weight = sum of W_{v_i}. This is equivalent to Dijkstra where each vertex has cost W_v and we want shortest path from s to t (visiting vertices, each contributing its W once). This is like Dijkstra on a graph with non-negative edge weights 0, but vertex costs.

Standard trick: Transform to edge-weighted graph. Replace each vertex v with two nodes v_in and v_out, edge v_in -> v_out with weight W_v, and for each graph edge (u,v), add edges u_out -> v_in and v_out -> u_in with weight 0. Then shortest path from s_out to t_out gives the answer. This works because the path visits each "vertex" exactly once in the transformed graph (well, the shortest path will naturally use each v_in -> v_out once per visit).

So we have an edge-weighted graph with up to 2*10^5 vertices and potentially many edges. We need to compute shortest path between many pairs (s, t) - Q up to 2*10^5. So we need an efficient approach.

Now, the structure: original graph G (co-interval) has a special structure. Maybe we can decompose it.

Connected components of G: Let's find them. Then within a component, what's the shortest path structure?

Let me think about a simpler related problem: the "interval graph" itself has a known structure - its maximal cliques correspond to points on the line. The complement graph is a "co-interval graph" which is a special kind of perfect graph.

Hmm, let me think about a different angle. Sort intervals by L. Consider the sweep line. As we sweep, we maintain active intervals. When two intervals become active together, they overlap (no edge in G). When an interval ends, intervals that don't overlap with it are those that ended before or start after it.

Key insight: The "non-overlap" graph (which is G) is actually related to the structure of intervals. Let me think about it as: two intervals are non-adjacent (i.e., edge in interval graph) iff they share a point. So G is the complement.

For shortest path in complement of interval graph: I recall a problem similar to this (from AtCoder or similar). The trick is:

Claim: In the co-interval graph, the shortest path (by vertex weight) between s and t, if it exists, has a specific structure. Actually, let's think about it.

Alternative approach: For each pair of points (a, b) on the line, consider the "best chain" of intervals from some interval containing a to some interval containing b, with non-overlapping constraints. This is complex.

Let me think about components more carefully. 

Definition: An interval [L, R] "covers" point p if L ≤ p ≤ R. Define the "coverage" at each point: the set of intervals covering that point. This is a clique in the interval graph.

The complement graph G: vertices are intervals. Edges connect non-overlapping intervals. 

Consider two intervals I and J. They are connected in G iff there's a sequence of intervals I = I_0, I_1, ..., I_k = J with each consecutive pair disjoint. Equivalently, I and J are NOT connected in G iff every interval I_0, ..., I_k = J has some I_a, I_{a+1} that overlap. In the interval graph, this means... hmm.

Let's think about the connected components of G. 

Consider a "covering" point p. All intervals covering p form a clique in interval graph (no edges between them in G). For any interval I covering p, the only edges from I in G go to intervals not covering p.

Claim: Two intervals I and J are in different components of G iff there exists a "barrier" of intervals that all pairwise overlap, separating I and J.

Specifically, I and J are in the same component of G iff for every "chain of overlaps" that separates them, there's an escape. 

Actually, I recall now: the connected components of the complement of an interval graph correspond to the "intervals of the line not covered by a single blocking set". More precisely, consider the set of "blocking" intervals - intervals whose removal disconnects... 

Let me try a different approach. Let me think about when two intervals I = [L_I, R_I] and J = [L_J, R_J] are in the same component of G.

Sort all intervals by L (and by R as tiebreak). I claim:

Two intervals I and J are in the same component of G iff there's no point p on the line such that... hmm.

Let me try small cases. Suppose intervals are [1,3], [2,4], [3,5]. 
- [1,3] and [2,4] overlap (share point 2,3). No edge in G.
- [1,3] and [3,5] overlap at point 3. No edge in G.
- [2,4] and [3,5] overlap at point 3,4. No edge in G.
So G has no edges. Three components.

Now add interval [5,7]:
- [1,3] and [5,7] don't overlap. Edge in G.
- [2,4] and [5,7] don't overlap. Edge in G.
- [3,5] and [5,7] overlap at point 5. No edge in G.
- [3,5] and [1,3] overlap. No edge.
- [3,5] and [2,4] overlap. No edge.

So G edges: {[1,3]-[5,7], [2,4]-[5,7]}. Components: {[1,3], [2,4], [5,7]} all connected, and {[3,5]} separate. So two components.

Now add interval [4,6]:
- [1,3] and [4,6] don't overlap. Edge.
- [2,4] and [4,6] overlap at 4. No edge.
- [3,5] and [4,6] overlap. No edge.
- [5,7] and [4,6] overlap. No edge.
G edges: {[1,3]-[5,7], [2,4]-[5,7], [1,3]-[4,6]}. So all four {[1,3],[2,4],[3,5],[4,6],[5,7]} are connected. Wait:
- [2,4] connected to [5,7].
- [1,3] connected to [5,7] and [4,6].
- [3,5] not directly connected to anything. But [2,4] is connected to [5,7], and [5,7] to [1,3], and [1,3] to [4,6]. [3,5] needs a path: [3,5] needs to connect to something. None of its pairs are non-overlapping. So [3,5] is still isolated!

OK so [3,5] is a separate component because every other interval overlaps with it.

In general, an interval is isolated in G iff it overlaps with every other interval. An interval [L, R] overlaps with another interval [L', R'] iff not (R < L' or R' < L), i.e., R ≥ L' and R' ≥ L. So [L, R] overlaps with [L', R'] iff L' ≤ R and R' ≥ L, i.e., [L', R'] ∩ [L, R] ≠ ∅.

For [L, R] to overlap with all other intervals, we need every other [L', R'] to satisfy L' ≤ R and R' ≥ L. This means all L' ≤ R (so max of all L' ≤ R) and all R' ≥ L (so min of all R' ≥ L). Equivalently: max L' ≤ R and min R' ≥ L, which means [L, R] contains the "intersection" of all intervals... well, the "common point" of all intervals, which is [max L', min R']. So this holds iff [L, R] contains all common points, i.e., L ≤ max L' and R ≥ min R'.

Hmm, so an interval is "universal" (overlaps with all others) iff L ≤ max_{all} L_j and R ≥ min_{all} R_j, i.e., it covers the "core" intersection. Hmm, but for an interval to be isolated, it must overlap with every OTHER interval, not itself. So L ≤ max_{j≠i} L_j and R ≥ min_{j≠i} R_j. If there's only one interval, it's trivially isolated.

This is getting complex. Let me think differently.

**Components of co-interval graph:** A known result is that co-interval graph's components correspond to "intervals that can be reached via gaps". 

Here's a cleaner formulation: Sort intervals by L. Process them and at each step, the "current component" is determined by the max R seen so far. An interval I starts a new component if its L > current_max_R (i.e., it doesn't overlap with any interval in the current group... wait that's for interval graph components).

Let me re-examine. For the interval graph (overlap = edge), connected components are determined by: sort by L, scan, when L > current_max_R, start a new component. Two intervals in the same "block" overlap transitively.

For the complement graph, components are different. Let me think again with the example.

Example: [1,3], [2,4], [3,5], [4,6], [5,7]. G has edges: non-overlapping pairs. Components:
- [3,5] is isolated (overlaps with all others).
- [1,3], [2,4], [4,6], [5,7] are all connected: [1,3]-[4,6], [1,3]-[5,7], [2,4]-[5,7].

Now if I add [6,8]: overlaps with [5,7] (at 6,7) and [4,6] (at 6). So no new connections to those. [6,8] vs [1,3]: no overlap, edge. [6,8] vs [2,4]: no overlap, edge. [6,8] vs [3,5]: no overlap, edge. So [6,8] is connected to everything except those that overlap, and overlaps with [4,6] and [5,7]. Hmm so [6,8] connects to [1,3], [2,4], [3,5] (the others). 

Now all intervals are in one component! Because [3,5] is connected via [6,8] (or [1,3] via [6,8], etc).

So the components can merge when we add an interval that bridges them.

Hmm, this is tricky. Let me think about it more carefully.

**Alternative approach: directly solve shortest path**

Given the structure, maybe we can solve each query by some clever means.

Let's think about it as: shortest path in G = complement of interval graph. The graph G is the "interval catch" graph or "co-interval" graph.

I recall that in co-interval graphs, shortest path problems can be solved by considering the "interval tree" or "segment tree" structure. Specifically:

The non-overlapping pairs can be characterized: for each point on the line, intervals not covering that point are "to the left" or "to the right" and can be non-overlapping.

Here's an idea using a segment tree / sweep line:

For each pair of "non-overlapping" intervals, we'd have an edge. But there can be O(N^2) such pairs. We can't enumerate.

Alternative: think of the problem as: the path from s to t, if exists, has some structure. What does the shortest path look like?

In the example, path from 1 to 4: [2,4] -> [7,8] -> [4,5]. Weights 1+4+2=7? Wait, sample 1: W_1=5, W_2=1, W_3=4, W_4=2, W_5=2. Intervals: [2,4], [1,2], [7,8], [4,5], [2,7]. G has edges (non-overlapping pairs):
- 1: [2,4]. 2: [1,2] - share point 2. Overlap. No edge.
- 1: [2,4]. 3: [7,8]. No overlap. Edge {1,3}.
- 1: [2,4]. 4: [4,5]. Share point 4. Overlap. No edge.
- 1: [2,4]. 5: [2,7]. Overlap. No edge.
- 2: [1,2]. 3: [7,8]. No overlap. Edge {2,3}.
- 2: [1,2]. 4: [4,5]. No overlap. Edge {2,4}.
- 2: [1,2]. 5: [2,7]. Share point 2. No edge.
- 3: [7,8]. 4: [4,5]. No overlap. Edge {3,4}.
- 3: [7,8]. 5: [2,7]. No overlap. Edge {3,5}.
- 4: [4,5]. 5: [2,7]. Overlap. No edge.

So G edges: {1,3}, {2,3}, {2,4}, {3,4}, {3,5}. Sample says 4 edges: {1,3}, {2,3}, {2,4}, {3,4}. I missed {3,5}. OK.

Query 1: 1 to 4. Path 1->3->4. Weight 5+4+2=11. ✓
Query 2: 4 to 3. Weight 2+4=6. ✓
Query 3: 5 to 2. 5 only connects to 3. 2 connects to 3, 4. So 5 -> 3 -> 2, weight 2+4+1=7. But sample says -1!?

Wait let me recheck. 5's interval is [2,7]. 3's interval is [7,8]. They share point 7. So they overlap. No edge!

Let me recheck. 2's interval is [1,2], 3's is [7,8]. No overlap. Edge {2,3}. Yes.
5's interval is [2,7], 3's is [7,8]. Share 7. Overlap. No edge.

OK so 5 only connects to: let me recompute.
- 5: [2,7]. 1: [2,4] overlap. 2: [1,2] overlap at 2. 3: [7,8] overlap at 7. 4: [4,5] overlap. So 5 has no edges! Isolated.

So G components: {5} alone, and {1,2,3,4} connected. Yes that matches sample's edge list (which has 4 edges among 1,2,3,4).

Good. So my approach to find components: 5 is isolated because [2,7] overlaps with all of [2,4], [1,2], [7,8], [4,5].

**Component identification:**

Observation: An interval I is "isolated" in G (i.e., its own component of size 1) iff it overlaps with all other intervals. That is, for all j ≠ i, [L_j, R_j] ∩ [L_i, R_i] ≠ ∅.

More generally, the components of the co-interval graph have a structure related to "barrier intervals". 

Let me think: a set S of intervals forms a "barrier" separating A and B if every interval in A overlaps with every interval in B. Then A and B are in different components.

Specifically: I and J are in different components of G iff there's a sequence of intervals (or a single interval) that "blocks" all paths. By Menger's theorem or direct argument, this means there's a clique in the interval graph whose removal separates I from J in G. But since interval graph is chordal, cliques correspond to "points" (sets of intervals covering a point).

Claim: I and J are in the same component of G iff for every "point clique" (set of intervals all covering some point p), it's not the case that this clique separates I from J in G. Hmm.

OK let me think differently. Here's a more constructive approach:

**Component Algorithm:**

Sort intervals by L. Scan and maintain current component and "barrier".

Alternative: Define equivalence: i ~ j if they're in the same component. 

I think the components of the co-interval graph can be found as follows:

Consider the "interval graph" H (edges = overlap). It has components C_1, C_2, ... (these are "overlap components", where two intervals are in the same C_k iff they overlap transitively). The complement G has different components.

Hmm, let me think about small cases.

Actually, here's a clean way to think about it: 

In G (complement), I and J are connected iff there's a path of non-overlapping intervals. Equivalently, in the interval graph H, we can find I and J such that we can "hop" through non-overlapping intervals.

Alternative formulation: Define a graph where two intervals are connected iff they don't overlap. This is the "disjointness graph" of intervals.

For disjointness graph of intervals on a line, the connected components can be found by considering "maximal separators".

Here's a thought: A set of intervals B is a separator in G (i.e., removing B disconnects G) iff B is a "clique" in H (i.e., all intervals in B pairwise overlap, which means they all share a common point). So separators in G correspond to "point cliques" in H.

Two vertices I, J are in the same component of G iff no point-clique of H separates them in G. I.e., for every point p, there's an interval not covering p that connects I to J... not quite.

Actually, I think the cleanest characterization is:

**Claim:** I and J are in the same component of the co-interval graph G iff the union of intervals on the path from I to J (in the sweep) doesn't form a "block".

Hmm, let me try yet another approach. Let me think about the "interval graph complement" from the perspective of the line.

For each point p, let A_p = set of intervals not covering p. These are intervals entirely to the left of p (R < p) or entirely to the right of p (L > p). Two intervals in A_p are disjoint iff one is to the left of the other (so they don't overlap) OR they're on the same side but don't overlap. Hmm, this isn't quite leading anywhere directly.

Let me just think computationally. Here's an idea:

**Idea:** Build the "interval graph" (overlap = edge) and find its connected components. Then the co-interval graph's components are different, but related.

Actually wait, I realize the structure is cleaner than I thought. Let me reconsider.

Observation: The co-interval graph G is equivalent to the following: define a graph on intervals where I and J are connected iff [L_I, R_I] ∩ [L_J, R_J] = ∅. The connected components of G are:

I'll think of it as: two intervals I, J are in different components iff there's a "chain of overlaps" that blocks all paths. By Helly's property and the structure of interval graphs, a chain of overlaps that blocks I and J corresponds to a set of intervals all pairwise overlapping (a clique in H) that "separates" I and J on the line.

Specifically: I and J are in different components of G iff there exists a point p such that for every interval K in the "path", K covers p, OR there's a set of intervals covering p that acts as a barrier.

Hmm, let me just think about it as: a point p "blocks" two intervals I and J if every interval containing p creates a barrier. Wait, if an interval K covers p, then K overlaps with any other interval covering p, but K might not overlap with I or J (if I, J don't cover p).

I think the right characterization is:

**Claim:** I and J are in the same component of G iff there's no "interval barrier" between them. An interval barrier is a single interval [L, R] such that I is to the "left" of [L,R] and J is to the "right" (or vice versa) in a strong sense, and similarly for all intermediate intervals... hmm.

Let me try once more. I'll think of it as:

I and J are in different components of G iff for every sequence I = I_0, I_1, ..., I_k = J in the co-interval graph sense, some I_a, I_{a+1} overlap. Equivalently, I and J are in the same component iff there's a sequence of non-overlapping pairs from I to J.

Hmm, let me just try to directly solve the problem without fully characterizing components.

**Direct approach for shortest path:**

For each query (s, t), I need shortest weighted path in G. G might be large.

Dijkstra per query is too slow. We need to preprocess.

Idea: Precompute all-pairs shortest paths? Too much.

Alternative: For each pair of points on the line, compute the best "intermediate" interval.

Wait, here's an idea. In the co-interval graph, the shortest path from s to t (if exists) might have a nice structure. Let me think.

Claim: In the co-interval graph, a shortest path from s to t can be found by going through intervals that "bridge" gaps.

Hmm, let me think about the problem as a graph problem on intervals. 

Define a graph H' on the intervals where I, J are connected iff they don't overlap. We want shortest weighted path in H'.

Key insight: Two intervals don't overlap iff one is entirely to the left of the other. So define a "left of" relation: I < J iff R_I < L_J. Then I and J are non-overlapping iff I < J or J < I.

So G is an "interval order" graph. Interval orders are well-studied.

The shortest path in this graph: from s, we can go to any t' with [L_t', R_t'] < [L_s, R_s] (i.e., R_t' < L_s) or [L_s, R_s] < [L_t', R_t'] (i.e., R_s < L_t'). Then from t', similarly.

So G = "interval order graph". 

A path from s to t in G: s = v_0, v_1, ..., v_k = t, where consecutive intervals don't overlap. The path is valid iff for each i, [L_{v_i}, R_{v_i}] and [L_{v_{i+1}}, R_{v_{i+1}}] are disjoint.

This means: the path goes through a sequence of intervals, each consecutive pair disjoint. The path could "alternate" directions or stay in one direction.

Observation: If s < t (i.e., R_s < L_t), then s and t are directly connected. Otherwise, we need to find a path.

Hmm, here's a cleaner idea:

**Reformulation as a different graph problem:**

For each point p on the line, intervals entirely to the left of p form a "left group" and intervals entirely to the right form a "right group". Intervals in the left group can be paired with intervals in the right group (as long as they don't overlap within their group, but actually any left interval is disjoint from any right interval of p).

Wait, this isn't quite right because two intervals both to the left of p can overlap.

Hmm.

Let me think about it differently. Here's an approach:

**Approach: Implicit graph via segment tree**

We want to compute shortest paths in G. G is dense potentially. But maybe we can express it as a "virtual" graph using a segment tree or similar.

Idea: Build a segment tree over [1, 2N]. Each node represents a range. The idea is: for a path from s to t, we can "decompose" the path through intervals that cover certain sub-ranges.

Hmm, let me think about a different reformulation.

**Alternative idea: Reduce to a different graph.**

Consider the "interval graph" H (overlap = edge). The complement of an interval graph is a co-interval graph. Co-interval graphs are perfect and have structure.

For co-interval graphs, the shortest path can potentially be computed efficiently using the structure.

Hmm, let me think about this. I'll consider a different approach.

**Approach via "BFS from each vertex" using data structures:**

For each vertex v, BFS/Dijkstra in G is hard because of dense edges. But we can use the structure.

From vertex v with interval [L_v, R_v], the neighbors in G are: all u with R_u < L_v or R_v < L_u. These are intervals entirely to the left or entirely to the right of v.

So from v, we can go to "all intervals in [1, L_v - 1]" that are "rightmost-extending" to the left, and "all intervals in [R_v + 1, 2N]" that are "leftmost-starting" to the right. But the edges aren't to all such intervals, only to those that are pairwise... wait no. The edges from v in G are to all u with R_u < L_v (entirely to the left) or R_v < L_u (entirely to the right). So the "neighborhood" of v is the set of intervals entirely to the left of L_v, union set entirely to the right of R_v.

So G's edges from v are: v -- u for all u with R_u < L_v, and v -- u for all u with L_u > R_v. So the degree of v can be O(N).

For Dijkstra, we want to "relax" neighbors. If we use a data structure to maintain "best v-reachable cost" for all u in a range, we can be efficient.

But Dijkstra from each source is still O(N * cost-per-step). With Q up to 2*10^5, we need faster.

**Hmm, let me think about the structure of shortest paths.**

Claim: The shortest path from s to t in G has at most O(log N) "interesting" vertices (or some small number). Wait, that's not quite right either.

Let me think about sample 1. Query 1: 1 to 4. Path 1 -> 3 -> 4. [2,4] -> [7,8] -> [4,5]. The intervals are [2,4], [7,8], [4,5]. They form a "chain": [2,4] < [7,8] (since 4 < 7) and [7,8] > [4,5] (since 5 < 7). So the chain goes left, then right, then left, then... it can alternate.

Hmm, this is the structure of interval orders, which are partially ordered sets. A "path" in the co-interval graph corresponds to a sequence where consecutive elements are comparable in the interval order. 

Interval orders are 2+2-free partial orders, and they're related to semiorders.

For the shortest path problem: I think the key insight is that the shortest path can be found by considering a "bipartite-like" structure or via the interval's relationship to specific points.

**Another idea: Use a "blocker" or "barrier" approach.**

For each query (s, t), consider the "blockers" - intervals that separate s from t. The shortest path must go "around" these blockers.

Hmm, let me think about this problem from a different angle: maybe think of the line as a number line and the intervals as "obstacles" on a graph. 

**Wait, here's a potentially key insight:**

The shortest path in the co-interval graph from s to t, if it exists, can be computed as the minimum over all "valid" sequences. A "valid" sequence is a sequence of non-overlapping intervals from s to t. But the shortest path minimizes sum of weights.

In an unweighted (or vertex-weighted) graph with this structure, maybe the shortest path can be computed using something like:

For each pair of "cut points" (a, b) on the line with a < b, the shortest path from any interval I with R_I < a to any interval J with L_J > b that uses the "bridge" from left of a to right of b can be computed.

Hmm wait. Here's an idea.

**Key idea: think of shortest path as composed of "left segments" and "right segments".**

For two intervals I and J, a path from I to J in G can be thought of as: starting from I, go to some interval to the "left" (or right), and so on, until reaching J.

The shortest path from I to J might be:
- Direct edge (if non-overlapping).
- Through some intermediate interval K.

The optimal K is one that minimizes (path from I to K) + W_K + (path from K to J).

This is recursive. To find shortest path from I to J, we want to find the best "split point".

**Idea: The shortest path is determined by a "best bridge"**

For each pair (a, b) of "separator" points, consider the best path that "crosses" from left of a to right of b. 

Hmm, let me think about it as follows:

Consider a path from s to t. The intervals visited form a sequence. Between s and t, the path must "go around" any interval that overlaps with all of them... no, that's not quite right.

Let me think about a specific decomposition.

**Reformulation via "gaps":**

For two intervals I and J, define a "path" as a sequence of intervals I = I_0, I_1, ..., I_k = J with each consecutive pair disjoint. Each I_a has weight W_{I_a}. We want to minimize sum.

Alternative: think of the intervals as nodes, and we want the shortest path in a graph where the "edges" implicitly connect non-overlapping pairs.

**Let me try to think about this as a graph where edges are implicit:**

For each interval I, define L(I), R(I). Two intervals I, J are adjacent iff R(I) < L(J) or R(J) < L(I).

In such a graph, we want shortest weighted path. Here's a clever trick:

For each point p on the line, consider the "cut" at p. Intervals are partitioned into: "left" (R < p), "covering" (L ≤ p ≤ R), "right" (L > p). Within each group, there are no edges (well, within "covering" there's no edge because all covering intervals pairwise overlap, so they're an independent set; but in G, wait, "covering" intervals pairwise overlap, so they have NO edge in G - they form an independent set in G). 

Wait, "covering" intervals all pairwise overlap (share point p), so they have NO edges in G. So they form an independent set in G, meaning no path can directly go through two "covering" intervals of p.

But "left" and "right" intervals can have edges within themselves and to each other (well, left-right pairs always non-overlapping if we use same p, but within left, intervals might overlap, etc).

Hmm.

OK let me think about this problem in a more direct manner.

**Approach: BFS / Dijkstra with segment tree optimization**

Run Dijkstra from each source. For each source s, we maintain a "frontier" of intervals. When we pop the minimum, we relax neighbors.

The trick: when relaxing from s (with cost d_s), the neighbors are all u with R_u < L_s or L_u > R_s. Instead of relaxing each individually, we want to find the "best" neighbor to relax first.

Use a segment tree indexed by R values (or L values). For "left" neighbors (R_u < L_s), maintain the minimum W_u + d_s over all such u (but d_s is fixed once we pop s, so this is d_s + min W_u for u in range [1, L_s - 1]). But we also need to "visit" the node u, which means we need to consider paths through u too.

This is the standard "0-1 BFS" or "Dijkstra with implicit graph" trick. Let me think.

**Idea: Multi-source Dijkstra with lazy propagation**

Instead of running Dijkstra from each source, run a multi-source Dijkstra where all vertices are sources, and compute the "shortest path tree". Then for each query, we just look up distances.

But this only gives shortest path from a single source, not between arbitrary pairs.

Hmm.

**Alternative: Compute distances between consecutive components or via a "central" structure.**

Let me think about the components of G. Within a component, what's the structure?

**Components of G:** I'll think about this more carefully.

I think the components of G correspond to "intervals that can't be separated by any point clique of the interval graph". Let me try to formalize.

**Lemma:** Two intervals I and J are in the same component of G iff for every point p, there's a sequence of intervals from I to J where consecutive ones don't overlap, AND this sequence can be chosen to "not be blocked" by any specific point.

Hmm, this is circular.

**Different lemma:** I and J are in the same component of G iff for every interval K that "separates" them in some sense... 

OK let me try to find a direct characterization. 

Sort all intervals by L (and by R as tiebreak). Let's index them as I_1, I_2, ..., I_N.

**Claim:** I and J are in the same component of G iff there's no "blocking chain" from I to J.

I'll define: a "blocking chain" from I to J is a sequence of intervals K_1, K_2, ..., K_m such that:
- K_1 overlaps with I (and I is "to the left" of K_1, i.e., R_I < L_{K_1} or ... wait, if K_1 overlaps with I, then they share a point, so neither is entirely to the left/right of the other).
Hmm.

OK let me think about it as: when can we NOT find a path from I to J? This means every sequence I = I_0, I_1, ..., I_k = J has some I_a, I_{a+1} that overlap.

A sufficient condition: there's an interval K such that K overlaps with both I and J, AND K also overlaps with every other interval that's on a "potential path" from I to J... no, this isn't a clean condition.

**Direct claim:** I and J are in different components of G iff there exists an interval K such that K overlaps with I, K overlaps with J, and K overlaps with every interval in some "separating set".

Hmm, let me try a different direct claim.

**Claim:** I and J are in different components of G iff there's an interval K such that K overlaps with both I and J. (NO, this is not sufficient; e.g., I=[1,2], J=[3,4], K=[1,4] - I and J are directly connected in G since they don't overlap. So the existence of K doesn't help here.)

OK so the characterization is more subtle.

Let me think about a "cut" in the co-interval graph. A cut separating I from J would be a set of intervals C such that every path from I to J in G passes through C. Equivalently, in the interval graph, C is a "vertex cut" separating I from J. 

By Menger / flow-cut, in the co-interval graph, the minimal vertex cut separating I and J is a "clique" in the interval graph (a set of pairwise-overlapping intervals, which by Helly share a common point).

So I and J are in different components of G iff there's a "clique" C in H (a set of intervals all sharing a common point p) that separates I and J in G. I.e., I is in the "left" component and J is in the "right" component of G \ C.

Hmm, but this is for connected components. Let me think more carefully.

**Components of G:** I'll define an equivalence: I ~ J if I and J are in the same component of G. 

I'll claim: I ~ J iff there's no point p on the line such that every "path" from I to J is "blocked" by intervals covering p.

Specifically: I ~ J iff for every point p, there's a path from I to J in G that doesn't use any interval covering p.

Equivalently (by some duality), I ~ J iff for every "clique" C in H (intervals covering a point p), there's a path from I to J in G avoiding C.

I think this is equivalent to: I ~ J iff for every "clique" C in H, either I or J is in the "left" group (not covering p) or they can connect through non-p-covering intervals.

Hmm, let me just try to find an algorithmic approach.

**Algorithmic approach for components:**

Here's an idea: 

Sort intervals by L. Sweep from left to right. Maintain a data structure of "active" intervals (those we've started but not finished).

For each new interval I (added when we hit L_I), it might connect to all "previous" intervals. In G, I connects to previous intervals J with R_J < L_I (J is entirely to the left).

Hmm wait, I and J are non-overlapping in G iff R_J < L_I (J to the left) or R_I < L_J (I to the right). So when processing I, it can connect to all J with R_J < L_I and all J with L_J > R_I.

The latter (J to the right of I) we don't know yet when processing I. So we'd need a two-pass approach or maintain things carefully.

For finding components only, here's an idea:

**Two-pass approach:** 
- Pass 1 (left to right): for each I, connect I to all J with R_J < L_I. Use DSU.
- Pass 2 (right to left): for each I, connect I to all J with L_J > R_I. But this might create new connections.

But each pass might create O(N^2) connections.

**Better idea:** Use a segment tree / interval tree to efficiently find "rightmost" or "leftmost" intervals to bridge.

Hmm wait, here's a cleaner way to think about components:

**Claim:** The connected components of G are exactly the connected components obtained by:
- Sort intervals by L.
- Sweep left to right, maintaining a DSU.
- When processing interval I, find the "rightmost" interval J that has been "ended" (R_J < L_I). Connect I to J (and transitively, I is now in the same component as J and all J's component).
- But wait, I might need to connect to multiple "groups" - all those that have ended before L_I.

Hmm, but connecting to just the "rightmost" might be enough because of transitivity.

Let me think. Suppose intervals A, B, C are processed (in some order) and all have R < L_I. They might be in different components. When I comes, it should connect to all of them, merging into one component.

But connecting I to the "rightmost" (which is the one with largest R, but smallest L perhaps) might be enough if the components are already connected through the segment tree structure.

Actually wait, the components of intervals with R < L_I might not be connected to each other. Hmm.

Wait, here's a key observation: if A, B have R_A, R_B < L_I, are A and B in the same component of G? Not necessarily. They could be in different components of G.

Hmm, let me think with example. A=[1,2], B=[3,4], C=[2,3]. Then R_A = 2, R_B = 4, R_C = 3. R_B > L_C = 2, R_C > L_B = 3, so B and C overlap (B=[3,4] and C=[2,3] share 3). A=[1,2] and C=[2,3] share 2. A and B don't overlap (R_A=2 < L_B=3).

In G: A-B edge (don't overlap), A-C no edge (overlap), B-C no edge (overlap). So G has edge A-B only. Component: {A, B}, {C}.

Now add I with L_I = 5. So I comes after B's end. We should connect I to A, B (which are in same component) and C is its own.

But how do we know A and B are in the same component? They are because they're directly connected in G.

Hmm wait, actually in this example, A and B are in the same component of G. C is separate.

If we process in order of L: A first, then C, then B. At each step:
- Process A=[1,2]: new component, {A}.
- Process C=[2,3]: L_C = 2. Intervals with R < 2: A. So C should connect to A? But A and C overlap! So no edge in G. Hmm, but if we just connect C to A in DSU based on "R < L_C", we'd wrongly merge.

So we can't just connect I to all J with R_J < L_I, because some of those might overlap with I (i.e., R_J < L_I but L_J ≤ R_I, meaning they overlap on some interval... wait, if R_J < L_I, then [L_J, R_J] and [L_I, R_I] don't overlap, since the rightmost point of J (R_J) is strictly less than the leftmost point of I (L_I)).

Oh wait, if R_J < L_I, then J is entirely to the left of I, so they don't overlap. So the edge {I, J} exists in G.

So the claim is: process in order of L. For each I, connect I (in DSU) to all previously processed J with R_J < L_I. This means I can reach all those J, and they merge into one component (since I bridges them).

But that creates many connections. The trick: connect I to the "rightmost" such J (largest R_J with R_J < L_I), and rely on transitivity.

Wait, but the J's in question might not all be in the same DSU component. If we connect I to the "rightmost" J, then I is in J's component, but I still needs to be connected to the other J's.

Hmm, here's the thing: if J_1 and J_2 are two intervals with R_{J_1}, R_{J_2} < L_I, are J_1 and J_2 connected in G? They might be in different components of G, so we can't assume.

But wait, for the "rightmost" J, by induction, J is in some DSU component. The other J's with R < L_I need to be connected.

Hmm, let me think. If J_1 and J_2 are both < L_I, then [J_1] and [J_2] are both to the left of I. They might or might not be in the same component of G.

If we connect I to the rightmost J (call it J*), then I is in J*'s component. The other intervals J with R_J < L_I: are they in J*'s component? Not necessarily, because we might have a J_2 with R_{J_2} < L_I that's in a different component of G.

But here's a thought: if J_1 and J_2 are both to the left of I, can they be in different components of G? Yes, as I showed with C=[2,3] being separate from {A, B}. But wait, in that example, A=[1,2] and B=[3,4] and C=[2,3]. R_A = 2, R_C = 3, R_B = 4. For I = some interval with L_I > 4, all of A, B, C have R < L_I. But in G, A and B are in one component, C in another. So if we just connect I to one of them (say A), we'd miss C.

So this simple approach doesn't work.

**Better approach:** Maintain a DSU and a "left endpoint" structure.

Hmm, let me think about it. I think the right approach is:

**Components of G:** 

Consider the interval graph H. The "cliques" of H are sets of intervals covering a single point. The maximal cliques correspond to "events" on the line.

The components of the co-interval graph G correspond to: the line is divided into "segments" by certain critical points, and the components are formed by intervals that "reach" into different segments.

Actually, here's a known result for the complement of an interval graph (co-interval graph):

**Theorem (I think):** The connected components of the co-interval graph correspond to the connected components of an auxiliary graph. Specifically, two intervals are in the same component of G iff for every "clique point" p (a point covered by a maximal clique), the intervals can "reach" each other without crossing p via non-overlapping intervals.

OK let me just think computationally and look for an algorithm.

**Algorithmic approach for shortest path:**

Given the complexity, let me think about what kind of structure the shortest path has.

Claim: In the co-interval graph G, a shortest path from s to t can be found by considering only paths of length at most O(log N) or some small number of "interesting" vertices.

Hmm, I don't think that's right in general.

Let me think about the problem differently.

**Approach: Transform to a different graph problem.**

Let's define a graph G' on the intervals where we add "virtual" nodes for each "point" on the line. Hmm, this is getting complex.

**Let me try yet another approach: "Sweep and conquer" with the line structure.**

Here's an idea that might work:

For each interval I = [L, R], define its weight W. Two intervals I, J are connected in G iff they're disjoint. The shortest path in G (with vertex weights) from s to t, if it exists.

I think the right approach is:

**Approach via a "segment tree" or "interval graph" data structure:**

Build a segment tree over the line [1, 2N]. Each node represents a range. For each interval I, we add it to the segment tree in a certain way.

For the shortest path: from s, we can reach t directly if disjoint, or via some intermediate intervals. The "best" intermediate intervals are determined by which intervals can "bridge" the gap.

Hmm, let me think about this:

Suppose s = [L_s, R_s] and t = [L_t, R_t] with R_s < L_t (s is to the left of t). Then s and t are directly connected. But maybe a shorter path exists through an intermediate interval u with R_s < L_u and R_u < L_t (u is between s and t).

In general, a path from s to t might go: s, u_1, u_2, ..., u_k, t with R_s < L_{u_1}, R_{u_1} < L_{u_2}, ..., R_{u_k} < L_t. So all intervals are "to the left of the next".

The shortest such path: among all chains of intervals from s to t, the shortest is the one with minimum weight.

In a "left to right" chain, this is like a shortest path in a DAG. The shortest path from s to t in the "left-to-right" DAG is: d(s) = W_s, d(u) = W_u + min_{v: R_v < L_u} d(v), d(t) = W_t + min_{v: R_v < L_t} d(v).

Similarly, we can have "right to left" chains. And chains that go left then right (i.e., the intervals first decrease, then increase, like the path in sample 1: [2,4] -> [7,8] -> [4,5]).

A "left-right" chain: I_0, I_1, ..., I_k where I_0 is leftmost and I_k is rightmost, but the chain can go: I_0 < I_1 (R_{I_0} < L_{I_1}), then I_1 > I_2 (R_{I_2} < L_{I_1}), so I_2 < I_1. So the chain "oscillates".

The shortest path in G from s to t can be any of: direct, left-to-right chain, right-to-left chain, or oscillating chain.

**Approach: Consider only "monotone" paths and "two-step" paths.**

For shortest path, consider: 
1. Direct path: weight W_s + W_t (if disjoint).
2. Path through one intermediate u: s -> u -> t, with s and u disjoint, u and t disjoint. Total weight W_s + W_u + W_t.
3. Longer paths.

In many cases, the shortest path is 2 or 3 vertices. But not always.

Hmm, let me think about whether the shortest path can be longer.

Example: consider 5 intervals A=[1,2], B=[3,4], C=[5,6], D=[7,8], E=[2,3]. G edges: A-B, B-C, C-D, B-E, A-E (A and E overlap? A=[1,2], E=[2,3], share 2, overlap, no edge). Wait, A and E share 2, so overlap, no edge. B and E share 3, overlap, no edge. So G edges: A-B, B-C, C-D.

From A to D: A-B-C-D, weight W_A + W_B + W_C + W_D. There's no shortcut. So path length 4 here.

OK so paths can be long. So we need a real algorithm.

**Back to thinking about components and shortest path:**

Let me think about the problem from the perspective of "interval graphs and their complements".

The complement of an interval graph is a co-interval graph. Co-interval graphs are perfect graphs. They have a structure that can be exploited.

Specifically, I recall that for interval graphs, certain problems can be solved by sweep line + data structures. For co-interval graphs, similar techniques might apply.

**Key insight (I think):** The shortest path in the co-interval graph from s to t, if it exists, can be computed by considering the "bottleneck" intervals.

Hmm, let me think about the structure more carefully.

**Alternative: Use a "stacked" or "layered" structure.**

Build a graph where the layers correspond to "gaps" in the interval structure. Each gap is a region on the line between two consecutive "events" (start or end of an interval). Within a gap, all intervals covering the gap pairwise overlap.

The number of gaps is O(N). 

Hmm, this might be useful.

**Concrete approach: Define a graph on "gap pairs" or something similar.**

For each pair of gaps (g_1, g_2) where g_1 is to the left of g_2, the "best" interval that "crosses" from g_1 to g_2 is the interval with minimum weight that's disjoint from g_1 and g_2... no, that's not quite right.

OK let me think about it differently. Here's an approach:

**Approach: Multi-source Dijkstra with implicit graph and segment tree.**

For all-pairs shortest paths, we'd want to do something smart. Let me think about the structure of the problem.

Hmm, I wonder if the answer can be computed per query using a "limited search" from s.

For each query (s, t):
- If s and t are directly connected (disjoint), answer is W_s + W_t.
- Else, find the best intermediate.

To find the best intermediate u: u must be disjoint from both s and t. So u is to the "left" of both s and t (R_u < min(L_s, L_t)) or to the "right" of both (max(R_s, R_t) < L_u), or "between" s and t in some way.

Case 1: u to the left of both. Then R_u < L_s and R_u < L_t. So u is in the range [1, min(L_s, L_t) - 1] (where R_u < min(L_s, L_t)).
Case 2: u to the right of both. Then R_s < L_u and R_t < L_u. So L_u > max(R_s, R_t).
Case 3: u "between" s and t. If s and t overlap, then u might be in various positions. If s is to the left of t (R_s < L_t), then u could be to the right of s and to the left of t (L_s < R_u < ... wait, R_s < L_u means u starts after s ends, and R_u < L_t means u ends before t starts, so u is in (R_s, L_t)).

So if s and t are disjoint, the "between" region is (R_s, L_t) and the "best between" is min W_u for u in this region (with R_s < L_u and R_u < L_t).

But the shortest path might be longer than 2 intermediate vertices.

**OK let me try to think about this problem in terms of "two-layer" shortest paths.**

The shortest path in G from s to t can be of the form:
- Direct: s-t.
- s-u-t: through one intermediate u.
- s-u-v-t: through two intermediates u, v.
- ...

For long paths, the structure matters.

**Hmm, let me think about the problem from the perspective of "what is the structure of the shortest path".**

Observation: in the co-interval graph, the shortest path has a specific structure. Let me think.

A path s = v_0, v_1, ..., v_k = t in G. Each consecutive pair (v_i, v_{i+1}) is disjoint. 

Define a "type" for each edge: "L" if v_i < v_{i+1} (R_{v_i} < L_{v_{i+1}}), "R" if v_{i+1} < v_i. The path is a sequence of L's and R's.

Hmm, the sequence can be any mix. But the key observation: once we go "L" (v_i is to the left of v_{i+1}), then v_{i+1} is to the right of v_i, but v_{i+2} could be on either side of v_{i+1} (as long as disjoint).

**Alternative formulation: think of the path as a sequence of "moves" on the line.**

Each move: from current interval v, go to a disjoint interval u. The "position" of the path on the line can be tracked.

Hmm, I think this is getting complex. Let me look for a different approach.

**Approach: Build a "compressed" graph.**

The co-interval graph G has a specific structure. Let me see if there's a way to "compress" it.

Observation: For each interval I, the "neighbors" of I in G are intervals to the left (R < L_I) and to the right (L > R_I). Within "left neighbors", the structure depends on the left intervals.

Hmm, what if we build a "segment tree" where each leaf represents a point and each internal node represents a range. We insert intervals into the tree based on their L and R.

For the shortest path: from s, we want to find the best "first step" u. The first step u is to the left of s (R_u < L_s) or to the right of s (L_u > R_s). 

Among left-first options, the "best" u (by weight) might be the closest one to s (smallest gap), but the optimal might not be the closest.

**Hmm, let me try a different angle. Let's see if there's a "two-level" structure.**

In the co-interval graph, the "neighborhood" of a vertex I consists of all intervals disjoint from I. This is a "large" set (could be O(N)).

**Approach: Consider the problem as a "multi-source BFS" on a different graph.**

Define a new graph G'' where vertices are intervals, and there's an edge from I to J iff I and J are "adjacent" in some specific sense (e.g., I and J are disjoint and there's no interval K disjoint from both I and J with W_K < min(W_I, W_J)). 

Hmm, this doesn't quite work either.

**OK let me just try to think about the problem algorithmically and code it up.**

Here's a plan:

1. Find the connected components of G.
2. For each component, compute the "internal shortest path structure" so that we can answer queries within the component.
3. For queries between different components, output -1.

For step 2, we need a way to compute shortest paths in the co-interval graph efficiently for many queries.

For step 1, finding components of G:

**Components of G algorithm:**

Sort intervals by L. Sweep left to right. Maintain:
- A set of "active" intervals (those that have started but not ended).
- A set of "ended" intervals (those that have ended).

For each new interval I (when we hit L_I), it connects to:
- All "ended" intervals (R < L_I) - they are disjoint from I.
- All "future" intervals (L > R_I) - they are disjoint from I, but we don't know them yet.

For the first part, connect I to all ended intervals. But we want to do this efficiently.

**Efficient DSU approach:**

For each I, find the "rightmost" ended interval J (largest R_J < L_I). Connect I to J in DSU. This handles the case where all ended intervals are transitively connected.

But as I noted, ended intervals might not be transitively connected (in G). Hmm.

Wait, actually, let me reconsider. If J_1 and J_2 are both ended (R < L_I), are J_1 and J_2 necessarily in the same component of G?

Not necessarily, as shown. Hmm.

But here's a thought: if I is "between" J_1 and J_2, then I connects to both, so they're in the same component (via I).

If I is to the right of both, then in G, J_1 and J_2 are in different components possibly.

Hmm.

**Wait, I think the key insight is:**

For the components of G, I think we can characterize them as follows:

I and J are in the same component of G iff there's no "interval K" that "separates" them. Specifically, K separates I and J if K overlaps with I, K overlaps with J, and for every other interval L on a potential path from I to J, K overlaps with L... no, this is too vague.

**Let me try a different characterization:**

I and J are in the same component of G iff there's a "path" of disjoint intervals. Equivalently, by the structure of interval graphs, the components of G correspond to "intervals that aren't separated by any single clique in H".

I'll just try to find an efficient algorithm.

**Algorithm for components:**

Here's an approach. Sort intervals by L. Sweep and maintain a stack / DSU.

For each interval I, when we encounter it (at L_I), it "starts". We add it to a DSU. We also "process" all intervals that "ended" (R < L_I).

When an interval J ends (at R_J), it's no longer "active". We need to "connect" J to the next interval that comes.

Specifically, when we process interval I (at L_I), we connect I to all "ended" intervals (those with R < L_I). But we need this to be efficient.

Use a DSU where we maintain the "rightmost" interval that's been ended. If we always connect to the rightmost, then by transitivity, I is connected to all the ones the rightmost is connected to. But as noted, ended intervals might be in different components.

Hmm wait, here's the key: at the time of processing I (L_I), the "ended" intervals might be in different components of G. We need to connect I to all of them, merging them.

But we can do this efficiently if we know all the components. The number of distinct components of "ended" intervals is at most O(N).

**Use DSU with a "merge" operation:**

Maintain DSU of components. For each interval I, find all distinct DSU components of intervals with R < L_I. Connect I to one representative from each, merging all into one component (containing I).

To find all distinct components: this could be expensive in the worst case. But maybe amortized O(α(N)) per interval if we use a "process all and skip" trick.

Hmm, but actually here's a simpler approach:

**The components of G are exactly the "components formed by the following merging process":**

1. Start with each interval as its own component.
2. Sort intervals by L.
3. For each interval I (in sorted order), at the point L_I:
   a. Find the "rightmost" interval J that's "open" at L_I (i.e., L_J ≤ L_I ≤ R_J, and J is not "ended" before L_I).
   b. Actually, find the interval J that "ends" just before L_I (largest R_J < L_I). Connect I to J.
4. After processing all intervals, also do the reverse pass: sort by R, for each interval I, find the "leftmost" interval J with L_J > R_I, connect.

Hmm wait, this is for the interval graph, not co-interval.

Let me think again about the co-interval graph.

**Approach: Use the line as a "guide"**

Here's a thought: at each point on the line, there's a set of "active" intervals. The "active intervals" at point p form a clique in H (no edges in G among them).

If we have intervals I, J and they overlap (i.e., share a point), they're "in the same clique at that point". For them to be in the same component of G, we need to "escape" the clique.

A "barrier" between I and J: a clique C in H such that I is "to the left" of C and J is "to the right" (or vice versa), meaning all intervals in C overlap with both I and J... hmm, this needs more thought.

OK let me just try to look up or recall: the co-interval graph's components.

**I think** the components of the co-interval graph G are the same as the "biconnected components" or "2-connected components" of some auxiliary graph, OR they're determined by the "maximal cliques" in H.

Specifically, I think:

**Claim:** Two intervals I and J are in the same component of G iff for every "maximal clique" C of H (a set of intervals all covering a point p), I and J are not "separated" by C in G (i.e., removing C from G doesn't disconnect them).

If we remove a single clique C from G, we disconnect it into some number of components. The components of G are formed by considering all such "clique removals".

But this is complex. Let me just try a direct approach.

**Direct approach for shortest path:**

I'll just implement Dijkstra from each source, but use a segment tree to make it efficient.

But Dijkstra from each source is O(N log N) each, and Q is up to 2*10^5. So total O(N * Q) is too slow.

**Alternative: Process all queries simultaneously with multi-source / Johnson-like approach.**

Hmm, this is hard.

**Wait, I think the right approach is:**

**Key insight:** The shortest path in the co-interval graph from s to t, if it exists, has a specific structure that allows efficient computation.

Specifically, I claim the shortest path from s to t can be found by considering a "two-step" or "few-step" path, and the structure allows efficient queries.

Hmm, but I showed earlier that paths can be long (length 4 in the example).

**Alternative key insight:** The graph G can be "compressed" into a smaller graph that preserves shortest path distances.

Let me think. In G, two intervals I, J are connected if disjoint. The "neighborhood" of I in G is large. But maybe we can find a smaller set of "important" neighbors.

**Claim:** For shortest path purposes, we only need to consider "extreme" intervals: those with extreme L or R values.

Specifically, for an interval I, the "important neighbors" in G are:
- Intervals with the largest R < L_I (closest to I from the left).
- Intervals with the smallest L > R_I (closest to I from the right).

Wait, but the "closest" might not be the "best" (in terms of weight).

Hmm.

**Alternative: Maintain a "best so far" using a segment tree.**

For each point p, maintain the "best interval not covering p" (by some criterion). Then for shortest path, use these.

Hmm, let me think.

**Approach: Sweep line with segment tree, find best "bridge".**

Here's an idea:

For each pair (s, t), if s and t overlap, then any path s -> u -> t requires u disjoint from both. The "best" u is the one with minimum W_u.

If s and t are disjoint, say s < t (R_s < L_t), then the shortest path from s to t is W_s + W_t (direct), OR via an intermediate u that's "between" s and t (R_s < L_u and R_u < L_t), or via an intermediate u "to the left of both" or "to the right of both".

The "best" intermediate u to the left of both: u has R_u < L_s. Then path is s -> u -> t (s disjoint from u, u disjoint from t). Weight: W_s + W_u + W_t. So we want min W_u over u with R_u < L_s (and R_u < L_t, but R_u < L_s implies R_u < L_t if R_s < L_t, wait no, R_u < L_s and R_s < L_t means R_u < L_s < R_s < L_t, so R_u < L_t).

Similarly, "to the right of both": u with L_u > R_t.

"Between" s and t: u with R_s < L_u and R_u < L_t.

So for s < t (disjoint), the shortest path is:
- Direct: W_s + W_t.
- Via left u: W_s + W_t + min W_u over u with R_u < L_s.
- Via right u: W_s + W_t + min W_u over u with L_u > R_t.
- Via between u: W_s + W_t + min W_u over u with L_u > R_s and R_u < L_t.

But wait, the "via u" might allow u to be a multi-step path itself. The shortest path from s to t might be longer than 2 steps.

Hmm, but maybe we can decompose: the shortest path from s to t in G is the min over all "first step" u of (W_s + shortest path from u to t in G). So it's a recursive problem.

The shortest path from u to t in G can be computed similarly. To avoid recomputation, we can use Dijkstra.

**Approach: Multi-source / All-pairs via segment tree**

Idea: For each source s, run Dijkstra. To make each Dijkstra efficient, use a segment tree.

For Dijkstra from s, the "neighbors" of s are all u with R_u < L_s or L_u > R_s. We want to find the min W_u among these.

But Dijkstra needs to also consider paths of length > 1. So after popping s with cost d_s, we update d_u for all neighbors u with d_s + W_u. Then we pop the next min, etc.

To do this efficiently, use a segment tree. The segment tree is indexed by, say, R values. For "left neighbors" (R_u < L_s), we want to update d_u for all such u. But there are many, and we need to "process" each.

**Use a "lazy segment tree" trick:**

After updating d_u for all u in a range, we want to skip them next time. This is the "Dijkstra with implicit graph" technique.

Specifically, maintain a segment tree where each node represents a range of R values, and the value is min (d_u - W_u) or something. When we "relax" all u in range [1, L_s - 1] with the current d_s, we update the segment tree to reflect the new d_u values.

But the issue is that after relaxing, we need to extract the min over the entire range, and the min might not be in the range we just relaxed.

Hmm wait, here's the standard approach for this kind of problem:

**"Connect all nodes in a range to a new node" trick:**

Create a virtual node v_s with cost 0, connect it to all u with R_u < L_s with edge weight