
## ideation
**Core Difficulty**:
The problem is a variation of the "select $k$ points to maximize the minimum pairwise distance" problem. The key constraints are:
1.  **Metric**: Manhattan distance ($|x_1-x_2| + |y_1-y_2|$).
2.  **Geometry**: Points lie strictly on the boundary of a square.
3.  **Optimization Goal**: Maximize the minimum distance. This structure strongly suggests **Binary Search on the Answer**.
4.  **Verification Step**: For a candidate distance $D$, can we select $k$ points such that all pairwise distances are $\ge D$?

**Candidate Approaches**:
1.  **Binary Search + Greedy**:
    *   **Range**: Low = 0, High = $2 \times \text{side}$ (maximum possible Manhattan distance on the boundary).
    *   **Check Function (`can_select(D)`)**:
        *   Since points are on the boundary, we can linearize them. The boundary consists of 4 segments: Bottom ($y=0, x \in [0, \text{side}]$), Right ($x=\text{side}, y \in [0, \text{side}]$), Top ($y=\text{side}, x \in [\text{side}, 0]$), Left ($x=0, y \in [\text{side}, 0]$).
        *   Sort points based on their position along this perimeter path.
        *   Iterate through the sorted points. Maintain `last_picked_index`.
        *   For each point, calculate its distance to the `last_picked_index`. If distance $\ge D$, select it and update `last_picked_index`.
        *   Count selected points. If count $\ge k$, return `True`.
    *   **Complexity**: Sorting takes $O(N \log N)$. Binary search takes $O(\log(\text{side}))$. Check takes $O(N)$. Total: $O(N \log N + N \log(\text{side}))$. Given $N \le 15000$, this is efficient.

2.  **Manhattan Distance Simplification**:
    *   Manhattan distance $|x_1-x_2| + |y_1-y_2|$ on the boundary can sometimes be tricky if points are on different sides. However, since we linearize the perimeter, the distance between two points $P_i$ and $P_j$ (where $P_i$ comes before $P_j$ on the path) is simply the length of the arc along the boundary *if* the shortest path between them on the grid is unique or if we are constrained to the boundary.
    *   **Crucial Check**: Is the Manhattan distance between two points on the boundary equal to the distance along the perimeter?
        *   Case 1: Same side. Yes.
        *   Case 2: Adjacent sides (e.g., Bottom and Right). Point $(x, 0)$ and $(\text{side}, y)$. Dist = $(\text{side}-x) + y$. Perimeter distance = $(\text{side}-x) + y$. Yes.
        *   Case 3: Opposite sides (e.g., Bottom and Top). Point $(x, 0)$ and $(x', \text{side})$. Dist = $|x-x'| + \text{side}$. Perimeter distance (shortest way around) = $\min(|x-x'| + \text{side}, \dots)$. Actually, the Manhattan distance is $|x-x'| + \text{side}$. The perimeter distance going one way is $x + (\text{side} - x') + \text{side}$? No.
        *   Let's re-evaluate: $P_1=(x_1, 0)$, $P_2=(x_2, \text{side})$. $D_M = |x_1-x_2| + \text{side}$.
        *   Perimeter path 1: $x_1 \to 0 \to \text{side} \to x_2$ (Left side then Top)? Length: $x_1 + \text{side} + (\text{side}-x_2) = x_1 - x_2 + 2\text{side}$.
        *   Perimeter path 2: $x_1 \to \text{side} \to x_2$ (Right side then Top)? Length: $(\text{side}-x_1) + \text{side} + (\text{side}-x_2)$? No, Right side goes from $(\text{side}, 0)$ to $(\text{side}, \text{side})$. Then Top goes left.
        *   Actually, the Manhattan distance between any two points on the boundary of a square is **always equal** to the distance along the perimeter if we traverse the perimeter in a specific way? No.
        *   Counter-example: Square side 2. $A=(0,0)$, $B=(2,2)$. $D_M = 4$. Perimeter length is 8. Half perimeter is 4.
        *   $A=(1,0)$, $B=(1,2)$. $D_M = 2$. Perimeter distance (via right): $(2-1) + 2 + (2-1) = 4$. Perimeter distance (via left): $1 + 2 + 1 = 4$.
        *   Wait, the Manhattan distance is the $L_1$ norm. The perimeter distance is the arc length. They are not the same for opposite sides.
        *   **Correction**: We cannot simply use the linearized perimeter index difference as the distance. We must calculate the actual Manhattan distance $|x_i - x_j| + |y_i - y_j|$ for every pair during the greedy check.
        *   Since $N$ is up to 15,000, an $O(N^2)$ check inside binary search is $15000^2 \approx 2.25 \times 10^8$, which might be too slow (TLE) given typical limits (usually $\sim 10^8$ ops/sec, and we have multiple steps).
        *   **Optimization**: Do we need $O(N^2)$?
            *   In the greedy approach, we only compare the current candidate with the *last picked* point. We do NOT need to compare with all previous points.
            *   Why? Because if we pick point $P_i$, and the next point $P_j$ satisfies $dist(P_i, P_j) \ge D$, do we need to check $dist(P_{prev}, P_j)$? No, because $P_{prev}$ was already picked, and we ensured $dist(P_{prev}, P_i) \ge D$. But what about $dist(P_{prev}, P_j)$?
            *   Triangle inequality doesn't directly apply to "min distance" in a simple chain. However, the standard greedy strategy for "maximize min distance on a line" works because on a line, if $A < B < C$ and $dist(A,B) \ge D$ and $dist(B,C) \ge D$, then $dist(A,C) \ge 2D \ge D$.
            *   On a 1D line (perimeter), the distance metric is the arc length. But our metric is Manhattan.
            *   **Critical Question**: Is the Manhattan distance metric on the boundary "metric-like" enough for the greedy strategy to work?
            *   If we linearize the boundary, the "distance" between two points is NOT the difference in their indices. It is the calculated Manhattan distance.
            *   If we use the greedy strategy: Pick $P_1$. Find first $P_i$ such that $dist(P_1, P_i) \ge D$. Pick $P_i$. Find first $P_j$ such that $dist(P_i, P_j) \ge D$.
            *   Does this guarantee that for any two picked points $P_a, P_b$, $dist(P_a, P_b) \ge D$?
            *   Consider points on a circle (perimeter). If we pick $P_1$, then $P_2$ (far enough from $P_1$), then $P_3$ (far enough from $P_2$). Is $P_3$ far enough from $P_1$?
            *   On a circle with arc-length distance, yes, if we pick points spaced by $\ge D$, the gap between non-adjacent picks is larger.
            *   But here, distance is Manhattan.
            *   Example: Square side 10. $P_1=(0,0)$. $P_2=(10, 5)$. $D_M = 15$. $P_3=(0, 10)$.
                *   $dist(P_1, P_2) = 15$.
                *   $dist(P_2, P_3) = |10-0| + |5-10| = 10+5=15$.
                *   $dist(P_1, P_3) = 10$.
                *   If $D=14$, we pick $P_1$, then $P_2$ (dist 15 >= 14). Then we look for next. $P_3$ is dist 15 from $P_2$. We pick $P_3$.
                *   But $dist(P_1, P_3) = 10 < 14$. Fail.
            *   **Conclusion**: The simple greedy strategy (only checking against the last picked point) **FAILS** for Manhattan distance on a square boundary because the "triangle inequality" for the minimum distance doesn't hold in the same way as on a line with the same metric. The "distance" function $d(p, q)$ is not monotonic with respect to the perimeter ordering in a way that preserves the property $d(P_i, P_{i+2}) \ge D$.
            *   **Revised Strategy**: We cannot use simple greedy. We need a different approach.
            *   Since $k$ is small ($k \le 25$), maybe we can use dynamic programming or bitmask?
            *   $N$ is up to 15,000. $O(N \cdot 2^k)$ is too big.
            *   However, $k$ is very small. Can we optimize?
            *   Wait, is there a property of the square boundary?
            *   The boundary is a cycle. We can break the cycle at an arbitrary point (e.g., (0,0)) and duplicate the array to handle wrap-around, or just handle the wrap-around in logic.
            *   Actually, with $k \le 25$, maybe we can iterate on the first point? $N$ choices for first point. Then we need to pick $k-1$ more.
            *   This looks like a variation of the "Maximum Independent Set" on a specific graph, but we want to maximize the minimum weight.
            *   Let's reconsider the constraints. $k \le 25$. $N \le 15000$.
            *   Is it possible the problem intends for us to use the perimeter distance? The problem statement says "Manhattan Distance".
            *   Let's re-read carefully: "points[i] lies on the boundary".
            *   Maybe the test cases are weak or the geometry allows a specific simplification?
            *   No, the counter-example $(0,0), (10,5), (0,10)$ with $D=14$ is valid. $P_1, P_2, P_3$ are on the boundary. $P_1=(0,0)$ (corner), $P_2=(10,5)$ (right edge), $P_3=(0,10)$ (corner).
                *   $P_1 \to P_2$: $10+5=15$.
                *   $P_2 \to P_3$: $10+5=15$.
                *   $P_1 \to P_3$: $0+10=10$.
            *   So simple greedy fails.
            *   We need to check if a subset of size $k$ exists.
            *   Since $k$ is small, can we use **Branch and Bound** or **DP with state compression**?
            *   State: `dp[i][mask]`? No, $i$ up to 15000.
            *   Alternative: Since we are maximizing the minimum distance, we binary search $D$.
            *   Inside `check(D)`: We need to find if there exists a subset of size $k$ with pairwise distances $\ge D$.
            *   This is equivalent to finding a clique of size $k$ in a graph where edges exist if $dist(u,v) \ge D$.
            *   Graph construction is $O(N^2)$. Too slow.
            *   However, the graph has a special structure (points on a cycle).
            *   Can we use DP? `dp[i]` = max points we can pick ending at index `i`?
                *   To compute `dp[i]`, we need `dp[j]` where $dist(j, i) \ge D$.
                *   `dp[i] = 1 + max(dp[j])` for all $j < i$ (in perimeter order) such that $dist(j, i) \ge D$.
                *   This is $O(N^2)$ per check. Still too slow ($15000^2 \approx 2.25 \times 10^8$, times log factor).
            *   Is there a way to optimize the transition?
                *   We need $\max \{ dp[j] \}$ such that $dist(j, i) \ge D$.
                *   $dist(j, i) = |x_j - x_i| + |y_j - y_i|$.
                *   This depends on which sides $j$ and $i$ are on.
                *   Since points are on the boundary, we can categorize them into 4 segments.
                *   Maybe we can process segment by segment?
                *   Or, notice that $k$ is very small ($\le 25$).
                *   Is it possible the intended solution relies on $k$ being small for a different algorithm?
                *   What if we fix the first $k-1$ points? No.
                *   What if we use the fact that we only need to pick $k$ points?
                *   Maybe the "perimeter distance" approximation is actually correct for the *optimal* solution in many cases, but the counter-example proves it's not.
                *   Wait, is the counter-example valid?
                    *   Points: $(0,0), (10,5), (0,10)$.
                    *   Are they on the boundary? Yes.
                    *   Is the Manhattan distance correct? Yes.
                    *   Does the greedy fail? Yes.
                *   So we must solve the general "Max Clique on Unit Disk Graph" (sort of) or "Max Independent Set on Complement" on a geometric graph.
                *   Given $k \le 25$, maybe we can use **Meet-in-the-middle**? No, $2^{12}$ is small, but we need to select from $N$.
                *   Actually, $k$ is small. Maybe we can iterate on the **first point** and then use a greedy-like approach with backtracking?
                *   Or, since $N$ is large, maybe the number of "relevant" points is small? No.
                *   Let's reconsider the constraints. $N \le 15000$. Time limit usually 2s. $O(N^2)$ is risky. $O(N \log N)$ is safe.
                *   Is there a property of Manhattan distance on a square boundary that makes it behave like 1D?
                *   On a square, the Manhattan distance between two points is the length of the shortest path along the grid lines. Since we are constrained to the boundary, the path must stay on the boundary.
                *   Wait, the definition of Manhattan distance is $|x_1-x_2| + |y_1-y_2|$. It does NOT require the path to be on the boundary. It's just the coordinate difference sum.
                *   My counter-example holds.
                *   Is there a constraint I missed? "points[i] lies on the boundary".
                *   Maybe the test cases are generated such that points are somewhat uniformly distributed or $k$ is small enough that $O(N \cdot k)$ or $O(N \cdot k^2)$ works?
                *   If we use DP: `dp[i]` = max points ending at `i`.
                *   Transition: `dp[i] = 1 + max(dp[j])` where $dist(j, i) \ge D$.
                *   Can we optimize finding `max(dp[j])`?
                *   The condition $|x_j - x_i| + |y_j - y_i| \ge D$ defines a region.
                *   Since points are on the boundary, for a fixed $i$, the valid $j$'s form one or two intervals on the perimeter?
                *   Let's check the shape of $|x_j - x_i| + |y_j - y_i| \ge D$ on the boundary.
                *   The function $f(j) = dist(j, i)$ is convex-like on the perimeter?
                *   If $f(j)$ is unimodal (increases then decreases), then the set $\{j : f(j) \ge D\}$ would be two intervals (one before $i$, one after).
                *   If the valid $j$'s are contiguous intervals, we can maintain the max of `dp` in those intervals using a sliding window maximum or segment tree.
                *   **Hypothesis**: For a fixed $i$ on the boundary, the function $g(j) = |x_j - x_i| + |y_j - y_i|$ as $j$ moves along the perimeter is not necessarily unimodal, but the set of $j$ satisfying $g(j) \ge D$ might be decomposable into intervals.
                *   Actually, $|x_j - x_i| + |y_j - y_i| \ge D$ is the complement of a diamond (rotated square) centered at $i$. The intersection of a diamond and the square boundary consists of at most 4 segments. The complement (distance $\ge D$) would be the rest of the boundary, which could be up to 4 intervals.
                *   With up to 4 intervals, we can query the max `dp` in each interval.
                *   We can maintain a Segment Tree or simply use a deque/slide window if the intervals are simple.
                *   Given the complexity of implementing a dynamic segment tree over the perimeter with coordinate transformations, and the constraint $k \le 25$, maybe there's a simpler trick.
                *   **Wait**, $k$ is up to 25. $N$ is 15000.
                *   Maybe the intended solution is $O(N \cdot k)$?
                *   If we fix the first point, can we greedily pick the next? No, greedy failed.
                *   But with $k$ small, maybe we can try all combinations of the first few points?
                *   Actually, there is a known technique for this specific problem ("select k points on a circle to maximize min distance"): If the metric was arc-length, greedy works. With Manhattan, it's harder.
                *   However, notice the constraint: $k \le 25$. This is extremely small.
                *   Could we use **Branch and Bound** with pruning?
                *   Or, since we binary search $D$, inside the check:
                    *   We want to know if there exists a subset of size $k$.
                    *   This is equivalent to: Can we pick $k$ points such that no two are within distance $< D$?
                    *   This is the **Maximum Independent Set** problem on the graph where edges connect points with distance $< D$.
                    *   The graph is an intersection graph of "diamonds" of radius $D$ centered at points, restricted to the boundary.
                    *   Since the points are on a line (topologically), the intersection graph is an **interval graph** (or close to it)?
                    *   If the "distance < D" relation defines intervals on the perimeter, then the graph is an interval graph (or circular interval graph).
                    *   For interval graphs, Maximum Independent Set can be solved in $O(N \log N)$.
                    *   **Key Insight**: Is the set of points $j$ such that $dist(j, i) < D$ a contiguous interval on the perimeter?
                        *   $dist(j, i) < D \iff |x_j - x_i| + |y_j - y_i| < D$.
                        *   This is the interior of a diamond.
                        *   The intersection of a diamond and the square boundary is a connected arc (or empty).
                        *   Therefore, for each $i$, the set of "conflicting" points $j$ forms a contiguous arc on the perimeter.
                        *   This means the conflict graph is a **Circular Interval Graph**.
                    *   **Algorithm for Circular Interval Graph MIS**:
                        *   Break the circle at an arbitrary point.
                        *   Duplicate the array to handle wrap-around.
                        *   For each point $i$, define the interval $[L_i, R_i]$ of points that conflict with $i$ (distance $< D$).
                        *   We need to select max points such that no two share an interval.
                        *   This is the standard "Activity Selection" problem (or Interval Scheduling) but we want to maximize the number of selected intervals (points) such that they don't overlap?
                        *   Wait, the standard problem is: Given intervals, select max number of non-overlapping intervals.
                        *   Here, the "intervals" are the conflicts. We want to select a set of points (vertices) such that no two vertices have an edge between them.
                        *   In the conflict graph, an edge $(i, j)$ exists if $i$ and $j$ conflict.
                        *   If the conflict sets are intervals, the graph is an interval graph.
                        *   For interval graphs, Max Independent Set can be solved greedily?
                        *   **Yes!** For interval graphs, the Maximum Independent Set can be found by sorting intervals by end time and picking greedily?
                        *   Wait, the standard greedy for Interval Scheduling (select max non-overlapping intervals) works.
                        *   Here, our "intervals" are the conflicts. If we pick a point $i$, we cannot pick any point in its conflict interval.
                        *   This is exactly the dual of the standard problem?
                        *   Let's clarify:
                            *   Standard: Given intervals $I_1, \dots, I_N$, select max subset of indices such that $I_a \cap I_b = \emptyset$.
                            *   Our problem: Given points $P_1, \dots, P_N$. Conflict if $dist(P_a, P_b) < D$.
                            *   We want max subset of points with NO conflicts.
                            *   This is exactly: Select max subset of points such that for any pair, they are NOT in each other's conflict interval.
                            *   This is NOT the standard interval scheduling. In standard, we select intervals. Here we select points, and the condition is about the points' relative positions.
                            *   However, if the conflict graph is an interval graph, there is a linear time algorithm.
                            *   Algorithm:
                                1.  Sort points by their position on the perimeter.
                                2.  For each point $i$, determine the range of indices $[l_i, r_i]$ such that for all $j \in [l_i, r_i]$, $dist(i, j) < D$. (Note: this range is contiguous on the sorted perimeter list).
                                3.  Now we have a set of intervals $[l_i, r_i]$. We want to select a maximum subset of indices $\{i_1, \dots, i_k\}$ such that for any pair, $i_a$ is NOT in $[l_{i_b}, r_{i_b}]$ AND $i_b$ is NOT in $[l_{i_a}, r_{i_a}]$.
                                4.  This is equivalent to: Select max points such that no two points "overlap" in their conflict intervals.
                                5.  This is exactly the **Maximum Independent Set on an Interval Graph**.
                                6.  Algorithm for MIS on Interval Graph:
                                    *   Sort the intervals by their right endpoint.
                                    *   Iterate and select an interval if it doesn't overlap with the last selected one.
                                    *   **Wait**: The "intervals" here represent the conflicts of the *points*. If we select point $i$, we "use up" the interval $[l_i, r_i]$? No.
                                    *   If we select point $i$, we cannot select any point $j$ where $j \in [l_i, r_i]$.
                                    *   This is exactly the problem: Given a set of intervals (conflict zones), select max points such that no two selected points have overlapping conflict zones?
                                    *   No. If $i$ and $j$ are selected, they must NOT conflict. So $j \notin [l_i, r_i]$ and $i \notin [l_j, r_j]$.
                                    *   Since the relation is symmetric, this is consistent.
                                    *   This is indeed the Maximum Independent Set on an interval graph.
                                    *   **Greedy Strategy for MIS on Interval Graph**:
                                        *   Sort the "conflict intervals" by their right endpoint.
                                        *   Iterate through the sorted intervals. If the current interval does not overlap with the previously selected interval, select it?
                                        *   **Correction**: The standard greedy for MIS on interval graphs selects the interval that ends earliest.
                                        *   Let's verify: We want to pick a set of vertices (points) that are pairwise non-adjacent.
                                        *   In an interval graph, vertices are intervals. Two vertices are adjacent if their intervals overlap.
                                        *   We want to pick a set of non-overlapping intervals.
                                        *   **YES!** This is exactly the Maximum Independent Set problem on an interval graph, which is solved by the greedy algorithm: Sort intervals by right endpoint, pick the first one, remove overlapping, repeat.
                                    *   **Mapping**:
                                        *   Vertices = Points.
                                        *   Interval for vertex $i$ = The set of points $j$ such that $dist(i, j) < D$. This is a contiguous range $[L_i, R_i]$ in the sorted perimeter list.
                                        *   Condition: $i$ and $j$ are adjacent if $j \in [L_i, R_i]$ (which implies $i \in [L_j, R_j]$).
                                        *   Goal: Select max number of vertices such that no two are adjacent.
                                        *   Solution: Sort the intervals $[L_i, R_i]$ by $R_i$. Greedily pick intervals that don't overlap with the last picked one.
                                        *   Wait, if we pick interval $I_a$, we cannot pick any interval $I_b$ that overlaps $I_a$.
                                        *   This correctly models the problem.

## worker: Sorting points along the perimeter of the square.
The problem asks to select $k$ points from a set on the boundary of a square to maximize the minimum Manhattan distance between any pair. This is a classic "maximize the minimum" problem, solvable via binary search on the answer.

**Key Insight**:
1.  **Binary Search**: We binary search for the maximum possible minimum distance $D$. The range is $[0, 2 \times \text{side}]$.
2.  **Verification (`check(D)`)**: For a fixed $D$, we need to determine if we can select $k$ points such that every pair is at least $D$ apart. This is equivalent to finding the Maximum Independent Set (MIS) on a graph where an edge exists between two points if their Manhattan distance is $< D$.
3.  **Interval Graph Property**: The points lie on the boundary of a square, which is topologically a circle. For any point $i$, the set of points $j$ such that $dist(i, j) < D$ forms a contiguous arc (interval) along the perimeter. This means the conflict graph is an **Interval Graph** (specifically, a circular interval graph).
4.  **Greedy MIS on Interval Graph**: The Maximum Independent Set on an interval graph can be solved greedily in $O(N \log N)$ (or $O(N)$ if already sorted). The algorithm is:
    *   For each point $i$, determine the interval $[L_i, R_i]$ of indices (in the sorted perimeter order) that conflict with $i$ (i.e., $dist(i, j) < D$).
    *   Sort these intervals by their right endpoint $R_i$.
    *   Iterate through the sorted intervals and select an interval if it does not overlap with the previously selected one.
5.  **Efficiency**:
    *   Sorting points along the perimeter takes $O(N \log N)$.
    *   For each binary search step, we compute the intervals $[L_i, R_i]$ for all $N$ points. Since the intervals shift monotonically as we iterate through the points, we can use a two-pointer approach to find $L_i$ and $R_i$ in $O(N)$ total time.
    *   Sorting the intervals takes $O(N \log N)$.
    *   The greedy selection takes $O(N)$.
    *   Total complexity: $O(N \log N + N \log(\text{side}))$. Given $N \le 15000$, this is well within the time limits.

**Edge Cases**:
*   $D=0$: Always possible (return True).
*   $k=1$: Always possible.
*   Points on corners/edges: Handled correctly by the perimeter sorting and distance calculation.
*   Wrap-around: Handled by duplicating the logic or using modulo arithmetic for indices.

## worker: Implement the full solution in the `Solution` clas
1.  **Problem Analysis**: The problem asks to maximize the minimum Manhattan distance between $k$ selected points on the boundary of a square. This is a "maximize the minimum" problem, which is solved using **Binary Search on the Answer**.
2.  **Verification Step**: For a candidate distance $D$, we need to check if we can select $k$ points such that every pair is at least $D$ apart. This is equivalent to finding the **Maximum Independent Set (MIS)** on a graph where an edge exists between two points if their distance is $< D$.
3.  **Interval Graph Property**: Since the points lie on the boundary of a square (topologically a circle), for any point $i$, the set of points $j$ such that $dist(i, j) < D$ forms a contiguous arc (interval) along the perimeter. This makes the conflict graph an **Interval Graph** (specifically, a circular interval graph).
4.  **Algorithm**:
    *   **Sorting**: Sort the points based on their position along the perimeter.
    *   **Interval Construction**: For each point $i$, determine the interval $[L_i, R_i]$ of indices (in the sorted list) that conflict with $i$ (i.e., $dist(i, j) < D$). We use a **two-pointer approach** to find these intervals efficiently in $O(N)$ time. We handle the circular nature by conceptually duplicating the array or using modulo arithmetic.
    *   **Greedy MIS**: The Maximum Independent Set on an interval graph can be solved greedily in $O(N \log N)$ (due to sorting) or $O(N)$ if already sorted. We sort the intervals by their right endpoint and select an interval if it does not overlap with the previously selected one.
    *   **Complexity**: Sorting points takes $O(N \log N)$. The binary search runs in $O(\log(\text{side}))$. Inside the check, interval construction is $O(N)$ and greedy selection is $O(N \log N)$. Total complexity is $O(N \log N + N \log(\text{side}))$, which fits well within the constraints ($N \le 15000$).

## worker: finalize
The solution uses Binary Search on the answer (the minimum distance $D$). The range for $D$ is $[0, 2 \times \text{side}]$.
For a fixed $D$, the problem reduces to finding if there exists a subset of $k$ points such that every pair has Manhattan distance $\ge D$. This is equivalent to finding the Maximum Independent Set (MIS) on a graph where edges connect points with distance $< D$.
Since the points lie on the boundary of a square (topologically a circle), the conflict graph is a **Circular Interval Graph**. The Maximum Independent Set on a circular interval graph can be solved by breaking the circle at an arbitrary point (or trying all possible break points, but here we optimize by trying two cases: including/excluding a specific point) and solving the linear interval graph problem using a greedy algorithm.
1.  **Sort Points**: Sort points along the perimeter.
2.  **Binary Search**: Iterate $D$ from 0 to $2 \times \text{side}$.
3.  **Check Function**:
    *   **Case 1**: Assume point 0 is NOT selected. Solve MIS on points $1 \dots n-1$ (linear).
    *   **Case 2**: Assume point 0 IS selected. Remove its conflict interval and solve MIS on the remaining linear segment(s) for $k-1$ points.
    *   **Linear MIS**: For a linear set of points, compute conflict intervals $[L_i, R_i]$ for each point (using two pointers since the conflict region is contiguous). Sort intervals by right endpoint and greedily select non-overlapping intervals.
4.  **Complexity**: Sorting takes $O(N \log N)$. Binary search takes $O(\log(\text{side}))$. The check function takes $O(N)$ (two pointers + greedy). Total: $O(N \log N + N \log(\text{side}))$.
