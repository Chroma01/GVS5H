
## ideation
The problem involves moving in a city grid with buildings of varying heights. Takahashi can move between adjacent buildings at the same floor using walkways (cost 0) or change floors within a building using stairs (cost 1 per floor). The goal is to minimize the number of stair uses between given start and end states.

Key observations:
- The cost depends only on vertical moves; horizontal moves are free.
- For any two buildings, the maximum height at which they can be connected via walkways is determined by the bottleneck (minimum edge weight) along the best path, where edge weight between adjacent buildings is `min(F[u], F[v])`.
- This bottleneck can be found using a maximum spanning tree of the grid graph, where the tree path between two nodes gives the maximum possible bottleneck.
- For a fixed path with minimum edge weight `m` between start and end buildings, the optimal stair usage is:
  - If `m >= min(Y, Z)`: cost = `|Y - Z|`
  - Else: cost = `Y + Z - 2*m`
  This follows because we can descend to height `m` (or any feasible height between `Y` and `Z`) and then ascend, with the total vertical distance being minimized.

Algorithm:
1. Build a maximum spanning tree of the grid using Kruskal's algorithm with edge weights `min(F[u], F[v])`.
2. Preprocess the tree for LCA with binary lifting, storing the minimum edge weight along paths to ancestors.
3. For each query, find the minimum edge weight `m` on the tree path between start and end buildings.
4. Compute the answer using the formula above.

Constraints: H, W ≤ 500 (N ≤ 250,000), Q ≤ 200,000. The approach runs in O(N log N + Q log N), which is efficient.

## worker: Implement the solution in Python: read H, W and th
The solution builds a maximum spanning tree of the grid graph where edge weights are `min(F[u], F[v])`. The tree path between any two buildings gives the maximum bottleneck height `m` at which they can be connected via walkways. For a query, the optimal stair usage is `|Y-Z|` if `m >= min(Y,Z)`, otherwise `Y+Z-2*m`. LCA with binary lifting answers each query in O(log N). The overall complexity is O((N+Q) log N) which fits constraints (N ≤ 250k, Q ≤ 200k).
