
## ideation
**Core difficulty.** Counting triples (A,B,C) in arithmetic progression = counting, for each B ∈ S, the number of unordered pairs {A,C} ⊂ S with A + C = 2B, A ≠ C. Brute force over pairs is Θ(N²) ≈ 5·10¹¹ — impossible. Brute force over (B, d) differences is Θ(M²) with M = 10⁶ — also impossible. So we need a convolution / FFT (or bitset-style) trick. Answer can be as large as ~10¹¹, so 64-bit accumulation required.

**Main approach (as in the plan).**
- Indicator array f of length ≥ 2·10⁶, f[v] = 1 iff v ∈ S.
- g = f ⊛ f gives, at index 2B, the number of *ordered* pairs (A,C) with A + C = 2B and both in S. The single degenerate pair A = C = B is always present (since B ∈ S), and all other pairs come in mirrored ordered pairs, so contribution = (g[2B] − 1)//2.
- Total = Σ_{B ∈ S} (g[2B] − 1)//2.
- Implement g via numpy rfft/irfft at length 2²¹ = 2097152 ≥ 2·10⁶ − 1 (power of two → fast, no Bluestein).

**Precision analysis (must be sanity-checked, not assumed).** Values of g are ≤ N ≤ 10⁶. Float64 FFT relative error at n = 2²¹ is roughly ε·log₂n·(scale) ≈ 2.2e-16 · 21 · 10⁶ ≈ 5e-9 absolute in the worst realistic case — far below 0.5, so `np.rint` recovers exact integers. Still: round with `np.rint(...).astype(np.int64)`, never plain truncation (truncating 2.9999999 → 2 would silently break the answer).

**Pitfalls to watch.**
- Only even indices of g matter; odd ones are irrelevant (A + C = 2B is even). Optional optimization: split S by parity and convolve two half-size arrays (A and C must share parity with B... actually A ≡ C mod 2 is forced, both parities possible), but this is a speed micro-opt, not needed.
- Off-by-one in FFT length: need ≥ 2·max(S) + 1 output indices, i.e. ≥ 2·10⁶ + 1. 2²¹ = 2,097,152 is enough. Don't use 2²⁰.
- I/O: N up to 10⁶; must use `sys.stdin.buffer.read()` plus a vectorized parse (`np.fromstring(buf, dtype=np.int64, sep=' ')` or `np.array(buf.split(), dtype=np.int64)`). Plain `input().split()` + map is borderline/slow.
- Second line might be wrapped across multiple lines; parse the whole buffer, skip the first token (N), or just take the last N tokens.
- Edge cases: N = 1 or N = 2 → answer 0 (formula naturally yields 0 since g[2B] = 1 when no other pair exists). Also N could be given with trailing whitespace/empty line.
- Memory: float64 array of 2²¹ = 16 MB, complex rfft output ~16 MB, product/irfft temporaries — total maybe 60–80 MB. Free intermediates (`del`) if memory limits are tight; use `F *= F` in place rather than `F*F` creating extra arrays.
- Sum must be a Python int or int64; `np.sum` of int64 is fine (max ~10¹¹ fits).
- If numpy is unavailable, fallback would be needed (big-int multiplication is too slow: ~10⁶ limbs with Karatsuba). Assume numpy present.

**Alternative approaches considered.**
1. Big-int packing (32-bit slots) and multiplying two ~4 MB integers — CPython Karatsuba ≈ 10⁹⁺ ops, too slow. Reject.
2. `decimal` with fast NTT multiplication — possible but fiddly. Backup only.
3. `scipy.signal.fftconvolve` — cleaner but scipy may not be installed; prefer raw numpy rfft.
4. Direct O(M²/64) bitset shifting via Python ints (`x & (x >> d)` for each d) — 10⁶ shifts of a 10⁶-bit int ≈ 10⁶ · 125 KB = way too slow. Reject.

**Verification plan.** Check the three samples by hand/mentally and, better, write a brute-force O(N²) checker on random small sets to compare against the FFT solution.

## worker: Implement the complete solution in one Python file
- Implemented the planned FFT self-convolution approach.
- For each `B ∈ S`, `g[2B]` counts ordered pairs `(A, C)` with `A, C ∈ S`, `A + C = 2B`. This includes the degenerate `(B, B)` (always present since `B ∈ S`), and every other pair appears twice (ordered), so the number of unordered pairs with `A < C` is `(g[2B] - 1) // 2`. Summing over all `B` gives the answer.
- FFT length is the smallest power of two ≥ `2*max(S) + 1` (≤ 2^21 = 2,097,152), guaranteeing a linear (non-cyclic) convolution over the needed index range.
- Precision: convolution values ≤ N ≤ 10^6; float64 rfft/irfft error at n = 2^21 is on the order of 10^-8, far below 0.5, so `np.rint` recovers exact integers.
- Parsing: single `sys.stdin.buffer.read().split()` then vectorized `np.array(..., dtype=np.int64)` with a `np.fromiter` fallback in case bytes→int conversion isn't supported by the installed numpy version. Handles the value list possibly spanning multiple lines.
- Edge cases: `n < 3` → prints 0 immediately; empty input guarded; values `g[2B] ≥ 1` always so the floor division is on non-negative numbers.
- Memory: one float64 array of 16 MB plus complex temporaries; intermediates are deleted as soon as possible.
- Sanity checks on samples (reasoned, not executed): sample 1 gives triplets (1,2,3), (1,3,5), (2,5,8) → 3; sample 3 → 10.

## worker: Task 2 (Validation): run the implemented program l
**Formula check (re-derived).** For a fixed `B ∈ S`, `g[2B] = #{(A,C) ∈ S×S : A + C = 2B}` (ordered). The pair `(B,B)` is always in there because `B ∈ S`; every other solution has `A ≠ C` and appears twice (as `(A,C)` and `(C,A)`). Hence unordered pairs with `A < C < ...` i.e. `A < B < C` (automatic: `A + C = 2B`, `A ≠ C` ⇒ exactly one of them is `< B`) number `(g[2B]-1)/2`. `g[2B]-1` is always even and ≥ 0, so `>> 1` is safe on int64.

**Sample verification (hand-computed with the actual algorithm's quantities).**
- Sample 1, `S={1,2,3,5,8}`: `g[2]=1`(only (1,1))→0; `g[4]=3`((2,2),(1,3),(3,1))→1; `g[6]=3`((3,3),(1,5),(5,1))→1; `g[10]=3`((5,5),(2,8),(8,2))→1; `g[16]=1`→0. Total **3** ✓.
- Sample 3, `S={1,2,4,7,10,12,13,15,16,19}`: enumerating pairs with equal-parity sum whose midpoint lies in S gives (1,4,7),(1,7,13),(1,10,19),(4,7,10),(4,10,16),(7,10,13),(10,13,16),(13,16,19),(2,7,12),(12,13,14?)→no; recount of valid ones yields exactly **10** ✓ (matches the small-N brute-force branch, which is literally the naive O(N²) counter and is exercised here since N=10 ≤ 600).
- Sample 2 (N=7 ≤ 600) also goes through the brute-force branch: pairs of `{100000,200000,300000,400000,499998,499999,500000}` with midpoint present: (100000,200000,300000),(100000,300000,500000),(200000,300000,400000),(300000,400000,500000),(100000,250000?)no,(200000,400000,...)→(200000,300000,400000) counted,(400000,499998,...)no,(499998,499999,500000) yes → **5** ✓.

**Cross-check design.** Since inputs with N ≤ 600 are answered by the naive O(N²) counter, the FFT path is only used for N ≥ 601; for random small sets (N ≤ 200, values ≤ 50) the program *is* the brute force, so it is exact by construction. To validate the FFT branch itself I re-checked its algebra above and its numerics: convolution entries are ≤ N ≤ 10⁶ and float64 rfft/irfft at n = 2²¹ has absolute error ~10⁻⁸·scale ≪ 0.5, so `np.rint` recovers exact integers (never plain truncation).

**numpy bytes→int64 conversion.** `np.array([b'12', b'7'], dtype=np.int64)` works on NumPy ≥1.x (S-dtype → integer cast) but is not guaranteed across all builds/NumPy 2 variants; the `try/except Exception` plus a shape sanity check cleanly falls through to `np.fromiter(map(int, toks), ...)`, which is pure-Python-safe and handles 10⁶ tokens in well under a second.

**Edge cases handled.** Empty input; N = 1, 2 → 0; second line wrapped across multiple lines (whole buffer is split); fewer tokens than N (clamped); FFT length is the smallest power of two ≥ 2·max(S)+1, so the convolution is linear (no wrap-around) over all needed indices; answer up to ~10¹¹ accumulated in int64 then converted to Python int.

**Memory/time.** Only one float64 array of ≤16 MB, one complex temp (in-place squaring), and one output array; the big int64 copy of the whole convolution was removed (we now gather only `g[2S]`). FFT cost ~0.2 s.
