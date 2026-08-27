
## ideation
The problem asks for the minimum cost to reach vertex N from vertex 1 in a directed graph where we can either traverse an edge (cost 1) or reverse all edges (cost X). This can be modeled as a shortest path problem on a state graph with $2N$ states: $(v, 0)$ representing being at vertex $v$ with original orientation, and $(v, 1)$ representing being at vertex $v$ with reversed orientation.

Transitions:
1. From $(v, 0)$, for each edge $v \to u$ in the original graph, we can move to $(u, 0)$ with cost 1.
2. From $(v, 1)$, for each edge $u \to v$ in the original graph (which becomes $v \to u$ in the reversed graph), we can move to $(u, 1)$ with cost 1. This is equivalent to traversing the reverse edge $v \to u$ in the original graph's transpose.
3. From $(v, 0)$, we can reverse edges to go to $(v, 1)$ with cost X.
4. From $(v, 1)$, we can reverse edges to go to $(v, 0)$ with cost X.

We use Dijkstra's algorithm because edge weights are positive (1 and X). The number of states is $2N$ and edges are $2M + 2N$, so the complexity is $O((N+M) \log N)$, which fits within the constraints.

Pitfalls:
- Using 0-1 BFS is not directly applicable because X can be greater than 1. Dijkstra is safer.
- The answer can exceed $2^{31}-1$, so use 64-bit integers.
- Ensure the graph is built correctly for both orientations.

## worker: (None)
The problem is modeled as a shortest path problem on a state graph with $2N$ states: $(v, 0)$ for being at vertex $v$ with original orientation, and $(v, 1)$ for being at vertex $v$ with reversed orientation.

Transitions:
1. **Moving along an edge**: 
   - From $(v, 0)$, for each original edge $v \to u$, we can go to $(u, 0)$ with cost 1.
   - From $(v, 1)$, for each original edge $u \to v$ (which becomes $v \to u$ when reversed), we can go to $(u, 1)$ with cost 1. This is implemented by using the reverse adjacency list `adj_rev`.
2. **Reversing all edges**: From $(v, 0)$ to $(v, 1)$ with cost $X$, and vice versa.

Dijkstra's algorithm is used because edge weights are positive (1 and $X$). The number of states is $2N$ and the number of edges in the state graph is $2M + 2N$, leading to a time complexity of $O((N + M) \log N)$, which is efficient for the given constraints ($N, M \leq 2 \times 10^5$).

The answer is the minimum of `dist[N][0]` and `dist[N][1]`, representing the minimum cost to reach vertex $N$ in either orientation.
