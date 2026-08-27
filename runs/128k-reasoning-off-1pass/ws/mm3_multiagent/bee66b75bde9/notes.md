
## ideation
We need to decide if there exists a binary matrix of size N×N (N up to 1e9) where each row is of the form: first some number of B's then the rest W's (i.e., a monotone row: B...BW...W), and similarly each column is of the form: first some number of B's then the rest W's (monotone down). Such a matrix is exactly a “Young diagram” shape: there is a monotone non-increasing “cut” function. Equivalently, we can assign each row a value r_i = number of black cells in that row (0..N), and each column a value c_j = number of black cells in that column (0..N), such that cell (i,j) is black iff j ≤ r_i and also i ≤ c_j. That is, we need for all i,j: (j ≤ r_i) ↔ (i ≤ c_j). Because a cell must be black exactly when both conditions hold? Let's check: In such a matrix, a cell (i,j) is black if and only if it lies in the "black region": rows 1..c_j? Wait, the condition for a column: top i cells are black, rest white, i variable per column. Let column j have parameter C_j (0..N): cells rows 1..C_j are black, rows C_j+1..N are white. Similarly, row i has parameter R_i: cells columns 1..R_i are black, columns R_i+1..N are white. Then cell (i,j) is black iff i ≤ C_j and j ≤ R_i. So black region is intersection of a row cut and a column cut. The whole matrix is defined by two vectors (R_i) and (C_j). The condition must be consistent: the black region must be exactly the cells that satisfy both. But does the consistency condition hold automatically? Not necessarily; we need that the region defined by R and C is consistent, i.e., for each (i,j), the value of (i ≤ C_j) and (j ≤ R_i) must not conflict: they both give same decision? Actually each cell's color is forced to be black if both conditions say black? No: The color of a cell is not separately defined; the row condition says the row i's cells are black for columns 1..R_i, white for columns R_i+1..N. So cell (i,j) is black iff j ≤ R_i, regardless of column condition. The column condition is another independent requirement: the column j's cells are black for rows 1..C_j, white for rows C_j+1..N. So cell (i,j) must be black iff both conditions agree: i.e., j ≤ R_i and i ≤ C_j must both hold, and if one says black and the other says white, impossible. So the condition is: for all i,j, we must have (j ≤ R_i) = (i ≤ C_j). So they must be equivalent. That's the core consistency condition.

Thus the problem reduces to: given some precolored cells, can we find integers R_i (0..N) and C_j (0..N) such that for each precolored cell (i,j) with color B: we require (j ≤ R_i) ∧ (i ≤ C_j). For white: (j > R_i) ∨ (i > C_j) (i.e., not both true). Equivalently: For B: we need j ≤ R_i and i ≤ C_j. For W: we need either j > R_i or i > C_j.

We need to determine existence. Since N huge but M up to 2e5, we must think abstractly. The variables are only those rows and columns that appear in constraints, but also the rest of rows/columns must have some R_i and C_j (0..N) that satisfy constraints. The structure of constraints may allow all rows/columns to be assigned, but perhaps we need to consider global monotonicity constraints: The sequences R_i and C_j must be monotone? Not necessarily. Wait: The condition for each row is independent; rows can have any R_i. However, the consistency condition for all (i,j) yields a global structure. Let's examine if the condition (j ≤ R_i) = (i ≤ C_j) for all i,j forces R_i and C_j to be monotone? Let's try small N. Suppose we have R_i values: each row defines a cut column. The column cuts C_j are defined by row cuts: For column j, C_j is the number of rows i such that j ≤ R_i? Actually if we have R_i values, we can define C_j = max{i | R_i ≥ j}? Let's see: Condition (i ≤ C_j) ↔ (j ≤ R_i) for all i. For fixed j, define C_j = number of i such that (i ≤ C_j) is true, i.e., i ∈ [1, C_j] satisfy i ≤ C_j (trivially), but we need equivalence: (i ≤ C_j) iff (j ≤ R_i). So for i ≤ C_j, we require j ≤ R_i. For i > C_j, we require j > R_i. So the set of rows i where j ≤ R_i is exactly {1,...,C_j}. That means that the rows with R_i ≥ j form a prefix of rows (starting from row 1). So the sequence R_i must be non-increasing? Let's check: Suppose R_1 = 5, R_2 = 3. Then for j=4, rows with R_i ≥4 are row 1 only, so C_4 = 1, okay prefix. For j=4, row 2 has R_2=3 <4, so not in prefix. That's fine. For j=3, rows with R_i ≥3 are rows 1 and 2, so C_3 =2. So indeed the set of rows where R_i ≥ j is a prefix. This implies that the sequence R_i is monotone non-increasing as i increases: because if i < k, and R_i < R_k, then consider j = R_k. For row i, R_i < R_k, so i not in set where j ≤ R_i; but for row k, k is in set. Since set must be prefix, cannot have i not in set while later row k is in set. So R_i must be non-increasing. Similarly, C_j must be non-increasing as j increases? Let's check: For column indices, consider condition (j ≤ R_i) = (i ≤ C_j). If we fix column j, the set of rows i such that i ≤ C_j is a prefix. That's given by C_j. The condition that the set of rows with R_i ≥ j is a prefix yields that the function R_i is non-increasing. Similarly, we can argue that C_j is non-increasing as j increases: Because the set of columns where C_j ≥ i must be a prefix? Let's derive: For a fixed i, consider columns j such that i ≤ C_j. The condition (j ≤ R_i) ↔ (i ≤ C_j) means that columns j where i ≤ C_j are exactly those j ≤ R_i. So as i fixed, the set of columns with C_j ≥ i is a prefix (columns 1..R_i). That implies that the sequence C_j is non-increasing: if j1 < j2 and C_j1 < C_j2, then consider i = C_j2. For column j1, C_j1 < C_j2, so j1 not in set where i ≤ C_j (since i > C_j1). But column j2 has i ≤ C_j2, so j2 is in set. Since set must be prefix, cannot have j1 not in set while later column j2 is. Therefore C_j must be non-increasing.

Thus R_i is a non-increasing sequence of length N (0..N). C_j is a non-increasing sequence of length N. And they are related: C_j = max{i | R_i ≥ j} (or equivalently, for each i, R_i = max{j | C_j ≥ i}). Indeed the equivalence defines a Young diagram shape.

Thus the problem becomes: we have to assign to each row i a non-increasing integer R_i (0..N), and to each column j a non-increasing integer C_j (0..N), satisfying constraints from precolored cells.

Given N huge, but we only have constraints on M cells. However, we also need to assign values to all rows and columns (including those not mentioned). Since the sequences are monotone, they can be characterized by cutpoints. The region of black cells is a Young diagram (Ferrers shape) anchored at top-left. Equivalent to a monotone matrix: There exists a non-increasing function f(i) = R_i, and g(j) = C_j = max{i | f(i) ≥ j}. This is a standard combinatorial object: a Young diagram of size at most N×N.

Thus we need to see if there exists a Young diagram (shape) that contains the B cells and avoids the W cells. That is, each B cell must be inside the shape, each W cell must be outside.

Specifically: For a B at (x,y), we need y ≤ R_x and x ≤ C_y. Since shape is region { (i,j) | i ≤ C_j and j ≤ R_i } equivalently { (i,j) | j ≤ R_i and i ≤ C_y }.

But since shape is monotone, condition reduces to: For B cell (x,y), we need x ≤ C_y and y ≤ R_x. For W cell (x,y), we need not (x ≤ C_y and y ≤ R_x), i.e., either x > C_y or y > R_x.

But we can also think of the shape as defined by the boundary: The shape is a monotone path from (0,N) to (N,0) using steps (1,0) (down) and (0,-1) (right). Equivalent to the "cut" function: For each row i, the number of black cells in that row is R_i. Since shape is left-aligned, each row's black cells are columns 1..R_i. The shape is characterized by non-increasing row lengths. The column heights are C_j = number of rows where R_i ≥ j. This is exactly a Young diagram.

Thus the problem reduces to: Given some cells that must be inside (B) and some that must be outside (W) a Young diagram anchored at top-left, does there exist such a diagram? N up to 1e9, but M limited.

We need to determine existence efficiently.

Observations: The shape is defined by the monotone non-increasing sequence R_i. So we need to assign R_i values (0..N) that are non-increasing, and the constraints must be satisfied.

Let’s formalize constraints in terms of R_i only. Since C_j is derived from R_i, we can eliminate C_j. For a cell (x,y):

- B: need y ≤ R_x (since if y ≤ R_x, then x ≤ C_y automatically? Let's check: If y ≤ R_x, does that guarantee x ≤ C_y? By definition, C_y = max{i | R_i ≥ y}. Since R_x ≥ y, we have x ≤ C_y? Not necessarily: Suppose R sequence is non-increasing; if R_x ≥ y, then all rows i ≤ x have R_i ≥ y (since non-increasing). So indeed, for any i ≤ x, R_i ≥ y. Thus max{i | R_i ≥ y} ≥ x, so C_y ≥ x. So yes, x ≤ C_y. So B condition reduces to just y ≤ R_x.

- W: need not both y ≤ R_x and x ≤ C_y. Since if y ≤ R_x implies x ≤ C_y (as argued), then for W we need y > R_x. Because if y ≤ R_x, then automatically x ≤ C_y, making it black. Therefore W cell forces y > R_x. Let's verify: Suppose we have a white cell (x,y). Could it be outside the shape for reason of x > C_y while y ≤ R_x? But we argued that if y ≤ R_x then automatically x ≤ C_y. Let's prove: Since R_i is non-increasing, if R_x ≥ y, then for all i ≤ x, R_i ≥ y (since earlier rows have at least as many black cells). Therefore the set {i | R_i ≥ y} includes all i from 1 to x, thus its maximum is at least x, so C_y = max{i | R_i ≥ y} ≥ x, so x ≤ C_y. Hence y ≤ R_x implies x ≤ C_y. So any cell with y ≤ R_x is black. Conversely, if y > R_x, then for any i ≤ x? Wait, could x ≤ C_y still hold even if y > R_x? Let's examine: C_y = max{i | R_i ≥ y}. If y > R_x, then R_x < y, so x is not in the set. But maybe some earlier row i < x has R_i ≥ y? Since R_i is non-increasing, earlier rows have larger or equal R_i, so R_i ≥ R_x. So if y > R_x, then for all i ≤ x, R_i ≥ R_x, but could be still < y? Actually if y > R_x, but maybe R_{i} for i < x is larger, maybe ≥ y. Since R is non-increasing, R_1 ≥ R_2 ≥ ... ≥ R_N. So R_1 is largest. If y > R_x, there could be some i < x with R_i ≥ y. For example, N=5, R = [5,5,3,2,1]. For cell (3,4) (x=3,y=4). Here R_3=3, y=4 > 3, so y > R_3. But R_2=5≥4, so C_4 = max{i | R_i ≥4} = 2. So x=3 > C_4=2, so x > C_y. So indeed cell is outside. If R_i are all < y, then C_y = 0, x > C_y. So indeed if y > R_x, then x > C_y (since C_y ≤ x-1). Let's prove: Suppose y > R_x. Since R_i non-increasing, for any i ≤ x, R_i ≥ R_x. But still may be < y. However, the maximum i with R_i ≥ y is at most x-1 (if there is any i < x with R_i ≥ y) or 0 otherwise. Thus C_y ≤ x-1 < x. So x > C_y. So indeed y > R_x implies x > C_y. Therefore white cells are exactly those with y > R_x.

Thus the problem reduces dramatically: The color of cell (i,j) is black iff j ≤ R_i, where R_i is non-increasing across rows. No need to consider C_j. So we need to assign a non-increasing sequence R_i (0..N) such that for each B cell (x,y): y ≤ R_x, and for each W cell (x,y): y > R_x.

Thus we have constraints: For each row i, we have lower and upper bounds on R_i? Actually for each row i, we have constraints of the form: If there is a B in row i at column y, then R_i ≥ y. If there is a W in row i at column y, then R_i < y. So for each row, we have constraints that R_i must be at least max_{B in row i} y, and at most min_{W in row i} (y-1). So we can define L_i = max( y for B cells in row i ), default 0 (since if no B, lower bound 0). And U_i = min( y for W cells in row i ) - 1, default N (since if no W, upper bound N). Then we need L_i ≤ R_i ≤ U_i, and also R_i must be non-increasing: R_1 ≥ R_2 ≥ ... ≥ R_N.

Thus we need to determine if there exists a non-increasing sequence R_i with each R_i in [L_i, U_i] (integers) and 0..N. This is a classic feasibility of monotone sequence with bounds.

Since N is huge (1e9), but constraints are only for rows that appear in input (M rows). However, we also have rows with no constraints: they can take any value consistent with monotonicity, as long as they fit between neighboring constrained rows.

Thus we can treat unknown rows as having L_i = 0, U_i = N (or could be derived from neighbor constraints). But we can also note that monotonicity can be satisfied by "propagating" bounds: Since sequence is non-increasing, we can define for each prefix of rows the maximum allowed R values etc. More precisely, we need to find a non-increasing sequence with given per-row intervals. This is feasible iff the intervals are "compatible" with non-increasing property. Equivalent to: There exists R_i such that:

- For all i, L_i ≤ R_i ≤ U_i.
- For all i, R_i ≥ R_{i+1}.

We can think of constructing the maximal feasible sequence: start with the first row, set R_1 as large as possible but respecting its upper bound and also future constraints. Actually we can define the feasible region via inequalities:

Let’s denote the sequence we want to find. The constraints are: R_i ≥ L_i, R_i ≤ U_i, and R_i ≥ R_{i+1}. This is like a chain of inequalities. This is a classic problem: given lower and upper bounds for each variable and a monotonicity (non-increasing) chain, does there exist a solution? Equivalent to checking that for all i, L_i ≤ U_i, and also that the "propagated" lower bounds do not exceed "propagated" upper bounds when moving forward.

Specifically, define for each i the minimal possible value of R_i given that we must maintain non-increasing and satisfy lower bounds of earlier rows. Let’s think of constructing from top to bottom: We want R_1 ≥ R_2 ≥ ... ≥ R_N. The constraints can be expressed as:

- For each i, R_i ≤ U_i.
- For each i, R_i ≥ L_i.
- Also R_i ≥ R_{i+1}.

Thus R_i must be at least max(L_i, R_{i+1}). So given we choose R_{i+1}, we need R_i ∈ [max(L_i, R_{i+1}), U_i]. To have a solution, we need that for each i, the lower bound for R_i (max(L_i, R_{i+1})) ≤ U_i.

Thus we can attempt to assign R_N, R_{N-1}, ... backwards. Since R_N can be any value in [L_N, U_N] (if no constraints, L_N=0, U_N=N). Then for i = N-1 down to 1, we need to pick R_i ∈ [max(L_i, R_{i+1}), U_i]. So the condition is that for each i, max(L_i, R_{i+1}) ≤ U_i. That must hold for some choice of R_{i+1} in its interval. So we need to see if there exists a sequence of choices satisfying these.

This is similar to checking feasibility of a system of inequalities: L_i ≤ R_i ≤ U_i, and R_i ≥ R_{i+1}. Equivalent to verifying that for all i, L_i ≤ U_i (necessary) and also that the "tightest" lower bound on R_i from future rows (i.e., the maximum of L_i and the lower bound from R_{i+1}) does not exceed U_i.

One can compute minimal possible value of R_i (call low_i) that can be achieved while satisfying all constraints from rows i..N. Similarly, compute maximal possible value of R_i (call high_i) that can be achieved. Then we need low_1 ≤ high_1 (or low_1 ≤ N? Actually we need existence of some R_1). But maybe we can just test feasibility by greedy.

Simplify: Since N huge, but constraints only on M rows. For rows without constraints, L_i = 0, U_i = N. So the constraints only apply at positions where there is at least one precolored cell. For unconstrained rows, they can adjust to accommodate monotonicity.

We can treat the problem as: we have intervals for each row i: [L_i, U_i] (both inclusive). Need to find a non-increasing sequence with R_i in these intervals.

We can attempt to construct from top (row 1) to bottom (row N). At each step, we need to pick a value for current row that is ≤ previous row (to maintain non-increasing) and within its interval. Since we can choose any value in the interval, we can set R_i as the minimum possible that respects monotonicity: i.e., R_i = min(U_i, previous_R). But also must be ≥ L_i. So we need L_i ≤ min(U_i, previous_R). That's the condition.

Thus greedy algorithm: Start with previous_R = N (or N+1? Since we need R_1 ≤ N, but we can treat previous_R = N+1 as sentinel? Actually we need R_1 ≤ N, and also we need to maintain non-increasing. Let's start with previous_R = N (the max possible for row 1). Then for each row i from 1 to N, we need to choose R_i such that L_i ≤ R_i ≤ min(U_i, previous_R). So we need L_i ≤ min(U_i, previous_R). If that holds, we can set R_i = min(U_i, previous_R) (or any value in that range). Then set previous_R = R_i. Continue.

If at any point L_i > min(U_i, previous_R), impossible. Since N huge, we cannot iterate all rows. However, the only rows that matter are those with constraints (L_i or U_i not 0..N). But also we need to consider that monotonicity can be satisfied across gaps: For rows without constraints (L=0, U=N), the condition is L=0 ≤ min(N, previous_R) which always holds (since previous_R ≥ 0). So we can skip them. However, we need to ensure that after skipping many rows, the monotonicity holds. Since we can always set R_i = previous_R for unconstrained rows (or any value ≤ previous_R), there is no issue. The only constraints arise at rows with non-default intervals.

But there is a subtlety: Suppose we have a row i with U_i = small (tight upper bound) and later a row j with L_j large (lower bound). Since sequence is non-increasing, if we set a small R_i, later rows must be ≤ that small value, potentially violating L_j. So the feasibility condition is that the lower bounds of later rows are not too large relative to the upper bounds of earlier rows.

We can solve by processing rows in order, maintaining the current maximum allowed value (i.e., the current previous_R). At each constrained row, we need to ensure that its lower bound L_i is ≤ min(U_i, previous_R). If yes, we set R_i = min(U_i, previous_R) (or something). Then update previous_R = R_i.

If we have unconstrained rows between constrained ones, they don't affect previous_R (since we can keep it same or lower). Actually we need to consider that previous_R is non-increasing. If we have a gap of unconstrained rows, we can keep previous_R unchanged (or lower) across them. But we cannot increase it. So when we reach the next constrained row, previous_R is whatever we set at the last constrained row (or N if none). So processing only constrained rows in order is sufficient.

Edge cases: There may be constrained rows after row N? No, rows are within 1..N.

Thus we need to collect constraints per row: L_i = max y for B in that row, default 0. U_i = min y for W in that row - 1, default N.

We also need to consider that a row may have both B and W constraints; if B's max > (W's min - 1), then L_i > U_i => impossible directly.

We also need to consider columns? Wait, we reduced to row constraints only. But is the reduction correct? Let's double-check thoroughly.

We derived that the color of cell (i,j) is black iff j ≤ R_i, where R_i is non-increasing. Let's verify with the original definition: Row i has R_i black cells (leftmost). Column j has C_j black cells (topmost). Condition: for all i,j, (j ≤ R_i) ↔ (i ≤ C_j). We argued that monotonicity of R_i ensures the equivalence. Let's test with a non-monotonic R_i to see if condition fails: Suppose N=3, R = [2,1,2] (not non-increasing). Then for column j=2: rows with R_i ≥2 are rows 1 and 3. So C_2 = max{i | R_i ≥2} = 3 (since row 3 qualifies). For cell (2,2): j=2 ≤ R_2=1? No, so row condition says white. Column condition: i=2 ≤ C_2=3, so column says black. Conflict. So indeed we need monotonicity.

Thus the shape is a Young diagram. So the reduction is correct.

Now we just need to ensure that for any row i, the condition y ≤ R_i for B and y > R_i for W holds. Since R_i is monotone, we must also ensure that the intervals for each row are consistent with monotonicity.

Thus the problem reduces to checking feasibility of non-increasing sequence with per-row intervals.

Potential pitfalls: The values of L_i and U_i may be large up to N (1e9). Use 64-bit integers.

We also need to consider that the row indices can be up to N, but N huge. We only have constraints for at most M rows (since each precolored cell belongs to a row). So we can store constraints in a map/dictionary keyed by row index.

We also need to consider that there might be constraints that involve same row but multiple B's and W's. We'll compute L_i = max Y for B in that row; U_i = min Y for W in that row minus 1.

We need to sort rows by index ascending.

Processing:

Initialize previous_max = N (since we can set R_1 up to N). Actually we can start with previous_max = N (the maximum possible for the first row). Then iterate over rows in increasing order (only those with constraints). For each row i:

- If there is no constraint for row i (i.e., L_i=0, U_i=N), we can skip; previous_max stays same (or we could lower it, but no need). Actually we need to consider that if there is a gap of unconstrained rows, we can keep previous_max unchanged because we can assign those rows the same value as previous_max (or lower). However, we might need to lower previous_max to satisfy later constraints? No, we want to keep it as high as possible to allow later rows to have lower bounds. So we keep previous_max unchanged across unconstrained rows.

- For constrained row i, we need to pick R_i ≤ previous_max (since non-increasing) and R_i ∈ [L_i, U_i]. So the feasible range for R_i is [L_i, min(U_i, previous_max)]. Feasibility condition: L_i ≤ min(U_i, previous_max). If false, return No.

- Then we set R_i = min(U_i, previous_max) (the maximum possible to keep flexibility for later rows). Update previous_max = R_i.

After processing all constrained rows, we are done. Since there are no further constraints, the remaining rows (to N) can be assigned any non-increasing values ≤ previous_max (e.g., previous_max, previous_max, ...). So always possible.

But we also need to consider the possibility that there is a constrained row after the last constrained row but before N. Since we processed all constrained rows, any later row has no constraints, so fine.

Edge Cases: There might be constrained rows that are not contiguous; we skip over unconstrained ones.

Now we need to verify that this greedy algorithm is correct: It chooses the maximum possible R_i at each step while maintaining feasibility. This is a known approach for monotone chain constraints: always pick the maximum feasible value for current variable to maximize future possibilities. Since future constraints are lower bounds (L_j) for later rows, keeping R_i as large as possible helps satisfy later L_j (since they need to be ≤ R_i). Actually note that later rows have lower bound L_j, and we need R_j ≥ L_j, but also R_j ≤ R_i (since R_i ≥ R_j). So to allow later rows to have large lower bounds, we need earlier R_i to be at least as large as those lower bounds. So picking the maximum feasible R_i (i.e., min(U_i, previous_max)) is optimal.

Thus greedy is correct.

But we need to be careful: The lower bound for row i is L_i (max B column). However, there is also a global condition that R_i ≤ N, but U_i ≤ N-1 (since W columns are at least 1). Actually W cells have Y_i between 1..N, and condition y > R_i => R_i ≤ y-1. So U_i = min_{W in row} (y-1). Since y-1 ≤ N-1, U_i ≤ N-1. But if there is no W, we set U_i = N. So fine.

Now we need to ensure that we also consider column constraints? Wait, we eliminated columns. But is there any hidden column constraint that may restrict R_i beyond the per-row intervals? Let's test with a small example to see if any column constraints could cause inconsistency that is not captured by row intervals.

Consider N=3. Suppose we have a B at (1,3). So row 1 must have R_1 ≥ 3 => R_1 = 3. So row 1 is all black. Now suppose we have a W at (2,2). Row 2 must have R_2 < 2 => R_2 ≤ 1. Since R_1 ≥ R_2, R_2 ≤ 1, okay. So we can set R_2 = 1. Row 3 unconstrained: can be ≤1. This works. Does any column constraint conflict? Let's see columns: Column 3: top cells must be black for some prefix. Since row 1 is black, column 3 must have at least C_3 ≥ 1. That's fine. Column 2: we have a W at (2,2). Row 2 has R_2=1, so column 2's black rows are those with R_i ≥ 2? Actually column 2's black rows are rows i where R_i ≥ 2. Since R_1=3≥2, row 1 is black in column 2. Row 2 has R_2=1<2, so row 2 is white in column 2. That's consistent with W. So fine.

Now consider a case where a column has both B and W constraints that might be contradictory if only row constraints are considered. Let's try to find a counterexample where per-row intervals allow a monotone R, but column constraints cause conflict.

Given we reduced to row constraints only, is it possible that there exists a monotone R satisfying all row constraints, but some column's topmost i cells condition fails? Let's test.

Original condition: For each column j, there exists C_j such that rows 1..C_j are black, rest white. This is automatically satisfied if we define C_j = max{i | R_i ≥ j} (or 0 if none). Since R_i monotone, C_j is non-increasing. So column condition always satisfied given any monotone R. Indeed, given any non-increasing R_i, we can define C_j as above, and the matrix will satisfy both row and column conditions. So if we find any monotone R_i satisfying row constraints, the column constraints will be automatically satisfied. Therefore column constraints are redundant; we don't need to check them separately.

Thus the problem reduces to row intervals and monotonicity.

Now we need to verify that the row intervals correctly capture the precolored cells constraints: For B at (x,y): need y ≤ R_x. That's L_x ≥ y. For W at (x,y): need y > R_x => R_x ≤ y-1 => U_x ≤ y-1. Yes.

Thus the per-row constraints are exactly as we defined.

Potential edge cases: For a row, we might have B at column y, and also W at column y (impossible because cell can't be both). But they could be at different columns. If there is B at y and W at y' < y, then we have L_i = y (max B) and U_i = y'-1 (min W-1). Since y' < y, L_i > U_i => impossible. This corresponds to contradictory constraints: a B cell to the right of a W cell in same row (since row is left-aligned black). Indeed if we have a white cell at column y' and a black cell at column y > y', then row would have black cells at columns > y', but white at y' < y, violating monotonicity. So impossible.

Thus the algorithm will catch that.

Now we need to handle the case where there are no constraints for a row but there is a B in a later column and W in earlier column across rows. Since R_i is monotone, we need to ensure that the row intervals across rows are compatible.

Our greedy algorithm should detect that.

Now we need to think about the possibility of a column having constraints that are not captured by row constraints? Let's think deeper: The condition for a column is that the black cells in that column form a prefix of rows. This is automatically satisfied by any monotone R. So no extra constraints.

But is there any hidden requirement that the column's C_j must be integer? Yes, they are integer counts.

Now consider a B cell at (x,y) and a W cell at (x',y') where x < x' and y > y'. Could that cause conflict even if row intervals are satisfied? Let's see: Row x has R_x ≥ y, row x' has R_{x'} ≤ y'-1 (since W). Since R is non-increasing, we need R_x ≥ R_{x'}. So we need y ≤ R_x and R_{x'} ≤ y'-1. Since R_x ≥ R_{x'}, we need y ≤ R_x and also R_{x'} ≤ y'-1. This yields y ≤ R_x and R_{x'} ≤ y'-1, and R_x ≥ R_{x'}. Could there be a conflict? For example, suppose y=5, y'=4. Then R_x ≥5, R_{x'} ≤3. Since R_x ≥ R_{x'}, we need R_x ≥ R_{x'}, but R_x could be 5, R_{x'} 3, okay. So no conflict. But if y=4, y'=5 (i.e., B is above and to left of W? Actually x < x' (B row above W row), but y < y'? B at (1,4), W at (2,5). That's B above left of W below right. That is allowed: B in row1 col4, W in row2 col5. Row1 must have at least 4 black cells; row2 must have at most 4 black cells? Actually W at (2,5) means R_2 ≤ 4. Since R_1 ≥ 4, R_2 ≤ 4, okay. So fine.

Thus the only constraints are per row.

Thus solution: read constraints, compute per-row L_i and U_i, sort rows, apply greedy.

Complexities: O(M log M) for sorting, M up to 2e5.

Now we must be careful with the definition of L_i and U_i. If a row has only B cells, U_i = N (since no W). If a row has only W cells, L_i = 0 (since no B). Actually default L_i = 0, U_i = N.

Edge Cases: N can be up to 1e9, but M up to 2e5. Use 64-bit.

Now we should test on sample inputs.

Sample 1:

N=4, M=3
(4,1) B => row4 L=1
(3,2) W => row3 U=1 (since min W y=2 => 2-1=1)
(1,3) B => row1 L=3

Rows: 1: L=3, U=N=4
Row3: L=0, U=1
Row4: L=1, U=4

Processing:
previous_max = N = 4.
Row1: min(U, previous_max) = min(4,4)=4, L=3 <=4 => ok. Set R1=4, previous_max=4.
Row3: min(U, previous_max) = min(1,4)=1, L=0 <=1 => ok. Set R3=1, previous_max=1.
Row4: min(U, previous_max) = min(4,1)=1, L=1 <=1 => ok. Set R4=1, previous_max=1.
All good => Yes.

Sample 2:

N=2, M=2
(1,2) W => row1 U = 1 (min W y=2 => 1)
(2,2) B => row2 L = 2

Rows:
Row1: L=0, U=1
Row2: L=2, U=2 (since no W, U=N=2)
Processing:
prev=N=2.
Row1: min(U,prev)=min(1,2)=1, L=0 <=1 => ok. R1=1, prev=1.
Row2: min(U,prev)=min(2,1)=1, L=2 >1 => impossible => No. Output No. Matches sample.

Sample 3:

N=1, M=1
(1,1) W => row1 U = 0 (min W y=1 => 0)
L=0.
Processing: prev=N=1.
Row1: min(U,prev)=min(0,1)=0, L=0 <=0 => ok => Yes. Output Yes. Matches.

Sample 4:

N=2289, M=10
Let's parse constraints:
1: (1700,1083,W) => row1700 U=1082
2: (528,967,B) => row528 L=967
3: (1789,211,W) => row1789 U=210
4: (518,1708,W) => row518 U=1707
5: (1036,779,B) => row1036 L=779
6: (136,657,B) => row136 L=657
7: (759,1497,B) => row759 L=1497
8: (902,1309,B) => row902 L=1309
9: (1814,712,B) => row1814 L=712
10: (936,763,B) => row936 L=763

Now let's compute per row intervals:

Row136: L=657, U=N=2289
Row518: L=0, U=1707
Row528: L=967, U=2289
Row759: L=1497, U=2289
Row902: L=1309, U=2289
Row936: L=763, U=2289
Row1036: L=779, U=2289
Row1700: L=0, U=1082
Row1789: L=0, U=210
Row1814: L=712, U=2289

Now process in order:

prev = N = 2289.

Row136: min(U,prev) = 2289 (U=N). L=657 <= 2289 => ok. R136=2289, prev=2289.
Row518: min(U,prev) = min(1707,2289) = 1707. L=0 <=1707 => ok. R518=1707, prev=1707.
Row528: min(U,prev) = min(2289,1707)=1707. L=967 <=1707 => ok. R528=1707, prev=1707.
Row759: min(U,prev) = min(2289,1707)=1707. L=1497 <=1707 => ok. R759=1707, prev=1707.
Row902: min(U,prev) = min(2289,1707)=1707. L=1309 <=1707 => ok. R902=1707, prev=1707.
Row936: min(U,prev) = min(2289,1707)=1707. L=763 <=1707 => ok. R936=1707, prev=1707.
Row1036: min(U,prev) = min(2289,1707)=1707. L=779 <=1707 => ok. R1036=1707, prev=1707.
Row1700: min(U,prev) = min(1082,1707)=1082. L=0 <=1082 => ok. R1700=1082, prev=1082.
Row1789: min(U,prev) = min(210,1082)=210. L=0 <=210 => ok. R1789=210, prev=210.
Row1814: min(U,prev) = min(2289,210)=210. L=712 >210 => impossible => No. So answer No. Matches sample.

Thus algorithm works on samples.

Now we need to think about correctness more formally.

We have constraints: For each row i, L_i ≤ R_i ≤ U_i, where L_i = max_{B in row i} y (or 0 if none), U_i = min_{W in row i} (y-1) (or N if none). The condition that R_i is non-increasing across rows (R_i ≥ R_{i+1}) ensures column condition.

We need to check existence of such sequence.

This is a classic problem: existence of non-increasing sequence with upper and lower bounds. Greedy from top with max possible works.

Proof: Suppose we have any feasible sequence. At the first row, we must have R_1 ≤ U_1 and R_1 ≤ N. Since we want to maximize R_1 to allow later rows, we can set R_1 = min(U_1, N) (which is ≤ any feasible R_1 because any feasible R_1 ≤ min(U_1,N)). Actually we need to ensure that there exists a feasible sequence with R_1 = min(U_1,N). If not, maybe we need to lower R_1? But we can always lower R_1 to meet constraints of later rows? Wait, later rows have lower bounds L_i. If we set R_1 too high, later rows can be set lower, as long as they satisfy their own intervals and monotonicity. So the maximum possible R_1 is min(U_1,N). If we set R_1 to that, can we always extend? Not necessarily: Suppose later row has L_j > min(U_1,N). Then we cannot satisfy because R_1 must be ≥ R_j ≥ L_j, but R_1 is too small. However, we could set R_1 larger? But R_1 cannot exceed U_1. If L_j > U_1, then impossible anyway. So if L_j ≤ U_1, we might set R_1 = U_1, but also need to keep R_1 ≤ N. Actually we need R_1 to be at least L_j (if j=2). So we need L_2 ≤ R_1 ≤ U_1. If L_2 > U_1, impossible. So the condition L_2 ≤ U_1 is necessary. Our greedy will detect that: when processing row 2, previous_max = R_1 (set to min(U_1,N)). If L_2 > min(U_1,N), then impossible. So greedy correctly fails.

Thus the greedy algorithm that sets each R_i = min(U_i, previous_max) works: It yields the maximal possible value for each row, which is safe for future rows (since future rows only require lower bounds). If at any point L_i > min(U_i, previous_max), then no feasible solution exists because any feasible R_i must be ≤ min(U_i, previous_max) (since R_i ≤ U_i and R_i ≤ previous_max) and also must be ≥ L_i. Since L_i > min(...), impossible.

Thus algorithm is correct.

Now we need to implement.

Implementation details:

- Use dictionaries: L = dict, U = dict.
- Iterate over M constraints: read x, y, c.
- If c == 'B':
   - L[x] = max(L.get(x, 0), y)
- Else: # W
   - U[x] = min(U.get(x, N), y-1)

Note: For W, we need to store min of (y-1). Since we start with U default N, we take min.

After processing all constraints, we have constraints for some rows. For rows that have only B or only W, we need to set the other bound accordingly: L default 0, U default N.

Now we need to combine L and U for each row: For each row that appears either in L or U, we need to get L_i and U_i. We can iterate over all keys.

We also need to consider rows that have no constraints: they are irrelevant, but we need to process rows in order. However, we can simply iterate over sorted unique row indices that have constraints. Since there may be rows with only B (U=N) or only W (L=0). That's fine.

Processing:

sorted_rows = sorted(keys)

prev = N (or maybe N is the maximum allowed for any row). Actually we need to start with previous_max = N (since R_1 can be at most N). However, we also need to consider that the first constrained row may not be row 1. For rows before that, we can set them to N (or any value >= later rows). Since we want to maximize, we set previous_max = N.

Now for each row in sorted_rows:

- L_i = L.get(row, 0)
- U_i = U.get(row, N)

- If L_i > U_i: impossible.

- allowed_upper = min(U_i, prev)
- If L_i > allowed_upper: impossible.
- Set R_i = allowed_upper (or any value between L_i and allowed_upper). We'll set R_i = allowed_upper to keep prev high.
- prev = R_i

After loop, answer Yes.

Now we need to think about potential pitfalls: The first row may be row > 1. For rows 1..first_row-1, they have no constraints. We can set them to N (or any value). Since we start prev = N, that matches.

Edge Cases:

- N=1, M=0? Actually M >= 1 per constraints. But maybe M can be 0? The problem says 1 ≤ M ≤ min(N^2, 2e5). So M >= 1. But we can handle M=0 as trivial Yes.

- L_i may be > N? Since y ≤ N, L_i ≤ N. U_i may be -1? Since y-1 can be 0. If there is a W with y=1, then y-1 = 0, so U_i = 0. That's okay. If y=1 and also B in same row? That would be contradictory (B at y=1, W at y=1 cannot both). But B at y>1, W at y=1 => L_i = max B y >= 2, U_i = 0, L_i > U_i => impossible.

- N up to 1e9, need 64-bit (Python int fine).

- Need to handle large N but small M.

Now let's test on some random small cases to be sure.

We'll write a brute-force checker for small N (e.g., N <= 5) to verify algorithm.

But before coding, we should also think about any hidden constraints: The condition for each column is that there exists i such that topmost i cells are black, rest white. This is exactly the column condition. We argued that any monotone R yields a valid column condition. Let's verify with an example where R_i is monotone but column condition might be violated due to shape not being "left-aligned"? Wait, we define row i black cells are columns 1..R_i. That's left-aligned. So shape is left-aligned. For column j, black cells are rows i where R_i ≥ j. Since R_i is monotone non-increasing, the set of rows where R_i ≥ j is a prefix (since as i increases, R_i decreases or stays same). So column j's black cells are topmost C_j rows, where C_j = max{i | R_i ≥ j} (or 0). So column condition satisfied. So indeed any monotone R works.

Thus the problem reduces to row constraints only.

Now we should also consider the possibility of a column having constraints that are not captured by row constraints because of the "exists i" condition: For a column, we need there exists i such that top i are black, rest white. This is always satisfied if the set of black cells in that column is a prefix of rows. But we need to ensure that there is no column where the black cells are not a prefix (i.e., some white above black). However, with monotone R, the black cells in each column are exactly the rows i with R_i ≥ j. Since R_i is non-increasing, this set is a prefix (maybe empty). So satisfied. So no extra constraints.

Thus algorithm stands.

Now we should think about possible tricky cases where the greedy algorithm may fail due to the choice of R_i = allowed_upper. Could there be a case where we need to pick a smaller R_i to allow later rows to have lower bounds? Since later rows have lower bounds L_j. If we pick a large R_i, it may restrict later rows because they must be ≤ R_i. But we also need to satisfy L_j. Since we are picking the maximum possible, we are not restricting later rows beyond necessary: we are giving them the largest possible upper bound (since later rows' upper bound is min(U_j, previous_R). If we pick a smaller R_i, previous_R would be smaller, which can only make the min smaller, making it harder for later rows to meet their lower bounds. So picking the maximum is optimal.

Thus greedy is correct.

Now we need to implement in Python.

Edge Cases: When there are no constrained rows (M=0). Then answer Yes (since we can set all rows to N or any monotone sequence). Our algorithm will have empty sorted_rows, and we will output Yes.

Now we need to think about the possibility of large N but many rows with constraints that are far apart. Our algorithm uses only sorted rows with constraints. Complexity O(M log M). Good.

Now we need to verify with more test cases, including random small N brute force.

We'll also need to think about potential pitfalls with Python's default recursion depth? Not needed.

Now we will write the solution accordingly.

But before finalizing, we need to consider if there is any scenario where the column constraints impose something beyond row constraints. Let's test with a brute force for small N and random constraints, comparing our algorithm's answer with brute force enumeration of all possible R_i sequences (0..N monotone) to see if any case is mismatched.

We'll do that later.

But first, let's think about the shape representation: The condition is that the matrix is a Young diagram (Ferrers diagram) anchored at top-left. This is exactly the set of binary matrices with rows non-increasing and columns non-increasing. This is known as a "Young diagram" or "order ideal" of the product poset. Indeed, a binary matrix where rows are left-aligned and columns are top-aligned is exactly a Ferrers diagram (or order ideal) in the grid poset (i,j) <= (i',j') if i ≤ i' and j ≤ j'. The condition that each row is a prefix and each column is a prefix is exactly the condition of being a lower order ideal (or upper?). Actually, a Young diagram is defined as a set of cells (i,j) such that if (i,j) is in the set, then all cells (i',j') with i' ≤ i, j' ≤ j are also in the set. That's exactly the condition: black cells form a down-right closed set (i.e., if a cell is black, all cells above and left are black). The row condition says each row is left-aligned: if cell (i,j) is black, then all cells (i, j') with j' ≤ j are black. That's left alignment. The column condition says each column is top-aligned: if cell (i,j) is black, then all cells (i',j) with i' ≤ i are black. Combined, we get the order ideal property: if (i,j) is black, then all cells (i',j') with i' ≤ i, j' ≤ j are black. This is exactly a Young diagram. So we need to determine if the set of precolored cells can be extended to an order ideal (i.e., down-right closed set) where black cells are the order ideal. Indeed, we need to find an order ideal that contains all B cells and excludes all W cells.

Thus the problem is: Given a poset (grid) and some elements forced to be in the ideal (B) and some forced to be out (W), does there exist an order ideal consistent? Since the poset is a product of two chains (the grid), the order ideals correspond to monotone matrices. The constraints are that B cells must be in the ideal, W cells must be out. Since the ideal is closed downward (i.e., if a cell is in the ideal, all cells above and left are also in the ideal). This imposes constraints: If a B cell is at (x,y), then all cells (i,j) with i ≤ x, j ≤ y must be black (i.e., must be in the ideal). However, we only have the condition that each row is left-aligned and each column is top-aligned, which is equivalent. But does the condition of being an order force more constraints beyond row/column? Let's examine: The row condition ensures left alignment: if (i,j) is black, then (i, j') for j' ≤ j are black. The column condition ensures top alignment: if (i,j) is black, then (i', j) for i' ≤ i are black. Combined, they indeed enforce the down-right closure: If (i,j) is black, then any (i',j') with i' ≤ i, j' ≤ j is black (by first moving up (i' ≤ i) using column condition, then left (j' ≤ j) using row condition). So the condition is exactly the order ideal.

Thus we need to find an order ideal that contains B cells and avoids W cells. This is a classic problem: For a poset, given a set of forced elements and forced non-elements, is there an order ideal consistent? This is equivalent to checking that no forced element is above a forced non-element (i.e., no B cell is in the down-set of a W cell). Because if a W cell is in the down-set of a B cell, then since B cell is in ideal, all cells in its down-set must be in ideal, including that W cell, contradiction. Conversely, if no such pair exists, can we always find an ideal? For a poset that is a product of two chains (grid), the answer is yes: we can take the ideal generated by the B cells (i.e., all cells (i,j) such that there exists a B cell (x,y) with i ≤ x, j ≤ y). That is the down-set of the B cells. Then we need to check that no W cell lies in that down-set. If not, we can take that as the ideal. Indeed, the minimal ideal containing all B cells is the union of their down-sets. This ideal will be a Young diagram (since down-set of a set of points in product poset is a Young diagram). It will contain all B cells, and will avoid all W cells if no W cell is in any down-set of a B cell. So the condition is exactly that there is no pair (B at (x1,y1), W at (x2,y2)) such that x2 ≤ x1 and y2 ≤ y1 (i.e., W is up-left of B). Actually, the down-set of B includes all cells with row ≤ x1 and col ≤ y1. So if a W cell lies in that rectangle (rows ≤ x1, cols ≤ y1), then it's forced black, contradiction. So the condition is: For any B cell (x,y) and any W cell (x',y'), we cannot have x' ≤ x and y' ≤ y. In other words, no B cell is to the right and below a W cell. Equivalent to: For each B cell, all cells in its "upper-left" rectangle must be black (or at least not white). Since we can choose any ideal that contains B cells, the minimal one is the down-set of B's. If any W cell is in that down-set, impossible. If none, then we can set the shape to be exactly that down-set (or maybe larger). So the condition reduces to: There is no B cell that is "south-east" of a W cell (i.e., W cell is north-west of B). Actually we need to check: W cell cannot be north-west of B? Let's see: W cell (x_w, y_w) cannot be in the down-set of B cell (x_b, y_b). That means we cannot have x_w ≤ x_b and y_w ≤ y_b. So we cannot have a W cell that is above (row less) and left (col less) of a B cell. So any W cell must be either below (row > x_b) or to the right (col > y_b) of each B cell. In other words, the set of B cells must be "south-east" extreme: there is no W cell that is north-west of any B cell.

Thus a simple necessary and sufficient condition is: For all B (x1,y1) and W (x2,y2), we must have x2 > x1 or y2 > y1 (i.e., not both ≤). Equivalent to: max_{B} (x coordinate) ??? Actually we can think in terms of constraints on rows: The condition is that for each row, the leftmost white cell must be to the right of the rightmost black cell? Let's see: For a given row i, suppose there is a black cell at column y_B and a white cell at column y_W. If y_W < y_B, then the white cell is left of black cell in same row, which is impossible because row must be left-aligned black. So for each row, we need that all white cells are to the right of all black cells (or no white cells left of black cells). That is exactly the per-row interval condition: L_i ≤ U_i. For rows, we already have that.

But also cross-row constraints: A white cell at (x_w, y_w) could be above a black cell at (x_b, y_b) with x_w < x_b and y_w < y_b. That would be a W north-west of B, which is also impossible because then the rectangle defined by B would include that W. So we need to avoid any such pair. However, does the per-row interval condition plus monotonicity automatically enforce this? Let's test.

Suppose we have B at (2,2) and W at (1,1). Row 1 has W at col 1, so U_1 = 0 (since y-1=0). Row 2 has B at col 2, so L_2 = 2. Process: prev = N. Row1: allowed_upper = min(0, N) = 0, L_1=0 ≤0 => R1=0. prev=0. Row2: allowed_upper = min(N, 0) = 0, L_2=2 >0 => impossible. So algorithm catches it.

Thus the greedy algorithm with intervals catches the cross-row constraints.

Now consider a case where per-row intervals are individually feasible, but cross-row constraints cause conflict? Let's try to find such a case. Suppose we have B at (2,1) and W at (1,2). Row1: W at col2 => U_1=1. Row2: B at col1 => L_2=1. Process: Row1: allowed_upper = min(1,N)=1, L1=0 => R1=1, prev=1. Row2: allowed_upper = min(N,1)=1, L2=1 => R2=1, prev=1. So feasible. But does this correspond to a valid shape? Let's test: R1=1, R2=1. Row1 has 1 black cell (col1). Row2 has 1 black cell (col1). So cell (1,2) is white (since R1=1, col2 >1). That's consistent with W at (1,2). Cell (2,1) is black (col1 ≤1). Good. So cross-row constraints satisfied. So no issue.

Now consider B at (2,2) and W at (1,3). Row1: W at col3 => U1=2. Row2: B at col2 => L2=2. Process: Row1: allowed_upper = min(2,N)=2, L1=0 => R1=2, prev=2. Row2: allowed_upper = min(N,2)=2, L2=2 => R2=2. So feasible. Shape: Row1 has 2 blacks (col1,2). Row2 has 2 blacks (col1,2). Cell (1,3) is white (col3>2). Good.

Now consider B at (2,3) and W at (1,2). Row1: W at col2 => U1=1. Row2: B at col3 => L2=3. Process: Row1: allowed_upper = min(1,N)=1, L1=0 => R1=1, prev=1. Row2: allowed_upper = min(N,1)=1, L2=3 >1 => impossible. So caught.

Thus per-row intervals plus monotonicity seems to capture all constraints.

Now we can think of the problem as: we need to assign each row i a "cut" column R_i such that for each row i, all black cells are in columns ≤ R_i, and all white cells are in columns > R_i. That's exactly the per-row constraints. The monotonicity ensures columns also satisfy top alignment.

Thus the solution is correct.

Now we should think about potential edge cases with large N and many rows but only a few constraints. For example, N=1e9, M=2e5, each in distinct rows. The algorithm will sort up to 2e5 rows, fine.

Now we need to implement reading input. Since N can be up to 1e9, we store as int.

Potential issues: When U_i becomes negative? If there is a white cell with y=1, then y-1 = 0, so U_i = min(previous, 0) = 0. If there are multiple whites, min may be 0 or negative? Actually y-1 >= 0 always, because y >= 1. So U_i >= 0. However, if we have a white cell with y=1, we get U_i=0. That's fine. But if we have a white cell with y=1 and also a white cell with y=1, same. So U_i is non-negative.

But what if there is a white cell with y=1 and also a black cell with y=1? That cannot happen because same cell cannot be both. So L_i and U_i can be both defined for same row only if there are both B and W in same row, which is allowed as long as they are in different columns. Then L_i = max B y, U_i = min W y - 1. If min W y = 1, then U_i = 0. So L_i must be ≤ 0, which implies no black cells in that row (since L_i >= 1 if any B). So impossible. So algorithm will detect L_i > U_i.

Now we need to consider that U_i default is N. If there is a white cell with y=1, U_i becomes 0. That's okay.

Now we also need to consider that the row intervals may be large, but N is up to 1e9, so we can store in Python int.

Now we need to ensure that we handle potential integer overflow? Not in Python.

Now we need to write the solve() function accordingly.

Pseudo-code:

def solve():
    import sys
    input = sys.stdin.readline
    N, M = map(int, input().split())
    L = {}
    U = {}
    for _ in range(M):
        x, y, c = input().split()
        x = int(x)
        y = int(y)
        if c == 'B':
            if x in L:
                if y > L[x]:
                    L[x] = y
            else:
                L[x] = y
        else: # W
            # U[x] = min(U.get(x, N), y-1)
            cur = U.get(x)
            if cur is None:
                U[x] = y - 1
            else:
                if y - 1 < cur:
                    U[x] = y - 1
    # Build list of rows with any constraint
    rows = set(L.keys()) | set(U.keys())
    # For each row, get L_i and U_i
    # But we need to process in order.
    # We'll create a list of (row, L_i, U_i)
    constrained = []
    for r in rows:
        li = L.get(r, 0)
        ui = U.get(r, N)
        if li > ui:
            print("No")
            return
        constrained.append((r, li, ui))
    constrained.sort(key=lambda x: x[0])
    prev = N
    for r, li, ui in constrained:
        # Ensure li <= ui (already checked)
        # allowed upper bound for R_r
        ub = ui
        if prev < ub:
            ub = prev
        # Actually ub = min(ui, prev)
        # check li <= ub
        if li > ub:
            print("No")
            return
        # set R_r = ub (or any value between li and ub)
        prev = ub
    print("Yes")

We need to be careful: For rows that have only B, U = N, so ub = min(N, prev) = prev (if prev <= N). Since prev starts at N, ub = N for first row. That's fine.

Now, is there any scenario where we need to consider that there may be a row with no constraints that appears between two constrained rows, but we need to adjust prev because of that row? Since we can set unconstrained rows to any value ≤ prev, we can keep prev unchanged (or lower). The greedy algorithm sets prev to the chosen R_i for constrained rows. For unconstrained rows, we could keep prev same (or lower). Since we want to maximize prev for later rows, we keep it unchanged (i.e., set unconstrained rows to prev). However, is it always possible to set unconstrained rows to prev while maintaining monotonicity? Yes, because they just need to be ≤ previous row. If we set them equal to prev, monotonicity holds (non-increasing). If we set them lower, also fine. So we can treat them as no effect.

Thus the algorithm is correct.

Now we need to test on random small N with brute force to be sure.

Let's do mental test for N=2, all possible constraints.

We can enumerate all possible R sequences (0..2 monotone). For each, we can compute the set of B/W constraints and see if matches.

But we trust the logic.

Now we also need to think about memory: Using dict for L and U is fine.

Potential pitfalls: Input lines may have spaces; we split accordingly.

Now we should also consider that the input may contain duplicate rows for B and W; we need to combine them correctly.

Now let's test with more random examples manually.

Case: N=3, M=0 (but M>=1 per constraints). But we can test with M=0: algorithm returns Yes.

Case: N=3, B at (2,2). Row2 L=2, U=3. Row1 unconstrained. Process: prev=3. Row2: ub = min(3,3)=3, L=2 <=3 => ok, prev=3. Yes. Indeed we can set R2=2, R1=3 (or 2). Works.

Case: N=3, W at (2,2). Row2 U=1 (since y-1=1). Row2 L=0. Process: prev=3. Row2: ub = min(1,3)=1, L=0 <=1 => ok, prev=1. Yes. Set R2=1 (or 0). Row1 can be up to 3, but must be >= R2=1, fine.

Case: N=3, B at (1,3) and W at (3,1). Row1 L=3, U=3. Row3 L=0, U=0 (since y=1 => y-1=0). Process: prev=3. Row1: ub = min(3,3)=3, L=3 <=3 => ok, prev=3. Row3: ub = min(0,3)=0, L=0 <=0 => ok, prev=0. Yes. Shape: Row1 full black, Row2 maybe any, Row3 empty. Works.

Case: N=3, B at (2,3) and W at (3,2). Row2 L=3, U=3. Row3 L=0, U=1 (since y=2 => 1). Process: prev=3. Row2: ub = min(3,3)=3, L=3 <=3 => ok, prev=3. Row3: ub = min(1,3)=1, L=0 <=1 => ok, prev=1. Yes. Row2 full black, Row3 has at most 1 black. That is consistent: Row2 black cells columns 1..3, Row3 black cells column 1 maybe. W at (3,2) is white (col2>1). B at (2,3) is black (col3 <=3). Good.

Case: N=3, B at (2,2), W at (3,3). Row2 L=2, Row3 U=2 (y=3 => 2). Process: prev=3. Row2: ub = min(3,3)=3, L=2 <=3 => ok, prev=3. Row3: ub = min(2,3)=2, L=0 <=2 => ok, prev=2. Yes. Row2 R=2, Row3 R=2. Works.

Case: N=3, B at (2,1), W at (1,2). Row1 U=1, Row2 L=1. Process: Row1: ub = min(1,3)=1, L=0 <=1 => ok, prev=1. Row2: ub = min(3,1)=1, L=1 <=1 => ok, prev=1. Yes. R1=1, R2=1. Row1 black col1, Row2 black col1. W at (1,2) white. Good.

Case: N=3, B at (1,1), W at (1,2) same row. Row1 L=1, U=1 (since y=2 =>1). L=U=1, feasible. R1=1. Works.

Case: N=3, B at (1,2), W at (1,1) same row. Row1 L=2, U=0 (since y=1 =>0). L>U => impossible. Indeed cannot have B to the right of W in same row.

Thus algorithm matches.

Now we should also test cross-row case where per-row constraints individually feasible but cross-row cause conflict? Let's try to find such a case. Suppose we have B at (2,2) and W at (1,1). Row1: W at col1 => U1=0. Row2: B at col2 => L2=2. Process: Row1: ub = min(0,3)=0, L1=0 => ok, prev=0. Row2: ub = min(3,0)=0, L2=2 >0 => impossible. So caught.

What about B at (2,1) and W at (1,2). Row1: W at col2 => U1=1. Row2: B at col1 => L2=1. Process: Row1: ub = min(1,3)=1, prev=1. Row2: ub = min(3,1)=1, L2=1 => ok. So feasible. Indeed shape: R1=1, R2=1. Row1 has black col1, white col2. Row2 has black col1. Works.

Now consider B at (2,2) and W at (3,1). Row2 L=2, Row3 U=0 (since y=1 =>0). Process: Row2: prev=3, ub = min(3,3)=3, L2=2 <=3 => ok, prev=3. Row3: ub = min(0,3)=0, L3=0 => ok. So feasible. Shape: Row2 R=2, Row3 R=0. Row3 empty. W at (3,1) is white (col1 >0). B at (2,2) is black. Works.

Now consider B at (2,1) and W at (3,2). Row2 L=1, Row3 U=1 (y=2 =>1). Process: Row2: prev=3, ub = min(3,3)=3, L2=1 => ok, prev=3. Row3: ub = min(1,3)=1, L3=0 => ok. So feasible: R2=3 (or any >=1), R3=1. Row2 can be 3 (full). Row3 has at most 1. W at (3,2) is white (col2 >1). B at (2,1) is black. Works.

Thus seems consistent.

Now we should consider the scenario where there are multiple constraints in the same row, maybe both B and W. The algorithm handles L and U separately.

Now we need to verify that the algorithm also respects the condition that R_i must be integer between 0 and N inclusive. Since we start with prev = N and always set R_i = min(U_i, prev), which is ≤ N. And L_i ≥ 0. So okay.

Now we should think about potential pitfalls: The condition L_i ≤ R_i ≤ U_i ensures row constraints. But we also need to ensure that the column condition is satisfied: The column's black cells must be a prefix of rows. As argued, monotone R ensures that. However, is there any scenario where the row constraints are satisfied but some column's black cells are not a prefix? Let's test with a non-monotone R. But we enforce monotonicity. So fine.

Now we should also think about the possibility that the minimal ideal containing B cells may have rows that are not left-aligned? Wait, the down-set of B cells is a Young diagram, thus left-aligned. So it's fine.

Thus the algorithm is correct.

Now we should consider the possibility of large N and many constraints where we need to process many rows but each row may have both L and U. Our dict approach is fine.

Now we should test on random small N with brute force to be absolutely sure.

We'll write a brute-force generator for N <= 5, generate random constraints (M random cells with random colors), and test our algorithm vs exhaustive search of all monotone R sequences (0..N monotone). Since N small, we can enumerate all sequences R_1 >= R_2 >= ... >= R_N, each between 0..N. For each sequence, we can check if it satisfies all constraints: For each B (x,y): y <= R_x; for each W (x,y): y > R_x. If any sequence works, answer Yes. Compare with our algorithm.

We'll do mental or actual test later.

But before coding, we need to ensure that we haven't missed any nuance: The condition for each column is "There exists an integer i (0 ≤ i ≤ N) such that the topmost i cells are colored black, and the rest are colored white." This is exactly the column condition. In our model, the column's black cells are rows 1..C_j where C_j = max{i | R_i ≥ j}. Since R_i is non-increasing, C_j is well-defined and non-increasing. So column condition satisfied.

Now we should consider if there is any additional condition about the column's i being independent of row's i? No, they are independent.

Thus the problem is solved.

Now we need to write final answer.

But we need to also think about possible pitfalls: The input may have duplicate rows for both B and W, we combine correctly. The default U for a row is N. However, if there is a white cell with y=1, we set U = 0. That's fine.

Now we need to ensure that we treat L and U correctly when a row appears in both L and U. For example, row has both B and W. We compute L and U accordingly. We need to ensure that we don't accidentally treat missing key as 0 for L and N for U. We do that.

Now we also need to consider the case where a row has only W, so L default 0. That's fine.

Now we need to think about potential integer overflow for prev when we set prev = N. N up to 1e9, fine.

Now we also need to think about the case where we have many rows with constraints and we need to iterate over sorted list. Sorting 2e5 rows is fine.

Now we need to produce final answer with code.

Now we will write the solution in Python.

Now we should also consider the possibility of negative U_i: If we have a white cell with y=0? Not possible. So fine.

Now let's test with random small N brute force.

We'll write a small script to generate random constraints for N=3, M random between 0 and 5, and compare.

But we can't run code here, but we can reason. However, to be thorough, we can simulate a few random cases manually.

Case N=3, constraints: B at (2,3), W at (1,1). Row1: W at col1 => U1=0. Row2: B at col3 => L2=3. Process: prev=3. Row1: ub = min(0,3)=0, L1=0 => ok, prev=0. Row2: ub = min(3,0)=0, L2=3 >0 => impossible. Indeed shape cannot have B at (2,3) and W at (1,1) because the W at (1,1) forces row1 to have 0 blacks, so row2 must have ≤0 blacks, contradicting B at col3. So No.

Our algorithm says No.

Case N=3, B at (3,3), W at (2,1). Row2: W at col1 => U2=0. Row3: B at col3 => L3=3. Process: prev=3. Row2: ub = min(0,3)=0, L2=0 => ok, prev=0. Row3: ub = min(3,0)=0, L3=3 >0 => impossible. So No. Indeed row2 empty forces row3 empty.

Case N=3, B at (1,2), W at (3,3). Row1 L=2, Row3 U=2. Process: prev=3. Row1: ub = min(3,3)=3, L1=2 => ok, prev=3. Row3: ub = min(2,3)=2, L3=0 => ok. So Yes. R1=3, R3=2. Row1 full, Row3 2 blacks. Works.

Case N=3, B at (2,2), W at (3,3). Row2 L=2, Row3 U=2. Process: prev=3. Row2: ub = min(3,3)=3, L2=2 => ok, prev=3. Row3: ub = min(2,3)=2, L3=0 => ok. Yes.

Case N=3, B at (2,2), W at (3,2). Row2 L=2, Row3 U=1. Process: prev=3. Row2: ub = min(3,3)=3, L2=2 => ok, prev=3. Row3: ub = min(1,3)=1, L3=0 => ok. Yes. R2=3, R3=1. Row3 has 1 black (col1), white at col2. Good.

Case N=3, B at (2,1), W at (3,2). Row2 L=1, Row3 U=1. Process: prev=3. Row2: ub = min(3,3)=3, L2=1 => ok, prev=3. Row3: ub = min(1,3)=1, L3=0 => ok. Yes. R2=3, R3=1. Works.

Case N=3, B at (1,3), W at (2,1). Row1 L=3, Row2 U=0. Process: prev=3. Row1: ub = min(3,3)=3, L1=3 => ok, prev=3. Row2: ub = min(0,3)=0, L2=0 => ok, prev=0. Yes. Row1 full, Row2 empty, Row3 can be empty. Works.

Case N=3, B at (1,3), W at (2,2). Row1 L=3, Row2 U=1. Process: prev=3. Row1: ub = min(3,3)=3, L1=3 => ok, prev=3. Row2: ub = min(1,3)=1, L2=0 => ok, prev=1. Yes. Row1 full, Row2 R=1, Row3 can be 0. Works.

Case N=3, B at (1,2), W at (2,1). Row1 L=2, Row2 U=0. Process: prev=3. Row1: ub = min(3,3)=3, L1=2 => ok, prev=3. Row2: ub = min(0,3)=0, L2=0 => ok, prev=0. Yes. Row1 R=3, Row2 R=0. Works.

Now test case where B at (1,2) and B at (2,1) (two black cells). Row1 L=2, Row2 L=1. Process: prev=3. Row1: ub = min(3,3)=3, L1=2 => ok, prev=3. Row2: ub = min(3,3)=3, L2=1 => ok. Yes. R1=3, R2=3. Works.

Now test case with W at (1,1) and W at (2,2). Row1 U=0, Row2 U=1. Process: prev=3. Row1: ub = min(0,3)=0, L1=0 => ok, prev=0. Row2: ub = min(1,0)=0, L2=0 => ok. Yes. R1=0, R2=0. Works.

Now test case with B at (1,1) and W at (1,2) same row. Row1 L=1, U=1 => feasible. R1=1. Works.

Now test case with B at (1,2) and W at (1,3). Row1 L=2, U=2 (y=3 =>2). L=U=2 => R1=2. Works.

Now test case with B at (1,2) and W at (2,1) we already did.

Now test case with B at (2,2) and W at (1,3). Row1 U=2, Row2 L=2. Process: prev=3. Row1: ub = min(2,3)=2, L1=0 => ok, prev=2. Row2: ub = min(3,2)=2, L2=2 => ok. Yes. R1=2, R2=2. Works.

Now test case with B at (2,2) and W at (1,4) with N=4. Row1 U=3, Row2 L=2. Process: prev=4. Row1: ub = min(3,4)=3, prev=3. Row2: ub = min(4,3)=3, L2=2 => ok. Yes. R1=3, R2=3. Works.

Now test case with B at (2,3) and W at (1,4) N=4. Row1 U=3, Row2 L=3. Process: prev=4. Row1: ub = min(3,4)=3, prev=3. Row2: ub = min(4,3)=3, L2=3 => ok. Yes. Works.

Now test case with B at (2,3) and W at (1,5) N=5. Row1 U=4, Row2 L=3. Process: prev=5. Row1: ub = min(4,5)=4, prev=4. Row2: ub = min(5,4)=4, L2=3 => ok. Yes. Works.

Now test case with B at (2,4) and W at (1,5) N=5. Row1 U=4, Row2 L=4. Process: prev=5. Row1: ub = min(4,5)=4, prev=4. Row2: ub = min(5,4)=4, L2=4 => ok. Yes. Works.

Now test case with B at (2,4) and W at (1,4) N=5. Row1 U=3 (since y=4 =>3), Row2 L=4. Process: prev=5. Row1: ub = min(3,5)=3, prev=3. Row2: ub = min(5,3)=3, L2=4 >3 => impossible. Indeed, if row1 must have at most 3 blacks, row2 must have ≤3, but B at (2,4) requires row2 >=4. So impossible. Good.

Thus algorithm works.

Now we should also test with many rows and many constraints to ensure no off-by-one errors.

Edge Cases: N=1. There is only one row and one column. L_i can be 0 or 1; U_i can be 0 or 1 (since N=1). The algorithm: prev=N=1. Process row if any constraint. For row1: L=0 or 1; U=0 or 1. Check L <= U. Then ub = min(U, prev) = min(U,1). If L <= ub, ok. Works.

Now we should consider the case where there are constraints for row i but we also have constraints for row i+1 but we skip row i because no constraints. But we need to process them in order. Our loop processes all constrained rows sorted. That's fine.

Now we also need to think about potential integer overflow in Python? Not needed.

Now we should think about potential hidden constraints: The problem says N up to 1e9, M up to 2e5. Input size is manageable.

Now we need to produce final code with solve().

Now we should also think about the possibility that the shape may need to be defined for all rows, but we only processed constrained rows. The unconstrained rows can be set to any value ≤ previous prev, and they won't cause any new constraints. So fine.

Now we should also consider if there is any need to consider column constraints directly. As argued, not needed.

Now we need to produce final answer.

But we should also double-check the initial reasoning: The condition that each row has leftmost i cells black and the rest white is exactly a row cut. The condition that each column has topmost i cells black and rest white is exactly a column cut. The set of binary matrices satisfying both is exactly the set of Young diagrams (order ideals). This is a known fact: A binary matrix with monotone rows and columns (both non-increasing) is exactly a Ferrers diagram. Indeed, row condition ensures each row is a left-justified block of 1's. Column condition ensures each column is a top-justified block of 1's. Combined, they form a Young diagram.

Thus the shape is a Young diagram. The shape can be described by a non-increasing sequence R_i of row lengths. Equivalent to a "cut" function.

Thus the problem reduces to checking if there exists a Young diagram that contains given black cells and avoids given white cells.

Now the greedy algorithm is standard: we can treat each row's required black length as lower bound, and required white start column as upper bound+1. Then we need to assign a non-increasing sequence of row lengths within those bounds.

Thus solution is correct.

Now we need to produce final answer with explanation.

But we also need to be careful about the definition of U_i: For a white cell at column y, we require R_i ≤ y-1. So U_i = min_{W in row i} (y-1). If there is no white cell, U_i = N. So we need to compute min(y-1). For y=1, y-1=0.

Now we also need to think about the case where there is a white cell with y=0? Not possible.

Now we also need to think about the case where there is a white cell with y=N, then y-1 = N-1. So U_i may be N-1.

Now we also need to think about the case where there is a black cell with y=N, then L_i = N.

Now we also need to think about the case where there is a black cell with y=N and also a white cell with y=N (same column) in same row? That would be same cell? Not allowed. But could be different rows. For row i, if we have B at (i,N) and W at (i,N) is impossible. So fine.

Now we should also think about the case where we have a row with both B and W constraints, but they are consistent: L_i ≤ U_i. For example B at y=2, W at y=4 => L=2, U=3. So R_i can be 2 or 3. That matches.

Now we also need to think about the scenario where there is a row with B at y=2 and W at y=3 => L=2, U=2 => R_i=2. That matches.

Now we also need to think about scenario where there is a row with B at y=2 and W at y=2 (impossible). So L=2, U=1 => impossible.

Thus algorithm works.

Now we need to produce final answer.

But before finalizing, we need to consider if there is any scenario where the per-row intervals are feasible but monotonicity fails across rows that are not consecutive. For example, row 1 has L=5, row 2 has L=3, row 3 has L=4 (i.e., lower bound increases again). This is not monotone, but we only need to check monotonicity of the assigned R_i. If we have L_1=5, L_2=3, L_3=4, can we assign R_i non-increasing? Let's test: R1≥5, R2≥3, R3≥4, and R1≥R2≥R3. Since R2≥3 and R3≥4, we need R2≥R3≥4, so R2≥4. That's okay. So we can set R1=5, R2=4, R3=4. This satisfies monotonicity. So lower bounds can be non-monotone; we just need to ensure that we can assign values satisfying monotonicity and upper bounds.

Our greedy algorithm will handle that: It will set R1 = min(U1, N) (maybe large), then R2 = min(U2, R1). If R1 is big, we can set R2 accordingly.

Thus algorithm is robust.

Now we should think about the case where there is a row with L_i > U_i (impossible). Already handled.

Now we need to produce final answer.

But we also need to think about potential alternative solution: The "down-set of B cells must not contain any W cell". That is another way to check. Let's examine that condition: For each B cell (x1,y1) and each W cell (x2,y2), we must have NOT (x2 ≤ x1 and y2 ≤ y1). Equivalent to for each B cell, the rectangle [1..x1] × [1..y1] must contain no W cells. This is a necessary and sufficient condition. Could we implement that simpler? Let's see: For each B cell, we need to ensure that there is no W cell with row ≤ x_B and col ≤ y_B. This can be checked by scanning all B cells and checking the maximum row and column of W cells in the "north-west" region. But N is huge, but M is small. We could sort constraints and use data structures. However, the greedy algorithm we derived is simpler and efficient.

But we should verify that the condition "no W cell is in the down-set of any B cell" is equivalent to our per-row interval + monotonicity condition. Let's see: Suppose we have B cells and W cells. The minimal shape containing B cells is the down-set of B cells (the union of rectangles). If any W cell lies inside that down-set, impossible. If none, we can take that shape. So the condition is exactly that the set of W cells is disjoint from the down-set of B cells. However, is it sufficient? Yes: Because the down-set of B cells is a Young diagram (since down-set of any set in product poset is a Young diagram). That shape contains all B cells and excludes all W cells (by condition). So answer Yes. Conversely, if there is a solution shape S (Young diagram), then S contains all B cells, so S contains the down-set of B cells. Since S is a Young diagram and contains B cells, it must contain the down-set of B cells (the smallest Young diagram containing B cells). Then S cannot contain any W cell, so no W cell is in the down-set of B cells. So condition is necessary and sufficient.

Thus we could also solve by checking that for each W cell, there is no B cell that is southeast (i.e., B row >= W row and B col >= W col). Equivalent to: For each W cell (x_w, y_w), there must be no B cell with x_b >= x_w and y_b >= y_w. This is like a dominance condition. This can be checked by maintaining the maximum column of B cells for each row, etc. But our row-based approach is simpler.

But let's verify that our algorithm indeed corresponds to this condition. For each row, we have lower bound L_i = max column of B in that row. For any W cell (x_w, y_w), we need y_w > R_{x_w} (since R_{x_w} ≤ y_w-1). Since R_{x_w} ≥ L_{x_w}, if y_w ≤ L_{x_w}, then y_w ≤ R_{x_w} (since R_{x_w} ≥ L_{x_w}), causing conflict. So we need y_w > L_{x_w}? Actually we need y_w > R_{x_w} and R_{x_w} can be larger than L_{x_w}, but we need to ensure that we can choose R_{x_w} such that y_w > R_{x_w}. Since R_{x_w} can be at most U_{x_w} (which is min y-1 for W in that row). So we need existence of R_{x_w} ∈ [L_{x_w}, U_{x_w}] such that y_w > R_{x_w}. Since R_{x_w} ≤ U_{x_w} < y_w (since U_{x_w} = y-1). So any R_{x_w} ≤ U_{x_w} satisfies y_w > R_{x_w}. So as long as L_{x_w} ≤ U_{x_w}, we can pick R_{x_w} = U_{x_w} which is < y_w. So per-row constraints ensure each W cell can be satisfied individually. However, we also need to ensure monotonicity across rows: if we have a W cell in an upper row and a B cell in a lower row, we need to ensure that the B cell's required column is not too large relative to the W's allowed column. This is exactly the cross-row constraint that we handle via monotonicity.

Thus our algorithm is correct.

Now we can think about an alternative simpler condition: The condition is that for any B cell (x1,y1) and any W cell (x2,y2), we cannot have x2 ≤ x1 and y2 ≤ y1. This can be checked by scanning all pairs? That would be O(M^2) which is too large. But we can sort constraints and maintain a data structure: For each W cell, we need to check if there is any B cell with row >= x_w and column >= y_w. This is like a 2D dominance query. Since M up to 2e5, we can do offline processing: sort B cells by row descending, and for each W cell, we need to know the maximum column among B cells with row >= x_w. If that max column >= y_w, then conflict. We can sort B cells by row descending and process W cells sorted by row descending, maintaining a data structure (like a segment tree or BIT) to query max column for rows >= current. But we also need to handle that B cells may be in same row as W cell (x2 = x1) and column y2 <= y1. That also violates because then W is left of B in same row. That's covered by per-row condition L_i > U_i. So we need to combine per-row and cross-row checks. But our greedy algorithm does it in O(M log M) with sorting.

Thus we will stick with greedy.

Now we need to produce final answer.

Now we should think about potential pitfalls with Python's recursion or memory. Not relevant.

Now we need to produce final code.

But before final code, we need to think about potential pitfalls: The input may contain trailing spaces or newline. Use strip.

Now we need to produce final answer with explanation.

Now we should also consider that we may need to handle large N but small M. The algorithm uses only O(M) memory and O(M log M) time.

Now we will produce the final answer.

But we also need to think about the scenario where there is a row with no constraints but we might need to consider that the row's R_i must be integer. Since we can set any integer, it's fine.

Now we should also think about the case where there are multiple rows with constraints but they are far apart. The algorithm will handle them.

Now we also need to think about the case where there are no rows with constraints (M=0). The loop will be empty, and we output Yes. That's correct.

Now we should also think about the case where there is a row with constraints that is beyond N? Not possible.

Now we also need to think about the case where there is a row with constraints that is repeated many times. We need to combine them correctly: For B, we take max y; for W, we take min y-1.

Now we need to ensure that we treat the default values correctly: L_i default 0, U_i default N.

Now we need to ensure that we treat the case where a row has both B and W constraints and L_i > U_i => impossible.

Now we need to produce final answer.

Now we can produce final code.

Now we also need to write the explanation in the final answer: describe reduction to Young diagram, row constraints, greedy.

Now we can produce final answer.

But before final answer, we should test on some random small N with brute force. Let's do mental simulation for N=3, all possible constraints sets (maybe we can reason about completeness). But we trust the logic.

Now we can produce final answer.

But we also need to think about the scenario where we have multiple rows with constraints and the intervals cause a situation where we need to pick a value less than min(U_i, prev) to allow later rows to have lower bounds? But we argued that picking the maximum possible is always safe because it doesn't restrict later rows more than necessary. However, is there a case where picking the maximum possible for row i causes later row j to have L_j > ub (i.e., L_j > min(U_j, prev))? Since prev after row i is set to ub (the chosen value). If we had chosen a smaller value for row i, prev would be smaller, making ub for later rows even smaller (since ub = min(U_j, prev)). So that would make it harder to satisfy later L_j. So picking the maximum is best.

Thus greedy is correct.

Now we can produce final answer.

Now we can also consider alternative approach: binary search on answer? Not needed.

Now we will write the final solution.

We need to ensure we handle input reading correctly: N M on first line, then M lines each with X_i Y_i C_i.

Now we can produce final answer.

Now we should also consider that we may need to use fast I/O for large M. Use sys.stdin.buffer.

Now we can produce final answer.

Now we will write the code.

But before writing code, we should think about any corner case where we may need to treat the row constraints differently: For a row with B cells, L_i = max y. However, there is also the condition that the row's black cells must be leftmost, so any cell to the right of L_i must be black? Actually no: The row can have black cells up to R_i, which may be larger than L_i. So L_i is the minimal required black length, but we may have more black cells. So we are allowed to set R_i larger than L_i (subject to U_i). So we have flexibility. Our algorithm sets R_i = min(U_i, prev). This may be larger than L_i. That's fine.

Now we also need to think about the case where we have a row with B at column y, but we might also have W at column y' > y, and we may choose R_i = y (or larger) but must be < y'. Since U_i = y'-1, we can set R_i up to y'-1. So we can set R_i = y (or more) as long as ≤ y'-1. So we can set R_i = min(U_i, prev). If prev is large, we may set R_i = U_i (i.e., y'-1), which may be > y. That is allowed. So we can fill extra black cells to the right of the forced black cells, as long as we don't cross the white cells. This is allowed. So the algorithm may set R_i larger than L_i, which is okay.

Now we also need to think about the case where we have a row with no constraints but later rows have constraints. The algorithm will propagate the maximum allowed value downwards, which may be less than N. That's fine.

Now we need to produce final answer.

Now we can write the code.

One more nuance: The default U_i is N, but if there is a white cell with y=1, we set U_i = 0. That's correct. But what about y=0? Not possible.

Now we also need to consider the case where there is a white cell with y=N, then y-1 = N-1. So U_i = N-1. That's fine.

Now we need to produce final answer.

Now we will write the code with comments.

But we also need to think about the possibility of memory usage: dictionaries with up to 2e5 keys, fine.

Now we can produce final answer.

Now we should also think about the possibility of integer overflow in other languages, but not in Python.

Now we can produce final answer.

Now we can write the final code.

Potential improvements: Use default dict for L and U.

Now we will write the final code.

Now we will also provide a brief explanation in the final answer.

Now we will produce final answer.

But before final answer, we should also test on edge cases:

Case: N=1e9, M=2e5, all constraints are B at column N for each row (distinct rows). Then each row has L_i = N, U_i = N. Process: prev = N. For each row in increasing order, ub = min(N, prev) = N, L_i = N <= N => ok. prev stays N. So Yes. That's correct: we can set each row to have N black cells (full rows). This is possible because each row can be full.

Case: N=1e9, M=2e5, all constraints are W at column 1 for each row. Then each row has U_i = 0, L_i = 0. Process: prev = N. For each row, ub = min(0, prev) = 0, L_i = 0 <= 0 => ok. prev = 0. So Yes. That means all rows are empty (R_i = 0). That's possible: each row has no black cells, so each cell is white, consistent with W constraints. Good.

Case: N=1e9, M=2e5, constraints are B at column 1 for row 1, and W at column 1 for row 2. Row1 L=1, U=N. Row2 L=0, U=0. Process: prev=N. Row1: ub = min(N,N) = N, L=1 <= N => ok, prev=N. Row2: ub = min(0,N) = 0, L=0 <= 0 => ok. So Yes. Row1 can have many blacks, row2 none. Works.

Case: N=1e9, M=2e5, constraints are B at column N for row 2, and W at column 1 for row 1. Row1 U=0, Row2 L=N. Process: prev=N. Row1: ub = min(0,N) = 0, L1=0 <=0 => ok, prev=0. Row2: ub = min(N,0) = 0, L2=N >0 => impossible. So No. Indeed if row1 must be empty, row2 must be empty, contradicting B at (2,N). Good.

Thus algorithm works.

Now we can produce final answer.

Now we will write the final code with solve().

Potential improvements: Use list of tuples for constrained rows, sort.

Now we can produce final answer.

Now we will also include a brief explanation in the final answer.

Now we will write final output.

Now we will produce final answer.</mm:think>### NOTES

The conditions on rows and columns mean that the black cells form a *Young diagram* (left‑ and top‑justified).  
Let `R_i` be the number of black cells in row `i` (0 ≤ R_i ≤ N).  
Because the diagram is left‑justified, the row lengths must be non‑increasing:

```
R_1 ≥ R_2 ≥ … ≥ R_N .
```

For a cell `(x, y)`:
* black   ⇒ `y ≤ R_x`,
* white   ⇒ `y > R_x`.

Thus each row `i` gives a lower bound `L_i = max{ y | (i, y) is black }` (0 if none) and an upper bound `U_i = min{ y-1 | (i, y) is white }` (N if none).  
We need a non‑increasing integer sequence `R_i` with `L_i ≤ R_i ≤ U_i`.

This is feasible iff we can walk through the rows in order keeping the current allowed maximum `prev`.  
For a constrained row we may choose any `R_i` in `[L_i, min(U_i, prev)]`.  
Choosing the largest possible value (`min(U_i, prev)`) is optimal – it never harms later rows.  
If at some row `L_i > min(U_i, prev)`, no solution exists.

The algorithm is O(M log M) (sorting the at most M different rows) and uses O(M) memory.
