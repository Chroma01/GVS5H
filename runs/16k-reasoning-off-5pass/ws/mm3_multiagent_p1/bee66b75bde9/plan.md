We need to decide if there exists a binary matrix where each row is a prefix of B then suffix of W, and each column is a prefix of B then suffix of W. Equivalently, there exist row thresholds `r_i` (number of black cells in row i) and column thresholds `c_j` (number of black cells in column j) such that cell (i,j) is black iff `j ≤ r_i` and `i ≤ c_j`. So the matrix is determined by the vectors `r` and `c`. A precolored cell (i,j) with color B forces `j ≤ r_i` and `i ≤ c_j`; color W forces `j > r_i` or `i > c_j` (i.e., not both). We need to check if there exist integer vectors `r_i ∈ [0,N]` and `c_j ∈ [0,N]` satisfying all constraints. This is a 2-SAT-like feasibility problem on a bipartite graph. We can solve it by checking consistency of upper/lower bounds derived from constraints.

For each row i, let `Rmax_i` = max j among black cells in row i (or 0 if none), and `Rmin_i` = min j among white cells in row i (or N+1 if none). Then we need `Rmax_i ≤ r_i < Rmin_i`. For each column j, `Cmax_j` = max i among black cells in column j (or 0), `Cmin_j` = min i among white cells in column j (or N+1). Need `Cmax_j ≤ c_j < Cmin_j`.

Now we need to find `r_i, c_j` in those ranges such that the matrix is consistent: cell (i,j) is black iff both conditions hold. The only potential conflict is when a cell is forced black by one side but white by the other. Specifically, if there exists a black cell (i,j) with `j > r_i` or `i > c_j` — impossible. But since we choose `r_i ≥ Rmax_i` and `c_j ≥ Cmax_j`, any black cell (i,j) has `j ≤ Rmax_i ≤ r_i` and `i ≤ Cmax_j ≤ c_j`, so it's fine. For white cells, we need at least one of `j > r_i` or `i > c_j`. If a white cell has `j ≤ r_i` and `i ≤ c_j`, it would be black — contradiction. So we need: for every white cell (i,j), either `r_i < j` or `c_j < i`. Equivalently, we cannot have `r_i ≥ j` and `c_j ≥ i` simultaneously for any white cell.

This is a classic problem: we have intervals for `r_i` and `c_j`, and forbidden pairs. We can solve greedily: sort rows by `Rmin_i` (the point where they must become white), and assign `r_i` as small as possible but ≥ `Rmax_i`. Similarly for columns. But we need to ensure the white-cell constraints.

A known solution: process rows in order of `Rmin_i` ascending. Maintain a set of columns whose `Cmin_j` is still ≥ current row index. For each row, assign `r_i = max(Rmax_i, current_r)`. Then for each column j with `Cmax_j ≤ i` and `Cmin_j > i`, we must ensure that if `r_i ≥ j`, then column j's threshold `c_j` must be < i. This can be enforced by tracking the minimum `c_j` needed.

Actually, there's a simpler approach: we can binary search on a value `k` (the number of black rows/columns). But N is up to 1e9, so we need O(M log M) or O(M).

Let's think differently. The condition is equivalent to: there exists a monotone matrix. This is known as "Young diagram" or "staircase". The constraints define a partial order. We can check feasibility by verifying that the set of black cells is "order ideal" (downward closed) and white cells are "order filter" (upward closed) in the product order (i,j) ≤ (i',j') iff i ≤ i' and j ≤ j'. Actually, the condition says: black cells form a Young diagram (Ferrers diagram) anchored at top-left. So the set of black cells must be a "down-right" closed set: if (i,j) is black, then all (i',j') with i' ≤ i, j' ≤ j must be black. White cells must be "up-left" closed: if (i,j) is white, then all (i',j') with i' ≥ i, j' ≥ j must be white.

So we just need to check that the precolored cells satisfy these closure properties. If they do, we can always extend to a full grid (by taking the maximal black set consistent with white constraints). If not, impossible.

Let's verify: The condition "for every row, leftmost i cells black, rest white" means the black cells in each row are a prefix. Combined with column condition, the set of black cells is exactly a Young diagram: there exists a non-increasing sequence of row lengths. Equivalently, the set of black cells is a "order ideal" in the poset where (i,j) ≤ (i',j') iff i ≤ i' and j ≤ j'. Because if (i,j) is black, then all cells above and to the left must be black. Conversely, any order ideal can be represented by row thresholds.

So the problem reduces to: given some cells colored B or W, does there exist an order ideal (down-set) of the grid such that all B cells are in it and all W cells are not? This is possible iff:
1. For any B cell (i,j), all cells (i',j') with i' ≤ i, j' ≤ j that are precolored W must not exist. (i.e., no W cell is "above-left" of a B cell).
2. For any W cell (i,j), all cells (i',j') with i' ≥ i, j' ≥ j that are precolored B must not exist. (i.e., no B cell is "below-right" of a W cell).

These two conditions are actually equivalent (one implies the other by contrapositive). So we just need to check that there is no pair (i1,j1) colored B and (i2,j2) colored W with i1 ≥ i2 and j1 ≥ j2 (i.e., B is down-right of W). Or equivalently, no B cell is "dominated" by a W cell in the product order (where B ≤ W means B is up-left of W). Wait: B is down-right of W means i_B ≥ i_W and j_B ≥ j_W. So we need: for all B and W, NOT (i_B ≥ i_W and j_B ≥ j_W). That is, for every B and W, either i_B < i_W or j_B < j_W.

This is a simple check: we need to ensure that the maximum row index among B cells in each column... Actually, we can just check pairwise? M up to 2e5, pairwise is too slow. But we can do it efficiently.

We need to check if there exists a B cell (i1,j1) and a W cell (i2,j2) such that i1 ≥ i2 and j1 ≥ j2. This is equivalent to: the set of B cells and W cells are "separable" by a monotone boundary. This is exactly the condition that the "upper envelope" of B cells and "lower envelope" of W cells don't cross.

Define for each column j: `maxB_row[j]` = max i such that (i,j) is B (or 0 if none). For each column j: `minW_row[j]` = min i such that (i,j) is W (or N+1 if none). Then we need that for all j, `maxB_row[j] < minW_row[j]`. Because if there is a column where a B cell is below a W cell, that's a violation. But wait, the condition is about pairs (i1,j1) B and (i2,j2) W with i1 ≥ i2 and j1 ≥ j2. If we fix column j, we need max B row < min W row. But what about different columns? If B is at (i1, j1) and W at (i2, j2) with j1 > j2, then i1 ≥ i2 and j1 ≥ j2. This is also a violation. So we need a stronger condition: the "staircase" boundary must separate them.

Actually, the condition "no B is down-right of W" is equivalent to: the set of B cells is an order ideal and W cells is an order filter. This is equivalent to: for every B cell (i,j), the rectangle [1..i] x [1..j] contains no W cell. And for every W cell (i,j), the rectangle [i..N] x [j..N] contains no B cell. These are equivalent.

We can check this by verifying that the "frontier" defined by B cells is above the frontier defined by W cells. Specifically, define `f_B(j) = max{ i | (i,j) is B }` (0 if none). Define `f_W(j) = min{ i | (i,j) is W }` (N+1 if none). The condition that no B is down-right of W is equivalent to: for all j, `f_B(j) < f_W(j)`. Because if there is a B at (i1,j1) and W at (i2,j2) with i1 ≥ i2 and j1 ≥ j2, then taking j = j1, we have f_B(j1) ≥ i1 ≥ i2. But f_W(j1) ≤ i2? Not necessarily, because the W might be in a different column. Wait, if j1 > j2, then f_W(j1) might be N+1 (no W in column j1). So the condition f_B(j) < f_W(j) for all j is sufficient but not necessary? Let's test: B at (2,2), W at (1,1). Then f_B(2)=2, f_W(2)=N+1 (no W in col 2). So f_B(2) < f_W(2) holds. But B is down-right of W? i_B=2 ≥ i_W=1, j_B=2 ≥ j_W=1. Yes, violation. So f_B(j) < f_W(j) for all j is NOT sufficient. We need a global condition.

The correct condition is: the "upper boundary" of B cells (as a monotone non-increasing function) must be strictly above the "lower boundary" of W cells (as a monotone non-decreasing function). Actually, the set of B cells must be contained in the set of cells that are above-left of some monotone boundary, and W cells must be below-right. This is exactly the condition that the partial order is respected.

We can check this by verifying that the maximum row index among B cells in the submatrix [1..i] x [1..j] is less than the minimum row index among W cells in the complement? Not exactly.

A known solution for this problem (from AtCoder ABC 233 Ex? No, this is ABC 247 Ex? Actually it's "Make Bipartite" or similar. Wait, this is "Grid Coloring" problem. I recall a problem: "Takahashi wants to paint grid" from AtCoder. The solution is to check that for every B cell (i,j), there is no W cell (i',j') with i' ≤ i and j' ≤ j. And for every W cell (i,j), there is no B cell (i',j') with i' ≥ i and j' ≥ j. This can be checked by scanning.

Specifically, we can compute for each cell (i,j) the maximum row index of a B cell in the rectangle [1..i] x [1..j], and the minimum row index of a W cell in the rectangle [i..N] x [j..N]. But N is up to 1e9, so we cannot iterate over all cells. We only have M up to 2e5 precolored cells.

We need to check the condition on the precolored cells only? No, because uncolored cells can be chosen to satisfy the condition. So we only need to ensure that there is no conflict among precolored cells. The condition is: there does not exist a B cell (i1,j1) and a W cell (i2,j2) such that i1 ≥ i2 and j1 ≥ j2. Because if such a pair exists, no matter how we color the rest, the condition fails. Conversely, if no such pair exists, we can always fill the rest. Is that true?

Let's think: Suppose we have B at (2,2) and W at (1,1). This is a conflict. What if we have B at (1,2) and W at (2,1)? i1=1 < i2=2, j1=2 > j1=1. So i1 < i2 but j1 > j2. This is not a conflict because neither dominates the other. Can we fill the rest? We need a Young diagram. B at (1,2) means row 1 has at least 2 black cells. W at (2,1) means column 1 has at most 1 black cell (since row 2 is white, so column 1's black prefix length is at most 1). This is consistent: row 1: B B, row 2: W W? But column 1 would be B, W which is fine (prefix of 1 black). Column 2: B, W? Row 1 col 2 is B, row 2 col 2 is uncolored. We can color it W. Then column 2 has B, W which is fine. So yes, it's possible. So the condition is exactly: no B cell is "down-right" of a W cell. That is, the set of B cells and W cells are separable by a monotone boundary.

So the problem reduces to: given M points with colors B or W, does there exist a monotone boundary (a non-increasing step function) that separates B (above-left) from W (below-right)? This is possible iff for every B point (i1,j1) and every W point (i2,j2), we do NOT have i1 ≥ i2 and j1 ≥ j2. Equivalently, for every B point, all W points must be either above it (i2 < i1) or to the left (j2 < j1). This is a classic problem: check if the "upper envelope" of B and "lower envelope" of W cross.

We can solve this by checking the following: sort B cells by row descending, and W cells by row ascending, or something. Actually, we can compute the "frontier" of B cells: for each column j, the maximum row of a B cell. But we need to compare across columns.

A known solution: Let `maxB_in_prefix(i,j)` = maximum row index among B cells with row ≤ i and col ≤ j. Let `minW_in_suffix(i,j)` = minimum row index among W cells with row ≥ i and col ≥ j. The condition is that for all i,j, `maxB_in_prefix(i,j) < minW_in_suffix(i,j)`. But we only need to check this for the coordinates of the precolored cells? Actually, if it holds for all precolored cells, it holds for all. Because the max/min functions are monotone.

We can compute the "upper boundary" of B cells: for each row i, the maximum column of a B cell in that row? No, we need a 2D condition.

Alternative approach: This is equivalent to checking if the bipartite graph of constraints is feasible. We can use the row/column threshold formulation with intervals and check feasibility via a greedy algorithm.

Let's go back to the threshold formulation. We have intervals for `r_i`: `[Rmax_i, Rmin_i-1]`. For `c_j`: `[Cmax_j, Cmin_j-1]`. We need to choose `r_i, c_j` such that for every white cell (i,j), `r_i < j` or `c_j < i`. This is a 2-SAT on a bipartite graph? Actually, it's a system of difference constraints? Not exactly.

We can solve it greedily: process rows in increasing order of `Rmin_i`. For each row i, we want to assign `r_i` as small as possible but ≥ `Rmax_i`. However, we also need to satisfy the white cell constraints. A white cell (i,j) requires that if `r_i ≥ j`, then `c_j < i`. So when we assign `r_i`, we must ensure that for all white cells in row i with column j ≤ r_i, the corresponding column j has `c_j < i`. This means that for those columns, we must have already assigned `c_j` to be < i, or we must assign them later to be < i. But we process rows in order of `Rmin_i`, which is the earliest row where the column must become white. Actually, `Rmin_i` is the first column that must be white in row i. So if we process rows by `Rmin_i` ascending, we are processing rows that become white earlier first.

Wait, there is a known solution for this exact problem (AtCoder ABC 247 Ex? No, it's "Grid Coloring" from AtCoder Regular Contest? Actually it's "ARC 108 D"? No. Let me recall: "There is an N×N grid. Takahashi wants to color each cell black or white..." This is AtCoder Beginner Contest 247 Ex? No, Ex is harder. This is ABC 247 F? No. It's "ABC 247 Ex"? Actually, I think it's "AtCoder Beginner Contest 247 Ex" is "Dice Product". This might be "AtCoder Regular Contest 108 D"? No.

Let me search my memory: The problem is "Grid Coloring" with N up to 1e9, M up to 2e5. The solution is to check if there is no B cell that is down-right of a W cell. The check can be done by sorting B cells by row descending and column descending, and W cells by row ascending and column ascending, and then sweeping.

Specifically, we can maintain the "frontier" of B cells: the maximum column of a B cell seen so far when scanning rows from top to bottom? No, we need to ensure that no W cell is above-left of a B cell.

Let's define: A B cell at (i,j) implies that all cells (i',j') with i' ≤ i, j' ≤ j must be black. So if there is a W cell at (i',j') with i' ≤ i and j' ≤ j, it's impossible. So we need: for every W cell (i_w, j_w), there is no B cell (i_b, j_b) with i_b ≥ i_w and j_b ≥ j_w. This is exactly the condition.

We can check this by verifying that the "upper envelope" of B cells (as a function of column) is strictly above the "lower envelope" of W cells. More precisely, define for each column j: `B_max_row[j]` = max row of B in column j (0 if none). Define for each column j: `W_min_row[j]` = min row of W in column j (N+1 if none). Then we need that for all j, `B_max_row[j] < W_min_row[j]`. But as we saw, this is not sufficient because B and W can be in different columns. However, if we also consider the "diagonal" condition? Actually, if B is at (2,2) and W at (1,1), then B_max_row[2]=2, W_min_row[2]=N+1, so column condition holds. But it's still impossible. So we need a stronger condition.

The correct condition is: the set of B cells must be contained in the set of cells that are "above" a monotone non-increasing function f(j) = max row of B in column ≤ j? Not exactly.

Let's think in terms of the partial order. The condition "no B is down-right of W" means that the B set is an order filter? No, B set must be an order ideal (down-set). W set must be an order filter (up-set). So we need to check if the given B cells form a down-set and W cells form an up-set. But they are just subsets; we need to check if there exists a down-set containing all B and no W. This is possible iff the B set is "downward" and the W set is "upward" relative to each other. That is, the B set and W set are "separated" by a monotone boundary.

This is equivalent to: the "upper boundary" of B (the set of maximal elements in B) and the "lower boundary" of W (the set of minimal elements in W) do not intersect in a certain way. Actually, we can compute the "frontier" of B: for each row i, the maximum column j such that (i,j) is B. But B might not be a full Young diagram; we only have some B cells. The condition that there exists a Young diagram containing all B and no W is equivalent to: for every B cell (i,j), the rectangle [1..i] x [1..j] contains no W cell. And for every W cell (i,j), the rectangle [i..N] x [j..N] contains no B cell. These two are equivalent.

So we can just check: for every B cell (i,j), is there a W cell (i',j') with i' ≤ i and j' ≤ j? If yes, impossible. For every W cell (i,j), is there a B cell (i',j') with i' ≥ i and j' ≥ j? If yes, impossible. We can check both, but they are symmetric.

How to check efficiently? We have M up to 2e5. We can sort B cells by row ascending, and within same row by column ascending. Then we can maintain the "frontier" of B: the maximum column seen so far for each row? Actually, we need to check if any W cell is "inside" the rectangle defined by a B cell.

We can process B cells in order of increasing row, and for each row, increasing column. For each B cell (i,j), we need to know if there is a W cell with row ≤ i and col ≤ j. We can pre-process W cells into a data structure that can answer: given (i,j), is there a W cell in [1..i] x [1..j]? This is a 2D range emptiness query. We can sort W cells and use a segment tree or BIT on the compressed coordinates. Since M is 2e5, we can compress coordinates and use a 2D BIT or segment tree to query the minimum row of W cells in a prefix. Actually, we need to check if there exists any W cell in the prefix. So we can store W cells in a 2D BIT that supports "is there any point in rectangle". Or we can sort W cells by row, and for each B cell, we only need to check W cells with row ≤ i. We can maintain a BIT over columns that tracks the minimum column of W cells seen so far? No, we need to check if there is a W cell with col ≤ j. So for each row prefix, we need to know the minimum column of W cells in that row prefix? Actually, we need to know if there exists a W cell with row ≤ i and col ≤ j. This is equivalent to: the minimum column among W cells with row ≤ i is ≤ j. So we can sort W cells by row ascending, and maintain a data structure (like a segment tree) that stores the minimum column for each row? But rows are up to 1e9, so we need to compress.

We can compress all row and column coordinates that appear in the input. There are at most 2e5 distinct rows and columns. We can sort B cells by row, and W cells by row. Then we can sweep: maintain a BIT over columns (compressed) that stores the minimum row? Wait, we need to answer: for a given B cell (i,j), is there a W cell with row ≤ i and col ≤ j? We can process B cells in order of increasing row. For each B cell, we add all W cells with row ≤ i to a BIT that stores the minimum column? Actually, we need to know if there is a W cell with col ≤ j. So we can maintain a BIT where each column index stores the minimum row of a W cell in that column? No, we need to query over columns ≤ j. So we need a BIT that supports range minimum query over columns. Specifically, we want to know if there exists a W cell with row ≤ i and col ≤ j. If we process W cells in order of increasing row, and insert them into a BIT that stores 1 if there is a W cell in that column, then we can query the sum over columns ≤ j. If sum > 0, then there is a W cell. But we need to ensure that the W cell's row is ≤ i. Since we process W cells in order of row, when we are at B cell with row i, we have inserted all W cells with row ≤ i. So we can just query if any column ≤ j has a W cell. This is a range sum query. We can use a BIT (Fenwick tree) over compressed columns. We insert 1 at the column of each W cell when we encounter it. Then for a B cell (i,j), we query sum over columns ≤ j. If > 0, then there is a W cell in the prefix, so impossible.

Similarly, we need to check the other direction: for every W cell (i,j), is there a B cell with row ≥ i and col ≥ j? We can process W cells in order of decreasing row, and insert B cells in order of decreasing row, and query if there is a B cell with col ≥ j. This is symmetric.

But wait, is this sufficient? Let's test with the counterexample: B at (2,2), W at (1,1). Process B cells: B at (2,2). W cells with row ≤ 2: W at (1,1). Insert W at col 1. Query for B (2,2): columns ≤ 2 includes col 1, which has a W. So we detect the conflict. Good.

What about B at (1,2), W at (2,1)? B at (1,2). W cells with row ≤ 1: none (W is at row 2). So query sum ≤ 2 is 0. No conflict. Then process W cells: W at (2,1). B cells with row ≥ 2: none (B is at row 1). So query for W (2,1): columns ≥ 1? We need to check if there is a B cell with col ≥ 1. B is at col 2, which is ≥ 1. But we need to ensure that the B cell's row is ≥ 2. Since we process B cells in decreasing row, when we are at W with row 2, we have inserted B cells with row ≥ 2. B is at row 1, so not inserted. So query returns 0. No conflict. So both checks pass. Correct.

So the algorithm is:
1. Separate cells into B and W.
2. Sort B cells by row ascending, then column ascending.
3. Sort W cells by row ascending, then column ascending.
4. Compress all column coordinates that appear in B or W. (We need to query columns ≤ j for B, and columns ≥ j for W. For the second check, we can also compress and use a BIT for suffix queries, or just reverse the column order.)
5. First pass: Sweep rows from top to bottom. Maintain a BIT over columns. Initially empty. For each B cell in order of increasing row, before processing it, add all W cells with row equal to the current row? Actually, we need to add W cells with row ≤ current row. So we can iterate through W cells in order of increasing row, and for each B cell, we add W cells with row ≤ B.row. Then query BIT for sum over columns ≤ B.col. If > 0, conflict.
6. Second pass: Sweep rows from bottom to top. Maintain a BIT over columns. For each W cell in order of decreasing row, add all B cells with row ≥ W.row. Query BIT for sum over columns ≥ W.col. If > 0, conflict.
7. If no conflicts, output Yes.

But wait: In the first pass, we query for each B cell if there is a W cell in the prefix. But we also need to ensure that the W cell is not the same cell? The problem says cells are distinct, so no issue. Also, we need to consider that the W cell might be in the same row? If W is in the same row and column ≤ B.col, then B is to the right of W in the same row. But B is black, W is white. In the same row, the condition is that black cells are a prefix. So if W is to the left of B in the same row, that's a conflict because the prefix of black cells would include the W cell. So our check correctly catches this: if W is in the same row and col ≤ B.col, then when we process B, we have added W (since row ≤ B.row), and query finds it.

Similarly, in the second pass, if B is in the same row and col ≥ W.col, that's a conflict (white cell to the left of black in same row? Actually, if B is to the right of W in same row, that's a conflict. In the second pass, we process W from bottom up. If B is in same row and col ≥ W.col, then when we process W, we have added B (since row ≥ W.row), and query finds it. So both checks are consistent.

But is it sufficient to only check these two directions? The condition "no B is down-right of W" is equivalent to: for every B, no W in its up-left rectangle; and for every W, no B in its down-right rectangle. These are exactly the two checks. So yes, it's sufficient.

Now, we need to implement this efficiently. M up to 2e5, so O(M log M) is fine.

Let's detail the steps:

Input: N, M. Then M lines of X_i, Y_i, C_i.

Collect all B cells and W cells.
Collect all column coordinates from both B and W for compression.

First pass (top-down):
- Sort B cells by X ascending, then Y ascending.
- Sort W cells by X ascending, then Y ascending.
- Use a pointer to iterate through W cells. For each B cell in order:
  - While W pointer < len(W) and W[W_pointer].X <= B.X:
    - Add W[W_pointer].Y to BIT (update +1).
    - Increment pointer.
  - Query BIT: sum of Y indices <= B.Y (using compressed coordinate). If > 0, conflict.
- After processing all B cells, we don't need to clear BIT for second pass; we can create a new BIT or reset.

Second pass (bottom-up):
- Sort B cells by X descending, then Y descending.
- Sort W cells by X descending, then Y descending.
- Use a BIT that supports suffix sum. We can either reverse the column coordinates (so that "≥ Y" becomes "≤ reversed_Y") or use a BIT that queries from Y to max. Let's just compress columns and use a BIT where we query sum over [Y, max]. We can implement BIT with range query by using prefix sum and total sum. Or we can store the BIT in reverse order: map Y to (max_coord - Y + 1). Then suffix becomes prefix.
- For each W cell in order of decreasing X:
  - While B pointer < len(B) and B[B_pointer].X >= W.X:
    - Add B[B_pointer].Y to BIT.
  - Query BIT for sum over Y >= W.Y. If > 0, conflict.

If no conflicts, output Yes.

Edge cases: N can be 1. M can be 1. Works.

Let's test with sample 1:
N=4, M=3.
B: (4,1), (1,3)
W: (3,2)
First pass:
B sorted: (1,3), (4,1)
W sorted: (3,2)
BIT initially empty.
Process B (1,3): W pointer: W(3,2) has X=3 > 1, so no add. Query Y<=3: sum=0. OK.
Process B (4,1): W pointer: W(3,2) has X=3 <=4, add Y=2. Query Y<=1: sum=0. OK.
Second pass:
B sorted desc: (4,1), (1,3)
W sorted desc: (3,2)
BIT initially empty.
Process W (3,2): B pointer: B(4,1) X=4 >=3, add Y=1. Query Y>=2: sum over Y>=2. Y=1 is not >=2, so sum=0. OK.
No conflicts. Yes.

Sample 2:
N=2, M=2.
B: (2,2)
W: (1,2)
First pass:
B sorted: (2,2)
W sorted: (1,2)
Process B (2,2): W(1,2) X=1 <=2, add Y=2. Query Y<=2: sum=1 >0. Conflict. No.

Sample 3:
N=1, M=1.
W: (1,1)
B: none.
First pass: no B cells, no conflict.
Second pass: W (1,1). B pointer: no B cells. Query Y>=1: sum=0. Yes.

Sample 4: Should output No. We can trust the algorithm.

Complexity: O(M log M) for sorting and BIT operations. M up to 2e5, so fine.

Memory: O(M).

Now, we need to write the code in Python. Use sys.stdin.read for fast input. Use list comprehensions. Implement BIT (Fenwick tree) with size = number of distinct columns + 2.

Implementation details:
- Read N, M.
- Initialize lists B = [], W = [].
- For each of M lines:
  - Read X, Y, C.
  - If C == 'B': B.append((X, Y))
  - else: W.append((X, Y))
- Collect all Y from B and W into a set, sort to get compressed coordinates.
- Map Y to index: 1-based for BIT.
- First pass:
  - Sort B by X asc, Y asc.
  - Sort W by X asc, Y asc.
  - BIT size = len(comp) + 2.
  - w_ptr = 0
  - For each (x, y) in B:
    - while w_ptr < len(W) and W[w_ptr][0] <= x:
      - update BIT at index of W[w_ptr][1] with +1.
      - w_ptr += 1
    - query BIT sum up to index of y. If > 0: print No, return.
- Second pass:
  - Sort B by X desc, Y desc.
  - Sort W by X desc, Y desc.
  - Reset BIT to zeros (create new BIT or clear array).
  - b_ptr = 0
  - For each (x, y) in W:
    - while b_ptr < len(B) and B[b_ptr][0] >= x:
      - update BIT at index of B[b_ptr][1] with +1.
      - b_ptr += 1
    - query BIT sum from index of y to end. If > 0: print No, return.
- If loop finishes, print Yes.

Note: In the second pass, we need to query suffix sum. We can compute total sum and subtract prefix sum up to y-1. Or we can use a BIT that supports range query by storing reversed indices. Let's just use total - prefix(y-1).

Edge case: If there are no B cells, first pass does nothing. If no W cells, second pass does nothing. Works.

Let's double-check the logic with a tricky case: B at (1,1), W at (1,2). Same row, B left, W right. This is valid: row 1 has B then W. First pass: B (1,1). W (1,2) has X=1 <=1, add Y=2. Query Y<=1: sum=0. OK. Second pass: W (1,2). B (1,1) X=1 >=1, add Y=1. Query Y>=2: sum over Y>=2. Y=1 is not >=2, sum=0. OK. Yes.

B at (1,2), W at (1,1). Invalid. First pass: B (1,2). W (1,1) X=1 <=1, add Y=1. Query Y<=2: sum=1 >0. Conflict. No.

B at (2,1), W at (1,2). Valid? B is down, W is up. B at (2,1) means column 1 has black at row 2. W at (1,2) means row 1 has white at col 2. Can we fill? We need a Young diagram. B at (2,1) implies row 2 has at least 1 black (col 1). W at (1,2) implies row 1 has at most 1 black (since col 2 is white). So row 1: B W, row 2: B ?. Column 1: B B, column 2: W ?. This is consistent: row 2 col 2 can be W. So valid. First pass: B (2,1). W (1,2) X=1 <=2, add Y=2. Query Y<=1: sum=0. OK. Second pass: W (1,2). B (2,1) X=2 >=1, add Y=1. Query Y>=2: sum=0. OK. Yes.

B at (1,2), W at (2,1). Valid? B at (1,2) means row 1 has at least 2 blacks. W at (2,1) means column 1 has at most 1 black (row 2 is white). So row 1: B B, row 2: W ?. Column 1: B W, column 2: B ?. This is consistent: row 2 col 2 can be W. So valid. First pass: B (1,2). W (2,1) X=2 >1, no add. Query Y<=2: sum=0. OK. Second pass: W (2,1). B (1,2) X=1 <2, no add. Query Y>=1: sum=0. OK. Yes.

B at (2,2), W at (1,1). Invalid. First pass: B (2,2). W (1,1) X=1 <=2, add Y=1. Query Y<=2: sum=1 >0. Conflict. No.

B at (1,1), W at (2,2). Invalid. First pass: B (1,1). W (2,2) X=2 >1, no add. Query Y<=1: sum=0. OK. Second pass: W (2,2). B (1,1) X=1 <2, no add. Query Y>=2: sum=0. OK. Wait, this says valid? But B at (1,1) and W at (2,2) means B is up-left, W is down-right. This is valid: the Young diagram can be just the single cell (1,1) black, rest white. So yes, valid. Our algorithm says valid. Good.

What about B at (1,3), W at (2,2)? B up, W down. Valid? B at (1,3) means row 1 has 3 blacks. W at (2,2) means column 2 has at most 1 black (row 2 is white). So row 1: B B B, row 2: W W ?. Column 1: B W, column 2: B W, column 3: B ?. This is consistent. First pass: B (1,3). W (2,2) X=2 >1, no add. Query Y<=3: sum=0. OK. Second pass: W (2,2). B (1,3) X=1 <2, no add. Query Y>=2: sum=0. OK. Yes.

What about B at (2,3), W at (1,2)? B down, W up. B at (2,3) means row 2 has 3 blacks. W at (1,2) means row 1 has at most 1 black. So row 1: B W, row 2: B B B. Column 1: B B, column 2: W B, column 3: B B. This is consistent? Check column 2: W at row 1, B at row 2. That's a prefix of 1 black? Actually, column 2 has B at row 2, W at row 1. The condition for column is topmost i black, rest white. So if row 1 is W and row 2 is B, that's not a prefix of black. So invalid. Let's check our algorithm: First pass: B (2,3). W (1,2) X=1 <=2, add Y=2. Query Y<=3: sum=1 >0. Conflict. No. Correct.

What about B at (3,1), W at (2,2)? B down, W up. B at (3,1) means column 1 has 3 blacks. W at (2,2) means row 2 has at most 1 black. So column 1: B B B, row 2: W W ?. This is consistent? Row 2 has W at col 2, so at most 1 black means col 1 must be B? Actually, row 2: col 1 is B (since column 1 has 3 blacks), col 2 is W. So row 2 has B W. That's fine. Column 2: row 1 ?, row 2 W, row 3 ?. We can set row 1 col 2 to B? But then column 2 would have B, W, ?. That's fine. So valid. First pass: B (3,1). W (2,2) X=2 <=3, add Y=2. Query Y<=1: sum=0. OK. Second pass: W (2,2). B (3,1) X=3 >=2, add Y=1. Query Y>=2: sum=0. OK. Yes.

So the algorithm seems correct.

One more check: What if there are multiple B cells in the same row? B at (1,1) and (1,3). W at (1,2). This is invalid because row 1 has B, W, B. First pass: B sorted: (1,1), (1,3). W sorted: (1,2). Process B (1,1): W (1,2) X=1 <=1, add Y=2. Query Y<=1: sum=0. OK. Process B (1,3): W already added. Query Y<=3: sum=1 >0. Conflict. No. Correct.

What if B at (1,1), (1,2), W at (1,3)? Valid: row 1 B B W. First pass: B (1,1): no W added (W X=1 <=1, but we add before query? Actually, we add W with X <= current B.X. For B (1,1), W (1,3) X=1 <=1, add Y=3. Query Y<=1: sum=0. OK. B (1,2): W already added. Query Y<=2: sum=0. OK. Second pass: W (1,3). B (1,1) X=1 >=1, add Y=1. B (1,2) X=1 >=1, add Y=2. Query Y>=3: sum=0. OK. Yes.

What about B at (2,2), W at (1,3) and (3,1)? B at (2,2). W at (1,3) is up-right, W at (3,1) is down-left. Is this valid? B at (2,2) means row 2 has 2 blacks, column 2 has 2 blacks. W at (1,3) means row 1 has at most 2 blacks? Actually, W at (1,3) means column 3 has at most 0 blacks? Wait, W at (1,3) means row 1 col 3 is white. So column 3 has white at row 1, so column 3 can have at most 0 blacks? No, column condition: topmost i black, rest white. If row 1 is white, then i must be 0. So column 3 has 0 blacks. W at (3,1) means row 3 col 1 is white, so row 3 has at most 0 blacks. So row 3 is all white. Row 2 has B B. Row 1: col 1 ?, col 2 ?, col 3 W. Column 1: row 1 ?, row 2 B, row 3 W. So column 1 must have B at row 2, W at row 3, so row 1 can be B or W? If row 1 col 1 is B, then column 1 has B B W, which is valid (prefix of 2). If row 1 col 1 is W, then column 1 has W B W, invalid. So row 1 col 1 must be B. Column 2: row 1 ?, row 2 B, row 3 ?. We can set row 1 col 2 to B, row 3 col 2 to W. Then column 2 has B B W, valid. Row 1: B B W, valid. So overall valid. Our algorithm: First pass: B (2,2). W sorted: (1,3), (3,1). Process B (2,2): add W with X<=2: W (1,3) added. Query Y<=2: sum=0 (Y=3 not <=2). OK. Second pass: W sorted desc: (3,1), (1,3). Process W (3,1): add B with X>=3: none. Query Y>=1: sum=0. Process W (1,3): add B with X>=1: B (2,2) added. Query Y>=3: sum=0 (Y=2 not >=3). OK. Yes.

What about B at (2,2), W at (1,2) and (2,1)? B at (2,2). W at (1,2) means row 1 col 2 white. W at (2,1) means row 2 col 1 white. So row 2: W B. Invalid because row 2 must be prefix of black. First pass: B (2,2). W sorted: (1,2), (2,1). Process B (2,2): add W with X<=2: both added. Query Y<=2: sum includes Y=1 and Y=2. sum=2 >0. Conflict. No. Correct.

So the algorithm is correct.

Now, we need to implement BIT. Since we need to reset for second pass, we can either create a new BIT array or reuse and zero it. Creating new is fine.

Complexities: O(M log M). M up to 2e5, log M ~ 18, so fast.

Let's write the code.

```python
import sys

def solve():
    import sys
    input = sys.stdin.readline
    N, M = map(int, input().split())
    B = []
    W = []
    cols = set()
    for _ in range(M):
        x, y, c = input().split()
        x = int(x)
        y = int(y)
        if c == 'B':
            B.append((x, y))
        else:
            W.append((x, y))
        cols.add(y)
    
    # Compress columns
    sorted_cols = sorted(cols)
    col_to_idx = {c: i+1 for i, c in enumerate(sorted_cols)}  # 1-based
    size = len(sorted_cols) + 2
    
    # First pass: top-down
    B.sort(key=lambda p: (p[0], p[1]))
    W.sort(key=lambda p: (p[0], p[1]))
    
    bit = [0] * size
    def update(i, v=1):
        while i < size:
            bit[i] += v
            i += i & -i
    def query(i):
        s = 0
        while i > 0:
            s += bit[i]
            i -= i & -i
        return s
    
    w_ptr = 0
    for x, y in B:
        idx = col_to_idx[y]
        while w_ptr < len(W) and W[w_ptr][0] <= x:
            wy = W[w_ptr][1]
            update(col_to_idx[wy])
            w_ptr += 1
        if query(idx) > 0:
            print("No")
            return
    
    # Second pass: bottom-up
    B.sort(key=lambda p: (-p[0], -p[1]))
    W.sort(key=lambda p: (-p[0], -p[1]))
    
    bit = [0] * size
    b_ptr = 0
    for x, y in W:
        idx = col_to_idx[y]
        while b_ptr < len(B) and B[b_ptr][0] >= x:
            by = B[b_ptr][1]
            update(col_to_idx[by])
            b_ptr += 1
        # Query suffix sum from idx to end
        total = query(size - 1)
        prefix = query(idx - 1)
        if total - prefix > 0:
            print("No")
            return
    
    print("Yes")

if __name__ == "__main__":
    solve()
```

Wait, in the second pass, we need to query sum over columns >= y. We used total - prefix(y-1). But we need to ensure that the BIT contains only B cells with row >= current W.row. Since we process W in decreasing row, and add B with row >= current W.row, this is correct.

One subtlety: In the first pass, we add W cells with row <= B.row. But we process B cells in increasing row. For a given B cell, we add all W cells with row <= B.row. This includes W cells in the same row. That's correct.

In the second pass, we process W cells in decreasing row. For a given W cell, we add all B cells with row >= W.row. This includes B cells in the same row. That's correct.

Edge case: If there are no B cells, the first pass loop doesn't execute. The second pass: W sorted desc. b_ptr = 0. For each W, while b_ptr < len(B) ... but len(B)=0, so no updates. Query total - prefix = 0 - 0 = 0. So no conflict. Yes.

If there are no W cells, second pass loop doesn't execute. First pass: B sorted. w_ptr = 0, len(W)=0. No updates. Query = 0. Yes.

What about the case where a B cell and W cell are in the same row and column? They can't be because input says distinct cells.

So the code is correct.

Let's test with sample 1:
N=4, M=3
B: (4,1), (1,3)
W: (3,2)
cols: {1,2,3}
sorted_cols: [1,2,3]
col_to_idx: {1:1, 2:2, 3:3}
size=5
First pass:
B sorted: [(1,3), (4,1)]
W sorted: [(3,2)]
bit = [0,0,0,0,0]
w_ptr=0
B (1,3): idx=3. W[0].X=3 >1, no add. query(3)=0.
B (4,1): idx=1. W[0].X=3 <=4, add Y=2 idx=2. w_ptr=1. query(1)=0.
Second pass:
B sorted desc: [(4,1), (1,3)]
W sorted desc: [(3,2)]
bit = [0,0,0,0,0]
b_ptr=0
W (3,2): idx=2. B[0].X=4 >=3, add Y=1 idx=1. b_ptr=1. total=query(4)=1. prefix=query(1)=1. total-prefix=0.
Done. Yes.

Sample 2:
N=2, M=2
B: (2,2)
W: (1,2)
cols: {2}
sorted_cols: [2]
col_to_idx: {2:1}
size=3
First pass:
B sorted: [(2,2)]
W sorted: [(1,2)]
bit=[0,0,0]
w_ptr=0
B (2,2): idx=1. W[0].X=1 <=2, add Y=2 idx=1. w_ptr=1. query(1)=1 >0. No.

Sample 3:
N=1, M=1
W: (1,1)
B: []
cols: {1}
sorted_cols: [1]
col_to_idx: {1:1}
size=3
First pass: no B.
Second pass: W sorted desc: [(1,1)]. bit=[0,0,0]. b_ptr=0. W (1,1): idx=1. no B. total=0, prefix=0. Yes.

Sample 4: Should be No. We can trust.

One more check: What if there are multiple cells with same row and column? Input guarantees distinct.

What about N up to 1e9? We don't use N except reading it. So fine.

Memory: B and W lists size up to 2e5. BIT size up to 2e5+2. Fine.

Time: Sorting O(M log M). BIT operations O(M log M). Total O(M log M). For M=2e5, ~2e5 * 18 = 3.6e6 operations, fast.

Potential issue: In the second pass, we query total - prefix(idx-1). But we need to ensure that the BIT is correctly updated. We update B cells with row >= current W.row. Since we process W in decreasing row, we add B cells as we go down. So for a W cell at row x, we have added all B cells with row >= x. That's correct.

But wait: In the second pass, we process W cells in decreasing row. For the first W cell (largest row), we add all B cells with row >= that row. Then for the next W cell (smaller row), we add more B cells (those with row between the previous W.row and current W.row). So the BIT accumulates B cells with row >= current W.row. So the query is correct.

One subtle point: In the first pass, we process B cells in increasing row. For the first B cell (smallest row), we add all W cells with row <= that row. Then for the next B cell (larger row), we add more W cells. So BIT accumulates W cells with row <= current B.row. Query is correct.

Thus the algorithm is correct.

Let's consider if there is any case where the condition holds but the algorithm says No? We already reasoned it's equivalent.

What about the case where a B cell is at (i,j) and a W cell is at (i,j+1) but there is another B cell at (i+1, j)? This is valid? B at (i,j) and (i+1,j), W at (i,j+1). Row i: B W, row i+1: B ?. This is valid if row i+1 col j+1 is W. Our algorithm: First pass: B (i,j) and B (i+1,j). W (i,j+1). Process B (i,j): W (i,j+1) has row i <= i, add Y=j+1. Query Y<=j: sum=0. Process B (i+1,j): W already added. Query Y<=j: sum=0. OK. Second pass: W (i,j+1). B sorted desc: (i+1,j), (i,j). Process W (i,j+1): add B with row >= i: both added. Query Y>=j+1: sum=0 (B are at Y=j). OK. Yes.

What about B at (i,j) and W at (i+1, j+1)? B up-left, W down-right. Valid. First pass: B (i,j). W (i+1,j+1) row i+1 > i, no add. Query Y<=j: sum=0. OK. Second pass: W (i+1,j+1). B (i,j) row i < i+1, no add. Query Y>=j+1: sum=0. OK. Yes.

What about B at (i+1, j+1) and W at (i,j)? B down-right, W up-left. Invalid. First pass: B (i+1,j+1). W (i,j) row i <= i+1, add Y=j. Query Y<=j+1: sum=1 >0. Conflict. No.

So all good.

One more edge case: M=0? But constraints say M >= 1. So no need to handle M=0.

What if N=1 and M=1, B at (1,1)? First pass: B (1,1). No W. Query=0. Second pass: no W. Yes.

What if N=1 and M=1, W at (1,1)? Yes.

What if N=1 and M=1, B at (1,1) and W at (1,1)? Not possible due to distinct cells.

So the solution is complete.

We should ensure that the BIT size is correct. We have `size = len(sorted_cols) + 2`. The indices go from 1 to len(sorted_cols). So size = len(sorted_cols) + 1 is enough, but +2 is safe. In query for total, we use `size - 1`. If size = len+2, then size-1 = len+1, which is beyond the last index. But BIT query works as long as we don't go out of bounds. Actually, if we update at index up to len, then query(size-1) where size-1 = len+1 will just sum up to len+1, but since no updates beyond len, it's the same as query(len). So it's fine. But to be precise, we can set size = len(sorted_cols) + 1 and use query(size-1) = query(len). Let's just use size = len(sorted_cols) + 1.

In the code above, I used `size = len(sorted_cols) + 2`. That's fine.

Now, write the final code.

One more optimization: We can avoid creating a new BIT for the second pass by clearing the array. But creating new is fine.

Let's write the final solution.### PLAN
We need to determine if there exists a binary matrix where each row is a prefix of black cells followed by white cells, and each column is a prefix of black cells followed by white cells. This is equivalent to the set of black cells forming a Young diagram (order ideal) in the product order. The condition is satisfied iff no precolored black cell is "down-right" of a precolored white cell (i.e., there is no pair (i₁,j₁) colored B and (i₂,j₂) colored W with i₁ ≥ i₂ and j₁ ≥ j₂). We can check this efficiently by sweeping rows in both directions using a Fenwick tree (BIT) over compressed column coordinates.