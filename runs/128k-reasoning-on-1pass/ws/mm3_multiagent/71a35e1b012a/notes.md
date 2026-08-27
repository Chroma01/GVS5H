
## ideation
The problem is a set cover problem with special structure: each operation can cover either an interval (type 1) or the complement of that interval (type 2), each at cost 1. The goal is to cover all positions with minimum total cost.

Key observations:
- The sets covered by type 2 operations are complements of intervals, which are unions of at most two intervals.
- The intersection of the gaps (uncovered parts) of a set of type 2 operations is always a contiguous interval (or empty).
- Thus, after selecting a set T of type 2 operations, the uncovered region is G_T = [max L_i, min R_i] for i in T (if T is non-empty; if T is empty, the whole line is uncovered). The remaining positions must be covered by type 1 operations.
- The optimal T will have size at most 2, because if |T| ≥ 3, the same intersection can be achieved with a subset of T (by taking the operation with maximum L and the one with minimum R), and using extra operations only increases cost without benefit.
- Therefore, we only need to consider T of size 0, 1, or 2.

For each candidate gap [a,b] (including the whole line for T empty), we can compute the minimal cost to cover [a,b] with type 1 operations, excluding the operations used for type 2. This reduces to a classic interval covering problem, solvable greedily in O(K log K) time for K intervals.

The challenge is to efficiently evaluate the covering cost for many candidate gaps. Since M ≤ 2e5, enumerating all possible gaps (a,b) with a from L_i and b from R_i could be O(M^2) in the worst case. However, the number of candidate gaps is actually much smaller due to monotonicity: for a fixed left boundary a, the optimal right boundary b is either R_i (using operation i alone) or the smallest b achievable via a two-operation gap.

A more efficient approach uses dynamic programming on intervals. Define f([l,r]) as the minimal cost to cover [l,r]. The recurrence considers using each operation i as type 1 or type 2:
- Type 1: covers [max(l,L_i), min(r,R_i)], leaving two subintervals.
- Type 2: covers [l,r] \ [L_i,R_i], leaving the intersection as a subinterval.

The number of distinct subintervals that appear is bounded by the number of distinct endpoints generated, which is O(M). We can compute f using memoization and a segment tree for range queries to find the best operation, achieving O(M log M) time.
