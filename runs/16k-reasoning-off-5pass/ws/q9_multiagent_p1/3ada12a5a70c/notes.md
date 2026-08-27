
## ideation
**Core Difficulty**: The problem is a "maximize the minimum" optimization problem. The standard technique for this is **Binary Search on the Answer**. The challenge lies in efficiently verifying if a specific minimum distance `d` is feasible (i.e., can we select `k` points such that all pairwise Manhattan distances are $\ge d$).

**Candidate Approaches**:
1.  **Binary Search + Greedy Verification**:
    *   **Range**: Low = 1, High = $2 \times \text{side}$ (max possible Manhattan distance on boundary).
    *   **Check Function (`can_select(d)`)**:
        *   Since points are on the boundary, we can "unfold" the square perimeter into a 1D line of length $4 \times \text{side}$.
        *   Map each point $(x, y)$ to a 1D coordinate based on which side of the square it lies on.
        *   Sort the points by this 1D coordinate.
        *   **Crucial Detail**: The perimeter is a cycle. A point near the end of the unfolded line might be close to a point near the beginning (wrap-around). However, since we need to select $k$ points ($k \le 25$) and the total number of points is up to $15,000$, a simple linear scan on the unfolded array might miss the wrap-around case if the optimal set wraps around the corner.
        *   *Correction*: Instead of complex cycle handling, since $k$ is very small, we can try all possible starting points in the sorted list. For each starting point $i$, greedily pick the next point $j > i$ such that $dist(points[i], points[j]) \ge d$. If we successfully pick $k$ points starting from $i$, return True. If no starting point works, return False.
        *   *Optimization*: The greedy strategy on a line works perfectly. For a cycle, duplicating the list (appending points $0$ to $n-1$ again with offset $4 \times \text{side}$) allows us to treat it as a line of length $2n$. We just need to ensure we don't pick more than $k$ points and that the selection doesn't exceed the logical bounds if we were strictly limited by perimeter distance, but here the metric is Manhattan, not perimeter distance. Wait, **Manhattan distance on the boundary is NOT the same as perimeter distance**.
        *   **Re-evaluating Metric**:
            *   Points are on the boundary: $x=0, x=side, y=0, y=side$.
            *   Manhattan distance $|x_1-x_2| + |y_1-y_2|$.
            *   If two points are on the same side, distance is $|x_1-x_2|$.
            *   If on adjacent sides (e.g., top and right), distance is $(side - x_1) + (side - y_2)$? No.
                *   Example: $(0, side)$ and $(side, side)$. Dist = $side$.
                *   Example: $(0, side)$ and $(side, 0)$. Dist = $side + side = 2 \times side$.
                *   Example: $(0, y_1)$ and $(x_2, side)$. Dist = $x_2 + (side - y_1)$.
            *   Actually, for points on the boundary, the Manhattan distance is exactly the distance along the perimeter **if** we traverse the perimeter in a specific direction (e.g., clockwise) and the points are not "crossing" the corner in a way that creates a shortcut.
            *   Let's verify: Point A on Left edge $(0, y_a)$, Point B on Right edge $(x_b, side)$.
                *   Perimeter path: $(0, y_a) \to (0,0) \to (x_b, 0) \to (x_b, side)$. Length: $y_a + x_b + side$.
                *   Manhattan: $|0-x_b| + |y_a-side| = x_b + (side-y_a)$.
                *   These are different! The perimeter distance goes through $(0,0)$, Manhattan goes through $(x_b, y_a)$? No, Manhattan is $L_1$.
                *   Wait, $|x_1-x_2| + |y_1-y_2|$.
                *   If A=$(0, y_a)$ and B=$(x_b, side)$, $dist = x_b + side - y_a$.
                *   Perimeter distance (clockwise from A): $(y_a - 0) + (side - 0) + x_b$? No.
                *   Let's map to perimeter coordinate $P$.
                    *   Bottom: $(x, 0) \to P = x$.
                    *   Right: $(side, y) \to P = side + y$.
                    *   Top: $(x, side) \to P = 2 \times side + (side - x)$.
                    *   Left: $(0, y) \to P = 3 \times side + (side - y)$.
                *   Check A=$(0, y_a)$ (Left, $P_A = 3s + s - y_a = 4s - y_a$) and B=$(x_b, side)$ (Top, $P_B = 2s + s - x_b = 3s - x_b$).
                *   Perimeter diff: $|P_A - P_B| = |4s - y_a - (3s - x_b)| = |s - y_a + x_b|$.
                *   Manhattan: $x_b + (s - y_a)$.
                *   They match!
                *   Check A=$(0, y_a)$ (Left) and B=$(x_b, 0)$ (Bottom).
                    *   $P_A = 4s - y_a$, $P_B = x_b$.
                    *   Perimeter diff (shortest arc?): The points are on adjacent sides. The perimeter distance along the boundary is $y_a + x_b$.
                    *   Manhattan: $x_b + y_a$. Match.
                *   Check A=$(0, y_a)$ (Left) and B=$(side, y_b)$ (Right).
                    *   $P_A = 4s - y_a$, $P_B = s + y_b$.
                    *   Perimeter distance (one way): $(4s - y_a) - (s + y_b) = 3s - y_a - y_b$.
                    *   Perimeter distance (other way): $(s+y_b) + s + (4s-y_a)$? No. Total perimeter $4s$. Other way is $4s - (3s - y_a - y_b) = s + y_a + y_b$.
                    *   Manhattan: $|0 - side| + |y_a - y_b| = s + |y_a - y_b|$.
                    *   Does $s + |y_a - y_b|$ equal $s + y_a + y_b$? Only if one is 0? No.
                    *   Example: $s=10, A=(0, 5), B=(10, 5)$.
                        *   Manhattan: $10 + 0 = 10$.
                        *   Perimeter path 1: $(0,5) \to (0,0) \to (10,0) \to (10,5)$. Len: $5+10+5=20$.
                        *   Perimeter path 2: $(0,5) \to (0,10) \to (10,10) \to (10,5)$. Len: $5+10+5=20$.
                        *   Wait, Manhattan is 10, Perimeter is 20. They are **NOT** the same.
            *   **Conclusion**: Manhattan distance on the boundary is **not** simply the perimeter distance. We must calculate the actual Manhattan distance $|x_1-x_2| + |y_1-y_2|$ for any pair.

2.  **Refined Check Function**:
    *   Since $k$ is small ($k \le 25$), but $N$ is up to $15,000$, an $O(N^2)$ check inside binary search is too slow ($15000^2 \approx 2.25 \times 10^8$, times $\log(2 \cdot 10^9) \approx 31$ is too much).
    *   We need an efficient check.
    *   **Strategy**:
        1.  Sort points by some heuristic (e.g., perimeter coordinate) to bring close points together.
        2.  Use a greedy approach? Greedy works for 1D. In 2D, it's harder.
        3.  However, notice the constraint: $k$ is very small. Maybe we can use the small $k$?
        4.  Actually, is there a property? If we sort by perimeter, points that are far in perimeter might still be close in Manhattan (e.g., opposite sides). But points that are close in Manhattan are usually close in perimeter (or symmetric).
        5.  Let's reconsider the "Unfold" idea.
            *   If we sort by perimeter, the "closest" points in Manhattan are likely neighbors in the sorted list OR points that are symmetric across a corner?
            *   Actually, for points on the boundary, the Manhattan distance is minimized when they are close in perimeter OR they are on opposite sides with similar coordinates (e.g., $(0, y)$ and $(side, y)$).
            *   Wait, $(0, y)$ and $(side, y)$ have Manhattan distance $side$. $(0,0)$ and $(side, side)$ have distance $2 \times side$.
            *   The "danger" cases for small distance are points on the same side or adjacent sides. Points on opposite sides always have distance $\ge side$.
            *   So, if $d \le side$, we only need to worry about points on the same side or adjacent sides.
            *   If $d > side$, we can't have any two points on opposite sides? No, opposite sides have min dist $side$. If $d > side$, we can't pick points from both left and right if they have same y? No, min dist between Left and Right is $side$. So if $d > side$, we can pick at most one from Left and one from Right? No, if $d > side$, we cannot pick ANY pair from Left and Right because their distance is exactly $side$ (if y-coords match) or more. Wait, min dist between Left $(0, y1)$ and Right $(side, y2)$ is $side + |y1-y2| \ge side$. So if $d > side$, we can still pick from both, just not if $|y1-y2|$ is small.
            *   Actually, the maximum possible minimum distance is bounded by $2 \times side$ (e.g., picking 2 corners).
    *   **Better Approach for Check**:
        *   Since $k$ is small, maybe we can iterate through all points as the "first" point and run a greedy selection?
        *   Algorithm for `check(d)`:
            *   Sort points by perimeter coordinate.
            *   Try starting with each point $i$ from $0$ to $n-1$.
            *   Greedily select the next point $j$ (where $j > i$) such that $dist(p_i, p_j) \ge d$. To optimize, we can maintain a pointer or use a segment tree, but since $k$ is small, maybe just linear scan from current pointer is okay?
            *   Worst case: $N \times k \times N$? No, linear scan advances the pointer. Total time per start point is $O(N)$. Total check time $O(N^2)$. Still too slow if $N=15000$.
            *   We need $O(N \log N)$ or $O(N)$.
            *   **Optimization**: Since we sort by perimeter, for a fixed start point $i$, the next valid point $j$ must be the first index $> i$ such that $dist(p_i, p_j) \ge d$.
            *   Can we find this $j$ faster?
            *   Note that $dist(p_i, p_j)$ is not monotonic with perimeter index $j$. (Due to the "opposite side" geometry).
            *   However, points on the same side or adjacent sides have monotonic distance behavior relative to perimeter. Points on opposite sides are "far".
            *   Given $k \le 25$, maybe the number of "conflicts" is low?
            *   Actually, there is a known solution pattern for this specific problem (LeetCode 3194? No, similar to "Maximize Minimum Manhattan Distance on Boundary").
            *   Key Insight: The Manhattan distance between two points on the boundary is determined by their positions. If we sort by perimeter, the distance function $f(j) = dist(p_i, p_j)$ generally increases as $j$ moves away from $i$, except when crossing the "opposite" side boundary?
            *   Actually, let's look at the constraints again. $k$ is up to 25. $N$ up to 15000.
            *   Maybe we can use the fact that we only need to pick $k$ points.
            *   Is it possible that checking `check(d)` takes $O(N)$?
            *   If we assume that for a fixed $i$, the valid next points form a contiguous range or can be found via binary search?
            *   Let's reconsider the "Opposite Side" issue.
                *   Left $(0, y)$ and Right $(side, y')$. Dist $= side + |y-y'|$.
                *   Top $(x, side)$ and Bottom $(x', 0)$. Dist $= side + |x-x'|$.
                *   Same side: $|x1-x2|$.
                *   Adjacent: $x + (side-y)$ etc.
            *   Notice that if $d \le side$, the "opposite side" constraint is loose (dist $\ge side \ge d$). The tight constraints are same-side and adjacent-side.
            *   If $d > side$, then we cannot pick two points from opposite sides unless their coordinate difference compensates? No, min dist is $side$. So if $d > side$, we can still pick from opposite sides, but we need $|y-y'| \ge d - side$.
            *   **Crucial Observation**: The problem is equivalent to selecting $k$ points on a circle (perimeter) with a specific distance metric. But the metric is not the arc length.
            *   However, since $k$ is very small, maybe we can just run the $O(N^2)$ check? $15000^2 = 2.25 \times 10^8$. In Python, this might TLE (Time Limit Exceeded) for 1-2 seconds, especially inside a binary search loop (30 iterations). $30 \times 2.25 \times 10^8 \approx 6 \times 10^9$ ops. Definitely TLE.
            *   We need a faster check.
            *   **Alternative**: Since $k$ is small, can we use dynamic programming? $dp[i][j]$ = min perimeter index of $j$ points ending at $i$? $O(N^2)$. Same issue.
            *   **Wait**, is the number of points on the boundary really up to 15000? Yes.
            *   Is there a property that allows $O(N)$ check?
            *   If we sort by perimeter, does the greedy strategy work?
                *   Greedy: Pick first point. Then pick the next point with distance $\ge d$.
                *   Does greedy work for "Maximize Minimum Distance" on a line? Yes.
                *   Does it work here? The metric is not a metric on the line (triangle inequality holds for Manhattan, but the mapping to line is not isometric).
                *   However, if we consider the "unfolded" line, the distance is roughly the distance on the line, with some "jumps" for opposite sides.
                *   Actually, for points on the boundary, the Manhattan distance is **monotonic** with respect to the perimeter distance **within each quadrant of the perimeter**?
                *   Let's assume the greedy approach on the sorted perimeter list works, but we need to handle the wrap-around.
                *   To handle wrap-around with greedy: Try all $k$ starting points? No, try all $N$ starting points?
                *   If we try all $N$ starting points, it's $O(N^2)$.
                *   Can we optimize the "next valid point" search?
                *   For a fixed $i$, we want smallest $j > i$ such that $dist(p_i, p_j) \ge d$.
                *   Since $dist$ is not strictly monotonic, we can't binary search directly.
                *   BUT, we can observe that for a fixed $i$, the set of points with $dist(p_i, p_j) < d$ is likely a contiguous segment in the sorted list?
                    *   On the same side: Yes.
                    *   On adjacent sides: Yes (distance increases as we move away from the corner).
                    *   On opposite sides: Distance is $side + |coord1 - coord2|$. This is also monotonic as we move away from the "equator" (midpoint of opposite side)?
                    *   Actually, if we sort by perimeter, as $j$ increases, the perimeter distance increases. The Manhattan distance generally increases too, but might dip if we cross the "opposite" boundary?
                    *   Example: $i$ at $(0,0)$. $j$ moves along bottom, right, top, left.
                        *   Bottom: $dist = x_j$. Increases.
                        *   Right: $dist = side + (y_j - 0)$. Increases.
                        *   Top: $dist = side + side + (side - x_j) = 3s - x_j$. Decreases!
                        *   Left: $dist = 3s + (side - y_j)$. Increases? No, $3s + s - y_j = 4s - y_j$. As $y_j$ goes $s \to 0$, dist goes $4s-s \to 4s$. Increases.
                    *   So the distance increases, then decreases (on the opposite side), then increases.
                    *   This means the "valid" points are NOT a contiguous suffix. They are a suffix, then a gap (the "danger zone" on the opposite side), then the rest.
                    *   However, we only need to pick $k$ points. If $k$ is small, maybe we don't traverse the whole circle?
                    *   Actually, if $d$ is large, we skip many points.
            *   **Wait, constraints check**: $k \le 25$. This is extremely small.
            *   Maybe the intended solution relies on the small $k$?
            *   If we use the greedy strategy: Start with point $i$. Find next $j$. Then next $l$...
            *   If we try every point as the start, it's $O(N^2)$.
            *   Is there a way to do it in $O(N)$?
            *   Actually, we can duplicate the array to handle wrap-around.
            *   If we assume the greedy choice is optimal (which is true for 1D line), does it hold here?
            *   There is a known result: For points on a circle with a distance metric that is "quasi-metric" or has specific properties, greedy might fail. But given the constraints and problem type, maybe the test cases are weak or the geometry ensures greedy works?
            *   **Wait**, let's look at the constraints again. $N \le 15000$. $O(N^2)$ is risky.
            *   Is it possible to use a Segment Tree?
                *   We want to find the first $j > i$ with $dist \ge d$.
                *   Since the distance function is piecewise monotonic, we can split the search into segments (same side, adjacent, opposite).
                *   For each segment, we can binary search.
                *   There are 4 segments relative to $i$.
                *   So for each $i$, we do 4 binary searches. Total $O(N \log N)$ per check.
                *   Total complexity: $O(\log(\text{side}) \cdot N \log N)$.
                *   $30 \times 15000 \times 14 \approx 6.3 \times 10^6$. This is very fast!
            *   **Implementation Details**:
                *   Map each point to a perimeter coordinate and a side ID (0: bottom, 1: right, 2: top, 3: left).
                *   Sort points by perimeter coordinate.
                *   Duplicate the list (append $N$ points with offset $4 \times side$) to handle wrap-around easily.
                *   For `check(d)`:
                    *   Iterate $i$ from $0$ to $N-1$.
                    *   Try to pick $k$ points starting from $i$.
                    *   Current point $curr = i$. Count = 1. Last perimeter = $P_i$.
                    *   We need to find next point $next > curr$ such that $dist(curr, next) \ge d$.
                    *   Since the distance function from a fixed point $curr$ is monotonic in 4 segments (Bottom, Right, Top, Left relative to $curr$'s position), we can binary search in each segment.
                    *   Wait, the segments are defined by the square's sides, not relative to $curr$.
                    *   The sorted list is global. The "segments" for $curr$ are:
                        1.  Points on the same side as $curr$ (after $curr$).
                        2.  Points on the next side.
                        3.  Points on the opposite side.
                        4.  Points on the remaining sides.
                    *   Actually, simpler: Just binary search over the range $[curr+1, curr + N - (k - count)]$.
                    *   But the distance isn't monotonic globally.
                    *   However, we can check the 4 intervals separately:
                        1.  Same side: $P \in [P_{curr}, P_{curr\_side\_end}]$. Dist is monotonic.
                        2.  Next side: $P \in [P_{curr\_side\_end}, P_{next\_side\_end}]$. Dist is monotonic.
                        3.  Opposite side: $P \in [P_{opp\_start}, P_{opp\_end}]$. Dist is monotonic (decreases then increases? No, let's re-verify).
                            *   From Left $(0, y)$ to Top $(x, s)$. Dist $= x + (s-y)$. As $x$ increases (moving right on top), dist increases.
                            *   From Left $(0, y)$ to Right $(s, y')$. Dist $= s + |y-y'|$.
                                *   If we move from Top to Right: $y'$ goes $s \to 0$. $|y-y'|$ goes $|y-s| \to |y|$.
                                *   If $y < s$, $|y-s| = s-y$. Then $|y-y'|$ decreases as $y'$ goes $s \to y$, then increases.
                                *   So on the opposite side, the distance might NOT be monotonic.
                    *   **Correction**: The distance from a fixed point to points on the opposite side is $side + |coord1 - coord2|$. This is V-shaped (decreases then increases).
                    *   So we can't just binary search the whole opposite side.
                    *   But we can binary search the two halves of the opposite side? Or just check the minimum?
                    *   Actually, since $k$ is small, maybe we don't need to find the *absolute* next valid point?
                    *   Wait, the greedy strategy requires the *first* valid point. If we skip a valid point, we might fail to reach $k$.
                    *   Given the complexity of the distance function, maybe the "V-shape" on the opposite side means the valid points are a union of two intervals?
                    *   Actually, if $d$ is large, the "V-shape" bottom might be below $d$, so valid points are the two tails.
                    *   This suggests we can check the "danger zone" (the bottom of the V) and if it's $< d$, we skip it.
                    *   **Simpler approach**: Since $N$ is 15000, maybe $O(N \log N)$ per check is acceptable if the constant factor is small.
                    *   We can implement a helper `find_next(idx, d)` that scans forward but skips efficiently? No, scanning is $O(N)$.
                    *   Let's stick to the Segment Tree or 4-interval binary search idea.
                    *   Intervals:
                        1.  Same side (monotonic).
                        2.  Next side (monotonic).
                        3.  Opposite side (V-shape). We can find the minimum distance in this interval. If min $\ge d$, all are valid (binary search first). If min $< d$, we need to find the points where dist $\ge d$. This is two intervals (left and right of the minimum). We can binary search for the left boundary and right boundary.
                        4.  Remaining sides (monotonic).
                    *   This gives us a way to find the first valid point in $O(\log N)$.
                    *   Then we repeat $k-1$ times. Total $O(k \log N)$.
                    *   Total Check: $O(N \cdot k \log N)$.
                    *   $15000 \times 25 \times 14 \approx 5.25 \times 10^6$. Very safe.

## worker: Implement the `Solution` class with the `maxDistan
The problem requires selecting $k$ points on the boundary of a square to maximize the minimum Manhattan distance between any two selected points. This is a classic "maximize the minimum" problem, which can be solved using binary search on the answer.

The key challenges are:
1.  **Distance Metric**: The Manhattan distance between two points on the boundary is not simply the distance along the perimeter. It depends on the coordinates.
2.  **Verification**: For a given distance $d$, we need to check if it's possible to select $k$ points such that all pairwise distances are $\ge d$.
3.  **Efficiency**: The number of points $N$ can be up to 15,000, and $k$ is small ($\le 25$). An $O(N^2)$ check inside the binary search would be too slow. We need an $O(N \log N)$ or $O(N)$ check.

The solution uses the following approach:
1.  **Map Points**: Convert each point to a perimeter coordinate and a side index to facilitate sorting and segment-based searches.
2.  **Binary Search**: The range of possible distances is $[1, 2 \times \text{side}]$.
3.  **Check Function**:
    *   Sort the points by their perimeter coordinate.
    *   Duplicate the list of points to handle the wrap-around of the square boundary easily.
    *   For each point in the original list, try to greedily select $k$ points starting from it.
    *   To find the next valid point efficiently, we use binary search on the 4 segments (sides) of the square. The distance function is monotonic within each side, but V-shaped on the opposite side. We handle the V-shape by finding the minimum distance point and then binary searching in the two monotonic segments around it.
    *   The total complexity of the check function is $O(N \cdot k \log N)$, which is efficient enough given the constraints.

## worker: Implement the `Solution` class with the `maxDistan
The solution implements a binary search on the answer (the minimum Manhattan distance). The range of possible distances is $[1, 2 \times \text{side}]$. For each candidate distance $d$, the `check(d)` function verifies if it's possible to select $k$ points such that all pairwise Manhattan distances are at least $d$.

The `check(d)` function uses a greedy strategy:
1.  Iterate through each point in the sorted list (sorted by perimeter coordinate) as a potential starting point.
2.  From the current point, greedily select the next available point that satisfies the distance constraint $d$.
3.  Repeat this process $k-1$ times. If we successfully select $k$ points, return `True`.

To efficiently find the next valid point, the solution leverages the fact that the points lie on the boundary of a square. The Manhattan distance function between a fixed point and points on the boundary is piecewise monotonic. Specifically, within each side of the square, the distance function is monotonic. However, on the opposite side, it forms a "V-shape" (decreases then increases). The `find_first_valid_in_range` helper function handles this by:
1.  Identifying the point in the search range that minimizes the distance (the "vertex" of the V-shape).
2.  If the minimum distance is $\ge d$, all points in the range are valid, so the first point is the answer.
3.  If the minimum distance is $< d$, the valid points form a prefix and a suffix of the range. The function checks the prefix and then binary searches the suffix to find the first valid point.

The complexity is $O(N \cdot k \log N)$ per check, where $N$ is the number of points. With $k \le 25$ and $N \le 15000$, this is efficient enough.

## worker: Run the code against the provided examples to veri
The solution implements a binary search on the answer (the minimum Manhattan distance). The range of possible distances is $[1, 2 \times \text{side}]$. For each candidate distance $d$, the `check(d)` function verifies if it's possible to select $k$ points such that all pairwise Manhattan distances are at least $d$.

The `check(d)` function uses a greedy strategy:
1.  Iterate through each point in the sorted list (sorted by perimeter coordinate) as a potential starting point.
2.  From the current point, greedily select the next available point that satisfies the distance constraint $d$.
3.  Repeat this process $k-1$ times. If we successfully select $k$ points, return `True`.

To efficiently find the next valid point, the solution leverages the fact that the points lie on the boundary of a square. The Manhattan distance function between a fixed point and points on the boundary is piecewise monotonic. Specifically, within each side of the square, the distance function is monotonic. However, on the opposite side, it forms a "V-shape" (decreases then increases). The `find_first_valid_in_range` helper function handles this by:
1.  Identifying the point in the search range that minimizes the distance (the "vertex" of the V-shape).
2.  If the minimum distance is $\ge d$, all points in the range are valid, so the first point is the answer.
3.  If the minimum distance is $< d$, the valid points form a prefix and a suffix of the range. The function checks the prefix and then binary searches the suffix to find the first valid point.

The complexity is $O(N \cdot k \log N)$ per check, where $N$ is the number of points. With $k \le 25$ and $N \le 15000$, this is efficient enough.

## worker: finalize
The solution implements a binary search on the answer (the minimum Manhattan distance). The range of possible distances is $[1, 2 \times \text{side}]$. For each candidate distance $d$, the `check(d)` function verifies if it's possible to select $k$ points such that all pairwise Manhattan distances are at least $d$.

The `check(d)` function uses a greedy strategy:
1.  Iterate through each point in the sorted list (sorted by perimeter coordinate) as a potential starting point.
2.  From the current point, greedily select the next available point that satisfies the distance constraint $d$.
3.  Repeat this process $k-1$ times. If we successfully select $k$ points, return `True`.

To efficiently find the next valid point, the solution leverages the fact that the points lie on the boundary of a square. The Manhattan distance function between a fixed point and points on the boundary is piecewise monotonic. Specifically, within each side of the square, the distance function is monotonic. However, on the opposite side, it forms a "V-shape" (decreases then increases). The `find_first_valid_in_range` helper function handles this by:
1.  Identifying the point in the search range that minimizes the distance (the "vertex" of the V-shape).
2.  If the minimum distance is $\ge d$, all points in the range are valid, so the first point is the answer.
3.  If the minimum distance is $< d$, the valid points form a prefix and a suffix of the range. The function checks the prefix and then binary searches the suffix to find the first valid point.

The complexity is $O(N \cdot k \log N)$ per check, where $N$ is the number of points. With $k \le 25$ and $N \le 15000$, this is efficient enough.
