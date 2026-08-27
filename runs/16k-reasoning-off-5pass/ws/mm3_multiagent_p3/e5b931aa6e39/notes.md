
## ideation
The equation is \(x^3 - y^3 = N\) with positive integers \(x, y\) and \(N \le 10^{18}\).
Factoring: \(x^3 - y^3 = (x-y)(x^2 + xy + y^2) = N\).
Set \(d = x - y > 0\). Then \(x = y + d\) and
\[
N = (y+d)^3 - y^3 = 3d y^2 + 3d^2 y + d^3.
\]
For a given \(d\) this is a quadratic in \(y\):
\[
3d\,y^2 + 3d^2 y + (d^3 - N) = 0.
\]
The discriminant must be a non‑negative perfect square:
\[
\Delta = (3d^2)^2 - 4 \cdot 3d \cdot (d^3 - N)
       = 9d^4 - 12d^4 + 12dN
       = 12dN - 3d^4 = 3d(4N - d^3).
\]
We require \(\Delta \ge 0\) and \(\sqrt{\Delta}\) to be an integer, and also
\((-3d^2 + \sqrt{\Delta})\) to be divisible by \(2\cdot 3d = 6d\) to give a positive integer \(y\).

**Bounds for d**:
Since \(x > y\) and \(x^3 - y^3 \ge (y+1)^3 - y^3 = 3y^2 + 3y + 1 \ge 1\), the smallest possible difference is \(d = 1\).
Also \(d^3 \le x^3 - y^3 < x^3 \le N + y^3\). A simple safe upper bound is
\(d \le \lfloor N^{1/3} \rfloor + 1\) or more tightly \(d \le \lfloor (4N)^{1/3} \rfloor\),
since \(\Delta = 3d(4N - d^3) \ge 0\) implies \(d^3 \le 4N\).
For \(N = 10^{18}\), \(d \le 1.6 \times 10^6\), which is easily enumerable.

## worker: Implement the algorithm in Python as described, re
The approach enumerates all possible differences `d = x - y` (positive).  
For each `d`, we solve the quadratic in `y`:

- `x^3 - y^3 = N`  
- Let `d = x - y`, then `x = y + d`  
- Expanding gives `3d*y^2 + 3d^2*y + d^3 - N = 0`  

The discriminant `Δ = 3d(4N - d^3)` must be a non‑negative perfect square, and the resulting `y = (-3d^2 + sqrt(Δ)) / (6d)` must be a positive integer.  

The bound `d^3 ≤ 4N` comes from requiring `Δ ≥ 0`. For `N ≤ 10^18`, `d` is at most about `1.6·10^6`, so a simple linear scan is fast.  

Verification of the candidate pair protects against possible floating‑point inaccuracies in the cubic root bound.
