
## ideation
The problem requires determining if we can assign integer strengths \(w_j\) to roads such that for a set of people, each person's stamina is 0 at start and end, and positive at all intermediate towns. 

**Core difficulty**: Reduce the stamina requirements to a set of constraints on a sequence of town "heights" \(C_k\) (where \(C_1=0\) and \(w_j = C_{j+1} - C_j\)). For a person traveling from \(S\) to \(T\):
- If \(S < T\): need \(C_S = C_T\) and \(C_k > C_S\) for all \(S < k < T\) (upward mountain).
- If \(S > T\): need \(C_S = C_T\) and \(C_k < C_S\) for all \(T < k < S\) (downward valley).

Thus each person imposes equality on endpoints and strict inequality on interior towns, with direction depending on travel direction. The global feasibility is equivalent to the directed graph of strict inequalities (after contracting equality components) being acyclic.

**Candidate approaches**:
1. **Laminar family check**: Initially I thought the condition is that intervals form a laminar family, but sample 1 shows crossing intervals with opposite directions can be compatible. The condition is more complex: it depends on the relative ordering of the heights.
2. **Difference constraints**: Build a graph of inequalities \(C_v - C_u \geq \delta\) (with \(\delta = 1\) for strict, after scaling) and check for positive cycles. With N up to 4e5, M up to 2e5, and Q up to 2e5, we need something faster than per-query Bellman-Ford.
3. **Segment tree with union-find + potentials**: Process people in order, maintain a data structure that can add constraints and detect cycles. For range queries, we could build a segment tree where each node stores the "state" after applying that node's people, and combine nodes by merging their union-find structures (small-to-large). This might be O((N+M+Q) log N) amortized.
4. **Observation about "nesting" and ordering**: Perhaps the constraints are equivalent to requiring that no two "up" intervals cross and no two "down" intervals cross. An "up" and a "down" can cross. This might be checkable with a sweep line or interval tree. But we have range queries on subsets of people, not all people.
