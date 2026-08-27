We need to maximize the minimum Manhattan distance among k chosen boundary points. Since all points lie on the square's perimeter, we can transform Manhattan distance on the boundary into a circular distance by "unfolding" the perimeter into a line of length 4*side. For each point, compute its position `p` along this perimeter (0 ≤ p < 4*side) in a consistent direction (e.g., start at (0,0), go right to (side,0), up to (side,side), left to (0,side), down to (0,0)). The Manhattan distance between two boundary points equals the shortest distance along this circular perimeter, i.e., `min(|p_i - p_j|, 4*side - |p_i - p_j|)`.

The problem reduces to: given up to 15000 points on a circle of length L = 4*side, choose k points to maximize the minimum circular distance between any two. This is a classic “maximize minimum distance on a circle” problem, solvable by binary search on the answer `d` and a greedy check: can we select k points such that every pair is at least `d` apart on the circle? The greedy works by sorting points by position, then repeatedly picking the next point that is at least `d` away from the last picked (using circular distance). If we can pick k points, `d` is feasible.

Binary search range: `low = 0`, `high = L // k` (or `L`). Since L ≤ 4·10⁹ and k ≤ 25, the number of iterations is ~32. The greedy check is O(n) per iteration, total O(n log L) ≈ 15000·32 = 480k operations, easily fast.

Edge cases: when `d = 0` always feasible; when `d > L` infeasible. Need to handle the circular wrap‑around: after picking a point near the end, the next valid point may be near the start (distance measured circularly). A simple way: duplicate the sorted list with each point + L, then for each starting point try to greedily pick k points within the next L distance. The maximum count over all starting points is the feasibility answer. Since k ≤ 25, we can also just try each point as a potential first pick (n ≤ 15000, still fine).

Implementation steps:
1. Compute `L = 4 * side`.
2. For each point, compute its perimeter coordinate `p`:
   - On bottom edge (y=0): `p = x`.
   - On right edge (x=side): `p = side + y`.
   - On top edge (y=side): `p = 2*side + (side - x)`.
   - On left edge (x=0): `p = 3*side + (side - y)`.
3. Sort points by `p`.
4. Binary search on `d`:
   - For each candidate `d`, check feasibility:
     - For each index `i` in `0..n-1` as potential first pick:
       - Greedily pick next points: start at `p[i]`, then repeatedly find the smallest index `j` such that `p[j] - current >= d` (using the duplicated array `p2 = p + [p_i + L]`). Count picks; if count ≥ k, feasible.
     - If any start works, `d` feasible.
   - Keep the largest feasible `d`.
5. Return the found `d`.

Complexities: O(n log L) time, O(n) extra space.