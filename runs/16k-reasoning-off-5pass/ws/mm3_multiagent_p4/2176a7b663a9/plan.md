1. Build an auxiliary graph that's sparse but preserves shortest paths.
2. For each component, run Dijkstra from each "source" or preprocess.

Actually, I think for this problem, since we need Q queries, we should preprocess per-component. But components could be large.

**Alternative: Answer each query independently with a clever algorithm.**

For query (s,t):
- If s,t disjoint: answer W_s+W_t.
- Else: compute the min-weight path.

When s,t overlap, the min path goes s—v1—v2—...—vk—t. 

Hmm, let me reconsider the example. s=[1,3], t=[2,4], v1=[3.5,3.5], v2=[1.5,1.5]. The min path is W_s+W_{v1}+W_{v2}+W_t. But this used the fact that v1∈(R_s,∞) and v2∈(-∞,L_t).

More generally, a path s=v0,v1,...,vm=t with m≥2, s,t overlap. The path must "go around" the overlap. The intervals along the path are arranged along the line.

I think the shortest path from s to t (in edges) in the disjointness graph, when s,t overlap, has a specific structure related to the "chain" through the complement. But for min WEIGHT, we want few cheap vertices.

**Given the difficulty, let me reconsider whether the graph can be built.**

N=2×10^5. If we build the graph, worst case O(N^2) edges. But maybe the graph is actually sparse due to coordinates ≤ 2N?

Worst case: N intervals, all pairwise disjoint. E.g., [1,1], [2,2], ..., [N,N]. Then G is complete, N(N-1)/2 edges. Too many.

So we cannot build G explicitly.

**Need a structural algorithm.**

**Key insight revisited**: Let me think about the poset. Define i ≺ j iff R_i < L_j. This is a strict partial order (interval order). G has edge (i,j) iff i≺j or j≺i, i.e., iff they're comparable in this poset.

So G is the **comparability graph** of the interval order.

In a comparability graph, the shortest path between two comparable elements s≺t is just the edge (s,t) directly. For incomparable s,t (overlapping), the shortest path goes through a chain of comparable pairs.

**Shortest path in comparability graph of interval order**:

s and t incomparable (overlap). A path s=v0, v1, ..., vm=t with each vi, vi+1 comparable. 

Claim: such a path corresponds to "going around" the overlap. The min-weight path: 

Let me think of the intervals on the number line. s=[L_s,R_s], t=[L_t,R_t], overlap, say L_s≤L_t≤R_s (and R_t≥L_t). 

A comparable pair (a,b) with a≺b means a is left of b (R_a<L_b). The comparability graph connects a,b iff a is left of b or b is left of a.

To go from s to t when they overlap, we need to leave s going either left or right, and arrive at t from the other side. 

Path: s ≺ v1 ≺ v2 ≺ ... ≺ t? But if s≺v1 (s left of v1), and v1≺v2, ..., vm=t, then by transitivity s≺t, so s,t comparable, contradiction. So the path can't be a single chain ≺.

It must reverse direction. E.g., s ≺ v1, then v2 ≺ v1 (v2 left of v1), etc. So the path goes s→right→...→left→...→t or s→left→...→right→...→t.

Concretely: s→v1 (s≺v1, s left of v1), v2→v1 (v2 left of v1), v2→v3 (v2 left of v3), ..., vk→t (vk left of t). 

So the path: s [left of] v1, v2 [left of] v1, v2 [left of] v3, v3 [left of] v4, ..., v_{m-1} [left of] t. 

This is like: start at s, go right to v1, then left to v2 (v2 left of v1), then right to v3, ..., ending at t with some v_{m-1} left of t.

This zigzag corresponds to the path "going over" the overlap region.

For the min-weight path, we want to minimize the sum of W along the path. 

**Formulation**: The shortest path from s to t in the comparability graph, with vertex weights.

This is a well-defined problem. Let me think computationally.

**Algorithm idea**: Since the poset is an interval order, we can process queries. But with 2×10^5 queries, need near O((N+Q) polylog) or O((N+Q)√N).

**Use the bounded coordinate**: L_i, R_i ≤ 2N. 

Let me define "left" and "right" neighbors more carefully. For interval i, sort other intervals. 

**Sparse graph construction**: 

For each "left end" R_j, maintain intervals with that R. For interval i, Left[i] = {j: R_j < L_i}. 

The issue is Left[i] could be large.

**Observation for path weight**: The min-weight path from s to t. Let's define:
- A[s] = min weight of a path from s to t. 

Hmm, let me think about the problem as finding shortest path in a graph with N=2×10^5 vertices and up to O(N^2) edges, but with a special structure (comparability graph of interval order).

**For comparability graphs, there's a known result**: Shortest paths can be found efficiently.

Actually, let's think about it as follows. For the min-weight path s to t (s,t overlap):

The path is s = v0, v1, ..., vm = t. Each edge (vi, vi+1) means one is left of the other. 

**Encoding by positions**: assign each interval a "position" on the line. Then comparability is about order on the line (with the overlap complicating things, since two intervals can overlap and be incomparable).

**Reduction**: Consider the "left" relation. For intervals a,b, a≺b iff R_a<L_b. The comparability graph connects comparable pairs. 

The min-weight path problem in this graph: this is equivalent to finding a sequence of intervals that "connect" s to t, where consecutive ones are disjoint (and one is left of the other).

**Trick**: Since L,R ≤ 2N, discretize to integer coordinates 1..2N. 

**Direct algorithm for one query**: Dijkstra on the implicit graph. But N=2×10^5 and edges are dense in worst case. Per query O(N^2) is too slow.

**Multi-query**: Preprocess.

**New idea**: The answer to query (s,t) depends only on the "region" around s and t. Specifically, intervals far from s and t (in the disjointness sense) might not matter. 

**Let me reconsider the problem constraints**: L_i, R_i ≤ 2N. And N ≤ 2×10^5. So the coordinate range is 4×10^5. 

**Segment tree / sweep approach**:

Sort intervals by L. Process from left to right. Maintain a data structure of "active" intervals (those started but not ended). 

When we add interval i (at position L_i), it becomes active. At position R_i+1 (or when we pass R_i), it becomes inactive. 

But how does this help with G?

Two intervals are adjacent in G iff they're disjoint. In the sweep, two intervals are disjoint iff they don't coexist in the "active" set at the same point... no, they could be disjoint and never coexist (one ends before the other starts). Actually, if they're disjoint, they don't both contain any point, so they're never both "active covering the same point". Conversely, if they overlap, they share a point and are simultaneously active.

This is just the interval graph characterization. The complement (disjointness) is harder.

**Let me think about connected components and shortest paths via a different lens.**

**The min-weight path equals**: W_s + W_t + (min weight of intermediates on the path).

**Two-hop path (length 2)**: s—k—t, weight W_s+W_k+W_t. Min over k: W_s+W_t + min_{k⊥s, k⊥t} W_k. This works when such k exists.

**Three-hop path**: s—a—b—t, weight W_s+W_a+W_b+W_t. s⊥a, a⊥b, b⊥t. 

In general, length m+1 path (m intermediates).

**Key**: For interval disjointness, what are the possible path lengths?

I showed diameter can be 3. Can it be larger? 

Try diameter 4. s,t overlap. Path s—v1—v2—v3—t. Each consecutive disjoint. s⊥v1, v1⊥v2, v2⊥v3, v3⊥t. 

Positions: s and t overlap. v1 is a neighbor of s. v3 is a neighbor of t. v2 is between. 

For the path to be length 4 (not shortcuttable to ≤3): no length-2 path (no common neighbor), and no length-3 path exists, or the length-3 paths are more expensive... wait, for the min-weight path, even if length-3 exists, a length-4 path is worse (more vertices, positive weights). So the min-weight path uses the minimum number of intermediates. 

So we want the min number of intermediates, then min weight among those.

**Min number of intermediates** (path length - 1) between s and t in G: this is the distance in G (number of edges) minus 1. Let dist_G(s,t) = number of edges in shortest path. Path length = dist_G. We want min-weight path of length dist_G (since positive weights, shorter is better weight-wise, and among same length, min weight).

Wait, is that true? If there are two paths of length 3 with different weights, we pick the lighter. But a path of length 4 is always worse than length 3 (adds positive weight). So yes, min-weight path = min-weight path among shortest paths (in edges). So we need to find shortest path in G (by edge count) and min-weight among those.

**Graph distance in comparability graph of interval order**: 

s,t overlap (incomparable). dist(s,t) ≥ 2. 

dist = 2 iff common neighbor exists (k⊥s, k⊥t).
dist = 3 iff no common neighbor, but dist ≤ 3.

Can dist = 3? Yes, my example. Can dist ≥ 4? 

For dist ≥ 4, need no path of length ≤ 3. This means:
- No direct edge.
- No common neighbor.
- No length-3 path.

A length-3 path is s—a—b—t. s⊥a, a⊥b, b⊥t. This means a is a neighbor of s, b is a neighbor of t, and a⊥b.

Neighbors of s: Left[s]∪Right[s] (intervals disjoint from s). 
Neighbors of t: Left[t]∪Right[t].

a ∈ N(s), b ∈ N(t), a⊥b.

So a length-3 path exists iff ∃a∈N(s), b∈N(t) with a⊥b.

Length-4 path: s—a—b—c—t, a∈N(s), b∈N(a)∩N... actually a—b—c—t with a∈N(s), c∈N(t), b∈N(a)∩N(c).

Hmm. Let me think when dist = 3 fails but dist = 4 exists.

For dist = 3: ∃a∈N(s), b∈N(t), a⊥b.
For no dist = 3: ∀a∈N(s), b∈N(t), a∩b≠∅ (overlap). I.e., every neighbor of s overlaps every neighbor of t.

N(s) = Left[s]∪Right[s] = {j: R_j<L_s} ∪ {j: R_s<L_j}.
N(t) = {j: R_j<L_t} ∪ {j: R_t<L_j}.

For all a∈N(s), b∈N(t): a∩b≠∅.

Take a∈Left[s] (R_a<L_s) and b∈Right[t] (R_t<L_b). a⊂(-∞,L_s), b⊂(R_t,∞). a∩b≠∅ means they overlap. a⊂(-∞,L_s), b⊂(R_t,∞). They overlap iff the intervals [R_a,L_s-1]? Well, a=[L_a,R_a] with R_a<L_s, b=[L_b,R_b] with R_t<L_b. a∩b: max(L_a,L_b)≤min(R_a,R_b). Since a is left and b is right, a∩b≠∅ iff L_b≤R_a. L_b>R_t and R_a<L_s. So L_b≤R_a iff R_a≥L_b>R_t and R_a<L_s. So R_a > R_t and R_a < L_s. Since s,t overlap, R_t ≥ L_t and L_s ≤ R_s... let's set coords. s=[L_s,R_s], t=[L_t,R_t], L_s≤L_t≤R_s≤R_t (s,t overlap, and WLOG this ordering). Then a⊂(-∞,L_s), b⊂(R_t,∞) with R_t≥R_s≥L_s. a∩b≠∅ requires L_b≤R_a with L_b>R_t≥R_s>L_s>R_a. So L_b>R_s>R_a, L_b≤R_a means R_a≥L_b>R_s, but R_a<L_s≤R_s. Contradiction. So a∈Left[s], b∈Right[t] are always disjoint (since a right end < L_s ≤ R_s ≤ R_t < b left end). 

So if both Left[s] and Right[t] are nonempty, we have a⊥b, giving dist ≤ 3. 

Therefore, for dist > 3 (i.e., no length-3 path), we need either Left[s]=∅ or Right[t]=∅ (assuming the WLOG s left of t).

Similarly, by symmetry, if Right[s] and Left[t] are both nonempty, dist ≤ 3 (take a∈Right[s], b∈Left[t]; a⊂(R_s,∞), b⊂(-∞,L_t); since R_s≥L_t, a and b are disjoint, edge).

So for dist ≥ 4: need Left[s]=∅ or Right[t]=∅ AND Right[s]=∅ or Left[t]=∅.

With s left of t (L_s≤L_t≤R_s≤R_t):
Left[s] = {j: R_j<L_s}. 
Right[s] = {j: R_s<L_j}.
Left[t] = {j: R_j<L_t}.
Right[t] = {j: R_t<L_j}.

For dist ≥ 4: (Left[s]=∅ or Right[t]=∅) and (Right[s]=∅ or Left[t]=∅).

Case 1: Left[s]=∅ and Right[s]=∅. Then N(s)=∅, s isolated. dist=∞. 
Case 2: Left[s]=∅ and Left[t]=∅. N(s)=Right[s], N(t)=Right[t]. For dist=3: need a∈Right[s], b∈Right[t], a⊥b. Both in (R_s,∞) and (R_t,∞) resp. a,b could overlap. For all a,b to overlap, the intervals in (R_s,∞) and (R_t,∞) must all pairwise overlap. Since R_s≤R_t, (R_s,∞)⊃(R_t,∞). So a∈(R_s,∞), b∈(R_t,∞)⊂(R_s,∞). So a,b both in (R_s,∞). They could overlap. For ALL such a,b to overlap, the family of intervals in (R_s,∞) must be such that any two overlap (a "clique" in interval graph, i.e., common point). Similarly for (R_t,∞). Hmm, and we need cross: a∈(R_s,∞), b∈(R_t,∞) overlap. This is possible (e.g., all intervals contain point 100). 

But we also need that there's no length-3 path. A length-3 path is s—a—b—t, a⊥s, b⊥t, a⊥b. With N(s)=Right[s], a∈Right[s]. N(t)=Right[t], b∈Right[t]. a⊥b. For no such a,b, all a∈Right[s], b∈Right[t] must overlap. This means every interval in Right[s] and every interval in Right[t] pairwise overlap. In particular, all intervals in Right[s]∪Right[t] pairwise overlap, so they have a common point p≥R_t. So Right[s]∪Right[t] is contained in intervals containing p.

Now, can there be a length-4 path? s—a—b—c—t. a∈N(s)=Right[s]. c∈N(t)=Right[t]. b∈N(a)∩N(c). b must be disjoint from a and c. a,c are in (R_s,∞) and both contain p (or are near). b disjoint from both means b is left of a's left or right of a's right, and similarly for c. Since a,c contain p, b disjoint from both means b doesn't contain p, and is either entirely left of min(L_a,L_c) or entirely right of max(R_a,R_c). 

Also, for the path s—a—b—c—t: s⊥a ✓, a⊥b, b⊥c, c⊥t ✓ (c∈Right[t]). 

So b is disjoint from a and c. Since a,c both contain p (or are in the common region), b must be outside. Say b is entirely left of p (left of L_a and L_c) or entirely right.

If b is left: b⊂(-∞,p). b disjoint from a (which contains p) means b's right < L_a. Similarly b's right < L_c. So b⊂(-∞, min(L_a,L_c)). 

Now, is b a