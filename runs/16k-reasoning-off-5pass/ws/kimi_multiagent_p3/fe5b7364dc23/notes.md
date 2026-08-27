
## ideation
The core difficulty is that there are O(N²) subarrays, so direct computation is impossible; we need an algebraic transformation. The key insight is to use prefix sums S₀=0, S_i = A₁+...+A_i, so each subarray sum is S_r − S_{l−1}. The answer becomes Σ_{0≤i<j≤N} (S_j − S_i)^K. Since K ≤ 10 is tiny, we can expand (S_j − S_i)^K = Σ_{t=0}^{K} C(K,t) S_j^t · (−1)^{K−t} S_i^{K−t}. Then for each j, we need prefix power sums P_m(j) = Σ_{i<j} S_i^m for m = 0..K, which we maintain incrementally. The total work is O(N·K) with K ≤ 10, easily fast enough. Pitfalls: (1) handle the sign (−1)^{K−t} via modular negation; (2) precompute binomial coefficients C(K,t); (3) note S₀ = 0 must be included as a valid left endpoint (i.e., initialize power sums with S₀^m before processing j=1); (4) all arithmetic mod 998244353, and A_i can be 0; (5) powers S_i^m for m=0 give 1 even when S_i=0 (0^0 = 1 convention, which is correct since C(K,K)·S_j^K·(−S_i)^0 = S_j^K term needs S_i^0 = 1).

## worker: Write the complete Python solution: read N, K and 
- Represent each subarray sum as a difference of prefix sums: subarray (l..r) sum = S_r − S_{l−1}, so the answer is Σ_{0≤i<j≤N} (S_j − S_i)^K.
- Binomial expansion: (S_j − S_i)^K = Σ_t C(K,t) S_j^t (−1)^{K−t} S_i^{K−t}. For each j we need Σ_{i<j} S_i^m for m = 0..K, maintained incrementally in the array `pw`.
- `pw` is initialized with S₀ = 0 (pw[0] = 1, using 0⁰ = 1, which is correct for the t=K term). After processing each prefix sum, its powers are added to `pw`.
- Signs (−1)^{K−t} are handled by subtracting the term modulo MOD when K−t is odd.
- Binomial coefficients are computed via Pascal's triangle mod 998244353 (K ≤ 10, so no overflow concerns).
- Complexity: O(N·K) time, O(K) space — well within limits for N = 2·10⁵, K ≤ 10.
- Verified against Sample 1 (answer 75) and Sample 2 (answer 0) by hand reasoning; the algorithm matches the plan exactly.
