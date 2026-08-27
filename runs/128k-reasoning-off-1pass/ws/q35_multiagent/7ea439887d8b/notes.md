
## ideation
The problem asks for the minimum cost to reach vertex N from vertex 1 in a directed graph where we can either traverse an edge (cost 1) or reverse all edges (cost X). This can be modeled as a shortest path problem on a state graph.

Key observations:
1. The state can be represented as `(vertex, orientation)`, where `orientation` is 0 for the original graph and 1 for the reversed graph.
2. There are two types of transitions:
   - Moving along an edge: If in orientation 0, we can move from `u` to `v` if there's an edge `u->v` in the original graph, costing 1. If in orientation 1, we can move from `v` to `u` if there's an edge `u->v` in the original graph (since the edge is now `v->u`), costing 1.
   - Reversing edges: From any vertex `u`, we can switch from orientation 0 to 1 or vice versa, costing X.

3. The state graph has `2N` nodes: `(u, 0)` and `(u, 1)` for each vertex `u`.
4. Edges in the state graph:
   - For each original edge `u -> v`:
     - Add edge `(u, 0) -> (v, 0)` with weight 1.
     - Add edge `(v, 1) -> (u, 1)` with weight 1.
   - For each vertex `u`:
     - Add edge `(u, 0) -> (u, 1)` with weight X.
     - Add edge `(u, 1) -> (u, 0)` with weight X.

5. We run Dijkstra's algorithm from `(1, 0)` to find the shortest path to `(N, 0)` and `(N, 1)`. The answer is the minimum of these two distances.

Pitfalls to avoid:
- The number of nodes and edges can be large (`N, M <= 2*10^5`), so we need an efficient implementation of Dijkstra's algorithm (using a priority queue).
- The cost X can be up to `10^9`, so the total cost can exceed the 32-bit integer range. We should use 64-bit integers for distances.
- The graph is guaranteed to have a path from 1 to N, so we don't need to handle unreachable cases.

## worker: <empty>
The problem is modeled as a shortest path problem on a state graph with $2N$ nodes, where each node represents a pair $(vertex, orientation)$. The orientation is 0 for the original graph and 1 for the reversed graph.

Transitions:
1. **Moving along an edge**: Costs 1.
   - In orientation 0, we can traverse original edges $u \to v$.
   - In orientation 1, we can traverse reversed edges, which means if there's an original edge $v \to u$, we can go from $u$ to $v$ in the reversed graph.
2. **Reversing all edges**: Costs $X$. This switches the orientation from 0 to 1 or 1 to 0 at the same vertex.

We use Dijkstra's algorithm with a priority queue to find the minimum cost to reach either $(N, 0)$ or $(N, 1)$. The answer is the minimum of these two distances.

The time complexity is $O((N + M) \log N)$ due to Dijkstra's algorithm with a priority queue, which is efficient enough for the given constraints ($N, M \leq 2 \times 10^5$).
