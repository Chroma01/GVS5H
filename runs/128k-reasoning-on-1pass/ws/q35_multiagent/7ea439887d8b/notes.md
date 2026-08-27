
## ideation
The problem asks for the minimum cost to travel from vertex 1 to vertex N in a directed graph where we can traverse edges (cost 1) or reverse all edges (cost X). This can be modeled as a shortest path problem on a state graph with $2N$ states: $(u, 0)$ for being at vertex $u$ with the original graph orientation, and $(u, 1)$ for being at vertex $u$ with the reversed orientation.

Transitions:
1. Move along an edge: From $(u, 0)$ to $(v, 0)$ with cost 1 if $u \to v$ exists. From $(u, 1)$ to $(v, 1)$ with cost 1 if $v \to u$ exists in the original graph (which becomes $u \to v$ in the reversed graph).
2. Reverse edges: From $(u, 0)$ to $(u, 1)$ with cost $X$, and vice versa.

We can solve this using Dijkstra's algorithm. The number of states is $2N$, and the number of transitions is $2M + 2N$. Dijkstra runs in $O((N+M)\log N)$ time, which fits well within the limits for $N, M \le 2 \times 10^5$. We use a priority queue to explore states in increasing order of cost. The first time we pop a state with vertex $N$, that cost is guaranteed to be the minimum due to Dijkstra's property with non-negative edge weights.

Potential pitfalls:
- Large costs: Use 64-bit integers or Python's arbitrary precision integers.
- Graph representation: Maintain both original and reversed adjacency lists for efficient traversal.
- State updates: Ensure we only push to the priority queue if a strictly shorter path is found.
- Input parsing: Use fast I/O to handle large inputs efficiently within Python's overhead.

## worker: Read input values N, M, X and the edges.
The problem is modeled as a shortest path problem on a state graph with $2N$ nodes. Each state is represented as $(u, \text{dir})$, where $u$ is the current vertex and $\text{dir} \in \{0, 1\}$ indicates whether the graph is in its original or reversed orientation. 
- Moving along an edge costs 1 and keeps the orientation unchanged.
- Reversing all edges costs $X$ and flips the orientation.
Dijkstra's algorithm is used to find the minimum cost from $(1, 0)$ to any state with vertex $N$. The first time we pop a state with vertex $N$ from the priority queue, its cost is guaranteed to be minimal due to Dijkstra's property with non-negative weights. 
The implementation uses a flat array for distances and 0-based indexing for vertices to optimize memory and access time. Time complexity is $O((N+M)\log N)$, which fits well within the limits for $N, M \le 2 \times 10^5$. Python's arbitrary-precision integers handle large costs safely.
