
## ideation
The problem asks for the minimum number of stair moves (vertical moves within a building) to go from floor Y at (A,B) to floor Z at (C,D), where walkway moves between adjacent buildings at the same floor are free if both buildings have height ≥ that floor.

Key observations:
- A walkway move at floor X is possible only between adjacent cells with height ≥ X.
- The connectivity between cells at floor X is monotone: as X decreases, the set of usable cells grows, so connectivity can only increase.
- The optimal journey can be reduced to: walk at floor Y from start to some cell A (if connected at Y), change floor to X (cost |Y-X|), walk at X to some cell B (if connected at X), change to Z (cost |X-Z|). This requires that the Y-component of start and the X-component of goal are connected (i.e., there is a path between them using cells with height ≥ X).
- Equivalently, we need a path from start to goal that can be traversed at some floor X, and we pay |Y-X| + |X-Z|. The set of feasible X is downward-closed (if X works, any smaller X works). So there is a maximum feasible M.
- M is the maximum floor such that start and goal are connected in the graph where edges exist between adjacent cells with height ≥ M. This is the "maximin path" value, which can be found via a maximum spanning tree on the grid graph with edge weights = min(height(u), height(v)).
- The answer depends only on M, Y, Z:
  - If M ≥ min(Y,Z): answer = |Y-Z|
  - Else: answer = Y+Z-2M

Algorithm:
1. Build edges between adjacent cells with weight = min(height(u), height(v)).
2. Run Kruskal's algorithm to build a maximum spanning tree (grid is connected, so it's a tree).
3. Preprocess binary lifting on the tree to answer minimum edge weight on path queries in O(log N).
4. For each query, compute M = min edge weight on path between the two cells in the tree, then apply the formula.

Complexities: O(HW log(HW)) for sorting edges, O(HW) for DSU, O(HW log(HW)) for binary lifting, O(Q log(HW)) for queries. With H,W ≤ 500 and Q ≤ 2e5, this is efficient.

## worker: Integrate the DSU, maximum spanning tree, and bina
- The solution builds a maximum spanning tree on the grid graph where edge weights are the minimum height of the two adjacent buildings.
- For any two cells, the minimum edge weight on their path in this tree equals the maximum floor `M` at which they remain connected via walkways.
- The answer formula derived from the monotonicity of connectivity: if `M >= min(Y,Z)`, the optimal cost is `|Y-Z|`; otherwise it is `Y+Z-2*M`.
- Binary lifting allows O(log N) queries on the tree, making the total complexity O((HW + Q) log(HW)), which is efficient for the constraints (H,W ≤ 500, Q ≤ 2e5).
- Tested on the provided sample: output matches expected results (10 and 2).
