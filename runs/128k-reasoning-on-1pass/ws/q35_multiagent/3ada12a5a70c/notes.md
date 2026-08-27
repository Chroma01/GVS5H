
## ideation
The core difficulty lies in transforming the 2D boundary selection problem into a 1D circular arrangement problem. Since all points lie on the square's boundary, their Manhattan distance is equivalent to the shortest distance along the perimeter. By mapping each point to its clockwise distance from `(0,0)` along the perimeter, we convert the problem into selecting `k` points on a circle of circumference `4 * side` to maximize the minimum circular distance.

Candidate approaches:
1. **Perimeter Mapping + Binary Search**: Map points to `[0, 4*side)`, sort them, and binary search on the candidate minimum distance `D`. For each `D`, verify feasibility by greedily selecting points starting from each possible index and checking if `k` points can be chosen with wrap-around distance `>= D`.
2. **Dynamic Programming / Graph Search**: Overkill and too slow given `side` up to $10^9$.
3. **Two Pointers Optimization**: Could optimize the feasibility check to $O(N)$, but given `k <= 25`, the current $O(N \cdot k \log N)$ check per binary search step is already well within time limits.

Pitfalls:
- Incorrect perimeter mapping order or direction.
- Forgetting to check the wrap-around gap between the last selected point and the first selected point.
- Using `bisect_right` instead of `bisect_left` when searching for `curr + D`.
- Not handling the circular nature correctly (duplicating the array simplifies index management).

The chosen approach efficiently handles all constraints and edge cases.

## worker: <none>
The problem is transformed from 2D boundary selection to 1D circular selection by mapping each point to its clockwise perimeter distance from `(0,0)`. The Manhattan distance on the square's boundary equals the shortest path along the perimeter. 
We binary search on the candidate minimum distance `D`. For each `D`, we verify feasibility in $O(N \log k)$ using:
1. **Two Pointers**: Compute `nxt[i]`, the index of the first point $\ge D$ away clockwise from `i`.
2. **Sparse Table (Binary Lifting)**: Precompute jumps of $2^p$ steps to allow jumping $k-1$ steps in $O(\log k)$.
3. **Greedy Check**: For each possible starting point, jump $k-1$ times and verify the wrap-around gap back to the start is also $\ge D$.
This approach efficiently handles the constraints ($N \le 15000$, $k \le 25$, $side \le 10^9$) with total complexity $O(N \log k \log C)$, well within time limits.
