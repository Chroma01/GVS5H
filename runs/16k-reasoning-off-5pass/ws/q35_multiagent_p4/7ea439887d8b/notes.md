
## ideation
The core difficulty lies in modeling the state space correctly to account for the edge reversal operation. The key insight is that the graph's connectivity changes globally when edges are reversed. We can model this as a shortest path problem on a state graph with $2N$ nodes: $(v, 0)$ representing being at vertex $v$ in the original orientation, and $(v, 1)$ representing being at vertex $v$ in the reversed orientation.

Transitions in this state graph are:
1. **Move**: From $(u, 0)$ to $(v, 0)$ if there is an edge $u \to v$ in the original graph, with cost 1.
2. **Move**: From $(u, 1)$ to $(v, 1)$ if there is an edge $v \to u$ in the original graph (which becomes $u \to v$ in the reversed graph), with cost 1.
3. **Reverse**: From $(u, 0)$ to $(u, 1)$ with cost $X$.
4. **Reverse**: From $(u, 1)$ to $(u, 0)$ with cost $X$.

Since edge weights are non-negative (1 and $X \ge 1$), Dijkstra's algorithm is appropriate. The number of states is $2N$ and the number of edges is $2M + 2N$, so the complexity $O((N+M) \log N)$ fits within the constraints.

Pitfalls to avoid:
- Forgetting that moving in the reversed state requires checking the *original* graph's reverse edges.
- Using BFS instead of Dijkstra if $X$ was small, but since $X$ can be large, Dijkstra is the safe general choice. Actually, since all costs are positive, Dijkstra is standard. Note that if $X=0$ or $X=1$, 0-1 BFS could be used, but Dijkstra handles all cases uniformly.
- Integer overflow: The answer can exceed $2^{31}-1$, so use 64-bit integers for distances. Python handles this automatically.

## worker: <none>
The problem is modeled as a shortest path problem on a state graph with $2N$ nodes. Each node $(v, o)$ represents being at vertex $v$ with graph orientation $o$ (0 for original, 1 for reversed). 

Transitions:
1. **Move in original orientation**: From $(u, 0)$ to $(v, 0)$ if there's an edge $u \to v$ in the original graph, cost 1.
2. **Move in reversed orientation**: From $(u, 1)$ to $(v, 1)$ if there's an edge $u \to v$ in the reversed graph, which means there's an edge $v \to u$ in the original graph, cost 1.
3. **Reverse operation**: From $(u, 0)$ to $(u, 1)$ with cost $X$, and from $(u, 1)$ to $(u, 0)$ with cost $X$.

Dijkstra's algorithm is used since all edge weights are non-negative. The complexity is $O((N + M) \log N)$ which fits within the constraints for $N, M \leq 2 \times 10^5$.

The answer is the minimum distance to reach vertex $N$ in either orientation.
