
## ideation
The problem asks to count 3-term arithmetic progressions (A, B, C) with A < B < C, all in S. Equivalently, for each B ∈ S, count d ≥ 1 such that B-d ∈ S and B+d ∈ S.

Key observations:
- N ≤ 10^6, values ≤ 10^6, so a boolean presence array of size 10^6+1 is feasible.
- Naive per-B iteration over d is O(M²) worst case (~5×10^11 for dense sets) — too slow.
- The count for each B equals (number of ordered pairs (x,y) ∈ S×S with x+y = 2B, minus the self-pair (B,B)) / 2. This is exactly a convolution of the indicator array with itself.
- Convolution via FFT: array size 2M+1 ≈ 2×10^6+1, next power of two = 2^21 ≈ 2.1M. numpy's FFT handles this in well under a second.
- Precision: coefficients up to N = 10^6; double-precision FFT rounding errors are ~1e-3 relative at this size, so rounding to nearest integer is safe. Could also use NTT or split-FFT, but plain numpy rfft suffices.
- Answer = Σ_{B ∈ S} (conv[2B] − 1) / 2. Each fine triplet has a unique middle B, so no double counting.
- Edge cases: N < 3 → answer 0 naturally; values at boundaries (B-d < 1 or B+d > max) handled automatically since conv only counts existing elements.

Pitfalls:
- Must subtract the self-pair (B,B) before dividing by 2.
- Use int64 for the answer (max answer ~ (10^6)²/8 ≈ 1.25×10^11, exceeds 32-bit).
- Memory: FFT of size 2^21 complex128 ≈ 32 MB — fine.
- Reading input fast (sys.stdin.buffer.read).

## worker: Implement the complete solution: parse input, buil
- A fine triplet is a 3-term arithmetic progression. For each middle element B ∈ S, the number of valid (A, C) pairs equals the number of d ≥ 1 with B−d ∈ S and B+d ∈ S.
- This count equals (number of ordered pairs (x, y) ∈ S×S with x+y = 2B, minus the self-pair (B,B)) / 2, which is coefficient 2B of the self-convolution of the indicator array.
- Primary path: numpy FFT (rfft/irfft) with size 2^21 (since 2·max_v+1 ≤ 2·10^6+1). Coefficients ≤ N = 10^6, so double-precision rounding to nearest integer is safe. Answer fits in int64 (max ≈ 1.25×10^11).
- Fallback path (if numpy unavailable): exact pure-Python NTT modulo 998244353. Coefficients ≤ 10^6 < MOD, so values are exact. Slower but correct.
- Each fine triplet has a unique middle B, so summing over B ∈ S counts each triplet exactly once.
- Edge cases: N < 3 → 0; boundary values handled automatically since convolution only includes existing elements.

## worker: Verify the solution correctness: trace through sam
**Verification of correctness:**

**Sample 1 trace:** S = {8,3,1,5,2}, max_v = 8. Indicator f has 1s at {1,2,3,5,8}. Convolution coefficients at 2B for B ∈ S:
- B=1: conv[2] = pairs summing to 2 = (1,1) only → 1. (1−1)/2 = 0 ✓
- B=2: conv[4] = (1,3),(3,1),(2,2) → 3. (3−1)/2 = 1 → triplet (1,2,3) ✓
- B=3: conv[6] = (1,5),(5,1),(3,3) → 3. (3−1)/2 = 1 → triplet (1,3,5) ✓
- B=5: conv[10] = (2,8),(8,2),(5,5) → 3. (3−1)/2 = 1 → triplet (2,5,8) ✓
- B=8: conv[16] = (8,8) → 1. (1−1)/2 = 0 ✓

Total = 3, matching expected output. ✓

**FFT precision analysis:** Coefficients are bounded by N ≤ 10⁶. For a double-precision FFT of size 2²¹, the relative error is O(ε·log n) where ε ≈ 2.2×10⁻¹⁶, giving absolute error well below 10⁻³ for values up to 10⁶. Rounding to nearest integer via `np.rint` is therefore safe. The convolution values are exact integers mathematically, so any error < 0.5 suffices — we have huge margin.

**Fallback NTT correctness:** Modulus 998244353 = 119×2²³+1 is a standard NTT prime with primitive root 3. Since coefficients ≤ 10⁶ < MOD, values are exact (no wraparound). The bit-reversal permutation and iterative butterfly loops follow the standard CP-algorithms implementation. The inverse transform multiplies by n⁻¹ mod MOD. Pointwise squaring then inverse NTT yields the self-convolution. The `(fa[2b] − 1) // 2` formula is identical to the FFT path.

**Edge cases validated:**
- N < 3: early return prints 0. ✓
- N = 3 with valid AP: e.g., {1,2,3} → B=2 gives conv[4]=3, (3−1)/2=1. ✓
- N = 3 without AP: e.g., {1,2,4} → B=2: conv[4]=(1,?)... pairs summing to 4: (2,2) only → (1−1)/2=0; B=1: conv[2]=1→0; B=4: conv[8]=(4,4)→0. Total 0. ✓
- Single element at value 1: max_v=1, size=4, works fine. ✓
- Dense set (all values 1..10⁶): answer ≈ Σ min(B−1, 10⁶−B) ≈ 2.5×10¹¹, fits in Python int (arbitrary precision) and int64 for numpy path. ✓
- Duplicate indices in `f[np.array(S)] = 1.0`: S has distinct elements per constraints, so no issue. ✓

**Complexity:** FFT path is O(M log M) with M = 2²¹, running in well under 1 second. NTT fallback is O(M log M) in pure Python — slower (~10-20s) but only used if numpy is unavailable.
