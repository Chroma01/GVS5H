
## ideation
The core difficulty is that there are O(N²) subarrays, so we must avoid enumerating them. Since K ≤ 10 is tiny, we can expand (S_i - S_j)^K with the binomial theorem over prefix sums S. The answer is Σ_{0≤j<i≤N} (S_i - S_j)^K = Σ_{i} Σ_{t=0..K} C(K,t) S_i^{K-t} · Σ_{j<i} (-S_j)^t. The inner sums over j can be maintained incrementally as we sweep i from 0..N (including the empty prefix S_0 = 0, which accounts for subarrays starting at l=1).

Key details/pitfalls:
- Must include prefix index j=0 (S_0 = 0) in the aggregates before processing i=1.
- Sign handling: (-S_j)^t mod p; easiest to add (-1)^t · S_j^t mod p.
- Precompute binomial coefficients C(K,t) mod p (small, Pascal's triangle is fine).
- Per index i, compute powers S_i^0..S_i^K once and reuse for both the answer contribution and updating aggregates.
- Complexity O(N·K), memory O(K). Python speed is fine for N=2e5, K≤10 (~2M operations).
- A_i can be 0 and mod values; keep everything reduced mod p.

## worker: Implement the complete solution: fast stdin parsin
- Let prefix sums be S_0=0, S_i = A_1+...+A_i. Every subarray sum equals S_i - S_j for some 0 ≤ j < i ≤ N, so the required sum is Σ_{0≤j<i≤N} (S_i - S_j)^K.
- Binomial expansion: (S_i - S_j)^K = Σ_{t=0}^{K} C(K,t) S_i^{K-t} (-S_j)^t. For fixed i, the inner sum over j factors: Σ_t C(K,t) S_i^{K-t} · G[t], where G[t] = Σ_{j<i} (-1)^t S_j^t.
- Sweep i = 1..N maintaining S mod p and the aggregates G[0..K]. Initialize G[0]=1 (the empty prefix S_0=0 contributes only to t=0). At each step compute powers S^0..S^K once, add the contribution, then fold S into G with alternating signs.
- Complexity: O(N·K) time (~2×10^6 modular ops for worst case), O(K) extra memory. Binomial coefficients built by Pascal's triangle mod 998244353.
- Verified against sample 1 mentally: subarrays give 9+1+4+16+9+36 = 75. Sign handling uses (G[t] ± pw[t]) % MOD, and Python's % yields non-negative results, so no negative-mod issues.
