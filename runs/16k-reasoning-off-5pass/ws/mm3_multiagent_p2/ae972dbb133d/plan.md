Model each tile's line segment as a set of edge-midpoint connections. For type A (4 rotations) the segment connects two adjacent edges; for type B (2 rotations) it connects two opposite edges. The torus condition requires that for every horizontal adjacency (right edge of (i,j) ↔ left edge of (i,(j+1) mod W)) and every vertical adjacency (bottom edge of (i,j) ↔ top edge of ((i+1) mod H, j)), the two endpoints are either both present or both absent.

We can encode each tile's rotation by a pair of bits (right, down) indicating whether the segment touches the right edge and the bottom edge. The other endpoints are determined by tile type:
- Type A: (right, down) ∈ {(0,0), (0,1), (1,0), (1,1)} (4 choices)
- Type B: (right, down) ∈ {(0,0), (1,1)} (2 choices)

The torus condition becomes: for every horizontal edge, the right bit of (i,j) equals the left bit of (i,j+1); for every vertical edge, the down bit of (i,j) equals the up bit of (i+1,j). Since left = right (for type A) or left = ¬right (for type B), and similarly up = down or up = ¬down, we can express the condition purely in terms of the (right, down) bits.

Let r[i][j] = right bit, d[i][j] = down bit. For type A: left = r, up = d. For type B: left = 1-r, up = 1-d.

Horizontal condition: r[i][j] = (type[i][j]=='A' ? r[i][j] : 1-r[i][j]) of (i,j+1). This forces r[i][j] = r[i][j+1] if both are type A, or r[i][j] = 1-r[i][j+1] if one is type B, etc. Similarly for vertical.

We can solve by treating each row independently for horizontal consistency, then coupling rows via vertical consistency. Since the grid is a torus, we need to handle cycles.

Approach: For each row, the horizontal constraints form a system on a cycle of W cells. We can determine how many valid assignments of r-bits exist per row given the tile types. Similarly for columns with d-bits. But r and d are coupled per cell (both must be chosen from allowed pairs).

Better: Process row by row. For a fixed row, given the d-bits of the previous row (which determine the up bits of current row), we count valid (r,d) assignments for this row satisfying horizontal constraints and vertical constraints with previous row. Then multiply across rows, with the first row's "previous" being itself (cycle).

For a single row of length W with tile types t[0..W-1] (each 'A' or 'B'), we need to count assignments (r[j], d[j]) where:
- (r[j], d[j]) ∈ allowed(t[j])
- r[j] = left(j+1) where left(j+1) = r[j+1] if t[j+1]='A' else 1-r[j+1]
- d[j] = up(j) where up(j) is given from previous row (for j=0..W-1, up(j) is a known bit)

This is a constraint satisfaction on a cycle. We can solve by dynamic programming with two states (r[0] = 0 or 1), propagate around the cycle, and check consistency at the wrap-around.

For each row, given the up-bits vector u[0..W-1] (from previous row's d-bits), we compute the number of valid (r,d) assignments for this row. Then the d-bits of this row become the u-bits for the next row.

Since H can be up to 10^6, we need O(H*W) total. The per-row DP is O(W) given u. But we have H rows, so O(H*W) which is fine (total cells ≤ 10^6).

However, we need to be careful: the DP state depends on u, which changes per row. We can do DP for each row independently.

Let's formalize the row DP:

Given tile types t[0..W-1] and up-bits u[0..W-1] (each 0 or 1), count number of sequences (r[0..W-1], d[0..W-1]) such that:
1. For each j: (r[j], d[j]) is allowed for t[j]:
   - If t[j]='A': (r,d) ∈ {(0,0),(0,1),(1,0),(1,1)} (all 4)
   - If t[j]='B': (r,d) ∈ {(0,0),(1,1)} (2 choices)
2. For each j: d[j] = u[j] (vertical condition with previous row)
3. For each j: r[j] = left(j+1) where left(j+1) = r[j+1] if t[j+1]='A' else 1-r[j+1]

Condition 2 fixes d[j] completely! So d[j] = u[j] is forced. Then r[j] must satisfy:
- If t[j]='A': r[j] can be 0 or 1 (no restriction from d)
- If t[j]='B': r[j] must equal d[j] = u[j] (since only (0,0) and (1,1) allowed)

So r[j] is determined or free depending on t[j]:
- t[j]='B': r[j] = u[j] (forced)
- t[j]='A': r[j] ∈ {0,1} (free)

Now condition 3: for each j, r[j] = (t[j+1]=='A' ? r[j+1] : 1-r[j+1]).

This is a constraint relating r[j] and r[j+1]. Let's define a relation:
- If t[j+1]='A': r[j] = r[j+1]
- If t[j+1]='B': r[j] = 1-r[j+1]

So r[j] = r[j+1] XOR (t[j+1]=='B' ? 1 : 0).

This means r[j] is determined by r[j+1] (or vice versa). Going around the cycle, we get a consistency condition.

Let's process left to right. Suppose we know r[0]. Then:
r[1] = r[0] XOR (t[1]=='B')
r[2] = r[1] XOR (t[2]=='B') = r[0] XOR (t[1]=='B') XOR (t[2]=='B')
...
r[j] = r[0] XOR XOR_{k=1..j} (t[k]=='B')

But we also have forced values: for any j where t[j]='B', r[j] = u[j].

So for each j with t[j]='B', we need:
r[0] XOR XOR_{k=1..j} (t[k]=='B') = u[j]

This gives a linear equation in r[0] (mod 2). If there are multiple such j, they must all be consistent. If inconsistent, 0 solutions.

If consistent, then r[0] is determined (0 or 1). Then all r[j] are determined. We also need to check that for j where t[j]='A', the determined r[j] is valid (it always is, since A allows both). But wait: we also need to ensure that the horizontal condition holds at the wrap-around: j = W-1 to j = 0.

The wrap-around condition: r[W-1] = left(0) where left(0) = r[0] if t[0]=='A' else 1-r[0].

But we already used the relation r[j] = r[j+1] XOR (t[j+1]=='B') for j=0..W-2. For j=W-1, we need:
r[W-1] = (t[0]=='A' ? r[0] : 1-r[0]) = r[0] XOR (t[0]=='B')

This is exactly the same formula! So the cycle condition is automatically satisfied if we define r[j] for all j using the recurrence from r[0]. But we must also satisfy the forced values from type B tiles.

So the algorithm for a row given u[0..W-1]:
1. Compute prefix XOR: P[j] = XOR_{k=1..j} (t[k]=='B') for j=1..W-1, P[0]=0.
   Then r[j] = r[0] XOR P[j].
2. For each j with t[j]='B': r[j] must equal u[j].
   So r[0] XOR P[j] = u[j], i.e., r[0] = u[j] XOR P[j].
   If there are multiple such j, all must give the same r[0]. If not, 0 solutions.
3. If consistent, r[0] is determined, so exactly 1 solution for this row (given u).

Wait, is that always 1 solution? Let's check: once r[0] is determined, all r[j] are determined. d[j] = u[j] is given. So the row has exactly 1 valid assignment given u, provided consistency.

But what about type A tiles? They have no restriction on r[j] (can be 0 or 1). However, the horizontal constraints force r[j] to specific values. So indeed, given u, the row has either 0 or 1 valid configuration.

Is that correct? Let's verify with a small example.

Example: W=3, t = A A A (all type A). Then P[j] = 0 for all j. No forced values. So r[0] can be 0 or 1? Wait, we said if there are no type B tiles, there are no equations forcing r[0]. So r[0] is free? But then r[j] = r[0] for all j, so 2 solutions.

Ah! I missed that. If there are no type B tiles in the row, then r[0] is not constrained by any forced value, so there are 2 choices. But wait, we also have the wrap-around condition. For all A, the condition is r[j] = r[j+1] for all j, which means all r[j] equal. So r[0] can be 0 or 1. So 2 solutions.

So the number of solutions is:
- 0 if inconsistent
- 2^(number of connected components of A-tiles in the cycle?) Actually, let's think.

The constraints are: for each j, r[j] = r[j+1] XOR b[j+1] where b[k] = 1 if t[k]='B' else 0.
This is a system of equations on a cycle. The number of free variables is the number of connected components when we consider the equations as edges.

Actually, the equations r[j] = r[j+1] XOR b[j+1] for j=0..W-1 (with j+1 mod W) form a cycle. The number of solutions is either 0 or 2, depending on consistency of the cycle. Specifically, the product of XORs around the cycle must be 0: XOR_{j=0..W-1} b[j+1] = 0? Let's check.

Going around: r[0] = r[1] XOR b[1]
r[1] = r[2] XOR b[2]
...
r[W-1] = r[0] XOR b[0]

Substituting: r[0] = (r[0] XOR b[0]) XOR b[1] XOR ... XOR b[W-1]
So r[0] = r[0] XOR (XOR_{j=0..W-1} b[j])
Thus XOR_{j=0..W-1} b[j] must be 0 for consistency.

If consistent, then r[0] is free, so 2 solutions.

But we also have forced values from type B tiles: for each j with t[j]='B', r[j] = u[j].
These are additional constraints that may fix r[0].

So the general solution:
- The horizontal cycle condition requires XOR of all b[j] = 0, where b[j] = 1 if t[j]='B' else 0.
- If this fails, 0 solutions regardless of u.
- If it holds, then the horizontal constraints alone give 2 solutions (r[0] free).
- Now apply forced values: for each j with t[j]='B', r[j] = u[j].
  Since r[j] = r[0] XOR P[j] (where P[j] = XOR_{k=1..j} b[k] for j≥1, P[0]=0), we need r[0] = u[j] XOR P[j] for all such j.
  If all give same r[0], then exactly 1 solution. If they give different r[0], 0 solutions.

Wait, but if there are no type B tiles, then b[j]=0 for all j, XOR=0, consistent. No forced values. So r[0] free, 2 solutions. That matches.

If there is exactly one type B tile at position j, then we have one equation fixing r[0]. So 1 solution.

If there are multiple type B tiles, they must all agree on r[0], else 0.

But is the horizontal cycle condition automatically satisfied if the forced values are consistent? Not necessarily. The forced values come from u, which is given. The horizontal cycle condition is independent of u. So we must check it first.

Actually, let's derive carefully.

We have variables r[0..W-1]. Constraints:
For each j=0..W-2: r[j] = r[j+1] XOR b[j+1]
For j=W-1: r[W-1] = r[0] XOR b[0]
For each j with t[j]='B': r[j] = u[j]

The first set of W constraints (the cycle) has either 0 or 2 solutions. The 2 solutions correspond to r[0]=0 or r[0]=1, with r[j] = r[0] XOR P[j] where P[j] = XOR_{k=1..j} b[k] for j≥1, P[0]=0. Note that P[W] = XOR_{k=1..W} b[k] = XOR_{k=0..W-1} b[k] (since b[0] is included in the wrap? Wait, careful.

Let's define P[j] for j=0..W-1 as the XOR from index 1 to j: P[0]=0, P[j] = b[1] XOR b[2] XOR ... XOR b[j] for j≥1.
Then r[j] = r[0] XOR P[j].

The wrap-around condition r[W-1] = r[0] XOR b[0] gives:
r[0] XOR P[W-1] = r[0] XOR b[0]
=> P[W-1] = b[0]
But P[W-1] = b[1] XOR ... XOR b[W-1].
So b[1] XOR ... XOR b[W-1] = b[0]
=> b[0] XOR b[1] XOR ... XOR b[W-1] = 0.

So the condition is XOR_{j=0..W-1} b[j] = 0.

If this holds, then for any r[0], the cycle constraints are satisfied. So we have 2 solutions parameterized by r[0].

Now the forced values: for each j with t[j]='B', we need r[0] XOR P[j] = u[j].
This gives r[0] = u[j] XOR P[j].

If there are no such j, r[0] is free: 2 solutions.
If there is at least one such j, r[0] is determined if all equations agree. If they agree, 1 solution. If disagree, 0 solutions.

So the number of solutions for a row given u is:
- 0 if XOR b[j] != 0
- else if no type B tiles: 2
- else if all type B tiles give same r[0]: 1
- else: 0

But wait, is that correct? Let's test with a simple case.

W=2, t = B B. b = [1,1]. XOR = 0, ok.
P[0]=0, P[1]=b[1]=1.
Forced: r[0] = u[0] XOR P[0] = u[0]
        r[1] = u[1] XOR P[1] = u[1] XOR 1
But also r[1] = r[0] XOR b[1] = r[0] XOR 1.
So r[0] = u[0], r[1] = u[0] XOR 1.
Forced from j=1: r[1] = u[1], so u[0] XOR 1 = u[1] => u[0] XOR u[1] = 1.
If u[0] XOR u[1] = 1, then 1 solution. Else 0.

Our formula: r[0] = u[0] from j=0, and r[0] = u[1] XOR 1 from j=1. These must agree: u[0] = u[1] XOR 1 => u[0] XOR u[1] = 1. So yes, 1 solution if consistent, 0 otherwise. Correct.

W=2, t = A B. b = [0,1]. XOR = 1, not 0. So 0 solutions always.
Check: r[0] = r[1] (since t[1]=A? Wait, t[1]=B, so b[1]=1. The constraint is r[0] = r[1] XOR 1.
And r[1] = r[0] XOR b[0] = r[0] XOR 0 = r[0].
So r[0] = r[0] XOR 1 => 0=1, impossible. Correct.

W=3, t = A A A. b = [0,0,0]. XOR=0. No forced values. So 2 solutions. Correct.

W=3, t = A B A. b = [0,1,0]. XOR=1. 0 solutions.
Check: r[0] = r[1] XOR 1, r[1] = r[2] XOR 0 = r[2], r[2] = r[0] XOR 0 = r[0].
So r[0] = r[0] XOR 1, impossible. Correct.

So the formula seems correct.

Now, we need to compute this for each row, and multiply across rows, with the u for the first row being the d of the last row (since torus).

But wait: the vertical condition is d[j] = u[j] where u[j] is the down bit of the previous row. For the first row, the previous row is the last row. So we have a cycle of rows.

We can do DP over rows: state is the u-vector (d-bits of previous row). But u has W bits, too large.

However, from the row analysis, given u, the number of solutions is either 0, 1, or 2, and if it's 1 or 2, the d-bits of this row (which become u for next row) are determined or have some freedom?

Let's see: d[j] = u[j] is forced by vertical condition. So the d-bits of this row are exactly the u-bits we were given! So the u-vector doesn't change? Wait, no.

The vertical condition is: d[i][j] = up(i,j) where up(i,j) is the down bit of row i-1.
So d[i][j] = d[i-1][j].
Thus d is constant across rows! Because d[i][j] = d[i-1][j] for all i, so d is the same for all rows.

Similarly, r[i][j] = right(i,j) = left(i,j+1) = ... but r can vary per row? Let's check horizontal: r[i][j] = left(i,j+1) = (t[i][j+1]=='A' ? r[i][j+1] : 1-r[i][j+1]). This is within the same row. So r can vary per row, but d is constant across rows.

Wait, is that right? The vertical condition says: the down bit of (i,j) equals the up bit of (i+1,j). The up bit of (i+1,j) is determined by the tile at (i+1,j): if type A, up = down; if type B, up = 1-down. So it's not simply d[i][j] = d[i+1][j].

Let's re-derive carefully.

For a cell (i,j):
- Type A: left = right, up = down.
- Type B: left = 1-right, up = 1-down.

Horizontal condition: right(i,j) = left(i,j+1).
So:
- If t[i][j+1]='A': right(i,j) = right(i,j+1)
- If t[i][j+1]='B': right(i,j) = 1 - right(i,j+1)

Vertical condition: down(i,j) = up(i+1,j).
So:
- If t[i+1][j]='A': down(i,j) = down(i+1,j)
- If t[i+1][j]='B': down(i,j) = 1 - down(i+1,j)

So d[i][j] is related to d[i+1][j] by the type of the cell below.

This means d is not constant; it changes according to the tile types in the column.

Similarly, r[i][j] is related to r[i][j+1] by the type of the cell to the right.

So we have two separate systems: one for r (horizontal) and one for d (vertical), but they are coupled because each cell has both r and d, and the tile type restricts the pair (r,d).

Specifically, for each cell (i,j):
- If t[i][j]='A': (r,d) can be (0,0), (0,1), (1,0), (1,1) — no restriction.
- If t[i][j]='B': (r,d) must be (0,0) or (1,1) — r = d.

So the coupling is: for type B cells, r = d.

Now, the horizontal system involves r only, with constraints r[i][j] = r[i][j+1] XOR b[i][j+1] where b[i][j] = 1 if t[i][j]='B' else 0.
The vertical system involves d only, with constraints d[i][j] = d[i+1][j] XOR c[i+1][j] where c[i][j] = 1 if t[i][j]='B' else 0? Let's check.

Vertical: down(i,j) = up(i+1,j).
up(i+1,j) = down(i+1,j) if t[i+1][j]='A', else 1-down(i+1,j).
So down(i,j) = down(i+1,j) XOR (t[i+1][j]=='B').

So d[i][j] = d[i+1][j] XOR b[i+1][j] where b[i][j] = 1 if t[i][j]='B' else 0.

So both r and d satisfy similar recurrence relations along their respective directions, with the same b values (based on tile type).

Now, the coupling: for each cell, if t[i][j]='B', then r[i][j] = d[i][j].

So we have two grids r and d, each satisfying linear constraints (XOR equations) on a torus, and for each B cell, r = d.

This is a system of linear equations over GF(2). We can solve it using union-find or Gaussian elimination, but H*W up to 10^6, so we need an efficient algorithm.

Since the constraints are local and structured, we can solve row by row or column by column.

Let's think about the r system alone. For each row i, the horizontal constraints form a cycle. As we derived, the number of solutions for r[i][0..W-1] is either 0 or 2, depending on XOR of b[i][j] over j. If 2, then r[i][j] = r[i][0] XOR P_i[j] for some prefix XOR P_i.

Similarly, for each column j, the vertical constraints on d form a cycle. The number of solutions for d[0..H-1][j] is either 0 or 2, depending on XOR of b[i][j] over i. If 2, then d[i][j] = d[0][j] XOR Q_j[i] for some prefix XOR Q_j.

Now, the coupling: for each B cell (i,j), we need r[i][j] = d[i][j].

This gives equations relating the free variables of the r and d systems.

Let's formalize.

For each row i:
- Let S_i = XOR_{j=0..W-1} b[i][j]. If S_i = 1, no solutions for r in this row. So overall 0.
- If S_i = 0, then r[i][j] = x_i XOR P_i[j], where x_i = r[i][0] is a free binary variable, and P_i[j] = XOR_{k=1..j} b[i][k] (with P_i[0]=0).

For each column j:
- Let T_j = XOR_{i=0..H-1} b[i][j]. If T_j = 1, no solutions for d in this column. So overall 0.
- If T_j = 0, then d[i][j] = y_j XOR Q_j[i], where y_j = d[0][j] is a free binary variable, and Q_j[i] = XOR_{k=1..i} b[k][j] (with Q_j[0]=0).

Now, for each cell (i,j):
- If t[i][j]='A': no constraint between r and d.
- If t[i][j]='B': we need r[i][j] = d[i][j], i.e., x_i XOR P_i[j] = y_j XOR Q_j[i].

So we have a bipartite graph of variables: x_i for each row i (H variables), y_j for each column j (W variables). The equations are: for each B cell (i,j), x_i XOR y_j = P_i[j] XOR Q_j[i].

This is a system of XOR equations on a bipartite graph. We can solve it using union-find (disjoint set union) with parity, or by Gaussian elimination. Since H+W can be up to 2*10^6, and number of equations is number of B cells (up to 10^6), we need an efficient method.

Union-find with parity works well: each variable is a node, each equation x_i XOR y_j = c is an edge between node i (in left set) and node j (in right set) with weight c. We can unify them.

But we have two types of variables: x_i (rows) and y_j (columns). We can map them to a single DSU: index 0..H-1 for x_i, index H..H+W-1 for y_j.

For each B cell (i,j), we add constraint: x_i XOR y_j = P_i[j] XOR Q_j[i].

We process all such constraints. If we find a contradiction, answer is 0. Otherwise, the number of solutions is 2^(number of connected components in the DSU).

Wait, is that correct? Let's verify.

The DSU with parity: each connected component has a value (0 or 1) for each node, consistent with the equations. The number of free choices is the number of connected components (each can be flipped). So if there are C components, there are 2^C solutions.

But we also need to ensure that the r and d systems are consistent individually, which we already checked with S_i and T_j.

So the algorithm:
1. For each row i, compute S_i = XOR of b[i][j]. If any S_i = 1, output 0.
2. For each column j, compute T_j = XOR of b[i][j]. If any T_j = 1, output 0.
3. Compute P_i[j] for all i,j: P_i[0]=0, P_i[j] = P_i[j-1] XOR b[i][j].
4. Compute Q_j[i] for all i,j: Q_j[0]=0, Q_j[i] = Q_j[i-1] XOR b[i][j].
5. Initialize DSU with H+W nodes.
6. For each cell (i,j) where t[i][j]='B':
   - Let c = P_i[j] XOR Q_j[i].
   - Union node i (for x_i) and node H+j (for y_j) with parity c.
   - If contradiction found, output 0.
7. Let C be the number of connected components in DSU.
8. Answer = 2^C mod 998244353.

But wait: is that all? We also need to consider that for type A cells, there is no constraint, but we already accounted for the 2 choices per row in the r system and per column in the d system? Actually, the 2 choices per row are captured by the free variable x_i. Similarly, the 2 choices per column are captured by y_j. But when we couple them with the B cell equations, the number of free components is exactly the number of connected components in the constraint graph.

Let's verify with a small example.

Example 1: H=3, W=3, grid:
AAB
AAB
BBB

So b[i][j] = 1 for B, 0 for A.
Row 0: A A B -> b = [0,0,1], S_0 = 1. So no solutions? But sample output is 2.

Wait, sample output for first test case is 2. So my calculation must be wrong.

Let's check the grid:
Row 0: A A B
Row 1: A A B
Row 2: B B B

b matrix:
Row 0: [0,0,1]
Row 1: [0,0,1]
Row 2: [1,1,1]

S_0 = 0 XOR 0 XOR 1 = 1. So according to my formula, row 0 has no solutions. But sample says 2 solutions exist.

So my derivation of the horizontal condition is wrong.

Let's re-examine the horizontal condition.

The condition is: for each cell (i,j), the right endpoint exists iff the left endpoint of (i,j+1) exists.

Right endpoint of (i,j) exists if the segment touches the right edge.
Left endpoint of (i,j+1) exists if the segment touches the left edge of (i,j+1).

For type A tile: segment connects two adjacent edges. So it touches two adjacent edges. The four rotations:
- touches top and bottom? No, adjacent edges. So: top-right, right-bottom, bottom-left, left-top.
So the endpoints are on two adjacent edges.

For type B tile: segment connects two opposite edges. So: top-bottom or left-right.

So for a tile, the set of edges it touches:
- Type A: exactly two adjacent edges. So it touches right edge in 2 out of 4 rotations: (top-right) and (right-bottom). Wait, top-right touches top and right. Right-bottom touches right and bottom. So yes, 2 rotations touch right.
- Type B: touches right edge in 1 out of 2 rotations: left-right.

So the probability or count is not simply determined by a single bit.

I made a mistake: I assumed that for type A, the right bit can be chosen independently of the down bit. But actually, for type A, the two edges are adjacent, so if it touches right, it must also touch either top or bottom. So the choices are:
- (right, top): touches right and top
- (right, bottom): touches right and bottom
- (left, top): touches left and top
- (left, bottom): touches left and bottom

So the pair (right, down) is not free; it's constrained: if right=1, then down can be 0 or 1? Wait:
- (right, top): right=1, down=0 (since top, not bottom)
- (right, bottom): right=1, down=1
- (left, top): right=0, down=0
- (left, bottom): right=0, down=1

So actually, for type A, (right, down) can be any of the four combinations! Because:
- (0,0): left-top
- (0,1): left-bottom
- (1,0): right-top
- (1,1): right-bottom

So my earlier statement that type A allows all 4 combinations of (right, down) is correct.

For type B:
- left-right: right=1, down=0? Wait, left-right touches left and right. So right=1, but does it touch top or bottom? No. So down=0 (not touching bottom). Similarly, top-bottom: right=0, down=1.
So type B allows (0,1) and (1,0)? Let's check.

Type B: connects two opposite edges.
- Horizontal: left and right. So touches left and right, not top or bottom. So right=1, down=0.
- Vertical: top and bottom. So touches top and bottom, not left or right. So right=0, down=1.

So type B allows (right, down) = (1,0) or (0,1). Not (0,0) or (1,1).

I had it backwards! Type B allows (1,0) and (0,1), which means right XOR down = 1.

Type A allows all four: (0,0), (0,1), (1,0), (1,1).

So the allowed pairs:
- A: any (r,d)
- B: r XOR d = 1

Now, the horizontal condition: right(i,j) = left(i,j+1).
Left(i,j+1) is determined by the tile at (i,j+1):
- If type A: left = right (since adjacent, if it touches left, it touches either top or bottom, but left bit is independent? Wait, for type A, the left bit is 1 if the tile touches left edge. From the four rotations:
  - left-top: left=1
  - left-bottom: left=1
  - right-top: left=0
  - right-bottom: left=0
So left = 1 in 2 cases, 0 in 2 cases. And it's independent of down? In left-top, down=0; in left-bottom, down=1. So left and down are independent for type A.
- If type B: left = 1 if horizontal (left-right), else 0. For horizontal, right=1, down=0. So left=1, right=1, down=0. For vertical, left=0, right=0, down=1.

So:
- Type A: left = right (since the segment connects adjacent edges, if it touches left, it doesn't touch right; if it touches right, it doesn't touch left). Wait, is that true?
  - left-top: touches left and top, not right.
  - right-top: touches right and top, not left.
  So yes, for type A, left and right are mutually exclusive: exactly one of left, right is 1.
  Similarly, top and bottom are mutually exclusive: exactly one of top, bottom is 1.
- Type B: 
  - horizontal: touches left and right, so left=1, right=1. Not top/bottom.
  - vertical: touches top and bottom, so top=1, bottom=1. Not left/right.

So:
- Type A: left XOR right = 1, top XOR bottom = 1.
- Type B: left = right, top = bottom.

Now, the horizontal condition: right(i,j) = left(i,j+1).

Let's define r[i][j] = right(i,j), l[i][j] = left(i,j).
Then:
- For type A: l[i][j] = 1 - r[i][j] (since exactly one of left,right is 1)
- For type B: l[i][j] = r[i][j]

So l[i][j] = r[i][j] XOR (t[i][j]=='A' ? 1 : 0).

Similarly, for vertical: d[i][j] = down(i,j), u[i][j] = up(i,j).
- Type A: u[i][j] = 1 - d[i][j]
- Type B: u[i][j] = d[i][j]

So u[i][j] = d[i][j] XOR (t[i][j]=='A' ? 1 : 0).

Now the conditions:
Horizontal: r[i][j] = l[i][j+1] = r[i][j+1] XOR (t[i][j+1]=='A' ? 1 : 0)
So r[i][j] = r[i][j+1] XOR a[i][j+1], where a[i][j] = 1 if t[i][j]='A' else 0.

Vertical: d[i][j] = u[i+1][j] = d[i+1][j] XOR (t[i+1][j]=='A' ? 1 : 0)
So d[i][j] = d[i+1][j] XOR a[i+1][j].

Now the tile constraints:
- Type A: any (r,d) allowed.
- Type B: r = d? Let's check.
  Type B: horizontal: r=1, d=0. Vertical: r=0, d=1. So r XOR d = 1.
  So for type B: r XOR d = 1.

So:
- If t[i][j]='A': no constraint between r and d.
- If t[i][j]='B': r[i][j] XOR d[i][j] = 1.

Now this is different from before.

Let's re-derive the row condition.

For a fixed row i, we have variables r[i][0..W-1] and d[i][0..W-1].
Constraints:
1. For each j: r[i][j] = r[i][j+1] XOR a[i][j+1] (with j+1 mod W).
2. For each j: d[i][j] = d[i+1][j] XOR a[i+1][j] (vertical, involves next row).
3. For each j: if t[i][j]='B', then r[i][j] XOR d[i][j] = 1.

The horizontal constraint on r alone: r[i][j] = r[i][j+1] XOR a[i][j+1].
This is a cycle. The condition for consistency is XOR_{j=0..W-1} a[i][j+1] = 0, i.e., XOR_{j=0..W-1} a[i][j] = 0.
Since a[i][j] = 1 for A, 0 for B.
So the number of A's in the row must be even? Wait, XOR of a[i][j] over j must be 0.
a[i][j] = 1 if A, 0 if B.
So XOR = (number of A's mod 2).
So the row must have an even number of A tiles.

In the sample: row 0: A A B -> two A's, even. Row 1: A A B -> two A's, even. Row 2: B B B -> zero A's, even.
So all rows have even number of A's. Good.

If consistent, then r[i][j] = x_i XOR P_i[j], where x_i = r[i][0], and P_i[j] = XOR_{k=1..j} a[i][k] (with P_i[0]=0).

Similarly, for columns: d[i][j] = y_j XOR Q_j[i], where y_j = d[0][j], and Q_j[i] = XOR_{k=1..i} a[k][j] (with Q_j[0]=0).
Consistency requires XOR_{i=0..H-1} a[i][j] = 0, i.e., even number of A's in each column.

Now the coupling: for each B cell (i,j), we need r[i][j] XOR d[i][j] = 1.
So (x_i XOR P_i[j]) XOR (y_j XOR Q_j[i]) = 1.
=> x_i XOR y_j = 1 XOR P_i[j] XOR Q_j[i].

So we have equations on x_i and y_j.

This is similar to before, but with different constants.

Let's test with the sample.

Sample 1:
H=3, W=3
Row 0: A A B -> a = [1,1,0]
Row 1: A A B -> a = [1,1,0]
Row 2: B B B -> a = [0,0,0]

Check row consistency:
Row 0: XOR a = 1 XOR 1 XOR 0 = 0. OK.
Row 1: same, OK.
Row 2: 0, OK.

Column consistency:
Col 0: a[0][0]=1, a[1][0]=1, a[2][0]=0. XOR = 0. OK.
Col 1: a[0][1]=1, a[1][1]=1, a[2][1]=0. XOR = 0. OK.
Col 2: a[0][2]=0, a[1][2]=0, a[2][2]=0. XOR = 0. OK.

Now compute P_i[j]:
P_0[0]=0
P_0[1] = a[0][1] = 1
P_0[2] = a[0][1] XOR a[0][2] = 1 XOR 0 = 1

P_1[0]=0
P_1[1] = a[1][1] = 1
P_1[2] = 1 XOR 0 = 1

P_2[0]=0
P_2[1] = a[2][1] = 0
P_2[2] = 0 XOR 0 = 0

Q_j[i]:
Q_0[0]=0
Q_0[1] = a[1][0] = 1
Q_0[2] = a[1][0] XOR a[2][0] = 1 XOR 0 = 1

Q_1[0]=0
Q_1[1] = a[1][1] = 1
Q_1[2] = 1 XOR 0 = 1

Q_2[0]=0
Q_2[1] = a[1][2] = 0
Q_2[2] = 0 XOR 0 = 0

Now B cells: (0,2), (1,2), (2,0), (2,1), (2,2).

For each, compute c = 1 XOR P_i[j] XOR Q_j[i].

(0,2): i=0,j=2. P_0[2]=1, Q_2[0]=0. c = 1 XOR 1 XOR 0 = 0.
Equation: x_0 XOR y_2 = 0.

(1,2): i=1,j=2. P_1[2]=1, Q_2[1]=0. c = 1 XOR 1 XOR 0 = 0.
Equation: x_1 XOR y_2 = 0.

(2,0): i=2,j=0. P_2[0]=0, Q_0[2]=1. c = 1 XOR 0 XOR 1 = 0.
Equation: x_2 XOR y_0 = 0.

(2,1): i=2,j=1. P_2[1]=0, Q_1[2]=1. c = 1 XOR 0 XOR 1 = 0.
Equation: x_2 XOR y_1 = 0.

(2,2): i=2,j=2. P_2[2]=0, Q_2[2]=0. c = 1 XOR 0 XOR 0 = 1.
Equation: x_2 XOR y_2 = 1.

Now we have variables x_0, x_1, x_2, y_0, y_1, y_2.
Equations:
x_0 = y_2
x_1 = y_2
x_2 = y_0
x_2 = y_1
x_2 XOR y_2 = 1

From x_0 = y_2 and x_1 = y_2, so x_0 = x_1.
From x_2 = y_0 and x_2 = y_1, so y_0 = y_1.
From x_2 XOR y_2 = 1.

Also, are there any other constraints? No.

So we have connected components:
Component 1: {x_0, x_1, y_2} with x_0 = y_2, x_1 = y_2. So all equal.
Component 2: {x_2, y_0, y_1} with x_2 = y_0 = y_1.
And equation between components: x_2 XOR y_2 = 1.

So there are 2 connected components. Thus 2^2 = 4 solutions? But sample output is 2.

Wait, sample output is 2. So maybe I have an extra factor.

Let's check: the number of solutions should be 2. So perhaps the number of free components is 1, not 2.

But we have two components linked by one equation. So the number of free components is 2 (each component can be flipped independently, but the equation fixes the relative value). Actually, with two components and one equation between them, the number of free choices is 1 (choose one component's value, the other is determined). So 2^1 = 2. Yes! So number of solutions is 2^(number of components - number of equations between components)? No, in DSU with parity, the number of solutions is 2^(number of connected components). Because each component can be assigned 0 or 1 freely, and the equations within the component are satisfied automatically. The equations between components are the edges that connect them; if we have C components, there are 2^C solutions.

But here we have two components? Let's see: the DSU has nodes for x_0,x_1,x_2,y_0,y_1,y_2.
Edges:
x_0 - y_2 (c=0)
x_1 - y_2 (c=0)
x_2 - y_0 (c=0)
x_2 - y_1 (c=0)
x_2 - y_2 (c=1)

So y_2 is connected to x_0 and x_1. x_2 is connected to y_0, y_1, and y_2.
So all nodes are in one connected component! Because x_2 is connected to y_2, and y_2 is connected to x_0,x_1.
So there is only 1 connected component.
Thus 2^1 = 2 solutions. Correct!

So the DSU approach works: number of solutions is 2^(number of connected components in the DSU).

But we need to be careful: the DSU includes both x and y variables. The number of components is the number of sets in DSU.

So algorithm:
1. Check that each row has even number of A's (XOR of a[i][j] = 0). If not, output 0.
2. Check that each column has even number of A's. If not, output 0.
3. Compute P_i[j] for all i,j.
4. Compute Q_j[i] for all i,j.
5. Initialize DSU with H+W nodes.
6. For each cell (i,j) where t[i][j]='B':
   - c = 1 XOR P_i[j] XOR Q_j[i]
   - Union i and H+j with parity c.
   - If contradiction, output 0.
7. Let C be the number of components in DSU.
8. Output 2^C mod 998244353.

This should work.

Let's verify with sample 2:
3 3
BBA
ABA
AAB

Grid:
Row 0: B B A -> a = [0,0,1]
Row 1: A B A -> a = [1,0,1]
Row 2: A A B -> a = [1,1,0]

Row 0: XOR a = 1. Odd. So output 0. Sample output is 0. Correct.

Sample 3:
3 4
BAAB
BABA
BBAA

Row 0: B A A B -> a = [0,1,1,0], XOR = 0. OK.
Row 1: B A B A -> a = [0,1,0,1], XOR = 0. OK.
Row 2: B B A A -> a = [0,0,1,1], XOR = 0. OK.

Columns:
Col 0: B,B,B -> a = [0,0,0], XOR=0.
Col 1: A,A,B -> a = [1,1,0], XOR=0.
Col 2: A,B,A -> a = [1,0,1], XOR=0.
Col 3: B,A,A -> a = [0,1,1], XOR=0.

All OK.

Now compute P and Q.
P_0: [0, a[0][1]=1, 1 XOR a[0][2]=1 XOR 1=0, 0 XOR a[0][3]=0 XOR 0=0] -> [0,1,0,0]
P_1: [0, a[1][1]=1, 1 XOR a[1][2]=1 XOR 0=1, 1 XOR a[1][3]=1 XOR 1=0] -> [0,1,1,0]
P_2: [0, a[2][1]=0, 0 XOR a[2][2]=0 XOR 1=1, 1 XOR a[2][3]=1 XOR 1=0] -> [0,0,1,0]

Q_0: [0, a[1][0]=0, 0 XOR a[2][0]=0 XOR 0=0] -> [0,0,0]
Q_1: [0, a[1][1]=1, 1 XOR a[2][1]=1 XOR 0=1] -> [0,1,1]
Q_2: [0, a[1][2]=0, 0 XOR a[2][2]=0 XOR 1=1] -> [0,0,1]
Q_3: [0, a[1][3]=1, 1 XOR a[2][3]=1 XOR 1=0] -> [0,1,0]

B cells: positions where t='B'.
Row 0: B at j=0,3.
Row 1: B at j=0,2.
Row 2: B at j=0,1.

So B cells: (0,0), (0,3), (1,0), (1,2), (2,0), (2,1).

Compute c for each:
(0,0): i=0,j=0. P_0[0]=0, Q_0[0]=0. c = 1 XOR 0 XOR 0 = 1.
(0,3): i=0,j=3. P_0[3]=0, Q_3[0]=0. c = 1 XOR 0 XOR 0 = 1.
(1,0): i=1,j=0. P_1[0]=0, Q_0[1]=0. c = 1 XOR 0 XOR 0 = 1.
(1,2): i=1,j=2. P_1[2]=1, Q_2[1]=0. c = 1 XOR 1 XOR 0 = 0.
(2,0): i=2,j=0. P_2[0]=0, Q_0[2]=0. c = 1 XOR 0 XOR 0 = 1.
(2,1): i=2,j=1. P_2[1]=0, Q_1[2]=1. c = 1 XOR 0 XOR 1 = 0.

Equations:
x_0 XOR y_0 = 1
x_0 XOR y_3 = 1
x_1 XOR y_0 = 1
x_1 XOR y_2 = 0
x_2 XOR y_0 = 1
x_2 XOR y_1 = 0

From x_0 XOR y_0 = 1 and x_1 XOR y_0 = 1, we get x_0 = x_1.
From x_2 XOR y_0 = 1, we get x_2 = x_0 XOR 1.
So x_0 = x_1, x_2 = NOT x_0.

Now x_0 XOR y_3 = 1 => y_3 = x_0 XOR 1 = x_2.
x_1 XOR y_2 = 0 => y_2 = x_1 = x_0.
x_2 XOR y_1 = 0 => y_1 = x_2 = x_0 XOR 1.

So all variables determined by x_0. So 2 solutions. Sample output is 2. Correct!

So the algorithm works.

Implementation details:
- We need to compute P_i[j] for all i,j. We can compute row by row.
- Similarly Q_j[i] column by column.
- DSU with parity: standard implementation.
- Number of components: we can count after all unions, or maintain a counter that increments when a new set is created and decrements when two sets are merged.

Complexities: O(H*W) time and space. H*W up to 10^6, so fine.

Edge cases: H=2, W=2, etc.

Let's write the code.

We'll parse T test cases. For each:
- Read H, W.
- Read grid as list of strings.
- Create a matrix a[i][j] = 1 if S[i][j]=='A' else 0.
- Check row parity: for each i, compute XOR of a[i][j]. If any !=0, print 0 and continue.
- Check column parity: for each j, compute XOR of a[i][j]. If any !=0, print 0 and continue.
- Compute P: P[i][0]=0, P[i][j] = P[i][j-1] XOR a[i][j] for j=1..W-1.
- Compute Q: Q[j][0]=0, Q[j][i] = Q[j][i-1] XOR a[i][j] for i=1..H-1.
- Initialize DSU with H+W elements.
- For each cell (i,j) where S[i][j]=='B':
  - c = 1 XOR P[i][j] XOR Q[j][i]
  - union(i, H+j, c)
- After processing, if any contradiction, print 0.
- Else, count number of components C.
- Answer = pow(2, C, MOD).
- Print answer.

We need to be careful with indices: P[i][j] corresponds to row i, column j. Q[j][i] corresponds to column j, row i.

Memory: storing a, P, Q as 2D arrays of size H*W. Since total cells across test cases is 10^6, we can allocate per test case.

DSU implementation:
- parent array of size H+W.
- rank or size.
- parity array: parity[x] = XOR of values from x to root.

Standard DSU with parity:
def find(x):
    if parent[x] == x: return x, 0
    else:
        root, par = find(parent[x])
        parity[x] ^= par
        parent[x] = root
        return parent[x], parity[x]

def union(x, y, c):
    rx, px = find(x)
    ry, py = find(y)
    if rx == ry:
        if (px ^ py) != c: contradiction
    else:
        # merge rx into ry
        parent[rx] = ry
        parity[rx] = px ^ py ^ c

Number of components: initially H+W. Each successful union reduces count by 1.

We need to handle up to 10^5 test cases, but total cells 10^6, so average small. DSU operations are nearly O(1).

Let's code it.

One more check: the problem says "modulo 998244353". So we use that.

Also, note that the number of components can be up to H+W, which could be large, but pow(2, C, MOD) is fine.

We should ensure that we don't use recursion for find to avoid stack overflow; use iterative path compression.

Let's write the code.

```python
import sys

MOD = 998244353

def solve():
    input = sys.stdin.readline
    T = int(input())
    for _ in range(T):
        H, W = map(int, input().split())
        S = [input().strip() for _ in range(H)]
        
        # a[i][j] = 1 if A else 0
        a = [[1 if c == 'A' else 0 for c in row] for row in S]
        
        # Check row parity
        ok = True
        for i in range(H):
            xor = 0
            for j in range(W):
                xor ^= a[i][j]
            if xor != 0:
                ok = False
                break
        if not ok:
            print(0)
            continue
        
        # Check column parity
        for j in range(W):
            xor = 0
            for i in range(H):
                xor ^= a[i][j]
            if xor != 0:
                ok = False
                break
        if not ok:
            print(0)
            continue
        
        # Compute P[i][j]
        P = [[0]*W for _ in range(H)]
        for i in range(H):
            for j in range(1, W):
                P[i][j] = P[i][j-1] ^ a[i][j]
        
        # Compute Q[j][i]
        Q = [[0]*H for _ in range(W)]
        for j in range(W):
            for i in range(1, H):
                Q[j][i] = Q[j][i-1] ^ a[i][j]