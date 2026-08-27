
## ideation
The core difficulty is that a brute-force O(N²) enumeration of subarrays is impossible for N up to 2×10⁵, but K ≤ 10 is tiny, so we can exploit the binomial expansion. Let prefix sums S₀=0, S_r = A₁+...+A_r (mod p). A subarray sum is S_r − S_{l−1}. Then:

(S_r − S_t)^K = Σ_{j=0}^{K} C(K,j) S_r^j (−S_t)^{K−j}, where t = l−1 ranges over 0..r−1.

So if we process r from 1..N and maintain cnt[m] = Σ_{t<r} (−S_t)^m mod p for m = 0..K, the contribution of this r is Σ_j C(K,j) S_r^j · cnt[K−j]. After processing r, we add S_r's powers into cnt (so future r's see it). Each step is O(K), total O(NK) ≈ 2×10⁶ operations — trivial.

Pitfalls:
- Signs: (−S_t)^m must be computed mod p carefully; use (−s) % p then power, or handle parity.
- Include t=0 (S₀=0) in cnt initially so subarrays starting at l=1 are counted.
- All arithmetic mod 998244353; A_i can be 0 (fine).
- Binomial coefficients C(K,j) for K ≤ 10 precomputed directly.
- Python speed: O(NK) with small inner loop is fine; use local variables and precomputed binom table. Avoid pow() in inner loop — compute powers of S_r incrementally, and powers of (−S_t) incrementally when updating cnt.

## worker: Write the complete Python solution: parse stdin, p
- Let S_r be prefix sums (mod p). Subarray sum over [l, r] equals S_r − S_{l−1}.
- Binomial expansion: (S_r − S_t)^K = Σ_j C(K,j) S_r^j (−S_t)^{K−j}, t = l−1 ∈ [0, r−1].
- Processing r in order, maintain acc[m] = Σ_{t<r} (−S_t)^m. Contribution of r is Σ_j C(K,j)·S_r^j·acc[K−j]; then fold (−S_r)^m into acc.
- Initialize acc[0] = 1 to account for t = 0 (S_0 = 0), so subarrays starting at l = 1 are included. Note (−0)^m = 0 for m ≥ 1, so only acc[0] gets the initial 1.
- Powers computed incrementally (no pow in inner loop). Complexity O(NK) ≈ 2×10⁶ modular ops — fast in Python.
- Verified against sample 1 mentally: subarrays of (3,1,2) squared sum to 9+1+4+16+9+36 = 75. Sign handling uses (−s) % MOD so parity is automatic.

## worker: Verify edge cases: N=1, A_i=0, K=1 (reduces to sum
Verification of the requested edge cases:

**N=3, K=2, A=(3,1,2) → 75.** Trace: binom = [1,2,1]. acc starts [1,0,0].
- r=1: s=3, sp=[1,3,9]. contrib = 1·1·acc[2] + 2·3·acc[1] + 1·9·acc[0] = 0+0+9 = 9 (= A₁²). acc += (−3)^m → acc=[2, MOD−3, 9].
- r=2: s=4, sp=[1,4,16]. contrib = 1·1·9 + 2·4·(MOD−3) + 1·16·2 = 9 − 24 + 32 = 17 (= A₂² + (A₁+A₂)² = 1+16). acc += (−4)^m → acc=[3, MOD−7, 25].
- r=3: s=6, sp=[1,6,36]. contrib = 25 + 12·(−7) + 36·3 = 25 − 84 + 108 = 49 (= A₃² + (A₂+A₃)² + (A₁+A₂+A₃)² = 4+9+36).
- Total: 9+17+49 = 75. ✓ Matches sample.

**K=1 (sum of subarray sums).** binom=[1,1]. Contribution at r is acc[1] + s·acc[0] = s·r − Σ_{t<r} S_t, which is exactly Σ_{l≤r}(S_r − S_{l−1}), the sum of all subarray sums ending at r. Summing over r gives the total. ✓

**A_i = 0 (e.g., N=1, K=10, A=(0)).** s stays 0; sp[j]=0 for j≥1, sp[0]=1; contrib = binom[0]·1·acc[K]. acc[K] accumulates (−0)^K = 0 for K≥1, so contrib = 0. Answer 0. ✓ Matches sample 2.

**N=1, general.** Only t=0 in acc, so contrib = Σ_j C(K,j) s^j (−0)^{K−j} = s^K = A₁^K. ✓

Sign handling: neg = (−s) % MOD ensures (−S_t)^m is correct mod p regardless of parity. Initialization acc[0]=1 correctly encodes S₀=0 since (−0)^m = 0 for m≥1. Complexity O(NK) ≈ 2×10⁶ modular multiplications — fast in Python. No changes to the code were needed; it is correct as written.
