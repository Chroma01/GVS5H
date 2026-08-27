
## ideation
The problem requires finding prefix lengths `R_i` (row) and `C_j` (column) where cell `(i,j)` is black iff `j ≤ R_i` AND `i ≤ C_j`. 

For each row `i`: `R_i` must be in `[a_i, b_i]` where `a_i = max{y : (i,y) is B}` (0 if none) and `b_i = min{y-1 : (i,y) is W}` (N if none). Similarly for columns with `c_j, d_j`.

Necessary: `a_i ≤ b_i` and `c_j ≤ d_j` for all rows/columns.

Sufficient: For every precolored W cell `(x,y)`, it must NOT be forced black. Since `R_x ≥ a_x` and `C_y ≥ c_y`, the cell is forced black iff `a_x ≥ y` AND `c_y ≥ x`. So we need: for all W cells, NOT (`a_x ≥ y` AND `c_y ≥ x`).

This is the complete condition. N can be up to 1e9 but only M ≤ 2e5 cells matter. We only need to track rows/columns that appear in the M cells; others get `a=0, b=N, c=0, d=N`.

## worker: Implement the solution in Python: read N, M and th
The solution uses the key insight that each row `i` has a black prefix length `R_i` and each column `j` has a black prefix length `C_j`. A cell `(i,j)` is black iff `j ≤ R_i` AND `i ≤ C_j`. For precolored cells, we derive constraints: B cells force `R_x ≥ y` and `C_y ≥ x`; W cells force `R_x ≤ y-1` OR `C_y ≤ x-1`. For each row we track `[a_i, b_i]` (min/max allowed `R_i`) and similarly for columns. The feasibility reduces to: (1) all row/column intervals are non-empty, and (2) no W cell is forced black, i.e., no W cell `(x,y)` with `a_x ≥ y` and `c_y ≥ x`. The algorithm is O(M) using dicts; N up to 1e9 is handled implicitly via default values.
