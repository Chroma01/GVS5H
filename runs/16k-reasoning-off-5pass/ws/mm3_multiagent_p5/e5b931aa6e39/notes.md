
## ideation
**Core difficulty:** Determine if a positive integer N can be expressed as a difference of two positive cubes: x^3 - y^3 = N with x > y ≥ 1.

**Key observations:**
- For large N (up to 10^18), we need an efficient method.
- Since x^3 - y^3 = (x - y)(x^2 + xy + y^2), the difference grows quickly.
- For any x, the maximum possible N for that x is x^3 - 1^3 = x^3 - 1.
- The smallest positive difference is 2^3 - 1^3 = 7. So if N < 7, answer is -1 immediately (except N=0 but N≥1).
- For N ≤ 10^18, x = (N+1)^(1/3) is an upper bound: x ≤ 10^6 + 1 (since (10^6)^3 = 10^18).

**Candidate approaches:**
1. **Cube root iteration (O(N^{1/3})):** Loop x from 2 to floor(cuberoot(N+1)). Compute t = x^3 - N. If t > 0, check if t is a perfect cube. If so, y = cbrt(t), and if y ≥ 1 and y < x, output (x, y). This is ~10^6 operations, very fast.
2. **Divisor iteration (O(√N) worst case):** For each d | N (d = x - y), solve quadratic 3dy^2 + 3d^2y + (d^3 - N) = 0. Check discriminant is perfect square, etc. Number of divisors ≤ ~10^5, but iterating up to √N = 10^9 is too slow.
3. **Hybrid / Optimization:** Since d = x - y and d^3 ≤ N, d ≤ N^{1/3} ≤ 10^6. So we can iterate d from 1 to N^{1/3} and check if d | N, then solve the quadratic. This is O(N^{1/3}) and feasible.

**Pitfalls:**
- Integer cube root: must compute exactly. In Python, use round(x ** (1/3)) and adjust, or use integer arithmetic via binary search.
- Overflow: Python handles big integers, so no overflow issues, but x^3 for x up to 10^6+1 is about 10^18, fine.
- Edge case: N = 1 to 6 → no solution.
- Ensure y is a positive integer (y ≥ 1).
- If multiple solutions, any is fine.

**Best approach:** Iterate x from 2 to floor(cuberoot(N+1)). For each x, compute diff = x^3 - N. If diff ≤ 0, continue. Check if diff is a perfect cube y^3. If so, and y < x, output x, y and return. If loop finishes, output -1.

## worker: Implement the algorithm: read N, handle small N ed
The initial approach of iterating x from 2 to cube root of N is insufficient because x can be much larger when y is close to x. For N = 10^18, x can be up to ~5.77e8 (when y = x-1), making O(N^{1/3}) iteration over x too slow.

The correct approach is to iterate over d = x - y (the difference). Since d^3 < N, we have d ≤ N^{1/3} ≤ 10^6. For each d that divides N, we solve the quadratic 3y² + 3dy + (d² - N/d) = 0, check if the discriminant is a perfect square, and if so, compute y. This runs in O(N^{1/3}) time, which is ~10^6 operations, fast enough.

Key formulas:
- d = x - y
- N = d × (3y² + 3dy + d²)
- Discriminant D = 3(4(N/d) - d²)
- y = (√D - 3d) / 6

Edge cases handled: N < 7 returns -1 (since smallest difference is 7), and we verify the solution before printing.

## worker: The current code already implements the divisor-ba
The current code implements the divisor-based approach iterating over `d = x - y` up to `N^(1/3)`. This is correct and efficient (~10^6 operations for N up to 10^18). Key points:

1. **Small N optimization**: N < 7 immediately returns -1 (smallest difference is 2³-1³=7).
2. **Upper bound calculation**: Uses cube root of N with safety margins to ensure all valid d are checked.
3. **Quadratic solving**: For each d dividing N, solves 3y² + 3dy + (d² - M) = 0 where M = N/d.
4. **Discriminant check**: D = 3(4M - d²) must be a non-negative perfect square.
5. **Integer verification**: Computes y = (√D - 3d)/6 and verifies x³ - y³ = N before output.

The code handles all edge cases: small N, N that aren't representable as difference of cubes, and large N up to 10^18. The verification step ensures correctness even with floating point approximations in the cube root calculation.
