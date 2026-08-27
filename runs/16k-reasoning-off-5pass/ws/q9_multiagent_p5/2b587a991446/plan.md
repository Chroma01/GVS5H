The problem asks for the minimum moves to swap two pieces on a graph without them occupying the same vertex simultaneously. Since the graph is connected and undirected, we can model this as a shortest path problem on a state space where a state is defined by the positions of both pieces $(u, v)$. However, constructing the full state space is too large ($O(N^2)$). Instead, we observe that the pieces effectively block each other. If the shortest path between $S$ and $T$ is unique and simple, we can just move them along it. If there are multiple paths or cycles, one piece might need to "wait" or "detour" to let the other pass. We can solve this by running BFS on the state space but optimizing: since we only care about the relative order and blocking, we can consider the distance from $S$ to $T$ and $T$ to $S$. Actually, a simpler approach is to realize that the pieces just need to traverse the path between $S$ and $T$. If they can pass each other (which requires a cycle or a vertex of degree $\ge 3$ allowing a detour), the cost is roughly $dist(S, T) + dist(T, S)$. If they cannot pass, we check if a valid sequence exists. The standard solution for this specific "swap without collision" on a general graph involves checking if there is a path for A to go $S \to T$ while B goes $T \to S$ without colliding. This is equivalent to finding if there exists a vertex $X$ such that A goes $S \to X \to T$ and B goes $T \to X \to S$ (or similar detours). Actually, the most robust method is to run a BFS on the state $(u, v)$ but prune states where $u=v$. Given constraints $N, M \le 2 \cdot 10^5$, $O(N^2)$ is too slow. However, notice that we only ever care about the path between $S$ and $T$. If the shortest path is unique, they can't pass. If there are multiple shortest paths or a cycle, they might pass.
Correct approach: The minimum moves is the length of the shortest path in the state graph. Since we can't build the whole graph, we observe that the pieces will always move towards their targets unless blocked. The only time they get stuck is if they are adjacent and want to cross. This happens if the graph is a simple path (or tree) between $S$ and $T$ with no alternative routes. In that case, if $S$ and $T$ are endpoints of a simple path, they can never swap (Output -1). If there is a cycle, they can swap. The cost is $dist(S, T) + dist(T, S)$ if they can pass directly? No, if they pass, one must wait.
Actually, the standard solution is: Calculate $d[u]$ = distance from $S$ to $u$, and $d'[u]$ = distance from $T$ to $u$.
The answer is $\min_{v} (d[v] + d'[v] + 2 \times \text{something})$?
Let's re-evaluate. We want to go from $(S, T)$ to $(T, S)$.
If the graph is a simple path $S - ... - T$, impossible.
If there is a cycle, possible.
The minimum operations is simply the shortest path in the implicit state graph.
Since $N$ is large, we cannot do full BFS. But notice that the pieces will never move away from their targets unnecessarily. They will move along shortest paths.
The state is $(u, v)$. Transitions: $(u, v) \to (u', v)$ if $u' \sim u, u' \neq v$, and $(u, v) \to (u, v')$ if $v' \sim v, v' \neq u$.
This is a shortest path on a graph with $N^2$ nodes.
However, we can optimize. The optimal strategy involves moving both pieces along shortest paths to some meeting point or swapping point.
Actually, there is a known result for this: The answer is $dist(S, T) + dist(T, S)$ if they can pass? No.
Let's look at the sample 1: S=3, T=4. Edges: (2,4), (1,4), (3,4), (2,3).
Path 3-4 is direct (len 1). Path 3-2-4 is len 2.
A at 3, B at 4. Goal A at 4, B at 3.
Move A: 3->2. State (2, 4).
Move B: 4->3. State (2, 3).
Move A: 2->4. State (4, 3). Total 3 moves.
Note $dist(3,4)=1, dist(4,3)=1$. Sum = 2. But answer is 3.
Why? Because they collide if they try to swap directly on the edge (3,4).
One must take a detour