The problem asks for the minimum cost to travel from vertex 1 to vertex $N$ in a directed graph where we can either traverse an edge (cost 1) or reverse all edges in the graph (cost $X$). This can be modeled as a shortest path problem on a state graph. The state is defined by the current vertex and the current orientation of the graph (original or reversed). There are $2N$ states: $(u, 0)$ for vertex $u$ in original orientation, and $(u, 1)$ for vertex $u$ in reversed orientation.

We can use Dijkstra's algorithm to find the shortest path from state $(1, 0)$ to either $(N, 0)$ or $(N, 1)$. The transitions are:
1. From $(u, 0)$, move to $(v, 0)$ with cost 1 if there is an edge $u \to v$ in the original graph.
2. From $(u, 1)$, move to $(v, 1)$ with cost 1 if there is an edge $v \to u$ in the original graph (which becomes $u \to v$ in the reversed graph).
3. From $(u, 0)$, switch to $(u, 1)$ with cost $X$.
4. From $(u, 1)$, switch to $(u, 0)$ with cost $X$.

We implement this by maintaining adjacency lists for the original graph and its reverse, and running Dijkstra on the implicit state graph. The answer is the minimum distance to reach vertex $N$ in either state.