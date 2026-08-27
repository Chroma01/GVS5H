
## ideation
The core difficulty is modeling the state space correctly to account for the edge reversal operation. The key insight is that the graph's orientation changes globally, so we need to track whether we are in the "original" orientation or the "reversed" orientation. This leads to a state graph with $2N$ nodes: $(u, 0)$ for being at vertex $u$ in the original orientation, and $(u, 1)$ for being at vertex $u$ in the reversed orientation.

Transitions:
1. From $(u, 0)$, we can move to any neighbor $v$ such that there is an edge $u \to v$ in the original graph. Cost: 1.
2. From $(u, 0)$, we can reverse all edges to enter state $(u, 1)$. Cost: $X$.
3. From $(u, 1)$, we can move to any neighbor $v$ such that there is an edge $v \to u$ in the original graph (which becomes $u \to v$ in the reversed graph). Cost: 1.
4. From $(u, 1)$, we can reverse all edges to enter state $(u, 0)$. Cost: $X$.

We can use Dijkstra's algorithm on this state graph. The number of states is $2N$ and the number of edges is roughly $2M + 2N$, so the complexity will be $O((N+M) \log N)$, which fits within the constraints.

Pitfalls:
- The cost $X$ can be large, so we must use 64-bit integers for distances.
- We need to build both the original adjacency list and the reversed adjacency list efficiently.
- The target is to reach vertex $N$ in either orientation, so the answer is $\min(\text{dist}[(N, 0)], \text{dist}[(N, 1)])$.

## worker: (None)
The problem is modeled as a shortest path problem on a state graph with $2N$ nodes, where each node represents `(vertex, orientation)`. Orientation 0 means we're using the original edge directions, and orientation 1 means we're using the reversed edge directions.

Transitions:
1. From `(u, 0)`, moving along an original edge `u→v` costs 1, leading to `(v, 0)`.
2. From `(u, 0)`, reversing all edges costs X, leading to `(u, 1)`.
3. From `(u, 1)`, moving along a reversed edge (which corresponds to an original edge `v→u`) costs 1, leading to `(v, 1)`.
4. From `(u, 1)`, reversing all edges costs X, leading to `(u, 0)`.

Dijkstra's algorithm is used since edge weights are positive (1 or X). The number of states is $2N$ and the number of transitions is $O(M + N)$, giving a time complexity of $O((N + M) \log N)$, which fits within the constraints.

The answer is the minimum distance to reach vertex N in either orientation.
