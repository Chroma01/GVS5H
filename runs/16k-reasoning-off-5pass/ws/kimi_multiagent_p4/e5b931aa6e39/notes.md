
## ideation
Core math: x³ − y³ = (x−y)(x² + xy + y²) = N. Setting d = x−y ≥ 1 and x = y+d:
- x² + xy + y² = 3y² + 3dy + d²
- So N = d·(3y² + 3dy + d²), meaning d | N and 3y² + 3dy + d² = N/d.

Key bound: since x² + xy + y² > d² (because x > d when y ≥ 1... actually x = y+d > d, so x² > d²), we get N = d·(x²+xy+y²) > d³, hence d < N^(1/3) ≤ 10^6 for N ≤ 10^18. So enumerating d from 1 to ~10^6 is feasible in Python (10^6 iterations, each cheap: a modulo check, and only for divisors a square-root computation).

Solving the quadratic: 3y² + 3dy + (d² − N/d) = 0.
Discriminant: Δ = 9d² − 12(d² − N/d) = 12·N/d − 3d². Need Δ ≥ 0 and a perfect square, and y = (−3d + √Δ)/6 a positive integer.

Pitfalls:
- Must use integer cube root carefully (compute integer cube root of N, adjust with while loops to avoid float inaccuracy at 10^18; float cube root can be off by 1).
- Integer square root via math.isqrt (exact).
- Check y > 0 (strictly positive) and verify the equation to be safe.
- N=1: d=1 gives Δ = 12−3 = 9, √Δ=3, y = (−3+3)/6 = 0, not positive → correctly outputs -1.
- Efficiency: 10^6 iterations with `%` and occasional isqrt is fine (~0.5–1s in Python).
- Edge: d must divide N; also Δ must be non-negative before isqrt.
- Alternative approach: enumerate divisors of N directly, but factoring 10^18 is harder; simple d-loop is better.

## worker: Write the complete Python solution: read N from st
- Factored x³ − y³ = (x−y)(x² + xy + y²). With d = x−y ≥ 1 and x = y+d, the second factor becomes 3y² + 3dy + d², so N = d·(3y² + 3dy + d²).
- Bound: x² + xy + y² > x² > d² (since x = y+d > d), so N > d³, i.e., d < N^(1/3) ≤ 10⁶. Enumerating d = 1..cbrt(N) is at most ~10⁶ iterations — fast in Python.
- Integer cube root computed with float seed then corrected by while loops (exact, safe at 10^18).
- For each d dividing N, discriminant Δ = 12·(N/d) − 3d² must be a non-negative perfect square s²; then y = (s − 3d)/6 must be a positive integer. Final verification x³ − y³ == N guards against any edge mistake.
- Checks: N=1 → d=1, Δ=9, s=3, y=0 → rejected, prints -1. N=397 → d=1: Δ = 12·397 − 3 = 4761 = 69², y = (69−3)/6 = 11, x = 12 → prints "12 11". Sample 3: d = 342756 − 66212 = 276544 ≤ cbrt(N) ≈ 3.4·10⁵... wait, cbrt(3.9977·10^16) ≈ 341,999, and d = 276,544 < that, so it's found within the loop. Good.

## worker: Review code for edge cases: N=1 → y=0 rejected → -
Reviewed the solution against the requested edge cases:

1. **N=1**: d=1 divides 1, m=1, D = 12−3 = 9, s=3, num = 3−3 = 0 → `num <= 0` rejects it (y would be 0, not positive). Loop ends, prints -1. ✓ Matches sample 2.

2. **N=397**: d=1, m=397, D = 4764−3 = 4761 = 69², num = 69−3 = 66, divisible by 6 → y=11, x=12. Verification 12³−11³ = 1728−1331 = 397 passes → prints "12 11". ✓ Matches sample 1.

3. **N=39977273855577088**: d = 342756−66212 = 276544. cbrt(N) ≈ 341,999 > 276,544, so d is within the enumeration range. The loop finds it and prints "342756 66212". ✓ Matches sample 3.

4. **Float safety in cube root**: seed is `round(N**(1/3)) + 2`, then two corrective while loops adjust to the exact integer cube root. Even if the float estimate is off by 1 (possible near 10^18), the `+2` margin plus correction loops guarantee c satisfies c³ ≤ N < (c+1)³. Since any valid d satisfies d³ < N (because N = d·(x²+xy+y²) > d·x² > d³), we have d ≤ c, so the range `1..c` is complete — no solution is missed.

5. **Performance**: at most ~10⁶ iterations. Each iteration is a `%` check; only divisors (few) reach the `isqrt` step. Runs well under 1 second in Python.

6. **Correctness guard**: final `x³ − y³ == N` verification ensures no spurious output even if some modular/parity condition were subtly wrong. The `num % 6 == 0` check combined with the perfect-square check is exactly the integrality condition for y = (s − 3d)/6.

The code is correct and complete as-is; no changes were needed.
