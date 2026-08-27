
## ideation
Core difficulty: N up to 1e18 rules out brute force over x or y. The factorization N = (x-y)(x²+xy+y²) reduces the problem to a one-dimensional search over d = x-y.

Key observations:
- d = x-y ≥ 1 and d must divide N.
- x²+xy+y² = 3y² + 3dy + d² > d², so N > d³, hence d < N^(1/3) ≤ 10^6. So at most ~1e6 candidate d values.
- For each d dividing N: need 3y² + 3dy + d² = N/d. Discriminant: Δ = 9d² - 12(d² - N/d) = 12N/d - 3d². Need Δ ≥ 0, perfect square, and y = (-3d + √Δ)/6 a positive integer.

Approach options:
1. Enumerate d from 1 to cbrt(N), check d | N, then discriminant check. O(N^(1/3)) = 1e6 iterations — fine in Python if kept lean (integer ops, isqrt).
2. Enumerate divisors of N via factorization — factoring 1e18 is harder (need Pollard Rho); unnecessary since option 1 is already fast enough.

Pitfalls:
- Integer cube root of N: use round(N ** (1/3)) carefully or integer adjustment loop to avoid floating-point error at 1e18 (float has 53-bit mantissa; N^(1/3) ≈ 1e6 so float error ~1e-10 relative — could be off by one near boundaries; safer to compute integer cbrt via adjustment).
- Must check y > 0 (strictly positive) and x = y + d.
- Δ must be a perfect square AND (-3d + √Δ) divisible by 6 AND result positive.
- Note √Δ > 3d is required for positive y, which is equivalent to Δ > 9d², i.e., N/d > 3d²... actually just check y > 0 directly.
- Sample 2: N=1, d=1 gives 3y²+3y+1=1 → y=0, not positive → -1. Correct.
- Performance: 1e6 iterations with isqrt each — isqrt on ~60-bit numbers is fast; total should run well under a second or two in Python.

## worker: Write the complete Python solution: read N from st
- Factorization: N = x³ − y³ = (x−y)(x²+xy+y²). Let d = x−y ≥ 1. Then x²+xy+y² = 3y² + 3dy + d² > d², so N > d³, i.e., d < N^(1/3) ≤ 10⁶. Hence enumerating d from 1 to cbrt(N) covers all possible solutions.
- For each d dividing N, solve 3y² + 3dy + d² = N/d. Discriminant Δ = 12(N/d) − 3d² must be a non-negative perfect square, and y = (√Δ − 3d)/6 must be a positive integer.
- Integer cube root computed via float approximation then adjusted with exact integer loops (safe against floating-point error at N = 10¹⁸).
- Complexity: O(N^(1/3)) = at most 10⁶ iterations, each doing a mod and an isqrt on ≤60-bit integers — runs in well under a second.
- Verified logic against samples: N=397 → d=1 gives Δ = 12·397 − 3 = 4761 = 69², y = (69−3)/6 = 11, x = 12 ✓. N=1 → d=1 gives y=0, rejected → -1 ✓. N=39977273855577088 → finds (342756, 66212) ✓.
- Final verification `x³ − y³ == N` guards against any edge-case arithmetic slip.
