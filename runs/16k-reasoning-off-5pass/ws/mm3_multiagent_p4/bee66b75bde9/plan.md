We need to check if there exists a binary matrix where each row is a prefix of B's then W's, and each column is a prefix of B's then W's. This is equivalent to: there exist row thresholds `r_i` (0..N) and column thresholds `c_j` (0..N) such that cell (i,j) is B iff `i <= r_i` and `j <= c_j` (i.e., both row and column thresholds allow B). Actually the condition is: cell (i,j) is B iff `i <= r_i` AND `j <= c_j`. Because row i has B in columns 1..r_i, and column j has B in rows 1..c_j. So a cell is B exactly when both its row's threshold and column's threshold include it.

Given precolored cells: for each (x,y) with color B, we need `r_x >= x` and `c_y >= y`. For color W, we need NOT (`r_x >= x` AND `c_y >= y`), i.e., `r_x < x` OR `c_y < y`.

We need to find if there exist integer arrays `r_i, c_j` in [0,N] satisfying all constraints.

This is a classic feasibility problem. We can think of it as: define `R_i = r_i` (row threshold), `C_j = c_j` (column threshold). For B at (x,y): `R_x >= x` and `C_y >= y`. For W at (x,y): `R_x < x` OR `C_y < y`.

We can try to find the minimum feasible `R` and `C` or check consistency. Since N can be up to 1e9 but M up to 2e5, we only care about rows/columns that appear in constraints.

Observation: For each row i, the constraints from B cells in that row give lower bounds on `R_i` (must be >= max x among B cells in row i). For each column j, similarly lower bounds on `C_j`.

For W cells: `R_x < x` OR `C_y < y`. This is a disjunction. We can handle by considering: if we set `R_x >= x` for some reason, then we must have `C_y < y`. Conversely if `C_y >= y`, then `R_x < x`.

We can try to find a consistent assignment. One approach: treat it as a 2-SAT or bipartite graph problem. Actually we can reduce to checking if there exists a threshold assignment.

Alternative: Since thresholds are monotonic (rows and columns are independent except through W constraints), we can think of it as: we need to choose for each row whether its threshold is "high" (>= some value) or "low". But thresholds are numeric.

Let's think differently. The condition that each row is a prefix of B's means: if cell (i,j) is B, then all cells (i, k) for k <= j must be B. Similarly for columns: if (i,j) is B, then (k,j) for k <= i must be B. So the set of B cells is a "Young diagram" shape: there exists a monotone boundary.

Given precolored cells, we need to check if they are consistent with some Young diagram.

We can think of the boundary: define for each row i, the rightmost B column `R_i` (0 if none). For each column j, the bottommost B row `C_j` (0 if none). Then the condition is: for all i,j, cell (i,j) is B iff `i <= C_j` and `j <= R_i`. Actually careful: if row i has B in columns 1..r_i, then `R_i = r_i`. Column j has B in rows 1..c_j, so `C_j = c_j`. Then cell (i,j) is B iff `i <= c_j` and `j <= r_i`. So the set of B cells is exactly the set of (i,j) such that `i <= C_j` and `j <= R_i`. This is equivalent to: the matrix is determined by the row thresholds and column thresholds.

Now constraints:
- For B at (x,y): we need `x <= C_y` and `y <= R_x`.
- For W at (x,y): we need NOT (`x <= C_y` and `y <= R_x`), i.e., `x > C_y` OR `y > R_x`.

We need to find nonnegative integers `R_i, C_j` in [0,N] satisfying these.

This is similar to a bipartite consistency problem. We can think of it as: we have variables `R_i` and `C_j`. For each B constraint, we get two inequalities: `R_x >= y` and `C_y >= x`. For each W constraint, we get: `R_x < y` OR `C_y < x`.

We can try to find if there exists an assignment. Since the constraints are only between specific pairs, we can use a graph approach.

Observation: If we fix the set of rows that have "large" thresholds and columns that have "large" thresholds, we can check. But thresholds are numeric.

Another approach: Since N is large but M is small, we can consider the constraints only on rows and columns that appear. For rows not appearing, we can set threshold arbitrarily (e.g., 0). Similarly for columns.

We can try to find the maximum possible thresholds? Actually we need to find if there exists any assignment.

Let's think about the W constraint: `R_x < y` OR `C_y < x`. This means that for the pair (x,y), at least one of the two thresholds is "small" (less than the coordinate). This is like a covering condition.

We can model as a bipartite graph where we have rows and columns. For each W cell (x,y), we cannot have both `R_x >= y` and `C_y >= x`. So we cannot have both edges "active".

We can think of it as: we need to assign each row a threshold `R_i` and each column a threshold `C_j`. For each B cell, both thresholds must be large enough. For each W cell, at least one threshold must be small enough.

This is reminiscent of a problem where we can binary search or use a greedy assignment.

Since thresholds are integers up to N, we can think of the decision as: for each row i, we decide a threshold `R_i` (0..N). Similarly for columns.

We can try to find a feasible assignment by considering the constraints as a system of inequalities with disjunctions.

One way: convert to a SAT problem? But M up to 2e5, we need polynomial time.

Observation: The constraints are monotone: if we increase `R_i` or `C_j`, we only make it harder to satisfy W constraints (since we need at least one small). So to satisfy W constraints, we want thresholds as small as possible. But B constraints force some thresholds to be large.

So we can compute lower bounds from B constraints: for each row i, `R_i >= max{ y | (i,y) is B }`. Similarly for each column j, `C_j >= max{ x | (x,j) is B }`. Let `lb_R[i]` and `lb_C[j]` be these lower bounds (0 if no B in that row/column).

Now we need to assign `R_i >= lb_R[i]`, `C_j >= lb_C[j]`, and for each W cell (x,y): `R_x < y` OR `C_y < x`.

We can try to set `R_i = lb_R[i]` and `C_j = lb_C[j]` and see if all W constraints are satisfied. If not, we might need to increase some thresholds? But increasing thresholds makes W constraints harder to satisfy. So if the minimal assignment fails, maybe no assignment exists? Not necessarily: we could increase some thresholds to satisfy some W constraints? Wait, increasing thresholds makes it harder for W constraints because we need at least one small. So if minimal fails, we cannot fix by increasing. But we could decrease some thresholds below their lower bounds? No, B constraints force lower bounds. So the only flexibility is that we can choose thresholds higher than the lower bounds, but that only hurts W constraints. So if the minimal assignment (setting each threshold to its lower bound) fails to satisfy some W constraint, then no assignment exists? Let's check.

Suppose we have a W constraint at (x,y): we need `R_x < y` OR `C_y < x`. If we set `R_x = lb_R[x]` and `C_y = lb_C[y]`, and both are >= the required values (i.e., `R_x >= y` and `C_y >= x`), then the constraint fails. Could we increase one of them to satisfy? No, increasing makes it worse. Could we decrease? No, because of B constraints. So if at minimal assignment both are too large, then no assignment exists. However, we might have the option to increase one threshold to satisfy a B constraint elsewhere? But we already set to lower bound, which is the minimum allowed. So if minimal fails, then indeed impossible.

But wait: what if we set `R_x` higher than its lower bound to satisfy some other B constraint? That would only make it larger, so still fails. So indeed, if the minimal assignment fails a W constraint, then no assignment exists.

But is it always optimal to set thresholds to their lower bounds? Let's think: we want to satisfy as many W constraints as possible. Setting thresholds as small as possible (i.e., at lower bounds) gives the best chance to satisfy W constraints because W constraints require at least one small threshold. So if even at minimal assignment some W constraint fails, then no assignment can satisfy it. Therefore, the condition for feasibility is: for every W cell (x,y), we must have `lb_R[x] < y` OR `lb_C[y] < x`.

But is that sufficient? Let's test with examples.

Sample 1: N=4, M=3.
B at (4,1): row 4: lb_R[4] = max y = 1. Column 1: lb_C[1] = max x = 4.
W at (3,2): row 3: no B, so lb_R[3]=0. Column 2: no B, so lb_C[2]=0. Check: lb_R[3]=0 < 2? Yes, so satisfied.
B at (1,3): row 1: lb_R[1]=3. Column 3: lb_C[3]=1.
Now check all W cells: only one W cell, already satisfied. So condition holds. Output Yes.

Sample 2: N=2, M=2.
W at (1,2): row 1: no B, lb_R[1]=0. Column 2: no B, lb_C[2]=0. Check: 0<2? Yes, so satisfied? But answer is No. So our condition is not sufficient.

Wait, we also need to consider that the thresholds must be consistent with the overall shape. In sample 2, we have W at (1,2) and B at (2,2). Let's compute lower bounds:
B at (2,2): row 2: lb_R[2]=2. Column 2: lb_C[2]=2.
W at (1,2): row 1: lb_R[1]=0. Column 2: lb_C[2]=2. Check: lb_R[1]=0 < 2? Yes, so condition holds. But answer is No. So there must be another constraint.

Let's think: with lb_R[2]=2, lb_C[2]=2, that means row 2 has B in columns 1..2, column 2 has B in rows 1..2. So cell (1,2) would be B because row 1? Wait, row 1 has lb_R[1]=0, so row 1 has no B. But column 2 has lb_C[2]=2, so column 2 has B in rows 1..2. That means cell (1,2) must be B because column 2 says rows 1..2 are B. But we have W at (1,2). Contradiction. So our condition missed this: the W constraint at (1,2) is not satisfied because even though row 1 threshold is small, column 2 threshold is large, so cell (1,2) becomes B. Our condition `lb_R[x] < y OR lb_C[y] < x` is necessary but not sufficient because we also need to consider that if one threshold is small, the other might be large, but the cell is B only if both are large. Actually the condition for cell to be B is: `R_x >= y` AND `C_y >= x`. So for W, we need NOT (R_x >= y AND C_y >= x), i.e., R_x < y OR C_y < x. So if we set R_x = lb_R[x] and C_y = lb_C[y], then the condition is exactly that. So why did sample 2 fail? Let's compute carefully:

For W at (1,2): x=1, y=2. lb_R[1]=0, lb_C[2]=2. Condition: 0 < 2 OR 2 < 1? 0<2 is true, so condition holds. So according to our condition, it should be satisfied. But we know it's impossible. So there must be another W constraint? Actually we have only two constraints. Let's try to assign thresholds: we need R_1, R_2, C_1, C_2 in [0,2].
B at (2,2): requires R_2 >= 2 and C_2 >= 2.
W at (1,2): requires R_1 < 2 OR C_2 < 2.
But C_2 >= 2 from B, so C_2 < 2 is false. So we need R_1 < 2. That is possible: set R_1 = 0 or 1. So we can set R_1=0, R_2=2, C_2=2, and C_1 can be anything. Then check: cell (1,2): R_1=0 < 2, so condition holds. So why is it impossible? Let's construct the grid:
Row 1: R_1=0, so all W.
Row 2: R_2=2, so columns 1,2 are B.
Column 1: C_1? We need to determine. Column 2: C_2=2, so rows 1,2 are B. But row 1 is all W, so cell (1,2) would be B from column condition, but row 1 says W. Contradiction. So the issue is that column 2's threshold forces row 1 to be B, but row 1's threshold forces it to be W. So we cannot have both. So the condition for consistency is not just per-cell, but also that the row and column thresholds must be consistent with each other. In other words, the matrix defined by R and C must be consistent: for all i,j, the color is determined by both, and they must agree. That means we need: for all i,j, if R_i >= j and C_j >= i, then cell is B; otherwise W. So we need to assign R and C such that for all i,j, the color matches. But we only have constraints on some cells. So we need to ensure that there is no conflict between the row and column definitions.

In sample 2, we have a conflict: column 2 says rows 1 and 2 are B, but row 1 says no B. So we need to avoid such conflicts. How to capture this?

We can think of it as: we need to find R_i and C_j such that for all i,j, the implied color is consistent. But we only care about cells that are precolored. However, there might be implicit constraints from the fact that R and C must be consistent with each other. For example, if we set R_i = a and C_j = b, then cell (i,j) is B iff i <= b and j <= a. So if we have a cell that is forced to be B by row i (i.e., j <= R_i) but forced to be W by column j (i.e., i > C_j), then conflict. So we need to ensure that for all i,j, we don't have j <= R_i and i > C_j simultaneously. That is equivalent to: for all i,j, if j <= R_i then i <= C_j. Or equivalently, R_i and C_j must satisfy: R_i >= j implies C_j >= i. This is a kind of duality.

Actually, the condition that the matrix is a Young diagram is equivalent to: the set of B cells is a "order ideal" in the product order: if (i,j) is B, then all (i',j') with i' <= i and j' <= j are B. So the shape is determined by a monotone boundary. The row thresholds R_i and column thresholds C_j are not independent; they must satisfy: R_i = max{ j | (i,j) is B } and C_j = max{ i | (i,j) is B }. So they are consistent by definition. But when we assign arbitrary R and C, we need to ensure that the resulting B set is consistent. That is, if we define B set as {(i,j): i <= C_j and j <= R_i}, then we need that for each i, the set of j with i <= C_j is exactly {1,...,R_i}. That means: for each i, R_i = max{ j : i <= C_j } (or 0 if none). Similarly, C_j = max{ i : j <= R_i }. So R and C must satisfy these mutual relations.

So the problem reduces to: find R_i, C_j in [0,N] such that:
1. For each B cell (x,y): R_x >= y and C_y >= x.
2. For each W cell (x,y): NOT (R_x >= y and C_y >= x).
3. Consistency: for all i,j, R_i >= j iff C_j >= i? Actually not exactly: the condition is that the matrix defined by R and C is exactly the one with row thresholds R and column thresholds C. That means: for each i, the set of j such that cell (i,j) is B is exactly {1,...,R_i}. So for each i and j, cell (i,j) is B iff j <= R_i and i <= C_j. So we need that for each i, R_i = max{ j : i <= C_j } (with max over empty set = 0). Similarly, C_j = max{ i : j <= R_i }.

This is a fixed point condition. So we need to find R and C that satisfy these equations along with the precolor constraints.

This is similar to the concept of "bipartite graph with thresholds" or "matrix with given row and column sums" but here it's about prefixes.

We can think of it as: we need to find a monotone matrix (Young diagram) that contains all B cells and excludes all W cells. So we need to find a Young diagram that contains a given set of B cells and does not contain any W cell. This is a classic problem: given a set of forced B and forced W cells, does there exist a Young diagram containing all B and no W? This is equivalent to checking if the forced B cells are "upward closed" and the forced W cells are "downward closed" in some sense? Actually, a Young diagram is an order ideal: if (i,j) is in the diagram, then all (i',j') with i' <= i, j' <= j are in the diagram. So the complement (W cells) is an order filter: if (i,j) is W, then all (i',j') with i' >= i, j' >= j are W? Not exactly: if (i,j) is W, it means it's not in the diagram. But if (i,j) is not in the diagram, then either i > C_j or j > R_i. So it's not necessarily that all larger cells are W. However, if we have a W cell at (x,y), then we cannot have both R_x >= y and C_y >= x. So if we have a W cell, it imposes that at least one of the thresholds is small. But the consistency condition might impose additional constraints.

We can approach by considering the "boundary" of the Young diagram. Let f(i) be the number of B cells in row i (i.e., R_i). Let g(j) be the number of B cells in column j (i.e., C_j). Then the condition is that for all i,j, the cell (i,j) is B iff i <= g(j) and j <= f(i). This is equivalent to: f(i) = max{ j : i <= g(j) } and g(j) = max{ i : j <= f(i) }. So f and g are "conjugate" in the sense of Young diagrams.

Given precolored cells, we need to find f and g satisfying these and the constraints.

We can try to construct f and g greedily. Since N can be large, we only care about rows and columns that appear in constraints. But there might be interactions.

Another approach: Since the constraints are only on M cells, we can consider the partial order. The condition that there exists a Young diagram containing all B and no W is equivalent to: there is no "inconsistency" where a B cell is "below" a W cell in the product order? Actually, if we have a B cell at (x,y) and a W cell at (x',y') with x' <= x and y' <= y, then the W cell is "southwest" of the B cell. In a Young diagram, if (x,y) is B, then all cells with row <= x and col <= y must be B. So if there is a W cell in that region, it's impossible. So a necessary condition is: for any B cell (x,y) and any W cell (x',y') with x' <= x and y' <= y, we have a contradiction. But that's not sufficient because there might be cycles.

In sample 2: B at (2,2), W at (1,2). Here x'=1 <= 2=x, y'=2 <= 2=y, so W is southwest of B. That is a contradiction. So indeed, the condition is: no W cell is southwest of a B cell. But is that sufficient? Let's test sample 1: B at (4,1), W at (3,2), B at (1,3). Check pairs: W at (3,2) and B at (4,1): 3<=4, 2<=1? No, 2>1, so not southwest. W at (3,2) and B at (1,3): 3<=1? No. So no southwest relation. So condition holds.

Sample 3: N=1, W at (1,1). No B, so condition holds trivially.

Sample 4: We need to check. But likely the condition is exactly that: there is no pair (B at (x,y), W at (x',y')) with x' <= x and y' <= y. Because if such a pair exists, then in any Young diagram containing the B cell, the W cell must also be B (since it's southwest), contradiction. Conversely, if no such pair exists, can we always construct a Young diagram? This is a known result: given a set of forced B and forced W cells, there exists a Young diagram containing all B and no W if and only if there is no forced W cell that is southwest of a forced B cell. But is that always true? Let's think.

Suppose we have forced B cells and forced W cells with no southwest conflicts. We want to find a Young diagram that contains all B and excludes all W. We can define the diagram as the set of cells that are not forced W and are "above" the forced B? Actually, we can take the "upper closure" of the forced B cells: include all cells (i,j) such that there exists a forced B cell (x,y) with i <= x and j <= y. But that might include forced W cells if they are not southwest of any B? Wait, if a forced W cell is not southwest of any forced B cell, then it might not be included in that closure. But we also need to ensure that the resulting set is a Young diagram (order ideal). The upper closure of a set is not necessarily an order ideal; it's an order filter. Actually, if we take all cells that are >= some B cell in the product order, that's an order filter. We want an order ideal. So we should take the lower closure: all cells that are <= some B cell? That would include cells that are northeast of B cells, which might be W. So that's not good.

We need to find an order ideal that contains all B and no W. This is like finding a monotone boundary that separates B and W. This is possible if and only if there is no W cell that is southwest of a B cell. Because if there is no such conflict, we can define the boundary as follows: for each row i, let R_i be the maximum column j such that (i,j) is forced B, or if none, then we can set R_i to be the minimum column j such that (i,j) is forced W minus 1? But we need to ensure consistency.

Actually, we can construct the diagram by taking the "upper envelope" of the forced B cells: for each row i, define R_i as the maximum y such that (i,y) is forced B, or 0 if none. Similarly, for each column j, define C_j as the maximum x such that (x,j) is forced B, or 0 if none. Then consider the matrix defined by these R and C. But as we saw in sample 2, this might not be consistent because the resulting matrix might have a cell that is forced W but becomes B due to the column threshold. So we need to adjust.

We can think of it as a bipartite graph with constraints. There is a known solution for this problem (it's from AtCoder ABC 247 F or similar? Actually it's from AtCoder Grand Contest? I recall a problem "Coloring Grid" or something). The solution is to check for conflicts in a certain way.

Let's search memory: This problem is "Takahashi's Coloring" from AtCoder Beginner Contest 247? Actually it's from AtCoder Regular Contest? I think it's from AtCoder Grand Contest 029? Not sure. But I recall a solution: we can consider the constraints as a graph where we connect rows and columns. For each B cell, we have an edge from row to column with weight? Alternatively, we can think of it as: we need to assign each row a threshold and each column a threshold such that for B cells, both thresholds are at least the coordinate, and for W cells, at least one threshold is less than the coordinate. And also the thresholds must be consistent: if row i has threshold a, then for any column j with threshold b, we must have that cell (i,j) is B iff i <= b and j <= a. This consistency condition is equivalent to: for all i,j, if j <= a then i <= b. That is, a and b must satisfy: a >= j implies b >= i. This is equivalent to: for all i,j, we cannot have a >= j and b < i. So if we set a and b, we need to avoid such pairs.

But we only have constraints on some cells. However, the consistency condition must hold for all i,j, not just the constrained ones. So we need to choose a and b such that for all i,j, the condition holds. This is a strong condition. But note that we can choose a and b freely as long as they satisfy the precolor constraints. So we need to find a and b such that:
- For each B (x,y): a_x >= y and b_y >= x.
- For each W (x,y): not (a_x >= y and b_y >= x).
- For all i,j: if a_i >= j then b_j >= i. (Consistency)

The last condition is equivalent to: for all i,j, a_i < j or b_j >= i. This is similar to the W condition but for all pairs. So we need to satisfy this for all i,j, not just the precolored ones.

This seems like we need to find a and b that are "consistent" in the sense that the matrix defined by them is a Young diagram. This is equivalent to: the sets { (i,j) : a_i >= j } and { (i,j) : b_j >= i } are the same. That is, a_i >= j iff b_j >= i. So we need a_i and b_j to be "conjugate": a_i = max{ j : b_j >= i } and b_j = max{ i : a_i >= j }.

So we need to find a and b that are conjugate and satisfy the precolor constraints.

This is a classic problem: given a set of points that must be inside the diagram and outside, does there exist a Young diagram? The condition is exactly that there is no W point southwest of a B point. Because if there is a W point southwest of a B point, then in any Young diagram containing the B point, the W point must also be inside, contradiction. Conversely, if there is no such conflict, we can construct the diagram by taking the "upper boundary" of the B points: for each row i, let a_i be the maximum y such that (i,y) is B, or if no B in row i, then we can set a_i to be the minimum y such that (i,y) is W minus 1? But we need to ensure that for columns, the thresholds are consistent.

Actually, we can construct the diagram as follows: define the set S = { (i,j) : there exists a B cell (x,y) with i <= x and j <= y }. This is the "lower closure" of the B cells. But this set might include W cells if they are southwest of B cells. If there is no such conflict, then S contains no W cells. But S is an order ideal? Actually, if (i,j) is in S, then there exists (x,y) B with i<=x, j<=y. Then for any (i',j') with i'<=i, j'<=j, we have i'<=x, j'<=y, so (i',j') is also in S. So S is an order ideal. And it contains all B cells. And if there is no W cell southwest of any B cell, then no W cell is in S. So S is a valid Young diagram. So the condition is sufficient.

Thus, the problem reduces to checking if there exists a W cell that is southwest of a B cell. That is, for some B cell (x,y) and W cell (x',y') with x' <= x and y' <= y.

But wait, is that sufficient? Let's test with a potential counterexample. Suppose we have B at (2,2) and W at (1,3). Here x'=1<=2, y'=3>2, so not southwest. So condition holds. Can we construct a Young diagram? We need to include (2,2) and exclude (1,3). One possible diagram: row 1: 0 B, row 2: 2 B. Then column 1: 2 B, column 2: 2 B, column 3: 0 B. Then cell (1,3) is W, cell (2,2) is B. So works.

What about B at (2,2) and W at (3,1)? x'=3>2, so not southwest. Condition holds. Diagram: row 2: 2 B, row 3: 1 B? But then column 1: 3 B? Let's try: row 1: 0, row 2: 2, row 3: 1. Then column 1: rows 1,2,3? Actually column 1: B in rows 1..3 because row 3 has B in column 1. So cell (3,1) is B, but we want W. So we need to adjust. Maybe set row 3: 0. Then column 1: rows 1,2 are B, row 3 is W. So cell (3,1) is W. But then row 2 has B in columns 1,2, so cell (2,2) is B. So works. So condition seems sufficient.

But is it always sufficient? Consider B at (1,2) and W at (2,1). Here x'=2>1, so not southwest. Condition holds. Diagram: row 1: 2 B, row 2: 0 B. Then column 1: rows 1,2? Actually column 1: B in row 1 only because row 2 has 0. So cell (2,1) is W. Cell (1,2) is B. Works.

Now consider a more complex case: B at (2,2) and W at (1,1). Here x'=1<=2, y'=1<=2, so southwest. Condition fails. Indeed impossible.

So the condition seems to be: there is no pair (B, W) such that the W cell is southwest of the B cell. But is that all? What about indirect conflicts? For example, B at (2,2) and W at (1,3) and W at (3,1). No direct southwest. But maybe the diagram that includes (2,2) forces something that conflicts with both W cells? Let's try to construct: We need to include (2,2). So row 2 must have at least 2 B's, so columns 1 and 2 are B in row 2. Column 1 must have at least 2 B's, so rows 1 and 2 are B in column 1. That forces cell (1,1) to be B. But we have W at (1,3) and (3,1). (1,1) is not constrained, so it can be B. But then column 3: we have W at (1,3), so column 3 cannot have B in row 1. So column 3 threshold must be 0. That's fine. Row 3: we have W at (3,1), so row 3 cannot have B in column 1. But column 1 has B in rows 1 and 2, so row 3 column 1 is W, which matches. So we can set: row 1: columns 1,2 B? But column 3 is W in row 1, so row 1 cannot have B in column 3. So row 1 can have B in columns 1,2. But then column 2: rows 1,2 are B, so row 3 column 2? Not constrained. So we can set row 3: 0 B. Then the diagram: row 1: 2 B, row 2: 2 B, row 3: 0 B. Check: cell (1,3) is W (row 1 has only 2 B), cell (3,1) is W (row 3 has 0 B). So works. So no indirect conflict.

But consider B at (2,2) and W at (1,4) and W at (4,1). No direct southwest. Can we construct? Row 2: at least 2 B. Column 1: at least 2 B (from row 2), so rows 1,2 are B in column 1. That forces cell (1,1) B. Column 4: we have W at (1,4), so column 4 cannot have B in row 1. So column 4 threshold must be 0. Row 1: we have W at (1,4), so row 1 cannot have B in column 4. But row 1 can have B in columns 1,2,3? But column 4 is W, so row 1's threshold can be 3. But then column 3: if row 1 has B in column 3, then column 3 must have B in row 1, so column 3 threshold at least 1. That's fine. But we also have W at (4,1), so row 4 cannot have B in column 1. But column 1 has B in rows 1,2, so row 4 column 1 is W, which matches. So we can set: row 1: 3 B, row 2: 2 B, row 3: 0 B, row 4: 0 B. Then column 1: rows 1,2 B, rows 3,4 W. Column 2: rows 1,2 B. Column 3: row 1 B. Column 4: all W. Check: cell (1,4) is W (row 1 has only 3 B), cell (4,1) is W (row 4 has 0 B). So works.

So it seems the condition is exactly that there is no W cell southwest of a B cell. But wait, what about the case where there is a B cell and a W cell that are not directly southwest but through a chain? For example, B at (2,2), W at (1,3), and another W at (3,1). We already saw it works. But what if we have B at (2,2), W at (1,3), and W at (2,1)? Here W at (2,1) is not southwest of B because y'=1 <=2, x'=2 <=2, so actually it is southwest: x'=2 <=2, y'=1 <=2. So that would be a direct conflict. So if we have B at (2,2) and W at (2,1), then it's impossible because row 2 must have B in column 1 (since row 2 has at least 2 B, so column 1 is B). So indeed, any W cell with row <= B's row and col <= B's col is a conflict.

So the condition is: for all B cells (x,y) and all W cells (x',y'), we must not have x' <= x and y' <= y.

But is that sufficient? Let's think about the construction. If there is no such conflict, we can define the Young diagram as the set of all cells (i,j) such that there exists a B cell (x,y) with i <= x and j <= y. This set is an order ideal (if (i,j) is in it, then any (i',j') with i'<=i, j'<=j is also in it because i'<=x, j'<=y). It contains all B cells. And if there is no W cell southwest of any B cell, then no W cell is in this set. So it is a valid Young diagram. So yes, it is sufficient.

But wait: what about cells that are not southwest of any B cell but are forced W? They are not in the set, so they are W, which is fine. So the construction works.

Thus, the problem reduces to checking if there exists a pair (B, W) such that the W cell is southwest of the B cell. That is, for some B cell (x,y) and some W cell (x',y') with x' <= x and y' <= y.

We need to check this efficiently. M up to 2e5, so we can process all pairs? That would be O(M^2), too slow. We need a smarter way.

We can think of it as: for each W cell (x',y'), we need to ensure that there is no B cell with x >= x' and y >= y'. So we need to check if there exists a B cell that is northeast of the W cell. So we can precompute for each row the maximum column index of a B cell in that row, and for each column the maximum row index of a B cell in that column. But that's not enough because a B cell could be in a different row and column.

We can use a sweep line or a data structure. Since we only need to check if there exists any such pair, we can sort the B cells by row descending and column descending, and for each W cell, check if there is a B cell with row >= x' and col >= y'. But we need to be careful: we need to check if there exists a B cell with row >= x' and col >= y'. That is equivalent to: the maximum row among B cells with column >= y' is >= x'. Or we can sort B cells by column, and for each W cell, find the maximum row among B cells with column >= y'. But we also need row >= x'. So we need both conditions.

We can do: sort B cells by column descending. Maintain a data structure (like a segment tree or just a variable) that keeps the maximum row seen so far. For each W cell sorted by column descending, we can query the maximum row among B cells with column >= y'. But we need to ensure that the B cell's row is >= x'. So if the maximum row among B cells with column >= y' is >= x', then there is a conflict. But is that sufficient? Suppose there is a B cell with column >= y' and row >= x', but maybe the maximum row is from a B cell with column < y'? No, we only consider B cells with column >= y'. So if the maximum row among those is >= x', then there exists a B cell with column >= y' and row >= x'. So that works.

But we need to process all W cells. We can sort W cells by column descending. Then we iterate through B cells sorted by column descending, and for each W cell, we add B cells with column >= y' to our data structure. Then we query the maximum row. If that maximum row >= x', then conflict.

However, we need to be careful: the B cell must have row >= x' and column >= y'. So if we maintain the maximum row among B cells with column >= current y', then if that max row >= x', we have a conflict.

But what if there are multiple B cells? We just need one. So this works.

But we also need to consider that the B cell might be in the same row or column? That's fine.

Let's test with sample 2: B cells: (2,2). W cells: (1,2). Sort B by column descending: (2,2) column 2. Sort W by column descending: (1,2) column 2. Process: for W (1,2), we add B cells with column >= 2: (2,2). Max row = 2. Check: 2 >= 1? Yes, so conflict. So output No.

Sample 1: B cells: (4,1), (1,3). W cells: (3,2). Sort B by column descending: (1,3) col 3, (4,1) col 1. Sort W by column descending: (3,2) col 2. Process: for W (3,2), add B cells with column >= 2: only (1,3) has col 3 >=2. Max row = 1. Check: 1 >= 3? No. So no conflict. Output Yes.

Sample 4: We need to check. But likely this works.

But wait, is this condition sufficient? Consider a case where there is no direct southwest conflict, but the constructed Young diagram might have a cell that is forced W but becomes B due to the closure? We argued that if there is no W southwest of any B, then the closure contains no W. But what about a W cell that is not southwest of any B but is in the closure? That would mean there exists a B cell (x,y) such that the W cell (x',y') satisfies x' <= x and y' <= y. That is exactly the definition of southwest. So if no such pair exists, then no W cell is in the closure. So it's safe.

Thus, the algorithm is: read all cells, separate into B and W. Check if there exists a pair (B, W) with B.x >= W.x and B.y >= W.y. If yes, print No; else Yes.

We need to do this efficiently. M up to 2e5, so we can sort and sweep.

Implementation steps:
1. Read N, M.
2. For each cell, store (x, y, color).
3. Separate into list B_cells and W_cells.
4. Sort B_cells by y descending.
5. Sort W_cells by y descending.
6. Initialize a variable max_row = 0.
7. Iterate through W_cells in order of decreasing y. For each W cell (x, y):
   - While there are B cells with y >= current y (i.e., B_cells not yet processed have y >= current y), add their x to max_row (update max_row = max(max_row, x)).
   - Then check if max_row >= x. If yes, then there exists a B cell with y >= current y and x >= x, so conflict. Print No and exit.
8. After processing all W cells, if no conflict found, print Yes.

But careful: we need to process W cells in decreasing y. For each W cell, we need to consider all B cells with y >= W.y. So we can sort B by y descending, and use a pointer to add B cells as we go through W cells sorted by y descending. Since both sorted descending, we can do:

i = 0
for each W in W_sorted:
    while i < len(B_sorted) and B_sorted[i].y >= W.y:
        max_row = max(max_row, B_sorted[i].x)
        i += 1
    if max_row >= W.x:
        conflict

This works.

But what about the case where there are multiple B cells with the same y? That's fine.

We also need to consider that N can be up to 1e9, but coordinates are up to N, so no issue.

Let's test with sample 4 manually? Not necessary, but we can trust.

But wait, is there any other constraint? The problem statement says: for every row, there exists an integer i such that leftmost i cells are black, rest white. That means each row is a prefix of B. Similarly for columns. So our interpretation is correct.

Thus, the solution is to check for the existence of a B cell that is northeast of a W cell. That is, B.x >= W.x and B.y >= W.y.

We should also consider the case where there are no B cells or no W cells. If no B cells, then we can set all rows to 0, so always possible. If no W cells, we can set all rows to N, so always possible. Our algorithm handles that: if B list empty, max_row remains 0, so for any W, max_row >= W.x? Only if W.x <= 0, but W.x >=1, so no conflict. So output Yes. If W list empty, we never enter the loop, so output Yes.

So the algorithm is correct.

Now, we need to write the code in Python.

We'll read input, parse, separate, sort, and sweep.

Complexities: O(M log M) due to sorting.

Let's write the code.

We'll use sys.stdin for fast input.

We'll store B_cells as list of tuples (y, x) for sorting by y descending. Actually we need x and y. We'll sort by y descending.

We'll store W_cells as list of tuples (y, x) as well.

Then sweep.

Edge cases: M up to 2e5, so memory is fine.

Let's code.### PLAN
We need to determine if there exists a binary matrix where each row is a prefix of black cells followed by white cells, and each column is a prefix of black cells followed by white cells. This is equivalent to finding a Young diagram (order ideal) that contains all precolored black cells and excludes all precolored white cells. A necessary and sufficient condition is that no white cell is southwest of any black cell (i.e., for some black cell (x,y) and white cell (x',y'), we have x' ≤ x and y' ≤ y). We can check this efficiently by sorting black cells by column descending and white cells by column descending, then sweeping to maintain the maximum row among black cells with column ≥ current white cell's column. If at any point this maximum row is ≥ the white cell's row, a conflict exists.