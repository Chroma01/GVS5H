
## ideation
The core difficulty lies in correctly handling the geometry of points on a square boundary and efficiently checking if a minimum distance `d` is achievable for `k` points.

1.  **Geometry Insight**: Points lie on the perimeter of a square. We can "unfold" the perimeter into a 1D circle of length `4 * side`. Each point can be mapped to a position `p` in `[0, 4*side)`.
2.  **Manhattan Distance vs Perimeter Distance**: The Manhattan distance between two points on the boundary is NOT simply the shortest arc length along the perimeter. However, a key property holds: for any two points on the boundary of a square, the Manhattan distance is equal to the minimum of the clockwise and counter-clockwise path lengths along the boundary *only if* the points are on adjacent sides or the same side in a specific way? Actually, it's simpler: The Manhattan distance $|x_1-x_2| + |y_1-y_2|$ for points on the boundary is always less than or equal to the shortest path along the perimeter. But more importantly, for the purpose of the "maximize minimum distance" problem with a small `k`, a greedy strategy on the sorted perimeter coordinates works.
3.  **Why Greedy Works**: When points are sorted by their perimeter coordinate, the problem resembles selecting points on a circle to maximize the minimum distance. A standard greedy approach for this is: pick the first point, then pick the next point that is at least `d` away (in Manhattan distance) from the last picked point. Because `k` is very small (<= 25), this greedy check is efficient enough if implemented carefully. The number of points `n` is up to 15,000. The check function runs in O(n) time. Binary search adds a factor of log(4*side) ~ 60. Total complexity O(n * log(side)), which is acceptable.
4.  **Circular Nature**: Since the boundary is a loop, we must handle the wrap-around. One robust way is to duplicate the sorted points list (append the first `n-1` points to the end with their perimeter coordinates increased by `4*side`) to simulate the circular nature linearly. Then, for each starting point `i` in the original `n` points, run the greedy check on the extended list starting from `i`. If any start leads to `k` points, `d` is feasible.
5.  **Pitfall**: The Manhattan distance calculation must be done correctly using coordinates, not just perimeter differences. The perimeter difference is an upper bound on the Manhattan distance (actually, it's not always an upper bound, but the Manhattan distance is always <= the shortest perimeter path). We must use the actual Manhattan formula `abs(x1-x2) + abs(y1-y2)`.

Plan:
1. Map each point to its perimeter coordinate.
2. Sort points by perimeter coordinate.
3. Binary search for the answer `d` in range `[0, 4*side]`.
4. In the `check(d)` function:
   - Create an extended list of points by appending the first `n-1` points with perimeter + `4*side`.
   - For each starting index `i` from `0` to `n-1`:
     - Greedily select points: start with `points[i]`, then find the next point in the extended list (starting from `i+1`) whose Manhattan distance from the last selected point is >= `d`.
     - If we can select `k` points, return `True`.
   - If no start index works, return `False`.
5. Return the maximum `d`.
