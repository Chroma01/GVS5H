
## ideation
**Core problem:** Compute, for each query (u,v), the sum over all (N-1)! parent sequences P of the distance between u and v in the random rooted tree T(P).

**Key observations:**
- In a random recursive tree (node i picks parent uniformly in {1,…,i-1}), the path from u to v (u<v) uses edge (k, parent(k)) iff removing it separates u and v, i.e., exactly one of {u,v} lies in the subtree of k.
- Subtree(k) ⊆ {k, k+1, …, N}, so for k > v, edge never used. For k = v, edge always used (v is endpoint). For u < k < v, edge used iff v is a descendant of k. For k = u, edge used iff v is NOT a descendant of u (and u ≥ 2, since no parent for 1).
- **Probability k is an ancestor of v** in random recursive tree on [N] (for k < v): equals **1/k**. Proof by recurrence A(v,k) = (1/(v-1))·Σ_{j=k}^{v-1} A(j,k) with A(k,k)=1, giving A(v,k) = 1/k for all v > k.

**Resulting formula** (u < v):
$$\text{Ans}(u,v) = (N-1)! \cdot \left[A_v + A_u \cdot \frac{u-1}{u} + \sum_{k=u+1}^{v-1} \frac{A_k}{k}\right] \pmod{998244353}$$

For u=1, the A_u term vanishes (A_1 undefined, and edge (1,parent(1)) doesn't exist), and the sum starts from k=2.

**Verification:** N=4, all A=1, query (1,4): (3)!·[1 + 1/3 + 1/2] = 6·(11/6) = 11 ✓. Query (2,3), N=3: 2·[1 + 1·(1/2)] = 3 ✓.

**Pitfalls:**
- Must handle u=1 separately (no A_1, and term (u-1)/u = 0 naturally).
- Modular inverse of k needed (k up to N ≤ 2e5).
- Prefix sums: let S[t] = Σ_{k=2}^{t} A_k · inv(k). Then Σ_{k=u+1}^{v-1} A_k/k = S[v-1] - S[u].
- Precompute factorials and inv factorials; just need (N-1)! once.

## worker: (Omit, task complete.)
The solution implements the formula derived in the planning section:
- Precompute modular inverses of 1..N using the standard O(N) recurrence.
- Build prefix sums S[t] = Σ_{k=2}^{t} A_k · k⁻¹ mod MOD.
- Precompute (N-1)! mod MOD.
- For each query (u, v) with u < v:
  - inner = A_v + (S[v-1] − S[u]) + A_u·(u−1)/u  (the last term is 0 for u=1)
  - answer = (N−1)! · inner mod MOD.

This is O(N + Q) after O(N log MOD) for modular exponentiation not needed since inverses are computed in O(N).
