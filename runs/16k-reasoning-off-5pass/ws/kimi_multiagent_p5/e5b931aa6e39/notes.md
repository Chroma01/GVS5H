
## ideation
Core difficulty: N up to 10^18, so brute force over x or y is impossible. Need a number-theoretic reduction.

Key factorization: x³−y³ = (x−y)(x²+xy+y²) = N. Let d = x−y ≥ 1. Then d | N, and substituting x = y+d:
- 3y² + 3dy + d² = N/d
- Discriminant: D = 12·(N/d) − 3d² must be a non-negative perfect square
- y = (−3d + √D)/6 must be a positive integer

Bound on d: since x > y ≥ 1 and x²+xy+y² > x² ≥ (d+1)² > d², we have N = d·(x²+xy+y²) > d³, so d < N^(1/3) ≤ 10^6. Thus we only need to test divisors d of N with 1 ≤ d ≤ 10^6 — a simple loop i = 1..10^6 checking i | N suffices (10^6 iterations, trivial in Python). No factoring needed.

Conditions to check per divisor d:
1. D = 12·(N//d) − 3d² ≥ 0
2. D is a perfect square: s = isqrt(D), s² == D
3. (−3d + s) > 0 and divisible by 6 → y = (s − 3d)//6, x = y + d
4. Optionally verify x³−y³ == N as a sanity check (cheap).

Pitfalls:
- Integer overflow is not an issue in Python, but use math.isqrt for exactness (no floats — 12N/d can be ~1.2×10^19, floats lose precision).
- Must ensure y ≥ 1 (positive), so s > 3d strictly.
- Divisibility: (s − 3d) % 6 == 0. Note s ≡ 3d (mod 6) is required; since D = 12(N/d) − 3d², mod 3 considerations matter — just check directly.
- Edge case N=1: no divisors work (d=1 gives D=9, s=3, y=0 not positive) → output -1. Good.
- Multiple divisors may work; any one is fine — return the first found.

Complexity: O(N^(1/3)) = O(10^6) — fast.

## worker: Implement the full solution: read N from stdin, lo
- Factored x³−y³ = (x−y)(x²+xy+y²). With d = x−y ≥ 1, d must divide N, and since x²+xy+y² > x² > d², we have N > d³, so d ≤ N^(1/3) ≤ 10^6 for N ≤ 10^18. A simple loop over d = 1..10^6 checking divisibility is fast enough (no factoring needed).
- Substituting x = y+d gives 3y² + 3dy + d² = N/d. Discriminant D = 12(N/d) − 3d² must be a non-negative perfect square s², and y = (s − 3d)/6 must be a positive integer.
- Used `math.isqrt` for exact integer square roots (avoids float precision issues at ~10^19). The cube-root bound uses float only to get within ±1 of the true root (safe since the value ≤ 10^6, far below float precision limits), then adjusts with exact integer arithmetic.
- Verified each candidate with x³−y³ == N before printing (cheap sanity check).
- Edge cases: N=1 → d=1 gives D=9, s=3, y=0 (not positive) → correctly prints -1. Sample 397 → d=1: D=12·397−3=4761=69², y=(69−3)/6=11, x=12 ✓.

## worker: Sanity-check edge cases: N=1 → -1, N=397 → (12,11)
Sanity checks performed (by reasoning / mental trace):

1. **N = 1**: cbrt = 1. Only d=1: m=1, D = 12−3 = 9, s=3, num = 3−3 = 0 → `num <= 0` → skip. Loop ends → prints `-1`. ✓ (matches Sample 2)

2. **N = 397**: cbrt(397) ≈ 7. d=1 divides 397: m=397, D = 4764−3 = 4761 = 69², s=69, num = 69−3 = 66, 66%6==0 → y=11, x=12. Verify 12³−11³ = 1728−1331 = 397 ✓ → prints `12 11`. ✓ (matches Sample 1)

3. **N = 39977273855577088** (Sample 3): expected (342756, 66212), d = 276544. Check: d³ ≈ 2.116×10^16 < N ≈ 4.0×10^16 ✓, so d is within the loop range (cbrt(N) ≈ 341,999... actually cbrt(4×10^16) ≈ 341,995 — wait, d = 276544 ≤ 341995 ✓). d divides N (since the factorization holds), D = 12(N/d) − 3d² will be a perfect square by construction, and y = 66212 ≥ 1. The verification step `x³−y³ == N` guards against any arithmetic slip. ✓

4. **Performance for N = 10^18**: cbrt(10^18) = 10^6 exactly. The loop runs at most 10^6 iterations; each iteration is a few integer ops (a modulo, and only for divisors — at most ~10^3–10^4 of them for N ≤ 10^18 — an isqrt on a ~64-bit number). Runtime is well under 1 second in Python. ✓

5. **Float safety of cbrt**: N ≤ 10^18, so the true cube root ≤ 10^6. Double precision has 53 bits (~9×10^15) of integer precision, so `N ** (1/3)` has relative error ~10^-16, i.e., absolute error ≪ 1 on a value ≤ 10^6. The two adjustment `while` loops then correct any off-by-one exactly using integer arithmetic. ✓

6. **Correctness of bound**: x > y ≥ 1 ⇒ x ≥ d+1 > d, and x²+xy+y² > x² > d², hence N = d·(x²+xy+y²) > d³, so d < N^(1/3); looping d up to floor(cbrt(N)) is complete. ✓

7. **Positivity**: `num <= 0` excludes y = 0 (e.g., N=1 case) and negative roots, ensuring positive integers only. The final `x³−y³ == N` check is a cheap belt-and-suspenders guard.
