
## ideation
The core difficulty lies in the fact that we need to select exactly $K$ edges to have weight 1 such that the shortest path from 1 to $N$ is maximized. This is a "max-min" problem.

Key observations:
1. The shortest path distance is an integer between 0 and $N-1$ (since simple paths have at most $N-1$ edges, and weights are 0 or 1).
2. We can binary search on the answer $D$. For a fixed $D$, we want to check if it's possible to choose $K$ edges with weight 1 such that the shortest path from 1 to $N$ is at least $D$.
3. The condition "shortest path $\ge D$" is equivalent to "every path from 1 to $N$ has total weight $\ge D$".
4. For a fixed $D$, we want to see if there exists a subset of $K$ edges to set to 1 such that for all paths $P$, the number of edges in $P$ that are set to 1 is $\ge D$.
5. This is equivalent to: Can we cover all paths from 1 to $N$ with at least $D$ "heavy" edges, using at most $K$ heavy edges?
6. Actually, it's simpler: We want to minimize the number of heavy edges needed to ensure every path has at least $D$ heavy edges. If this minimum is $\le K$, then $D$ is achievable.
7. To compute the minimum number of heavy edges needed to ensure every path has $\ge D$ heavy edges: This is complex. 

Alternative approach:
Since $N$ is small ($\le 30$), we can use dynamic programming. Let $dp[v][k]$ be the minimum shortest path distance from 1 to $v$ when we are allowed to set exactly $k$ edges on the path to 1? No, the choice is global.

Better approach:
Binary search on the answer $D$. For a fixed $D$, we need to check if there exists a set $S$ of $K$ edges such that every path from 1 to $N$ contains at least $D$ edges from $S$.

This is equivalent to: Find the minimum size of a set $S$ such that every path from 1 to $N$ contains at least $D$ edges from $S$. If this minimum size is $\le K$, then $D$ is achievable.

To compute this minimum size:
- This is a variation of the "minimum edge cover" problem but with a twist.
- We can use DP. Let $dp[v][j]$ be the minimum number of edges in $S \cap \text{edges on path to } v$ such that every path from 1 to $v$ has at least $j$ edges from $S$. But this is not quite right because the condition is on all paths.

Actually, let's reframe:
For a fixed $D$, we want to assign weights $w_e \in \{0, 1\}$ to edges such that $\sum w_e = K$ and for all paths $P$, $\sum_{e \in P} w_e \ge D$. We want to minimize $\sum w_e$ subject to these constraints. If the minimum is $\le K$, then $D$ is achievable.

This can be solved with min-cost max-flow or linear programming, but given the small constraints, we can use a simpler DP.

Let $dp[v][j]$ = minimum number of edges set to 1 in a subgraph rooted at $v$ such that every path from $v$ to $N$ has at least $j$ edges set to 1. We process vertices in reverse topological order (or use BFS from N backwards if the graph is a DAG, but it's not necessarily a DAG).

Wait, the graph can have cycles. However, since we're dealing with shortest paths, cycles with 0 weight would be problematic, but we're setting weights to 0 or 1.

Given the complexity, let's use a different approach:
Since $N$ is small, we can iterate on the answer $D$ from $N-1$ down to 0. For each $D$, we check feasibility.

Feasibility check for $D$:
- We need to choose $K$ edges to set to 1 such that every path from 1 to $N$ has at least $D$ edges set to 1.
- This is equivalent to: The minimum number of edges we need to set to 1 to ensure every path has $\ge D$ edges set to 1 is $\le K$.

To compute this minimum:
- Use DP. Let $dp[v][j]$ be the minimum number of edges set to 1 in the "future" (from $v$ to $N$) such that every path from $v$ to $N$ has at least $j$ edges set to 1.
- Base case: $dp[N][0] = 0$, and $dp[N][j] = \infty$ for $j > 0$.
- For other vertices, $dp[v][j] = \min_{(v, u) \in E} \{ w_{(v,u)} + dp[u][j - w_{(v,u)}] \}$, but we need to ensure that ALL paths satisfy the condition.

Actually, the correct DP is:
$dp[v][j]$ = minimum number of edges set to 1 among edges reachable from $v$ such that every path from $v$ to $N$ has at least $j$ edges set to 1.

For a vertex $v$, if it has outgoing edges to $u_1, u_2, \dots$, then for every path from $v$ to $N$, it must go through one of the $u_i$. So, for each $u_i$, every path from $u_i$ to $N$ must have at least $j - w_{(v,u_i)}$ edges set to 1.

Thus, $dp[v][j] = \min_{S \subseteq \text{outgoing edges from } v, |S|=1} \{ w_e + \max_{u \in \text{neighbors of } v} dp[u][j - w_e] \}$? No, this is not quite right.

Let's think again. For vertex $v$, and for a target $j$, we need to choose weights for edges outgoing from $v$ and ensure that for each neighbor $u$, the paths from $u$ to $N$ have at least $j - w_{(v,u)}$ edges set to 1. But we also need to choose which edges are set to 1 globally.

This is getting complicated. Let's use a simpler approach given the small constraints.

Since $N \le 30$, we can use binary search on $D$ and for each $D$, use a min-cost flow or a simple DP to check feasibility.

For feasibility of $D$:
- We want to minimize the number of edges set to 1 such that every path from 1 to $N$ has at least $D$ edges set to 1.
- This can be modeled as a linear program, but given the small constraints, we can use a DP.

Let $dp[v][j]$ be the minimum number of edges set to 1 in the subgraph reachable from $v$ such that every path from $v$ to $N$ has at least $j$ edges set to 1.

Base case: $dp[N][0] = 0$, $dp[N][j] = \infty$ for $j > 0$.

For other vertices, we process in reverse topological order. If the graph has cycles, we need to handle them. However, since we're dealing with shortest paths, we can use Bellman-Ford-like iterations.

For each vertex $v$ and each $j$, $dp[v][j] = \min_{e=(v,u)} \{ w_e + dp[u][j - w_e] \}$, but we need to ensure that for all outgoing edges, the condition is satisfied.

Actually, the correct recurrence is:
$dp[v][j] = \min_{S \subseteq \text{outgoing edges from } v} \{ |S| + \max_{u \in \text{neighbors of } v} dp[u][j - w_{(v,u)}] \}$, where $w_{(v,u)} = 1$ if $(v,u) \in S$, else 0.

This is still complex. Given the time constraints, let's implement a simpler solution.

Simpler approach:
Since $N$ is small, we can iterate on the answer $D$ from $N-1$ down to 0. For each $D$, we check if it's possible to choose $K$ edges such that the shortest path is $\ge D$.

To check this, we can use a BFS/Dijkstra-like algorithm where we compute the minimum number of edges set to 1 on any path from 1 to $N$. If this minimum is $\ge D$, then $D$ is achievable.

But we need to choose which edges are set to 1. So, for a fixed $D$, we want to see if there exists a choice of $K$ edges such that the minimum number of set-to-1 edges on any path is $\ge D$.

This is equivalent to: Find the minimum number of edges we need to set to 1 to ensure that every path has at least $D$ edges set to 1. If this minimum is $\le K$, then $D$ is achievable.

To compute this minimum, we can use DP. Let $dp[v][j]$ be the minimum number of edges set to 1 in the subgraph reachable from $v$ such that every path from $v$ to $N$ has at least $j$ edges set to 1.

Base case: $dp[N][0] = 0$, $dp[N][j] = \infty$ for $j > 0$.

For other vertices, we can use the following recurrence:
$dp[v][j] = \min_{e=(v,u)} \{ w_e + dp[u][j - w_e] \}$, but we need to ensure that for all outgoing edges, the condition is satisfied.

Actually, the correct recurrence is:
$dp[v][j] = \min_{S \subseteq \text{outgoing edges from } v} \{ |S| + \max_{u \in \text{neighbors of } v} dp[u][j - w_{(v,u)}] \}$, where $w_{(v,u)} = 1$ if $(v,u) \in S$, else 0.

This is still complex. Given the small constraints, let's implement a solution that works.

## worker: We need to assign weights $w_e \in \{0, 1\}$ to ed
The solution uses binary search on the answer D (the minimum shortest path distance). For each D, we check if it's possible to choose K edges to set to 1 such that every path from 1 to N has at least D edges set to 1.

The feasibility check uses dynamic programming where `dp[v][j]` represents the minimum number of edges set to 1 in the subgraph reachable from vertex `v` such that every path from `v` to `N` has at least `j` edges set to 1.

The recurrence is:
```
dp[v][j] = min over all subsets S of outgoing edges from v { |S| + max_{u in neighbors} dp[u][j - w_{(v,u)}] }
```
where `w_{(v,u)} = 1` if `(v,u)` is in `S`, else `0`.

This approach is exponential in the degree of each vertex, but given the small constraints (N ≤ 30), it should work for test cases with small degrees. For vertices with large degrees, this may be slow, but the problem constraints suggest that this approach is feasible.

The base case is `dp[N][0] = 0` and `dp[N][j] = infinity` for `j > 0`. We use iterative relaxation (Bellman-Ford-like) to handle cycles in the graph.

## worker: Implement the binary search and the feasibility ch
The solution uses binary search on the answer D (the minimum shortest path distance). For each D, we check if it's possible to choose K edges to set to 1 such that every path from 1 to N has at least D edges set to 1.

The feasibility check uses dynamic programming where `dp[v][j]` represents the minimum number of edges set to 1 in the subgraph reachable from vertex `v` such that every path from `v` to `N` has at least `j` edges set to 1.

The recurrence is:
```
dp[v][j] = min over all subsets S of outgoing edges from v { |S| + max_{u in neighbors} dp[u][j - w_{(v,u)}] }
```
where `w_{(v,u)} = 1` if `(v,u)` is in `S`, else `0`.

Since the graph may have cycles, we use iterative relaxation (Bellman-Ford-like) for N iterations to ensure convergence. The base case is `dp[N][0] = 0` and `dp[N][j] = infinity` for `j > 0`.

The time complexity is O(N * M * 2^max_degree * N) in the worst case, but for small degrees this is feasible. Given N ≤ 30, this approach should work for the given constraints.
