
## ideation
Core difficulty: `N` and value domain `M=max(S)` are both up to `1e6`, so `O(N^2)` pair enumeration is impossible, and the answer itself can be `Θ(M^2)` (e.g. `S={1..1e6}` gives ~`2.5e11` triplets), so we must count without enumerating and use 64-bit/Python-big-int accumulation.

Key reformulation: `(A,B,C)` fine ⇔ `A+C=2B` with `A<B<C`. If `P` is the 0/1 indicator over values, self-convolution `Q=P*P` gives `Q[k]` = ordered pairs `(x,y)` with `x+y=k`. For a present `B`, `Q[2B]` includes the diagonal `(B,B)` once and each valid `{A,C}` twice (`(A,C)` and `(C,A)`), so contribution is `(Q[2B]-1)//2`. Answer = sum over `B in S`.

Main pitfalls:
- FFT rounding: coefficients up to `1e6`, transform length ~`2^21`; double FFT is usually OK but worst-case all-present is the stress case. Safer to use split-FFT (15-bit limbs) or NTT+CRT if precision is doubtful.
- Pure-Python NTT at `2^21` is too slow; rely on `numpy.fft` (rfft/irfft) if available, with an exact fallback.
- Index bound: need `Q` length at least `2*M+1`; `2B` max is `2M`.
- Diagonal handling: subtract exactly 1 only for present `B`; never count `A=C` (strict `A<B<C`).
- `N<3` ⇒ 0; distinctness guaranteed so no duplicate-value corrections beyond the diagonal.
- Memory: indicator/FFT arrays of size ~`2^21` complex are fine (~tens of MB).

## worker: Implement the complete solution: parse input, buil
- Reformulation: `(A,B,C)` fine ⇔ `A+C=2B`, `A<C`. With indicator `P` of `S`, self-convolution `Q=P*P` gives ordered pairs summing to `2B`, including the diagonal `(B,B)` once; each valid `{A,C}` pair appears twice. So each present `B` contributes `(Q[2B]-1)//2`.
- Built indicator over `0..max(S)`, padded to next power of two ≥ `2*max(S)+1` so index `2B ≤ 2M` is always valid.
- Convolution via `numpy.fft.rfft/irfft` (real FFT, ~2× faster than complex). Coefficients are ≤ N ≤ 1e6 with transform length ≤ 2^21; double-precision roundoff is far below 0.5, so `rint` recovers exact integers.
- Pure-Python iterative radix-2 FFT fallback included for environments without numpy (correct, though only practical for smaller sizes).
- Early return `0` for `N<3`. Answer can be ~2.5e11 (full set `1..1e6`), handled by Python big ints / int64.
- Verified logic against samples: `{1,2,3,5,8}` → contributions B=2:1, B=3:1, B=5:1 → 3.

## worker: Cross-check the convolution solution against an O(
- Cross-checked the counting identity against a hash brute force: for each `B`, iterate over present `A < B` and test whether `C = 2B - A` is present and `C > B`. This matches `(conv[2B] - 1) // 2` because `conv[2B]` counts ordered pairs `(x,y)` with `x+y=2B`, including the single diagonal `(B,B)` and counting each valid `{A,C}` twice.
- Random small cases used for comparison: `N <= 40`, values in `1..80`, many seeds; also shuffled duplicates-free sets, consecutive sets, sparse sets, and sets with no triplets. Edge cases checked: `N=1`, `N=2`, `{1,2,4}` -> `0`, `{1,2,3}` -> `1`, powers of two -> `0`, near-boundary case `{1,500000,999999}` -> `1`, and `{1,500000,1000000}` -> `0`.
- Sample verification by middle-element contributions:
  - Sample 1: `B=2,3,5` each contribute `1`, total `3`.
  - Sample 2: contributions by sorted middles are `1+2+1+0+1 = 5`.
  - Sample 3: contributions are `B=4:1`, `B=7:3`, `B=10:3`, `B=13:2`, `B=16:1`, total `10`.
- Complexity: FFT length is the next power of two at least `2*max(S)+1 <= 2,000,001`, so time is `O(M log M)` with `M <= 1e6`; memory is `O(M)`. The answer can be about `2.5e11` for `S={1..1e6}`, accumulated safely as a Python integer.
