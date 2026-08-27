
## ideation
- Core difficulty: Find positive integers x>y with x^3 - y^3 = N (N up to 1e18).  
- Factorization: x^3 - y^3 = (x - y)(x^2 + xy + y^2) = d * (3y^2 + 3dy + d^2), where d = x - y ≥ 1.  
- For each d, we get a quadratic in y: 3d y^2 + 3d^2 y + (d^3 - N) = 0. Solve: y = (-3d^2 + sqrt(9d^4 - 12d(d^3 - N))) / (6d) = (-3d^2 + sqrt(12dN - 3d^4)) / (6d). The discriminant must be a perfect square and the resulting y must be a positive integer.  
- Since x^3 - y^3 = N ≥ 1, d cannot exceed N^(1/3)+1. With N ≤ 1e18, d ≤ 1e6+1, so iterating d from 1 to floor(N^(1/3)) is efficient.  
- Pitfalls: Use 128-bit integer arithmetic in languages with overflow risks; in Python it's fine. Need to ensure y > 0, y is integer, and x = y + d positive.  
- Alternative: iterate d only up to N^(1/3) (or while d^3 ≤ N). Use integer arithmetic for discriminant check to avoid floating errors.  
- Edge cases: N=1 returns -1 (since 2^3-1^3=7>1). N=2^3-1^3=7 should be found (d=1, y=1). N large up to 1e18 must be handled.

## worker: Implement the algorithm: read N, iterate d from 1 
- The algorithm iterates over possible values of `d = x - y` from 1 up to `floor(N^(1/3))`. For each `d`, it solves the quadratic equation `3d*y^2 + 3d^2*y + (d^3 - N) = 0` using the quadratic formula.
- The discriminant `12*d*N - 3*d^4` must be non-negative and a perfect square. If it is, we compute `y` and verify that it is a positive integer, then output `(x, y) = (y+d, y)`.
- The loop is at most about 1e6 iterations, which is efficient. We use `math.isqrt` for integer square root to avoid floating-point errors.
- Edge case: if `d^3 > N`, we break early because no solution exists for larger `d` (since `N = d*(3y^2+3dy+d^2) >= d^3`).
- The sample inputs have been verified: N=397 gives d=1, N=1 gives -1, N=39977273855577088 gives (342756, 66212).
