
## ideation
**Core difficulty:**  
We need the sum of Manhattan distances over *all* unordered pairs of pieces across *all* `C(m·n, k)` arrangements. Brute force is impossible because `m·n` can be up to `10^5`.

**Key insight (symmetry / linearity):**  
Fix an unordered pair of distinct cells `(A, B)`. In any valid arrangement, the Manhattan distance between the two pieces contributes to the sum **iff** both cells are occupied. The number of arrangements where a specific unordered pair of cells is simultaneously occupied is exactly `C(m·n − 2, k − 2)` (choose the remaining `k−2` cells out of the other `m·n − 2` cells). Therefore:

\[
\text{Total} = C(m \cdot n - 2,\; k - 2) \times S
\]

where `S` is the sum of Manhattan distances over all unordered pairs of distinct cells on the grid.

**Computing `S` efficiently:**  
Manhattan distance decomposes: `S = Sx + Sy`.

- For `Sx`: treat rows `0..m−1`. Row `x` has `n` cells. The number of unordered row pairs `(x, x')` with `x < x'` is `C(m, 2)`, and for each such pair there are `n·n = n²` cell pairs separated by `(x'−x)` in the x-direction. So:

\[
S_x = n^2 \sum_{0 \le x < x' < m} (x' - x) = n^2 \sum_{d=1}^{m-1} d (m - d) = n^2 \cdot \frac{m(m-1)(m+1)}{6}
\]

- For `Sy`: symmetrically,

\[
S_y = m^2 \cdot \frac{n(n-1)(n+1)}{6}
\]

So `S = n²·m(m−1)(m+1)/6 + m²·n(n−1)(n+1)/6`.

**Final formula:**

\[
\text{Answer} = C(mn-2,\; k-2) \times \frac{n^2 m(m-1)(m+1) + m^2 n(n-1)(n+1)}{6} \pmod{10^9+7}
\]

**Pitfalls:**
- Need modular inverse of `6` (since `MOD = 10^9+7` is prime, `inv6 = pow(6, MOD-2, MOD)`).
- Precompute factorials and inverse factorials up to `N = m*n` (≤ `10^5`) to compute `C(N-2, k-2)` quickly.
- Watch out for `k = 2` and `k = m*n`; formula works because `C(N-2, k-2)` becomes `1` in the extreme case `k = N` (all cells filled, exactly one arrangement, `C(N-2, N-2) = 1`).
- Use `int` arithmetic in Python, apply `% MOD` only at the end (or intermediate to avoid huge numbers).

## worker: Implement the `Solution` class with the `distanceS
- The total sum of Manhattan distances across all valid `k`-piece arrangements equals `C(mn-2, k-2) * S`, where `S` is the sum of Manhattan distances over every unordered pair of distinct cells.
- `S` splits into x- and y-contributions: `Sx = n² · m(m−1)(m+1)/6`, `Sy = m² · n(n−1)(n+1)/6`.
- Precomputing factorials/inverses up to `mn` (≤ 10⁵) makes the binomial coefficient O(1).
- The modular inverse of 6 is computed via Fermat's little theorem (`MOD` is prime).
- Verified conceptually with the examples:
  - `m=2, n=2, k=2`: `mn=4`, `C(2,0)=1`, `S = 1·(2·1·3)/6 + 1·(2·1·3)/6 = 1 + 1 = 2` → answer `2`. (Example output is 8; however, with the formula the answer is `C(4,2)=6` arrangements times average distance 4/3? Wait, recompute: `C(4,2)=6`, sum of distances over all unordered pairs of cells is `1+1+1+1+2+2 = 8`. Then `C(2,0) * 8 = 8`. My mental arithmetic for `S` was off – plugging `m=n=2`: `Sx = 4·(2·1·3)/6 = 4`, `Sy = 4·(2·1·3)/6 = 4`, `S = 8`. Correct.)
  - `m=1, n=4, k=3`: `mn=4`, `C(2,1)=2`, `Sx = 16·(1·0·2)/6 = 0`, `Sy = 1·(4·3·5)/6 = 10`, `S=10`, answer `2·10=20`. Matches.

## worker: Test the implementation with the given examples an
- The core idea is linearity: each unordered pair of distinct cells contributes its Manhattan distance in every arrangement where both are occupied. The number of such arrangements is `C(mn-2, k-2)`.
- `S` is decomposed into x- and y-components. For a fixed row difference `d` (`1 ≤ d ≤ m-1`), there are `n^2` cell pairs separated by `d` in the x-direction, and `m-d` ways to choose the two rows, giving the sum `n^2 * Σ d(m-d) = n^2 * m(m-1)(m+1)/6`. Symmetrically for the y-direction.
- Factorials are precomputed up to `mn` (≤ 10⁵) to evaluate the binomial coefficient in O(1). The modular inverse of 6 is computed via Fermat's little theorem because `MOD = 10⁹+7` is prime.
- Verified with the provided examples:
  - `m=2, n=2, k=2` → `C(2,0)=1`, `Sx = 4·(2·1·3)/6 = 4`, `Sy = 4`, total `8` ✓
  - `m=1, n=4, k=3` → `C(2,1)=2`, `Sx = 0`, `Sy = 1·(4·3·5)/6 = 10`, total `20` ✓
- Edge cases handled: `k=2` (just sum over all pairs), `k=mn` (only one arrangement, coefficient is `1`), and any `m, n` up to 10⁵ with `mn` ≤ 10⁵.
