
## ideation
Core difficulty: N up to 2e5, K ≤ 10. Need sum over all subarrays of (subarray sum)^K mod p=998244353. Direct O(N^2) impossible.

Key identity: Let prefix sums S_0=0, S_r = A_1+...+A_r (mod p). Subarray sum (l..r) = S_r - S_{l-1}. Answer = Σ_{0≤a<b≤N} (S_b - S_a)^K.

Binomial expansion: (S_b - S_a)^K = Σ_{j=0}^{K} C(K,j) S_b^{K-j} (-S_a)^j = Σ_j C(K,j)(-1)^j S_b^{K-j} S_a^j.

So answer = Σ_{b=1}^{N} Σ_{j=0}^{K} C(K,j)(-1)^j S_b^{K-j} · (Σ_{a=0}^{b-1} S_a^j).

Maintain running prefix power sums P_j = Σ_{a=0}^{b-1} S_a^j for j=0..K. For each b, compute contribution Σ_j C(K,j)(-1)^j S_b^{K-j} P_j, then add S_b^j into P_j for all j. O(NK) time, O(K) memory. K ≤ 10 so trivially fast.

Pitfalls:
- Sign (-1)^j: use modular subtraction or precompute sign = p-1 when j odd.
- Binomial coefficients C(K,j) computed exactly (small integers), then mod.
- Powers S_b^e for e=0..K: compute incrementally (pow0=1, pow_e = pow_{e-1} * S mod p). Note 0^0 = 1 convention is correct here since binomial expansion uses S^0 = 1 even when S=0.
- A_i can be 0; S can be 0; fine.
- Mod negative handling in Python: % p yields non-negative, so just do arithmetic with modulo and subtract carefully.
- Answer must be mod p; keep everything reduced.

Alternative approaches considered: polynomial/FFT-based (overkill), generating function with formal power series (unnecessary given K ≤ 10). The O(NK) DP is clearly sufficient: 2e5 * 11 ≈ 2.2e6 ops.

Verification with sample 1: A=(3,1,2), K=2. S = [0,3,4,6]. Pairs: (3)^2+(4)^2+(6)^2+(1)^2+(6)^2+(2)^2? Wait subarray sums: 3,1,2,4,3,6 → squares 9+1+4+16+9+36=75. ✓ matches.

## worker: Implement the full Python solution: read N, K and 
- Identity used: answer = Σ_{0≤a<b≤N} (S_b − S_a)^K where S_t are prefix sums mod p.
- Binomial expansion: (S_b − S_a)^K = Σ_j C(K,j)(−1)^j S_b^{K−j} S_a^j. For each b we need P[j] = Σ_{a<b} S_a^j, maintained incrementally.
- Initialization P[0]=1 accounts for S_0 = 0 (0^0 = 1 convention, consistent with the expansion).
- Per element: compute powers S^0..S^K in O(K), contribution in O(K), update P in O(K). Total O(NK) ≈ 2.2×10^6 operations — well within limits.
- Sign handled by subtracting terms for odd j; final `% MOD` keeps result non-negative (Python modulo is safe for negatives anyway).
- Verified logic against sample 1 mentally: subarray sums 3,1,2,4,3,6 → squares sum to 75.
