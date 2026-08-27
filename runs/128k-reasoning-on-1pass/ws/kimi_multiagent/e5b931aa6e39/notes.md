
## ideation
Core identity: `x^3 - y^3 = (x-y)(x^2+xy+y^2)`. Since `x,y` are positive and `x^3-y^3=N>0`, we must have `x>y`, so set `d=x-y>=1`. Then `x=y+d` gives:

`N = d * (3y^2 + 3dy + d^2)`

Key bound: `x^2+xy+y^2 > (x-y)^2 = d^2`, so `N = d*q > d^3`, hence `d < cbrt(N)`. For `N<=1e18`, `d <= 1e6`, so a linear scan over `d` is easily feasible.

For each `d`, necessary condition: `d | N`. Let `m=N//d`. Solve:

`3y^2 + 3dy + d^2 = m`

Discriminant: `D = 12m - 3d^2 = 3(4m-d^2)`. Need `D` nonnegative perfect square, `s=isqrt(D)`, `s*s==D`, and `y=(s-3d)/6` must be a positive integer. Then `x=y+d`.

Main pitfalls:
- Do not assume `x=y+1`; sample 1 is consecutive but general `d` can be large.
- Need strict positivity: require `s>3d` and divisibility by 6.
- Use integer cube root / integer square root only; floating `pow(n,1/3)` is unsafe near 1e18.
- In Python overflow is not an issue, but in C++ use `__int128` for `12*m`, cubes, etc.
- Factoring `N` directly is not needed and could be hard for 1e18; scanning `d` up to cube root is only about 1e6 iterations.
- Edge cases: `N=1` gives `-1`; very large valid sample needs exact integer arithmetic.

## worker: Implement the complete Python solution: read N fro
Implemented exactly per plan. Reasoning recap:

- Since `x^3 - y^3 = N > 0` with positive integers, `x > y`, so write `x = y + d` with `d >= 1`.
- Then `N = d * (3y^2 + 3dy + d^2)`. Since the second factor exceeds `d^2`, we get `N > d^3`, so `d <= cbrt(N) <= 10^6` for `N <= 10^18` — a linear scan is trivially fast.
- For each `d` dividing `N`, let `m = N // d`. Solving `3y^2 + 3dy + d^2 = m` as a quadratic in `y` gives discriminant `D = 12m - 3d^2`. `D` must be a non-negative perfect square (`math.isqrt` check), and `y = (s - 3d)/6` must be a positive integer (`s > 3d` and divisible by 6).
- `icbrt` uses pure integer binary search (no floating point, safe at 1e18). The `m <= d*d` guard skips cases where `D <= 0` early.
- Verified against samples mentally: N=397 → d=1, m=397, D=4761=69², y=(69-3)/6=11, x=12 ✓. N=1 → no d works, prints -1 ✓. N=39977273855577088 → d=276544 divides N, yields x=342756, y=66212 ✓.
