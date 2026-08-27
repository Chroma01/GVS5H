
## ideation
Core difficulty: count 3-term arithmetic progressions (A, B, C) with all elements in S, N up to 10^6, values up to M = 10^6. A naive per-center scan over all offsets is O(N·M) worst case (e.g., S = {1..10^6} gives ~5·10^11 checks), far too slow. Need an O(M log M) approach.

Key insight: (A, B, C) is fine iff A + C = 2B with A ≠ C (A < B < C then follows from A ≠ C and the sum condition). So for each B ∈ S, the number of valid pairs (A, C) with A + C = 2B, A, C ∈ S, A ≠ C, equals (conv[2B] − 1) / 2 where conv = f * f and f is the 0/1 indicator array of S (the −1 removes the A = C = B self-pair; dividing by 2 because (A, C) and (C, A) both appear in the convolution). Answer = Σ_{B ∈ S} (conv[2B] − 1) / 2.

Approach options:
1. FFT convolution with numpy (np.fft.rfft): size next power of two ≥ 2M+1 ≈ 2^21 = 2097152. Coefficients up to 10^6, float64 rounding exact enough (values well below 2^53, and FFT error for these sizes is tiny; rounding to nearest int is safe). Fast and simple, but relies on numpy being available.
2. Pure-Python NTT (e.g., mod 998244353, iterative, precomputed roots): no dependency, guaranteed exact, but a hand-written NTT at size 2^21 in pure Python is ~2·10^7·(a few ops) — likely 10–30 s, risky for typical time limits. Mitigation: since coefficients ≤ N ≤ 10^6 < 998244353, a single modulus suffices.
3. PyPy-friendly alternative: for each B, iterate d over present values — still too slow in dense case.

Pitfalls:
- Must exclude the self-pair (B, B) and halve, otherwise overcount.
- Rounding FFT output: use int(round(real)); error is ≪ 0.5 for these magnitudes.
- Memory: arrays of size 2^21 complex128 ≈ 32 MB each — fine, but avoid extra copies.
- Input parsing speed for 10^6 integers: use sys.stdin.buffer.read().split().
- Edge cases: N < 3 → answer 0 naturally; ensure conv index 2B ≤ 2M within array bounds (size ≥ 2M+1).
- If numpy is unavailable, fall back plan needed; but most AtCoder-style environments (this looks like AtCoder ABC/typical) provide numpy in Python. Actually this problem is AtCoder (typical "fine triplet" style); numpy is allowed there.

## worker: Implement the complete solution: read input with f
- A fine triplet (A, B, C) with A < B < C and B − A = C − B is exactly a 3-term arithmetic progression, i.e., A + C = 2B with A ≠ C (the strict ordering follows automatically).
- Let f be the 0/1 indicator array of S over [0, M]. The convolution conv = f * f has conv[2B] = number of ordered pairs (x, y) ∈ S² with x + y = 2B. This includes the self-pair (B, B) exactly once (since elements are distinct) and counts each {A, C} pair twice (as (A, C) and (C, A)). Hence the number of fine triplets centered at B is (conv[2B] − 1) / 2, and the answer is the sum over all B ∈ S.
- Primary path: numpy FFT. f is float64 of length M+1, transform size = next power of two ≥ 2M+1 (≤ 2^21). Coefficients ≤ N ≤ 10^6 ≪ 2^53, and FFT rounding error at these sizes is far below 0.5, so np.rint gives exact integers. Complexity O(M log M), memory ~tens of MB.
- Fallback path (if numpy is missing): iterative radix-2 NTT modulo 998244353 with primitive root 3. Since every coefficient satisfies conv[k] ≤ N ≤ 10^6 < MOD, a single modulus yields exact results. Same formula applied afterward.
- Fast input via sys.stdin.buffer.read().split(); early exit 0 when N < 3.
- Verified mentally on samples:
  - Sample 1: S = {1,2,3,5,8}. Centers: B=2 → conv[4]=3 ({1,3},{2,2},{3,1}) → 1; B=3 → conv[6]=3 ({1,5},{3,3},{5,1}) → 1; B=5 → conv[10]=3 ({2,8},{5,5},{8,2}) → 1; B=1,8 → 0. Total 3. ✓
  - Sample 2: APs centered at 200000 (100000,300000), 300000 (100000,500000; 200000,400000), 400000 (300000,500000), 499999 (499998,500000) → 5. ✓
  - Sample 3: brute-force reasoning gives 10 triples. ✓
