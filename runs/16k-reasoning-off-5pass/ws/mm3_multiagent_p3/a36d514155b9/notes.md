
## ideation
**Core difficulty:** We must compute the sum of Manhattan distances across *all* unordered pairs of pieces in *every* valid placement of `k` indistinguishable pieces on an `m×n` grid, modulo `10^9+7`. The grid can be up to `10^5` cells, so enumerating placements is impossible.

**Key insight – linearity of expectation / counting:**
Total sum over all arrangements = Σ over unordered pairs of pieces (in a given arrangement) of distance. 
Equivalently, for each *ordered* pair of distinct cells `(u, v)`, count the number of arrangements where the two pieces occupy `u` and `v` (i.e., choose the remaining `k-2` cells from the other `mn-2`), and add `dist(u,v)`.

**Manhattan decomposition:**
`|x_u - x_v| + |y_u - y_v|`. The row-contribution and column-contribution separate completely. So we can compute the total sum as:
  `RowSum + ColSum`, where
  `RowSum` = Σ_{ordered pairs (u,v)} (number of arrangements containing both) × |x_u - x_v|,
  `ColSum` = similar with |y_u - y_v|.

**Reducing to 1D:**
Consider a single row of length `n`. The number of ways to place the remaining `k-2` pieces in the *other* rows (there are `m-1` other rows, each with `n` cells, total `(m-1)*n` cells) plus in the *same* row but in the other `n-2` cells is `C(mn - 2, k - 2)`. This factor does *not* depend on the choice of `u, v` in the same row. So:
  RowSum = `C(mn - 2, k - 2) * n * S(n)`, where `S(n)` = sum of |i - j| over all ordered pairs (i, j) with 1 ≤ i, j ≤ n, i ≠ j.
Wait — careful: the pair (u, v) can be in the same row *or* different rows. If they are in different rows, their x-coordinates differ, contributing to |x_u - x_v|. So we must consider all ordered pairs of cells, not just same-row ones, for the x-contribution.

**Correct decomposition:**
For the x-coordinate (column index from 1 to n):
Total X-contribution = Σ_{all ordered pairs of cells (c1, c2)} |c1 - c2| × (# arrangements containing both cells).
The number of arrangements containing both specific cells is `C(mn - 2, k - 2)`.
The factor `C(mn - 2, k - 2)` is constant for every ordered pair of cells.
There are `m` rows, and the column indices for cells in a given row range over 1..n. So summing |c1 - c2| over all ordered pairs of all cells:
  Each row contributes S(n) (ordered pairs within the row, c1 ≠ c2) and also cross-row pairs: a cell in row r1 with column c1 and a cell in row r2 (r2 ≠ r1) with column c2. For different rows, |c1 - c2| is just |c1 - c2| (rows don't affect x-difference). Number of such cross-row ordered pairs: `m * (m-1) * n * n`.
  Within a row, ordered pairs: `m * n * (n-1)`. Sum of |c1-c2| over these is `m * S(n)`.
  Cross-row: `m*(m-1) * T(n)`, where `T(n) = n * n * (sum of |c1-c2| over c1,c2) / something`? Actually, cross-row ordered pairs: for each ordered pair of distinct rows (r1, r2), and each ordered pair of columns (c1, c2), we have a pair of cells. So the x-contribution from cross-row pairs is `m*(m-1) * Σ_{c1,c2} |c1-c2| = m*(m-1) * S_full(n)`, where `S_full(n) = Σ_{c1=1}^{n} Σ_{c2=1}^{n} |c1-c2|` includes c1=c2 (which contributes 0). So `S_full(n) = S(n)` effectively (since |c-c|=0).

Thus X-contribution = `C(mn-2, k-2) * [m * S(n) + m*(m-1) * S_full(n)]`
But `S_full(n) = S(n) + n*0 = S(n)`. So:
  X-contribution = `C(mn-2, k-2) * S(n) * [m + m*(m-1)] = C(mn-2, k-2) * S(n) * m * m`.
Wait, that's `m^2 * S(n)`. But this seems to treat column differences as if they happen `m^2` times. Let's re-derive carefully.

Actually, a cleaner approach: 
Total sum over ordered pairs of cells (u, v), u ≠ v, of `|col(u) - col(v)|` = 
  (number of ordered pairs of cells with given column indices c1, c2) × |c1-c2|.
  For each ordered pair of columns (c1, c2) (allowing c1=c2), the number of ordered pairs of cells with those columns is `m * m = m^2` (pick a row for u, pick a row for v; if c1=c2, u and v can be in same or different row, but `m^2` counts all).
  So total X-contribution (over all ordered pairs of cells) = `m^2 * Σ_{c1,c2=1}^{n} |c1-c2|`.
  This sum `Σ_{c1,c2} |c1-c2|` over 1..n includes c1=c2 (zero). So it equals `S_full(n)`.
  And the number of arrangements containing both cells (u, v) is `C(mn-2, k-2)`.
  So X-contribution = `C(mn-2, k-2) * m^2 * S_full(n)`.

Similarly, Y-contribution = `C(mn-2, k-2) * n^2 * S_full(m)`.

**But the problem asks for unordered pairs of pieces**, not ordered pairs of cells. In a given arrangement, the sum over unordered pairs of pieces. When we sum over arrangements, we can either:
  (a) Sum over ordered pairs of pieces: each unordered pair is counted twice (piece A, piece B) and (piece B, piece A). Since pieces are indistinguishable, the sum over unordered pairs = (sum over ordered pairs of pieces) / 2. But careful: if we use the "ordered pair of cells" trick, we are choosing an ordered pair of distinct cells to be occupied by two specific (distinguishable) pieces. The number of arrangements with pieces on cells u and v (ordered) is still `C(mn-2, k-2)` (since the remaining k-2 pieces go anywhere). So sum over ordered pairs of cells of distance × `C(mn-2, k-2)` gives the sum over ordered pairs of *distinguishable* pieces. Dividing by 2 gives the sum over unordered pairs.

Alternatively, we can directly count unordered pairs: for each unordered pair of cells {u, v}, number of arrangements containing both is `C(mn-2, k-2)`, and we add `dist(u, v)`. The number of unordered pairs of cells is `C(mn, 2)`, and the sum of distances over them is what we need. So:
  Total = `C(mn-2, k-2) × (sum of Manhattan distance over all unordered pairs of cells)`.

This is cleaner. The sum of Manhattan distance over all unordered pairs of cells in an m×n grid:
  `SumDist(m,n) = Σ_{all unordered pairs of cells} (|x1-x2| + |y1-y2|) = X_pairs + Y_pairs`.
  `X_pairs` = sum over unordered pairs of cells of |x1-x2|. 
  Each unordered pair of cells corresponds to an unordered pair of columns (c1, c2) with c1 ≤ c2. The number of unordered pairs of cells with columns c1, c2:
    - If c1 = c2: cells must be in different rows. Number = `C(m, 2)`.
    - If c1 < c2: cells can be in any rows independently. Number = `m * m = m^2` (pick row for cell 1, pick row for cell 2; since cells are unordered but we fix the column of cell 1 as c1 and cell 2 as c2, we get `m^2` ordered pairs of cells, but we are counting unordered pairs of cells with column-set {c1, c2}, and we need to avoid double counting. Better to use ordered-pair approach for cells and divide by 2.)

Let's use the ordered-pair-of-cells approach and divide by 2 at the end:
  Sum over ordered pairs of distinct cells (u,v) of |x_u - x_v| = `m^2 × S_full(n)`, where `S_full(n) = Σ_{c1,c2=1}^{n} |c1-c2|`.
  Similarly for y: `n^2 × S_full(m)`.
  So sum over unordered pairs = `[m^2 × S_full(n) + n^2 × S_full(m)] / 2`.

And total answer = `C(mn-2, k-2) × [m^2 × S_full(n) + n^2 × S_full(m)] / 2` (mod `10^9+7`).

Now, compute `S_full(N) = Σ_{i=1}^{N} Σ_{j=1}^{N} |i - j|`.
  `S_full(N) = 2 × Σ_{1 ≤ i < j ≤ N} (j - i)`.
  The sum Σ_{i<j} (j-i) = Σ_{d=1}^{N-1} d × (N - d).
  `Σ_{d=1}^{N-1} d(N-d) = N × Σ d - Σ d^2 = N × (N-1)N/2 - (N-1)N(2N-1)/6`
  `= (N-1)N × [N/2 - (2N-1)/6] = (N-1)N × [3N - (2N-1)]/6 = (N-1)N × (N+1)/6 = (N-1)N(N+1)/6`.
  So `S_full(N) = 2 × (N-1)N(N+1)/6 = (N-1)N(N+1)/3`.

Check: N=2: |1-1|+|1-2|+|2-1|+|2-2| = 0+1+1+0 = 2. Formula: (1)(2)(3)/3 = 2. ✓
N=3: 0+1+2+1+0+1+2+1+0 = 8. Formula: (2)(3)(4)/3 = 24/3 = 8. ✓

**So:**
  `S_full(n) = (n-1)*n*(n+1)/3`
  `S_full(m) = (m-1)*m*(m+1)/3`

Total sum over unordered pairs of cells:
  `U = [m^2 * (n-1)*n*(n+1)/3 + n^2 * (m-1)*m*(m+1)/3] / 2`
  `= [m^2 n (n^2-1) + n^2 m (m^2-1)] / 6`
  `= mn [m(n^2-1) + n(m^2-1)] / 6`
  `= mn [m n^2 - m + n m^2 - n] / 6`
  `= mn [mn(m+n) - (m+n)] / 6`
  `= mn (m+n) (mn - 1) / 6`.

Let me verify: `U = m*n*(m+n)*(m*n - 1) / 6`.
For m=2, n=2: cells = 4. Unordered pairs = 6. Distances: 
  (1,1)-(1,2):1, (1,1)-(2,1):1, (1,1)-(2,2):2,
  (1,2)-(2,1):2, (1,2)-(2,2):1, (2,1)-(2,2):1. Sum=8.
Formula: 2*2*(4)*(3)/6 = 48/6 = 8. ✓

For m=1, n=4: cells = 4 (in a line). Unordered pairs = 6. Distances: 1+2+3+1+2+1 = 10.
Formula: 1*4*(5)*(3)/6 = 60/6 = 10. ✓

Great! So the sum of Manhattan distances over all unordered pairs of cells is:
  `U(m,n) = m * n * (m + n) * (m * n - 1) / 6`.

Now, the final answer is:
  `Ans = C(m*n - 2, k - 2) * U(m,n) mod (10^9+7)`.

Wait — is that correct? Let me double-check with the examples.
Example 1: m=2, n=2, k=2. mn=4. U=8. C(2,0)=1. Ans = 8. ✓
Example 2: m=1, n=4, k=3. mn=4. U=10. C(2,1)=2. Ans = 20. ✓

**Edge cases:** Division by 6 and 2. We need modular inverse of 6 and 2 mod 10^9+7 (prime). 6⁻¹ = 166666668, 2⁻¹ = 500000004.

**Wait, the example 2 calculation:**
m=1, n=4, k=3. Total cells = 4. U = 1*4*5*3/6 = 10. C(4-2, 3-2) = C(2,1) = 2. Total = 20. The problem says arrangements = C(4,3)=4. Sum of distances = 4+6+6+4=20. Formula gives 20. ✓

**Conclusion:** The answer is simply:
  `Ans = C(mn - 2, k - 2) * mn * (m+n) * (mn - 1) / 6  (mod 10^9+7)`.

We need to precompute factorials up to `mn` (which is ≤ 10^5) to compute the binomial coefficient efficiently.

**Potential pitfalls:**
- Division by 6: need modular inverse.
- The formula `U = mn(m+n)(mn-1)/6` is always an integer? Let's check: mn(m+n)(mn-1). Among mn, (mn-1), and (m+n), at least one is divisible by 2, and among three consecutive-like numbers... Actually, product of 4 numbers, divided by 6=2×3. Since mn and mn-1 are consecutive, one is even. Also, among any three integers, one is divisible by 3. Here we have mn, (m+n), (mn-1). Note that mn - (mn-1) = 1, so they are consecutive. And m+n... we need to ensure divisibility. Actually, let's verify: the sum S_full(N) = (N-1)N(N+1)/3 is always integer (product of 3 consecutive numbers divisible by 3!). And U = [m^2 * S_full(n) + n^2 * S_full(m)] / 2. m^2 * S_full(n) is integer (m^2 times integer). The sum of two such terms divided by 2. Is it always integer? From the closed form mn(m+n)(mn-1)/6, it should be. Let's trust the algebra. To be safe in code, we can do all operations modulo p using modular inverses.

**Implementation plan:**
- Precompute factorials `fact[0..mn]` and inverse factorials `inv_fact[0..mn]` mod M = 10^9+7.
- Function `C(a, b) = fact[a] * inv_fact[b] % M * inv_fact[a-b] % M` (return 0 if b<0 or b>a).
- Compute `total_cells = m * n`.
- `binom = C(total_cells - 2, k - 2)`.
- Compute `U = total_cells * (m + n) % M * (total_cells - 1) % M * inv6 % M`, where `inv6 = pow(6, M-2, M)`.
- `ans = binom * U % M`.
- Return `ans`.

**Double-check constraints:** m,n up to 10^5, mn up to 10^5. Factorial array of size up to 10^5 is fine. Time: O(mn) precomputation, O(1) query. Memory: O(mn).

**Alternative verification with a larger example:**
m=2, n=3, k=2. mn=6. U = 6*5*5/6 = 25. C(4,0)=1. Ans=25.
List all C(6,2)=15 pairs and their distances:
Grid (r,c): (1,1),(1,2),(1,3),(2,1),(2,2),(2,3).
Manhattan distances:
(1,1)-(1,2):1, (1,1)-(1,3):2, (1,1)-(2,1):1, (1,1)-(2,2):2, (1,1)-(2,3):3
(1,2)-(1,3):1, (1,2)-(2,1):2, (1,2)-(2,2):1, (1,2)-(2,3):2
(1,3)-(2,1):3, (1,3)-(2,2):2, (1,3)-(2,3):1
(2,1)-(2,2):1, (2,1)-(2,3):2
(2,2)-(2,3):1
Sum: row 1: 1+2+1+2+3+1+2+1+2+3+2+1 = let's sum systematically:
Pairs: 
(1,1): with (1,2)=1, (1,3)=2, (2,1)=1, (2,2)=2, (2,3)=3. Sum=9.
(1,2): with (1,3)=1, (2,1)=2, (2,2)=1, (2,3)=2. Sum=6.
(1,3): with (2,1)=3, (2,2)=2, (2,3)=1. Sum=6.
(2,1): with (2,2)=1, (2,3)=2. Sum=3.
(2,2): with (2,3)=1. Sum=1.
Total = 9+6+6+3+1 = 25. ✓ Formula works.

**All good!**

## worker: Implement the `Solution` class with `distanceSum(s
The closed-form sum of Manhattan distances over all unordered cell pairs in an `m×n` grid is `U = m*n*(m+n)*(m*n - 1) / 6`. Each such pair appears in exactly `C(m*n - 2, k - 2)` arrangements (choose remaining `k-2` cells from the rest). Total answer is `C(m*n-2, k-2) * U` mod `10^9+7`. Verified against given examples and a 2×3 case. Factorials are memoized per `N` (here always `m*n ≤ 10^5`).
