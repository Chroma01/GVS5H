We are given a grid of buildings with heights `F[i][j]`. Movement costs are: (1) stairs cost 1 per floor change, (2) walkways allow moving between adjacent buildings at the same floor X, provided both buildings have height ≥ X.

For a query from floor Y at (A,B) to floor Z at (C,D), we want to minimize stairs. Walkways are free but restricted by floor height.

Key idea: For any floor X, consider the subgraph of buildings with height ≥ X. The walkways allow us to traverse connected components in this subgraph. To move from Y to Z, we can choose intermediate floors X1, X2, ... where we walk at that floor, and use stairs only to change floors.

The optimal strategy is: use stairs to change from Y to some floor Y', walk through connected components at floor Y', change to another floor, etc., eventually reaching floor Z.

The key observation: the number of stairs used is sum of |X_k - X_{k-1}| over the floor changes. So we want to minimize total vertical distance, but we are constrained that we can only "teleport" (walk) between connected components at specific floors.

The critical insight: the set of reachable building-floor pairs without using stairs is a set of (cell, floor) where the floor X is ≤ min height along the path. Actually, if we fix a floor X, we can move through any building of height ≥ X via walkways.

But we can also go up/down by stairs. So effectively, we have a state (i,j, X) but X is bounded by F[i][j].

The classic solution: precompute for each cell the maximum floor `H[i][j] = F[i][j]`. The movement constraints: we can walk between adjacent cells if both have height ≥ X. This is like having a "skyline" where for floor X, the graph of cells with height ≥ X is some connected components.

A query is: start at (A,B,Y), end at (C,D,Z). Minimum stairs.

Observation: It's always optimal to "go up or down" in one continuous motion at a single building, or use walkways at a fixed floor. Actually, we can model this as: we can move freely at any floor X, but we must be in a building with height ≥ X. The cost is the total floor difference traveled.

This can be solved by BFS on a graph where nodes are cells and edges have costs related to height. But Q is up to 2e5, H,W up to 500, so we need a fast query solution.

The standard approach: Build a union-find or BFS from the query cells. Actually, we can precompute for each cell the "height profile" - for each possible height X, the connected component of cells with height ≥ X. But there are 1e6 floors.

Alternative: The answer is the minimum over all paths of sum of absolute differences in floors. This is equivalent to: the minimum vertical distance to go from Y to Z, given that you can "teleport" for free if there is a path of buildings with height ≥ the teleport floor.

This is exactly the problem of finding the minimum L1 distance in a graph where you can move horizontally for free if the height is sufficient.

Wait, actually, you can walk on any floor X, as long as all buildings in your path have height ≥ X. So the "walkable" graph for floor X is the subgraph of cells with F ≥ X. This graph changes as X changes.

A known solution: For each cell, we can think of the "maximum floor we can reach from this cell without stairs" in each direction, but that's complex.

Another approach: We can perform a multi-source BFS from all cells, but Q is 2e5.

Actually, the query asks: min stairs from Y to Z. This is equivalent to: we can choose a sequence of floors Y = x0, x1, ..., xk = Z, and paths between consecutive cells at those floors. The cost is sum |xi - x_{i-1}|. The path at floor xi must be through buildings of height ≥ xi.

This means we can reduce the problem: The answer is the minimum total vertical distance such that we can connect the start and end via walkways at those floors.

If we can go from (A,B) to (C,D) at floor X (i.e., they are in the same component of cells with height ≥ X), then we can reach Z from Y by stairs: we go down/up to X, walk, then go to Z. The cost would be |Y-X| + |Z-X|. But we might need to change floors multiple times: e.g., if the cells are not connected at any single floor, we might need to use multiple floors.

This is similar to: we have a grid where we can "teleport" between cells if there is a path of sufficient height. The cost is the total vertical movement.

Actually, we can solve this with a BFS on a state (i,j) with dynamic programming, but the state space is huge.

Better: We can think of this as a graph where the "height" of a cell is a resource. We can move between adjacent cells at cost 0 if we choose a floor ≤ min of the two heights. We want to minimize the total "floor change" cost.

This is exactly the problem of finding the minimum cost to go from (A,B,Y) to (C,D,Z) where moving horizontally requires the floor to be ≤ min(heights), and moving vertically costs 1 per floor.

This can be solved by building a graph where we have a node for each cell, and edges with weights based on the maximum height we can traverse. Actually, if we are at cell (i,j) and we want to move to adjacent (i',j'), we can do so for free at any floor X ≤ min(F[i][j], F[i'][j']). So we can traverse that edge at any floor X ≤ min_h.

This means we can model the problem as: we have a graph G of cells. We want to find a path from A to C. Along the path, we will have a sequence of cells. For each edge in the path, we choose a floor X_e ≤ min(F[u], F[v]). The total cost is the sum of absolute differences between consecutive X's, plus |Y - X_first| + |Z - X_last|.

This is like: we have a path, and we want to assign a value X to each vertex (the floor at which we leave that vertex) such that X ≤ F[v] for each v, and we minimize the total variation |X_v - X_u| for edges plus the boundary terms.

Actually, the floor changes happen at vertices. At each vertex, we are at some floor. When we move to an adjacent vertex, we can only move at floor X where X ≤ min(F[u], F[v]). So the sequence of floors must satisfy: for each step, the floor X is ≤ the minimum height of the two cells.

So the path is a sequence of cells v0, v1, ..., vk with v0=(A,B), vk=(C,D). We assign a floor value x_i to each vertex (the floor we are at when we leave vi, or the floor we arrive). The constraints: 1 ≤ x_i ≤ F[v_i], and |x_i - x_{i+1}| is the cost of stairs, but wait: if we walk from vi to v_{i+1} at floor x, then we are at floor x at both. So x_i and x_{i+1} should be equal? No, the stairs are used to change floors. We can change floors at a cell, then walk to the next cell.

So the sequence is: start at Y at v0. We can take stairs to some floor y0 ≤ F[v0]. Then walk to v1 (requires y0 ≤ F[v1]). Then at v1, we can take stairs to y1 ≤ F[v1], then walk to v2 (requires y1 ≤ F[v2]), etc. At the end, at vk, we take stairs to Z.

The cost is |Y - y0| + sum_{i=0}^{k-1} |y_i - y_{i+1}| + |y_k - Z|.

But we can also combine: the total vertical distance is the total variation of the sequence of floors we visit at each cell. Actually, it's the total absolute difference between consecutive floors in the path, plus the start and end differences.

We can choose to stay at the same floor, or change. The constraint is that at each cell vi, the floor we are at when leaving must be ≤ F[vi]. And when walking to v_{i+1}, the floor must be ≤ F[v_{i+1}] as well. So effectively, the floor assigned to the edge (vi, v_{i+1}) must be ≤ min(F[vi], F[v_{i+1}]).

This is equivalent to: we choose for each edge e=(u,v) a floor x_e ≤ min(F[u], F[v]). The cost is the total variation along the path: sum |x_{e_i} - x_{e_{i+1}}| + |Y - x_{e_0}| + |Z - x_{e_{k-1}}|.

We want to minimize this over all paths and all assignments.

This is a min-cost path problem in a state space where the state is the current floor. But the floor is up to 1e6, so we cannot do standard BFS.

However, we can observe that the optimal solution can be found by considering the "profile" of the path. The floors we use will be determined by the minimum of the heights along the path.

Actually, the optimal strategy is: we can only walk at a floor X if there is a path of buildings with height ≥ X connecting the two points. So the set of reachable (cell, floor) pairs without stairs is: for each cell, all floors 1..F[cell]. But we can move between cells at the same floor X if they are adjacent and both have height ≥ X.

So the "walkable" relation is: two cells are connected at floor X if there is a path of cells with height ≥ X between them.

Thus, for a fixed floor X, the graph G_X has edges between adjacent cells where min(F[u],F[v]) ≥ X. This graph is the same as the subgraph of the grid induced by cells with F ≥ X.

Now, for a query, we can go from Y to Z by:
- Choosing a sequence of floors X_0, X_1, ..., X_m.
- For each i, we are in some connected component of G_{X_i}.
- The cost is sum of |X_i - X_{i-1}|.

We start at floor Y at (A,B). We can only move within the component of (A,B) in G_Y (actually, we are at floor Y, so we are in G_Y). We can take stairs to change to another floor X, which puts us in the component of (A,B) in G_X (assuming we are still at (A,B)), etc.

The key is: the component of a cell in G_X changes only at heights that are in the set of F values.

This is a classic problem: we can solve queries offline by sorting by floor, or we can use the concept of "union-find" on the grid as we decrease the floor.

Actually, we can solve this with a Dijkstra-like approach on a graph where we treat the cells as nodes, but the cost to move from (i,j,X) to (i,j,X-1) or (i,j,X+1) is 1 (stairs), and from (i,j,X) to (i',j',X) is 0 if adjacent and both have height ≥ X.

But the state space is H*W*maxF, which is 500*500*1e6 = 2.5e11, too large.

However, we can compress the floors. For a cell, the set of reachable floors is 1..F[i][j]. The edges only exist at floors ≤ min(F[u],F[v]). This is a "layered" graph.

We can think of it as: we have a grid, and for each cell, we have a vertical line of nodes from 1 to F[i][j]. Edges:
- vertical: (i,j,x) to (i,j,x+1) with cost 1.
- horizontal: (i,j,x) to (i',j',x) with cost 0 if adjacent and x ≤ F[i'][j'].

The start is (A,B,Y), end is (C,D,Z).

This is a graph with O(sum F) nodes and O(sum F + E) edges. Sum F is up to 500*500*1e6 = 2.5e11, too large.

But we can compress the vertical dimension. Notice that we only care about floor values that are either Y, Z, or F[i][j] for some cell on the path. Actually, the cost is the total vertical distance, which is like the L1 norm.

We can solve this by considering that the optimal path will only change floors at "critical" heights: the heights of buildings.

In fact, we can solve the problem with a BFS on the grid where the state is just the cell, but we keep track of the current floor as a value, and the cost is the current floor distance to target, but we need exact minimum.

Another perspective: The answer is the minimum over all paths P from (A,B) to (C,D) of the minimum total floor variation, which is equal to: the maximum over the path of the minimum height along the path? No.

Let's think about the continuous version. We want to go from Y to Z, and we can move horizontally at any floor X ≤ F[cell]. The cost is the total variation of X. This is exactly the L1 length of a path in the space where we can "lower" the floor for free if the building is tall enough.

Actually, if we consider the floor X as a "potential", we want to find a path that minimizes the total variation of X, subject to X ≤ F[cell] at each cell.

This is like finding a path in a graph where the node values are bounded above by F[cell]. We want to assign a value x(v) to each node v on the path such that 1 ≤ x(v) ≤ F[v], and minimize |Y - x(start)| + |x(start) - x(v1)| + ... + |x(vk) - Z|.

But note: the walk from v to w at floor x requires x ≤ F[v] and x ≤ F[w]. So the floor used on the edge (v,w) must be ≤ min(F[v],F[w]). If we assign x(v) to each vertex, then we need x(v) = x(w) for the edge to be traversed at that floor? Actually, we can change floors at v, then walk to w at the new floor. So the floor when walking from v to w is some x ≤ min(F[v],F[w]). This x can be different from the floor we arrived at v, but we can change floors at v using stairs.

So the cost includes the stairs at v. The sequence of floors at v is: we arrive at floor x_in, we take stairs to x_out, then walk to neighbor. The cost is |x_in - x_out|.

So the total cost is the sum of absolute differences between consecutive x values along the path, plus the start and end.

We can choose to not change floors at many vertices. The optimal solution will change floors only when necessary: i.e., when the path is blocked at the current floor.

This is equivalent to: we have a graph where we can move from cell u to cell v at floor X if min(F[u],F[v]) ≥ X. The "state" is (cell, floor). We want min stairs from (A,B,Y) to (C,D,Z).

We can solve this with a multi-source BFS if we process queries, but Q is 2e5, which is too many for BFS per query.

We need a global preprocessing. The grid is up to 500x500 = 2.5e5 cells. We can compute something for all pairs? No.

But note: the grid is small: 500x500. We can precompute distances between all pairs of cells? That would be 2.5e5^2, too large.

However, the cost is not just shortest path in a graph with fixed weights; it depends on the floor.

Another idea: For each cell, we can compute the "minimum stairs to reach any other cell from floor Y". But Y varies.

Wait, the problem is equivalent to: we have a matrix F. We can move from (i,j) to (i',j') with cost 0 if there is a path of cells with min height ≥ X, but we can also change X with cost 1 per unit.

This is exactly the problem of finding the minimum L1 distance in a "terrain" where we can walk at elevation X, and we pay for elevation changes.

Actually, we can solve this by considering the "dual" graph or by using a min-cost max-flow or by building a graph where we add edges based on height.

There is a known solution for this problem (it's from AtCoder, likely). The constraints H,W ≤ 500 suggest O(HW log(HW)) or O(HW α) preprocessing.

The standard solution: Build a graph with H*W nodes. For each adjacent pair (i,j) and (i',j'), let h = min(F[i][j], F[i'][j']). Add an edge between them with weight h. But the cost is not directly h; the cost to move between them is related to the floor.

Actually, if we consider the floor as the "height" we are at, and we can move horizontally only at floor ≤ min height, then the maximum floor at which we can move between two cells is the min height of the two cells. So we can think of the "bottleneck" height for an edge.

For a path, the set of floors at which we can traverse the entire path is the minimum of the min-heights of edges along the path, which is the minimum over the path of the minimum adjacent height, but that's not simple.

Wait, for a path v0, v1, ..., vk, the condition to walk at floor X is that for each i, X ≤ min(F[v_i], F[v_{i+1}]). This is equivalent to X ≤ min_i min(F[v_i], F[v_{i+1}]). Let M(P) = min_{i} min(F[v_i], F[v_{i+1}]). Then we can walk at any floor X ≤ M(P).

If we walk at floor X, the cost is |Y-X| + |Z-X| if we just go down/up once. But we might need to change floors in the middle.

However, if we can walk at floor X, we can also walk at any lower floor. So if we want to minimize |Y-X| + |Z-X|, we would choose X = clamp(Z, 1, Y) or something. Actually, for a given X, the cost to go from Y to Z via floor X is |Y-X| + |Z-X|. We can also choose to not go via a single X but multiple.

But the key is: we can only change floors at cells. So we need to consider the connectivity at various floors.

This problem can be solved by building a graph where the nodes are the cells, and we add edges with "height" attribute. Then for each query, we need to find the minimum cost.

Since H,W ≤ 500, we can precompute for each cell the "height profile" to all other cells? No.

But we can use the fact that the grid is small to run a BFS from every cell, but 2.5e5 BFS is too much.

Alternative: We can compute the minimum cost to go from any cell to any other cell for a given starting floor? That seems hard.

Another approach: The problem is symmetric. We can think of it as: we are allowed to move from (i,j) to (i',j') with cost 0 if we choose a floor X ≤ F[i][j] and X ≤ F[i'][j']. This is like having a "resource" X that we can carry, and moving to an adjacent cell requires X ≤ min(F[u],F[v]).

We want to minimize the total change in X.

This is exactly the problem of finding a path in a graph where the cost is the total variation of a label, subject to label ≤ node capacity.

We can solve this with a min-cut or by transforming the graph.

Consider constructing a new graph: for each cell (i,j), create a node. Also, consider the values of F. Sort the cells by F.

We can process cells in decreasing order of F. When we process a cell, we can "activate" it at its height. We can use union-find to connect cells that are adjacent and have height ≥ current height.

For a query (A,B,Y) to (C,D,Z), we can think of it as: we need to find a sequence of heights.

Actually, we can solve the problem by reducing to a standard shortest path on a graph with H*W nodes, but where the edge weight depends on the height.

Wait, there is a known trick: we can transform the floor changes into edge weights.

Consider two adjacent cells u and v. Let h = min(F[u], F[v]). If we are at floor X ≤ h, we can move from u to v for free. If we are at floor X > h, we cannot move directly; we would have to change floors.

But we can change floors at any cell with cost 1 per floor.

This is similar to: we have a terrain where the "altitude" is the floor, and we can walk horizontally at altitude X if the terrain is at least X at both cells. We want to minimize the total climb/descent.

Actually, if we think of F[i][j] as the maximum altitude we can be at in that building. Then walking at altitude X is possible if both buildings have F ≥ X.

So for a fixed altitude X, the walkable graph is the subgraph of cells with F ≥ X. The connected components of this graph are the regions where we can walk freely at altitude X.

Now, to go from (A,B,Y) to (C,D,Z), we can choose a path that changes altitude at certain cells. The optimal path will have the property that we only change altitude when necessary: when the current altitude is too high for the next edge.

Specifically, if we are at cell u at altitude X, and we want to go to neighbor v, we can do so if X ≤ F[v]. If not, we need to decrease altitude (take stairs down) at u to some X' ≤ F[v], then walk to v at X'. The cost is X - X' (if we go down) or X' - X (if we go up), but we can also go up if needed.

Actually, we can always go up or down at cost 1 per floor. So from altitude X, we can reach any altitude Y at the same cell with cost |X-Y|.

So the problem is: find a path from A to C, and for each vertex u on the path, assign an altitude x_u such that:
- 1 ≤ x_u ≤ F[u]
- |x_u - x_{prev}| + |x_u - x_{next}| ... wait, the cost is the sum of |x_u - x_v| for consecutive vertices? No.

When we walk from u to v, we are at altitude x_u when we leave u, and we arrive at v at altitude x_u (since we walked at that altitude). Then at v, we may change to x_v with cost |x_u - x_v|. Then walk to next at x_v, etc.

So the sequence of altitudes is: at start: Y. We can change at A to some y0 ≤ F[A] with cost |Y - y0|. Then walk to neighbor v1 at y0 (requires y0 ≤ F[v1]). At v1, change to y1 with cost |y0 - y1|, etc. At end, at C, we change to Z with cost |yk - Z|.

The constraints: y0 ≤ F[A], y0 ≤ F[v1], y1 ≤ F[v1], y1 ≤ F[v2], ..., yk ≤ F[C].

So the sequence of altitudes y0, y1, ..., yk must satisfy y_i ≤ F[v_i] for all i, and y_i ≤ F[v_{i+1}] (since we walk from v_i to v_{i+1} at altitude y_i). So actually, y_i ≤ min(F[v_i], F[v_{i+1}]).

But note that y_i is the altitude at which we leave v_i and arrive at v_{i+1}. So it must be ≤ F[v_i] and ≤ F[v_{i+1}].

So the constraints are: for each i from 0 to k, y_i ≤ F[v_i] and y_i ≤ F[v_{i+1}] (with v_{k+1} = end cell C, and v_0 = start cell A? Actually, y0 is used for edge (v0, v1), so y0 ≤ F[v0] and y0 ≤ F[v1]. y1 ≤ F[v1] and y1 ≤ F[v2]. etc. yk ≤ F[vk] and yk ≤ F[C].

The cost is |Y - y0| + sum_{i=0}^{k-1} |y_i - y_{i+1}| + |yk - Z|.

We want to minimize this over all paths and all choices of y_i.

This is a min-cost path problem on the graph where the state is (cell, altitude), but we can compress because the altitudes are bounded by the F values.

Since H*W ≤ 2.5e5, and F can be large, we need to be careful.

However, we can observe that the optimal y_i will be chosen from the set of F values or Y or Z. Actually, since the cost is linear and the constraints are upper bounds, the optimal y_i will be either as high as possible or as low as possible relative to the constraints. But not exactly.

Another observation: the problem is equivalent to finding the shortest path in a graph where we add a "height" dimension. We can solve it by building a graph with (H*W) nodes, and for each cell, we have a "height" that we can adjust.

But there is a known solution for this problem: we can precompute for each cell the "maximum floor reachable without stairs" in the four directions, and then use a Dijkstra-like algorithm with a state of (cell, floor). But the floor is up to 1e6.

Wait, we can solve the problem by reducing it to a standard graph problem by adding "stair" edges.

Consider the following graph: nodes are (i,j). For each node, we have a value F[i][j]. We can think of the floor as a "resource" that we can increase or decrease at cost 1.

This is similar to the problem of "minimum cost to go from A to B where you can move horizontally if the resource is sufficient, and you can adjust the resource at nodes".

We can solve this with a BFS on a graph where we keep track of the current floor, but we only care about the floor when it matters: i.e., when we are at a cell, the only thing that matters is the current floor relative to the neighbors' F.

Actually, we can do a multi-source BFS from the start cell at all floors? No.

Another idea: Since the grid is only 500x500, we can precompute the "minimum cost to reach each cell from the start" for the specific query, but Q is 2e5.

But we can precompute something global: the "height profile" of the grid. For each cell, we can compute the minimum cost to reach any other cell for each possible starting floor? That is 2.5e5 * 1e6, too large.

However, the floor is up to 1e6, but the number of distinct F values is at most 2.5e5. So we can compress the floors.

We can think of the problem as: we have a grid with heights F. We can move horizontally at any level X ≤ F[cell]. The cost is the total vertical movement.

This is exactly the problem of finding the minimum L1 path length in a "mountain range" where you can walk at constant elevation if the terrain is high enough, and you pay for elevation changes.

I recall a similar problem: "Walking on a grid with heights, minimize the total vertical distance". The solution is to build a graph where the nodes are the cells, and the edge weights are the absolute difference in heights? No.

Let's think about the continuous case. Suppose we have a function h(x,y) = F[i][j] on the grid. We want to find a path from A to B that minimizes the total variation of the z-coordinate, subject to z ≤ h(x,y) at all points.

This is like finding a path in 3D. We can project to 2D.

Actually, we can transform the problem by considering the "upper envelope" or by using the fact that we can only go up to F[i][j].

One approach: We can solve each query with a BFS on the state (i,j, current_floor), but we need to handle the large floor.

Since the grid is small (500x500 = 2.5e5 cells), and Q is 2e5, we can afford O(HW) per query? 2e5 * 2.5e5 is too much.

We need something like O(log(HW)) or O(1) per query after O(HW) or O(HW log HW) preprocessing.

Is the answer simply the absolute difference in some "heights"? No, because of the walkways.

Consider the sample: from (1,1,10) to (3,1,6). The straight Manhattan distance is |1-3|+|1-1| = 2. The answer is 10. So we need to go down 4, walk, then up 3, etc.

In the sample, the path uses multiple floor changes.

We need a way to compute the minimum stairs efficiently.

I recall a solution for this problem (it's from AtCoder ABC 305 F or similar? Actually, it's from a recent contest). The constraints H,W ≤ 500 and Q up to 2e5 suggest that we can precompute something like "the minimum cost to go from any cell to any other cell if we start at the maximum floor" or something.

Wait, maybe we can reduce the problem to finding the minimum cost path in a graph with H*W nodes, where the edge weight between (i,j) and (i',j') is something like the absolute difference of the minimum height along the path? Not exactly.

Another idea: The problem is equivalent to: we can move from (i,j) to (i',j') with cost 0 if there is a path of cells with min height ≥ X. The cost to change from X1 to X2 is |X1-X2|.

This means that if we fix the path, the optimal floors are determined by the constraints. In fact, the optimal sequence of floors is the "lower envelope" of the path and the start/end.

Specifically, for a fixed path, we can think of the maximum floor we can maintain along the path: it is limited by the minimum F along the path. So we can walk at any floor X ≤ min_path_F.

But we can also change floors at intermediate cells. The optimal strategy is to "hug" the lower bound: we want to stay as high as possible to minimize stairs? Actually, if we stay high, we can cover more ground without stairs, but we might have to go down to pass under low buildings.

This is similar to the "minimum cost to traverse a graph with height constraints".

I think the correct approach is to model this as a shortest path problem on a graph where we have edges for stairs and walkways, but we need to compress the vertical dimension.

Since the floor only changes when we use stairs, and stairs are only used at buildings, we can think of the state as (cell, floor) but we can compress consecutive floors that have the same connectivity.

For a fixed cell, the connectivity to neighbors changes only at floor values that are equal to F[neighbor] for some neighbor. So we can compress the vertical dimension to the set of distinct F values plus the query Y and Z.

But the number of distinct F values is 2.5e5, so the graph would have 2.5e5 * 2.5e5 = 6.25e10 nodes, too large.

However, we don't need to keep all floors. We only need to know, for each cell, the "profile" of the maximum reachable floor in each direction.

Another approach: We can precompute for each pair of adjacent cells, the minimum height h = min(F[u],F[v]). This is the maximum floor at which we can walk between them.

Now, for a query, we need to find a path from A to C. The cost of using a path is the minimum over all floor assignments of the total variation. This is like: we have a path with edges, each edge has a maximum floor h_e. We want to assign a floor x_e to each edge such that x_e ≤ h_e, and we want to minimize the total variation |Y - x_{e0}| + sum |x_e - x_{e'}| + |x_{ek} - Z|, where the sum is over consecutive edges in the path.

But note that when we traverse the path, we visit vertices. At each vertex, we may have multiple edges. The floor at which we arrive from one edge and leave to another may be different, but the stairs are taken at the vertex.

Actually, the sequence of floors is associated with the vertices: we are at floor x_v at vertex v. When we move to neighbor w, we must have x_v ≤ F[w] and x_v ≤ F[v] (which is true). So the constraint is x_v ≤ F[v] and x_v ≤ F[w] for the edge (v,w). This means that x_v ≤ min(F[v], F[w]) for each incident edge used.

So the path is a sequence of vertices v0, v1, ..., vk. We assign x_i to v_i. The constraints: x_i ≤ F[v_i] for all i, and also x_i ≤ F[v_{i+1}] for i=0..k-1. So x_i ≤ min(F[v_i], F[v_{i+1}]).

The cost is |Y - x0| + sum_{i=0}^{k-1} |x_i - x_{i+1}| + |xk - Z|.

We want to minimize this over all paths and assignments.

This is a classic problem: it can be solved by finding the minimum cost path in a graph where the edge weights are defined by the constraints.

Notice that the constraints only involve upper bounds. The cost is convex (L1). The optimal x_i will be chosen as high as possible or as low as possible.

In fact, the optimal solution is: x_i = min( F[v_i], F[v_{i+1}] , something )? Not exactly.

We can think of the problem as: we have a sequence of upper bounds. We want to choose x_i to minimize the total variation, with the constraint x_i ≤ U_i, where U_i = min(F[v_i], F[v_{i+1}]).

But also x_i ≤ F[v_i] is implied if we set U_i = min(F[v_i], F[v_{i+1}])? Not exactly: for the first vertex v0, the constraint from the edge (v0,v1) is x0 ≤ min(F[v0], F[v1]), and also x0 ≤ F[v0] (redundant). For the last vertex vk, constraint is xk ≤ min(F[vk-1], F[vk]) and xk ≤ F[vk] (redundant). For interior vertices, we have two constraints: x_i ≤ min(F[v_i], F[v_{i-1}]) from the left edge, and x_i ≤ min(F[v_i], F[v_{i+1}]) from the right edge. So x_i ≤ min( F[v_i], F[v_{i-1}], F[v_{i+1}] ). But the left and right constraints are both upper bounds, so x_i ≤ min( min(F[v_i], F[v_{i-1}]), min(F[v_i], F[v_{i+1}]) ) = min(F[v_i], F[v_{i-1}], F[v_{i+1}]).

So overall, the constraint is x_i ≤ F[v_i] and for each incident edge (v_i, v_j), x_i ≤ F[v_j].

Thus, x_i ≤ min( F[v_i], min_{j neighbor on path} F[v_j] ).

But the path is not fixed.

This looks like we need to find a path and assign values.

We can reformulate: the problem is equivalent to finding a path from A to C in a graph where we can move from u to v at "level" X if X ≤ min(F[u],F[v]). The cost is the total variation of X.

This is exactly the problem of finding a path with minimum "total variation" in a graph with node capacities.

There is a known technique: we can transform the graph by adding a "super source" and "super sink" or by using a min-cost flow.

Another idea: We can solve the problem by building a graph with H*W nodes, and for each node, we add a "height" edge to a global node, but that doesn't work.

Wait, I recall a solution for this problem: we can precompute for each cell the "maximum floor" we can reach without stairs, and then use a union-find to find connected components at each floor, and then answer queries by finding the minimum floor X such that A and C are connected in G_X, and then compute |Y-X| + |Z-X|? But in the sample, the answer is 10, and the minimum X such that they are connected? Let's check the sample.

Grid:
12 10 6
1 1 3
8 6 7

Query 1: (1,1,10) to (3,1,6).
The cells: (1,1)=12, (3,1)=8.
At floor 10: cells with F≥10: (1,1) only. So (1,1) and (3,1) are not connected at floor 10.
At floor 8: (1,1), (1,2)=10, (3,1)=8, (3,2)=6, (3,3)=7. Also (1,3)=6 is not. (2,*) are 1, so not. So at floor 8, the component of (1,1) includes (1,1), (1,2). (3,1) is separate. Not connected.
At floor 7: (1,1), (1,2), (3,1), (3,2), (3,3). Are (1,1) and (3,1) connected at floor 7? We need a path of cells with F≥7. (1,1) to (1,2) ok. (1,2) to (1,3)? F[1,3]=6, so no. (1,2) to (2,2)? F=1, no. So (1,1) and (1,2) are isolated from the rest. (3,1) to (3,2) to (3,3) are connected. So not connected.
At floor 6: (1,1), (1,2), (1,3), (3,1), (3,2), (3,3). But are they connected? (1,3) to (2,3)? F=3, so at floor 6, (2,3) is not included. So (1,3) is only connected to (1,2). (1,2) to (1,1). (3,1) to (3,2) to (3,3). (2,3) is height 3, so not. (2,1)=1, (2,2)=1. So (1,1) component and (3,1) component are not connected at floor 6.
At floor 5: same as 6 basically.
At floor 3: (1,1), (1,2), (1,3), (2,3), (3,3), (3,2), (3,1). Now (2,3) is included. So we have a path: (1,1) - (1,2) - (1,3) - (2,3) - (3,3) - (3,2) - (3,1). All have F≥3. So at floor 3, they are connected!
So the minimum X such that A and C are connected is 3.
Then the cost via X=3 is |10-3| + |6-3| = 7+3=10. That matches the answer 10.
What about via X=4? |10-4|+|6-4|=6+2=8. But are they connected at floor 4? At floor 4, cells with F≥4: (1,1), (1,2), (3,1), (3,2), (3,3). (1,3) has F=6, so included. (2,3) has F=3, not included. So the component of (1,1) is (1,1),(1,2),(1,3). (3,1) is (3,1),(3,2),(3,3). Not connected. So at X=4, not connected.
So we cannot use X=4 directly. We need to change floors.

So the answer is the minimum over all X of ( |Y-X| + |Z-X| + cost to go from A to C at floor X ), where the cost to go from A to C at floor X is 0 if they are in the same component of G_X, and infinity otherwise? But in the sample, at X=3, they are connected, so cost 0, total 10. At X=4, they are not connected, so we cannot use X=4 directly. But we could use multiple X.

The actual path used in the sample uses multiple floors: it goes down to 6, walks, down to 3, walks, up to 6. So it uses X=6 and X=3.

So the answer is not simply min_X ( |Y-X| + |Z-X| + 0 if connected else inf ). It is the minimum over all sequences of floors.

However, we can model this as: we want to find a path in the graph where the cost is the total vertical movement. This is equivalent to: we can move from (cell, floor) to (cell, floor±1) at cost 1, and to (neighbor, floor) at cost 0 if floor ≤ min(F[cell], F[neighbor]).

This is a shortest path problem in a graph with vertical layers. The graph has a node for each (cell, floor) where 1 ≤ floor ≤ F[cell]. The edges are vertical and horizontal.

The number of nodes is sum F[i][j], which is up to 2.5e11, too large. But we can compress the vertical dimension because the horizontal connectivity only changes at floor values that are in the set of F values.

Specifically, for a fixed cell, the set of floors that have the same set of neighbors is from 1 to min(F[cell], min_{neighbor} F[neighbor]). Actually, for a cell u, the neighbor v is accessible at floor X if X ≤ min(F[u], F[v]). So for X ≤ min(F[u], F[v]), v is accessible. For X > min(F[u], F[v]), v is not accessible.

So the set of accessible neighbors changes at X = F[v] for each neighbor v (if F[v] < F[u]). So the number of intervals is at most degree of u, which is 4.

Therefore, for each cell, the vertical line can be compressed to O(degree) segments. Since the grid is planar, the total number of segments is O(HW). More precisely, for each cell, we have at most 5 segments (including the top). So the total number of nodes in the compressed graph is O(HW).

We can then run Dijkstra on this compressed graph to answer queries. But we have 2e5 queries, and we cannot run Dijkstra for each query.

However, we can run a multi-source Dijkstra from all query starts? Or we can use the fact that the graph is static and we want to answer many queries.

Actually, the graph is static, and the start and end are specific (cell, floor) pairs. We can run Dijkstra from each query start, but that's too slow.

But note: the graph has O(HW) nodes, and we have Q=2e5 queries. We can potentially run Dijkstra from all query starts simultaneously (multi-source) and then for each query compute the distance to the end. But the start floors are different.

We can add a super source connected to all query start nodes with cost 0, and then run Dijkstra once to get distances to all nodes. Then the answer for each query is the distance to the corresponding end node. But we have 2e5 queries, so the super source would have 2e5 edges. That's fine.

But wait, the graph has O(HW) nodes, which is 2.5e5. Dijkstra on a graph with 2.5e5 nodes and O(HW) edges is O(HW log HW) ≈ 2.5e5 * 18 ≈ 4.5e6, which is fast. And we only do it once! Then for each query, we look up the distance.

But is the graph size O(HW)? Let's verify.

For each cell (i,j), we consider the set of floors 1..F[i][j]. The neighbors are up, down, left, right. The condition to move to neighbor (i',j') at floor X is X ≤ min(F[i][j], F[i'][j']). So the maximum floor at which (i',j') is accessible is min(F[i][j], F[i'][j']). Let's call this h_{i,j,i',j'}.

So for cell (i,j), the accessible neighbors at floor X are those with h ≥ X. As X increases, neighbors drop out when X exceeds their h.

The set of floors where the set of accessible neighbors is constant is: from 1 to min_{neighbor} h, then from min+1 to next min, etc. Also, at the top, F[i][j] itself is a boundary: we cannot go above F[i][j], but that's just the max floor.

So the breakpoints are: 0, and the values h for each neighbor, and F[i][j]. But we only care about floors from 1 to F[i][j]. The breakpoints are the distinct values of h among neighbors that are less than F[i][j], and F[i][j].

For each cell, the number of intervals is at most (degree + 1). So the total number of vertical segments in the graph is O(HW * 5) = O(HW).

We can create a node for each cell and each "interval" of floors. But we need to allow movement between intervals within the same cell: moving up or down one floor costs 1, so within the same cell, we have edges between consecutive floors with cost 1. But if we compress the vertical line, we need to represent the cost of moving between intervals.

Specifically, for a cell, we have intervals [1, a1], [a1+1, a2], ..., [ak, F]. The cost to move from the top of one interval to the bottom of the next is (a1 - a1) + 1 = 1, but actually moving from floor x to x+1 costs 1. If we have an interval [L, R], we can move from any floor in [L,R] to any other floor in [L,R] with cost |x-y| using stairs, but we also have walkway edges.

To model this correctly, we can create a node for each (cell, floor) at the boundaries, and connect them with edges of cost equal to the distance. For example, for cell u, we create nodes for the key floors: 1, and each h_{u,v} for neighbors, and F[u]. Then we connect consecutive nodes with edges of weight equal to the difference in floors.

This is a standard trick: for each cell, we have a chain of nodes representing the "significant" floor levels. The edges between them have weight equal to the floor difference (since stairs cost 1 per floor).

Then, for each neighbor v of u, at floor X, we can move from u to v if X ≤ h_{u,v}. This means that from any node in u's chain that represents a range covering X, we can move to v. But we need to be careful: if we have a node for the range [L,R] in u, and h_{u,v} ≥ L, then for any X in [L,R], we can move to v. But we need to move to a specific node in v's chain that represents the same floor X.

So we can add edges from the node representing [L,R] in u to the node representing [L',R'] in v, with cost 0, but we need to ensure that the floor X is in both ranges. This can be done by creating edges between all pairs of intervals that overlap and have X ≤ h.

However, this might create many edges: O(HW * degree^2) = O(HW * 16) = O(HW), which is fine.

Specifically, for each cell u, we sort the key floors: 1, and for each neighbor v, h_{u,v}, and F[u]. Let the sorted distinct key floors be k1=1, k2, ..., km. We create m nodes for u: one for each interval [ki, k_{i+1}-1]? Or we can create nodes for the points themselves.

A common approach: create a node for each cell and each key floor value. Then we have vertical edges between consecutive key floors with weight equal to the difference.

For example, for cell u, we have nodes for floors k1, k2, ..., km where k1=1 and km=F[u]. We add edges (u,k_i) to (u,k_{i+1}) with weight k_{i+1} - k_i (cost to go up by that many floors).

Then, for a neighbor v, we can move from (u, X) to (v, X) if X ≤ h_{u,v}. So for each neighbor v, and for each key floor X in u that is ≤ h_{u,v}, we need to add a horizontal edge from (u,X) to (v,X). But v may not have a node for floor X. We can add the edge to the node in v that represents the interval containing X. Since v has nodes for its key floors, we can find the largest key floor in v that is ≤ X, and add the edge from (u,X) to (v, that_key_floor). This works because if we are at floor X in u, we can walk to v at floor X, and then we are at floor X in v. In v's chain, being at floor X means we are between the node for the previous key floor and the next. But to use the chain, we need to be at a specific node.

We can design the nodes such that each node represents a specific floor value. For cell u, we have a node for each key floor value. The meaning is: being at node (u, k) means we are at floor k. We can move up/down along the chain with cost equal to the floor difference.

Then, for a walkway between u and v at floor X, we can only use it if X ≤ h_{u,v}. So we add a zero-weight edge from (u,X) to (v,X) for each X that is a key floor in u and X ≤ h_{u,v}. But what if X is not a key floor in v? We can add the edge to the node in v that has key floor ≤ X and as large as possible. But then the cost to reach X in v is not zero; we have to go up from that node to X. However, the walkway is at floor X, so we should be able to arrive at v at floor X without additional cost (other than the stairs to change floors later).

So if we add an edge from (u, X) to (v, Y) where Y is the key floor in v that is ≤ X, and the cost is 0, then from there we can take stairs up to X in v with cost X - Y. But we could have also taken stairs at u. So the total cost from (u, X) to (v, X) is at most (X - Y) if we go via Y. But we want the cost to be 0 for the walkway itself, and then we pay for stairs if we need to change floor.

Actually, if we add the edge from (u,X) to (v, floor_key_in_v_just_below_X) with cost 0, then from there we can go up to X in v with cost X - floor_key. But we could also go from (u,X) down to some other floor and then walk. The graph should capture the possibility of walking at any floor X ≤ h.

The standard way is to add edges from (u, X) to (v, X) for all X that are key in u, and also for X that are key in v, but we need to cover all X.

Since we only care about distances, and the cost is linear, we can use the fact that the optimal path will only change floors at key floors. So we can restrict to key floors.

Specifically, for each cell u, we define the set of "relevant" floors as: 1, F[u], and for each neighbor v, min(F[u], F[v]). These are the floors where the set of accessible neighbors changes. Between these, the set of accessible neighbors is constant.

For a cell u, let the sorted distinct relevant floors be r1=1, r2, ..., rk. We create nodes (u, ri) for each ri. We add vertical edges: (u, ri) to (u, r_{i+1}) with weight r_{i+1} - ri. Also, we need to consider that from (u, ri) we can walk to neighbor v at any floor X such that ri ≤ X ≤ r_{i+1} and X ≤ h_{u,v}. But since the set of neighbors is constant in this interval, we can walk to v at any floor in the interval. So we can add a zero-weight edge from (u, ri) to (v, X) for some X? Or we can add an edge from (u, ri) to (v, the highest relevant floor in v that is ≤ min(r_{i+1}-1, h_{u,v})).

This is getting complicated. There is a known construction for this type of problem.

I recall a solution: we build a graph with H*W nodes, and we add edges based on the heights. Then we run a shortest path algorithm. But we need to incorporate the floor changes.

Another idea: The problem can be solved by reducing to a standard shortest path on a graph with H*W nodes, where the edge weight between adjacent cells is the absolute difference of the "min height" or something. But that doesn't capture the floor changes.

Wait, I remember a problem: "Takahashi's Solitaire" or something? No.

Let's think about the answer formula. The answer is the minimum number of stairs. This is equivalent to: we can choose a path and a sequence of floors. The total stairs is the total vertical distance traveled.

We can think of it as: we want to find a path in the grid that minimizes the sum of absolute differences of the "floor at which we traverse each edge", plus the start and end differences.

This is exactly the problem of finding a path in a graph where the cost of an edge depends on the "level" at which we traverse it, and we can change levels at vertices.

We can model this as a minimum cost flow or as a shortest path in a graph where we add a "height" dimension.

Given the constraints, I think the intended solution is to build a graph with O(HW) nodes as described, and then run Dijkstra from all query start nodes simultaneously.

Let's try to construct the graph properly.

For each cell (i,j), we have a vertical line. We want to compress it. The key observation: for a fixed cell, the set of neighbors accessible at floor X is constant for X in [L, R] where L and R are consecutive values in the set {1} ∪ {min(F[i][j], F[i'][j']) for neighbors} ∪ {F[i][j]}.

So for each cell, we partition the range [1, F[i][j]] into O(degree) intervals. For each interval [a,b], the set of accessible neighbors is the same. Let's call this set S.

In the graph, we can represent the cell and interval as a node. The cost to move from the bottom of the interval to the top is (b - a) using stairs. So we can have two nodes per interval: one for the bottom and one for the top, and an edge between them with weight (b-a)? But we also need to connect consecutive intervals.

Actually, we can have a single node per interval, and edges between intervals. But we need to allow movement up and down within the cell. If we have a node for interval [a,b], it represents being at some floor in [a,b]. But we cannot distinguish being at a or at b. However, the cost to reach a particular floor is determined by the distance from the reference point.

A common technique is to use the "difference constraints" or to create a node for each cell and each "height level", and connect them.

Since the number of intervals per cell is small, we can create a node for each (cell, interval). Let's say cell u has intervals I1, I2, ..., Ik. For each interval I = [l, r], we create a node. We add edges from I to I+1 with weight 0? No, moving from the top of I to the bottom of I+1 costs (l_{I+1} - r_I) = l_{I+1} - l_I - (r_I - l_I) = (l_{I+1} - l_I) - (length of I). This is messy.

Alternatively, we can create nodes for the "breakpoints": for each cell, we have nodes for floors 1, and for each min(F[u],F[v]) + 1? Actually, we need to represent the ability to be at any floor.

A simpler approach: for each cell u, we have a node for each distinct value in the set {1, F[u]} ∪ {min(F[u],F[v]) for neighbors}. Let's call these values v1=1, v2, ..., vm. We create m nodes: (u, v1), (u, v2), ..., (u, vm). We add vertical edges between consecutive nodes: weight v_{i+1} - v_i. This represents the cost to go from floor v_i to v_{i+1} using stairs.

Now, for a walkway between u and v at floor X, we can only use it if X ≤ min(F[u],F[v]). So for each X that is a key floor in u and X ≤ h_{u,v}, we can add a zero-weight edge from (u, X) to (v, X). But v may not have a node for X. We can add the edge to the node in v with key floor ≤ X and as large as possible. But then we need to account for the stairs from that node to X. However, we can also add edges for key floors in v.

To cover all possibilities, we can add edges from (u, X) to (v, Y) for every key floor X in u and every key floor Y in v such that Y ≤ X ≤ h_{u,v} and X is in the range of u. But this could be O(degree^2) per edge, which is O(16) per edge, so O(HW) edges total.

Specifically, for each adjacent pair (u,v), let h = min(F[u],F[v]). We consider the set of key floors in u: K_u, and in v: K_v. For each x in K_u with x ≤ h, and each y in K_v with y ≤ h, we add an edge from (u, x) to (v, y) with weight 0 if we can walk at some floor X that is ≥ y and ≤ x? No, we need to be at the same floor to walk.

Actually, if we are at floor x in u, we can walk to v at floor x. So we need an edge from (u, x) to (v, x). But if v does not have a node for x, we can go from (u, x) to (v, y) where y is the largest key floor in v that is ≤ x, and then take stairs up from y to x in v. The cost of that is (x - y). But we can also take stairs down in u to some other floor and walk. So the graph should have an edge from (u, x) to (v, y) with weight 0, and then from (v, y) to (v, x) with weight x-y. But (v, y) to (v, x) is a vertical edge in v, which we already have. So we can simply add a zero-weight edge from (u, x) to (v, y) for all x in K_u and y in K_v such that y ≤ x ≤ h. Then the cost to go from (u, x) to (v, x) will be 0 (walk) + (x-y) (stairs in v) = x-y. But we could also walk from (u, x) to (v, x) directly if we add a direct edge. However, adding edges for all x in K_u and y in K_v with y ≤ x ≤ h is O(|K_u| * |K_v|) per edge, which is O(16) per edge since |K| is at most 5. So total edges O(HW * 16 * 2) = O(HW).

Then the graph has O(HW * 5) = O(HW) nodes and O(HW * 16) = O(HW) edges. We can run Dijkstra on this graph from a super source connected to all query start nodes (A_i, B_i, Y_i). But note that Y_i may not be a key floor in cell (A_i,B_i). We need to add a node for Y_i or connect to the nearest key floor.

For a query start (A,B,Y), we need to find the node in cell (A,B) that corresponds to floor Y. Since we only have key floors, we can connect the start to the node for the largest key floor ≤ Y, and add an edge with weight Y - key. Similarly, for the end (C,D,Z), we can connect from the node for the largest key floor ≤ Z, and add an edge with weight Z - key. But we want the distance from the exact floor Y to Z. So we can add a super source node connected to (A,B, Y) with weight 0, but we need to have a node for Y. We can create a temporary node for the query, or we can compute the distance to the key floor and adjust.

Actually, we can add edges from the super source to the appropriate node in the cell with weight (Y - key), and then from the cell to the super sink with weight (Z - key). But we have to be careful: the distance from (A,B,Y) to (C,D,Z) is the shortest path in the graph from a virtual node at (A,B,Y) to (C,D,Z). We can add a virtual node for each query, but that would be too many.

Instead, we can use the fact that the graph is static. We can run Dijkstra from multiple sources: we add a super source that has an edge to (A_i, B_i, key_i) with weight (Y_i - key_i) for each query, where key_i is the largest key floor in (A_i,B_i) that is ≤ Y_i. Then we run Dijkstra to compute distances to all nodes. Then for each query, the answer is distance to (C_i, D_i, key'_i) + (Z_i - key'_i), where key'_i is the largest key floor in (C_i,D_i) that is ≤ Z_i.

But is this correct? We need to ensure that the path from Y to Z is represented. The path might go through floors that are not key floors. But the optimal path will only change floors at key floors? Not necessarily, but because the cost is linear and the constraints are upper bounds, the optimal path will have the property that we only change floors when necessary, which is at the key floors. More precisely, the set of relevant floors for a cell is finite. So yes, the optimal path can be represented in the compressed graph.

Let's verify with the sample.

Sample grid:
F:
(1,1)=12, (1,2)=10, (1,3)=6
(2,1)=1, (2,2)=1, (2,3)=3
(3,1)=8, (3,2)=6, (3,3)=7

For each cell, the key floors are 1, F[cell], and for each neighbor, min(F[cell], F[neighbor]).

For (1,1): neighbors: (1,2): min(12,10)=10, (2,1): min(12,1)=1. So key floors: 1, 10, 12. Nodes: (1,1,1), (1,1,10), (1,1,12).
Vertical edges: 1-10 weight 9, 10-12 weight 2.

For (1,2): neighbors: (1,1):10, (1,3): min(10,6)=6, (2,2):1. Key: 1,6,10. Nodes: 1,6,10.
Vertical: 1-6 w5, 6-10 w4.

For (1,3): neighbors: (1,2):6, (2,3): min(6,3)=3. Key: 1,3,6. Nodes: 1,3,6.
Vertical: 1-3 w2, 3-6 w3.

For (2,1): neighbors: (1,1):1, (2,2):1, (3,1):1. Key: 1. Node: 1.

For (2,2): neighbors: (1,2):1, (2,1):1, (2,3): min(1,3)=1, (3,2):1. Key: 1.

For (2,3): neighbors: (1,3):3, (2,2):1, (3,3): min(3,7)=3. Key: 1,3. Nodes: 1,3.
Vertical: 1-3 w2.

For (3,1): neighbors: (2,1):1, (3,2): min(8,6)=6. Key: 1,6,8. Nodes: 1,6,8.
Vertical: 1-6 w5, 6-8 w2.

For (3,2): neighbors: (3,1):6, (2,2):1, (3,3): min(6,7)=6. Key: 1,6. Nodes: 1,6.
Vertical: 1-6 w5.

For (3,3): neighbors: (2,3):3, (3,2):6. Key: 1,3,6,7? min(7,3)=3, min(7,6)=6, F=7. So key: 1,3,6,7. Nodes: 1,3,6,7.
Vertical: 1-3 w2, 3-6 w3, 6-7 w1.

Now, horizontal edges: for each adjacent pair (u,v), and for each key x in u and key y in v with y ≤ x ≤ min(F[u],F[v]), add edge from (u,x) to (v,y) weight 0.

But wait, we also need to consider walking from (u,x) to (v,x). If we have an edge from (u,x) to (v,y) with y ≤ x, then we can walk at floor x from u to v, and then we are at floor y in v's chain? No, we are at floor x in v, but v's chain only has nodes for key floors. So from (u,x) we take walkway to v at floor x. In v, we are at floor x, but v has a node for the largest key floor ≤ x, which is y. We can model this as: we arrive at (v,y) and then take stairs up to x. But we don't want to pay for stairs up to x if we are going to continue walking. However, in the graph, from (v,y) we can go up to (v,x) if x is also a key floor in v, or we can go to the next key floor.

The edge from (u,x) to (v,y) with weight 0 means: from (u,x), we can reach (v,y) with 0 cost. But we actually want to reach (v, the key floor that is ≥ x?) No, we are at floor x in v. We can represent this as being at the node for the key floor just below x, with the understanding that we are at x. But the cost to go from y to x is not paid yet. When we later need to go to another floor, we pay the stairs from y to x.

This is correct because the stairs are local to the cell. If we are at floor x in v, and we want to walk to neighbor w at floor x, we need to be at floor x. In the graph, from (v,y) we can take stairs to (v, next_key) etc. But to walk to w at floor x, we need an edge from (v, ?) to (w, ?). If we have an edge from (v,y) to (w,z) for some z, we need z ≤ x. But we are at x, so we can walk to w at x. However, in the graph, we have an edge from (v,y) to (w,z) with z ≤ y? No, our condition was y ≤ x. So from (v,y) we can only walk to w at floors ≤ y? That's wrong.

We need to fix the horizontal edges. The walkway can be used at any floor X ≤ h. So from any floor X in v that is ≤ h, we can walk to u. In our node representation, we have a node for each key floor. For a given key floor y in v, it represents the range of floors from y to the next key floor (or the top). But we don't know exactly which floor we are at.

To handle this, we need to allow walking at any floor X. A common way is to add edges from (u, x) to (v, y) for all x in K_u and y in K_v such that the intervals overlap and X ≤ h. More precisely, for each adjacent pair (u,v), we add edges from (u, x) to (v, y) with weight 0 if there exists a floor X such that X is in the interval represented by x in u and by y in v, and X ≤ h. But we also need to allow walking from y to x in v.

Actually, the standard construction for this problem is to create a graph with H*W nodes, and add edges based on the heights, and then run a shortest path algorithm. I think I have seen a solution where we build a graph with edges weighted by the height difference.

Let's search memory: This problem is from AtCoder Grand Contest 2024? Or ABC? I think it's "Walking Takahashi" or something. The constraints H,W <= 500 and Q up to 2e5 suggest a solution with O(HW) preprocessing and O(log HW) or O(1) per query.

Another idea: We can compute the "minimum stairs" by considering the "height profile" along the shortest path in terms of the graph where edge weights are the minimum height. But that's not it.

Wait, I think the answer is simply: the minimum over all paths of the sum of the absolute differences of the "minimum height" along the path? No.

Let's think about the problem as finding a path that minimizes the total vertical distance. This is equivalent to: we can move horizontally at any level, but we pay for level changes.

This is exactly the problem of finding a path in a graph with node weights (F) where the cost is the total variation of the level we choose at each node.

There is a known reduction: we can create a new graph with H*W nodes, and for each node, we add a self-loop or we use a different metric.

Actually, we can solve this by running a multi-source BFS from the start cell at all floors, but that's per query.

But note that the grid is only 500x500. We can precompute all-pairs shortest paths in this "stair" metric? That would be O((HW)^2) which is too large (6e10).

However, the number of queries is 2e5, which is large, but the grid is small. Maybe we can precompute the "distance" between all pairs of cells for the "walkway" component, but the cost depends on the start and end floors.

Another thought: The problem can be solved by building a graph where the nodes are the cells, and we add edges with weight equal to the absolute difference of the "height" of the cells, but that's for a different problem.

Let's look at the sample again. The answer for query 1 is 10. The path used: down to 6, walk, down to 3, walk, up to 6. The floors used are 6 and 3. These are key floors.

In general, the optimal floors will be chosen from the set of F values of the cells on the path. So if we can find the path, we can compute the cost. But we need to find the path.

Maybe we can model this as: we want to find a path from A to C such that the "profile" of the path (the minimum of F along the path at each point) allows us to connect the floors.

This is like: we can go from Y to Z if there is a path where the "bottleneck" heights are at least something.

I recall a solution for this problem: we can solve it by building a graph with H*W nodes, and adding edges based on the minimum height of the two cells. Then we run a shortest path algorithm where the edge weight is the height difference? Not exactly.

Let's try to think from first principles. We want to minimize the total stairs. This is equivalent to minimizing the total vertical distance traveled. We can think of the "floor" as a state. The set of reachable floors at a cell is [1, F]. Moving horizontally is free if we are at a floor ≤ the min height of the two cells.

This is exactly the problem of finding a path in a graph where the cost is the L1 distance in the vertical dimension. This can be solved by a BFS in 3D, but the vertical dimension is large.

We can compress the vertical dimension because the horizontal connectivity only changes at F values.

So the compressed graph has O(HW) nodes. We can run Dijkstra on it. Since we have Q=2e5 queries, we can run a multi-source Dijkstra from all query starts. But each query start is at a specific floor Y. We can add a super source connected to all (A_i, B_i, Y_i) with cost 0. But Y_i may not be a node. We can connect to the node for the largest key floor ≤ Y_i, with edge weight Y_i - key. Similarly for the sink.

But the graph is directed? The edges are undirected for walkways, but stairs are directed (up and down both cost 1). So the graph is undirected with positive weights, so Dijkstra works.

So the plan is:
1. For each cell, determine the key floors: 1, F[i][j], and for each neighbor, min(F[i][j], F[neighbor]).
2. Create a node for each (cell, key_floor). Let's assign an ID to each node.
3. Add vertical edges: for each cell, sort the key floors. For each consecutive pair (a,b), add an edge between the nodes with weight b - a.
4. Add horizontal edges: for each adjacent pair (u,v), let h = min(F[u],F[v]). For each key floor x in u and each key floor y in v such that y ≤ x ≤ h, add a zero-weight edge from (u,x) to (v,y). Also, we need edges from (v,y) to (u,x) for the symmetric condition. But note: if we add edges for all y ≤ x ≤ h, we cover both directions because we will add for (v,u) as well.
5. For each query, we have start (A,B,Y) and end (C,D,Z). We need to find the shortest path in this graph from floor Y to Z. We can do this by adding the start and end as nodes, or by using the key floors.

But we cannot add nodes per query. We can use the following trick: we can run Dijkstra from a super source that is connected to the "start" node for each query. For query i, we find the node in cell A_i,B_i for the largest key floor ≤ Y_i. We add an edge from super source to that node with weight Y_i - key. But we also need to account for the possibility of starting at a floor higher than the key floor? Actually, if Y_i is not a key floor, we can start at the key floor below, and then take stairs up to Y_i. But we want to start at Y_i. So we add an edge with weight Y_i - key. This represents the stairs we take at the start to reach Y_i from the key floor. But we could also start at a higher key floor and walk down? No, the key floors are the ones we care about. Starting at Y_i is equivalent to being at the key floor below Y_i and then taking stairs up to Y_i. So the cost to reach Y_i from the key floor is Y_i - key. So from the super source, we can reach the key floor node with cost 0, and then take stairs to Y_i. But we want the distance from Y_i. So we should connect the super source to the key floor node with weight 0, and then from that node we can take stairs to Y_i. But Y_i is not a node. However, we can compute the distance from the key floor node to the end, and then add the stairs from Y_i to key and from end key to Z.

Specifically, let d[x] be the shortest distance from the super source to node x. We set d[key_start] = 0 for the key start node. Then the distance from Y_i to any node x is d[x] + (Y_i - key_start) if x is in the same cell? Not exactly, because we might take stairs at other cells.

Actually, the distance from Y_i to Z_i in the original problem is the shortest path in the full graph. In our compressed graph, the shortest path from the key start node to the key end node, plus the stairs at start and end, gives the answer? Not necessarily, because the path might go through floors that are not key floors, and the stairs might be taken at different cells.

But in the compressed graph, the nodes represent specific floors. The path in the compressed graph corresponds to a path in the full graph where we only change floors at key floors. Is it always optimal to only change floors at key floors? Yes, because between key floors, the set of accessible neighbors is constant, so there is no benefit to changing floors in between. You can always delay the floor change to the next key floor without increasing the cost. More formally, the cost is linear, and the constraints are upper bounds that are constant in the interval, so the optimal solution will have floor changes only at the breakpoints.

Therefore, the shortest path in the compressed graph from a start node at floor Y to an end node at floor Z is exactly the answer. But we need to handle Y and Z not being key floors.

We can map Y to the key floor just below Y. Let k_Y be the largest key floor in the start cell that is ≤ Y. Then any path starting at Y can start by taking stairs up to Y (cost Y - k_Y) from k_Y. But we could also start at a higher key floor and walk down? No, we start at Y. So the distance from Y to Z is at least the distance from k_Y to Z plus (Y - k_Y) minus something? Actually, if we start at k_Y, we can take stairs up to Y with cost Y - k_Y. So the distance from Y is the distance from k_Y to Z plus Y - k_Y, but we also need to add the stairs to Z at the end.

Wait, let's be precise. In the compressed graph, we have nodes for key floors. The distance between two nodes (u, x) and (v, y) in the compressed graph is the minimum stairs to go from floor x at cell u to floor y at cell v, with the restriction that we can only change floors at key floors. But in the original problem, we can change floors at any floor. However, as argued, we can restrict to key floors.

Now, for a query start at floor Y (not necessarily a key floor), we can start at the key floor k_Y ≤ Y, and then take stairs up to Y. So the distance from Y to Z is at least the distance from k_Y to Z plus (Y - k_Y) plus the stairs from the end key floor to Z. But we could also start at a higher key floor? No, because we start at Y, which is higher than k_Y. To reach k_Y, we would have to take stairs down, which costs Y - k_Y. So starting at k_Y and going up to Y is the same as starting at Y. So the distance from Y to Z equals the distance from k_Y to Z_end_key plus (Y - k_Y) + (Z - k_Z), where k_Z is the largest key floor in end cell ≤ Z? But wait, if Z is not a key floor, we end at Z, which is above the key floor. So we need to add the stairs from the end key floor to Z.

But is it possible that the optimal path ends at a key floor that is greater than Z? No, because we need to end at Z exactly. So the last node on the path must be at a floor ≥ Z, and then we take stairs down to Z? Or we could end at a floor < Z and take stairs up. The cost is the absolute difference. So if we end at key floor k_Z ≤ Z, we need to add Z - k_Z. If we end at a key floor k' > Z, we would need to add k' - Z, but we could also choose to end at a lower key floor. The optimal end key floor will be the one that minimizes the total.

So for a query, the answer is min over key floors x in start cell and y in end cell of ( |Y - x| + dist(x, y) + |Z - y| ), where dist(x,y) is the shortest path in the compressed graph from (start, x) to (end, y). But wait, the compressed graph has nodes for all cells and all their key floors. So dist(x,y) is the shortest path between those two nodes.

But we cannot run Dijkstra for each query. However, we can run a multi-source Dijkstra from all possible start nodes? That would be all (cell, key floor) nodes, which is too many.

But we can use the super source trick: we add a super source, and for each query i, we add an edge from super source to (A_i, B_i, k) for each key floor k in that cell? No, that would be too many edges.

We can do the following: for each query, we want to compute min_k ( |Y - k| + dist(k, end) ). This is like: we have a graph, and we want to compute the distance from multiple sources with different initial costs. We can add the query start nodes as sources with initial cost |Y - k|. But there are 2e5 queries, and each has up to 5 key floors, so we can add 1e6 sources. That's acceptable? A multi-source Dijkstra with 1e6 sources on a graph of 2.5e5 nodes is O(1e6 log 2.5e5) ≈ 1e6 * 18 = 1.8e7, which is okay. But we also need to query the distance to the end nodes. We can do a multi-source Dijkstra from all query start nodes, and then for each query, we look at the distances to the key floors in the end cell and add |Z - y|.

But wait, the dist(k, end) is the distance from the start key floor to the end key floor in the compressed graph. If we run a multi-source Dijkstra from all start key floors, we get the distance from the nearest start key floor to every node. But we need the distance from a specific start key floor to the end key floor. If we just take the distance to the end node, it will be the distance from the closest start key floor among all queries. That's not what we want.

We need the distance from the specific start key floor of the query to the end key floor. So we need to run Dijkstra from each query start separately, or we need to incorporate the initial cost into the node.

We can do: for each query i, we add a virtual node for the start, and connect it to the key floors in that cell with weight |Y - k|. Then we run Dijkstra from all these virtual nodes. But there are 2e5 virtual nodes, each with up to 5 edges. That's 1e6 edges. Then we run Dijkstra from all these virtual nodes simultaneously. The number of nodes is the original graph nodes plus the virtual nodes, which is about 2.5e5 + 2e5 = 4.5e5. The number of edges is original edges (O(HW)) plus the virtual edges (1e6). So total edges O(1e6). Dijkstra is O(E log V) ≈ 1e6 * log(4.5e5) ≈ 1e6 * 19 = 1.9e7, which is fine in Python if optimized? Maybe borderline but should be okay with heapq.

Then for each query, the answer is the distance to the virtual end node? But we also have the end floors. We can similarly add virtual end nodes? Or we can just look at the distances to the key floors in the end cell.

Let's design it properly:

We have the compressed graph G with nodes (cell, key floor). We have Q queries.

For each query i, we want min_{x in keys(start), y in keys(end)} ( |Y_i - x| + dist_G( (start,x), (end,y) ) + |Z_i - y| ).

We can compute this by running a multi-source Dijkstra from the set of nodes S = { (A_i, B_i, x) for all queries i and all x in keys(A_i,B_i) }, with initial distance |Y_i - x|. Then for each query, we compute min_{y in keys(end)} ( distance[ (C_i, D_i, y) ] + |Z_i - y| ).

But this gives the distance from the start to the end through the graph, but we have multiple sources with different initial costs. If we push all sources into the heap with their initial costs, the distance to a node will be the minimum over all sources of ( initial_cost(source) + path_cost(source, node) ). That's exactly what we want for the start part. But we need to combine with the end part. So for each query, we need to know the distance from its specific start to the end. If we just take the distance to the end node, it will be the distance from the closest start among all queries, not necessarily the one belonging to this query.

So we cannot just take the global distance. We need to compute the distance for each query separately. However, we can note that the graph is the same for all queries, and the start nodes are specific. We can run Dijkstra from each query start, but that's too slow.

But wait: the number of distinct start cells is at most 2.5e5. The number of queries is 2e5. Many queries may have the same start cell. We can group by start cell. For each cell that is a start cell, we need to run Dijkstra from the key floors in that cell. But there are up to 2.5e5 cells, and running Dijkstra for each is too much.

However, we can reverse the graph: run Dijkstra from all end nodes? Still the same issue.

We need a way to answer many queries on a static graph with different sources. This is exactly the problem of computing shortest paths from multiple sources in a graph where the sources have weights.

One way: we can add a super source, and for each query i, add a node s_i connected to (A_i, B_i, x) with weight |Y_i - x|. Then we run Dijkstra from the super source. Then the distance from super source to (C_i, D_i, y) is the minimum over x of ( |Y_i - x| + dist( (A_i,B_i,x), (C_i,D_i,y) ) ). But we need to combine with the end cost |Z_i - y|. So we can add another super sink, and for each query i, add a node t_i connected from (C_i, D_i, y) with weight |Z_i - y|. Then the answer for query i is the shortest path from s_i to t_i. This is exactly a standard trick: we add a super source and super sink, and for each query, we add a node s_i and t_i, and connect them appropriately. Then we run Dijkstra from super source, and then we get distances to all nodes. But we need the distance from s_i to t_i, which is the distance from super source to t_i minus the distance from super source to s_i? Not exactly, because there might be paths that go from s_i to other nodes and back. But since the graph has no negative cycles, the shortest path from s_i to t_i is the distance from super source to t_i if we set the distance of s_i to 0? Actually, if we add a super source that connects to all s_i with weight 0, and run Dijkstra, we get the distance from the super source to all nodes. But the distance from s_i to t_i is not simply dist[t_i] - dist[s_i] because the graph is not a tree. However, if we set dist[s_i] = 0 for all s_i, then the distance to t_i is the minimum over i of dist_{s_i}(t_i). That gives the minimum over all queries of the distance from that query's start to t_i. But we need the distance for each specific query.

We can do the following: for each query, we want the distance from s_i to t_i. We can compute this by running Dijkstra from all s_i simultaneously, and then for each query, we look at the distance to t_i. But the distance to t_i from the multi-source Dijkstra is the minimum over all s_j of dist(s_j, t_i). This is not necessarily the distance from s_i to t_i. However, if we run Dijkstra from each s_i separately, we get the exact answer. But that's too slow.

But note: the graph has O(HW) nodes. The number of queries is 2e5. If we run Dijkstra from each query start, it's 2e5 * O(HW log HW) which is too slow.

We need a way to batch the queries. Since the graph is static, we can use the fact that the cost is additive. Maybe we can compute all-pairs shortest paths? No.

Another idea: The graph is actually a tree? Or a planar graph? The grid is planar, but with vertical edges, it might be a graph with treewidth? Not sure.

Wait, the graph we built has a special structure: it is a graph of cells with vertical chains and horizontal edges. This is similar to a graph of a grid with heights. There might be a more efficient algorithm.

I recall a solution for this problem: we can precompute the "height" of each cell as the minimum F along the path to some reference? No.

Let's look at the constraints again: H,W <= 500, so HW <= 2.5e5. Q <= 2e5. The graph has O(HW) nodes and O(HW) edges. Running a single Dijkstra on this graph takes O(HW log HW) which is about 2.5e5 * 18 = 4.5e6 operations. That's very fast. So we can afford to run a Dijkstra for each query? No, 2e5 * 4.5e6 is 9e11, too slow.

But maybe we can run a Dijkstra from each cell? There are 2.5e5 cells, each with a few key floors. If we run Dijkstra from each key floor, that's 1e6 Dijkstras, still too much.

We need a way to answer many queries on a static graph with different sources. This is exactly the "many-to-many shortest paths" problem. For a general graph, we would need to run Dijkstra from each source, or use a more advanced algorithm. But our graph is a special grid graph.

Wait, the graph we built has a very specific structure: it is a graph with H*W nodes (cells) and additional vertical nodes. Actually, the compressed graph has O(HW) nodes and O(HW) edges. It is a planar graph. Many-to-many shortest paths on a planar graph can be computed faster, but maybe not necessary.

Another approach: Since the grid is only 500x500, we can precompute the shortest path between all pairs of cells in the "stair" metric? That would be (2.5e5)^2 = 6e10, too large.

But maybe we can precompute for each cell the "distance" to all other cells using a multi-source BFS from that cell? Still too large.

Let's think differently. The problem asks for the minimum stairs. This is equivalent to: we can move horizontally for free if we are at a floor ≤ the minimum of the two cells. The stairs cost is the total vertical distance.

This is exactly the problem of finding a path in a graph where the cost is the L1 norm in the vertical dimension. This can be solved by a BFS on the state (cell, floor) if we compress the floors. But we need to answer many queries.

Observation: The answer depends only on the "profile" of the grid. For a fixed grid, we can precompute the "minimum stairs to go from any cell to any other cell starting at floor 1" or something. But the start floor varies.

Maybe we can transform the problem: The minimum stairs from Y to Z is equal to the minimum over all paths of the sum of the "drops" and "rises" along the path. This is similar to the "minimum energy" path.

Another idea: We can use the fact that the cost is the total variation, which is at least the absolute difference of the start and end floors if we stay at the same floor. But we can change floors.

I think the intended solution is to build the graph as described and run a multi-source Dijkstra from all query starts, but with a trick: we can add the query start nodes as nodes in the graph, and then run Dijkstra from a super source. But we need the distance from each specific start to its specific end. We can do this by running Dijkstra from each query start, but caching the results: if multiple queries have the same start cell and same start floor (or same key floor), we can reuse the Dijkstra. But even then, there could be 2e5 unique starts.

Wait, the number of distinct start cells is at most 2.5e5, but with different floors. However, the number of distinct start (cell, floor) pairs is at most the number of distinct F values, which is 2.5e5. So we could run Dijkstra from each distinct start (cell, floor) where floor is a key floor. That's at most 2.5e5 Dijkstras, each on a graph of 2.5e5 nodes. That's 6e10 operations, too slow.

But maybe the graph is much smaller? The compressed graph has O(HW) nodes, but running Dijkstra 2.5e5 times is too much.

We need a better way.

Let's reconsider the compressed graph. It has O(HW) nodes and O(HW) edges. We want to answer Q queries of the form: distance from (s, y) to (t, z) in this graph. This is a many-to-many shortest path problem on a graph with O(HW) nodes. For a general graph, we can solve this by running Dijkstra from each query start, but that's O(Q * (V log V + E)). With V=2.5e5, E=O(2.5e5), Q=2e5, that's 2e5 * 2.5e5 = 5e10, too slow.

But maybe the graph has a special structure that allows for faster queries. For example, if the graph is a tree, we can do O(1) queries after preprocessing. But our graph is not a tree.

Wait, is the compressed graph a tree? The vertical edges form chains, and horizontal edges connect them. The graph is actually a graph of a grid with extra nodes. It might have many cycles.

Another idea: The cost is the total vertical distance. This is equivalent to: we can move from (i,j) to (i',j') with cost 0 if we choose a floor X ≤ min(F[i][j], F[i'][j']). The total cost is the sum of |X_i - X_{i+1}|.

This is exactly the problem of finding a path in a graph where the edge weight is the "height" of the edge? No.

I recall a known solution for this problem: we can solve it by building a graph with H*W nodes, and for each node, we add edges based on the "height" of the building. The trick is to consider the "skyline" and use a union-find to find connected components at each height, and then answer queries by binary searching on the height.

But the queries ask for the minimum stairs, not the connectivity.

Let's think about the answer. The answer is the minimum over all paths of the total vertical distance. This is like: we want to find a path that minimizes the sum of the "ups" and "downs". If we fix the path, the optimal floor sequence is to go down to the minimum possible, walk, and go up. But we can go down multiple times.

In fact, the optimal path is: we choose a sequence of floors x0, x1, ..., xk. We can go from Y to x0, then walk at x0, then change to x1, etc., and finally to Z. The cost is |Y-x0| + |Z-xk| + sum |xi - x_{i+1}|. But since we can combine the changes, the cost is the total variation of the sequence of floors along the path. This is exactly the total variation of the floor function along the path.

We can think of it as: we assign a floor to each edge in the path, with the constraint that the floor is ≤ the min height of the two cells. The cost is the sum of absolute differences between consecutive edges, plus the start and end.

If we consider the path as a sequence of edges e1, e2, ..., ek, we assign x_i to ei. The constraints: x_i ≤ h(e_i). The cost is |Y - x1| + sum |x_i - x_{i+1}| + |xk - Z|.

We want to minimize this over all paths and assignments.

This is a min-cost path problem in a graph where the edges have upper bounds on the assigned value.

This can be solved by creating a new graph: for each cell, we have a node, but we also have edges that represent the "height".

Another way: we can reduce this to a standard shortest path by transforming the floors. Consider the following: the cost is the total vertical distance. We can think of the "up" and "down" moves as separate. But the cost is the absolute difference.

This is similar to: we have a graph, and we want to find a path that minimizes the "total ascent and descent". This is like the "minimum effort" path, where the effort is the absolute difference in heights. But here the "height" is the floor we choose, not the building height.

Wait, we can choose the floor. So we are not constrained to the building height except as an upper bound.

This is exactly the problem of finding a path in a graph with node capacities, minimizing the total variation of a label.

There is a known algorithm for this: we can use a BFS on the "difference" graph.

I think I need to look for a different approach.

Let's consider the problem from the perspective of the "skyline". For a fixed floor X, the graph G_X has connected components. If we are at (A,B,Y), we can reach any cell in the component of (A,B) in G_Y. From there, we can change floor to X (cost |Y-X|), and then reach any cell in the component of that cell in G_X. So the reachable set with stairs ≤ S is: start with component of (A,B) in G_Y, then for each cell in that component, we can "jump" to any floor X with cost |Y-X|, and then walk in G_X, etc.

This is like: we have a set of components at each floor. The cost to move from floor X to Y is |X-Y|. So we can think of each component as a node, and the cost to switch components is the floor difference.

But the components change with floor. When we change floor from X to Y, the components may split or merge. This is similar to the "dynamic connectivity" problem.

We can process the floors in decreasing order. As we decrease the floor, we add edges (cells with height exactly the new floor). We can maintain the connected components. For each component, we know the current floor.

We can build a tree of components: as we lower the floor, components merge. This forms a union-find tree (or a Kruskal tree). The cost to go from one component to another through the tree is the difference in the floor at which they merge.

This is a known technique: we can build a merge tree by sorting cells by height and doing union-find. When two components merge at height h, we create a new node with weight h, and connect the two component nodes to it. The resulting tree is a binary tree with leaves being the original cells, and internal nodes having the merge height. The distance between two leaves in this tree (sum of edge weights along the path) is exactly the minimum stairs? Not exactly.

Let's test this idea. For each cell, we have a leaf node. We sort cells by F decreasing. We maintain a union-find of cells. Initially, each cell is its own component. We also create a node for each cell with weight F[i][j]? Actually, when we process a cell, we union it with neighbors that have the same height? No.

Standard construction: we want to build a graph where the cost to go from cell u to cell v is the minimum over all paths of the maximum of the minimum height? No.

There is a known data structure for this: the "minimum spanning tree" on the grid where edge weights are the minimum of the two cells. The maximum edge weight on the path between two cells in the MST is the minimum possible maximum min-height. But we need the total vertical distance.

Wait, if we can walk at floor X if the path has min height ≥ X, then the maximum X at which we can walk between two cells is the minimum over all paths of the minimum edge weight (min height). This is the "bottleneck" path. The maximum X is the minimum over paths of the minimum min(F[u],F[v]) along the path. Let's call this B(A,C). Then we can walk at any floor X ≤ B(A,C) for free? Not exactly, because we might need to change floors.

If we want to go from Y to Z, and we can walk at floor X for free between the components that contain A and C at floor X, then the cost is |Y-X| + |Z-X| if A and C are in the same component at floor X. But if they are not, we might need to change floors multiple times.

However, if we consider the "merge tree" as we decrease the floor, each component at floor X has a "representative". The tree is built as follows: sort all cells by F descending. Use union-find. When two cells become connected for the first time at floor h, we create a new node with weight h, and make it the parent of the two components. This creates a tree (actually a forest, but we can add a root). The leaves are the cells, and internal nodes have weight equal to the floor at which the merge happened.

Now, consider two cells u and v. Their lowest common ancestor (LCA) in this tree has weight h, which is the maximum floor at which u and v are connected? Actually, in this tree, u and v are connected in G_X if and only if X ≤ weight(LCA(u,v)). So the maximum X at which they are connected is weight(LCA).

But we want to go from Y to Z. We can walk at floor X if we are in the same component at floor X. So if we go down to floor h = weight(LCA), we can walk between u and v. The cost would be |Y - h| + |Z - h|. But we might do better by not going all the way down to the LCA, but by changing floors multiple times.

However, the tree structure gives us a way to compute the minimum cost if we only change floors at the merge points. Is it always optimal to only change floors at the merge points? In the merge tree, the components are the connected components of G_X. As we decrease X, components merge. So any walk at floor X is confined to a component. To change floors, we can do it at any cell. The optimal strategy might involve changing floors at a cell that is in a certain component, and then walking in the new component.

But the merge tree exactly captures the connectivity at all floors. The path in the merge tree from u to v goes through a series of merges. The weight decreases as we go up. We can think of starting at u, going up the tree to the LCA, then down to v. At each step, we are changing components. The cost to go from u to v in terms of stairs is the total vertical distance we travel.

If we only change floors at the merge points, the cost is: from Y, we go down to the floor of the first merge, then up? Actually, the merge tree has weights decreasing as we go up. Let's define the tree with root at infinity? We can add a root with weight 0. The leaves have weight F[i][j]. When we union two components at height h, we create a node with weight h. So the tree has leaves with weight F, and internal nodes with weight h where h is the floor at which the two components became connected.

The path from u to v in the tree goes up from u to LCA, then down to v. The weights along the path: from u to LCA, the weights are non-decreasing? Actually, as we go up from u, the merge floor increases or stays the same? When we union at height h, that means at floor h, the components merge. For higher floors, they were separate. So as we go up in the tree, the weight increases. The leaves have weight F[u]. When u merges with a neighbor at floor min(F[u],F[neighbor]), that weight is ≤ F[u]. So the weight of the parent is ≤ the weight of the child. So the tree is decreasing as we go up? Let's be careful.

We process cells in decreasing order of F. We start with no cells. When we add a cell with height h, we activate it and union with active neighbors. The union happens at floor h. So the new node has weight h. The children have weight ≥ h? Actually, the neighbors we union with have height ≥ h because we are processing in decreasing order. So the children have weight ≥ h. So the weight of the parent is ≤ the weight of the children. So the tree is such that the weight decreases as we go up to the root. We can add a root with weight 0.

So the path from u to v goes up from u to LCA (weights decreasing) and then down to v (weights increasing). The floor at which u and v are connected is exactly the weight of LCA. But to walk from u to v, we need to be in the same component, which happens at floor ≤ weight(LCA). So we can walk at any floor X ≤ weight(LCA) between u and v.

Now, the cost to go from Y to Z: we can think of starting at u at floor Y. We can go down to weight(LCA) with cost Y - weight(LCA) (if Y > weight(LCA)). Then walk to v at weight(LCA). Then go up/down to Z with cost |Z - weight(LCA)|. Total cost: |Y - weight(LCA)| + |Z - weight(LCA)|. But this assumes we go directly to the LCA floor. However, we might do better by not going all the way to the LCA, but by changing floors in between.

For example, in the sample, the LCA of (1,1) and (3,1) in the merge tree? Let's build the merge tree for the sample.

Cells sorted by F:
(1,1):12
(1,2):10
(3,1):8
(3,3):7
(1,3):6
(3,2):6
(2,3):3

Process in decreasing order:
Start: no cells.
Add (1,1) with F=12. Active: {(1,1)}. No neighbors active.
Add (1,2) with F=10. Active: {(1,1),(1,2)}. Union (1,1) and (1,2) at min(12,10)=10. Create node with weight 10. Parent of (1,1) and (1,2).
Add (3,1) with F=8. Active: (3,1). No active neighbors ( (2,1) not active, (3,2) not active).
Add (3,3) with F=7. Active: (3,3). No active neighbors.
Add (1,3) with F=6. Active: (1,3). Neighbors: (1,2) active, (2,3) not. Union (1,3) and (1,2) at min(10,6)=6. But (1,2) is already in a component with (1,1). The component of (1,2) has cells (1,1),(1,2). Union (1,3) with that component at floor 6. So we create a node with weight 6, parent of (1,3) and the component (1,1,1,2).
Add (3,2) with F=6. Active: (3,2). Neighbors: (3,1) active, (3,3) active, (2,2) not. Union (3,2) with (3,1) at min(8,6)=6. Union (3,2) with (3,3) at min(7,6)=6. So all three merge at floor 6. Create node with weight 6.
Add (2,3) with F=3. Active: (2,3). Neighbors: (1,3) active, (2,2) not, (3,3) active. Union with component of (1,3) at min(6,3)=3. Union with component of (3,3) at min(7,3)=3. So these two big components merge at floor 3. Create node with weight 3.
Finally, add root with weight 0.

The tree leaves: (1,1), (1,2), (1,3), (3,1), (3,2), (3,3), (2,3). Internal nodes: N10 (weight 10) with children (1,1),(1,2). N6a (weight 6) with children (1,3) and N10. N6b (weight 6) with children (3,1),(3,2),(3,3). N3 (weight 3) with children N6a and N6b and (2,3). Root (0).

Now, query from (1,1) to (3,1). Path in tree: (1,1) -> N10 -> N6a -> N3 -> N6b -> (3,1). The LCA is N3 with weight 3. So weight(LCA)=3. The cost via LCA: |10-3| + |6-3| = 7+3=10. That matches the answer.

What if we go via N6a? From (1,1) to (3,1), can we go via floor 6? At floor 6, (1,1) and (3,1) are not connected (as we saw earlier). So we cannot walk at floor 6 directly. But we can change floors at (1,3) or something. The tree path has weights 12,10,6,3,6,8. The sequence of floors along the path: start at 10. We can go to 6 (cost 4), then to 3 (cost 3), then to 6 (cost 3), then to 8? Wait, (3,1) has F=8, but we end at 6. So we don't need to go to 8.

The cost is the sum of absolute differences along the path in the tree? Not exactly, because we can choose any floor along the path, not just the node weights.

But the tree structure gives a way to compute the answer. In fact, the answer is the distance in the tree between (A,B) and (C,D) where the edge weights are the absolute differences of the node weights? But the tree nodes have weights. The path in the tree has a sequence of node weights. We can start at Y, and we need to reach Z. The minimum cost is the minimum over all paths in the tree of the total variation, but we can also change floors at any point.

Actually, if we only change floors at the nodes in the tree, the cost is: start at Y. At each node, we can change floor to any value ≤ the weight of the node (since the node represents a component at that floor). The weight of the node is the maximum floor at which the component exists. So at a node with weight w, we can be at any floor X ≤ w. When we move to a child node with weight w' < w, we must be at a floor ≤ w'. So the floor must be ≤ w'. Then at the child, we can change to any floor ≤ w'.

So the sequence of maximum allowed floors along the path is the node weights. We want to choose a sequence of floors x0, x1, ..., xk such that x0 ≤ w_start, x0 ≥ Y? Actually, we start at Y, so we need to be at Y at the start. At the start cell, the maximum floor is F[A] = w_start? In the tree, the leaf has weight F[A]. So at the leaf, we can be at any floor ≤ F[A]. So we start at Y, and we can change to x0 ≤ w_start with cost |Y - x0|. Then we move to parent, which has weight w1 ≤ w0. To move, we must be at a floor ≤ w1. So x0 ≤ w1. Then we can change to x1 ≤ w1 with cost |x0 - x1|, etc. At the end, we reach the other leaf, and need to get to Z.

This is exactly the problem of finding a path in the tree with node weights (the maximum allowed floor at that component). We want to minimize the total variation, with the constraint that at each node, the floor is ≤ its weight.

The tree is a binary tree (or a general tree) with weights decreasing from leaves to root. The leaves have weights F[i][j]. The internal nodes have weights equal to the merge floor.

The query is: from leaf u with start floor Y, to leaf v with end floor Z. Find minimum cost to traverse the tree from u to v, changing floors at nodes, with the constraint that at each node, the floor is ≤ the node's weight.

This is a known problem! We can solve it by preprocessing the tree.

Since the tree has O(HW) nodes, we can answer each query in O(log(HW)) time using LCA and some precomputation.

Let's analyze the cost. The path in the tree from u to v goes up to LCA and down. The weights along the path: starting from u, the weights are: F[u] = w0, then w1, ..., wk = weight(LCA), then wk+1, ..., wm = F[v]. Note that w0 ≥ w1 ≥ ... ≥ wk ≤ wk+1 ≤ ... ≤ wm? Actually, as we go up from u, the weights decrease: w0 ≥ w1 ≥ ... ≥ wk. Then from LCA down to v, the weights increase: wk ≤ wk+1 ≤ ... ≤ wm. So the sequence of weights is V-shaped: decreasing then increasing.

The minimum cost to go from Y to Z along this path is: we can choose a sequence of floors x_i at each node such that x_i ≤ w_i, and |Y - x0| + sum |x_i - x_{i+1}| + |xm - Z| is minimized. The x_i can be any values ≤ w_i.

This is a simple 1D problem! Because the constraints are only upper bounds, and the weights are monotonic on each side of the LCA.

Specifically, on the path from u to LCA, the weights are non-increasing. On the path from LCA to v, the weights are non-decreasing.

We can solve the problem by considering the "profile" of the path. The optimal strategy is to go down to the LCA, and then up. But we might not need to go all the way to the LCA. We can stop at some point and come back up.

Actually, since the weights are decreasing then increasing, the optimal floor sequence is to go down to some minimum floor X, and then up. The minimum floor X we can achieve along the path is the weight of the LCA, but we can also stop earlier. However, if we go down to X, we must have X ≤ all weights along the path from the point we start descending. The deepest we can go is the weight of the LCA.

So the optimal cost is: we choose a floor X to be the "turning point". We go from Y down to X (or up if Y < X) with cost |Y-X|, then from X to Z with cost |Z-X|, but we must ensure that X is achievable along the path. The achievable X is any value ≤ the minimum weight on the path? Not exactly, because we can change floors at any node. The path consists of segments. We can change floors at each node. So we can go from Y to some floor at the first node, then to the next node, etc. The total cost is the sum of absolute differences. This is exactly the total variation of a sequence bounded above by the node weights.

The minimum total variation to go from Y to Z with upper bounds w0, w1, ..., wm (where w0 = F[u], wm = F[v], and w_i are the weights along the path) is: we want to find x_i ≤ w_i minimizing |Y - x0| + sum |x_i - x_{i+1}| + |xm - Z|.

This is a classic problem. The solution is: the optimal x_i will be either as high as possible or as low as possible. In fact, we can think of the path as having a "bottleneck" which is the minimum of the w_i along the path. Let h = min_i w_i. This is exactly the weight of the LCA? Not necessarily, because the path from u to LCA has decreasing weights, so the minimum on that side is w_LCA. The path from LCA to v has increasing weights, so the minimum on that side is also w_LCA. So the minimum weight on the entire path is w_LCA. So h = w_LCA.

But we can achieve any floor X ≤ h? Actually, we can only be at floor X at a node if X ≤ w_i. So at the LCA, we can be at any X ≤ h. At the leaves, we can be at any X ≤ F. So if we want to be at floor X, we need X ≤ w_i for all i on the path. This is true if and only if X ≤ h, where h = min_i w_i = w_LCA. So we can only be at floor X ≤ h at all nodes simultaneously. But we don't need to be at the same floor at all nodes. We can be at different floors at different nodes, as long as the differences sum up.

The cost is the total variation. We can think of it as: we can move freely in the "tree" but with upper bounds. The optimal solution is to go down to some floor X ≤ h, and then go up. But we might also go up then down? Since the weights are V-shaped, the optimal is to go monotonically to the minimum and then monotonically up. So the floor sequence is non-increasing from u to LCA, and non-decreasing from LCA to v. Therefore, the total cost is |Y - X| + |Z - X| for some X ≤ h. But we also need to ensure that at each node, the floor is ≤ w_i. If we choose X ≤ h, then at the LCA we are at X (ok). At the nodes on the way down, we are at floors between Y and X. Since w_i ≥ h ≥ X, and w_i ≥ Y? Not necessarily, if Y > w_i, we cannot be at Y. But we start at Y, and Y ≤ F[u] = w0. As we go up, the weights decrease. If at some node w_i < Y, we cannot have floor Y at that node. So we must start decreasing before we hit a node with weight < Y.

So the constraint is that at each node, the floor we are at must be ≤ w_i. So the floor sequence must satisfy x_i ≤ w_i. Since w_i is non-increasing from u to LCA, if we start at Y, we can have x0 = Y, but if Y > w1, we need to decrease. The maximum floor we can maintain on the path from u to LCA is limited by the minimum of the weights on that subpath. Let's define for each node, the maximum floor we can be at when leaving that node towards the parent. This is the minimum of the weights from that node to the LCA.

Similarly, from LCA to v, the floor can increase, but it cannot exceed the weights on the path.

So the problem reduces to: on the path from u to LCA, we have a non-increasing sequence of upper bounds w0 ≥ w1 ≥ ... ≥ wk. We start at Y, and we want to reach some floor X at the LCA, with the constraint that the floor at node i is ≤ w_i. The cost is the total variation. Since the upper bounds are non-increasing, the optimal strategy is to decrease as late as possible: we stay at Y as long as Y ≤ w_i, and when we hit a node where w_i < Y, we must decrease. So the floor sequence is: Y, Y, ..., Y, then decrease to some value, etc. Actually, the minimum cost to go from Y to X with upper bounds w0 ≥ w1 ≥ ... ≥ wk is: we can stay at Y as long as Y ≤ w_i. If Y > wk, we must decrease to at most wk. The optimal is to decrease exactly to max(X, something). Actually, it's known that the minimum cost to go from a to b with upper bounds w0 ≥ w1 ≥ ... ≥ wk is: we can think of it as: the cost is |Y - X| if we can maintain Y and X, but if Y > wk, we have to pay extra.

In fact, the cost is: let h = wk (the minimum upper bound on the path). Then the cost from Y to X is at least |Y - X|, but also we cannot have Y > h. So if Y > h, we must decrease to at most h. The minimum cost to go from Y to X with the constraint that at each step the value is ≤ w_i is: if Y ≤ h, then we can stay at Y until we need to change to X. The cost is |Y - X|. If Y > h, we must decrease to h at some point. The cost is Y - h + |h - X| = Y - h + |X - h|. But we could also decrease to something else.

Actually, the optimal cost from Y to X on a path with decreasing upper bounds w0 ≥ w1 ≥ ... ≥ wk is:
- If X ≤ h: the cost is (Y - h) + (h - X) = Y - X, but we have to decrease to h, so cost is Y - h + (h - X) = Y - X if we go directly? No, if Y > h and X ≤ h, the minimum cost is Y - h + |X - h| = Y - h + h - X = Y - X. But we have to pay Y - h to go down, and h - X to go up? Actually, we go from Y down to h (cost Y-h), then from h down to X? No, X ≤ h, so we go from h to X (cost h - X). Total Y - X. But is that possible? We start at Y, go down to h, then down to X. The cost is (Y - h) + (h - X) = Y - X. And we never exceed w_i because we are decreasing. So yes, if X ≤ h, the cost is Y - X (assuming Y > h). If Y ≤ h, then we can go from Y to X directly with cost |Y-X|, as long as we don't exceed w_i. But if Y > some w_i, we need to decrease. The condition to be able to stay at Y is Y ≤ min w_i = h. So if Y ≤ h, cost is |Y-X|. If Y > h, cost is Y - X (since X ≤ h, Y - X > 0).

Similarly, if X > h, we need to go down to h and then up to X? But X is the floor at the LCA. On the path from u to LCA, we are decreasing. So X is the floor at the end of this segment. It must be ≤ h. So X ≤ h always. So on the u to LCA segment, we are going from Y to some X ≤ h. The cost is: if Y ≤ h, cost = |Y-X|. If Y > h, cost = Y - X.

On the LCA to v segment, we have increasing upper bounds wk ≤ wk+1 ≤ ... ≤ wm. We start at X at the LCA, and want to reach Z at the leaf. The upper bounds are increasing. The constraint is that at each node, the floor must be ≤ w_i. Since the bounds are increasing, if we start at X, we can increase as we go down, but we cannot exceed the bound. The minimum cost to go from X to Z with increasing upper bounds is: if Z ≤ X, we can go down directly, cost = X - Z. If Z > X, we can go up to Z, but we must ensure that Z ≤ w_i for all i. The maximum Z we can achieve is the minimum of the upper bounds on this segment? Actually, the bounds are increasing, so the smallest bound is at the LCA: wk = h. So we can only go up to Z if Z ≤ w_i for all i. The minimum upper bound on this segment is h. So if Z > h, we cannot achieve Z? But wait, at the leaf, the bound is F[v] = wm ≥ h. So we can be at any floor up to wm. But on the path from LCA to v, the bounds are increasing: h = wk ≤ wk+1 ≤ ... ≤ wm. So if we start at X ≤ h, we can increase. The maximum floor we can achieve at the leaf is wm. But we can also have intermediate floors. The constraint is that at each node, the floor must be ≤ w_i. So if we want to reach Z, we need Z ≤ wm. That's true since Z ≤ F[v] = wm. But can we go from X to Z while respecting the bounds? Yes, as long as we don't exceed the bound at any node. Since the bounds are increasing, the most restrictive bound is at the LCA: h. So if we start at X ≤ h, and we want to go to Z, we can simply increase from X to Z, and at each node, the floor will be ≤ the current bound because the bound is ≥ h ≥ X, and we are increasing to Z, but if Z > bound at some node, we would exceed it. The bound at node i is w_i. We need that for the sequence, at each node, the floor is ≤ w_i. If we increase monotonically from X to Z, the maximum floor before reaching the leaf is at the leaf, which is Z ≤ wm. At the previous node, the floor is ≤ Z ≤ wm, but we need it to be ≤ w_{m-1}. Since w_{m-1} ≤ wm, we need Z ≤ w_{m-1}? Not necessarily: we can be at a floor that is less than the bound. We are not forced to use the full bound. We can choose any floor ≤ bound. So we can always stay below the bound. The only constraint is that we cannot exceed the bound at any node. So if we go from X to Z monotonically, we will be at some floor at each node. To ensure we don't exceed the bound, we need that for each node i, the floor we pass through is ≤ w_i. If we increase linearly, the floor at node i is some value between X and Z. The maximum of this sequence is Z (at the leaf). The bound at the leaf is wm, and we need Z ≤ wm, which is true. For other nodes, the bound is smaller. So if we go from X to Z, and Z is large, we might exceed the bound at an intermediate node. For example, if w_{m-1} is small, we cannot have a floor > w_{m-1} at that node. So we must be ≤ w_{m-1} at that node. Therefore, the maximum floor we can have at node i is w_i. So the sequence must satisfy x_i ≤ w_i.

So the cost from X to Z with increasing bounds is: we can go from X to some maximum floor M, and then down to Z? Actually, we want to minimize |X - Z| with the constraint that at each node, the floor is ≤ w_i. The minimum cost is simply |X - Z| if we can find a path that doesn't exceed the bounds. But since the bounds are increasing, the most restrictive is the smallest bound, which is at the LCA: h. So if we can find a path from X to Z that stays ≤ h until the bounds become large enough. Actually, we can always go from X to Z directly if we can find a sequence. The condition for the existence of a sequence from X to Z with x_i ≤ w_i and total variation |X-Z| (i.e., monotonic) is that we can go from X to Z without exceeding the bounds. This is possible if and only if for all i, the value at i is ≤ w_i. If we go monotonically from X to Z, the value at i is some interpolation. The worst case is at the node with the smallest w_i. The smallest w_i is h (at LCA). So if we start at X ≤ h, and we want to go to Z, we can go from X to min(Z, h) or something. Actually, if Z > h, we cannot jump from X ≤ h to Z > h in one step because at the next node, the bound is still h, so we must be ≤ h. So we can only increase when the bounds allow. So we can go from X to h at the LCA, and then from h to Z along the increasing bounds. The cost would be: from X to h: |X-h|, then from h to Z: |Z-h|, but we have to be careful about the path.

In general, the optimal cost on a path with bounds w0, w1, ..., wm to go from Y to Z is: we can compute it as: the cost is max( Y, max_{i} something )? There is a known formula.

Actually, the problem reduces to: on the path, the set of achievable floors at each node is (-inf, w_i]. We want to find a sequence x_i with x_0 = Y, x_m = Z, x_i ≤ w_i, minimizing sum |x_i - x_{i+1}|.

This is a shortest path problem on a line with upper bounds. The optimal solution is: we can think of the "hull" of the bounds. The cost is: let M = max_{i} min(w_i, something). Actually, the minimum total variation to go from Y to Z with upper bounds w_i is: we can go up to min(w_i) on the way, etc.

I recall that the answer is simply: the cost is the maximum of (Y, Z, and the minimum bound on the path)? No.

Let's test with the sample path from (1,1) to (3,1) through the tree. The path nodes and their weights:
(1,1): w=12
N10: w=10
N6a: w=6
N3: w=3
N6b: w=6
(3,1): w=8

Start Y=10, end Z=6.
Path: w0=12, w1=10, w2=6, w3=3, w4=6, w5=8.
Y=10, Z=6.
We need to go from 10 to 6.
At node 0: w0=12, can have 10.
Node 1: w1=10, can have 10.
Node 2: w2=6, cannot have 10, must be ≤6.
So we must decrease to ≤6 before node 2.
At node 3: w3=3, must be ≤3.
At node 4: w4=6, can have up to 6.
At node 5: w5=8, can have up to 6.
So the optimal sequence: at node 0: 10. node1: 10. node2: 6 (decrease cost 4). node3: 3 (decrease cost 3). node4: 6 (increase cost 3). node5: 6 (no change). Total cost: 4+3+3=10. Plus start and end? The start cost is |Y - x0| = 0. End cost |x5 - Z| = 0. So total 10.

Now, can we do better? What if we go to 3 at node 3, then to 6 at node 4, cost 3+3=6, plus the initial 4 = 10. What if we go to 6 at node 2, stay at 6 until node 4, then go to 6? But at node 3, w3=3, so we cannot stay at 6. So we must go down to 3 at node 3. So the minimum cost is indeed 10.

The formula: the cost is the sum of the "drops" at the points where the bound forces a decrease. Specifically, we need to decrease whenever the current floor exceeds the next bound. The optimal is to decrease as late as possible, i.e., we stay at the current floor until the bound drops below it, then we decrease to the new bound? Or to the minimum required? Actually, we can decrease to any value ≤ the new bound. To minimize future cost, we should decrease to the maximum possible that doesn't cause future issues. But since the bounds are non-increasing on the left, decreasing to the new bound is optimal. On the right side, after the LCA, the bounds are non-decreasing. So we can increase as late as possible.

In general, for a path with bounds w0, w1, ..., wm, the minimum cost from Y to Z is: we can compute it by scanning. But for our tree, the path is V-shaped: non-increasing to LCA, then non-decreasing.

There is a known result: for a V-shaped bound sequence with minimum h at the LCA, the minimum cost from Y to Z is:
- If Y ≤ h and Z ≤ h: cost = |Y-Z|.
- If Y > h and Z > h: cost = (Y - h) + (Z - h) + something? Actually, if both > h, we can go down to h, then up to Z, cost = (Y-h) + (Z-h) = Y+Z - 2h. But is that possible? We have to go down to h, then up. The cost is the sum of absolute differences. If we go Y -> h -> Z, cost = (Y-h) + (Z-h) = Y+Z-2h. But we might also have to pay for the fact that the path from Y to h might have intermediate bounds. But since the bounds are decreasing, the minimum bound on the way is h, so we can go directly to h. Similarly on the way up. So cost = Y+Z-2h.
- If Y > h and Z ≤ h: cost = Y - h + (h - Z) = Y - Z. (Since we go down to h, then down to Z? But Z ≤ h, so from h to Z is down, cost h-Z. Total Y-h + h-Z = Y-Z. But wait, we have to go from h to Z on the right side. The bounds on the right are increasing from h. So we can go from h to Z directly? If Z ≤ h, then we are going down on the right side? But the bounds on the right are increasing, so the maximum bound at the LCA is h, and it increases. If Z ≤ h, we can go from h to Z, which is down. That's fine. Cost h-Z. So total Y-h + h-Z = Y-Z.
- If Y ≤ h and Z > h: cost = Z - Y.

Let's check the sample: Y=10 > h=3, Z=6 > h=3. According to the formula, cost = Y+Z-2h = 10+6-6=10. That matches.
What if Y=2, Z=4, h=3: both ≤ h? No, Z=4 > h=3. Formula for Y ≤ h, Z > h: cost = Z - Y = 4-2=2. Is that correct? Path bounds: w0=12, w1=10, w2=6, w3=3, w4=6, w5=8. Y=2, Z=4. h=3. Y=2 ≤ 3, Z=4 > 3. We can go from 2 to 4 directly? But at node 2, w2=6, ok. At node 3, w3=3, we must be ≤3. If we go from 2 to 4, we would pass through 4 at node 4, which is allowed (w4=6). But at node 3, we would need to be at some floor between 2 and 4. To minimize cost, we can go 2 -> 3 -> 4? Cost: |2-3| + |3-4| = 1+1=2. That matches Z-Y=2.
What if Y=5, Z=5, h=3: both > h. Cost = 5+5-6=4. Path: we go down to 3, then up to 5. Cost: 5-3 + 5-3 = 4. Can we do better? If we stay at 5, at node 3 w3=3, so we must decrease. So 4 is minimal.

So the formula is: cost = max(Y, h) + max(Z, h) - 2h? Let's see:
If Y ≤ h, Z ≤ h: max(Y,h)=h, max(Z,h)=h, sum -2h = 0? But cost is |Y-Z|. So that's not right.
Actually, the cost is: if Y ≤ h and Z ≤ h: cost = |Y-Z|.
If Y > h and Z > h: cost = (Y-h) + (Z-h) = Y+Z-2h.
If Y > h and Z ≤ h: cost = Y - h + (h - Z) = Y - Z.
If Y ≤ h and Z > h: cost = Z - Y.

This can be written as: cost = max(Y, Z, h) - min(Y, Z, h) ? No.
Let's test: Y=10, Z=6, h=3. max=10, min=3, diff=7, not 10.
Another: Y=5, Z=5, h=3. max=5, min=3, diff=2, not 4.

So the formula is not simply based on h. It depends on the relative order of Y, Z, h.

In fact, the cost is: we have to go from Y to Z. The bottleneck is h. We can think of the path as having a "valley" at height h. The cost is the total distance traveled: we go from Y to the valley, then from the valley to Z. But if both are on the same side of the valley, the cost is |Y-Z|. If one is above and one below, the cost is the distance from the higher to the lower plus the distance from the valley to the lower? No.

From the cases:
- Both ≤ h: cost = |Y-Z|.
- Both > h: cost = (Y-h) + (Z-h).
- One > h, one ≤ h: cost = |Y-Z|.

Notice that in the mixed case, the cost is exactly |Y-Z|. So in all cases, the cost is max( |Y-Z|, (Y-h)_+ + (Z-h)_+ ), where (x)_+ = max(0,x).

Check:
Y=10,Z=6,h=3: |10-6|=4, (10-3)+(6-3)=7+3=10, max=10.
Y=2,Z=4,h=3: |2-4|=2, (2-3)_+ + (4-3)_+ =0+1=1, max=2.
Y=5,Z=5,h=3: |0|=0, (2+2)=4, max=4.
Y=1,Z=10,h=3: |9|=9, (0+7)=7, max=9? But formula for Y≤h, Z>h is Z-Y=9. So max(9,7)=9. Correct.
Y=1,Z=2,h=3: |1|=1, (0+0)=0, max=1. Correct.

So the cost is max( |Y-Z|, max(0, Y-h) + max(0, Z-h) ).

Is this always true? Let's test with a path that has a more complex shape? But our path is V-shaped: decreasing to LCA, then increasing. So the minimum bound is h = weight(LCA). And the bounds on the left are ≥ h, and on the right are ≥ h. So the above formula should hold.

We can prove it: the optimal sequence is either monotonic or goes down to h and up. If both Y and Z are on the same side of h (both > h or both ≤ h), then the optimal is to go to h and back? No, if both > h, we can go down to h and up, cost Y-h + Z-h. If both ≤ h, we can go directly, cost |Y-Z|. If one > h and one ≤ h, we can go directly from the higher to the lower, cost |Y-Z|, by decreasing monotonically. But can we always do that? If Y > h and Z ≤ h, we want to go from Y to Z. We can decrease from Y to Z directly. Is that allowed? We need to ensure that at each node, the floor is ≤ w_i. Since we are decreasing from Y to Z, and Z ≤ h, the floor at each node is between Z and Y. The maximum floor on the left path is Y, but we start at Y. As we go up, the bounds decrease. If at some node w_i < Y, we need to decrease. But we are decreasing to Z. So we will be ≤ w_i if we decrease to Z before hitting the node. Since the bounds are non-increasing, the first node where w_i < Y is where we need to start decreasing. We can decrease to Z, and since Z ≤ h ≤ w_i, we are fine. On the right side, the bounds are non-decreasing, starting at h. If Z ≤ h, we can continue decreasing to Z, and at each node the bound is ≥ h ≥ Z, so it's fine. So yes, we can go directly from Y to Z with cost |Y-Z|.

Therefore, the cost is exactly max( |Y-Z|, max(0, Y-h) + max(0, Z-h) ).

This is a beautiful formula! So the answer for a query is: let h = weight(LCA(A,C)) in the merge tree. Then answer = max( |Y-Z|, max(0, Y-h) + max(0, Z-h) ).

We need to verify with the sample query 2: (1,1,6) to (1,2,4). The cells are adjacent. In the merge tree, what is the LCA of (1,1) and (1,2)? They are siblings under N10 (weight 10). So LCA is N10 with weight 10. h=10. Y=6, Z=4. |Y-Z|=2. Y-h = -4, Z-h = -6, so max(0,...) =0. So answer = max(2,0)=2. That matches the sample output 2.

So this formula works for the samples.

Now we need to build the merge tree and answer LCA queries with weights.

The merge tree is built as follows:
- For each cell, create a leaf node with weight F[i][j].
- Sort cells by F decreasing.
- Use union-find. Initially each cell is its own set.
- Also maintain a mapping from cell to its current node in the tree.
- When processing a cell (i,j) with height h, we activate it. For each active neighbor (i',j'), we union the sets. The union operation should merge the two components. The weight of the new node is min(h, F[neighbor])? Actually, the two components merge at the current floor h (since we are adding a cell of height h, and unioning with neighbors of height ≥ h). So the merge weight is h.
- We create a new node with weight h. Its children are the roots of the two components being merged. Then the new node becomes the root of the combined set.
- After processing all cells, we may have multiple trees. We can add a root with weight 0 and connect all tree roots to it.

We need to be careful: when we add a cell, it might have multiple active neighbors. We should union them all. This can be done by iterating over active neighbors and unioning pairwise. The resulting tree will have internal nodes with weight equal to the height at which the merge happened.

This tree has at most 2*HW - 1 nodes. We can then preprocess for LCA with weights. We need to answer LCA queries on this tree. The tree is static.

We can do a standard LCA preprocessing: depth, parents, etc. Since the tree is large (up to 5e5 nodes), we can use binary lifting.

For each query, we compute the LCA of the two leaf nodes (A,B) and (C,D). Let h = weight(LCA). Then compute the answer with the formula.

Let's verify the formula on another example. Suppose two cells are the same? Not allowed.

What if the LCA is the root with weight 0? Then h=0. Then answer = max(|Y-Z|, Y+Z). Since Y,Z ≥1, Y+Z ≥ |Y-Z|, so answer = Y+Z. That makes sense: if there is no path with any positive height, we have to go from Y to 0? But wait, the minimum height in the tree is 0 at the root. But the leaves have weight F≥1. The path between any two leaves goes up to some internal node with weight at least 1? Actually, the root is weight 0. The children of the root are the last merges. The minimum possible h is 1? Not necessarily: if two components never merge until weight 0, that means they are not connected even at floor 0. But at floor 0, every building has floor 0? No, the floors are 1-indexed. The walkways are available for floor X ≥1. So the graph G_X for X=1 is all cells with F≥1. Since F≥1, all cells are in G_1. So the whole grid is connected at floor 1. So in the merge tree, the root should have weight 1, not 0. Actually, the merges happen at the height of the cell being added. The last merge happens at the minimum height among all cells. Since all F≥1, the minimum F is at least 1. So the root will have weight equal to the minimum F in the grid. So h ≥ 1.

But we can add a root with weight 0 for convenience. Then the LCA of two cells might be the root with weight 0. In that case, the components never merged, meaning they are not connected at any floor >0? But as argued, at floor 1, all cells are connected. So they must have merged at some point. The last merge happens at the minimum height. So the root's weight should be the minimum height. So we don't need weight 0.

Let's test the formula when h is very large, e.g., h = min(F[A], F[C]). Then the path might be direct. If h ≥ max(Y,Z), then Y ≤ h and Z ≤ h, so answer = |Y-Z|. That makes sense: if the two cells are in a component where all heights are ≥ max(Y,Z), we can walk at a floor between Y and Z, so cost is |Y-Z|.

If h is small, answer = Y+Z-2h if both > h, which is the cost to go down to h and up.

So the formula seems correct.

Now, we need to build the merge tree correctly.

Algorithm to build the merge tree:
1. Read H, W and F.
2. Create a list of cells sorted by F descending. For each cell, store its coordinates and F.
3. Initialize union-find for H*W cells.
4. For each cell in sorted order:
   - Activate the cell.
   - For each of its 4 neighbors that are already active:
     - Union the two components. The union operation will merge the two trees. We need to create a new node with weight = current F. The children are the roots of the two trees. The new node becomes the root of the combined tree.
   - After processing all neighbors, the cell is now part of a component.
5. After processing all cells, we have a forest. We can add a root node with weight 0 (or weight = min F) and connect all tree roots to it.
6. We need to map each cell to its leaf node ID.
7. We can then run a DFS from the root to compute depth, parent[0], and weight for each node.
8. Preprocess binary lifting for LCA.
9. For each query, find the leaf nodes of (A,B) and (C,D). Compute their LCA. Get h = weight(LCA). Compute answer using the formula.

We need to be careful with the union operation: when we union two components, we need to get the current root nodes of those components. The union-find structure can store the current node ID for each set. Initially, each set has node ID = leaf ID. When we union two sets, we create a new node, and the new set's node ID is the new node. We also need to union the sets in the union-find.

The number of unions is at most the number of edges, which is O(HW). So the total number of nodes is O(HW).

Let's test this on the sample.

We need to sort cells by F descending. But we must be careful: when we process a cell, we union it with active neighbors. The active neighbors are those with F ≥ current F (since we process in descending order). The union happens at floor = current F. So the new node has weight = current F. This is correct.

In the sample, we processed in that order. The tree built matches the one we described.

Now, what about the case where multiple cells have the same F? The order among them doesn't matter as long as we process them all before moving to lower F. We can sort by F descending, and for equal F, any order. When we process a cell, we union with active neighbors. Since all cells with F > current F are already active, and cells with F = current F might not be active yet. So we only union with strictly greater F neighbors. This means that cells with the same F are not connected via walkways at floor F unless they are adjacent and both have F ≥ F. Actually, if two adjacent cells have the same F, say both have F=10, then when we process the first one, the second is not active. When we process the second, the first is active. They union at floor 10. So they will be connected at floor 10. That's correct: at floor 10, both have height 10, so walkway is possible.

But what if we process cells with the same F in some order, and we union them at floor F. That's correct.

However, we must ensure that when we process a cell, we only union with neighbors that are already active. That means neighbors with F > current F, or neighbors with F = current F that were processed earlier. This is fine because the merge floor is min(F[u], F[v]). Since we are processing in decreasing order, when we process a cell of height h, any active neighbor has height ≥ h. So the merge floor is h. This is exactly min(F[u], F[v]) because the neighbor has height ≥ h, so min is h. So the weight of the new node is h.

Now, we need to store the tree. We can use arrays: for each node, store weight, children, etc.

We also need to answer LCA queries quickly. We have up to 5e5 nodes. Binary lifting with log(5e5) ≈ 19. So O(log N) per query.

Total time: O(HW log HW) for building and preprocessing, and O(Q log HW) for queries. With HW=2.5e5 and Q=2e5, this is about 4.5e6 operations, which is very fast.

We need to be careful with 1-indexed or 0-indexed.

Let's write the steps in detail:

1. Read H, W.
2. Read F as a 2D array.
3. Create a list of cells: each cell is (F, i, j).
4. Sort the list in descending order of F.
5. Create a union-find array for H*W cells. Initially, each cell is its own set. The set ID is the cell index. We also need an array `node_id` for each set, initially the cell's leaf node ID.
6. Create a global node counter. For each cell, assign a leaf node ID. We can use an array `leaf_id[i][j]` to store the node ID for the leaf.
7. Also, we need to store the active status of each cell.
8. Process each cell in sorted order:
   - Let (i,j) be the cell, h = F[i][j].
   - Mark cell (i,j) as active.
   - For each of the 4 directions:
     - If neighbor (ni,nj) is active:
       - Get the root of (i,j) and (ni,nj) in union-find. If they are different, union them:
         - Create a new node with ID = next_node_id, weight = h.
         - The children are the current node IDs of the two sets.
         - Union the two sets in union-find. The new set's node ID is the new node ID.
   - After processing all neighbors, ensure that the set for (i,j) has the correct node ID. Actually, we can union as we go. But note: a cell might have multiple active neighbors. We should union them all into one component. We can do this by iterating over neighbors and unioning the cell's set with the neighbor's set.
9. After processing all cells, we have a set of roots. Create a root node with weight 0 (or weight = min F). For each root that is not the root node, add an edge from the root node to that root. This ensures a single tree.
10. Now we have a tree with N nodes (N = H*W + number of unions + 1). We can run a DFS from the root to compute depth, parent[0], and weight for each node. We also need to store the weight of each node.
11. Preprocess binary lifting: for k from 1 to LOG-1, parent[k][v] = parent[k-1][ parent[k-1][v] ].
12. For each query:
    - Get the leaf node IDs for (A,B) and (C,D).
    - Compute LCA of these two nodes. Let h = weight[LCA].
    - Compute ans = max( abs(Y-Z), max(0, Y-h) + max(0, Z-h) ).
    - Print ans.

We need to be careful with the weight of the root. If we set root weight = 0, then for any two cells, their LCA might be the root, and h=0. Then the formula gives max(|Y-Z|, Y+Z). Since Y,Z ≥1, this is Y+Z. But is that correct? If the grid is completely disconnected? But at floor 1, all cells are connected because all F≥1. So the merge tree should connect all cells at the minimum F. The root we add should have weight = min F, not 0. Because the last merges happen at the minimum height. So we should set the root weight to the minimum F in the grid. Alternatively, we can not add a root and just have the forest, but then we need to handle disconnected components? But the grid is always connected at floor 1. So the merge tree is actually a single tree? Not necessarily: if the grid has multiple components at floor 1? No, at floor 1, every building has at least 1 floor, so all cells are active. The graph G_1 is the entire grid, which is connected. So the union-find will eventually connect all cells. The last union will happen at the minimum F. So the tree is a single tree with root being the last node created with weight = min F. So we don't need an extra root. We can just take the root of the union-find as the root. But the root node has weight = min F. So h will be at least 1.

Wait, is the entire grid always connected at floor 1? The grid is H x W, and we can move between adjacent cells. The graph of cells is connected because the grid is connected. So yes, at floor 1, all cells are in the same component. So the merge tree is a single tree with root weight = minimum F.

So we can just use the root of the union-find as the root of our tree. We need to do a DFS from that root.

But we have to be careful: the union-find tree is built with nodes created during unions. The leaves are the original cells. The internal nodes are the union nodes. The root is the last node created. So we can do a DFS from that root.

We need to store the children of each internal node. When we create a new node during union, we know its two children. So we can build the tree as an adjacency list.

Then we DFS from the root to set depth, parent, and weight.

One more thing: the weight of a node is the floor at which the merge happened. For a leaf, the weight is F[i][j]. For an internal node, the weight is the height h at which the union was performed.

Now, the formula: answer = max( |Y-Z|, max(0, Y-h) + max(0, Z-h) ).

Let's test on a simple case: two adjacent cells, both height 10. Merge: we process one, then the other. The union happens at height 10. So the LCA of the two cells is the union node with weight 10. So h=10. Y and Z ≤10. Then answer = |Y-Z|. That matches: we can walk directly.

Another case: two cells separated by a cell of height 1. The path must go through the height 1 cell. The merge tree will have the union at height 1 for that part. So the LCA of the two cells will be the node with weight 1. Then h=1. If Y=10, Z=10, answer = max(0, 10-1 + 10-1) = 18. That is: go down to 1 (cost 9), walk, go up to 10 (cost 9). Total 18. That seems correct: you have to go down to floor 1 to pass through the low building, then up.

What if Y=1, Z=1? Then answer = max(0, 0) = 0. Correct.

What if Y=5, Z=5? answer = max(0, 4+4)=8. Go down to 1 (cost 4), up to 5 (cost 4). Correct.

So the formula is correct.

Now, we need to implement the merge tree building.

Implementation details:
- H, W up to 500, so HW up to 250,000.
- Number of nodes in tree: each cell is a leaf, each union creates a node. Number of unions is at most (number of edges) = O(HW). So total nodes ≤ 2*HW + 1.
- We can store the tree in arrays: for each node, weight, first_child, second_child. Since it's a binary tree (each union combines two components), it's a binary tree. We can store children as a list.
- We need to map (i,j) to a leaf node ID. We can assign leaf IDs from 0 to HW-1.
- Then node IDs for internal nodes start from HW.
- We need a union-find structure. Since we are processing cells in order, we can use a 2D array for parent in union-find. Also, we need to store the current node ID for each set. We can use a dict or a 2D array `set_node[i][j]`.
- When we union two cells, we get their roots (i1,j1) and (i2,j2). We get the node IDs of those sets. Then we create a new node with weight = current F, children = [node_id1, node_id2]. The new node ID is the next available. Then we union the two sets in union-find, and set the new set's node ID to the new node ID.
- We also need to mark cells as active. We can have a 2D boolean array.

We must be careful with the union order: we want to union the current cell with each active neighbor. But if we union one by one, the first union will create a new node, and then the next union will union that new node with another neighbor. That's fine, it still builds a tree. However, to make the tree binary, we should union pairwise. The standard way is to union the current cell's set with the neighbor's set. The current cell's set might have been already merged with previous neighbors. So the first neighbor we union with will merge the cell with that neighbor. Then the second neighbor will merge that component with the second neighbor. This creates a tree where the root of the component is the last union. The children of the new node are the roots of the two sets being merged. This is exactly what we want.

So in the loop for neighbors, we can do:
for each active neighbor:
    if find(i,j) != find(ni,nj):
        n1 = set_node[find(i,j)]
        n2 = set_node[find(ni,nj)]
        create new node with weight = h, children = [n1, n2]
        union(i,j, ni,nj)
        set_node[find(i,j)] = new_node_id

This will build a tree.

After processing all cells, we have a set of roots. Since the entire grid is connected at floor 1, there should be only one root. We can find the root by checking any cell's find. Or we can just take the node ID of the set containing (0,0) or something.

Then we do a DFS from that root to compute depth, parent[0], and weight. Since the tree is large, we should use an iterative DFS to avoid recursion limits.

For LCA, we need LOG = ceil(log2(N)). N up to 5e5, so LOG=19.

We need to store the weight of each node. The weight is the height at which the merge happened, or F[i][j] for leaves.

Now, queries: we have up to 2e5 queries. We need to read them, and for each, compute the answer.

We need to be careful: the input gives A,B,C,D as 1-indexed. We convert to 0-indexed.

Let's test with the sample.

Sample:
H=3, W=3
F:
12 10 6
1 1 3
8 6 7

Cells sorted by F:
(0,0):12
(0,1):10
(2,0):8
(2,2):7
(0,2):6
(2,1):6
(1,2):3

Process:
Init: each cell is its own set, node_id = leaf_id.
Leaf IDs: let's assign (0,0)=0, (0,1)=1, (0,2)=2, (1,0)=3, (1,1)=4, (1,2)=5, (2,0)=6, (2,1)=7, (2,2)=8.
Active: none.

Cell (0,0), h=12. Activate. Neighbors: (0,1) not active, (1,0) not active. No unions. Set node_id remains 0.

Cell (0,1), h=10. Activate. Neighbors: (0,0) active, (0,2) not, (1,1) not. Union with (0,0): n1=0, n2=1. Create node 9 with weight 10, children 0,1. Union sets. New set node_id=9.

Cell (2,0), h=8. Activate. Neighbors: (1,0) not, (2,1) not. No unions.

Cell (2,2), h=7. Activate. Neighbors: (1,2) not, (2,1) not. No unions.

Cell (0,2), h=6. Activate. Neighbors: (0,1) active, (1,2) not. Union with (0,1): set of (0,1) is node 9. n1=9, n2=2. Create node 10 with weight 6, children 9,2. Union. New set node_id=10.

Cell (2,1), h=6. Activate. Neighbors: (2,0) active, (2,2) active, (1,1) not. Union with (2,0): n1=6, n2=7. Create node 11 with weight 6, children 6,7. Union. New set node_id=11.
Now union with (2,2): set of (2,1) is node 11. set of (2,2) is node 8. n1=11, n2=8. Create node 12 with weight 6, children 11,8. Union. New set node_id=12.

Cell (1,2), h=3. Activate. Neighbors: (0,2) active, (1,1) not, (2,2) active. Union with (0,2): set of (0,2) is node 10. set of (1,2) is leaf 5. n1=10, n2=5. Create node 13 with weight 3, children 10,5. Union. New set node_id=13.
Union with (2,2): set of (1,2) is node 13. set of (2,2) is node 12. n1=13, n2=12. Create node 14 with weight 3, children 13,12. Union. New set node_id=14.

Now all cells processed. The root is node 14 with weight 3. The tree has nodes 0-14. The leaves: 0,1,2,3,4,5,6,7,8. Internal: 9(w10),10(w6),11(w6),12(w6),13(w3),14(w3).

Now query 1: (0,0,Y=10) to (2,0,Z=6). Leaf nodes: 0 and 6.
Path from 0 to 6: 0 -> 9 -> 10 -> 13 -> 14 -> 12 -> 11 -> 6? Wait, 6 is leaf 6, which is under 11. Let's trace:
0 is under 9. 9 is under 10. 10 is under 13. 13 is under 14. 14 has children 13 and 12. 12 has children 11 and 8. 11 has children 6 and 7.
So path: 0-9-10-13-14-12-11-6.
LCA of 0 and 6 is 14, weight=3. h=3.
Y=10, Z=6. |Y-Z|=4. Y-h=7, Z-h=3. Sum=10. max(4,10)=10. Correct.

Query 2: (0,0,Y=6) to (0,1,Z=4). Leaf nodes 0 and 1.
Path: 0-9-1. LCA is 9, weight=10. h=10.
Y=6, Z=4. |Y-Z|=2. Y-h=-4, Z-h=-6. max(0,..)=0. Answer=2. Correct.

So the algorithm works.

We need to implement the union-find with path compression. We also need to store the set_node ID. Since the grid is up to 500x500, we can use 2D arrays for parent and set_node.

Let's write the code.

Steps:
- Read H, W.
- Read F as a list of lists.
- Create a list of cells: [(F[i][j], i, j) for i in range(H) for j in range(W)].
- Sort the list in descending order of F.
- Initialize union-find: parent = [[(i,j) for j in range(W)] for i in range(H)].
- set_node = [[None]*W for _ in range(H)].
- leaf_id = [[-1]*W for _ in range(H)].
- Assign leaf_id for each cell: we can assign leaf_id[i][j] = i*W + j.
- set_node[i][j] = leaf_id[i][j] for all cells.
- active = [[False]*W for _ in range(H)].
- next_node_id = H*W.
- For each cell in sorted list:
  - h, i, j = cell
  - active[i][j] = True
  - for each direction:
    - ni, nj = neighbor
    - if active[ni][nj]:
      - root1 = find(i,j), root2 = find(ni,nj)
      - if root1 != root2:
        - n1 = set_node[root1]
        - n2 = set_node[root2]
        - create node: weight = h, children = [n1, n2]
        - union(i,j, ni,nj) -> let's say union takes (i,j) and (ni,nj), finds roots, and merges.
        - After union, set_node[find(i,j)] = next_node_id
        - next_node_id += 1
- After processing all cells, we have a set of roots. Since the whole grid is connected at floor 1, there should be one root. We can find the root of (0,0) or any cell. Let root = find(0,0). The tree root is set_node[root]. But note: the tree root is a node in the tree. We need to start DFS from that node.
- We have the tree stored as children. We need to build an adjacency list or just use the children arrays.
- We have an array `weight` for each node.
- We need to compute depth and parent[0] for each node. We can do a stack-based DFS.
- Then binary lifting.
- For queries, read Q, then for each query, read A,B,Y,C,D,Z. Convert A,C to 0-indexed.
- u = leaf_id[A][B], v = leaf_id[C][D].
- Compute LCA(u,v). Let h = weight[lca].
- ans = max(abs(Y-Z), max(0, Y-h) + max(0, Z-h))
- Print ans.

We need to be careful with the DFS: the tree is stored with children. We can do:
stack = [(root, 0, -1)] # (node, depth, parent)
while stack:
    node, d, p = stack.pop()
    depth[node] = d
    parent[0][node] = p
    weight[node] = weight[node]  # already set
    for child in children[node]:
        stack.append((child, d+1, node))

But we need to have weight for each node. We can initialize weight array with size N, and set weight for leaves and internal nodes when we create them.

Also, we need to store children for each node. Since the tree is binary, we can store left and right children, or a list.

Let's define:
N = H*W (max leaves)
We will have at most 2*N nodes.
We can use lists:
weight = [0] * (2*N)
children = [[] for _ in range(2*N)]
We will assign node IDs from 0 to H*W-1 for leaves.
For internal nodes, we assign the next available ID.

In the loop, when we create a new node:
    weight[next_node_id] = h
    children[next_node_id] = [n1, n2]
    next_node_id += 1

After building, we have a forest. The root is the node with no parent. Since we added a root? Actually, we didn't add an extra root. The root of the tree is the last node created, which is the root of the union-find. We can find it by taking any cell, e.g., (0,0), and doing find(0,0) to get the set root, then set_node[that root] is the node ID of the tree root.

But wait: the union-find root is a cell, not a tree node. The set_node maps the set root (a cell) to the tree node that is the current root of that component's tree. So the tree root is set_node[find(0,0)].

So we can do: tree_root = set_node[find(0,0)].

Then we DFS from tree_root.

Now, the number of nodes: we start with H*W leaves. Each union adds one node. The number of unions is at most (number of edges) which is about 2*H*W. So total nodes ≤ H*W + 2*H*W = 3*H*W. So we can allocate arrays of size 3*H*W.

But to be safe, we can allocate up to 4*H*W.

Now, LCA preprocessing: we need LOG = ceil(log2(max_nodes)). For 2.5e5 leaves, max_nodes ~ 1e6, log2(1e6) ~ 20. So LOG=20 or 21.

We can do:
LOG = 20
parent = [[0]*max_nodes for _ in range(LOG)]
depth = [0]*max_nodes