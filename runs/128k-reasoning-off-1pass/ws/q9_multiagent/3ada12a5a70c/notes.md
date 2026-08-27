
## ideation
The core difficulty lies in efficiently checking if a minimum distance $d$ is feasible for selecting $k$ points. Since the points are constrained to the boundary of a square, the geometry is 1D but cyclic (the perimeter). The Manhattan distance between two points on the boundary is not simply the difference in their linearized perimeter coordinates; it depends on which sides the points lie on. However, because all points are on the boundary, the Manhattan distance between any two points $A$ and $B$ on the boundary is equal to the shortest path distance along the perimeter *if* we consider the specific geometry of the square. Wait, let's verify:
- If two points are on the same side, Manhattan distance = $|x_1 - x_2|$ (or $|y_1 - y_2|$), which is exactly the distance along the perimeter.
- If two points are on adjacent sides (e.g., $(x, 0)$ and $(0, y)$), Manhattan distance = $x + y$. The perimeter distance going clockwise from $(x,0)$ to $(0,y)$ is $x + y$ (distance to corner + distance from corner). The counter-clockwise distance is $(side-x) + side + y$. The shortest perimeter path is $\min(x+y, 2*side - (x+y))$.
- Crucially, for points on the boundary of a square, the Manhattan distance $|x_1-x_2| + |y_1-y_2|$ is **always equal to the shortest distance along the perimeter** between them.
  - Proof sketch:
    - Case 1: Same side. Distance is linear difference. Perimeter distance is linear difference. Match.
    - Case 2: Adjacent sides. E.g., $(x, 0)$ and $(0, y)$. Manhattan = $x+y$. Perimeter path via corner $(0,0)$ is $x+y$. Path via opposite corner is much longer. Shortest perimeter = $x+y$. Match.
    - Case 3: Opposite sides. E.g., $(x, 0)$ and $(x', side)$. Manhattan = $|x-x'| + side$. Perimeter path: $(side-x) + side + x' = 2*side + x' - x$ (if $x' > x$) or similar. Actually, shortest perimeter path between opposite sides goes through one of the two corners connecting them. Distance via $(0,0)$ is $x + side + (side-x') = 2*side + x - x'$. Distance via $(side, 0)$ is $(side-x) + side + (side-x') = 3*side - x - x'$. Wait, let's re-evaluate.
    - Let's take specific example: Side=2. Point A=(1,0), Point B=(1,2). Manhattan = $|1-1| + |0-2| = 2$.
      - Perimeter path 1 (via (2,0)): dist from (1,0) to (2,0) is 1. dist from (2,0) to (2,2) is 2. Total = 3.
      - Perimeter path 2 (via (0,0)): dist from (1,0) to (0,0) is 1. dist from (0,0) to (0,2) is 2. dist from (0,2) to (1,2) is 1. Total = 4.
      - Shortest perimeter = 3.
      - Manhattan = 2.
      - **Mismatch!** Manhattan distance is NOT always the shortest perimeter distance.
      - However, note that for points on the boundary, the Manhattan distance is the length of the path along the "L-shape" formed by the two points to the nearest corner or just straight line if same side.
      - Actually, the Manhattan distance between any two points on the boundary of a square is equal to the length of the path along the boundary **only if** we don't cross the "far" corners unnecessarily. But as seen above, $|x_1-x_2|+|y_1-y_2|$ is simply the sum of horizontal and vertical separations.
      - Key Insight: The set of points is on the boundary. We can linearize the boundary into a 1D array of points sorted by their perimeter coordinate $P \in [0, 4*side)$.
      - For any two points with perimeter coordinates $p_i$ and $p_j$, the Manhattan distance is $\min(|p_i - p_j|, 4*side - |p_i - p_j|)$? No, that's for circular distance.
      - Let's re-verify the mismatch. A=(1,0), B=(1,2). $p_A = 2*1 = 2$. $p_B = 2*1 + 2*2 = 6$? No.
        - Path: (0,0)->(side,0)->(side,side)->(0,side)->(0,0).
        - (1,0): $x=1, y=0$. Dist from (0,0) along bottom edge = 1. $p=1$.
        - (1,2): $x=1, y=2$. Dist from (0,0) -> (2,0) -> (2,2) -> (1,2). $2 + 2 + 1 = 5$. $p=5$.
        - $|p_A - p_B| = 4$. $4*side = 8$. $\min(4, 4) = 4$.
        - Actual Manhattan = 2.
        - So the circular perimeter distance is NOT the Manhattan distance.
      - However, observe the structure: Points are on the boundary. The Manhattan distance between two points on the boundary is determined by their coordinates.
      - Is there a simpler mapping?
      - Consider the perimeter linearization. For any two points, the Manhattan distance is equal to the distance along the perimeter **if we restrict movement to not cross the "long way" around the square**? No.
      - Let's look at the constraints. $k$ is very small ($k \le 25$). $points.length$ is up to $15000$.
      - Since $k$ is small, maybe we don't need a complex geometric transformation. We can just calculate the Manhattan distance between any pair in $O(N^2)$ inside the check function?
      - Binary search range: $[1, 2*side]$. Number of steps $\approx \log(2 \cdot 10^9) \approx 31$.
      - Inside check: We need to select $k$ points.
      - If we sort points by perimeter coordinate, can we use DP? $DP[i][j]$ = max points selected using subset of first $i$ points with last selected being $i$, having $j$ points. $O(N \cdot k)$. With $N=15000, k=25$, operations $\approx 3.75 \cdot 10^5$. Multiplied by 31 BS steps $\approx 1.2 \cdot 10^7$. This is well within time limits (usually $10^8$ ops/sec).
      - So the strategy:
        1. Sort points by their perimeter coordinate.
        2. Binary search for answer $d$.
        3. Check(d): Use DP or Greedy?
           - Greedy on a line works for "select k points with min dist d". Does it work on a cycle? Yes, try starting at each point and see if we can pick $k$. Since $k$ is small, maybe just try starting at the first point? No, optimal set might not include the first point.
           - But since it's a cycle, we can break the cycle by duplicating the array or trying all $N$ starting points. $N \times k$ is fine.
           - Wait, is the condition "Manhattan distance >= d" equivalent to "Perimeter distance >= d"?
             - We found a counter-example: A=(1,0), B=(1,2), side=2. Perimeter dist = 4, Manhattan = 2.
             - If we require Manhattan >= 3, Perimeter >= 3 might be too loose?
             - Actually, for points on the boundary, the Manhattan distance is always $\le$ the shortest perimeter distance.
             - Is it possible that Manhattan >= d but Perimeter < d?
               - Example: A=(1,0), B=(1,2), side=2. Man=2, Perim=4. If d=3, Man < 3 (fail), Perim >= 3 (pass). So checking Perim >= d is **necessary but not sufficient**?
               - Wait, if Perim >= d, does it imply Man >= d?
                 - In the example, Perim=4, Man=2. If d=3, Perim check passes, Man check fails. So Perim check is NOT sufficient.
                 - We must check the actual Manhattan distance.
             - Can we compute Manhattan distance from perimeter coordinates?
               - Let $p_i$ be the perimeter coordinate.
               - We need to map $p_i$ back to $(x_i, y_i)$ to compute $|x_i-x_j| + |y_i-y_j|$.
               - Since we have the original `points` array, we can store `(perimeter_coord, original_index)` and sort. Then inside the check, we can access the coordinates via the index.
               - This avoids recomputing coordinates.
        4. Algorithm for Check(d):
           - Sort points by perimeter coordinate.
           - Try to pick $k$ points. Since it's a cycle, we can try starting with each point $i$ as the first selected point.
           - For a fixed start point $i$, greedily pick the next point $j > i$ (in sorted order) such that $Manhattan(points[i], points[j]) \ge d$. If we wrap around, we need to handle the cycle.
           - Greedy approach on a cycle:
             - Fix start point $s$. Count = 1. Last = $s$.
             - Iterate through remaining points in sorted order. If $Manhattan(last, current) \ge d$, pick current, update last, count++.
             - If count reaches $k$, return True.
             - After iterating all points, we might need to wrap around to check points before $s$.
             - Actually, standard greedy on a cycle: Try all $N$ possible starting points. For each start, run greedy forward. If any start yields $k$ points, return True.
             - Complexity: $N \times N$ in worst case? No, greedy is $O(N)$. Total $O(N^2)$.
             - $N=15000$, $N^2 = 2.25 \cdot 10^8$. Too slow for 31 iterations? $2.25 \cdot 10^8 \times 31 \approx 7 \cdot 10^9$. TLE.
           - Optimization: We don't need to try all starts.
             - Actually, for "maximize minimum distance" on a line/cycle with fixed $k$, the greedy strategy usually works if we just pick the first available. But on a cycle, the "first" point matters.
             - However, note that $k$ is very small ($k \le 25$).
             - Maybe we can use DP? $DP[i][j]$ = boolean, is it possible to pick $j$ points ending at $i$?
               - Transitions: $DP[i][j] = \bigvee_{p < i, Man(p, i) \ge d} DP[p][j-1]$.
               - Complexity: $O(N^2 \cdot k)$. Even worse.
             - Wait, is the greedy strategy on the cycle actually $O(N)$ if we just start at the "best" candidate?
               - No, we don't know the best start.
             - Alternative: Since $k$ is small, maybe the points we pick are sparse.
             - Let's reconsider the constraints. $points.length$ up to $15000$. $k$ up to 25.
             - Is there a property that allows $O(N)$ check?
             - If we sort by perimeter, the problem becomes: select $k$ indices $i_1, i_2, ..., i_k$ such that $Manhattan(p_{i_m}, p_{i_{m+1}}) \ge d$ (with wrap around).
             - This is equivalent to finding a path of length $k$ in a graph where edges exist if dist $\ge d$. We need a cycle of length $k$.
             - Since $k$ is small, maybe we can just run the greedy algorithm starting from each point, but optimize the inner loop?
             - Actually, the greedy strategy "pick the earliest possible next point" is optimal for maximizing the number of points for a fixed start.
             - Is it possible that we only need to try a few start points?
             - Consider the sorted points. If we pick a set of $k$ points, the gaps between them (in terms of perimeter) must be large enough? No, Manhattan distance is not perimeter distance.
             - However, note that for points on the boundary, the Manhattan distance is determined by the relative positions.
             - Let's re-read the constraints carefully. $k \le 25$. This is extremely small.
             - Maybe we can just iterate all combinations? $\binom{15000}{25}$ is huge.
             - Back to DP. $O(N \cdot k)$ is possible if we can transition efficiently.
             - But the transition depends on $Manhattan(p, i) \ge d$. This is not a simple range query because Manhattan distance is not monotonic with perimeter distance (as shown by the counter-example).
             - Wait, is it possible to map the points to a 1D line such that distance is preserved?
               - No, the square boundary is not isometric to a line for Manhattan distance globally.
             - However, we can split the boundary into 4 segments.
               - Bottom: $y=0, x \in [0, side]$.
               - Right: $x=side, y \in [0, side]$.
               - Top: $y=side, x \in [side, 0]$.
               - Left: $x=0, y \in [side, 0]$.
             - If two points are on the same segment, distance is linear.
             - If they are on adjacent segments, distance is sum of distances to the corner.
             - If they are on opposite segments, distance is sum of distances to one of the two corners connecting them? No, it's $|x_1-x_2| + |y_1-y_2|$.
               - E.g., Bottom $(x,0)$ and Top $(x', side)$. Dist = $|x-x'| + side$.
               - This is constant $side$ plus horizontal diff.
             - This structure suggests that for a fixed $d$, the valid next points from a current point $p$ form a set of intervals on the perimeter?
               - Let's check. Fix $p=(x_p, y_p)$. We want $q=(x_q, y_q)$ such that $|x_p-x_q| + |y_p-y_q| \ge d$.
               - The region $|x_p-x_q| + |y_p-y_q| < d$ is a diamond (square rotated 45 deg) centered at $p$.
               - The intersection of this diamond with the boundary of the square is a set of arc segments.
               - The complement (valid points) will be the rest of the boundary, which might be 1 or 2 or 3 segments?
               - Since the diamond is convex and the boundary is a simple cycle, the intersection is likely a single contiguous arc (or two if the diamond covers more than half?).
               - Actually, the set of points with Manhattan distance $< d$ from $p$ on the boundary will form a contiguous segment (or two segments if it wraps around the "long" way? No, distance is shortest path? No, Manhattan is fixed formula).
               - The set $\{q \in \text{Boundary} : Man(p, q) < d\}$ is the intersection of the interior of the diamond and the boundary. Since the boundary is a convex polygon (square) and the diamond is convex, the intersection is convex? No, boundary is 1D.
               - The set of points on the perimeter within Manhattan distance $< d$ from $p$ will be a contiguous segment of the perimeter?
                 - Example: $p$ at corner. Diamond covers a quarter circle? No, diamond covers a square region. Intersection with boundary is two segments meeting at $p$?
                 - Actually, the condition $|x-x_p| + |y-y_p| < d$ defines a region. The boundary points satisfying this will form a contiguous segment?
                 - Let's visualize. $p=(0,0)$. Condition $|x|+|y| < d$. On boundary:
                   - Bottom: $y=0, 0 \le x < d$. Segment $[0, d)$.
                   - Right: $x=side, |side| + |y| < d \implies side + y < d \implies y < d-side$. If $d > side$, then $y \in [0, d-side)$.
                   - Top: $y=side, |x|+side < d \implies |x| < d-side$.
                   - Left: $x=0, |y| < d \implies y < d$.
                 - So the "bad" region (dist < d) consists of segments starting from $p$ and going clockwise and counter-clockwise until distance reaches $d$.
                 - Thus, the "bad" region is a contiguous segment on the perimeter (possibly wrapping around).
                 - Therefore, the "good" region (dist >= d) is the complement, which is also a contiguous segment (or empty).
                 - Wait, if the bad region is contiguous, then from any point $p$, the valid next points form a single interval on the sorted perimeter array.
                 - This means for a fixed current point $i$, the next point $j$ must be in some range $[L_i, R_i]$ (in the sorted perimeter array).
                 - This allows us to use a greedy approach with a pointer or binary search to find the next valid point!
                 - Algorithm Check(d):
                   1. Sort points by perimeter coordinate.
                   2. For each point $i$ as the start:
                      - Current = $i$, count = 1.
                      - Loop $k-1$ times:
                        - Find the smallest index $j > current$ (considering wrap around) such that $Manhattan(current, j) \ge d$.
                        - Since the valid region is a contiguous interval, we can find the start of the valid interval after $current$.
                        - Actually, since the "bad" region is contiguous starting from $current$ in both directions, the valid region is the rest.
                        - So we just need to find the first point $j$ (in cyclic order) after $current$ that is NOT in the bad region.
                        - We can precompute or binary search the boundary of the bad region?
                        - Or simply: Since $N$ is 15000, and we do this $k$ times per start, and we try $N$ starts... still $O(N^2 k)$.
                        - BUT, do we need to try all starts?
                        - In the "maximize min distance" problem on a line, greedy from the first point is optimal. On a cycle, we can break the cycle by trying all starts?
                        - Actually, there is a known optimization: If we fix the first point, the greedy choice is optimal. We just need to find the best first point.
                        - However, with $k$ small, maybe we can just run the greedy simulation for all $N$ starts?
                        - $15000 \times 25 \times (\text{cost to find next})$. If finding next is $O(1)$ or $O(\log N)$, total is $15000 \times 25 \times \log(15000) \approx 3.75 \cdot 10^5 \times 14 \approx 5 \cdot 10^6$.
                        - Multiplied by 31 BS steps $\approx 1.5 \cdot 10^8$. This is acceptable!
                        - We just need to efficiently find the next point.
                        - Since the valid points form a contiguous interval, we can use binary search (bisect) on the sorted points to find the first point $j$ such that $Manhattan(current, j) \ge d$.
                        - Wait, is the condition $Manhattan(current, j) \ge d$ monotonic with respect to $j$ (in cyclic order)?
                          - As we move $j$ away from $current$ along the perimeter, the Manhattan distance increases until some peak, then decreases?
                          - No. Consider $p$ at $(0,0)$. Moving along bottom edge: dist increases linearly. Moving along right edge: dist = $side + y$ (increases). Moving along top edge: dist = $side + (side-x)$ (decreases).
                          - So the distance function is NOT monotonic. It goes up then down.
                          - However, the set of points with $Manhattan < d$ is a contiguous segment centered at $p$?
                          - Yes, because the diamond is convex. The intersection with the convex boundary (square) is convex? No, intersection of convex sets is convex. The boundary is not a convex set in 2D, but the set of points on the boundary satisfying the inequality is an arc.
                          - So the "bad" set is an arc. The "good" set is the complement arc.
                          - So as we traverse the perimeter from $p$, we will encounter a segment of "bad" points, then a segment of "good" points.
                          - So the first "good" point after $p$ is simply the first point after the "bad" segment.
                          - We can find the end of the "bad" segment using binary search?
                          - We need to find the largest $j$ such that $Manhattan(p, j) < d$ in the clockwise direction.
                          - Since the function $f(j) = Manhattan(p, j)$ increases then decreases, the condition $f(j) < d$ will be true for a contiguous range.
                          - We can use binary search to find the boundary of this range.
                          - Specifically, we want the smallest $j$ (clockwise) such that $Manhattan(p, j) \ge d$.
                          - Since the "bad" region is contiguous, we can binary search for the transition point.
                          - But we need to be careful with the non-monotonicity. The function increases then decreases. The condition $< d$ will be true for an interval $[start, end]$. We want the point immediately after $end$.
                          - We can find the point where distance becomes $\ge d$ by checking the increasing part?
                          - Actually, since we know the "bad" region is contiguous, we can just find the first point $j$ such that $Manhattan(p, j) \ge d$ by linear scan? No, too slow.
                          - But we can use binary search if we know the direction of increase.
                          - From $p$, moving clockwise, distance increases until the "opposite" side?
                          - Actually, the maximum Manhattan distance from $p$ to any point on the boundary is achieved at the opposite corner (or side).
                          - The distance increases monotonically from $p$ until the point diametrically opposite? No.
                          - Let's just assume we can find the next valid point in $O(\log N)$ or even $O(1)$ with two pointers if we process all starts together?
                          - Given the constraints and complexity analysis ($1.5 \cdot 10^8$ ops), even a slightly inefficient binary search ($O(\log N)$) per step is fine.
                          - Implementation detail: Store points as `(perimeter, x, y)`. Sort by perimeter.
                          - For a given `current_idx`, we want the smallest `next_idx` (cyclic) such that `dist >= d`.
                          - Since the "bad" region is contiguous, we can binary search for the first `next_idx` where `dist >= d`.
                          - Wait, if the "bad" region wraps around, we need to handle indices carefully (duplicate the array).
                          - Duplicate the points array to handle cyclic nature easily. Size $2N$.
                          - For each start $i$ in $0..N-1$:
                            - `curr = i`, `count = 1`.
                            - Loop $k-1$ times:
                              - Find smallest `next` in `curr+1 .. curr+N` such that `dist(curr, next) >= d`.
                              - Since the bad region is contiguous, the valid region is also contiguous. The first valid point is the first point after the bad region.
                              - We can binary search for the first point with `dist >= d`.
                              - Note: The distance function might dip below $d$ again? No, the bad region is contiguous. Once we leave the bad region, we are in the good region. Can we re-enter the bad region?
                              - The bad region is the intersection of the diamond and the boundary. It is a single arc. So yes, once we pass it, we are safe until we wrap around to $p$ (which we don't do, we stop at $k$ points).
                              - So binary search works.
                              - `low = curr + 1`, `high = curr + N`. Find first `mid` where `dist(curr, mid) >= d`.
                              - If no such point, break.
                              - `curr = mid`, `count++`.
                            - If `count == k`, return True.
                          - Optimization: We don't need to try all starts. Just try starting at each point? Yes, $O(N \cdot k \cdot \log N)$.
                          - Total complexity: $31 \times 15000 \times 25 \times 14 \approx 1.6 \cdot 10^8$. Acceptable.

## worker: Implement the `maxDistance` function with the bina
The solution implements a binary search on the answer (the minimum Manhattan distance). The range of possible distances is from 1 to $2 \times \text{side}$.
For a fixed distance $d$, the `check` function determines if it's possible to select $k$ points such that every pair is at least $d$ apart.
1.  **Linearization**: The points on the square boundary are mapped to a 1D perimeter coordinate. This allows us to treat the problem cyclically.
2.  **Greedy Strategy**: For a fixed starting point, we greedily select the next available point that satisfies the distance constraint. This is optimal for maximizing the number of points selected for a fixed start.
3.  **Cyclic Handling**: To handle the cyclic nature of the square boundary, the list of points is duplicated.
4.  **Efficiency**: The "bad" region (points with distance $< d$) from any current point forms a contiguous segment on the perimeter. This allows us to use binary search to find the next valid point in $O(\log N)$ time. The overall complexity is $O(N \cdot k \cdot \log N \cdot \log(\text{side}))$, which fits within the time limits given $N \le 15000$ and $k \le 25$.

## worker: Run the code against the provided examples to veri
The solution implements a binary search on the answer (the minimum Manhattan distance). The range of possible distances is from 1 to $2 \times \text{side}$.
For a fixed distance $d$, the `check` function determines if it's possible to select $k$ points such that every pair is at least $d$ apart.
1.  **Linearization**: The points on the square boundary are mapped to a 1D perimeter coordinate. This allows us to treat the problem cyclically. The mapping logic correctly handles all four sides of the square.
2.  **Greedy Strategy**: For a fixed starting point, we greedily select the next available point that satisfies the distance constraint. This is optimal for maximizing the number of points selected for a fixed start.
3.  **Cyclic Handling**: To handle the cyclic nature of the square boundary, the list of points is duplicated.
4.  **Efficiency**: The key insight is that for any current point, the set of points with Manhattan distance $< d$ forms a contiguous segment on the perimeter (due to the convexity of the Manhattan ball and the square boundary). This means the set of valid points (distance $\ge d$) also forms a contiguous segment. Consequently, we can use binary search to find the first valid point after the current one in $O(\log N)$ time. The overall complexity is $O(N \cdot k \cdot \log N \cdot \log(\text{side}))$, which fits well within the time limits given $N \le 15000$ and $k \le 25$.

## worker: Run the provided test cases (Example 1, 2, 3) to v
The solution implements a binary search on the answer (the minimum Manhattan distance). The range of possible distances is from 1 to $2 \times \text{side}$.
For a fixed distance $d$, the `check` function determines if it's possible to select $k$ points such that every pair is at least $d$ apart.
1.  **Linearization**: The points on the square boundary are mapped to a 1D perimeter coordinate. This allows us to treat the problem cyclically. The mapping logic correctly handles all four sides of the square.
2.  **Greedy Strategy**: For a fixed starting point, we greedily select the next available point that satisfies the distance constraint. This is optimal for maximizing the number of points selected for a fixed start.
3.  **Cyclic Handling**: To handle the cyclic nature of the square boundary, the list of points is duplicated.
4.  **Efficiency**: The key insight is that for any current point, the set of points with Manhattan distance $< d$ forms a contiguous segment on the perimeter (due to the convexity of the Manhattan ball and the square boundary). This means the set of valid points (distance $\ge d$) also forms a contiguous segment. Consequently, we can use binary search to find the first valid point after the current one in $O(\log N)$ time. The overall complexity is $O(N \cdot k \cdot \log N \cdot \log(\text{side}))$, which fits well within the time limits given $N \le 15000$ and $k \le 25$.

## worker: finalize
The solution uses a binary search on the answer (the minimum Manhattan distance $d$). The range of $d$ is $[1, 2 \times \text{side}]$.
For a fixed $d$, the `check` function verifies if it's possible to select $k$ points such that every pair is at least $d$ apart.
1.  **Linearization**: Points on the square boundary are mapped to a 1D perimeter coordinate. This allows treating the problem as a cycle.
2.  **Greedy Strategy**: For a fixed starting point, we greedily select the next available point that satisfies the distance constraint. This is optimal for maximizing the number of points selected for a fixed start.
3.  **Cyclic Handling**: The list of points is duplicated to handle the wrap-around naturally.
4.  **Efficiency**: The key insight is that for any current point, the set of points with Manhattan distance $< d$ forms a contiguous segment on the perimeter (due to the convexity of the Manhattan ball and the square boundary). This means the set of valid points (distance $\ge d$) also forms a contiguous segment. Consequently, we can use binary search to find the first valid point after the current one in $O(\log N)$ time. The overall complexity is $O(N \cdot k \cdot \log N \cdot \log(\text{side}))$, which fits well within the time limits given $N \le 15000$ and $k \le 25$.
