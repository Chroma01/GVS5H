
## ideation
The problem asks whether we can assign integer strengths to the N‑1 edges of a line so that a given set of people each walk from S_i to T_i (|S_i−T_i|>1) with stamina 0 at the endpoints and a positive integer at every interior town.

**Core difficulty:** Understanding the feasibility condition for a set of intervals and how overlapping constraints interact.

**Key observations:**
- For a single person with interval length L = |S_i−T_i|, we need a sequence of L integers w such that the partial sums P_0=0, P_L=0, and 0<P_k<L for 1≤k<L. This is exactly a strictly positive excursion of length L. Such a sequence exists **iff L is even** (e.g. alternating +1,−1 works).
- If we set every edge strength to an alternating pattern (e.g. w_j = 1 if j odd, −1 if j even), then for **any** even‑length interval the partial sum is 0 at both ends and exactly +1 at all interior points. This single global assignment satisfies all even‑length intervals simultaneously.
- Therefore, a set of people can be satisfied iff **every person in the set has an even distance**. Overlap does not create additional constraints because the alternating assignment works uniformly for all even intervals.

**Reduction:** Precompute an array `even[i] = 1` if `|S_i - T_i|` is even, else `0`. For each query [L,R], answer “Yes” if the sum of `even[L..R]` equals `R-L+1`, otherwise “No”. This is a standard range‑sum query solvable with prefix sums in O(1) per query.

**Pitfalls to avoid:**
- Forgetting that |S_i−T_i|>1 is guaranteed, but distance 2 is even and feasible.
- Confusing “positive integer” with “≥0”; interior stamina must be ≥1, which the alternating assignment satisfies.
- Trying to solve per‑query with complex interval intersection logic; the global alternating assignment trivializes it.

## worker: Implement the solution: read N, M, Q, then M pairs
The solution uses the key insight: a single alternating edge weight assignment (+1, -1, +1, -1, ...) satisfies all even-length intervals simultaneously. Therefore, a set of people can be satisfied iff every person has an even distance between their start and end towns. We precompute a binary array indicating even distances, build a prefix sum for O(1) range queries, and answer each query by checking if all persons in the range have even distance.
