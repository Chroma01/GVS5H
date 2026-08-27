
## ideation
- Core difficulty: summing Manhattan distances over all C(mn, k) arrangements is exponential if done naively; need a combinatorial counting argument.
- Key insight (linearity of expectation / counting): every unordered pair of distinct cells appears in exactly C(mn-2, k-2) arrangements. So total = C(mn-2, k-2) × (sum of Manhattan distances over all unordered pairs of cells).
- The sum over all cell pairs decomposes into row-distance sum + column-distance sum:
  - Row part: for each pair of rows (i<j), distance (j-i), there are n² ordered column choices (n choices for each cell's column). Sum over row pairs: Σ_{d=1}^{m-1} d·(m-d) = m²(m²-1)/6. So row contribution = n² · m²(m²-1)/6.
  - Column part symmetric: m² · n²(n²-1)/6.
  - Total pair-distance sum = n²·m²(m²-1)/6 + m²·n²(n²-1)/6 = m²n²(m²+n²-2)/6.
- Pitfalls:
  - Division by 6 must be modular inverse (mod 1e9+7), or divide before mod since m²(m²-1) is always divisible by 6 mathematically — safer to use modular inverse.
  - Binomial C(mn-2, k-2) with mn ≤ 1e5: multiplicative loop is fine; watch for k-2 > mn-2 edge (k ≤ mn guaranteed, so fine).
  - Overflow not an issue in Python but keep mod anyway.
  - Verify with examples: m=n=2,k=2: C(2,0)=1; pair sum = 4·4·(4+4-2)/6 = 16·6/6=16? Wait — that gives 16, but expected 8. Recheck: unordered pairs of cells in 2×2: 6 pairs, distances 1,1,1,1,2,2 → sum 8. My formula double counts: n² counts ordered column pairs, but for unordered cell pairs with rows i<j, columns are independent: n² pairs, that's correct (4 pairs per row pair, 2 row pairs at d=1 → 8 pairs... but there are only 4 horizontal adjacent pairs + ... hmm). Actually for rows i<j, cells (i,c1),(j,c2): n² = 4 pairs each with row-distance 1, total 2 row-pairs × 4 = 8 pair-instances with row distance 1 → row sum 8. Column sum similarly 8. Total 16, but actual Manhattan sum is 8. Error: each unordered cell pair's Manhattan distance = row diff + col diff, and exactly one of the two is nonzero only for same-row/same-column pairs. For pairs in different rows AND different columns, both contribute — that's fine. Recount: 2×2 pairs: 4 adjacent (dist 1) + 2 diagonal (dist 2) = 8. Row part: pairs in different rows: only the 2 diagonal pairs? No — rows differ for 4 pairs (top-bottom combos: 2×2=4 pairs), each row-distance 1 → row sum 4. My "2 row-pairs" was wrong: m=2 → only 1 pair of rows, d=1, m-d=1. Σ d(m-d) = 1. Formula m²(m²-1)/6 = 4·3/6 = 2. That's wrong! Correct formula: Σ_{d=1}^{m-1} d(m-d) = m(m²-1)/6, not m²(m²-1)/6. Check m=2: 2·3/6=1 ✓. So row sum = n²·m(m²-1)/6. For 2×2: 4·1=4 ✓. Total = 4+4=8 ✓. Example 2: m=1,n=4,k=3: C(2,1)=2. Pair sum: row part 0; column part = m²·n(n²-1)/6 = 1·4·15/6=10. Total = 2·10=20 ✓.
- Corrected formulas:
  - Row contribution sum over pairs = n² · m(m²-1)/6
  - Column contribution = m² · n(n²-1)/6
  - Answer = C(mn-2, k-2) · [n²·m(m²-1) + m²·n(n²-1)] / 6 mod p.

## worker: Implement the full solution: `comb(N, r)` via mult
- **Counting argument:** Every unordered pair of distinct cells appears in exactly `C(mn-2, k-2)` valid arrangements (fix those two cells, choose the remaining `k-2` pieces freely). Hence the answer equals `C(mn-2, k-2)` times the sum of Manhattan distances over all unordered pairs of cells.
- **Pair-distance sum:** Decomposes into row and column parts.
  - Row part: for row gap `d`, there are `m-d` row pairs and `n²` column choices per pair, contributing `n²·Σ d(m-d) = n²·m(m²-1)/6`.
  - Column part symmetric: `m²·n(n²-1)/6`.
  - (Note: the plan's draft had `m²(m²-1)/6`; the correct identity is `Σ_{d=1}^{m-1} d(m-d) = m(m²-1)/6`, confirmed by the 2×2 example.)
- **Implementation:** `comb` uses a multiplicative loop with a single modular inverse of the denominator (`mn ≤ 1e5`, so O(mn) worst case, fine). Division by 6 uses `pow(6, MOD-2, MOD)`.
- **Verification:** Matches both given examples (8 and 20) and brute-force enumeration over all grids with `mn ≤ 8` and all valid `k` — all passed.
