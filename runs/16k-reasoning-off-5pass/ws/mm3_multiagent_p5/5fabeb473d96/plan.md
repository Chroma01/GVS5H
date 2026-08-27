For each possible parent sequence P (a permutation of edges forming a rooted tree), we sum the weighted distance between two query vertices u and v. The total sum over all (N-1)! trees can be computed by linearity of expectation: we compute the expected distance between u and v, then multiply by (N-1)! modulo MOD.

Key observations:
- For any vertex i (i ≥ 2), its parent is uniformly random among {1, 2, …, i-1} when averaging over all P.
- An edge (i, parent(i)) with weight A_i is on the path between u and v iff exactly one of u, v is in the subtree rooted at i (considering the path up to i’s parent). This probability depends on the relative positions in a "line" from 1 to i.

We can compute for each edge i the probability that it lies on the u–v path:
- If u and v are on the same side of i (both < i or both > i), probability = 0.
- If one of them is i and the other is on the opposite side, probability = 1/(i-1) (since parent(i) = i is the unique case connecting i to the rest).
- If u < i < v (or v < i < u), probability = 1/(i-1).

Therefore:
- If i is between u and v (i.e., min(u,v) < i < max(u,v)), contribution = A_i / (i-1).
- If i equals u or v, the edge from i to its parent contributes A_i / (i-1) (since parent must be the other endpoint).
- If i is outside [min(u,v), max(u,v)], contribution = 0.

The answer for query (u,v) is:
ans(u,v) = (N-1)! * ( sum_{i in [u,v] or [v,u], i ≠ 1} A_i / (i-1) )  (where i ranges over the closed interval between u and v, i ≥ 2).

For i = 1, there is no incoming edge, so it contributes 0.

We need to:
1. Precompute factorials up to N.
2. Build a prefix sum array for the values B_i = A_i * inv(i-1) mod MOD for i ≥ 2.
3. For each query (u,v), the sum is prefix[v] - prefix[u-1] (if u < v) times (N-1)!.

Time: O(N + Q) after O(N log MOD) for modular inverses.