
## ideation
Core difficulty: N up to 10^18 means we cannot iterate over x or y directly. The key algebraic step is factoring x³ − y³ = (x−y)(x²+xy+y²). Setting d = x−y ≥ 1 turns the problem into: find a divisor d of N such that the quadratic 3y² + 3dy + (d² − N/d) = 0 has a positive integer solution y.

Key bounds: since x²+xy+y² > (x−y)² = d² (because x²+xy+y² = (y+d)² + (y+d)y + y² = 3y²+3dy+d² > d²), we need d² < N/d, i.e., d³ < N, so d < N^(1/3) ≤ 10^6. This means we only need to enumerate divisors of N that are below ~10^6, which can be done by simple trial division up to N^(1/3) (about 10^6 iterations — cheap). No need for full factorization.

For each candidate divisor d with d³ < N: compute m = N/d, discriminant D = 12m − 3d² = 3(4m − d²). Need D ≥ 0 (guaranteed if d³ < N... actually d³ < N ⟺ d² < N/d = m ⟺ 4m − d² > 3m > 0, yes positive). Then y = (−3d + √D)/6 must be a positive integer: check D is a perfect square, s = isqrt(D), s² == D, (s − 3d) > 0, and (s − 3d) % 6 == 0. Also note s ≡ 3d (mod 6) condition: since D = 3(4m−d²), parity/divisibility checks just fall out of the mod-6 test.

Pitfalls:
- Integer cube root / loop bound: iterate i from 1 while i*i*i < N... but careful: we need divisors d with d³ < N strictly (if d³ = N then m = d², D = 9d², s = 3d, y = 0 — not positive, so exclude; indeed y=0 not allowed). Loop i while i³ < N and check N % i == 0.
- Sample 2: N=1, no d with d³<1 exists, output -1. Good.
- Use math.isqrt for exact big-integer square roots (Python handles big ints natively).
- Edge: also must double check y ≥ 1 strictly.
- Overflow is not an issue in Python.
- Complexity: ~10^6 iterations of modulo — fine.

## worker: Write the complete Python solution: read N from st
- Factored x³ − y³ = (x−y)(x²+xy+y²). With d = x−y ≥ 1 and x = y+d, the equation becomes 3y² + 3dy + d² = N/d, so d must divide N.
- Since x²+xy+y² = 3y²+3dy+d² > d² for y ≥ 1, we need d³ < N, i.e., d < N^(1/3) ≤ 10⁶. Trial division up to that bound is ~10⁶ iterations — trivially fast.
- For each divisor d with d³ < N: discriminant D = 12(N/d) − 3d² must be a perfect square s², and y = (s − 3d)/6 must be a positive integer. Checked via math.isqrt, positivity, and mod-6 test, plus a final direct verification of x³ − y³ = N for safety.
- N=1: no d with d³ < 1 exists, loop doesn't run, prints -1. Sample 1: d=1 divides 397, D = 12·397 − 3 = 4761 = 69², y = (69−3)/6 = 11, x = 12. ✓

## worker: Sanity-check edge cases mentally: N=1 → -1 (loop b
- Sanity checks:
  - **N = 1**: condition `d*d*d < 1` fails immediately for d=1, loop never runs → prints `-1`. ✓ (matches sample 2)
  - **d³ = N exactly** (e.g., N = 8, d = 2): excluded by strict `<`. Even if included, m = d², D = 12d² − 3d² = 9d², s = 3d, num = 0 → y = 0, rejected by `num > 0`. So no false positive with y = 0. ✓
  - **N = 397**: d=1 divides 397, m=397, D = 4764 − 3 = 4761 = 69², num = 69 − 3 = 66, y = 11, x = 12 → prints `12 11`. ✓ (matches sample 1)
  - **N = 39977273855577088** (sample 3): expected (342756, 66212), d = 276544. Check: d³ ≈ 2.116×10¹⁶ < N ≈ 4.0×10¹⁶ ✓, and d ≤ N^(1/3) ≈ 341,999... wait, N^(1/3) ≈ (4×10¹⁶)^(1/3) ≈ 341,995, and d = 276,544 < that ✓, so the loop reaches it. The loop bound is ~3.4×10⁵ iterations here — fast. The discriminant/mod-6 logic yields y = 66212, x = 342756, and the final verification `x³ − y³ == N` guards against any arithmetic slip. ✓
  - **Loop bound worst case**: N = 10¹⁸ − 1 → N^(1/3) ≈ 10⁶, so at most ~10⁶ iterations of a modulo and occasional isqrt — runs in well under a second in CPython... actually ~10⁶ big-int modulos on ≤60-bit numbers is fine (~0.2–0.5 s).
  - **Correctness of bound**: x² + xy + y² = 3y² + 3dy + d² > d² for y ≥ 1, so N = d·(x²+xy+y²) > d³; hence any solution has d³ < N and the enumeration is complete.
  - **D > 0 vs D ≥ 0**: D = 0 would give y = −d/2 < 0 anyway; using `D > 0` is safe (and D=0 can't occur since D = 3(4m − d²) with m > d² from d³ < N... actually m > d² ⟹ 4m − d² > 3d² > 0, so D > 0 always inside the loop; the check is just belt-and-suspenders).
