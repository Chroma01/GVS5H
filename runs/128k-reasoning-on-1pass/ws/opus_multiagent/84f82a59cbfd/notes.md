
## ideation
**Core reduction.** "Every prime exponent is even" ⟺ N is a perfect square, N = m². And the set of distinct primes of m² equals that of m, so the condition "exactly 2 distinct prime factors" becomes ω(m) = 2. Hence:

> N is a 400 number ⟺ N = m² with ω(m) = 2.

So for a query A: let x = isqrt(A); answer = (largest m ≤ x with ω(m) = 2)².

**Bounds.** A ≤ 10¹² ⟹ x ≤ 10⁶. So we only need ω(m) for m ≤ 10⁶ — tiny sieve. Smallest valid m is 6 (6² = 36), matching the guarantee A ≥ 36 always has an answer. isqrt(10¹²) = 10⁶ exactly, and 10⁶ = 2⁶·5⁶ has ω = 2, consistent with sample output 10¹² → 10¹².

**Algorithm.**
1. LIM = 10⁶. Build `omega` array (bytearray of size LIM+1). Standard sieve: for p from 2..LIM, if omega[p] == 0 then p is prime, so for j in range(p, LIM+1, p): omega[j] += 1. This is O(N log log N); in Python the inner loop should be done with slice assignment tricks if possible — but += on a slice isn't directly vectorizable with bytearray. Options: numpy (`omega[p::p] += 1` on an int8/uint8 numpy array) — much faster. Careful with dtype overflow: max ω for m ≤ 10⁶ is 7 (2·3·5·7·11·13·17 = 510510), so uint8 is safe.
2. Build `best` array of size LIM+1: best[x] = largest m ≤ x with omega[m] == 2, computed by a forward running max (prefix scan). Values below 6 are unused/0 (queries guarantee x ≥ 6). With numpy: `mask = (omega == 2)`; `idx = np.where(mask, np.arange(LIM+1), 0)`; `best = np.maximum.accumulate(idx)`.
3. Per query: x = isqrt(A) (use math.isqrt — exact for ints, no float error), print best[x]**2. Watch: numpy int32/int64 squaring — cast to Python int before squaring to avoid overflow (best[x] up to 10⁶, square is 10¹², fits int64, but if array is int32 the square overflows!). Safest: convert to Python int, or use int64 dtype.

**Pitfalls to watch.**
- Using `int(A**0.5)` instead of `math.isqrt` → float precision errors near 10¹². Must use isqrt (or isqrt + correction).
- Q up to 2·10⁵ → need `sys.stdin.buffer.read().split()` and `'\n'.join(...)` output; per-line input()/print() may TLE.
- numpy int32 overflow when squaring (see above).
- Don't confuse ω (distinct primes) with Ω (with multiplicity): m = 12 = 2²·3 has ω = 2, and 144 = 2⁴·3² is indeed a valid 400 number — so multiplicity in m is fine.
- Edge: answer for A = 36..47 is 36; check best[6] = 6.
- If avoiding numpy (in case it's unavailable), the pure-Python sieve over 10⁶ with byte increments is ~2.8M operations for primes... actually sum over primes of N/p ≈ N ln ln N ≈ 3·10⁶ increments — acceptable (~1–2 s) but numpy is safer. Alternative pure-Python speedup: only need m with exactly 2 distinct primes; could instead compute smallest-prime-factor sieve, or mark counts using a list and `for` loops. Another trick: build `omega` via bytes and use a second bytearray trick — but simplest fallback is fine.

**Alternative (no full sieve):** for each query, walk down from x checking ω(m) = 2 by trial division up to 10³. Gaps between consecutive ω=2 numbers are small, but worst case per query cost × 2·10⁵ queries is risky. Precomputation is clearly better since domain is only 10⁶.

## worker: Write the complete final Python program: try numpy
- Reduction: all prime exponents even ⟺ N is a perfect square N = m²; distinct prime set of m² equals that of m, so condition is ω(m) = 2. Thus answer = (largest m ≤ isqrt(A) with ω(m)=2)².
- Since A ≤ 10¹², m ≤ 10⁶. Sieve ω over [0,10⁶] with numpy (uint8; max ω is 7 for 510510, no overflow), using `omega[p::p] += 1` for each prime p (primes found by a boolean sieve first, avoiding 10⁶ numpy scalar reads).
- `best = maximum.accumulate(where(omega==2, arange, 0))` gives prefix largest valid m; converted with `.tolist()` to Python ints so squaring gives exact big-int results (no int32/int64 overflow) and indexing is fast for 2·10⁵ queries.
- Pure-Python bytearray fallback provided on ImportError (~3·10⁶ increments, acceptable).
- Uses `math.isqrt` (exact, no float error near 10¹²) and bulk stdin/stdout I/O.
- Sanity: 10¹² → isqrt=10⁶=2⁶·5⁶, ω=2 → 10¹²; 404 → isqrt=20, largest m≤20 with ω=2 is 20 (2²·5) → 400; 36..47 → 36; 123456789 → isqrt=11111, largest valid m = 11111 = 41·271 → 123454321.
