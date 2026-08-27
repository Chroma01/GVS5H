We need to count the number of monotone (right/up) lattice paths within the rectangle [0,W]×[0,H] but outside the forbidden rectangle [L,R]×[D,U] (which is empty of blocks). Since movement is only right/up and the forbidden region is an axis-aligned rectangle, the total number of possible paths (any start, any end, any number of steps) equals the number of directed lattice paths in the complement region.

Key insight: the complement of a rectangle in a grid is a "frame" — left of the rectangle, right of the rectangle, below the rectangle, and above the rectangle. A monotone path that stays in the complement must either:
1. Stay entirely in one of the four "arms" (left, right, below, above) — these are simple rectangular regions.
2. Cross from one arm to another — but the only way to cross is to go around the rectangle. Since movement is only right/up, to go from left arm to right arm you must pass below or above the rectangle, and similarly for other transitions.

We can compute the total using the principle of inclusion-exclusion or by considering the four regions and transitions. Actually, a cleaner approach: use the transfer matrix / grid DP idea but compressed because the forbidden rectangle is contiguous.

Since the region is the union of 4 rectangles that share corners with the forbidden rectangle, and monotone paths can only enter/exit these regions at specific points, we can compute the total count via a formula.

Let me think more carefully. The blocks form a "frame":
- Region A: x ≤ L, 0 ≤ y ≤ H (left strip, width L+1, but excluding the part of the forbidden rect — but forbidden rect has x in [L,R], so for x ≤ L, we are always outside if x<L; at x=L, we need y<D or y>U. So actually region A is not a full rectangle.

Let me redefine. The allowed points are those in [0,W]×[0,H] \ [L,R]×[D,U].

This is a region with a rectangular hole. Monotone paths from any start to any end in this region.

The standard trick: use generating functions / formal power series. Let f(x,y) be the generating function. Actually, the number of monotone paths in a region with a hole can be computed using the Lindström-Gessel-Viennot lemma or direct summation.

Actually, here's a direct approach. The total number of paths in the region equals:
(sum over all paths in full rectangle) - (paths that enter the forbidden region).

A path enters the forbidden region iff it visits a point in [L,R]×[D,U]. 

Alternatively, we can use the fact that the number of monotone paths from point a to point b in the full grid is C((bx-ax)+(by-ay), bx-ax). So we can write the total as a sum of C values.

A cleaner way: think of the region as a grid graph. The number of paths is:
sum over all valid (start, end) pairs of (number of paths from start to end in the complement).

We can use the transfer matrix method. The grid has W+1 columns and H+1 rows. The forbidden region is a rectangle. We can compute the number of paths by dynamic programming on the grid, but skipping the forbidden region. Since W,H ≤ 10^6, we need an O(W+H) or O((W+H) log) solution.

A DP by columns: for each column, the number of paths ending at each row. When we process column by column, moving from column x to x+1, we sum over valid y in column x+1. This is O(W*H) naively.

But we can use the fact that the forbidden region is a rectangle, so the DP transitions are simple. In fact, for monotone paths, the number of paths to (x,y) is just C(x+y, x) (binomial coefficient) in the full grid. In the complement, we subtract paths that go through the hole.

A path from s to t in the complement equals (paths from s to t in full grid) - (paths from s to t that touch the hole). But "touch the hole" is complex.

Alternative: Decompose the region. The complement is connected (assuming the hole doesn't touch the boundary in a way that disconnects it, but the constraints allow that). Actually, the complement of a rectangle in a rectangle might be disconnected if the hole touches the boundary. But the problem says there's at least one block, so we don't have full coverage.

Actually, the complement of a rectangle [L,R]×[D,U] in [0,W]×[0,H] is connected as long as the hole is strictly inside or touches at most one side? No, if the hole touches two adjacent sides, the complement is disconnected. For example, if L=0 and D=0, the hole is in the corner, and the complement is three disconnected pieces? Let's see: with hole at corner, the complement consists of points with x>R or y>U, which is connected (you can go from any point to any other by going far right or far up). So it's connected.

Actually, the complement of an axis-aligned rectangle in an axis-aligned rectangle is always connected (as a subset of the integer grid) as long as the hole doesn't span the full width or height. Even if the hole touches one side, say L=0, the complement is points with x>R (which is connected and extends to x=W) and points with 0≤x≤W but y outside [D,U] with x in [0,R]. The set x>R is connected to the top/bottom via going up/down at x>R. So yes, it's connected.

OK, back to counting. The number of paths in a grid region (vertices are lattice points, edges go right/up) is what we want. The graph is a DAG. The number of paths equals sum over all s of (number of paths starting at s). We can compute this via DP on the grid.

Standard DP: Let P[x][y] = number of paths from (0,0) to (x,y) staying in allowed region. Then P[x][y] = 0 if forbidden, else P[x-1][y] + P[x][y-1]. This is O(WH).

But we need a formula. Since the forbidden region is a rectangle, we can use the formula for grid with a rectangular hole.

The number of monotone paths from (0,0) to (W,H) avoiding a rectangular hole is given by the Lindström-Gessel-Viennot (LGV) determinant or by inclusion-exclusion.

Actually, for paths avoiding a rectangular obstacle, there's a known formula:
C(W+H, W) - sum over boundary crossings.

But we want the total number of paths (any start, any end), not just from (0,0) to (W,H).

Let me reconsider. We want sum_{s,t in allowed} paths(s,t).

This equals sum_{s} (number of paths starting at s and staying in allowed region).
By symmetry, this equals sum_{t} (number of paths ending at t).
It's also equal to sum over all paths of 1.

We can compute it as: the total number of directed paths in the DAG. This equals the permanent of the adjacency matrix, but that's hard.

Alternative: Let Q[x][y] = number of paths from (0,0) to (x,y) in allowed region.
Let R[x][y] = number of paths from (x,y) to (W,H) in allowed region.
Then total = sum_{x,y} Q[x][y] * R[x][y] / (number of paths through (x,y) counted properly? No, each path is counted once at its endpoint, so total paths = sum_{t} (paths from some s to t) = sum_{t} (sum_s paths(s,t)) = sum_t (number of paths ending at t). And number of paths ending at t = R[t] where R is computed from (W,H) backwards. So total = sum_{x,y} R[x][y] where R[x][y] is number of paths from (x,y) to (W,H) in allowed region.

Similarly, total = sum_{x,y} Q[x][y].

So we need to compute sum_{x,y} Q[x][y] or sum_{x,y} R[x][y].

Compute Q[x][y] for the allowed region. Q satisfies:
Q[0][0] = 1.
Q[x][y] = 0 if (x,y) is forbidden.
Q[x][y] = Q[x-1][y] + Q[x][y-1] otherwise, for x,y ≥ 0, with Q[-1][*] = Q[*][-1] = 0.

Then sum = sum_{x=0..W, y=0..H} Q[x][y].

We need to compute this sum efficiently.

The allowed region is the full rectangle minus the forbidden rectangle. So Q_allowed = Q_full - Q_through_forbidden, but Q_through_forbidden is not simply defined because Q_allowed is 0 at forbidden points.

Actually, Q_allowed[x][y] = number of paths from (0,0) to (x,y) that don't visit any forbidden point.

This is a classic problem. The number of paths avoiding a rectangular obstacle can be computed using the reflection principle or by decomposition.

We can write:
Q_allowed[x][y] = C(x+y, x) - sum_{(a,b) in forbidden} (paths that first hit (a,b) then go to (x,y)).
But this is complex.

A better way: use the transfer matrix approach but exploit the structure. The grid has W+1 columns. The state is the set of active rows (y-coordinates). But with H up to 10^6, state per column is too large.

However, the forbidden region is a rectangle. Let's think about the DP by columns.

For a fixed x, let f_x(y) = Q[x][y]. Then f_{x+1}(y) = f_x(y) + f_{x+1}(y-1).
This is convolution-like.

Actually, f_{x+1}(y) = sum_{k=0}^y f_x(k) for y < D (below hole) and y > U (above hole), and we skip y in [D,U].

Wait, f_{x+1}(y) = f_x(y) + f_{x+1}(y-1). This gives f_{x+1}(y) = sum_{k=0}^y f_x(k) if there are no holes. With holes, we need to subtract the forbidden y's.

For the full grid, f_x(y) = C(x+y, x).

For the grid with a rectangular hole, the DP is:
Q[x][y] = 0 if L≤x≤R and D≤y≤U.
Otherwise, Q[x][y] = Q[x-1][y] + Q[x][y-1].

We want S = sum_{x=0}^W sum_{y=0}^H Q[x][y].

Since the DP is linear, we can compute S by summing as we go. But still O(WH).

We need a formula. Let's think of generating functions.

Let F(x,y) = sum_{x,y} Q[x][y] x^y or something. The DP is a partial difference equation.

Standard trick: For a grid with a rectangular hole, the number of paths from (0,0) to (W,H) avoiding [L,R]×[D,U] is:
C(W+H, W) - C(L+D, L) * C((W-L)+(H-D), W-L) - ... (inclusion-exclusion over the four corners).

Actually, the formula for paths avoiding a rectangle is:
N = C(W+H, W) - C(L+D, L)*C((W-L)+(H-D), W-L) - C((R+1)+(U+1), R+1)*C((W-R-1)+(H-U-1), W-R-1) + C(L+(U+1), L)*C((W-L)+(H-U-1), W-L) + C((R+1)+D, R+1)*C((W-R-1)+(H-D), W-R-1) - C(L+D, L)*C((R-L)+(U-D), R-L)*C((W-R)+(H-U), W-R) ... no, this is getting complicated.

Wait, the standard formula for paths from (0,0) to (W,H) avoiding [L,R]×[D,U] (with L≤R, D≤U) uses the reflection principle at the corners. It is:
Total = C(W+H, W)
Minus: paths that enter the rectangle from the left/below.
Using the LGV lemma or determinant, the number is:
det [ C(a_i - b_j) ... ] but for a single rectangle it's simpler.

Actually, for a single rectangular obstacle, the number of paths from s to t avoiding the rectangle can be computed as:
C(t-s) - C(...) + C(...) - ... via inclusion-exclusion on the four ways to go around.

The four "detour" paths:
1. Go left of rectangle: requires going around the left side. Path: s -> (L, y1) -> (L, y2) -> t, where y1 ≤ D, y2 ≥ U (or something). Actually, to avoid [L,R]×[D,U], a path must pass either left of x=L (at x=L) with y<D or y>U, or right of x=R with y<D or y>U, etc.

The inclusion-exclusion formula for avoiding a rectangle is known. Let me recall it.

The number of monotone paths from (0,0) to (W,H) that do not enter (L,R]×(D,U] (assuming the hole is open on the right/top? Actually the hole is closed [L,R]×[D,U]).

Using the method of images (reflection principle for a rectangle), we subtract paths that cross the boundaries. There are four boundaries: left, right, bottom, top of the rectangle. A path enters the rectangle iff it crosses the left boundary x=L at some y in [D,U], or the bottom boundary y=D at some x in [L,R], etc.

This is equivalent to: paths that go from s to t without entering the rectangle = total paths - paths that go through the rectangle.

A path goes through the rectangle iff it has a point in [L,R]×[D,U]. This is equivalent to: the path enters through the left/bottom and exits through the right/top.

The standard result: number of paths from (a,b) to (c,d) avoiding [L,R]×[D,U] is:
sum_{k=0}^1 (-1)^k [ C((c-a)+(d-b), c-a) with some transformation ]

Actually, the formula uses the four corners of the rectangle. Let me denote the rectangle corners: BL=(L,D), BR=(R,D), TL=(L,U), TR=(R,U).

The valid paths are those that go either:
- entirely in x<L, or
- entirely in x>R, or
- entirely in y<D, or
- entirely in y>U, or
- pass from x<L region to x>R region via y<D, or
- pass from x<L region to x>R region via y>U, or
- pass from y<D region to y>U region via x<L, or
- pass from y<D region to y>U region via x>R.

Actually, any path in the complement must be in one of four "quadrants" relative to the rectangle, but can move between quadrants only at the "gates" (the four extensions of the rectangle edges to the boundary).

Specifically, the complement is divided into:
- Left of L: x ≤ L, but y ∉ [D,U] when x=L? Actually, for x < L, all y are allowed. For x = L, y < D or y > U. So the left region is connected and includes the left boundary and below/above the rectangle at x=L.
- Right of R: x ≥ R, y ∉ [D,U] at x=R.
- Below D: y ≤ D, x ∉ [L,R] at y=D.
- Above U: y ≥ U, x ∉ [L,R] at y=U.

These four regions are connected to each other through the "corridors": the region below D (for x in [L,R]) connects the left and right regions. The region above U connects left and right. The region left of L (for y in [D,U]) connects below and above. The region right of R connects below and above.

So the state of a path can be described by which of the four "arms" it's in. But as it moves, it can transition between arms.

Actually, since movement is only right/up, the path's x and y are non-decreasing. The path starts at some (x0,y0) and ends at (x1,y1) with x0≤x1, y0≤y1.

The path can be decomposed into segments that lie in the four regions:
- Initially at (x0,y0). If x0 < L, we're in the left arm (including below and above parts, but since we can only move right/up, we might enter the below part, then the right arm, etc.

Let me define the four "zones":
Zone A: x < L (left arm)
Zone B: x > R (right arm)
Zone C: y < D (bottom arm) - note that for x in [L,R], y<D is separate from A and B but connects them.
Zone D: y > U (top arm)

But zones overlap at the corners. The complement is the union of:
- A: {(x,y): x ≤ L, y < D} ∪ {(x,y): x ≤ L, y > U} ∪ {(x,y): x < L, D ≤ y ≤ U}
- B: {(x,y): x ≥ R, y < D} ∪ {(x,y): x ≥ R, y > U} ∪ {(x,y): x > R, D ≤ y ≤ U}
- C: {(x,y): L ≤ x ≤ R, y ≤ D}
- D: {(x,y): L ≤ x ≤ R, y ≥ U}

Note that A and C share the segment x=L, y<D. A and D share x=L, y>U. B and C share x=R, y<D. B and D share x=R, y>U.

Since movement is right/up, a path can go:
- From A to C: at x=L, y<D. So it moves right from (L,y) with y<D to enter C? Wait, from A (x<L) to C (y<D, x in [L,R]), it must cross x=L at y<D. So it can go from (L-1, y) to (L, y) to (L+1, y) etc, staying in C. Actually, to go from A to B, it must go through C or D.
- Specifically, to go from x<L to x>R, the path must either have y<D and x in [L,R] at some point (i.e., go through C), or y>U and go through D.
- To go from y<D to y>U (with x in [L,R]), the path must go through x<L (zone A) or x>R (zone B) at the appropriate y.

So the path's "state" in terms of which arm it's in can change only at specific boundaries.

We can model the path as moving through a graph with 4 nodes (A, B, C, D) and edges between them, where the edges correspond to traversing the corridors.

The number of paths can be computed by considering that the path makes a sequence of moves in the "free" parts and transitions at the gates.

Specifically, the path goes from start to end. The start is in one of the four zones (or on the boundary). As it moves, it can transition between zones.

The four zones are:
- Left arm: L-zone = { (x,y) : x ≤ L, (y < D or y > U) } ∪ { (x,y) : x < L, D ≤ y ≤ U }
- Right arm: R-zone = { (x,y) : x ≥ R, (y < D or y > U) } ∪ { (x,y) : x > R, D ≤ y ≤ U }
- Bottom corridor: B-zone = { (x,y) : L ≤ x ≤ R, y ≤ D }
- Top corridor: T-zone = { (x,y) : L ≤ x ≤ R, y ≥ U }

Note that at x=L, the L-zone and B-zone meet (y<D), and L-zone and T-zone meet (y>U).
At x=R, R-zone and B-zone meet (y<D), R-zone and T-zone meet (y>U).

A monotone path in this region: it starts somewhere, ends somewhere, and moves right/up. It can move within a zone, or cross between zones at the meeting points.

Transitions possible (right/up only):
- L-zone to B-zone: at x=L, y<D. The path must be at (L, y) with y<D, then move right to (L+1, y) in B-zone.
- L-zone to T-zone: at x=L, y>U.
- B-zone to R-zone: at x=R, y<D.
- T-zone to R-zone: at x=R, y>U.
- B-zone to L-zone? To go from B-zone to L-zone, we'd need to decrease x, which is not allowed. So once we enter B-zone from L-zone (by moving right at x=L), we cannot go back to L-zone. We can only go to R-zone (by moving right to x>R) or stay in B-zone until y=D, but y can only increase, so if we're in B-zone (y≤D), we can increase y up to D, but we cannot decrease y. We can also move right within B-zone.
Wait, in B-zone, y can be any value ≤ D. But D is a constant. Since y can increase, we might hit y=D. At y=D, we are on the boundary. The next step up would be to y=D+1, but that point (x, D+1) with x in [L,R] is forbidden! So in B-zone, we cannot increase y beyond D. So if we enter B-zone at some x and y<D, we can only move right (increasing x) until x>R, entering R-zone, or we are stuck. Actually, we can move right and also up, but up is limited by y=D. At y=D, we cannot go up. So the path in B-zone is constrained: it enters at (L, y0) with y0<D, and then moves right and up, but y ≤ D. To reach R-zone, it must be at x=R, y<D, then move right to x=R+1.

Similarly for T-zone: enters at (L, y0) with y0>U, then moves right and up, but x can increase. To leave T-zone to R-zone, it must be at x=R, y>U, then move right.

Can a path go from B-zone to T-zone directly? No, because that would require y to increase from ≤D to ≥U, passing through [D,U], but those points are forbidden. So it must go through L-zone or R-zone.

Can a path go from L-zone to R-zone without going through B or T? That would require passing through the interior, which is forbidden. So no.

So the sequence of zones visited by a monotone path is a sequence like: starts in L, B, R, T, or combinations, but respecting the partial order:
- L is "left", R is "right", B is "bottom", T is "top".
- Transitions: L->B, L->T, B->R, T->R.
- So the path can visit a sequence of zones that is consistent with this DAG of zones.
- The DAG has edges L->B, L->T, B->R, T->R.
- Note that L can transition to B or T, then from B to R, from T to R. But L cannot transition to R directly. Also, B and T are not connected.
- Also, a path can stay in one zone, or visit L then B then R, or L then T then R, or just L, etc.

Moreover, the path starts at some point in some zone, and ends at some point in some zone (possibly same or different).

The number of paths can be computed by decomposing the path into segments within zones, and transitions between zones.

Specifically, a path is determined by:
- Starting zone and point.
- Ending zone and point.
- Sequence of zones visited (which must be a valid path in the zone DAG: possibly L, L->B, L->B->R, L->T, L->T->R, B, B->R, T, T->R, R, or start in R directly? Can a path start in R-zone? Yes, if x0 > R or x0=R with y<D or y>U.
Similarly, can start in B, T, L.

Actually, a path can start in any zone, and end in any zone, as long as the sequence is consistent with the transition rules and the actual coordinates.

But we need to count all paths (any start, any end).

Total paths = sum over all valid (start zone Z_s, start point s) of (number of paths starting at s in Z_s that stay in allowed region).
By symmetry and linearity, we can compute the number of paths by considering the "transfer matrix" or by computing the number of paths in each zone and the transitions.

A cleaner approach: the total number of directed paths in a DAG can be computed as the sum over all vertices of the number of paths from some source to that vertex, but we want all paths, not just from a fixed source.

Wait: total number of paths in a DAG = sum_{v} (number of paths ending at v).
This equals sum_{v} R[v] where R[v] = number of paths from v to sink (but we don't have a single sink; we want all endpoints).

Actually, for any DAG, the number of paths is sum_{v} (number of paths from any source to v). This is because each path has a unique endpoint v, and is counted once in R[v] = sum_{s} paths(s,v).

So total = sum_{v in allowed} (sum_{s in allowed} paths(s,v)) = sum_v out-degree-sum? No.

Let P(v) = number of paths ending at v (i.e., from any source to v). Then P(v) = sum_{u->v} P(u) + 1 if v is a source (in-degree 0). Wait, sources are vertices with in-degree 0. In our grid, the sources are (0,0) only? No, (0,1) has in-edge from (0,0), so in-degree 1. Actually, in the directed grid (right/up), the only source is (0,0), and the only sink is (W,H). All other vertices have in-degree 2 (from left and below) and out-degree 2 (to right and above), except on the boundary.

Wait, in the full grid, (0,0) has in-degree 0, (W,H) has out-degree 0. But in the complement, there might be multiple sources and sinks? No, because movement is only right/up, so (0,0) is the only point with no incoming edges. Similarly, (W,H) is the only point with no outgoing edges? Not necessarily: if we remove some points, other points might have no incoming or outgoing edges within the allowed set.

For example, if (0,1) is removed, then (0,0) still has out-edge to (1,0) and (0,1), but (0,1) is removed, so only to (1,0). But (0,2) has in-edge from (0,1) which is removed and (1,2) which might be present. So it still has incoming from (1,2) if that's allowed. So it depends.

But in our case, the forbidden region is [L,R]×[D,U]. It doesn't include the boundaries necessarily? It includes them. So points adjacent to the hole might have reduced degree.

However, the only source in the directed graph (edges right/up) is (0,0), because any other point (x,y) has an incoming edge from (x-1,y) or (x,y-1), and at least one of those is in the allowed region and is a valid predecessor. Actually, if both predecessors are forbidden, then (x,y) has in-degree 0. When would that happen? (x-1,y) and (x,y-1) both forbidden. Since the forbidden set is a rectangle, this requires (x-1,y) and (x,y-1) both in [L,R]×[D,U]. So x-1 ≥ L, x ≤ R, y in [D,U], and y-1 ≥ D, y ≤ U. So x-1 ≥ L, x ≤ R implies x in [L+1, R]. y in [D+1, U]. So (x,y) is a point just inside the top-right of the forbidden region? Actually, if x in [L+1,R] and y in [D+1,U], then (x-1,y) has x-1 in [L,R] and y in [D,U], so forbidden. (x,y-1) has x in [L,R] and y-1 in [D,U], so forbidden. So (x,y) has in-degree 0 if both predecessors are forbidden. That means (x,y) is in the interior of the forbidden region? Wait, (x,y) itself: if x in [L,R] and y in [D,U], it's forbidden. So (x,y) is allowed only if it's not in the rectangle. So for (x,y) allowed, it cannot be in [L,R]×[D,U]. So the case x in [L+1,R] and y in [D+1,U] means (x,y) is in the rectangle (since L+1 ≤ R, so x in [L,R]), so forbidden. So no allowed point has both predecessors forbidden.

What about the boundary? If (x,y) = (L, y) with y=D+1 to U, then (x-1,y) = (L-1,y) is allowed (since x-1 < L), and (x,y-1) = (L,y-1). If y-1 ≥ D, then (L,y-1) is forbidden. So in-edge from (L-1,y) is present, in-edge from (L,y-1) is absent. So in-degree 1. Not a source.

Similarly, (x,y) with x=L, y=U: (L-1,U) allowed, (L,U-1) is it allowed? (L, U-1) has x=L, y=U-1. If U-1 ≥ D, then it's in [L,R]×[D,U] since R≥L, so forbidden. So in-degree 1 from (L-1,U).

So indeed, (0,0) is the only source. Similarly, (W,H) is the only sink? Check: (W,H) has out-edges to (W+1,H) and (W,H+1), which are outside the grid, so out-degree 0. Any other point (x,y) with x<W or y<H has at least one out-edge to (x+1,y) or (x,y+1) that is in the grid. But is it allowed? It might be forbidden. For example, (L-1, D) has out-edge to (L,D) which is forbidden, and to (L-1, D+1). If (L-1, D+1) is allowed, then out-degree 1. If (L-1,D+1) is forbidden? (L-1,D+1) has x<L, so allowed. So yes, out-degree 1.

What about (R, U)? out-edge to (R+1,U) which is allowed (x>R), and to (R,U+1) which is allowed (y>U). So out-degree 2.

What about (R, D)? out-edge to (R+1,D) allowed, to (R,D+1) forbidden. So out-degree 1.

So the graph has unique source (0,0) and unique sink (W,H).

Therefore, the total number of paths in the DAG is exactly the number of paths from (0,0) to (W,H) in the allowed region!

Wait, is that true? In a DAG with a unique source and unique sink, every path starts at the source and ends at the sink. Is that true here? A path is a sequence of vertices v0, v1, ..., vk where each step is an edge (right or up). v0 must have in-degree 0, so v0 = (0,0). vk must have out-degree 0, so vk = (W,H). Yes! Because any other vertex has both incoming and outgoing edges available (as argued, no other vertex is a source or sink). 

So the total number of paths is exactly the number of monotone paths from (0,0) to (W,H) that avoid the forbidden rectangle [L,R]×[D,U].

This is a classic problem! Number of paths from (0,0) to (W,H) avoiding [L,R]×[D,U].

Now, how to compute this efficiently?

The formula uses the reflection principle. The number is:
C(W+H, W) 
minus the number of paths that go through the forbidden region.

A path goes through the forbidden region iff it enters the rectangle. Since it's a convex region (in the grid sense), a path enters [L,R]×[D,U] iff it crosses the left or bottom boundary into it, and then crosses the right or top boundary out.

The standard inclusion-exclusion: the number of paths that avoid the rectangle is:
sum over the four "detour" possibilities.

Actually, the exact formula is:
Let the four corners of the forbidden rectangle be:
A = (L, D)   bottom-left
B = (R, D)   bottom-right
C = (L, U)   top-left
D = (R, U)   top-right

Paths from (0,0) to (W,H) avoiding the interior of the rectangle (the rectangle itself is forbidden, so including boundary).

The number is:
C(W+H, W) 
- C(L+D, L) * C((W-R)+(H-U), W-R)  [go around left-bottom to right-top?]
Wait, let's derive it.

A path from (0,0) to (W,H) that enters the rectangle must have a first point in the rectangle and a last point in the rectangle. The first point must be on the left or bottom edge of the rectangle (since it comes from outside). Similarly, the last point is on the right or top edge.

By inclusion-exclusion, or by the reflection principle, the number of paths that enter the rectangle is:
Paths that go from (0,0) to some point on the left edge (L, y) with y in [D,U], then to some point on the right edge (R, y') with y' in [D,U], then to (W,H). But this overcounts paths that enter and exit multiple times, but since the rectangle is convex, a monotone path enters and exits at most once.

Actually, for monotone paths, if a path enters a rectangle, it enters through the left or bottom edge, and exits through the right or top edge. It cannot re-enter because the rectangle is convex and movement is monotone.

So we can classify by the entry and exit edges.

The four possibilities for (entry edge, exit edge):
1. Left to Right: enter at (L, y) with y in [D,U], exit at (R, y') with y' in [D,U], with y ≤ y' (since y is non-decreasing).
2. Left to Top: enter at (L, y) with y in [D,U], exit at (x, U) with x in [L,R].
3. Bottom to Right: enter at (x, D) with x in [L,R], exit at (R, y') with y' in [D,U].
4. Bottom to Top: enter at (x, D), exit at (x', U), with x ≤ x'.

And also, the path might touch the corner. We need to be careful with double-counting at corners.

A cleaner way is to use the transformation that maps the problem to paths in a full grid with some "reflected" points.

The formula is:
Avoid(A,B) = C(B-A) - C(B - A') + C(B - A'') - ... where A' is the reflection of source across the first side hit, etc.

Specifically, the formula for the number of paths from s=(0,0) to t=(W,H) avoiding the rectangle [L,R]×[D,U] is:
det | C(t_i - s_j) | for some 2x2 determinant, or sum over four terms:

Let f(p,q) = number of paths from p to q = C((q.x-p.x)+(q.y-p.y), q.x-p.x).

The number of paths avoiding the rectangle is:
f((0,0), (W,H)) 
- f((0,0), (L-1, D-1)) * f((R+1, U+1), (W,H))  [reflecting across the bottom-left corner?]
No.

The standard result: the number of lattice paths from (0,0) to (W,H) that do not pass through any point of [L,R]×[D,U] is:
C(W+H, W) 
- C(L+D, L) * C((W-R-1)+(H-D-1)+2, W-R-1) ... I'm messing up the indices.

Let me look it up mentally. The formula is often written using the four "images" of the destination.

Define the four corners of the forbidden rectangle: (L,D), (R,D), (L,U), (R,U).

The number is:
C(W+H, W) 
- C((L-1)+(D-1), L-1) * C((W-R)+(H-U), W-R)  [paths that go through bottom-left corner area?]
This is not right.

Let me derive it from scratch using the transfer matrix or by writing the DP solution in O(W+H) time.

The DP for Q[x][y] (paths to (x,y) avoiding rectangle) is:
Q[0][0] = 1.
For x from 0 to W:
  For y from 0 to H:
    if L ≤ x ≤ R and D ≤ y ≤ U: Q[x][y] = 0.
    else if x>0 or y>0: Q[x][y] = (x>0 ? Q[x-1][y] : 0) + (y>0 ? Q[x][y-1] : 0).

We want Q[W][H].

This DP can be computed in O(WH) naively. We need O(W+H).

Since the forbidden region is a rectangle, the DP has a special structure. Specifically, the recurrence Q[x][y] = Q[x-1][y] + Q[x][y-1] means that Q is a sum of binomials, and the hole subtracts some binomials.

We can write Q[x][y] = C(x+y, x) - sum_{(a,b) in hole} (contribution of (a,b)).

Specifically, in the full grid, Q_full[x][y] = C(x+y, x).
With the hole, Q[x][y] = Q_full[x][y] - sum_{a=L..R, b=D..U} Q_full[a][b] * (paths from (a,b) to (x,y) in full grid) * I(condition that the path first hits the hole at (a,b)?) No, that's not right because the hole points are set to 0, and the DP propagates the zeros.

The correct formula using the matrix-tree theorem or Lindström is:
Q[x][y] = sum over paths in full grid from (0,0) to (x,y) that don't visit the hole.
This equals the coefficient in the generating function.

A standard way to compute this is to use the formula:
Q[W][H] = C(W+H, W) 
- C(L+D, L) * C((W-R-1)+(H-U-1)+2, W-R-1) 
+ C(L+U+1, L) * C((W-R-1)+(H-D-1)+2, W-R-1) 
+ C(R+D+1, R+1) * C((W-R-1)+(H-U-1)+2, W-R-1) 
- C(R+U+2, R+1) * C((W-R-1)+(H-D-1)+2, W-R-1)

Wait, let's think of the four "gates" around the rectangle.

A path that avoids the rectangle must go either:
- entirely in x < L (then it cannot reach W if L>0? But x can increase to W, so it must pass the rectangle. So it must go around.

The path can go around the rectangle by passing:
- Below: y < D when x in [L,R]. So it enters the "below" corridor at x=L, y<D, and exits at x=R, y<D.
- Above: y > U when x in [L,R]. Enters at x=L, y>U, exits at x=R, y>U.
- Left: x < L when y in [D,U]. Enters at y=D, x<L, exits at y=U, x<L.
- Right: x > R when y in [D,U]. Enters at y=D, x>R, exits at y=U, x>R.

But a path can only go around in one of these four ways? No, it can go around in multiple ways? Since the path is monotone, it can only go around once. It goes around either on the bottom, top, left, or right of the rectangle.

Actually, to go from x=0 to x=W while avoiding x in [L,R] for y in [D,U], the path must at some point be at y<D or y>U while crossing from x<L to x>R. So it goes through the bottom corridor or the top corridor.

Similarly, if it stays in y<D or y>U for all x, it goes around on the bottom or top.
If it goes through y in [D,U], it must be at x<L or x>R for all such y, so it goes around on the left or right.

So there are four "modes" for a path:
1. Pass below: y ≤ D for all x in [L,R]. (Actually, y can be >D outside [L,R], but when x in [L,R], y must be ≤D. Since y is non-decreasing, this means y ≤ D for all x ≥ some point.)
2. Pass above: y ≥ U for all x in [L,R].
3. Pass left: x ≤ L for all y in [D,U].
4. Pass right: x ≥ R for all y in [D,U].

Note that mode 1 and 2 are mutually exclusive for a given path? A path can have y ≤ D for x in [L,R] (mode 1), or y ≥ U (mode 2), or it can switch? If it switches from y<D to y>U, it must pass through y in [D,U], so it must be at x<L or x>R at that time. So it could be mode 1 then mode 3 or 4, etc.

Actually, the path's trajectory in the (x,y) plane relative to the rectangle: the rectangle is [L,R]×[D,U]. The path goes from (0,0) to (W,H). It can go:
- Below the rectangle: never enters the rectangle, and y ≤ D for x in [L,R]? Not necessarily y≤D everywhere, but when crossing the x-range [L,R], y is ≤D.
- Above: y ≥ U when crossing.
- Left: x ≤ L when crossing y-range [D,U].
- Right: x ≥ R when crossing.

These are the four "pure" strategies. But a path can combine them. For example, go left (x≤L) for low y, then go up, then go right (x≥R) for high y. That would be left then right, which means it passes through the left side of the rectangle and the right side.

In fact, the path must go around the rectangle on one of the four sides: bottom, top, left, or right. Because the rectangle is a connected obstacle, and the path is monotone, it must "go around" it. Going around means the path stays in the region that is, say, "south" of the rectangle, or "west", etc.

The four regions are:
South: y < D (plus the part at y=D outside x in [L,R])
North: y > U
West: x < L
East: x > R

A path from (0,0) to (W,H) in the complement must be contained in one of these four regions? No, because the path starts at (0,0) which is in the southwest (x<L if L>0, y<D if D>0). It can go north first, then east, etc.

But the path is monotone. The four regions are:
- SW: x<L, y<D
- NW: x<L, y>U
- SE: x>R, y<D
- NE: x>R, y>U

And the corridors:
- South corridor: L≤x≤R, y≤D
- North corridor: L≤x≤R, y≥U
- West corridor: y in [D,U], x≤L
- East corridor: y in [D,U], x≥R

A monotone path from (0,0) to (W,H) that avoids the interior of the rectangle must visit a sequence of these regions. Specifically, it can go:
- Start in SW (x<L, y<D) or south corridor (L≤x≤R, y<D) or if L=0, then x=0 is allowed.
- It can move right into south corridor, then continue to SE (x>R, y<D) or east corridor? No, from south corridor, moving right goes to x>R, y<D, which is SE. Or it can move up in south corridor, but y is bounded by D. So from south corridor, it can only go right to SE.
- From SW, it can go up to west corridor (y in [D,U], x<L), then up to NW, then right to north corridor, then right to NE.
- Or from SW, go right to south corridor, then right to SE, then up to east corridor, then up to NE.
- Or combinations.

So the possible "topologies" of the path around the rectangle are:
1. Go south: stay in y<D throughout. This means the path never has y≥D. But it needs to reach y=H, so if H>D, this is impossible unless the path goes through the rectangle? Wait, if y<D always, then the path is confined to y<D. But to get to y=H, it must increase y, so it must enter y≥D. So "go south" alone is impossible unless the path doesn't need to increase y past D. But the path must reach y=H, so it must go to y>H≥... so it must cross y=D. When it crosses y=D, if x is in [L,R], it enters the forbidden region. So to cross y=D safely, it must do so at x<L or x>R. So it must go to the west or east first.

Therefore, the path must pass through the west corridor (x<L, y in [D,U]) or the east corridor (x>R, y in [D,U]) to go from y<D to y>U (assuming H>U, which it is since U≤H, and if H≤U, then no top).

Similarly, to go from x<L to x>R, it must pass through the south or north corridor.

So the path must make two "turns" around the rectangle: one to go from x-side to y-side and one to go from y-side to x-side. The four pure paths are:
- South then East: go right at y<D, passing south of rectangle, then go up at x>R, passing east of rectangle.
- South then West: go up at x<L (but this is left), then go right at y>U? No.
- The four pure ways are:
  1. Bottom: cross from x=L to x=R at y<D (south corridor), then from there, to reach y=H, go up at x>R (east corridor). This is "go south, then east".
  2. Bottom then West: cross south, then go up at x<L? But if you cross south, you're at x>R, y<D. To go up at x<L, you have to go left, which is not allowed. So not possible.
  3. Left then Top: go up at x<L, crossing west corridor (y in [D,U]), then go right at y>U (north corridor). This is "go west, then north".
  4. Right then Bottom: go up at x>R (east corridor), then go left? No, can't go left. So not possible.

The valid sequences are:
- South corridor then East corridor: path goes from (0,0) to (L,D-1) or something, then through south corridor to (R, D-1), then up through east corridor to (W,H). This requires the path to enter the south corridor at x=L, y<D, and exit at x=R, y<D, then enter east corridor at x=R, y<D, exit at x=R, y=U, then go to (W,H).
- West corridor then North corridor: path goes up through west corridor (x=L, y from D-1 to U+1? Actually, enter at (L-1, D) or (L,D) with y=D, but (L,D) is forbidden? The corridor is y in [D,U], x=L. But (L,D) is in the forbidden rectangle (since x=L, y=D). So the west corridor is actually x<L, y in [D,U], and at x=L, the points (L,y) for y in [D,U] are forbidden. So to cross from x<L to x=L, we hit forbidden points. So we cannot be at x=L with y in [D,U]. The west corridor is x≤L, y in [D,U], but with the hole, x=L, y in [D,U] is removed. So the west corridor is x<L, y in [D,U] plus the points at x=L with y<D or y>U, but those are already in the south or north.
  The connection: to go from y<D to y>U, the path must be at x<L for all y in [D,U] (since if it is at x in [L,R], y in [D,U] is forbidden). So it goes up along x=L-1 or x<L, then at y>U, it can go right.
  This is the "left then top" path: stay in x<L until y>U, then go right.
- South corridor then East corridor: stay in y<D until x>R, then go up.
- North corridor then East corridor? That's just the left-right combination.
Actually, the four "corner" paths are determined by which two sides of the rectangle the path goes around. The path goes around two adjacent sides: either (south and east), or (south and west)? No, south and west are not adjacent; south is bottom, west is left, they are adjacent at the bottom-left corner. But the path cannot go around both because to go from south to west, it would have to go through the bottom-left corner, which is forbidden.

The path goes around exactly one corner of the rectangle? No, it goes around two sides: it must avoid the rectangle, so it passes either to the left of it or to the right of it (in the x-direction), and either below it or above it (in the y-direction). But it can only choose one of the four combinations: (left and below), (left and above), (right and below), (right and above). But (left and below) means it stays in x<L and y<D, which is the bottom-left region. From there, to reach (W,H), it must go to x>R and y>U. So it must cross both x=L and y=D or x=R and y=U, etc.

Actually, the path must go from (0,0) to (W,H). It can be classified by the order in which it passes the "gate" lines x=L, x=R, y=D, y=U.

Since the path is monotone, it can cross these lines in a specific order.

The lines are x=L, x=R, y=D, y=U.
The path starts at (0,0) with 0≤0≤L≤R≤W, 0≤0≤D≤U≤H.
It ends at (W,H) with W≥R, H≥U.

The path must cross x=L and x=R (if L<R or L>0). It must cross y=D and y=U (if D<U or D>0).

The crossings:
- To go from x<L to x>R, it must cross x=L and x=R in that order (since x is non-decreasing).
- To go from y<D to y>U, it must cross y=D and y=U in that order.

The path can cross these four lines in various orders, but it must respect the monotonicity.

The possible sequences of crossing the four "gates" (x=L, x=R, y=D, y=U) are constrained by the geometry: you cannot cross y=D before x=L if you are at x<L? No, you can cross y=D at x<L, then cross x=L at y>D, etc.

Let's list the possible orderings of the four events: cross x=L, cross x=R, cross y=D, cross y=U.
- The path must cross x=L before x=R.
- The path must cross y=D before y=U.
- Other than that, any order is possible? No, because you cannot be at (x,y) with x>L and y<D if you are going to x>R? You can.

But we also have the constraint that the path cannot visit the forbidden region. So the path cannot be at (x,y) with x in [L,R] and y in [D,U].

This means that between crossing x=L and crossing x=R, the path must have y<D or y>U.
Between crossing y=D and crossing y=U, the path must have x<L or x>R.

This severely restricts the orderings.

Let's denote the four "events":
E1: cross x=L (i.e., move from x=L-1 to x=L, or start at x≥L? We can start at x≥L. Similarly for others.)
E2: cross x=R (move from x=R to x=R+1, or start at x>R)
E3: cross y=D
E4: cross y=U

The path starts at (x0,y0) with 0≤x0≤W, 0≤y0≤H, and ends at (x1,y1) with x0≤x1, y0≤y1.
It must avoid the rectangle.

The condition to avoid the rectangle means that the path cannot be in the interior.

The four "detour" paths that go around the rectangle are:
1. Go south then east: the path crosses y=D? No. It stays in y<D until x>R, then goes up. This means it crosses x=L and x=R while y<D. It may or may not cross y=D and y=U later.
   Specifically, it is at y<D for all points with x in [L,R]. It can have y<D before and after, and y>U after.
   In this case, the path crosses x=L and x=R (if it goes to x>R) while y<D. It then crosses y=D and y=U while x>R.
   Order: cross x=L, cross x=R, cross y=D, cross y=U. All while avoiding the hole.
2. Go west then north: stay in x<L until y>U, then go right. Crosses y=D and y=U while x<L. Then crosses x=L and x=R while y>U.
   Order: cross y=D, cross y=U, cross x=L, cross x=R.
3. Go south then west? That's not possible because if you go south (y<D) and then west (x<L), but you start at x<L. You can't go to x<L after x>R.
4. Go east then north: stay in y<D until x>R, then go up to y>U. This is the same as 1: south then east.
5. Go west then south: stay in x<L until y>U? That's north.
   Actually, the only two "around" paths are:
   - Pass south of the rectangle: y < D when x in [L,R]. Then to get to y=H, must go up at x>R or x<L. But to go up at x<L after x>R is impossible. So must go up at x>R. This is the "bottom-right" path.
   - Pass north: y > U when x in [L,R]. Then go up at x>R or x<L. But to go up at x>R, already at x>R. To go up at x<L, must not have passed x=L yet. So either:
     a) Not yet passed x=L: then go up at x<L, then cross x=L and x=R at y>U. This is "top-left" path: west then north? Actually, if you go up at x<L, you are going through the west corridor. Then you go right at y>U. So this is the "left then top" path.
     b) Already passed x=R: then go up at x>R. This is "right then top", but if you already passed x=R, you are at x>R. To go up at x>R, you are in the east corridor. But to have passed x=R, you must have crossed x=L and x=R. When you crossed x=R, you must have been at y<U (to avoid the hole, since y>U would mean you were in the north corridor, but you could have been). 
     Let's be systematic.

The path from (0,0) to (W,H) avoiding [L,R]×[D,U] must be contained in the complement. The complement has four "connected components"? No, it's connected, but the path can be thought of as going around the rectangle.

There are exactly four ways to go around the rectangle, corresponding to the four "gates" at the corners. Actually, for a rectangle, there are four ways to go from the southwest to the northeast while avoiding it: go around the bottom, or around the top, or around the left, or around the right? No, going around the bottom means staying south, but then you can't go north. You have to go around two sides.

The standard result: the number of paths is the sum of four terms, each corresponding to going around a specific corner. But with the rectangle, it's the sum of four terms with signs.

The formula is:
C(W+H, W) 
- C(L+D, L) * C((W-R-1)+(H-U-1)+2, W-R-1)  [around bottom-left?]
+ C(L+U+1, L) * C((W-R-1)+(H-D-1)+2, W-R-1)  [around top-left?]
- C(R+D+1, R+1) * C((W-L-1)+(H-U-1)+2, W-L-1)  [around bottom-right?]
+ C(R+U+2, R+1) * C((W-L-1)+(H-D-1)+2, W-L-1)  [around top-right?]

This is getting messy. Let me derive it using the method of images.

The number of paths from A to B avoiding the rectangle is given by the determinant formula or by summing over the four images of B reflected across the sides of the rectangle.

Define the four corners of the rectangle: P1=(L,D), P2=(R,D), P3=(L,U), P4=(R,U).

The number of paths from (0,0) to (W,H) avoiding the closed rectangle [L,R]×[D,U] is:
det | 
C(W+H, W)  ... |
Actually, it's:
N = C(W+H, W) 
- C((0,0) to P1) * C(P1' to (W,H)) 
- C((0,0) to P2) * C(P2' to (W,H)) 
- C((0,0) to P3) * C(P3' to (W,H)) 
- C((0,0) to P4) * C(P4' to (W,H)) 
+ C((0,0) to P1'') * C(P1'' to (W,H)) 
+ ...

The reflection method: to avoid the rectangle, we reflect the destination across the sides. The four "primary" images of (W,H) across the four sides of the rectangle:
- Reflect across x=L: (2L - W, H)
- Reflect across x=R: (2R - W, H)
- Reflect across y=D: (W, 2D - H)
- Reflect across y=U: (W, 2U - H)

Then the number of paths avoiding the rectangle is:
C(W+H, W) 
- [paths that hit x=L] - [paths that hit x=R] - [paths that hit y=D] - [paths that hit y=U] 
+ [paths that hit two sides] - ...

A path hits x=L if it has a point with x=L. The first such point is at (L, y) for some y. The number of paths that hit x=L is the number of paths that go from (0,0) to some (L,y) and then to (W,H), with the first point on x=L being (L,y). This is sum_{y} C(L+y, L) * C((W-L)+(H-y), W-L).
This equals C(W+H, W) - C(W+H, W-L-1)? No.

The standard formula for paths avoiding a vertical line x=L is: C(W+H, W) - C(W+H, W-L-1) (with appropriate adjustments).

But for a rectangle, we use the inclusion-exclusion on the four boundaries.

The number of paths from (0,0) to (W,H) that do not visit any point in [L,R]×[D,U] is:
C(W+H, W) 
- A(L,D) - A(R,U) + ... 

Let me look for the correct formula online in my memory.

The formula is:
N = sum_{i=0}^1 sum_{j=0}^1 (-1)^{i+j} C( (L-1+i) + (D-1+j), L-1+i ) * C( (W-R-1+i) + (H-U-1+j), W-R-1+i ) 
   for the case where we go around the bottom-left? No.

Actually, the four "paths around the rectangle" correspond to choosing a corner to go around. But the formula is a 2x2 determinant.

The number of paths from (0,0) to (W,H) avoiding [L,R]×[D,U] is:
det [ C( (W - a_i) + (H - b_j), W - a_i ) ] for a_i, b_j being the coordinates of the corners? 

Let's define the four "detour" points. The path can be decomposed as:
(0,0) -> (x1,y1) -> (x2,y2) -> (W,H)
where (x1,y1) is the exit from the "west" or "south" side, and (x2,y2) is the entry to the "east" or "north" side.

Specifically, to avoid the rectangle, the path must pass through one of the four "gates": the point (L, D-1) or (L-1, D) is not a single point.

I recall that the number of paths from (0,0) to (W,H) avoiding [L,R]×[D,U] is:
C(W+H, W) 
- C(L+D, L) * C((W-R-1)+(H-D-1)+2, W-R-1) 
- C(L+U+1, L) * C((W-R-1)+(H-U-1)+2, W-R-1) 
- C(R+D+1, R+1) * C((W-L-1)+(H-D-1)+2, W-L-1) 
- C(R+U+2, R+1) * C((W-L-1)+(H-U-1)+2, W-L-1) 
+ 2 * C(R+D+1, R+1) * C((W-L-1)+(H-U-1)+2, W-L-1)? No.

Let me derive it using the transfer matrix or by computing the DP in O(W+H) time.

Since the DP is Q[x][y] = Q[x-1][y] + Q[x][y-1] for allowed points, and the forbidden region is a rectangle, we can compute Q[W][H] by processing the grid row by row or column by column, but we need to skip the forbidden region.

The standard way to handle a rectangular hole in grid DP is to note that the DP values are binomial coefficients, and the hole subtracts a "block" of influence.

Specifically, let f(x,y) = C(x+y, x) for the full grid.
For the grid with hole, Q(x,y) = f(x,y) - sum_{a=L..R, b=D..U} f(a,b) * g(x-a, y-b) where g is the number of paths from (a,b) to (x,y) in the full grid, but only if the path doesn't visit the hole again. Since the hole is convex, if we remove it, the first visit to the hole is at some boundary point.

This is equivalent to: Q(x,y) = f(x,y) - sum_{boundary points p of hole} (number of paths from (0,0) to p in full grid that don't visit hole before p) * (number of paths from p to (x,y) in full grid).
And the paths that don't visit the hole before p are exactly the paths that avoid the hole up to p.

This is circular. But we can use the fact that the hole is a rectangle to write an explicit formula.

Another approach: use generating functions. The number of paths from (0,0) to (W,H) in the complement is the coefficient of x^W y^H in 1/(1-x-y) minus the contribution of the hole.

The generating function for full grid is 1/(1-x-y).
The generating function for the grid with a hole [L,R]×[D,U] removed is:
F(x,y) = 1/(1-x-y) - x^L y^D * (1-x^{R-L+1})(1-y^{U-D+1})/(1-x)(1-y) * 1/(1-x-y)?
No.

The hole means we set the coefficients of x^a y^b for a in [L,R], b in [D,U] to 0.
So the generating function is:
G(x,y) = 1/(1-x-y) * (1 - x^L y^D (1-x^{R-L+1})(1-y^{U-D+1}) / ((1-x)(1-y)) )? 
No, the hole is a product, not a sum.

Actually, the generating function for the number of paths to (x,y) is the coefficient in:
sum_{paths} x^{end.x} y^{end.y} = 1/(1-x-y).
When we remove points, we subtract the paths that go through those points.
A path that goes through a point (a,b) contributes to the coefficient.
The set of paths that visit the hole is the union over (a,b) in hole of paths through (a,b).
By inclusion-exclusion on the rectangle, the generating function for paths avoiding the rectangle is:
1/(1-x-y) * [1 - (hole factor)] but the hole is not a simple factor.

We can write the number as:
N = [x^W y^H] ( 1/(1-x-y) * (1 - x^L y^D * P(x,y)) ) where P accounts for the hole.

Specifically, the "transfer matrix" for a row: when we go from row y to y+1, we multiply by a matrix. But with a hole, it's messy.

Let's go back to the idea of computing the sum S = sum_{x,y} Q[x][y] in O(W+H) time.

We have Q[x][y] = number of paths from (0,0) to (x,y) avoiding the hole.
The total number of paths in the DAG is S = sum_{x,y} Q[x][y] * (is (x,y) allowed?).

But earlier we argued that the number of paths in the DAG is Q[W][H] (since unique source and sink). Wait, is that true? The number of paths from (0,0) to (W,H) is Q[W][H]. And since every path in the DAG must go from (0,0) to (W,H) (because (0,0) is the only source and (W,H) is the only sink), the total number of paths is exactly Q[W][H].

Is (W,H) the only sink? A sink is a vertex with no outgoing edges to allowed vertices.
For (W,H), the out-edges would be to (W+1,H) and (W,H+1), which are outside the grid, so no out-edges. So it's a sink.
For (W, y<H), out-edge to (W, y+1) is present if (W, y+1) is allowed. (W, y+1) has x=W, which is ≥R, and y+1 ≤ H. If y+1 is in [D,U], then (W, y+1) is allowed only if W>R or y+1 not in [D,U] at x=W. Since x=W>R, (W,y+1) is allowed for all y+1. So (W, y) for y<H has an out-edge to (W, y+1) which is allowed. So not a sink.
For (x<W, H), out-edge to (x+1, H) is allowed since y=H≥U, so if x+1 in [L,R], then (x+1, H) is allowed because y=H>U. So not a sink.
So (W,H) is the unique sink. Similarly, (0,0) is the unique source. (Check: (0,0) has no in-edges. (0,y>0) has in-edge from (0,y-1) which is allowed if y-1 not in [D,U] or x=0<L? Actually (0,y-1) has x=0<L, so always allowed. So (0,y) has in-edge from (0,y-1) for y>0. So not a source.)
Therefore, yes, every path starts at (0,0) and ends at (W,H).
So total paths = Q[W][H].

Great! So we just need to compute Q[W][H] for the grid with rectangular hole.

Now, how to compute Q[W][H] efficiently?

Q[W][H] = number of paths from (0,0) to (W,H) avoiding [L,R]×[D,U].

This is a standard problem. The formula is:

Let C(n,k) be binomial coefficient.
Define:
A = C(L+D, L)
B = C(L+U+1, L)   (path to just above the top-left? No)
Actually, the formula uses the four corners of the forbidden rectangle as "via" points.

The number is:
N = C(W+H, W) 
- A1 * B1 - A2 * B2 - A3 * B3 - A4 * B4 
+ A12 * B12 + A13 * B13 + A14 * B14 + A23 * B23 + A24 * B24 + A34 * B34 
- A123 * B123 - A124 * B124 - A134 * B134 - A234 * B234 
+ A1234 * B1234

This is the inclusion-exclusion over the four sides. But since the sides are lines, it's complex.

For a rectangle, the number of paths that avoid it is given by the determinant:
| C(W+H, W)   C(W+H, W-L-1) |
| C(W+H, W-D-1) C(W+H, W-L-D-2) | ? No.

I recall that the number of paths from (0,0) to (W,H) avoiding a rectangle [1,a]×[1,b] is:
C(W+H, W) - C(W+H, W-a-1) - C(W