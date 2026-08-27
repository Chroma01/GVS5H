
## ideation
**Core structure.** Let `d = x − y ≥ 1`. Then
`N = x³ − y³ = d·(3y² + 3dy + d²)`.
Two immediate consequences:

1. **`d` divides `N`.**
2. **`d³ ≤ N`** (since `3y² + 3dy + d² ≥ d²`), so `d ≤ ⌊N^{1/3}⌋ ≤ 10⁶` for `N ≤ 10¹⁸`. Even tighter with `y ≥ 1`: `d(d² + 3d + 3) ≤ N`.

So the whole search space is only ~10⁶ candidate values of `d`, and for each we solve a quadratic in `y`.

**Quadratic step.** With `M = N/d`: `3y² + 3dy + (d² − M) = 0`
⇒ `y = (−3d + √(12M − 3d²)) / 6`.
Let `D = 12M − 3d²`. Need `D ≥ 0`, `s = isqrt(D)` with `s² = D`, `s > 3d` (strict, so `y ≥ 1`), and `(s − 3d) % 6 == 0`. Then `y = (s − 3d)//6`, `x = y + d`.

Note `D = 3(4M − d²)` so any perfect-square `D` forces `3 | s`; the mod-6 test then reduces to a parity condition, but just testing `% 6 == 0` directly is simplest and safe.

**Pitfalls to watch:**
- **Cube-root bound via floats** (`N ** (1/3)`) is unreliable at 10¹⁸ — must use an integer cube root (Newton iteration or `round` + correction loop that adjusts while `(c+1)³ ≤ N` / `c³ > N`).
- **Perfect-square test with floats** — must use `math.isqrt`, never `math.sqrt`.
- `y` must be **positive**, not just nonnegative: `N = 1` gives `d = 1`, `D = 9`, `s = 3`, `y = 0` → must reject and print `-1`. Similarly any `N = d³` case yields `y = 0`.
- Overflow: none in Python, but `12*M` can be ~1.2·10¹⁹ — fine.
- Performance: ~10⁶ iterations with a `N % d` filter first; the expensive `isqrt` only runs on divisors (few). Should be well under 1 s, but keep the inner loop tight (local variable for `N`, avoid function calls, maybe `divmod` or `if N % d == 0`).
- Output format: single line `x y`, or `-1`.
- Reading input: may have trailing whitespace/newline; use `int(sys.stdin.readline())` / `input()` stripped.

**Sanity checks (mental, not run):** N=397 → d=1 divides, M=397, D=4764−3=4761=69², y=(69−3)/6=11, x=12 ✓. N=39977273855577088: d = 342756−66212 = 276544 divides N presumably; the loop would find some valid `d` (any valid answer accepted).

**Alternative approaches considered:**
- Iterating over `y` directly: `y` can be ~10¹⁷ → infeasible.
- Factoring `N` fully to enumerate divisors ≤ 10⁶: unnecessary and harder (10¹⁸ factoring); trial loop over all `d ≤ 10⁶` is simpler and strictly covers all divisors in range.
- For each `d`, instead of the quadratic formula one could binary search `y` in `f(y) = 3y²+3dy+d² = M` — equivalent, slightly slower but avoids the mod-6 reasoning; a good cross-check.

## worker: Write the complete Python solution: read N from st
- Derivation: with `d = x - y ≥ 1`, `N = d(3y² + 3dy + d²)`. Hence `d | N` and `d³ ≤ N`, so `d ≤ icbrt(N) ≤ 10⁶` for `N ≤ 10¹⁸`.
- For each divisor `d`, solve `3y² + 3dy + (d² − M) = 0` with `M = N/d`; `y = (−3d + √(12M − 3d²))/6`. Exact integer test with `math.isqrt` (no float precision issues). Require `s − 3d > 0` (so `y ≥ 1`, rejecting `y = 0` cases like `N = 1` or `N = d³`) and divisibility by 6.
- `D = 12M − 3d² ≥ 12d² − 3d² > 0` whenever `d³ ≤ N`, so the negative check is just defensive.
- `icbrt` uses a float estimate plus downward/upward integer correction loops — exact for all `N ≤ 10¹⁸`.
- Inner loop is just a modulo test for ~10⁶ iterations (~0.1–0.3 s in CPython); `isqrt` only runs for actual divisors (few hundred at most).
- Sample check: `N=397`, `d=1` → `D=4761=69²`, `t=66`, `y=11`, `x=12` ✓. `N=1` → `d=1`, `D=9`, `s=3`, `t=0` rejected → `-1` ✓.
