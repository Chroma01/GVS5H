We need the sum of Manhattan distances over all unordered pairs of pieces across every placement of k indistinguishable pieces on an m×n grid, at most one per cell.

Key observations:
- Manhattan distance separates into |Δx| + |Δy|, so total sum = sum of row-contribution + column-contribution.
- For a fixed unordered pair of cells, its contribution to the answer is the number of placements containing both cells.
- Number of placements of k pieces containing a specific pair = C(mn-2, k-2). Since this factor is the same for all pairs, we can compute:
  answer = C(mn-2, k-2) * (sum over all unordered pairs of cells of Manhattan distance).
- So we need S = sum_{i<j} (|x_i-x_j| + |y_i-y_j|) for the complete grid.
  Compute row part and column part independently (grid is a product of coordinates).
- For a 1D line of length L (cells 0..L-1), the sum of |i-j| over all unordered pairs is a known formula:
  Pairs at distance d: (L-d) pairs. Total = sum_{d=1}^{L-1} d*(L-d) = (L^3 - L)/6.
- So sum over rows contribution: n * sum_{pairs of rows} |r1 - r2| where r1, r2 in 0..m-1, each unordered pair contributes n*n in column (since for each row pair, any column with another column gives n^2 cells). Actually the row contribution from positions is: choose two distinct rows (r1, r2), the number of cell pairs with those rows is n * n (column1 from first, column2 from second). So row part = n^2 * sum_{r1<r2} |r1-r2| = n^2 * (m^3 - m)/6.
- Similarly column part: m^2 * (n^3 - n)/6.
- Therefore S = n^2 * (m^3 - m)/6 + m^2 * (n^3 - n)/6.
- Final answer = C(mn-2, k-2) * S mod (1e9+7).
- Compute combination mod p using precomputed factorials up to mn.

Since m,n up to 1e5, mn up to 1e5, factorials up to 1e5 are fine.

Time O(mn) for precomputing factorials; modular inverses with Fermat.