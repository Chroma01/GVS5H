
## ideation
Core difficulty: N up to 1e6 and values up to 1e6 rule out O(N^2) or O(N*MAX) per-element scans. The condition B-A = C-B is equivalent to A + C = 2B, i.e., counting 3-term arithmetic progressions in a subset of [1, 1e6].

Key insight: Let f be the indicator array of S (length M = 1e6+1). The convolution g = f * f gives g[2B] = number of ordered pairs (x, y) in S with x + y = 2B. This includes the pair (B, B) once, plus pairs (A, C) with A ≠ C counted twice (as (A,C) and (C,A)). So the number of fine triplets with middle B is (g[2B] - 1) / 2. Total answer = sum over B in S of (g[2B] - 1) // 2.

Convolution via FFT: use numpy's rfft/irfft with size = next power of two ≥ 2M+1. Rounding: values are integers, so round irfft output to nearest int. Sizes: f has up to 1e6+1 entries; convolution length ~2e6+1; FFT size ~2^21 = 2097152, which is fine memory-wise with float64 (each array ~16 MB complex128 for rfft output ~8 MB). Precision: values up to 1e6, coefficients 0/1, convolution values up to 1e6 — double precision FFT rounding is safe at this size.

Pitfalls:
- Must subtract the (B,B) self-pair and divide by 2 to avoid double counting and ordering.
- Only sum over indices 2B where B ∈ S (equivalently where f[B]=1).
- Ensure integer rounding (np.rint) and use int64 accumulation; answer can be up to ~C(1e6,3)/... actually max number of APs in [1..1e6] full set is about 2.5e11, so need 64-bit (Python int fine).
- Read input fast (sys.stdin.buffer.read).
- Edge cases: N < 3 → answer 0 naturally.

Alternative considered: number-theoretic transform for exactness, but numpy FFT with rounding is standard and reliable here.

## worker: Write the complete Python solution: parse input, b
- The fine triplet condition B−A = C−B is equivalent to A + C = 2B, i.e., counting 3-term arithmetic progressions in S.
- Built indicator array f of size max(S)+1 and computed its self-convolution g = f * f via numpy's real FFT with length L = next power of two ≥ 2*maxv+1 (≤ 2^21 for maxv = 1e6, well within memory/time limits).
- For each B ∈ S, g[2B] counts ordered pairs (x, y) ∈ S² with x + y = 2B: the self-pair (B, B) once and each unordered {A, C} (A ≠ C) twice. Summing g[2B] over all B ∈ S and subtracting N (the self-pairs) then dividing by 2 yields the number of fine triplets.
- Rounding with np.rint is safe: coefficients are 0/1 and convolution values ≤ 1e6, far below double-precision FFT error thresholds at this size.
- Answer can be as large as ~2.5e11 (full set {1..1e6}), accumulated in int64 / Python int — no overflow.
- Complexity: O(M log M) time with M ≈ 2^21, O(M) memory. Handles N < 3 trivially (answer 0).
