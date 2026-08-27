
## ideation
**Core difficulty:** We must sum Manhattan distances over *all* C(m·n, k) arrangements — an astronomically large set — so we need a combinatorial decomposition that avoids enumeration. Constraints: m, n ≤ 1e5 individually but m·n ≤ 1e5, so at least one dimension is small; factorials up to m·n are feasible.

**Key decomposition idea:**
- Manhattan distance = row-distance + column-distance. Sum each axis independently.
- For the row axis: consider a fixed pair of rows (r1, r2) with r1 < r2. A piece in row r1 and a piece in row r2 contribute (r2 − r1). Count arrangements containing at least one piece in each of these rows... but careful: a single arrangement may have *multiple* pieces in row r1 and row r2, and each cross-row pair of pieces contributes.

**Better formulation (pair of cells):** Sum over unordered pairs of cells {c1, c2} of dist(c1,c2) × (number of arrangements containing both cells). The number of arrangements containing both cells is C(m·n − 2, k − 2), independent of the cells! So:

**Answer = C(N−2, k−2) × (sum of Manhattan distances over all unordered pairs of cells)**, where N = m·n.

This reduces the problem to: compute S = Σ over all cell pairs of (|x1−x2| + |y1−y2|).

**Computing S:**
- Row part: for each pair of rows (i, j), distance |i−j|, there are n² pairs of cells (n choices of column for each cell). Row contribution = n² · Σ_{0≤i<j≤m−1} (j−i).
- Σ_{i<j} (j−i) for m rows = Σ_{d=1}^{m−1} d·(m−d) = m(m²−1)/6 (closed form: C(m+1,3)·... let me verify: Σ d(m−d) = m·Σd − Σd² = m·m(m−1)/2 − (m−1)m(2m−1)/6 = m(m−1)[3m − (2m−1)]/6 = m(m−1)(m+1)/6 = m(m²−1)/6. ✓)
- Similarly column part = m² · n(n²−1)/6.
- S = n²·m(m²−1)/6 + m²·n(n²−1)/6.

**Verification with Example 1:** m=n=2, k=2. N=4, C(2,0)=1. S = 4·2·3/6 + 4·2·3/6 = 4+4 = 8. ✓

**Verification with Example 2:** m=1, n=4, k=3. N=4, C(2,1)=2. Row part: 16·1·0/6 = 0. Column part: 1·4·63/6 = 42. S=42. Answer = 2·42 = 84?? Expected 20. ✗ — wait, recheck: column formula is m²·n(n²−1)/6 = 1·4·(64−1)/6 = 4·63/6 = 42. Hmm, 2·42=84 ≠ 20. Let me recheck: direct sum over pairs of cells in a 1×4 row: distances: pairs with d=1: 3 pairs, d=2: 2 pairs, d=3: 1 pair → 3+4+3=10. So S should be 10, not 42. Error: n(n²−1)/6 with n=4 gives 4·15/6=10 ✓ (I miscomputed 4³−4 = 60, not 63). So S = 1·10 = 10, answer = C(2,1)·10 = 20. ✓

**Pitfalls:**
- Modular division by 6: use modular inverse (mod = 1e9+7 is prime), or divide before modding carefully (m(m²−1) is always divisible by 6? m(m−1)(m+1) is a product of 3 consecutive integers → divisible by 6 ✓). Safer: use pow(6, mod−2, mod) or divide the integer product since m,n ≤ 1e5 → m³ ≤ 1e15 fits in Python int anyway (Python has arbitrary precision, so just compute integer then mod).
- k can equal N: then C(N−2, k−2) = C(N−2, N−2) = 1, fine. k ≥ 2 guaranteed.
- Edge case k=2: C(N−2, 0) = 1 ✓.
- Need binomial C(N−2, k−2) mod p with N ≤ 1e5: precompute factorials or use multiplicative formula. Factorials up to 1e5 are fine.
- Note: pieces are identical, arrangements are subsets of cells — consistent with C(N,k) counting. ✓

**Complexity:** O(N) for factorial precomputation (or O(k) multiplicative), O(1) for the closed-form sums. Totally fine.

## worker: Implement `distanceSum` per the derived formula an
- **Derivation:** Pieces are identical, so arrangements = k-subsets of the N = m·n cells. For any unordered pair of cells {c1, c2}, the number of arrangements containing both is C(N−2, k−2), independent of which cells they are. Hence answer = C(N−2, k−2) · Σ_{pairs} dist(c1, c2).
- **Pair-distance sum:** Manhattan distance splits by axis. For rows: each pair of rows (i, j) with distance d = j−i contributes d for each of the n² column choices; Σ_{i<j}(j−i) = Σ_d d(m−d) = m(m²−1)/6 (product of 3 consecutive integers, exactly divisible by 6). Symmetrically for columns.
- **Exactness:** m, n ≤ 1e5 so m³ ≤ 1e15; Python integers are arbitrary precision, and `m*(m*m-1)` is always divisible by 6, so `// 6` is exact. `math.comb` is exact; modulo applied at the end.
- **Verification:**
  - Example 1 (m=n=2, k=2): C(2,0)=1; row part = 4·(2·3/6)=4, col part = 4 → total 8 → answer 8 ✓
  - Example 2 (m=1, n=4, k=3): C(2,1)=2; row part = 16·0 = 0, col part = 1·(4·15/6)=10 → 2·10 = 20 ✓
  - Brute-force cross-check (mentally/structurally): for 2×3, k=2: N=6, C(4,0)=1; row part = 9·(2·3/6)=9, col part = 4·(3·8/6)=16 → 25. Direct enumeration of all 15 pairs of cells in a 2×3 grid yields total distance 25 ✓ (pairs: horizontal 3 per row ×2 rows ×d=1 → 6; vertical 3 pairs ×d=1 → 3; diagonal cross-row pairs: 6 pairs with column diff 1 → 6·2=12, 2 pairs with column diff 2 → 2·3=6; total 6+3+12+... let me just trust the formula: 9+16=25, and enumeration: same-row pairs: 2 rows × (d1:2 pairs, d2:1 pair) = 2·(2+2)=8; cross-row pairs: 9 pairs, column diffs 0,1,2 with counts 3,4,2 → distances 1,2,3 → 3+8+6=17; total 8+17=25 ✓).
- **Edge cases:** k = N → C(N−2, N−2) = 1 ✓; k = 2 → C(N−2, 0) = 1 ✓; m = 1 or n = 1 → the corresponding axis term is 0 ✓.
- **Complexity:** O(1) time and space (math.comb on N ≤ 1e5 is fast).
