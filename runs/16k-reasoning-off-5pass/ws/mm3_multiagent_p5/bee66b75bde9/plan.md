The condition means each row has a prefix of black cells (length `r_i`) and each column has a prefix of black cells (length `c_j`). A cell `(i,j)` is black iff `j ≤ r_i` AND `i ≤ c_j`. So a cell is forced white if either `j > r_i` or `i > c_j`. Equivalently, a cell is black iff `r_i ≥ j` and `c_j ≥ i`.

We need to find integers `r_i ∈ [0,N]` and `c_j ∈ [0,N]` consistent with all precolored cells. For a precolored cell `(x,y)`:
- If it's B: we need `r_x ≥ y` and `c_y ≥ x`.
- If it's W: we need `r_x ≤ y-1` or `c_y ≤ x-1` (i.e., not both `r_x ≥ y` and `c_y ≥ x`).

This is a 2-SAT-like feasibility problem. Key observation: define `R_i = r_i`, `C_j = c_j`. Constraints:
- B at (x,y): `R_x ≥ y` and `C_y ≥ x`.
- W at (x,y): `R_x ≤ y-1` OR `C_y ≤ x-1`.

For each row `i`, let `R_min[i] = max y over B cells in row i` (or 0), `R_max[i] = min(y-1) over W cells in row i` (or N). Need `R_min[i] ≤ R_max[i]`.
Similarly for columns: `C_min[j] = max x over B cells in col j`, `C_max[j] = min(x-1) over W cells in col j`.

But these alone aren't sufficient because W constraints couple rows and columns. However, we can solve via a clever reduction: the problem is equivalent to checking if there exist `R_i, C_j` satisfying all. 

A known approach: For each row, compute the tightest constraint. For each column, compute the tightest constraint. Then check feasibility by iterating: the answer is "Yes" iff for every precolored W cell `(x,y)`, it's not the case that both `R_x ≥ y` and `C_y ≥ x` are forced. 

Actually, the clean solution: 
- For each row `i`, let `a_i = max{y : (i,y) is B}` (0 if none), `b_i = min{y-1 : (i,y) is W}` (N if none). Need `a_i ≤ b_i`.
- For each column `j`, let `c_j = max{x : (x,j) is B}` (0 if none), `d_j = min{x-1 : (x,j) is W}` (N if none). Need `c_j ≤ d_j`.

But these row/column independent checks are necessary but not sufficient. We need the joint check.

The correct approach: We need `R_i ∈ [a_i, b_i]` and `C_j ∈ [c_j, d_j]`. For a W cell `(x,y)`: need `R_x ≤ y-1` OR `C_y ≤ x-1`. This means: if `R_x ≥ y` (i.e., `a_x ≥ y` and we choose `R_x ≥ y`), then we need `C_y ≤ x-1`. 

Algorithm: 
1. Compute `a_i, b_i` for rows and `c_j, d_j` for columns.
2. Check `a_i ≤ b_i` and `c_j ≤ d_j` for all.
3. For each W cell `(x,y)`: if `a_x ≥ y` AND `c_y ≥ x`, then impossible. Because any valid `R_x ≥ a_x ≥ y` and `C_y ≥ c_y ≥ x`, making the cell black — contradiction.

Wait, but `R_x` could be chosen less than `a_x`? No, `a_x` is the minimum required. So `R_x ≥ a_x`. Similarly `C_y ≥ c_y`. So if `a_x ≥ y` and `c_y ≥ x`, the cell must be black, contradicting W.

So the condition is: for every W cell `(x,y)`, NOT (`a_x ≥ y` AND `c_y ≥ x`).

Let me verify with samples:
Sample 1: N=4. B at (4,1),(1,3). W at (3,2).
- Row 4: a=1 (from (4,1)B), b=N=4. 
- Row 1: a=3, b=4.
- Row 3: a=0, b=1 (from (3,2)W, y-1=1).
- Row 2: a=0, b=4.
- Col 1: c=4 (from (4,1)B), d=4.
- Col 2: c=0, d=2 (from (3,2)W, x-1=2).
- Col 3: c=1, d=4.
- Col 4: c=0, d=4.
Check W (3,2): a_3=0 < 2, so condition holds. Yes.

Sample 2: N=2. W at (1,2), B at (2,2).
- Row 1: a=0, b=1.
- Row 2: a=2, b=2.
- Col 2: c=2, d=1 (from (1,2)W, x-1=0... wait (1,2)W means x=1, so x-1=0). Actually d_2 = min(x-1) over W in col 2 = min(0) = 0. c_2 = max(x) over B in col 2 = 2. So c_2=2 > d_2=0. Fail. No.

Sample 4: should give No. The algorithm should detect it.

This is the standard solution for this AtCoder problem (ABC 309 E or similar — actually it's "Takahashi's Basics in Education and Learning" or "Grid Coloring"... I recall this is ABC 309 or similar).

Let me code this up.