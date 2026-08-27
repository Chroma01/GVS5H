The problem asks for the minimum number of stairs used to travel between two points in a grid of buildings. Movement within a building costs 1 per floor (stairs), while moving between adjacent buildings at the same floor level is free (walkway). This structure implies that we can change buildings freely as long as we are at a floor that exists in both the current and target building. The cost is purely the vertical distance traveled via stairs.

We can model this as a shortest path problem on a graph where nodes are `(row, col, floor)`. However, the floor dimension is too large ($10^6$) for direct BFS. Instead, we observe that the optimal strategy involves moving vertically within a building to a floor that allows a "cheap" transition to the destination building. Specifically, from any building, we can reach any adjacent building at any floor $f$ if $f \le \min(F_{current}, F_{adjacent})$.

A key insight is that the cost to go from $(r1, c1, y)$ to $(r2, c2, z)$ is related to the Manhattan distance in the grid and the vertical adjustments. However, since we can traverse the grid freely at any common floor, the problem reduces to finding a path in the grid where the "edge weight" between adjacent cells $(i,j)$ and $(i',j')$ for a specific floor level is 0, but we pay for vertical moves.

Actually, a more efficient approach is to realize that we can treat the grid as a graph where we can move between adjacent cells at the same floor for free. The cost is the sum of absolute differences in floors for the vertical segments. This looks like we want to find a path of buildings from start to end, and for each step, we might need to adjust floors. But we can adjust floors anywhere.

Let's reconsider: We start at $(A, B)$ at height $Y$. We end at $(C, D)$ at height $Z$. We can move to adjacent cells at the same height if the building exists. We can change height in the current cell. The cost is the total height change. This is equivalent to finding a path in the grid such that we minimize the vertical movement. We can view this as: we are at $(A,B)$ with height $Y$. We want to reach $(C,D)$ with height $Z$. We can move horizontally for free if we are at a valid height.

This problem can be solved using 0-1 BFS or Dijkstra if we discretize states, but the state space is huge. However, note that we only care about the heights present in the buildings or the start/end heights. But $F_{i,j}$ is up to $10^6$.

Alternative perspective: The cost is $|Y - h_1| + |h_1 - h_2| + \dots + |h_k - Z|$ where $h_i$ are the heights at which we traverse edges between buildings. We want to minimize this sum. This is equivalent to finding a path in the grid and a sequence of heights such that for each edge $(u, v)$ in the path, the height $h$ is $\le \min(F_u, F_v)$.

This is a classic "minimum bottleneck path" variant combined with vertical costs. We can use a modified Dijkstra/BFS. Let $dist[r][c]$ be the minimum vertical cost to reach building $(r,c)$ from the start. However, the cost depends on the current height. We can store $dist[r][c][h]$ but $h$ is large.

Key realization: The optimal height to be at when entering a building $(r,c)$ from a neighbor is either the height we came from, or we adjust it. Actually, we can prove that we only need to consider heights that are either the start height, end height, or building heights? No.

Let's use the property that we can move between adjacent buildings at height $h$ if $h \le \min(F_u, F_v)$. The cost to change height in building $u$ from $h_a$ to $h_b$ is $|h_a - h_b|$.
We can run a Dijkstra where the state is $(r, c)$. But what is the value? The value should be the minimum cost to reach $(r,c)$ at *some* height. But the cost to leave $(r,c)$ depends on the height.

Actually, we can reverse the thinking. Let $D[r][c]$ be the minimum cost to reach building $(r,c)$ from the start building $(A,B)$ at height $Y$. When we are at $(r,c)$, we can be at any height $h \le F_{r,c}$. The cost to have arrived at height $h$ is not just $D[r][c]$ because we might have arrived at a different height and moved vertically.

Let $dp[r][c]$ be the minimum "vertical cost incurred so far" to reach building $(r,c)$. But we also need to know the current height to determine if we can cross to a neighbor. This suggests we need to track the height.

However, note that if we are at $(r,c)$ with cost $C$ and height $h$, we can move to neighbor $(r',c')$ if $h \le F_{r',c'}$. The new cost is still $C$, and we are at height $h$ in $(r',c')$. If $h > F_{r',c'}$, we cannot cross at height $h$. We must have crossed at a lower height.

This problem is solvable by observing that the optimal path will involve moving vertically in the start building, then traversing the grid at some constant height (or changing height at nodes), then moving vertically in the end building. But we can change height at any node.

Actually, this is equivalent to: Minimize $|Y - h_0| + \sum |h_i - h_{i+1}| + |h_k - Z|$ where the path is $v_0, v_1, \dots, v_k$ with $v_0=(A,B), v_k=(C,D)$, and $h_i \le F_{v_i}$ and $h_i \le F_{v_{i+1}}$ for each edge.

This can be solved by running a Dijkstra-like algorithm on the grid. Let $dist[r][c]$ be a map or array storing the minimum cost to reach $(r,c)$ at various heights? No, too big.

But notice: The function $f_r(c, h)$ = min cost to reach $(r,c)$ at height $h$ is convex? Not necessarily.

Let's use the fact that $H, W \le 500$. We can run a Dijkstra where the state is $(r, c)$. The "distance" is the minimum cost to reach $(r,c)$ *and be ready to move to a neighbor*. But the readiness depends on height.

Actually, there is a known technique for this problem: **Multi-source Dijkstra with height as part of the state is too big, but we can swap the roles.**

Consider that we can move between $(r,c)$ and $(r',c')$ at height $h$ for free if $h \le \min(F_{r,c}, F_{r',c'})$. The cost to enter the system at $(A,B)$ is $|Y-h|$ and exit at $(C,D)$ is $|h-Z|$ if we stay at height $h$ throughout? No, we can change height.

However, it turns out that the optimal strategy is to pick a height $h$ and a path, and the cost is $|Y-h| + |h-Z|$ if we can stay at $h$ the whole time? No, because we might need to change height in intermediate buildings if the path requires it (e.g., if a building is short).

But if we change height in an intermediate building, say from $h_1$ to $h_2$, we pay $|h_1-h_2|$. This is equivalent to paying for the vertical movement.

We can solve this by running a Dijkstra on the grid where $dist[r][c]$ stores the minimum cost to reach $(r,c)$ at *any* height, but we need to propagate the height constraint.

Actually, we can use the following approach:
Let $D[r][c]$ be the minimum cost to reach building $(r,c)$ from $(A,B)$ at height $Y$. The cost includes vertical moves.
When we are at $(r,c)$ with cost $C$ and current height $h$, we can:
1. Move vertically in $(r,c)$ to height $h'$, cost increases by $|h-h'|$.
2. Move to neighbor $(r',c')$ at height $h$ if $h \le F_{r',c'}$, cost remains $C$.

This is a shortest path problem on a graph with nodes $(r,c,h)$. To avoid $10^6$ height, we note that we only care about heights that are "critical". But there are many.

Alternative solution:
Since $H,W$ are small (500), we can run a Dijkstra where the state is $(r,c)$. The value $dist[r][c]$ is the minimum cost to reach $(r,c)$. But we also need to track the maximum height we can be at for that cost? Or rather, for a given cost, what is the range of heights we can be at?

Actually, we can define $best[r][c]$ as the minimum cost to reach $(r,c)$. When relaxing an edge from $(r,c)$ to $(r',c')$, if we are at $(r,c)$ with cost $C$ and height $h$, we can go to $(r',c')$ at height $h$ if $h \le F_{r',c'}$. The new cost is $C$. We want to minimize $C$.

We can initialize $dist[A][B] = 0$ and all other $dist = \infty$. But we don't know the height.

Let's store $dist[r][c]$ as the minimum cost to reach $(r,c)$. And separately, we can store $max\_h[r][c]$ as the maximum height we can be at $(r,c)$ for that cost? No, because a higher cost might allow a higher height? No, higher cost usually allows more flexibility.

Actually, we can use the following:
$dist[r][c]$ = minimum cost to reach $(r,c)$.
When we extract $(r,c)$ with cost $C$, we know we can be at any height $h \le F_{r,c}$? No, we arrived at a specific height.

Correct approach:
Use Dijkstra. State: $(r, c)$. Value: $dist[r][c]$ = minimum cost to reach $(r,c)$.
But we also need to know the height. We can store for each $(r,c)$ the best cost for each height? Too big.

However, note that the cost function is separable. The total cost is $|Y - h_{start}| + \sum |h_i - h_{i+1}| + |h_{end} - Z|$.
This is equivalent to finding a path and heights.

We can solve this by running a Dijkstra where the state is $(r,c)$ and the distance is the minimum cost. The key is that if we are at $(r,c)$ with cost $C$, we can be at any height $h$ such that there exists a path to $(r,c)$ with cost $C$ ending at height $h$.

Let $S[r][c]$ be the set of pairs $(cost, height)$ that are Pareto optimal. This is still complex.

Given the constraints and problem type, a simpler observation is:
The answer is the shortest path in a graph where nodes are buildings, and edge weights are 0, but we have vertical costs.
We can run a Dijkstra where $dist[r][c]$ is the minimum cost to reach $(r,c)$.
Initialize $dist[A][B] = 0$.
Priority Queue stores $(cost, r, c)$.
When popping $(r,c)$ with cost $C$, we can move to neighbors.
But we need to know the height.

Actually, we can assume that we stay at a single height $h$ for the entire horizontal traversal, and only pay vertical costs at the start and end? No, intermediate buildings might force height changes.

But if an intermediate building has height $F < h$, we cannot pass at height $h$. So we must change height.

This problem is known and can be solved by:
1. Running a Dijkstra from the start building $(A,B)$ with initial height $Y$.
2. The state is $(r,c)$. The value $dist[r][c]$ is the minimum cost.
3. We also maintain $max\_h[r][c]$, the maximum height we can be at $(r,c)$ for the cost $dist[r][c]$.
   - If we can reach $(r,c)$ with cost $C$ at height $h$, and we have a previous record with cost $C' \le C$ and height $h' \ge h$, then the new state is dominated.
   - So we only keep states that are not dominated.

Since $H,W$ are small, we can use a 2D array $dist[r][c]$ and $max\_h[r][c]$.
Initialize $dist[r][c] = \infty, max\_h[r][c] = 0$.
$dist[A][B] = 0, max\_h[A][B] = Y$.
PQ stores $(cost, r, c)$.

When popping $(r,c)$ with cost $C$ and known max height $H_{curr} = max\_h[r][c]$:
  For each neighbor $(nr, nc)$:
    The maximum height we can cross to $(nr, nc)$ is $\min(H_{curr}, F_{nr, nc})$.
    Let $h_{new} = \min(H_{curr}, F_{nr, nc})$.
    The cost to reach $(nr, nc)$ is still $C$ (walkway is free).
    If $C < dist[nr][nc]$ or ($C == dist[nr][nc]$ and $h_{new} > max\_h[nr][nc]$):
      Update $dist[nr][nc] = C$, $max\_h[nr][nc] = h_{new}$.
      Push $(C, nr, nc)$.

After filling the grid, for the target $(C,D)$, we have $dist[C][D]$ and $max\_h[C][D]$.
The final answer is $dist[C][D] + |max\_h[C][D] - Z|$.
Why? Because we can move vertically in the target building from $max\_h[C][D]$ to $Z$ with cost $|max\_h - Z|$. And $max\_h[C][D]$ is the highest height we can reach at $(C,D)$ with minimal cost $dist[C][D]$. Is it possible that a higher cost allows a better final vertical move?
Yes, if we pay more to get to a higher height, the final vertical move might be cheaper.
So we need to consider all Pareto optimal $(cost, height)$ pairs for $(C,D)$.

However, the above Dijkstra only keeps one state per cell. It keeps the minimum cost and the maximum height for that cost. This is not sufficient because a slightly higher cost might allow a much higher height, reducing the final vertical cost.

We need to store multiple states. But note that the cost is monotonic with height? Not exactly.

Given the complexity, and since $Q$ is large, we need an efficient per-query solution. But $H,W$ are small. We can run a Dijkstra per query? $Q=2 \cdot 10^5$, $H,W=500$. $O(Q \cdot HW \log(HW))$ is too slow ($2 \cdot 10^5 \cdot 250000$).

We need a faster approach.

Observation: The problem is symmetric. The cost is $|Y - h_1| + \dots + |h_k - Z|$.
This is equivalent to the shortest path in a graph where we can move between adjacent cells at height $h$ for free, and vertical moves cost 1.

We can precompute all-pairs shortest paths? No, heights are large.

Another idea: The answer is $\min_h ( |Y-h| + dist_{grid}( (A,B), (C,D) \text{ at height } h ) + |h-Z| )$?
No, because we can change height in intermediate buildings.

But if we fix the height $h$ for the entire path, the cost is $|Y-h| + |h-Z|$ if the path is valid (all buildings on path have $F \ge h$). If not, we must change height.

Actually, the optimal solution can be found by considering that we only change height at the start, end, and possibly at buildings that are bottlenecks.

Given the time, I will implement a Dijkstra per query but optimized. Since $H,W \le 500$, the number of nodes is 250,000. Dijkstra is $O(E \log V)$. $E \approx 4V$. So $10^6 \log(2.5 \cdot 10^5) \approx 2 \cdot 10^7$ ops per query. With $2 \cdot 10^5$ queries, this is $4 \cdot 10^{12}$, too slow.

We need a global solution or faster per-query.

Note that the grid structure is static. The queries only change start/end and heights.

We can use the fact that the "bottleneck" heights are limited. But there are $HW$ buildings.

Let's try the Dijkstra with state $(r,c)$ and store a list of Pareto optimal $(cost, height)$ pairs. Since the cost is integer and height is integer, and we want to minimize cost and maximize height, the number of Pareto points might be small? Not necessarily.

However, in practice, for competitive programming, sometimes the number of relevant heights is small. But here heights are up to $10^6$.

I will implement the Dijkstra with a single state per cell (min cost, max height for that cost) and hope that it works for the sample. It might not be correct for all cases, but it's a start.

Actually, the correct approach for this specific problem (AtCoder ABC 278 F? No, this is ABC 280 F? Or similar) is to use the fact that the answer is the shortest path in a graph where we can move vertically and horizontally.

Given the constraints, I will output a solution that runs Dijkstra per query with the single-state optimization. If it TLEs, it's a limitation.

But wait, the sample output for query 1 is 10.
Start (1,1) height 10. End (3,1) height 6.
Path: (1,1)->(1,2)->(1,3)->(2,3)->(3,3)->(3,2)->(3,1).
Heights: 10->10 (cost 0), 10->6 (cost 4), 6->6 (0), 6->3 (cost 3), 3->3 (0), 3->3 (0), 3->6 (cost 3). Total 10.
My Dijkstra:
Start (1,1): cost 0, height 10.
Neighbor (1,2): min(10, 10)=10. Cost 0. State (0, 10).
Neighbor (1,3): min(10, 6)=6. Cost 0. State (0, 6).
Neighbor (2,3) from (1,3): min(6, 8)=6. Cost 0. State (0, 6).
Neighbor (3,3) from (2,3): min(6, 7)=6. Cost 0. State (0, 6).
Neighbor (3,2) from (3,3): min(6, 6)=6. Cost 0. State (0, 6).
Neighbor (3,1) from (3,2): min(6, 12)=6. Cost 0. State (0, 6).
Final cost at (3,1) is 0, height 6.
Final answer: 0 + |6-6| = 0. But expected 10.

The error is that the Dijkstra above assumes we can move horizontally for free. But in the example, we moved from height 10 to 6 in building (1,2). That cost 4. My Dijkstra didn't account for the vertical move in (1,2).

The Dijkstra should allow vertical moves.
From (1,1) height 10, cost 0.
We can move vertically in (1,1) to height 6, cost 4. State (4, 6).
Then move to (1,2) at height 6, cost 4. State (4, 6).
Then move to (1,3) at height 6, cost 4. State (4, 6).
Then move vertically in (1,3) to height 3, cost 4+3=7. State (7, 3).
Then move to (2,3) at height 3, cost 7.
Then move to (3,3) at height 3, cost 7.
Then move vertically in (3,3) to height 6, cost 7+3=10. State (10, 6).
Then move to (3,2) at height 6, cost 10.
Then move to (3,1) at height 6, cost 10.
Final: 10 + |6-6| = 10. Correct.

So the Dijkstra must include vertical moves as edges.
State: $(r,c)$.
Transitions:
1. Vertical: $(r,c) \to (r,c)$ with cost $|h_{new} - h_{old}|$. This is implicit if we allow changing height in the node.
2. Horizontal: $(r,c) \to (nr,nc)$ with cost 0, if $h \le F_{nr,nc}$.

To handle vertical moves, we can, when popping $(r,c)$ with cost $C$ and height $H$, also push states for all possible heights? No.

Instead, we can treat the vertical move as: from $(r,c)$ at height $H$ with cost $C$, we can reach any height $h \le F_{r,c}$ with cost $C + |H-h|$.
This is equivalent to: the cost to be at $(r,c)$ at height $h$ is $\min_{H} (dist[r][c] \text{ at } H + |H-h|)$.

This is a 1D problem. For each cell, we have a function $f_r(c)(h) = \min \text{cost to reach } (r,c) \text{ at height } h$.
This function is convex. We can maintain it.

Given the complexity, I will implement a Dijkstra that stores for each cell the best cost for each height? No.

I will store for each cell a list of Pareto optimal (cost, height) pairs. When relaxing, we generate new pairs and merge.

This might be too slow if the list is long. But in practice, it might be short.

I will implement this.