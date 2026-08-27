
## ideation
The problem asks for shortest path (by sum of vertex weights) in the co-interval graph G where edges connect pairs of disjoint intervals. N, Q up to 2×10^5.

Key observations:
- G is the complement of an interval graph (co-interval graph).
- Two intervals I,J are connected iff R_I < L_J or R_J < L_I.
- Need to answer Q queries for shortest weighted path.

The graph is dense (potentially O(N²) edges), so we need implicit representation.

Critical insight: The shortest path in G from s to t can be computed by considering "bridge" intervals. The structure suggests using a segment tree / sweep line approach.

For each interval I, neighbors are all u with R_u < L_I (left) or L_u > R_I (right). 

Approach: Build a segment tree over R values. For each query, we need to find shortest path. The trick is to use a "virtual node" approach: for each interval I, conceptually connect all "left neighbors" to I via a virtual node with edge weight 0, and I to the virtual node with weight W_I. Then shortest path in this augmented graph gives the answer.

But this creates too many virtual nodes. Better: use a segment tree where each node stores the minimum W among intervals in its range, and we can "jump" through the tree.

Actually, the cleanest approach: For each point p on the line, the intervals not covering p can be partitioned into "left" (R<p) and "right" (L>p). Any left interval is disjoint from any right interval. So we can use a segment tree where each node represents a range, and we store the best interval in that range.

For shortest path from s to t: if they're disjoint, direct. Otherwise, find the best "bridge" - an interval u disjoint from both. The bridge is either entirely left of both, entirely right of both, or "between" them.

But paths can be longer than 2 steps. So we need a more general approach.

**Plan**: Use Dijkstra with a segment tree optimization. Build a segment tree over R values. For each interval I, store it at position R_I in the segment tree with value W_I. When relaxing from I with current distance d_I, we want to update all u with R_u < L_I (left neighbors) to d_I + W_u, and all u with L_u > R_I (right neighbors) to d_I + W_u.

For "left neighbors": query segment tree for range [1, L_I - 1] to find min W_u, update that u, then "remove" it (mark as visited) and repeat. This is the standard "range minimum + pop" trick.

For "right neighbors": similar but indexed by L. We'd need a second segment tree over L values.

After Dijkstra from s, we have distances to all vertices. But running Dijkstra per query is O(N log N) each, too slow for Q=2×10^5.

**Better approach**: Since the graph has special structure, maybe we can preprocess all-pairs or use a different decomposition.

Actually, I think the right approach is to recognize that the shortest path in the co-interval graph has a specific structure related to "interval chains". Let me think about this more carefully.

For two intervals s and t, the shortest path from s to t in G can be computed as follows:
- If s and t are disjoint, answer is W_s + W_t.
- Otherwise, we need to find a path. The path goes through intervals that "bridge" the gap.

The key observation: any path from s to t in G corresponds to a sequence of intervals where consecutive ones are disjoint. This sequence can be decomposed into "left-to-right" and "right-to-left" segments.

Hmm, let me think about the problem from the perspective of "what queries can be answered efficiently".

**Alternative approach**: For each query (s,t), compute the answer using a limited search. If s and t are in the same component, the shortest path might have a specific structure.

Let me think about the components of G more carefully. I claim:

**Components of G**: Two intervals I and J are in the same component of G iff there's no "interval K" such that K overlaps with I, K overlaps with J, and K is "between" them in a strong sense.

Actually, I think the components are determined by: I and J are in the same component iff for every point p, there's a path from I to J avoiding intervals covering p.

This is equivalent to: I and J are in the same component iff for every "clique" C in H (intervals covering a point), I and J are connected in G \ C.

Hmm, this is still complex.

Let me just try to implement a solution and see.

**My plan**:
1. Find connected components of G using DSU with sweep line.
2. For each component, precompute shortest paths or use a clever query algorithm.
3. Answer queries.

For step 1, I'll use the following approach:
- Sort intervals by L.
- Sweep left to right. Maintain a DSU.
- For each interval I (at L_I), find all intervals J with R_J < L_I (ended before I starts). These are all disjoint from I, so connect I to them.
- To do this efficiently: maintain a "rightmost ended" pointer. When we process I, find the rightmost J with R_J < L_I. Connect I to J. But this only connects I to one J, not all.

Wait, here's the key: if J_1 and J_2 are both ended (R < L_I), and they're in different DSU components, then connecting I to just one doesn't merge them. We need to connect I to all distinct components.

But here's a trick: if J_1 and J_2 are both ended and in different components, can they be "merged" later? Only if some future interval connects them. But I is the first future interval (L_I > R_{J_1}, R_{J_2}), so I connects to both, merging them.

So the algorithm: for each I, find all distinct DSU components of intervals with R < L_I, and merge them all with I.

To find distinct components efficiently: use a "visited" set or a "representative" map.

Actually, here's a cleaner approach:

**Two-pass algorithm for components**:
- Pass 1 (left to right): for each I, connect I to the interval J with the largest R_J < L_I. This handles "left" connections.
- Pass 2 (right to left): for each I, connect I to the interval J with the smallest L_J > R_I. This handles "right" connections.

But this might miss some connections. Let me think.

If I connects to J (largest R_J < L_I), and J connects to K (largest R_K < L_J), then I, J, K are in the same component. This handles "chains to the left".

But what about "parallel" intervals? E.g., J_1 and J_2 both with R < L_I, but J_1 and J_2 are in different components. Then connecting I to only the "largest R" misses J_2's component.

Hmm, so this doesn't work directly.

**Better approach**: Use a segment tree to maintain the "rightmost interval in each component" or something.

Actually, let me think about it differently. Here's an approach that works:

**DSU with "merge all in range"**:
- Sort intervals by L.
- For each I, find all intervals J with R_J < L_I. These are all disjoint from I.
- Merge I with all of them in DSU.
- To do this efficiently: maintain a map from R to interval. For each I, iterate over all J with R_J < L_I and merge. But this is O(N²) in the worst case.

**Optimization**: Use a "skip" list. After merging J into I's component, mark J as "processed" and skip it next time. But we need to process all J with R_J < L_I, which could be many.

Hmm, but here's the thing: the total number of "merge" operations across all I is bounded. Because each interval J is "ended" once, and at that point, it's merged with the next interval I that starts after R_J. So each interval is involved in O(1) merges (as the "ended" one).

Wait, let me think. When interval J ends (at R_J), the next interval I that starts (L_I > R_J) will merge with J. But there might be multiple intervals starting after R_J before the next "merge point".

Hmm, actually, here's the key: when we process I (at L_I), we want to merge I with all J with R_J < L_I. The number of such J is the number of intervals that have ended. Over all I, the total number of "merge attempts" is O(N²) in the worst case.

But we can optimize: if J_1 and J_2 are both ended and in the same DSU component, we only need to merge once. So we can use a "representative" for each component.
