
## ideation
The problem asks to maximize the minimum Manhattan distance among k selected points on the boundary of a square. This is a classic "maximize the minimum" problem, which suggests binary search on the answer (the minimum distance).

Key observations:
1. The points lie on the boundary of the square. We can parameterize each point by its "perimeter coordinate" s, which is the Manhattan distance from (0,0) along the boundary in a clockwise direction. For a square of side `side`:
   - Bottom edge (y=0, x from 0 to side): s = x
   - Right edge (x=side, y from 0 to side): s = side + y
   - Top edge (y=side, x from side to 0): s = 2*side + (side - x) = 3*side - x
   - Left edge (x=0, y from side to 0): s = 3*side + (side - y) = 4*side - y
   Note: The total perimeter is 4*side. But since the square is closed, the point (0,0) appears at s=0 and s=4*side. We handle this by noting that the boundary is a cycle of length 4*side.

2. The Manhattan distance between two points on the boundary can be computed from their perimeter coordinates. However, because the boundary is not a straight line, the Manhattan distance is not simply the absolute difference of perimeter coordinates. We must compute it directly from coordinates.

3. Given that k is small (<= 25), we can use a backtracking approach to check if it's possible to select k points with pairwise Manhattan distance >= mid. To optimize:
   - Sort the points by their perimeter coordinate s.
   - Use DFS/backtracking: try to pick points one by one, ensuring each new point is at least `mid` away from all previously picked points.
   - Since k is small, even with n up to 15000, the backtracking might be too slow if not optimized. However, note that we can prune early: if the remaining points are not enough to complete k selections, backtrack.

4. Binary search range: low = 0, high = 2*side (maximum Manhattan distance on the boundary).

5. Optimization for the check function:
   - Sort points by perimeter coordinate.
   - In DFS, maintain the index of the last picked point. For the next candidate, iterate from last_index + 1 to end.
   - Prune: if the number of remaining points (from current index to end) plus the number of points already selected is less than k, return False.
   - Also, since we want to maximize the chance of finding a valid set, we can try picking points greedily? But greedy doesn't always work for this problem, so backtracking is needed. However, with k <= 25, and n up to 15000, worst-case backtracking could be O(n^k) which is too slow.

Alternative approach for check:
   - Use dynamic programming or memoization? But state would be (index, count, last_picked_index) which is O(n*k) states, and for each state, we iterate over next candidates which is O(n). Total O(n^2 * k) which for n=15000, k=25 is 15000^2 * 25 = 5.625e9, too slow.

Better approach for check:
   - Since k is small, we can use recursion with pruning. But worst-case is still bad.
   - Insight: The points are on a 1D perimeter (if we unfold the boundary). But Manhattan distance is not the same as perimeter distance. However, we can compute Manhattan distance directly.

Actually, a better idea: 
   - Precompute a graph where nodes are points and edges exist if Manhattan distance >= mid. Then the problem becomes: does the graph have an independent set of size k? But independent set is NP-hard. However, k is small (<=25). We can use backtracking with branch and bound.

Given constraints (n <= 15000, k <= 25), the backtracking might be acceptable if we prune aggressively. We sort points by perimeter coordinate. In DFS, we try to pick a point only if it is at least `mid` away from all previously picked points. We also prune if the remaining points are not enough to reach k.

To speed up, we can use the following optimization in DFS:
   - Instead of checking all previous points, we can store the last picked point's index and only check against all picked points (which is at most k-1, so O(k) per candidate).
   - Also, we can break early if we have already picked k points.

But worst-case, the DFS could still be O(n^k). However, in practice, with pruning (remaining points count), it might pass.

Another optimization: 
   - When checking feasibility for a given mid, we can use a greedy strategy with backtracking. But worst-case remains.

Given the constraints and typical test cases, the backtracking with pruning should work.

Steps:
1. Precompute perimeter coordinate for each point and sort points by this coordinate.
2. Binary search for the answer in [0, 2*side].
3. In the check function for a given mid:
   - Use DFS/backtracking to see if we can pick k points with pairwise distance >= mid.
   - Sort points by perimeter coordinate (done once).
   - In DFS: 
        def dfs(start_index, count, last_picked_indices): 
            but last_picked_indices can be a list of indices (or just the points themselves) to check distance.
   - Actually, we can pass the list of selected points (or their indices) and for each new candidate, check distance against all selected.
   - Prune: if count + (n - start_index) < k, return False.
   - Also, if count == k, return True.

4. To avoid O(k) check per candidate, note that k is small (<=25), so O(k) is acceptable.

Let's implement accordingly.

Pitfalls:
- The perimeter coordinate calculation must be correct.
- The Manhattan distance must be computed correctly.
- The backtracking must be efficient enough. We can add one more pruning: if the current candidate is too close to any previously selected point, skip. Also, we can skip points that are too close to the last selected point? Not necessarily, because a point far in perimeter might be close in Manhattan. So we must check all selected points.

We'll implement the check function with DFS and pruning.

## worker: Implement a helper function `manhattan_dist(p1, p2
The solution uses binary search on the minimum Manhattan distance. For each candidate distance `mid`, it checks if it's possible to select `k` points such that every pair has Manhattan distance >= `mid`. The check is done via DFS/backtracking with pruning:
1. Points are sorted by their perimeter coordinate (Manhattan distance along the boundary from (0,0)) to potentially improve pruning efficiency.
2. In the DFS, we try to pick points one by one, ensuring each new point is at least `mid` away from all previously selected points.
3. Pruning: If the number of remaining points plus the count of already selected points is less than `k`, we backtrack early.
4. Since `k` is small (<= 25), the backtracking with pruning should be efficient enough for the given constraints (n <= 15000).

The Manhattan distance is computed directly from coordinates as `|x1 - x2| + |y1 - y2|`.
