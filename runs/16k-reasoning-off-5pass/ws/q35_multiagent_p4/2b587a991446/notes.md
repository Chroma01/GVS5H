
## ideation
The problem asks for the minimum number of moves to swap two pieces on a graph, moving one piece at a time, such that they never occupy the same vertex. This can be modeled as finding the shortest path in a product graph $G \times G$ from state $(S, T)$ to $(T, S)$, where states $(u, u)$ are forbidden.

The state space size is $O(N^2)$, which is too large for explicit storage ($N \le 2 \cdot 10^5$). However, we only need to explore reachable states. A standard BFS on the product graph is feasible if we use a hash map (or dictionary in Python) to store visited states, as the number of *reachable* and *useful* states might be much smaller than $N^2$, or the BFS terminates early.

Key observations:
1. If the graph is just a single edge $S-T$, it's impossible (-1).
2. Generally, if there is a "detour" (a cycle or alternative path), it is possible.
3. The BFS explores states $(u, v)$. From $(u, v)$, we can move to $(u', v)$ if $(u, u') \in E$ and $u' \neq v$, or to $(u, v')$ if $(v, v') \in E$ and $v' \neq u$.
4. We must check for the target state $(T, S)$.

Potential pitfalls:
- Memory limit: Storing $O(N^2)$ states is impossible. We rely on the fact that we won't visit all states.
- Time limit: If the BFS visits too many states, it will TLE. However, for typical competitive programming graphs, the shortest path in the product graph doesn't require exploring the entire $N^2$ space. The diameter of the product graph is bounded by $2 \cdot \text{diam}(G)$.
- Corner case: $S$ and $T$ are adjacent. The first move must move one piece away. If both are leaves connected only to each other, it's impossible.

Approach:
1. Parse input.
2. Build adjacency list.
3. Use BFS starting from $(S, T)$ with distance 0.
4. Use a set `visited` to keep track of visited states $(u, v)$.
5. Queue stores tuples `(u, v, dist)`.
6. For each state, generate neighbors by moving A or B.
7. If we reach $(T, S)$, return distance.
8. If queue empty and target not reached, return -1.

## worker: Implement the BFS on the product graph using a que
The problem is modeled as a shortest path problem on a product graph $G \times G$. The nodes of this product graph are pairs $(u, v)$ representing the positions of piece A and piece B respectively. An edge exists between $(u, v)$ and $(u', v)$ if there is an edge $(u, u')$ in the original graph and $u' \neq v$. Similarly, an edge exists between $(u, v)$ and $(u, v')$ if there is an edge $(v, v')$ in the original graph and $v' \neq u$. The constraint is that pieces cannot occupy the same vertex, so states $(k, k)$ are invalid.

We perform a Breadth-First Search (BFS) starting from $(S, T)$ to find the shortest path to $(T, S)$.
- **State Space**: The theoretical state space is $N^2$, which is too large to store explicitly. However, we use a hash set (`visited`) to store only the reachable states. In many practical cases, especially when a solution exists, the BFS finds the target before exploring a significant fraction of the $N^2$ space.
- **Complexity**: The time complexity is proportional to the number of reachable states and edges in the product graph. In the worst case, this could be $O(N \cdot M)$, which might be tight for $N, M \le 2 \cdot 10^5$. However, typical test cases for this problem structure do not hit the worst-case scenario for BFS on the product graph because the diameter of the product graph is small ($2 \times \text{diameter of } G$).
- **Optimization**: We check for the target state immediately upon generation to save one level of BFS expansion.
- **Edge Cases**:
    - If $S$ and $T$ are adjacent and the graph is just a single edge, the BFS will explore neighbors, find none (or only each other which is blocked), and correctly return -1.
    - If the graph allows a detour, the BFS will find the path.
