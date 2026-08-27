
## ideation
The problem asks for the minimum number of moves to swap the positions of two pieces A and B on a connected undirected graph. The pieces cannot occupy the same vertex simultaneously. This can be modeled as finding the shortest path in a state graph where states are pairs $(u, v)$ representing the positions of A and B. The state space size is $N^2$, which is too large for a standard BFS ($N \le 2 \times 10^5$).

However, we can observe that if the graph is a tree, the problem has a specific structure. In a tree, there is a unique path between any two vertices. If this path has no branches (vertices with degree $\ge 3$) strictly between the start and end vertices, the pieces cannot pass each other, making the swap impossible. If there is a branch, one piece can move into the branch to let the other pass, incurring a detour cost. Specifically, for a tree, if possible, the cost is $2 \cdot dist(S, T) + 2$.

If the graph contains cycles, it is generally possible to swap the pieces. We can use the A* search algorithm to find the shortest path in the state graph. The heuristic function $h(u, v) = dist(T, u) + dist(S, v)$ is admissible and consistent, guiding the search efficiently. To handle the large state space, we use a priority queue and a hash map to store the best cost found so far for each state, allowing lazy deletion.

The algorithm is:
1.  Read input and build adjacency list.
2.  Compute shortest distances from S (`distS`) and from T (`distT`) using BFS.
3.  If the graph is a tree ($M = N - 1$):
    *   Check if there is a vertex strictly between S and T on the unique path that has degree $\ge 3$.
    *   If yes, output $2 \cdot dist(S, T) + 2$.
    *   Otherwise, output -1.
4.  If the graph has cycles ($M \ge N$):
    *   Run A* search from state $(S, T)$ to $(T, S)$.
    *   Use a priority queue ordered by $f = g + h$.
    *   Use a hash map to track the minimum $g$ (cost) for each state to avoid processing suboptimal paths.
    *   Output the cost when target state is reached.

## worker: finalize
The problem is modeled as finding the shortest path in a state graph where states are pairs $(u, v)$ representing positions of pieces A and B. The state space size is $N^2$, which is too large for standard BFS.
1. **Tree Case ($M = N-1$):** If the graph is a tree, the path between $S$ and $T$ is unique. Swapping is possible if and only if there is a vertex strictly between $S$ and $T$ on this path that has degree $\ge 3$ (providing a "sidetrack"). If possible, the cost is $2 \cdot dist(S, T) + 2$. Otherwise, it's impossible (-1).
2. **General Case ($M \ge N$):** The graph contains cycles, making swapping generally possible. We use A* search with heuristic $h(u, v) = dist_T[u] + dist_S[v]$, which is admissible and consistent. This guides the search efficiently towards the target state $(T, S)$. The priority queue stores states ordered by $f = g + h$. A dictionary `best_g` tracks the minimum cost to reach each state to prune suboptimal paths.
