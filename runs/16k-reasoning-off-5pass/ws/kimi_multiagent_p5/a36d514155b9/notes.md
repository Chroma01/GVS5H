
## ideation
**Core difficulty:** The number of arrangements C(mn, k) is astronomically large, so we cannot enumerate. We need a counting argument that aggregates distances combinatorially, plus modular arithmetic (division → modular inverse).

**Key insight (linearity of summation over pairs):**
- Total answer = Σ over arrangements Σ over pairs of pieces (distance).
- Swap the order: Σ over unordered cell-pairs {c1, c2} of dist(c1,c2) × (number of arrangements where both c1 and c2 are occupied).
- For any fixed pair of cells, the number of arrangements containing both is C(mn−2, k−2) — a constant independent of which pair. So:
  **answer = C(mn−2, k−2) × S**, where S = sum of Manhattan distances over all unordered pairs of distinct cells.

**Computing S:** Manhattan distance splits into x-part + y-part.
- x-part: for each pair of rows (r1, r2) with |r1−r2| = d, there are n choices of column for each cell → n² pairs of cells. Number of row-pairs at distance d is (m−d). So x-part = n² · Σ_{d=1}^{m−1} d(m−d).
- Σ_{d=1}^{L−1} d(L−d) = L·Σd − Σd² = L²(L−1)/2 − (L−1)L(2L−1)/6 = L(L²−1)/6. (Verify: L=2 → 2·3/6=1 ✓; L=4 → 4·15/6=10, and 1·3+2·2+3·1=10 ✓.)
- Similarly y-part = m² · n(n²−1)/6.
- S = n²·m(m²−1)/6 + m²·n(n²−1)/6.

**Sanity checks against examples:**
- Ex1: m=n=2, k=2. S = 4·2·3/6 + 4·2·3/6 = 4+4 = 8. C(2,0)=1. Answer 8 ✓.
- Ex2: m=1, n=4, k=3. S = 16·0 + 1·4·15/6 = 10. C(2,1)=2. Answer 20 ✓.

**Pitfalls:**
- Division by 6 must be done via modular inverse (or divide before mod since L(L²−1) is always divisible by 6 — but safer to use pow(6, MOD−2, MOD)).
- Overflow isn't an issue in Python, but keep everything mod 10^9+7 anyway.
- Edge cases: m=1 or n=1 (one term vanishes — formula handles it since L(L²−1)=0 when L=1); k=2 → C(mn−2, 0)=1; k=mn → C(mn−2, k−2) still fine.
- Factorials up to mn ≤ 10^5 — trivially cheap. Could even compute C(mn−2, k−2) directly with a small loop, but factorial + inverse is clean.

**Complexity:** O(mn) for factorials (≤10^5), O(1) for the rest. Well within limits.

## worker: Implement the full `distanceSum` solution in Pytho
- **Counting argument:** Total answer = Σ over arrangements Σ over piece-pairs dist. Swapping summation order: each unordered pair of cells {c1, c2} contributes dist(c1,c2) × (number of arrangements containing both cells). The latter is C(mn−2, k−2), constant for all pairs. So answer = C(mn−2, k−2) × S, where S = sum of Manhattan distances over all unordered cell pairs.
- **Computing S:** Manhattan distance splits into row and column parts. Row part: for row pairs at distance d there are (m−d) row pairs and n² column choices, giving n²·Σ_{d=1}^{m−1} d(m−d) = n²·m(m²−1)/6 (closed form verified: L=2→1, L=4→10). Column part symmetric: m²·n(n²−1)/6. Division by 6 uses modular inverse.
- **Binomial:** factorials + inverse factorials up to mn ≤ 10⁵, O(mn) time, O(mn) memory — trivially fast.
- **Verification:**
  - m=2, n=2, k=2: S = 4·(2·3)/6 + 4·(2·3)/6 = 4+4 = 8; C(2,0)=1 → 8 ✓
  - m=1, n=4, k=3: S = 0 + 1·(4·15)/6 = 10; C(2,1)=2 → 20 ✓
  - m=1, n=2, k=2: S = 0 + 1·(2·3)/6 = 1; C(0,0)=1 → 1 ✓
  - m=1, n=3, k=3: S = 0 + 1·(3·8)/6 = 4; C(1,1)=1 → 4 ✓
- Edge cases handled: m=1 or n=1 makes the corresponding term vanish naturally (L(L²−1)=0 at L=1); k=2 gives C(mn−2, 0)=1; k=mn works fine.
