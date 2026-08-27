
## ideation
The core difficulty is modeling the state space correctly to account for the edge reversal operation. The key insight is that the "orientation" of the graph is global, so the state must include both the current vertex and whether the edges are in their original or reversed state.

1.  **State Definition**: A state is `(u, k)` where `u` is the current vertex (1 to N) and `k` is the orientation (0 for original, 1 for reversed).
2.  **Transitions**:
    *   **Move (Cost 1)**:
        *   If `k=0` (original): From `(u, 0)`, we can move to `(v, 0)` if there is an edge `u -> v` in the original graph.
        *   If `k=1` (reversed): From `(u, 1)`, we can move to `(v, 1)` if there is an edge `v -> u` in the original graph (which becomes `u -> v` in the reversed graph). This is equivalent to traversing incoming edges to `u` in the original graph.
    *   **Reverse (Cost X)**:
        *   From `(u, 0)`, we can go to `(u, 1)` with cost `X`.
        *   From `(u, 1)`, we can go to `(u, 0)` with cost `X`.
3.  **Algorithm**: Since edge weights are positive (1 and X), Dijkstra's algorithm is appropriate. The number of states is `2N` and the number of transitions is roughly `2M + 2N` (each original edge contributes two move transitions, one in each orientation state, plus two reverse transitions per vertex). This fits within the time limits for `N, M <= 2*10^5`.
4.  **Graph Construction**:
    *   We need the original adjacency list `adj` for moving in orientation 0.
    *   We need the reverse adjacency list `rev_adj` for moving in orientation 1 (since moving `u->v` in reversed graph means `v->u` existed originally).
    *   We can run Dijkstra on a virtual graph with `2*N` nodes. Node `i` represents `(i, 0)` and node `i+N` represents `(i, 1)`.
    *   Edges:
        *   For each `u -> v` in original graph:
            *   Add edge `(u, v)` with weight 1 in the "0" layer.
            *   Add edge `(v+N, u+N)` with weight 1 in the "1" layer? No, wait.
            *   Let's be precise.
            *   State `(u, 0)` corresponds to index `u`. State `(u, 1)` corresponds to index `u + N`.
            *   Original edge `u -> v`:
                *   In orientation 0: `u -> v` is valid. So add directed edge from `u` to `v` with weight 1.
                *   In orientation 1: The edge is `v -> u`. So if we are at `v` in orientation 1, we can go to `u`. So add directed edge from `v + N` to `u + N` with weight 1.
            *   Reverse operation:
                *   From `(u, 0)` to `(u, 1)`: Add edge from `u` to `u + N` with weight `X`.
                *   From `(u, 1)` to `(u, 0)`: Add edge from `u + N` to `u` with weight `X`.
5.  **Start and End**:
    *   Start at `(1, 0)`, i.e., node `1`.
    *   End at `(N, 0)` or `(N, 1)`. We take the minimum distance to node `N` or node `N + N`.

Pitfalls:
- Large X: Use 64-bit integers for distances.
- Graph size: Ensure adjacency lists are built efficiently.
- Bidirectional reverse edges: The reverse operation is always available, so the "swap" edges exist for all vertices.

## worker: (None)
The problem is modeled as a shortest path problem on a state graph where each state is `(vertex, orientation)`. The orientation can be 0 (original) or 1 (reversed). 

- **States**: There are `2N` states. State `(u, 0)` is represented by index `u-1`, and state `(u, 1)` is represented by index `u-1 + N`.
- **Transitions**:
  - **Move (cost 1)**: 
    - In orientation 0, from `(u, 0)`, we can move to `(v, 0)` if there's an edge `u -> v` in the original graph.
    - In orientation 1, from `(u, 1)`, we can move to `(v, 1)` if there's an edge `v -> u` in the original graph (which becomes `u -> v` in the reversed graph). This is handled by using the reverse adjacency list.
  - **Reverse (cost X)**:
    - From `(u, 0)` to `(u, 1)` with cost X.
    - From `(u, 1)` to `(u, 0)` with cost X.
- **Algorithm**: Dijkstra's algorithm is used because edge weights are positive. The number of states is `2N` and the number of transitions is `O(M + N)`, leading to a time complexity of `O((N + M) log N)`, which is efficient for the given constraints.
- **Result**: The minimum cost to reach vertex N is the minimum of the distances to states `(N, 0)` and `(N, 1)`.
