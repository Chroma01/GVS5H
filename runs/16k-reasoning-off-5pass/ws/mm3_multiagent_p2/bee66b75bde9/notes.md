
## ideation
The problem requires coloring an N×N grid such that each row is a prefix of black cells followed by white cells, and each column is also a prefix of black cells followed by white cells. This is equivalent to choosing row thresholds R_i and column thresholds C_j where cell (i,j) is black iff j ≤ R_i and i ≤ C_j. Precolored cells impose constraints: black at (i,j) requires R_i ≥ j and C_j ≥ i; white at (i,j) requires R_i ≤ j-1 and C_j ≤ i-1.

These constraints decouple into independent intervals for each row and each column. For a row i, define:
- L_i = max column index of a black cell in row i (or -1 if none)
- W_i = min column index of a white cell in row i (or N+1 if none)
We need L_i < W_i whenever both exist (i.e., row has both black and white cells). Similarly for columns:
- T_j = max row index of a black cell in column j (or -1 if none)
- B_j = min row index of a white cell in column j (or N+1 if none)
We need T_j < B_j whenever both exist.

If these conditions hold for all rows and columns that have both colors, we can always pick R_i and C_j within the allowed intervals to satisfy all precolored cells. The intervals are non-empty exactly when the inequalities hold. Thus the problem reduces to checking these per-row and per-column inequalities.

## worker: <omitted because status is done>
The solution models the problem using row thresholds \(R_i\) and column thresholds \(C_j\). Each precolored cell imposes a simple inequality: black at \((i,j)\) requires \(R_i \ge j\) and \(C_j \ge i\); white at \((i,j)\) requires \(R_i \le j-1\) and \(C_j \le i-1\). These constraints separate into independent intervals for each row and column. A row \(i\) can be satisfied iff the rightmost black cell (if any) lies strictly to the left of the leftmost white cell (if any). The same holds for columns. If all such pairwise checks pass, we can always pick thresholds within the allowed intervals (e.g., \(R_i = \max\) black column, \(C_j = \max\) black row, etc.) to satisfy every precolored cell. The algorithm runs in \(O(M)\) time and uses \(O(M)\) memory, well within limits.
