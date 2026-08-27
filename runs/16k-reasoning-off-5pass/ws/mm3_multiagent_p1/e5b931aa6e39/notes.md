
## ideation
**Core difficulty:**  
We need to find positive integers `x > y` such that `x^3 - y^3 = N` for `1 ≤ N ≤ 10^18`.  
A direct approach iterating over `y` (up to ~10^6) is feasible because `x^3 = N + y^3` and `x` cannot exceed `(N+1)^(1/3) + 1 ≈ 10^6 + 1`.

**Candidate approaches:**

1. **Enumerate `y` and compute `x`:**
   - For `y` from 1 upward while `y^3 < N`:
     - Compute `x_cubed = N + y^3`.
     - Compute the integer cube root `x = round(x_cubed^(1/3))`.
     - Check if `x^3 - y^3 == N` and `x > y`.
   - Complexity: O(N^(1/3)) ≈ 10^6 iterations, each O(1) with a fast integer cube root. Fits comfortably in time.

2. **Enumerate the difference `d = x - y`:**
   - Since `x^3 - y^3 = (x-y)(x^2 + xy + y^2) = d * (something)`, `d` must divide `N`.
   - For each divisor `d` of `N` (up to N^(1/2) divisors worst-case), we would solve a quadratic in `y`. However, enumerating all divisors of N up to 10^18 is slow in the worst case (though possible with prime factorization, but unnecessarily complex).

3. **Iterate over `x` and solve for `y`:**
   - For each `x`, `y^3 = x^3 - N`. Same complexity as approach 1.

4. **Mathematical shortcut:**
   - Note that `x^3 - y^3 = (x-y)(x^2 + xy + y^2)`. If `d = x-y` is small, we might solve a quadratic. But again, enumeration is simpler.

**Pitfalls:**

- Floating point inaccuracies when computing cube roots. Must use integer arithmetic (e.g., binary search) for exact integer cube root, or use `round` with care (the `decimal` or `Fraction` approach is safer but slower). Python's `int(round(x ** (1/3)))` is generally safe for 10^18 because `float` has 53 bits of mantissa (~15-16 decimal digits), and 10^18 is near the limit but rounding errors can occur.
  - Safer: implement an integer cube root via binary search or use `gmpy2.iroot` if allowed, but standard CP environment won't have gmpy2.
  - Simpler safe method: use `int(round(x ** (1/3)))` and verify by cubing, or use a custom integer cube root. Given the small number of iterations (10^6), a binary search for cube root per iteration is acceptable, but a faster method is to use `int((x) ** (1/3))` and then adjust by ±2 to be safe.
  - Best approach: use `int(x ** (1/3))` as a starting point, then adjust downward while `(t+1)**3 <= x` and upward while `t**3 > x`. This is fast and correct.

- Loop bound: iterate `y` while `y^3 < N` (i.e., while `y < N^(1/3) + 1`). At the end, if no solution found, print `-1`.

- `N` can be 1, which has no solution. The loop should handle this correctly (starts at y=1, computes x^3 = 2, cube root is 1, x=y, not > y, so no solution; then y=2 has y^3=8>1, loop ends, print -1).

- Input is a single integer, output is either `-1` or `x y`.

**Concrete plan for implementation:**

1. Read `N`.
2. Set `y = 1`.
3. While `y^3 < N`:
   - `target = N + y^3`.
   - Compute integer cube root `x` of `target` via:
     - `x = int(target ** (1/3))`
     - While `(x+1)**3 <= target`: x += 1
     - While `x**3 > target`: x -= 1
   - If `x**3 == target` and `x > y`: print `x y` and exit.
   - `y += 1`
4. If loop finishes, print `-1`.

**Edge cases:**
- `N` is a perfect cube minus 1 (like 1): no solution.
- `N` is very large (10^18): loop runs up to 10^6 iterations, fine.
- `y` reaches the limit but we must ensure `y^3` doesn't overflow Python's integer (Python has arbitrary precision integers, so safe). But we can break early when `y^3 >= N` since `x > y` means `x^3 > y^3 >= N`, impossible unless `x^3 - y^3` can still equal N? Actually if `y^3 >= N`, then `x^3 = N + y^3 >= 2*y^3 > y^3`, so `x > y` is possible, but we need `x^3 - y^3 = N`. If `y^3 >= N`, the difference `x^3 - y^3` with `x > y` is at least `(y+1)^3 - y^3 = 3y^2 + 3y + 1`. For large `y`, this grows. But we can safely stop when `3*y*y + 3*y + 1 > N` and `y^3 >= N`? Actually simpler: just iterate up to when `y^3 >= N` because the maximum possible `x` is `N^(1/3) + 1`, so `y` can be at most that. So we can compute `max_y = int(N ** (1/3)) + 2` and iterate `y` from 1 to `max_y`. This is safe.

**Optimization for cube root:**  
Since we are iterating `y` from 1 to `max_y` ~ 10^6, and for each we compute a cube root, the total operations are ~10^6. The correction loop (adjusting by ±1 or ±2) will almost never run more than once. So this is efficient.

**Verification with samples:**
- N=397: y=11 -> target=397+1331=1728 -> cube root=12, 12^3-11^3=1728-1331=397. Works.
- N=1: y=1 -> target=2 -> cube root=1, x not > y. y=2 -> y^3=8 > 1, loop ends (if we use `y^3 < N` condition). Print -1. Works.
- N=39977273855577088: should find the given pair.

## worker: Implement the solution in Python: read N, iterate 
The solution iterates over possible values of `y` from 1 up to approximately `N^(1/3) + 3` (a safe upper bound). For each `y`, it computes `target = N + y^3` and finds the integer cube root `x` using a float approximation followed by a small correction loop (±1 adjustments) to ensure exactness. It checks whether `x^3 - y^3 == N` and `x > y`, printing the pair and exiting immediately if found. If the loop completes without finding a valid pair, it prints `-1`. The cube root correction loop runs at most a few iterations because float's 53-bit mantissa is accurate enough for numbers up to 10^18. The total time complexity is O(N^(1/3)) ≈ 10^6 operations, well within limits. Edge cases like N=1 are handled correctly (no solution exists).
