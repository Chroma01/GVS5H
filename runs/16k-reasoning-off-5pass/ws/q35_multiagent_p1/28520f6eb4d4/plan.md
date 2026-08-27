1. **Sort and Filter**: Sort buildings by coordinate. Since we are at x=0, we only care about buildings with X_i > 0. The problem states X_i are positive and sorted, so we can use them directly.
2. **Visibility Condition**: A building `j` is visible from `(0, h)` if there is no building `k` (with `X_k < X_j`) that blocks the line of sight. Specifically, for building `j` to be visible, the line segment from `(0, h)` to any point on building `j` (specifically the top `(X_j, H_j)` is the hardest to see if blocked, but actually we need *any* point. However, if the top is blocked, a lower point might be visible. But wait, if the top is blocked by a building `k`, the line from `(0,h)` to `(X_j, H_j)` passes above `(X_k, H_k)`? No, it passes below or through.
   Actually, the condition "building i is visible if there exists a point Q on building i such that PQ does not intersect any other building" simplifies. The "hardest" point to see on building `j` is the top if we are looking from below, but here we are at height `h`.
   Let's rephrase: Building `j` is *blocked* if for ALL points `Q` on building `j` (i.e., `(X_j, y)` for `0 <= y <= H_j`), the segment `PQ` intersects some other building.
   The segment from `(0,h)` to `(X_j, y)` has slope `(y-h)/X_j`.
   A building `k` (`X_k < X_j`) blocks the view to `(X_j, y)` if the line passes through or below the top of building `k`? No, it intersects the building `k`. Building `k` occupies `x \in [X_k, X_k]` (negligible width) and `y \in [0, H_k]`.
   The line from `(0,h)` to `(X_j, y)` at `x=X_k` has height `y_k = h + (y-h) * (X_k / X_j)`.
   If `0 <= y_k <= H_k`, then the line intersects building `k`.
   So, building `j` is visible if there exists a `y \in [0, H_j]` such that for all `k < j`, either `y_k < 0` or `y_k > H_k`.
   
   This is complex. Let's look at the "maximum height from which it is NOT possible to see ALL buildings".
   This is equivalent to finding the maximum `h` such that there is at least one building `j` that is NOT visible.
   Building `j` is NOT visible if for all `y \in [0, H_j]`, there exists some `k < j` that blocks it.
   
   Let's consider the "line of sight" from `(0,h)`. The buildings cast shadows.
   Actually, a simpler geometric interpretation:
   Building `j` is visible if the segment from `(0,h)` to `(X_j, H_j)` is not blocked? No, because a lower point might be visible.
   However, note that if the top `(X_j, H_j)` is visible, then building `j` is visible.
   If the top is blocked, is it possible that a lower point is visible?
   If the top is blocked by building `k`, it means the line from `(0,h)` to `(X_j, H_j)` passes through building `k`.
   The line equation at `X_k` is `Y = h + (H_j - h) * (X_k / X_j)`.
   If `Y <= H_k`, it might be blocked.
   
   Let's use the property: The set of visible buildings from `(0,h)` are those that are "upper envelope" candidates.
   Actually, we can binary search on `h`. For a fixed `h`, can we check if all buildings are visible?
   To check if building `j` is visible from `(0,h)`:
   We need to know if there is any `y \in [0, H_j]` such that the line to `(X_j, y)` is clear.
   The "clearest" point is usually the top, unless the top is blocked by a building that is very tall but narrow? No, buildings are lines.
   If the line to the top is blocked by building `k` (i.e., the intersection height at `X_k` is `<= H_k`), then any point lower than the top on building `j` will have an even lower intersection height at `X_k` (since the slope is less steep or more negative).
   Wait, if `h < H_j`, the slope is positive. Lower `y` means lower slope.
   If `h > H_j`, the slope is negative. Lower `y` means steeper negative slope (more negative).
   
   Let's analyze the blocking condition for a specific `j`.
   Building `j` is blocked if for every `y \in [0, H_j]`, there is a `k < j` such that the line intersects building `k`.
   This happens if the "shadow" of all previous buildings covers the entire vertical span of building `j`.
   
   Alternatively, we can compute the "minimum height required to see building `j`".
   Let `min_h(j)` be the minimum height `h` at `(0,h)` such that building `j` becomes visible.
   If we can compute `min_h(j)` for all `j`, then the answer is `max_j (min_h(j))`.
   Why? If we are at height `H = max_j (min_h(j))`, then for the building `j*` that achieves the maximum, we are at exactly `min_h(j*)`, so it is just visible (or barely visible). If we go slightly higher, it becomes visible. If we go lower, it is not visible.
   Wait, the question asks for the maximum height from which it is NOT possible to see ALL buildings.
   If we are at height `h`, we see all buildings if `h >= min_h(j)` for all `j`.
   So we fail to see all buildings if there exists some `j` such that `h < min_h(j)`.
   The maximum such `h` is `max_j (min_h(j)) - epsilon`.
   So the answer is `max_j (min_h(j))`.
   If `max_j (min_h(j)) <= 0`, then at height 0 we see all buildings (since `min_h` is non-negative? No, `min_h` could be negative? No, height must be non-negative. If `min_h(j) <= 0`, it means building `j` is visible at height 0. If all `min_h(j) <= 0`, answer is -1).
   
   So the core problem is: Calculate `min_h(j)` for each building `j`.
   Building `j` is visible from `(0,h)` if there exists `y \in [0, H_j]` such that for all `k < j`, the line from `(0,h)` to `(X_j, y)` does not intersect building `k`.
   Intersection with building `k` at `X_k`:
   Line height at `X_k`: `L_k(y, h) = h + (y - h) * (X_k / X_j)`.
   Blocked by `k` if `0 <= L_k(y, h) <= H_k`.
   
   We want to find the minimum `h >= 0` such that there exists `y \in [0, H_j]` where for all `k < j`, `L_k(y, h) < 0` OR `L_k(y, h) > H_k`.
   
   Let's fix `j`. We want to minimize `h`.
   Consider the constraints imposed by each `k < j`.
   For a fixed `k`, the condition "not blocked by `k`" means:
   `h + (y - h) * (X_k / X_j) < 0`  OR  `h + (y - h) * (X_k / X_j) > H_k`.
   
   Let `r_k = X_k / X_j`. Note `0 < r_k < 1`.
   Condition: `h(1 - r_k) + y r_k < 0`  OR  `h(1 - r_k) + y r_k > H_k`.
   
   We need to find `h, y` satisfying this for ALL `k < j`, with `0 <= y <= H_j` and `h >= 0`.
   We want to minimize `h`.
   
   Let's analyze the two cases for each `k`:
   Case 1: `h(1 - r_k) + y r_k < 0`.
   Since `h >= 0, y >= 0, r_k > 0, 1-r_k > 0`, the LHS is non-negative. So this case is impossible unless `h=y=0` and we allow `<0`? No, strictly less. So Case 1 is never satisfied for `h,y >= 0`.
   Wait, if `h=0, y=0`, LHS=0. Not `<0`.
   So we must always satisfy Case 2: `h(1 - r_k) + y r_k > H_k`.
   
   So, building `j` is visible from `(0,h)` if there exists `y \in [0, H_j]` such that for all `k < j`:
   `h(1 - r_k) + y r_k > H_k`.
   
   This inequality can be rewritten as:
   `h(1 - r_k) > H_k - y r_k`
   `h > (H_k - y r_k) / (1 - r_k)`
   
   Let `f_k(y) = (H_k - y r_k) / (1 - r_k)`.
   We need `h > f_k(y)` for all `k < j`.
   So `h > max_{k < j} f_k(y)`.
   To minimize `h`, we should choose `y \in [0, H_j]` to minimize `max_{k < j} f_k(y)`.
   Let `G_j(y) = max_{k < j} f_k(y)`.
   We want `min_{y \in [0, H_j]} G_j(y)`.
   Then `min_h(j) = min_{y \in [0, H_j]} G_j(y)`.
   
   Note: `f_k(y)` is a linear function of `y` with negative slope `-r_k / (1 - r_k)`.
   `G_j(y)` is the upper envelope of a set of lines with negative slopes.
   The upper envelope of lines with negative slopes is a convex function?
   Each line has slope `m_k = -r_k / (1 - r_k)`. Since `r_k` increases with `X_k`, `m_k` becomes more negative as `k` increases (for larger `X_k`).
   So lines with larger `X_k` (larger `r_k`) have steeper negative slopes.
   
   We want to minimize the upper envelope of these lines over `y \in [0, H_j]`.
   The minimum of the upper envelope of lines occurs at the "bottom" of the convex hull.
   Since all slopes are negative, the function `G_j(y)` is decreasing?
   Not necessarily. The upper envelope of decreasing functions is decreasing.
   Proof: If `f_1` and `f_2` are decreasing, `max(f_1, f_2)` is decreasing.
   So `G_j(y)` is a decreasing function of `y`.
   Therefore, the minimum of `G_j(y)` on `[0, H_j]` occurs at `y = H_j`.
   
   So, `min_h(j) = G_j(H_j) = max_{k < j} f_k(H_j)`.
   `f_k(H_j) = (H_k - H_j * r_k) / (1 - r_k)`.
   `r_k = X_k / X_j`.
   `1 - r_k = (X_j - X_k) / X_j`.
   `f_k(H_j) = (H_k - H_j * (X_k / X_j)) / ((X_j - X_k) / X_j)`
   `= (H_k * X_j - H_j * X_k) / (X_j - X_k)`.
   
   So, `min_h(j) = max_{k < j} [ (H_k * X_j - H_j * X_k) / (X_j - X_k) ]`.
   
   If this value is negative, it means even at `h=0`, the condition `h > ...` is satisfied?
   Wait, if `max f_k(H_j) < 0`, then `h=0` satisfies `h > f_k(H_j)` for all `k`.
   So `min_h(j) = 0` (since height must be non-negative).
   Actually, if the calculated max is negative, it means building `j` is visible at height 0.
   So `min_h(j) = max(0, max_{k < j} ... )`.
   
   Algorithm:
   1. Initialize `ans = 0`.
   2. For each building `j` from 1 to N:
      Compute `val_j = max_{k < j} ( (H_k * X_j - H_j * X_k) / (X_j - X_k) )`.
      If no `k < j` exists (i.e., j=1), `val_j = -infinity` (so `min_h(1) = 0`).
      `min_h(j) = max(0, val_j)`.
      `ans = max(ans, min_h(j))`.
   3. If `ans == 0`, check if it's possible to see all at height 0.
      If `ans > 0`, output `ans`.
      If `ans == 0`, it means for all `j`, `min_h(j) == 0`. This implies all buildings are visible at height 0. Output -1.
      
   Wait, Sample 3:
   1 1
   2 2
   3 3
   j=1: min_h=0.
   j=2: k=1. `(1*2 - 2*1)/(2-1) = 0`. min_h(2)=0.
   j=3: k=1: `(1*3 - 3*1)/(3-1) = 0`. k=2: `(2*3 - 3*2)/(3-2) = 0`. min_h(3)=0.
   Ans = 0. Output 0. Correct.
   
   Sample 1:
   3 2
   5 4
   7 5
   j=1 (3,2): min_h=0.
   j=2 (5,4): k=1. `(2*5 - 4*3)/(5-3) = (10-12)/2 = -1`. min_h(2)=0.
   j=3 (7,5): 
     k=1: `(2*7 - 5*3)/(7-3) = (14-15)/4 = -0.25`.
     k=2: `(4*7 - 5*5)/(7-5) = (28-25)/2 = 1.5`.
     max = 1.5. min_h(3)=1.5.
   Ans = 1.5. Correct.
   
   Complexity: O(N^2) if we iterate all k for each j. N=2e5, so we need O(N log N) or O(N).
   
   We need to compute `max_{k < j} ( (H_k X_j - H_j X_k) / (X_j - X_k) )`.
   Let `A_k = H_k`, `B_k = X_k`.
   Term: `(A_k X_j - H_j B_k) / (X_j - B_k)`.
   
   This looks like finding the maximum slope or something related to convex hull.
   Rewrite: `(A_k X_j - H_j B_k) / (X_j - B_k) = (A_k X_j - A_k B_k + A_k B_k - H_j B_k) / (X_j - B_k)`
   `= A_k + (A_k - H_j) B_k / (X_j - B_k)`.
   
   Let's interpret geometrically.
   We are looking for the "highest" line from `(0, h)` to `(X_j, H_j)` that clears all previous buildings.
   The condition `h > (H_k X_j - H_j X_k) / (X_j - X_k)` defines a half-plane for `h` given `H_j`.
   
   Actually, this is equivalent to:
   Consider the point `(X_j, H_j)`. We want to find the minimum `h` such that the line from `(0,h)` to `(X_j, H_j)` is above all `(X_k, H_k)`.
   Wait, earlier I derived that we only need to check the top of building `j`.
   And the condition for building `k` to NOT block the top of `j` is `h > (H_k X_j - H_j X_k) / (X_j - X_k)`.
   
   So `min_h(j)` is determined by the "tightest" constraint from any `k < j`.
   
   To compute this efficiently:
   We maintain a convex hull of the "blocking" lines?
   The expression `(H_k X_j - H_j X_k) / (X_j - X_k)` can be viewed as the y-intercept of the line passing through `(X_k, H_k)` and `(X_j, H_j)` extended to `x=0`?
   Line through `(X_k, H_k)` and `(X_j, H_j)`:
   Slope `m = (H_j - H_k) / (X_j - X_k)`.
   Eq: `y - H_k = m (x - X_k)`.
   At `x=0`: `y = H_k - m X_k = H_k - (H_j - H_k) X_k / (X_j - X_k)`
   `= (H_k (X_j - X_k) - (H_j - H_k) X_k) / (X_j - X_k)`
   `= (H_k X_j - H_k X_k - H_j X_k + H_k X_k) / (X_j - X_k)`
   `= (H_k X_j - H_j X_k) / (X_j - X_k)`.
   
   Yes! `f_k(H_j)` is exactly the y-intercept of the line connecting `(X_k, H_k)` and `(X_j, H_j)`.
   
   So `min_h(j)` is the maximum y-intercept of the lines connecting `(X_j, H_j)` to any previous `(X_k, H_k)`.
   
   We want `max_{k < j} (y-intercept of line k-j)`.
   
   This is equivalent to finding the line from `(X_j, H_j)` to some `(X_k, H_k)` (`k<j`) that has the largest y-intercept.
   Geometrically, if we draw lines from `(X_j, H_j)` to all previous points, the one with the largest y-intercept is the one that is "most counter-clockwise" from the vertical?
   Actually, consider the set of points `(X_k, H_k)`. We want the line from `(X_j, H_j)` to a point in this set that maximizes the intercept.
   This is equivalent to finding the point `(X_k, H_k)` that maximizes the slope of the line from `(0, y_int)` to `(X_j, H_j)`? No.
   
   Let's use the property of the Upper Convex Hull.
   The maximum y-intercept from `(X_j, H_j)` to any previous point will be achieved by a point on the upper convex hull of the previous points.
   Specifically, if we maintain the upper convex hull of points `(X_1, H_1), ..., (X_{j-1})`, the optimal `k` will be on this hull.
   Furthermore, since `X_k < X_j`, we are looking for the tangent from `(X_j, H_j)` to the upper convex hull.
   Wait, we want to MAXIMIZE the intercept.
   The line with the largest intercept is the one that is "highest" at x=0.
   This corresponds to the line from `(X_j, H_j)` that is tangent to the upper convex hull from the "right" side?
   
   Actually, for a fixed `(X_j, H_j)`, the function `g(k) = y-intercept(k, j)` is unimodal with respect to the position on the convex hull?
   We can use binary search (ternary search) on the convex hull to find the maximum.
   Or, since we process `j` in increasing order, we can maintain the hull and use a pointer.
   
   The upper convex hull of points `(X_k, H_k)` can be maintained in O(N) total time using a stack (monotonic chain).
   For each new point `(X_j, H_j)`, we first query the hull to find the max intercept, then add `(X_j, H_j)` to the hull.
   
   Query: Given a convex hull (list of points sorted by X), find `k` on the hull that maximizes the y-intercept of the line connecting `(X_k, H_k)` and `(X_j, H_j)`.
   The y-intercept is `H_k - slope * X_k`.
   Slope `m = (H_j - H_k) / (X_j - X_k)`.
   Intercept `I = H_k - (H_j - H_k) X_k / (X_j - X_k)`.
   
   This is equivalent to finding the point on the hull that maximizes the angle?
   Actually, this is a standard problem: "Given a convex polygon and a point outside, find the tangent".
   Here we want the tangent that maximizes the intercept.
   Since the hull is upper, and we are to the right, the "upper" tangent from `(X_j, H_j)` to the hull will give the maximum intercept?
   Let's check.
   If we draw a line from `(X_j, H_j)` to the hull, the one that is "most steep" upwards to the left will have the highest intercept.
   This is the upper tangent.
   
   We can find this tangent using binary search on the hull vertices.
   The slope of the line from `(X_j, H_j)` to `(X_k, H_k)` is `m_k`.
   We want to maximize `H_k - m_k X_k`.
   
   Alternatively, note that the optimal `k` is such that the line `(k, j)` is above all other points on the hull? No, it's a tangent.
   The upper tangent from `(X_j, H_j)` to the upper convex hull of `1..j-1`.
   
   Algorithm:
   1. Maintain an upper convex hull of points processed so far.
   2. For each `j`:
      a. Find the vertex `k` on the hull that maximizes the y-intercept of the line `(k, j)`. This is the upper tangent point.
      b. Compute `min_h(j) = max(0, intercept)`.
      c. Update global answer.
      d. Add `(X_j, H_j)` to the hull (maintaining convexity).
      
   Finding the tangent:
   The slope of the tangent from `(X_j, H_j)` to the hull decreases as we move along the hull?
   We can use binary search. The hull is convex. The function "intercept" is unimodal.
   
   Implementation details:
   - Hull stored as list of points.
   - Binary search for the peak.