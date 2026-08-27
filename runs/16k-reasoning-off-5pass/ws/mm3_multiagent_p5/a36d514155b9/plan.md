We need the sum of Manhattan distances over all unordered pairs of pieces, summed across every way to place k indistinguishable pieces on distinct cells of an m×n grid.

For Manhattan distance |x_i-x_j|+|y_i-y_j|, by linearity the total sum equals:
- (number of arrangements) × (sum over unordered pairs of expected |x_i-x_j|) 
- similarly for y.

Number of arrangements = C(mn, k). Let S = total cells = mn.

**Row contribution.** Choose a row r (0-indexed). The number of arrangements where a given pair of pieces lies in row r with distance d in columns is: choose the two columns, the remaining k-2 pieces from other rows.

Expected column absolute difference across all unordered pairs: E|X1-X2| where X1, X2 are distinct uniformly random cells among mn.
- Total sum over unordered pairs of |x_i - x_j| across all placements = C(S-2, k-2) × Σ_{i<j} |col_i - col_j| over all cell pairs in the grid.
But simpler: Expected |col difference| = (1/ S) × Σ_r count_in_row_r × … Actually, use indicator: for each pair of cells, |x_i-x_j| contributes. Σ_{cells} x_coord = n · (0+1+…+(m-1)) = n·m(m-1)/2.
Sum over unordered pairs of |row difference| = Σ_{a<b} (row_b - row_a) · (cells_in_row_a)·(cells_in_row_b) / (per pair) but since all cells in same row share row coordinate, distance depends only on row values.

Cleanest formula: Pick the two distinguished pieces uniformly among all C(S,2) cell-pairs. E|Δrow| = (2 / (S·(S-1))) · Σ_{r} r · (cells with row < r)·(cells with row ≥ r)... 

Better closed form:
Let R_i be row of cell i (0..m-1), each row has n cells.
Σ_{pairs} |R_i - R_j| = n² · Σ_{0≤a<b<m} (b-a) + n·(S-n)·Σ_{0≤a<m} a
Because: pairs both in rows a,b: contributes n²·(b-a). Pairs in row a vs any other row: each cell in row a (n cells) pairs with cells not in row a (S-n), contributes |a - other_row|. But that's still complex.

Simplest: Let T = Σ over all ordered distinct pairs (i,j) of (R_j - R_i) with R_j ≥ R_i = Σ_{r} r·(cells with row ≤ r)·(cells with row > r)... 

Actually do it directly:
- Pairs with different rows: for row a < b, contribution per pair = (b-a). #pairs between row a and row b = n·n = n². Total = n² Σ_{a<b}(b-a) = n² · [Σ_b b·b - Σ_b b·(b-1)/...]. Known: Σ_{a<b}(b-a) = m(m²-1)/6.
- So inter-row pairs total = n² · m(m²-1)/6.
- Pairs within same row: contribution 0.

So E|Δrow| = n²·m(m²-1)/6 / C(S,2) = n²·m(m²-1)/(6·S·(S-1)/2) = n²·m(m²-1)/(3·S·(S-1)).

Similarly E|Δcol| = m²·n(n²-1)/(3·S·(S-1)).

Total sum = C(S,k) · [E|Δrow| + E|Δcol|] · C(k,2) ... wait.

Let me redo. We want Σ over all arrangements of Σ_{pairs in arrangement} (|Δrow|+|Δcol|).

= Σ_{unordered cell-pairs (a,b)} |Δrow(a,b)+Δcol(a,b)| · (number of arrangements containing both a and b)
= Σ_{cell-pairs} dist(a,b) · C(S-2, k-2)

So total = C(S-2, k-2) · Σ_{all cell-pairs} dist(a,b).

Σ_{cell-pairs} dist = Σ_row_part + Σ_col_part.
Row part = n² · m(m²-1)/6.
Col part = m² · n(n²-1)/6.

Answer = C(S-2, k-2) · [n²·m(m²-1)/6 + m²·n(n²-1)/6] mod (10^9+7).

Precompute factorials up to S = m·n ≤ 10^5.