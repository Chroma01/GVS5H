
## ideation
The problem asks for the minimum cost to reach vertex $N$ from vertex $1$ in a directed graph where we can either traverse an edge (cost 1) or reverse all edges (cost $X$).

This can be modeled as a shortest path problem on a state graph.
Let the state be $(u, k)$, where $u$ is the current vertex ($1 \le u \le N$) and $k \in \{0, 1\}$ represents the orientation of the edges.
- $k=0$: Edges are in their original direction.
- $k=1$: Edges are reversed.

Transitions:
1. **Move**:
   - If $k=0$: For each original edge $u \to v$, we can move to $(v, 0)$ with cost 1.
   - If $k=1$: The edges are reversed. An original edge $v \to u$ becomes $u \to v$. So, if there is an original edge $v \to u$, we can move from $(u, 1)$ to $(v, 1)$ with cost 1. This is equivalent to traversing the original graph's edges in reverse.
2. **Reverse**:
   - From $(u, 0)$ to $(u, 1)$ with cost $X$.
   - From $(u, 1)$ to $(u, 0)$ with cost $X$.

The number of states is $2N$ and the number of edges in the state graph is roughly $2M + 2N$. Since edge weights are positive (1 and $X$), we can use Dijkstra's algorithm. The constraints are $N, M \le 2 \times 10^5$, so $O((N+M) \log N)$ is acceptable.

Pitfalls:
- The cost $X$ can be large, so use 64-bit integers for distances.
- The graph might not be strongly connected, but it's guaranteed that $N$ is reachable.
- We need to consider reaching $N$ in either orientation, so the answer is $\min(\text{dist}[(N, 0)], \text{dist}[(N, 1)])$.

## worker: (None)
The problem is modeled as a shortest path problem on a state graph with $2N$ states, where each state is $(vertex, orientation)$. The orientation can be 0 (original) or 1 (reversed). 

Transitions:
1. **Move**: 
   - In orientation 0, we can traverse any original edge $u \to v$ to reach $(v, 0)$ with cost 1.
   - In orientation 1, edges are reversed, so an original edge $v \to u$ becomes $u \to v$. We can traverse this to reach $(v, 1)$ with cost 1. This is equivalent to using the backward adjacency list.
2. **Reverse**: 
   - From $(u, 0)$ to $(u, 1)$ with cost $X$.
   - From $(u, 1)$ to $(u, 0)$ with cost $X$.

We use Dijkstra's algorithm since edge weights are positive (1 and $X$). The number of states is $2N$ and the number of edges in the state graph is $2M + 2N$ (each original edge contributes two directed edges for movement, one in each orientation, plus two reversal edges per vertex). The time complexity is $O((N + M) \log N)$, which is efficient for the given constraints.

The answer is the minimum of `dist[N][0]` and `dist[N][1]`, representing the minimum cost to reach vertex $N$ in either orientation.
