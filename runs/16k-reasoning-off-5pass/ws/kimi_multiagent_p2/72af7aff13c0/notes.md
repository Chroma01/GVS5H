
## ideation
We must maintain F = Σ over monotone paths of Π A_cells under Q=2e5 point updates, where the updated cell is always adjacent to the previous one (Takahashi walks). Since HW ≤ 2e5, the smaller dimension s = min(H,W) ≤ 447. Key structural facts discovered:

1. **Transfer-matrix view**: orient so H=s ≤ W=n (transpose if needed, remapping directions L↔U? no—L/R↔U/D appropriately). Column-to-column DP: g(·,j)[c] = A_{c,j}·(g(·,j−1)[c] + g(·,j)[c−1]), i.e. g(·,j) = T_j·g(·,j−1) with T_j upper-triangular. Crucially, applying T_j (or its transpose) to a vector is a simple O(s) first-order recurrence (running value), NOT O(s²). Full matrix products are never needed.

2. **Answer factorization**: F = Rrow[j+1] · Lpre[j], where Lpre[j] = T_j···T_1·e₁ (prefix DP vector at current column) and Rrow[j+1] = e_Hᵀ·T_W···T_{j+1} (suffix row vector). Update at column j only affects T_j, so Rrow[j+1] stays valid; recompute Lpre[j] from Lpre[j−1] in O(s), then F = dot(Rrow[j+1], Lpre[j]) in O(s).

3. **Validity frontiers give O(s) amortized/worst-case per query**: store Lpre[0..W] and Rrow[1..W+1] (total memory O(HW) ≤ 2e5). Update at column j invalidates Lpre[k] for k>j and Rrow[k] for k≤j. Since the pointer moves ≤1 column per query and we always refresh Lpre[j] (and Rrow[j] when moving left) at the visited column, the needed neighbor vectors are always valid — no cascades. Moves U/D cost O(1) bookkeeping; every query is O(s).

4. Total: O(HW + Q·min(H,W)) ≤ ~9e7 modular ops — fine in C++, tight in Python; numpy is awkward (sequential mod-recurrence, cumprod overflow), so use PyPy-style tight loops, precomputed local references, and fast I/O. Zeros in A are handled naturally by the recurrence (no inverses needed — avoid any division-based formulation).

## worker: Implement the full solution: input parsing with op
- **Orientation**: If H > W, transpose the grid so the DP row-dimension `s = min(H,W) ≤ 447`; directions remap U↔L, D↔R (a path down/right in the transposed grid corresponds to right/down in the original).
- **DP vectors**: `Lpre[j][c] = A_{c,j}·(Lpre[j-1][c] + Lpre[j][c-1])` (prefix path-product sums ending at row c of column j), `Rrow[j][r] = A_{r,j}·(Rrow[j+1][r] + Rrow[j][r+1])` (suffix sums starting at row r of column j). Each column transition is an O(s) first-order recurrence — no matrix products, no divisions (zeros in A are fine).
- **Answer**: F = Σ_r Rrow[j+1][r]·Lpre[j][r], since every path crosses column j exactly once.
- **Validity invariant**: an update at column j only invalidates Lpre[k] (k>j) and Rrow[k] (k≤j). Since the pointer moves ≤1 column per query: Lpre[j-1] and Rrow[j+1] are always valid when needed; after a left move into column j we refresh Rrow[j] from the still-valid Rrow[j+1] in O(s). Hence every query costs O(s) with no cascades.
- **Complexity**: O(HW + Q·min(H,W)) ≤ ~9e7 modular ops worst case; memory O(HW).
- **Verification**: Sample 1 produces 456/666/822 (matches). Sample 2 produces 299123226, 548055393, 810247224, 876210800, 773990840, 506814544 (matches). Also cross-checked against a brute-force O(HW)-per-query DP on random small grids (including H>W to exercise the transpose path, zero values, and random walks) — all matched.
