
## ideation
Core difficulty: counting 3-term APs (A,B,C) with A<B<C, i.e., for each middle B, count d≥1 with B-d and B+d both in S. N and values up to 1e6, so per-element scanning of d is O(V^2) worst case (~2.5e11) — too slow. The right tool is convolution: with indicator array f over [0, V], conv = f*f gives conv[2B] = number of ordered pairs (x,y) in S with x+y = 2B. This includes the (B,B) diagonal term (exactly 1 since elements distinct) and counts (A,C) and (C,A) symmetrically. So for each B in S, valid pairs with A<C = (conv[2B]-1)/2. Answer = sum over B in S.

Implementation options in pure Python: FFT via numpy (np.fft.rfft on length ~2^21) is fast and numerically safe here because coefficient values ≤ N ≤ 1e6, well within double precision's 53-bit exactness after rounding. Fallback without numpy: NTT with iterative loops would be too slow in pure Python; alternative is a bucketed/hashing approach but worst case degrades. Numpy is typically available in AtCoder-style environments (this looks like an AtCoder problem). If numpy is unavailable, a PyPy-friendly alternative: iterate over pairs? That's O(N^2). Another pure-Python option: for each d, count B with B-d and B+d present — still O(V^2). So rely on numpy FFT; round with int(round()) via np.rint.

Pitfalls: (1) subtract the diagonal (B,B) term; (2) integer rounding errors — use np.rint and int64; (3) FFT size must be ≥ 2V+1; (4) memory: arrays of size 2^21 complex128 = ~32MB, fine; (5) reading input fast for N=1e6.

## worker: Write the complete Python solution: parse input, b
- A fine triplet is a 3-term arithmetic progression: for middle element B, count d ≥ 1 with both B−d and B+d in S.
- Built indicator array f over [0, V] (V = max(S) ≤ 1e6) and computed the self-convolution `conv = f * f` via numpy FFT (`rfft`/`irfft` with size = next power of two ≥ 2V+1).
- `conv[2B]` counts ordered pairs (x, y) ∈ S² with x + y = 2B. This includes the diagonal pair (B, B) exactly once (elements are distinct) and counts each (A, C) with A < C twice. Hence per B: `(conv[2B] − 1) // 2`; summed over all B ∈ S gives the answer.
- Coefficient values ≤ N ≤ 1e6, far below 2^53, so double-precision FFT with `np.rint` rounding is exact.
- Complexity: O(V log V) time (~2^21 FFT), well within limits; memory ~tens of MB.
- Included a pure-Python O(Σ min(B−1, V−B)) fallback in case numpy is unavailable (correct but only fast enough for sparse/small cases).
