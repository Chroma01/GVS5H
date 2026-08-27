
## ideation
The problem is to select `k` points from a set of points on the boundary of a square (side length `side`) so that the minimum Manhattan distance between any two selected points is as large as possible. Points lie on the perimeter, so Manhattan distance between two boundary points equals the shortest distance along the perimeter (a circular metric). This transforms the problem to: given up to 15,000 points on a circle of length `L = 4*side`, choose `k` points to maximize the minimum circular distance between any two.

**Core difficulty**: The feasible region (minimum distance ≥ d) is not simply a set of intervals on a line because the circle wraps around. A classic approach is binary search on the answer `d` and a greedy check: can we pick `k` points such that each is at least `d` away from the previously picked one (circularly)? For a circle, we need to consider that the first pick could be anywhere; we can simulate this by duplicating the sorted positions with an offset of `L` and, for each possible starting position, greedily pick as many as possible within the next `L` distance. If we can pick at least `k` points for any start, `d` is feasible.

**Candidate approaches**:
- Binary search + greedy circular selection: O(n log L) time, easy to implement.
- Pre‑compute all pairwise distances and binary search on them, then check with a graph (max‑clique or independent set?). Not feasible due to constraints.
- DP on sorted positions for line, then adjust for circle. Could work but more complex.
- Direct binary search on distance values is standard for similar problems (e.g., “Aggressive cows” on a circle).

## worker: Implement the perimeter coordinate mapping functio
The mapping function correctly converts each boundary point to a 1D position:
- Bottom edge (y=0): position = x
- Right edge (x=side): position = side + y
- Top edge (y=side): position = 2*side + (side - x)
- Left edge (x=0): position = 3*side + (side - y)

The solution uses binary search on the answer `d` with a greedy feasibility check. For each candidate distance, it tries each point as a potential starting point and greedily selects points at least `d` apart (using the duplicated array to handle circular wrap-around). If it can select `k` points for any starting position, `d` is feasible.

Time complexity: O(n log L) where n ≤ 15,000 and L ≤ 4×10⁹, so about 32 iterations × 15,000 operations = ~480K operations. Space: O(n).
