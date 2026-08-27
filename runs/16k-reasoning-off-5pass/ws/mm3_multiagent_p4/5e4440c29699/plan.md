We need to count monotone lattice paths (only right/up steps) among allowed blocks: all points in rectangle [0,W]×[0,H] except the forbidden rectangle [L,R]×[D,U] (the region with L≤x≤R and D≤y≤U is removed). The answer is sum over all allowed starting points of the number of monotone paths from that start to any other allowed point (including the start itself as a zero-length path). Equivalently, sum over ordered pairs (A,B) of allowed lattice points with A≤B componentwise of the number of monotone paths from A to B. A standard trick: total ordered pairs = sum over all paths of (length+1) choose 2? Let's derive.

Alternative: For each path (sequence of points P0,P1,…,Pk where each step is +x or +y, and all points are allowed), count it once. So we just need total number of monotone paths staying inside allowed region. Since starting point can be any allowed point, this is exactly the number of such paths. Wait, sample 1 says 192. Let's test: allowed region is a rectangle with a hole. Number of monotone paths from any allowed start to any allowed end, moving only through allowed points. That's exactly the count. So we need to compute total number of monotone lattice paths in the region.

We can compute via DP: dp[x][y] = number of paths ending at (x,y) from any allowed start, i.e., sum of dp[x-1][y] + dp[x][y-1] (with dp of out-of-region as 0, and dp at each allowed point starts at 1 for the path of length 0 starting there). Sum over all dp[x][y] is the answer.

But W,H up to 1e6, so we cannot iterate full grid. However, the forbidden region is a single axis-aligned rectangle. The allowed region is the grid minus a rectangular hole. We need a combinatorial formula.

Observation: Monotone paths in a full rectangle [0,W]×[0,H] from any start to any end: total = number of lattice points in rectangle squared? No. For full rectangle, number of paths (any start, any monotone path) is sum_{x=0..W} sum_{y=0..H} C(x+y, x). Because each point (x,y) has C(x+y, x) paths from (0,0), but start is arbitrary. Actually, if we allow any start, the number of paths ending at (x,y) is sum_{i=0..x} sum_{j=0..y} C((x-i)+(y-j), x-i) = C(x+y+2, x+1)? Let's compute. The number of monotone paths from any allowed start to (x,y) within the rectangle is the number of ways to choose a start (i,j) with i≤x, j≤y and a path from (i,j) to (x,y). A path from (i,j) to (x,y) has C((x-i)+(y-j), x-i) choices. So total = sum_{i=0..x} sum_{j=0..y} C(x-i+y-j, x-i) = sum_{a=0..x} sum_{b=0..y} C(a+b, a) where a=x-i, b=y-j. This equals C(x+y+2, x+1). Indeed, known identity: sum_{a=0..x} sum_{b=0..y} C(a+b, a) = C(x+y+2, x+1). So total paths in full rectangle = sum_{x=0..W} sum_{y=0..H} C(x+y+2, x+1).

We can compute this closed form. Let S(W,H) = sum_{x=0}^W sum_{y=0}^H C(x+y+2, x+1).

Now we have a hole. We need to subtract paths that go through the forbidden region. But careful: a path is invalid if it visits a point in the forbidden region. We can use inclusion-exclusion or subtract paths that enter the forbidden region.

We can count valid paths = total paths in full rectangle - paths that pass through the forbidden region (i.e., contain at least one point in the hole). Since the hole is a rectangle, any path that enters the hole must pass through its boundary. Standard technique: sum over entry points.

Alternatively, we can compute dp restricted to allowed region using combinatorial formulas. The allowed region is a rectangle minus a hole. The DP recurrence dp[x][y] = dp[x-1][y] + dp[x][y-1] + 1 (for the path of length 0). The +1 is because at each point we can start a new path. This is equivalent to counting all monotone paths in the region.

We can compute sum of dp over the region. Let's denote f(x,y) = sum of dp over rectangle [0,x]×[0,y] within allowed region. But the region is not convex.

Better approach: The set of allowed points is the union of up to 4 rectangles: the big rectangle minus the hole. The big rectangle is [0,W]×[0,H]. The hole is [L,R]×[D,U]. The complement consists of:
- Left part: [0, L-1] × [0, H] (if L>0)
- Right part: [R+1, W] × [0, H] (if R<W)
- Bottom middle part: [L, R] × [0, D-1] (if D>0)
- Top middle part: [L, R] × [U+1, H] (if U<H)

But the left and right parts are full height, while the middle parts are only in the y-range below and above the hole.

Since DP is additive in the sense that paths are confined to allowed region, we can compute the total number of paths by inclusion-exclusion: total paths in full rectangle minus paths that go through the hole. A path goes through the hole if and only if it visits at least one point in the hole. Because the hole is a rectangle, any monotone path that enters the hole must pass through its left boundary x=L at some y in [D,U] or its bottom boundary y=D at some x in [L,R]. Actually, a path enters the hole at some point (x0,y0) with L≤x0≤R, D≤y0≤U. Since it moves only right/up, once it enters, it stays inside (because it can only move right or up, so x,y non-decreasing). So the entry point is the first point in the hole along the path. The entry point must have either x=L (coming from x=L-1) or y=D (coming from y=D-1). So we can count paths that enter the hole by summing over entry points on the left or bottom boundary of the hole.

Let E be the set of points in the hole that are reachable from outside without passing through other hole points. The left boundary of the hole: (L, y) for y in [D, U]. The bottom boundary: (x, D) for x in [L, R]. The corner (L,D) is on both.

For each such entry point e, the number of paths that have e as the first point in the hole is: (number of paths from any allowed start to the point just before e, i.e., the neighbor outside) × (number of paths from e to any allowed end, staying inside the hole or leaving? Wait, after entering the hole, the path can continue inside the hole, and eventually exit. But the path is invalid if it enters the hole at all. So we need to count all paths that ever visit the hole. We can count: number of paths that pass through the hole = sum_{e in entry set} (paths from allowed start to the point just before e, staying in allowed region) × (number of paths from e to any allowed end, staying anywhere). But careful: after e, the path can go anywhere (including staying in hole or exiting the hole). However, if we sum over all e as the first entry point, and for each e count all paths that go through e (including those that may have entered earlier via another e?), since e is the first point in the hole, we must restrict that the path does not visit the hole before e. That is automatically satisfied if e is the first entry. So for each e, we need: number of paths from any allowed start to a point just outside the hole that is adjacent to e (i.e., (L-1, y) if e=(L,y) with L>0, or (x, D-1) if e=(x,D) with D>0), staying in allowed region, times the number of paths from e to any allowed end (including staying in hole, or exiting the hole? Actually after e, the path can go anywhere, but since e is inside the hole, the path from e to end is a path starting at e, moving right/up, possibly leaving the hole (by passing through the right or top boundary of the hole) and then continuing in allowed region. But for the purpose of counting invalid paths (those that visit the hole), we need all paths that visit the hole at least once. If we count for each e the number of paths that have e as the first hole point, we cover all invalid paths exactly once. The number of such paths = (paths from any start to the predecessor of e) × (paths from e to any end). Because the predecessor is outside the hole, and from e onward, any path is allowed (it will stay in the hole until possibly exiting, but that's fine; the path is invalid anyway).

But we must be careful: the predecessor of e might be outside the allowed region? The predecessor of (L, y) is (L-1, y). Since y is in [D,U], and L-1 < L, so (L-1, y) is not in the hole. But could it be outside the big rectangle? If L=0, then (L-1,y) is outside. In that case, there is no predecessor on the left; the path must have started at (L,y) itself. So we need to handle L=0 and D=0 cases.

Similarly for e=(x,D), predecessor is (x, D-1). If D=0, then (x, D) is a start point.

So we can write:
Invalid paths = sum_{y=D..U} (paths ending at (L-1, y) with L>0) * (paths starting from (L, y) to any end) + sum_{x=L..R} (paths ending at (x, D-1) with D>0) * (paths starting from (x, D) to any end) - double count the corner (L,D) if both L>0 and D>0? Actually the corner is included in both sums: as (L, D) in left boundary (y=D) and in bottom boundary (x=L). But if we treat them separately, we must subtract the overcount. However, if we consider the predecessor: for (L,D), predecessor on left is (L-1, D), on bottom is (L, D-1). A path that has (L,D) as first entry point could have come from (L-1, D) or from (L, D-1) or started at (L,D) if L=0 and D=0? Actually if both L>0 and D>0, (L,D) has two predecessors. The path could approach from left or from bottom. So the set of paths with first entry at (L,D) is the union of those coming from left and those coming from bottom. They are disjoint because the last step before (L,D) is either from (L-1,D) or from (L,D-1). So if we sum over left boundary entry points, we count paths coming from left; over bottom boundary, paths coming from bottom. At (L,D), these are disjoint. So we don't need to subtract. Wait, but if we sum over all left boundary points (L, y), y in [D,U], and for each we multiply by paths ending at (L-1, y), that counts paths that enter the hole at (L, y) from the left. Similarly for bottom. At the corner, the path could enter from left or from bottom. These are two disjoint sets of paths. So total invalid paths = sum_{y=D..U, L>0} A(L-1, y) * B(L, y) + sum_{x=L..R, D>0} C(x, D-1) * D(x, D), where A(x,y) is number of paths from any allowed start to (x,y), B(x,y) is number of paths from (x,y) to any allowed end.

But note: after entering the hole, the path can go anywhere. The number of paths from (x,y) to any allowed end is the same as the number of paths from (x,y) to any end in the full rectangle, but restricted to allowed region. However, if we start at a point inside the hole, the path can go through the hole and then exit. But the number of paths from (x,y) to any allowed end is exactly the total number of monotone paths from (x,y) to points in the allowed region, moving right/up. This is the same as the total number of paths in the allowed region starting at (x,y). But we can compute it as the number of paths to (x,y) in the "reversed" region? Alternatively, by symmetry, the number of paths from (x,y) to any end in a region is equal to the number of paths from any start to (W-x, H-y) in the region reflected. But the region is not symmetric.

We need to compute:
- A(x,y): total number of monotone paths from any allowed start to (x,y) within allowed region.
- B(x,y): total number of monotone paths from (x,y) to any allowed end within allowed region.

Note that by reversing the grid (x -> W-x, y -> H-y), the allowed region is preserved? The hole is [L,R]×[D,U], after reversal the hole becomes [W-R, W-L] × [H-U, H-D]. That's a different hole unless W-R = L and W-L = R, i.e., symmetric. So not symmetric.

But we can compute B(x,y) = total number of paths from (x,y) to any end = sum_{x'>=x, y'>=y} (number of paths from (x,y) to (x',y')) over allowed (x',y'). This is similar to A but for the region shifted.

Alternatively, we can compute the total number of valid paths directly using a combinatorial formula with inclusion-exclusion on the hole. There is a known formula for counting lattice paths avoiding a rectangular obstacle. The number of paths from (0,0) to (W,H) that avoid a rectangle is given by the Lindström-Gessel-Viennot lemma or using the reflection principle. But here we have arbitrary start and end.

Wait, the problem is to count all monotone paths in the region (any start, any end). This is equivalent to the sum over all start-end pairs of the number of paths between them. This is the same as the number of paths in the "free" monoid generated by the region. Another approach: The total number of paths is the sum over all points (x,y) of the number of paths from any start to (x,y) that stay in the region. This is exactly the DP we mentioned.

We can compute the DP sum efficiently by splitting the region into rectangles. The allowed region is the union of up to 5 rectangles: the big rectangle minus the hole. Actually, the complement of the hole in the big rectangle is a union of disjoint rectangles:
- A: [0, L-1] × [0, H]  (if L>0)
- B: [R+1, W] × [0, H]  (if R<W)
- C: [L, R] × [0, D-1]  (if D>0)
- D: [L, R] × [U+1, H]  (if U<H)

These are axis-aligned rectangles that together form the allowed region. However, the region is not just the disjoint union; the DP paths can go between these rectangles. For example, a path can go from A to C to B, etc. So we cannot just sum independent contributions.

But the DP on the whole region can be computed by processing the grid row by row or column by column, but the grid is too large. We need a formula.

Let's think about the structure. The hole is a rectangle. The allowed region is a rectangle with a rectangular hole. The number of monotone paths in such a region can be computed using the principle of inclusion-exclusion on the hole: total paths in big rectangle minus paths that go through the hole.

We already started that. Let's denote:
Total = sum_{x=0}^W sum_{y=0}^H C(x+y+2, x+1) = T(W,H).

Now we need to subtract paths that visit the hole H = [L,R]×[D,U].

A path visits H if and only if it has a point in H. As argued, the first point in H is either on the left boundary (L, y) for y in [D,U] or on the bottom boundary (x, D) for x in [L,R]. Let's define:
For a point (x,y) in the allowed region, let f(x,y) be the number of paths from any start to (x,y) within allowed region. Let g(x,y) be the number of paths from (x,y) to any end within allowed region.

Then the number of invalid paths is:
I = sum_{y=D}^U f(L-1, y) * g(L, y)   (if L>0; if L=0, f(-1, y) is 0, but we need to account for paths that start at (0,y). Actually, if L=0, then the left boundary of the hole is at x=0. A path could start at (0,y) for y in [D,U]. The number of such paths is 1 (start at (0,y)) * g(0,y). So we need to add g(0,y) for y in [D,U] when L=0.)
Similarly, I_bottom = sum_{x=L}^R f(x, D-1) * g(x, D)   (if D>0; if D=0, add g(x,0) for x in [L,R]).

But careful: This counts each invalid path exactly once? Let's check: an invalid path has a unique first point in H. That point is either on the left boundary or bottom boundary (or both if it's the corner). If it's on the left boundary, the path must have come from the left (from (L-1, y) or started there). If it's on the bottom boundary, it came from below. The corner is on both, but a path that enters at the corner must have come from either left or below, not both. So the sets of paths with first entry on left (excluding corner?) and on bottom are disjoint if we define carefully.

Specifically:
- Left entry: first point is (L, y) for some y in [D, U], and the previous point is (L-1, y) or it's the start if L=0. The predecessor's y-coordinate is the same.
- Bottom entry: first point is (x, D) for some x in [L, R], and the previous point is (x, D-1) or it's the start if D=0.

These are disjoint because the first point in H cannot have both x=L and y=D unless it came from either left or below, and we can attribute it to one based on the previous step. So the sum is correct.

Thus, Invalid = (if L>0: sum_{y=D}^U f(L-1, y) * g(L, y)) + (if L=0: sum_{y=D}^U g(0, y)) + (if D>0: sum_{x=L}^R f(x, D-1) * g(x, D)) + (if D=0: sum_{x=L}^R g(x, 0)).

But wait: if L=0, the left boundary of the hole is at x=0. The points (0, y) for y in [D,U] are in the hole. A path that starts at (0,y) has first point in the hole. So we should count g(0,y) for those. But also, could a path enter the hole at (0,y) from the left? No, because x cannot be negative. So only start. So the term is g(0,y).

Similarly for D=0.

Now, we need to compute f(x,y) and g(x,y) for points on the boundary of the hole. f(x,y) is the number of paths from any allowed start to (x,y) staying in allowed region. g(x,y) is the number of paths from (x,y) to any allowed end staying in allowed region.

Notice that g(x,y) for a point inside the hole is not the same as g in the full rectangle, because the path is restricted to allowed region. However, we can compute f and g using the DP formula, but we need efficient computation.

Observe that the allowed region is a rectangle minus a hole. The DP on this region can be solved by considering the contributions from the left and bottom parts. For f(x,y), it depends on whether (x,y) is left of the hole, right of the hole, or in the middle x-range. Since f is the sum of paths from any start, we can derive formulas for f in different regions.

Similarly for g, we can compute it by symmetry: g(x,y) is the number of paths from (x,y) to any end. This is equivalent to f in the region reflected across both axes, but the hole moves. However, we can compute g by a similar DP backwards.

Let's attempt to compute f(x,y) for any (x,y) in the allowed region. The recurrence: f(x,y) = 1 (for start) + f(x-1,y) + f(x,y-1) for x,y in allowed region, with f(-1, y) = f(x, -1) = 0, and if a point is in the hole, f(x,y) is not defined (we don't care). We want to compute f for points on the left boundary of the hole (L, y) with y in [D,U], and for points on the bottom boundary (x, D) with x in [L,R]. But note: for the left boundary, the point (L, y) is in the hole! Wait, the hole is [L,R]×[D,U]. The left boundary of the hole is at x=L, but those points are inside the hole. However, in our invalid path count, we need f(L-1, y) for y in [D,U]. f(L-1, y) is the number of paths to the point just left of the hole. That point is in the allowed region (since x < L). So we need f for points with x = L-1, y in [D,U]. Similarly, we need f(x, D-1) for x in [L,R].

So we need f on the left side of the hole (x = L-1) and on the bottom side of the hole (y = D-1). And we need g for points on the left boundary of the hole (x = L) and bottom boundary (y = D). But g(L, y) for y in [D,U] is the number of paths from (L, y) to any end. (L,y) is in the hole, but we can still compute g for it as if it were allowed? Wait, g(x,y) is defined for allowed points only? In our definition, g(x,y) is the number of paths from (x,y) to any allowed end, staying in allowed region. If (x,y) is in the hole, then the path from (x,y) is not allowed to stay in allowed region because the start is in the hole. But in the invalid path counting, we consider the path after it has entered the hole. The start of the suffix is the entry point, which is in the hole. The path from that point onward is allowed to go anywhere, including staying in the hole or exiting. So g(L,y) should count all paths from (L,y) to any allowed end, where the path can go through the hole and then exit. But wait, if we count all paths from (L,y) to any end, that includes paths that might go back through the hole? No, from (L,y), the path moves right/up. It can stay in the hole until it exits through the right or top boundary, or it can exit immediately if it goes right and x>R or up and y>U. But all such paths are valid continuations of an invalid path. So we need to count the number of monotone paths from (L,y) to any point in the allowed region (including points inside the hole and points outside). But careful: after entering the hole, the path is already invalid, so we just need to count all possible continuations, which are all paths from (L,y) to any point in the big rectangle, because the path can go anywhere (the restriction to allowed region is only for the part before entering the hole; after entering, the path is not restricted? Actually, the problem says: Snuke moves such that the point after moving must also have a block. So the path must always stay on blocks. If the path enters the hole, there are no blocks there. So the path cannot enter the hole. So any path that goes through the hole is invalid. So the set of valid paths is exactly those that never visit the hole. So when we count invalid paths, we are counting paths that violate the condition. The part of the path after entering the hole is not a valid path by itself, but we can still count it as a continuation of an invalid path. The number of ways to continue from the entry point to the end is the number of monotone paths from that entry point to any point in the big rectangle (since the path could go through the hole, but we are counting the total number of paths that start at the entry point and go to some end, without any restriction? Wait, no: the path after entering the hole is still a path in the town, but the town has no blocks in the hole. So the path cannot go through the hole. So an invalid path is one that includes a point in the hole. But the path is a sequence of points, each of which must be a block. So if a path includes a point in the hole, that point is not a block, so the path is not a valid path. But we are counting the number of possible paths Snuke could have taken. Those are exactly the valid paths. So we want to count valid paths. We can compute total paths in the full rectangle (where every point is a block) and subtract those that visit the hole. The paths that visit the hole are those sequences of points that lie in the full rectangle but include at least one point in the hole. For such a path, the part before the hole is in the allowed region, and the part after the first hole point can be anywhere in the full rectangle (including the hole). So the number of ways to continue from the first hole point to the end is the number of monotone paths from that point to any point in the full rectangle, with no restrictions. So g(x,y) for a point in the hole should be the number of paths from (x,y) to any point in the full rectangle [0,W]×[0,H] (since after entering the hole, the path can go anywhere, even back through the hole, but it's already invalid). So g(x,y) for (x,y) in the hole is simply the total number of paths from (x,y) to any end in the full rectangle, which is sum_{x'>=x, y'>=y} C((x'-x)+(y'-y), x'-x) = C((W-x)+(H-y)+2, W-x+1) by the same identity. So g(x,y) for a point in the hole is independent of the allowed region; it's just the full rectangle value.

But wait: is that correct? The path after entering the hole can go anywhere in the full rectangle, but does it have to avoid the hole? No, because the path is already invalid; we are just counting how many such invalid paths exist. So yes, any continuation from the entry point is possible, as long as it's a monotone path in the full rectangle. So g(x,y) for a hole point is the total number of monotone paths in the full rectangle from (x,y) to any end.

Now, what about f(x,y) for points outside the hole? f(x,y) is the number of paths from any start to (x,y) that stay in the allowed region. This is the DP value in the allowed region.

So we need:
- f(x,y) for x = L-1, y in [D, U] (if L>0)
- f(x, D-1) for x in [L, R] (if D>0)
- g(0, y) for y in [D, U] (if L=0)
- g(x, 0) for x in [L, R] (if D=0)
- g(L, y) for y in [D, U] (if L>0)
- g(x, D) for x in [L, R] (if D>0)

And g for points in the hole is the full rectangle value. g(0,y) and g(x,0) are also full rectangle values? Actually, g(0,y) for y in [D,U] when L=0: (0,y) is in the hole. So g(0,y) is full rectangle value. Similarly g(x,0) for x in [L,R] when D=0: (x,0) is in the hole, so full rectangle value.

So we need to compute:
1. f(x,y) for x < L, and for x in [L,R] with y < D, and for x > R, and for x in [L,R] with y > U. But we only need f on the left and bottom boundaries of the hole.
2. g(x,y) for points in the hole (or on the boundary of the hole when L>0 or D>0). But g on the left boundary (L,y) with y in [D,U] is full rectangle value? Wait, (L,y) is in the hole if L>0? The hole is [L,R]×[D,U]. So if L>0, (L,y) is in the hole. So yes, it's a hole point. Similarly (x,D) is in the hole. So for L>0, g(L,y) is full rectangle value. For D>0, g(x,D) is full rectangle value. For L=0, g(0,y) is full rectangle. For D=0, g(x,0) is full rectangle.

So the only non-trivial part is f on the left and bottom boundaries of the hole. f(x,y) is the number of paths from any allowed start to (x,y) staying in allowed region.

We can compute f(x,y) efficiently. The allowed region is a rectangle minus a hole. The DP for f can be computed by considering the region as a whole. Since the hole is a rectangle, we can derive formulas for f in different parts.

Let's define the allowed region. We can compute f(x,y) for any (x,y) using the principle of inclusion-exclusion or by splitting into cases based on whether the path goes through the hole or not. Actually, f(x,y) is exactly the number of paths from any start to (x,y) in the allowed region. This is the same as the number of paths from any start to (x,y) in the full rectangle minus those that visit the hole. But that seems circular.

Alternatively, we can compute f(x,y) by dynamic programming with a combinatorial formula. The recurrence f(x,y) = 1 + f(x-1,y) + f(x,y-1) for allowed points, with f(-1,y)=f(x,-1)=0. This is a linear recurrence. For a rectangle, the solution is f(x,y) = C(x+y+2, x+1) - something? Actually, for the full rectangle, the solution is exactly C(x+y+2, x+1). For a region with a hole, we can think of f as the sum of contributions from starts in the allowed region.

We can also compute f(x,y) by summing over all start points (i,j) in the allowed region with i≤x, j≤y, the number of paths from (i,j) to (x,y). That is:
f(x,y) = sum_{i=0..x} sum_{j=0..y} [ (i,j) allowed ] * C((x-i)+(y-j), x-i).

So f(x,y) is the sum over allowed start points in the rectangle [0,x]×[0,y] of the binomial coefficient. This is exactly the same as the total number of paths in the allowed region that end at (x,y). This might be easier to compute if we can sum over the allowed region.

But we need f for specific lines: x = L-1, y in [D,U]; and y = D-1, x in [L,R].

Let's try to compute f(x,y) for x < L. For x < L, the entire column x is free (no hole restriction because hole starts at L). So for x ≤ L-1, the allowed region in the rectangle [0,x]×[0,y] is just the full rectangle [0,x]×[0,y] (since the hole is to the right). Therefore, for x ≤ L-1, f(x,y) is exactly the same as in the full rectangle: f(x,y) = C(x+y+2, x+1). But wait: is that true? The hole is at x ≥ L. If x ≤ L-1, then the rectangle [0,x]×[0,y] does not intersect the hole because x < L. So all points in that rectangle are allowed. So indeed, for any y, as long as x ≤ L-1, the set of allowed start points with i≤x, j≤y is the full rectangle. So f(x,y) = sum_{i=0}^x sum_{j=0}^y C((x-i)+(y-j), x-i) = C(x+y+2, x+1). So for x = L-1, f(L-1, y) = C(L-1+y+2, L-1+1) = C(L+y+1, L) for any y. But wait, is this true for all y? What if y is large and the hole covers some y? The start points are only those with i≤L-1 and j≤y. Since i ≤ L-1 < L, no start point can be in the hole. So indeed, the sum is over all start points in [0, L-1]×[0,y], which is a full rectangle. So f(L-1, y) = C((L-1)+y+2, (L-1)+1) = C(L+y+1, L). This is independent of D and U! That's great.

Now, what about f(x, D-1) for x in [L,R]? Here x is in the hole's x-range, but y = D-1 is below the hole. So the point (x, D-1) is below the hole. We need the number of paths from any allowed start to (x, D-1). The allowed starts are points (i,j) with i≤x, j≤D-1, and (i,j) not in the hole. The hole is [L,R]×[D,U]. Since j≤D-1, no point with j≤D-1 can be in the hole. So actually, for y = D-1, the entire row y = D-1 is below the hole, so all points with y ≤ D-1 are allowed. So the allowed region in the rectangle [0,x]×[0,D-1] is the full rectangle! Because the hole only starts at y = D. So for any x, f(x, D-1) = C(x + (D-1) + 2, x+1) = C(x+D+1, x+1). But wait, is that true for x in [L,R]? Yes, because the start points have j ≤ D-1, so they are all below the hole. So they are all allowed. So f(x, D-1) = C(x+D+1, x+1).

So we have:
- f(L-1, y) = C(L+y+1, L) for any y.
- f(x, D-1) = C(x+D+1, x+1) for any x.

But wait: these formulas are for any y and x? Let's check: f(L-1, y) is the number of paths to (L-1, y). The start points are (i,j) with i ≤ L-1, j ≤ y. Since i ≤ L-1, all these start points are left of the hole, so they are allowed. So indeed, f(L-1, y) is just the full rectangle value. Similarly for f(x, D-1): start points with j ≤ D-1 are below the hole, so allowed. So these are full rectangle values.

But is that correct? What if the path from (i,j) to (L-1, y) goes through the hole? The path from (i,j) to (L-1, y) has x-coordinates non-decreasing. Since i ≤ L-1 and the destination is L-1, all x-coordinates in the path are ≤ L-1. So the path never reaches x ≥ L. Thus it never enters the hole. So indeed, the path stays in the allowed region. So the number of such paths is exactly the number of paths in the full rectangle, which is C((L-1-i)+(y-j), L-1-i). Summing over i,j gives the formula. So yes, f(L-1, y) = C(L+y+1, L) for all y. Similarly, f(x, D-1) = C(x+D+1, x+1) for all x.

So we have simple formulas for f on the left and bottom boundaries of the hole.

Now we need g(L, y) for y in [D,U] (if L>0) and g(x, D) for x in [L,R] (if D>0). As argued, these are points inside the hole, so g is the full rectangle value from that point to any end. So:
g(L, y) = sum_{x'=L..W} sum_{y'=y..H} C((x'-L)+(y'-y), x'-L) = C((W-L)+(H-y)+2, W-L+1).
Similarly, g(x, D) = C((W-x)+(H-D)+2, W-x+1).

For L=0, we need g(0, y) for y in [D,U]. g(0,y) = C(W + (H-y) + 2, W+1) = C(W+H-y+2, W+1).
For D=0, g(x,0) = C((W-x)+H+2, W-x+1).

So all the g values are simple full rectangle values from that point to the end.

Now we can compute the invalid paths I.

Let's write I in terms of these.

Case 1: L > 0 and D > 0.
I = sum_{y=D}^U f(L-1, y) * g(L, y) + sum_{x=L}^R f(x, D-1) * g(x, D).

Case 2: L = 0, D > 0.
I = sum_{y=D}^U g(0, y) + sum_{x=0}^R f(x, D-1) * g(x, D). Note: when L=0, the left boundary is x=0. The points (0,y) for y in [D,U] are in the hole. The paths that start at (0,y) are counted by g(0,y) (since f(0,y) is not defined for start? Actually, if L=0, the hole includes x=0. A path that starts at (0,y) is invalid. The number of such paths is 1 (start) * g(0,y) = g(0,y). So we add g(0,y). Also, we need to consider paths that enter the hole from the bottom? The bottom boundary of the hole is y=D, x in [0,R]. The entry points are (x,D). For x in [0,R], the predecessor is (x, D-1). So we sum f(x, D-1)*g(x, D) for x in [0,R]. Note: f(x, D-1) is still the full rectangle value because D-1 < D, so the row is below the hole. So f(x, D-1) = C(x+D+1, x+1). And g(x, D) = C((W-x)+(H-D)+2, W-x+1).

Case 3: L > 0, D = 0.
Symmetric: I = sum_{y=0}^U f(L-1, y) * g(L, y) + sum_{x=L}^W g(x, 0). Note: when D=0, the bottom boundary is y=0. The points (x,0) for x in [L,W] are in the hole. Paths that start at (x,0) are counted by g(x,0). So we add g(x,0). And for the left boundary, we sum f(L-1,y)*g(L,y) for y in [0,U].

Case 4: L = 0, D = 0.
I = sum_{y=0}^U g(0, y) + sum_{x=0}^W g(x, 0). Note: the hole is [0,R]×[0,U]. The allowed region is the big rectangle minus this corner. The invalid paths are those that start in the hole? Actually, if L=0 and D=0, the hole touches the axes. A path can start at any point in the hole? But wait, the hole is [0,R]×[0,U]. The allowed region is the rest. A path that starts at (x,y) with x≤R, y≤U is invalid. The number of such paths is g(x,y) for those points. But also, a path could start outside the hole and enter it. But if L=0 and D=0, the hole is at the bottom-left corner. A path that starts outside the hole (x>R or y>U) and moves left/down? No, it only moves right/up. So if it starts with x>R, it never goes to x≤R. If it starts with y>U, it never goes to y≤U. So the only invalid paths are those that start inside the hole! Because any path starting outside the hole will never enter the hole. Let's verify: Suppose start is (i,j). If i>R, then all future x are ≥i > R, so never in hole. If j>U, then all future y are ≥j > U, so never in hole. If i≤R and j≤U, then start is in hole. So indeed, all invalid paths are exactly those starting in the hole. So I = sum_{x=0}^R sum_{y=0}^U g(x,y). But our formula gave I = sum_{y=0}^U g(0,y) + sum_{x=0}^W g(x,0). That would double count something? Actually, our formula for case L=0, D=0 from the general formula: the left boundary entry: points (0,y) for y in [0,U] with L=0, so we add g(0,y). The bottom boundary entry: points (x,0) for x in [0,W] with D=0. But wait, the bottom boundary of the hole is y=0, x in [0,R]. Not x in [0,W]. So the sum over x should be from L to R, i.e., 0 to R. So it's sum_{x=0}^R g(x,0). So the formula should be: I = sum_{y=0}^U g(0,y) + sum_{x=0}^R g(x,0). But this counts g(0,0) twice? Actually, the left boundary sum includes y=0, so g(0,0) is in the first sum. The bottom boundary sum includes x=0, so g(0,0) is in the second sum. So we would double count g(0,0). But in case 4, the invalid paths are all paths starting in the hole. The number of such paths is sum_{x=0}^R sum_{y=0}^U g(x,y). Our inclusion-exclusion formula for general L>0 and D>0 had no double count because the left and bottom boundary entry points are disjoint except at the corner (L,D). But when L=0 or D=0, the corner is on the axes, and the sets of entry points might overlap? Let's think carefully.

The general formula we derived was:
I = (if L>0: sum_{y=D}^U f(L-1, y) * g(L, y)) + (if L=0: sum_{y=D}^U g(0, y)) + (if D>0: sum_{x=L}^R f(x, D-1) * g(x, D)) + (if D=0: sum_{x=L}^R g(x, 0)).

This assumes that the sets of first entry points are disjoint. For L>0, D>0, they are disjoint because left entry points have x=L, bottom entry points have y=D, and the only common point is (L,D). But at (L,D), the path could have come from left or bottom. However, a path that enters at (L,D) from left is counted in the first sum, and one from bottom in the second sum. They are disjoint because the last step determines which predecessor it came from. So no double count.

For L=0, D>0: The left boundary of the hole is x=0. The entry points are (0,y) for y in [D,U]. These are points where the path could start. The bottom boundary entry points are (x,D) for x in [0,R]. Are these disjoint? The left entry points have x=0, the bottom entry points have y=D. They intersect at (0,D). At (0,D), a path could start at (0,D) (if L=0 and D>0, (0,D) is in the hole) or come from (0, D-1). So the first sum (L=0) gives g(0,y) for y in [D,U]. This counts paths that start at (0,y). The second sum (D>0) gives f(0, D-1)*g(0,D) + sum_{x=1}^R f(x, D-1)*g(x,D). The term for x=0 in the second sum is f(0, D-1)*g(0,D). But a path that starts at (0,D) is also counted in the first sum? No, the first sum is for y in [D,U], so it includes y=D, so it includes g(0,D). So g(0,D) is counted in both the first sum (as a start at (0,D)) and in the second sum (as an entry from below). But are these the same paths? A path that starts at (0,D) is a path that has its first point at (0,D). That path is invalid. A path that enters the hole at (0,D) from (0, D-1) has first point at (0,D-1) (which is allowed) and then moves up to (0,D). That is a different path. So they are disjoint sets. However, in the second sum, when we compute f(0, D-1)*g(0,D), f(0, D-1) includes paths that start at (0, D-1) and paths that start elsewhere. But one of the paths starting at (0, D-1) is the path of length 0 at (0, D-1). Then moving up to (0,D) gives a path that starts at (0, D-1) and goes to (0,D). That path's first hole point is (0,D). That path is not counted in the first sum because the first sum only counts paths that start at (0,y) for y in [D,U]. The path starting at (0, D-1) does not start at (0,D); it starts at (0, D-1). So it's a different path. So there is no double count: the first sum counts paths that start at (0,y); the second sum counts paths that reach (0,D) from below, regardless of start. So they are disjoint. Similarly for other points.

But wait: what about a path that starts at (0, D-1) and goes up to (0,D), and then continues? That path is counted in the second sum as part of f(0, D-1)*g(0,D). It is not counted in the first sum because its start is (0, D-1), not in the hole. So it's correctly counted as an invalid path with first entry at (0,D) from below. So the formula is correct.

Now, for L=0, D=0: The hole is [0,R]×[0,U]. The left boundary is x=0, y in [0,U]. The bottom boundary is y=0, x in [0,R]. They intersect at (0,0). The first sum (L=0) is sum_{y=0}^U g(0,y). The second sum (D=0) is sum_{x=0}^R g(x,0). Now, are these disjoint? The first sum counts paths that start at (0,y) for y in [0,U]. The second sum counts paths that start at (x,0) for x in [0,R]. The path that starts at (0,0) is counted in both! So we double count the paths that start at (0,0). But in case L=0, D=0, the invalid paths are exactly all paths that start in the hole. The set of paths that start at (0,0) is a subset. So if we sum g(0,y) over y in [0,U] and g(x,0) over x in [0,R], we are counting the path starting at (0,0) twice. So the formula as stated would overcount. We need to correct for the double count at the corner when both L=0 and D=0.

In general, when L=0, the left boundary points are (0,y). When D=0, the bottom boundary points are (x,0). The intersection is (0,0). The path starting at (0,0) is counted in both. So we need to subtract g(0,0) once. So for L=0, D=0, the correct I is sum_{y=0}^U g(0,y) + sum_{x=0}^R g(x,0) - g(0,0).

Let's verify with the logic: The first entry point in the hole for a path starting at (0,0) is (0,0) itself. The path is invalid. It should be counted once. In the left boundary sum, we count all paths with first point (0,y). In the bottom boundary sum, we count all paths with first point (x,0). The path starting at (0,0) has first point (0,0), which is both (0,y) and (x,0). So it's counted twice. So we subtract one copy.

What about L=0, D>0? The intersection of the sets is (0,D). The first sum counts paths starting at (0,D). The second sum counts paths entering at (0,D) from below. These are disjoint as argued. So no double count.

Similarly for L>0, D=0: intersection at (L,0). First sum counts paths entering at (L,0) from left. Second sum counts paths starting at (L,0). These are disjoint because one comes from left, one starts there. So no double count.

So the only double count is when both L=0 and D=0, at the corner (0,0). So we can handle that separately.

Thus, the invalid paths I is:
If L>0 and D>0:
I = sum_{y=D}^U C(L+y+1, L) * C(W-L+H-y+2, W-L+1) + sum_{x=L}^R C(x+D+1, x+1) * C(W-x+H-D+2, W-x+1)
If L=0 and D>0:
I = sum_{y=D}^U C(W+H-y+2, W+1) + sum_{x=0}^R C(x+D+1, x+1) * C(W-x+H-D+2, W-x+1)
If L>0 and D=0:
I = sum_{y=0}^U C(L+y+1, L) * C(W-L+H-y+2, W-L+1) + sum_{x=L}^W C(W-x+H+2, W-x+1)  [Note: g(x,0) = C(W-x+H+2, W-x+1)]
If L=0 and D=0:
I = sum_{y=0}^U C(W+H-y+2, W+1) + sum_{x=0}^R C(W-x+H+2, W-x+1) - C(W+H+2, W+1)  [since g(0,0) = C(W+H+2, W+1)]

Wait, in case L=0, D>0, the first sum is sum_{y=D}^U g(0,y) = sum_{y=D}^U C(W+H-y+2, W+1). That's correct.
In case L>0, D=0, the second sum is sum_{x=L}^W g(x,0) = sum_{x=L}^W C(W-x+H+2, W-x+1). That's correct.

Now, we also need to consider the total paths in the full rectangle: T = sum_{x=0}^W sum_{y=0}^H C(x+y+2, x+1). This can be computed as C(W+H+4, W+2) - 1? Let's check. There is a known identity: sum_{x=0}^W sum_{y=0}^H C(x+y, x) = C(W+H+2, W+1) - 1. But here we have C(x+y+2, x+1). Let's derive.

We want S = sum_{x=0}^W sum_{y=0}^H C(x+y+2, x+1).
Let u = x+1, v = y+1. Then u from 1 to W+1, v from 1 to H+1. C(u+v-1, u)?? Actually, x+y+2 = (x+1)+(y+1) = u+v. So C(u+v, u) with u from 1..W+1, v from 1..H+1. The sum over u=1..W+1, v=1..H+1 of C(u+v, u). There is a known identity: sum_{u=1}^m sum_{v=1}^n C(u+v, u) = C(m+n+2, m+1) - 1? Let's test small values. W=0, H=0: sum_{x=0}^0 sum_{y=0}^0 C(x+y+2, x+1) = C(2,1)=2. C(0+0+2, 0+1) - 1 = C(2,1)-1=1. Not 2. So maybe it's C(W+H+4, W+2) - something.
Let's compute: sum_{u=1}^m sum_{v=1}^n C(u+v, u) = C(m+n+2, m+1) - (m+1)(n+1)? Not sure.
Alternatively, we can use the identity: C(u+v, u) = C(u+v+1, u+1) - C(u+v, u+1). Then sum telescopes. Or we can use the fact that sum_{u=0}^m sum_{v=0}^n C(u+v, u) = C(m+n+2, m+1) - 1. Our sum is from u=1 to m, v=1 to n of C(u+v, u). We can write it as (sum_{u=0}^m sum_{v=0}^n) - (sum_{u=0}^m C(u, u)) - (sum_{v=0}^n C(v, 0)) + C(0,0). That is C(m+n+2, m+1) - 1 - (m+1) - (n+1) + 1 = C(m+n+2, m+1) - m - n - 1. But wait, check: sum_{u=0}^m sum_{v=0}^n C(u+v, u) = C(m+n+2, m+1) - 1. Then subtract the u=0 row: sum_{v=0}^n C(v, 0) = n+1. Subtract the v=0 column: sum_{u=0}^m C(u, u) = m+1. But we subtracted the (0,0) term twice, so add back 1. So total = C(m+n+2, m+1) - 1 - (n+1) - (m+1) + 1 = C(m+n+2, m+1) - m - n - 1. For m=W+1, n=H+1, this is C(W+H+4, W+2) - (W+1) - (H+1) - 1 = C(W+H+4, W+2) - W - H - 3. Let's test with W=0, H=0: m=1, n=1. C(1+1+2, 1+1)=C(4,2)=6. Then 6 - 0 - 0 - 3 = 3. But we computed sum = 2. So that's wrong.
Let's recompute carefully.
We want S = sum_{x=0}^W sum_{y=0}^H C(x+y+2, x+1).
Let i = x+1, j = y+1. Then i=1..W+1, j=1..H+1. Term is C(i+j, i).
We know that sum_{i=0}^W sum_{j=0}^H C(i+j, i) = C(W+H+2, W+1) - 1. (This is a standard identity: number of paths in a rectangle not touching the top-right? Actually, sum_{i=0}^W sum_{j=0}^H C(i+j, i) = C(W+H+2, W+1) - 1. Let's verify: W=0,H=0: sum=1, C(2,1)-1=1. Correct.)
Now, S = sum_{i=1}^{W+1} sum_{j=1}^{H+1} C(i+j, i) = (sum_{i=0}^{W+1} sum_{j=0}^{H+1}) - (sum_{i=0}^{W+1} C(i, i)) - (sum_{j=0}^{H+1} C(j, 0)) + C(0,0).
But careful: the full sum in the identity is for indices 0 to W, 0 to H. Here we have up to W+1 and H+1. So we can use the identity with m=W+1, n=H+1:
sum_{i=0}^{W+1} sum_{j=0}^{H+1} C(i+j, i) = C((W+1)+(H+1)+2, W+2) - 1 = C(W+H+4, W+2) - 1.
Now subtract the i=0 row: sum_{j=0}^{H+1} C(j, 0) = H+2.
Subtract the j=0 column: sum_{i=0}^{W+1} C(i, i) = W+2.
Add back (0,0): C(0,0)=1.
So S = [C(W+H+4, W+2) - 1] - (H+2) - (W+2) + 1 = C(W+H+4, W+2) - W - H - 3.
Test with W=0, H=0: C(4,2)=6, minus 0-0-3=3. But actual S for W=0,H=0: only x=0,y=0: C(2,1)=2. So 6-3=3, not 2. So error.
Let's compute manually for W=0, H=0: x in {0}, y in {0}. C(0+0+2, 0+1)=C(2,1)=2. So S=2.
For W=0, H=1: x=0, y=0,1. C(2,1)=2, C(3,1)=3, sum=5.
Now formula: C(0+1+4, 0+2)=C(5,2)=10. Minus 0-1-3 = 6. 10-6=4, not 5.
So the identity is off by something. Let's re-derive the identity for sum_{i=0}^m sum_{j=0}^n C(i+j, i).
We know that C(i+j, i) = C(i+j+1, i+1) - C(i+j, i+1). This is a standard telescoping sum. Actually, sum_{i=0}^m C(i+j, i) = C(m+j+1, m) (hockey-stick). So sum_{i=0}^m sum_{j=0}^n C(i+j, i) = sum_{j=0}^n C(m+j+1, m). And sum_{j=0}^n C(m+j+1, m) = C(m+n+2, m+1) - 1? Let's check: hockey-stick: sum_{k=0}^n C(r+k, k) = C(r+n+1, n). Here we have sum_{j=0}^n C(m+j+1, m). Let k = m+j+1, then when j=0, k=m+1; j=n, k=m+n+1. So sum = sum_{k=m+1}^{m+n+1} C(k, m) = C(m+n+2, m+1) - C(m+1, m+1) = C(m+n+2, m+1) - 1. Yes, that's correct. So sum_{i=0}^m sum_{j=0}^n C(i+j, i) = C(m+n+2, m+1) - 1.
Now for our S: i from 1 to W+1, j from 1 to H+1. Let's set m = W+1, n = H+1. Then sum_{i=0}^{W+1} sum_{j=0}^{H+1} C(i+j, i) = C(W+H+4, W+2) - 1.
Now we want sum_{i=1}^{W+1} sum_{j=1}^{H+1} = full sum - sum_{i=0} (j=0) - sum_{j=0} (i=0) + (0,0).
The i=0 terms: j from 0 to H+1: C(j, 0) = 1. There are H+2 terms. So sum = H+2.
The j=0 terms: i from 0 to W+1: C(i, i) = 1. There are W+2 terms. So sum = W+2.
The (0,0) term is 1.
So S = [C(W+H+4, W+2) - 1] - (H+2) - (W+2) + 1 = C(W+H+4, W+2) - W - H - 3.
But for W=0, H=0: m=1, n=1. Full sum = C(0+0+4, 0+2) - 1 = C(4,2)-1=6-1=5. Then subtract i=0: j=0,1: C(0,0)=1, C(1,0)=1, sum=2. Subtract j=0: i=0,1: C(0,0)=1, C(1,1)=1, sum=2. Add (0,0):1. So S = 5 - 2 - 2 + 1 = 2. That works! I earlier mistakenly used C(W+H+4, W+2) - 1 as 5, but then subtracted W+H+3 = 0+0+3=3, giving 2? Wait, 5 - 3 = 2. So C(4,2)=6, 6-1=5, 5-3=2. So the formula C(W+H+4, W+2) - W - H - 3 is correct. I miscalculated C(4,2) as 6, but 6-1=5, 5-3=2. So it's correct. Let's test W=0, H=1: C(0+1+4, 0+2)=C(5,2)=10. Then 10 - 0 - 1 - 3 = 6. But actual S=5. So 10-1- (H+2)=10-1-3=6? Wait, for W=0, H=1: m=1, n=2. Full sum = C(0+1+4, 0+2) - 1 = C(5,2)-1=10-1=9. i=0: j=0,1,2: C(j,0)=1,1,1 sum=3. j=0: i=0,1: C(i,i)=1,1 sum=2. (0,0)=1. So S = 9 - 3 - 2 + 1 = 5. Now formula: C(W+H+4, W+2) - W - H - 3 = C(5,2) - 0 - 1 - 3 = 10 - 4 = 6. So the formula gave 6, but actual is 5. So the formula C(W+H+4, W+2) - W - H - 3 is not correct for W=0, H=1. Why? Because when we did the subtraction, we assumed the full sum is C(W+H+4, W+2) - 1. For W=0, H=1, that is C(5,2)-1=9. Then we subtracted (H+2) = 3, (W+2)=2, added 1. So 9-3-2+1=5. But my simplified expression was C(W+H+4, W+2) - W - H - 3. For W=0,H=1: C(5,2)=10, minus 0 -1 -3 = 6. That's because I incorrectly simplified: [C - 1] - (H+2) - (W+2) + 1 = C - 1 - H - 2 - W - 2 + 1 = C - W - H - 3. But wait, 1+2+2-1 = 4, so C - 4? Actually: -1 - (H+2) - (W+2) + 1 = -1 -H -2 -W -2 +1 = -W -H -4. So it should be C - W - H - 4. Let's recompute: Full sum = C(m+n+2, m+1) - 1. Here m=W+1, n=H+1, so C(W+H+4, W+2) - 1.
Subtract i=0: sum_{j=0}^{H+1} C(j, 0) = H+2.
Subtract j=0: sum_{i=0}^{W+1} C(i, i) = W+2.
Add (0,0): 1.
So S = [C(W+H+4, W+2) - 1] - (H+2) - (W+2) + 1 = C(W+H+4, W+2) - 1 - H - 2 - W - 2 + 1 = C(W+H+4, W+2) - W - H - 4.
Check W=0,H=0: C(4,2)=6, -0-0-4=2. Correct.
W=0,H=1: C(5,2)=10, -0-1-4=5. Correct.
W=1,H=0: C(5,2)=10, -1-0-4=5. Correct.
W=1,H=1: x=0,1; y=0,1. C(2,1)=2, C(3,1)=3, C(3,2)=3, C(4,2)=6. Sum=2+3+3+6=14. Formula: C(1+1+4, 1+2)=C(6,3)=20. 20 - 1 -1 -4 = 14. Correct.
So T = S = C(W+H+4, W+2) - W - H - 4.

Wait, is that the total number of paths in the full rectangle? Let's test with W=1, H=1. The full rectangle has points (0,0), (0,1), (1,0), (1,1). Total paths: each point can be start, each path is a sequence. The number of paths: start (0,0): can go to (0,1) or (1,0) or (1,1) via two paths? Actually, from (0,0), possible paths: length 0: 1; to (0,1): 1; to (1,0): 1; to (1,1): 2 (via (0,1) or (1,0)). So 5 paths from (0,0). Start (0,1): paths: length 0:1; to (1,1):1. Total 2. Start (1,0): length 0:1; to (1,1):1. Total 2. Start (1,1): length 0:1. Total 1. Sum = 5+2+2+1=10. But our T formula gave 14. So there is a discrepancy. Let's recount the paths in the full rectangle for W=1, H=1. The allowed region is all 4 points. The paths are sequences of adjacent points moving right/up. Let's list all paths:
- Length 0: (0,0), (0,1), (1,0), (1,1) -> 4 paths.
- Length 1: (0,0)->(0,1), (0,0)->(1,0), (0,1)->(1,1), (1,0)->(1,1) -> 4 paths.
- Length 2: (0,0)->(0,1)->(1,1), (0,0)->(1,0)->(1,1) -> 2 paths.
Total = 10. So T=10.
Our formula gave 14. So the formula is wrong. Let's find the correct T.
We want sum_{x=0}^W sum_{y=0}^H f_full(x,y) where f_full(x,y) is the number of paths from any start to (x,y) in full rectangle. We know f_full(x,y) = C(x+y+2, x+1). So T = sum_{x=0}^W sum_{y=0}^H C(x+y+2, x+1). For W=1, H=1: sum = C(2,1)+C(3,1)+C(3,2)+C(4,2) = 2+3+3+6=14. But we counted 10 paths. So there is a mistake in the interpretation of f_full(x,y). Let's recompute f_full(x,y) for the full rectangle.
f_full(x,y) = number of paths from any start to