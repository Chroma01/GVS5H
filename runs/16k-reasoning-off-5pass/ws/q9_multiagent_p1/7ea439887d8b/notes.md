
## ideation
**Core Difficulty**: The problem involves a state-dependent graph where the global structure changes based on an operation (reversing all edges). A naive simulation or BFS might fail if the number of reversals isn't strictly limited to 1, but the problem constraints and nature of "global reversal" suggest that reversing twice is equivalent to doing nothing (cost $2X$ vs 0), so optimal paths likely involve at most one reversal. However, we must rigorously prove or ensure the shortest path algorithm handles the state transitions correctly without assuming a fixed number of reversals upfront, although Dijkstra on a state graph naturally handles this.

**Candidate Approaches**:
1.  **State-Space Dijkstra**:
    *   Create a graph with $2N$ nodes: $(u, 0)$ representing being at vertex $u$ with edges in original direction, and $(u, 1)$ representing being at vertex $u$ with edges reversed.
    *   Edges from $(u, 0)$:
        *   To $(v, 0)$ for every original edge $u \to v$ with weight 1.
        *   To $(u, 1)$ with weight $X$ (cost to reverse).
    *   Edges from $(u, 1)$:
        *   To $(v, 1)$ for every reversed edge $u \to v$ (which corresponds to original $v \to u$) with weight 1.
        *   To $(u, 0)$ with weight $X$ (cost to reverse back).
    *   Run Dijkstra starting from $(1, 0)$ with distance 0.
    *   The answer is $\min(dist[N, 0], dist[N, 1])$.
    *   *Complexity*: $O(M \log N)$ or $O(M + N \log N)$, which fits within $2 \times 10^5$.

2.  **Bidirectional Search / BFS with Heuristic**: Not necessary given the weights are positive and Dijkstra is efficient enough.

3.  **Graph Construction Pitfalls**:
    *   Ensure the adjacency list for state 1 correctly maps to the reverse of the original edges.
    *   Handle large values of $X$ and the potential answer exceeding 32-bit integers (use 64-bit integers).
    *   Ensure the initial state is $(1, 0)$ and we don't start with a reversed graph unless specified (we start at 1 with original edges).

## worker: Implement the solution in Python using Dijkstra's 
- **Algorithm**: The solution uses Dijkstra's algorithm on a state graph with $2N$ nodes. Each node is represented as $(u, \text{orientation})$, where $u$ is the vertex index and $\text{orientation}$ is either 0 (original edge directions) or 1 (reversed edge directions).
- **Transitions**:
  - From $(u, 0)$, we can move to $(v, 0)$ for each original edge $u \to v$ with cost 1.
  - From $(u, 0)$, we can switch to $(u, 1)$ with cost $X$.
  - From $(u, 1)$, we can move to $(v, 1)$ for each reversed edge $u \to v$ (which corresponds to original $v \to u$) with cost 1.
  - From $(u, 1)$, we can switch to $(u, 0)$ with cost $X$.
- **Complexity**: The number of vertices in the state graph is $2N$ and edges are roughly $2M$ (movement) + $2N$ (reversals). Dijkstra's complexity is $O(E' \log V')$, which is $O((M+N) \log N)$. Given constraints $N, M \le 2 \times 10^5$, this fits well within time limits.
- **Edge Cases**: 
  - Large $X$ values are handled naturally by the algorithm.
  - The answer can exceed 32-bit integer range, so Python's arbitrary precision integers handle this automatically.
  - Disconnected components are handled by Dijkstra naturally (unreachable states remain at infinity).
- **Input Parsing**: Uses `sys.stdin.read().split()` for efficient bulk reading of inputs.

## worker: Run the code against the provided sample inputs to
The provided code implements Dijkstra's algorithm on a state graph where each vertex $u$ has two states: $(u, 0)$ representing the original graph orientation and $(u, 1)$ representing the reversed graph orientation.
- Transitions from $(u, 0)$ allow moving to neighbors in the original graph (cost 1) or switching to state $(u, 1)$ (cost $X$).
- Transitions from $(u, 1)$ allow moving to neighbors in the reversed graph (cost 1) or switching back to state $(u, 0)$ (cost $X$).
- The adjacency list `rev_adj` is precomputed such that `rev_adj[v]` contains `u` if there is an edge $u \to v$ in the original graph, effectively modeling the reversed graph where an edge $v \to u$ exists if $u \to v$ existed originally.
- The algorithm correctly handles the constraints and edge cases, including large values for $X$ and the potential for the answer to exceed 32-bit integers (Python handles large integers automatically).
- The logic covers the scenario where one might reverse edges multiple times, though optimally one would reverse at most once (since reversing twice costs $2X$ and returns to the original state, which is suboptimal compared to not reversing if $X > 0$). The Dijkstra approach naturally finds the shortest path regardless of the number of reversals.

## worker: Run the code against Sample 1, 2, 3, and 4 to veri
The provided code implements Dijkstra's algorithm on a state graph with $2N$ nodes. Each node is represented as $(u, \text{orientation})$, where $u$ is the vertex index and $\text{orientation}$ is either 0 (original edge directions) or 1 (reversed edge directions).
- Transitions from $(u, 0)$ allow moving to neighbors in the original graph (cost 1) or switching to state $(u, 1)$ (cost $X$).
- Transitions from $(u, 1)$ allow moving to neighbors in the reversed graph (cost 1) or switching back to state $(u, 0)$ (cost $X$).
- The adjacency list `rev_adj` is precomputed such that `rev_adj[v]` contains `u` if there is an edge $u \to v$ in the original graph, effectively modeling the reversed graph where an edge $v \to u$ exists if $u \to v$ existed originally.
- The algorithm correctly handles the constraints and edge cases, including large values for $X$ and the potential for the answer to exceed 32-bit integers (Python handles large integers automatically).
- The logic covers the scenario where one might reverse edges multiple times, though optimally one would reverse at most once (since reversing twice costs $2X$ and returns to the original state, which is suboptimal compared to not reversing if $X > 0$). The Dijkstra approach naturally finds the shortest path regardless of the number of reversals.

## worker: finalize
The solution implements Dijkstra's algorithm on a state graph where each vertex $u$ has two states: $(u, 0)$ representing the original graph orientation and $(u, 1)$ representing the reversed graph orientation.
- **Transitions**:
  - From $(u, 0)$, we can move to neighbors in the original graph (cost 1) or switch to state $(u, 1)$ (cost $X$).
  - From $(u, 1)$, we can move to neighbors in the reversed graph (cost 1) or switch back to state $(u, 0)$ (cost $X$).
- **Graph Construction**: The `rev_adj` list is precomputed such that `rev_adj[v]` contains `u` if there is an edge $u \to v$ in the original graph. This effectively models the reversed graph where an edge $v \to u$ exists if $u \to v$ existed originally.
- **Complexity**: The number of vertices in the state graph is $2N$ and edges are roughly $2M$ (movement) + $2N$ (reversals). Dijkstra's complexity is $O(E' \log V')$, which is $O((M+N) \log N)$. Given constraints $N, M \le 2 \times 10^5$, this fits well within time limits.
- **Edge Cases**: Large $X$ values and answers exceeding 32-bit integers are handled naturally by Python's arbitrary precision integers and the algorithm's logic.
