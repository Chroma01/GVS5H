
## ideation
**Core Difficulty**: The problem involves a state space that includes both the current vertex and the orientation of the graph (original vs. reversed). A naive BFS/Dijkstra on $2N$ nodes is feasible given $N, M \le 2 \times 10^5$. The main challenge is correctly modeling the transitions:
1. Moving along an edge $(u, v)$ in the original graph:
   - If orientation is Original: Can move $u \to v$ (cost 1).
   - If orientation is Reversed: The edge becomes $v \to u$, so can move $v \to u$ (cost 1).
2. Reversing edges:
   - From Original state at $u$, switch to Reversed state at $u$ (cost $X$).
   - From Reversed state at $u$, switch to Original state at $u$ (cost $X$).

**Candidate Approaches**:
1. **Dijkstra's Algorithm on State Graph**:
   - Nodes: $(u, 0)$ for original orientation, $(u, 1)$ for reversed orientation.
   - Edges:
     - For each original edge $u \to v$:
       - $(u, 0) \to (v, 0)$ with weight 1.
       - $(v, 1) \to (u, 1)$ with weight 1 (since in reversed state, the edge is $v \to u$).
     - For every vertex $u$:
       - $(u, 0) \to (u, 1)$ with weight $X$.
       - $(u, 1) \to (u, 0)$ with weight $X$.
   - Start: $(1, 0)$ with distance 0.
   - Target: $\min(dist(N, 0), dist(N, 1))$.
   - Complexity: $O((N+M) \log N)$, which fits within time limits.

2. **BFS with 0-1 weights?** No, weights are 1 and $X$. If $X$ is large, Dijkstra is necessary. If $X$ is small, maybe BFS layers, but $X$ can be up to $10^9$, so Dijkstra is the robust choice.

## worker: Implement the Dijkstra's algorithm solution in Pyt
The problem is modeled as a shortest path problem on a graph with $2N$ states. Each state is represented by $(u, \text{orientation})$, where $u$ is the current vertex and $\text{orientation}$ is a boolean (0 for original, 1 for reversed).
- **Transitions**:
  1. **Move**: 
     - If orientation is 0 (original), from $u$ we can move to $v$ if there is an edge $u \to v$ in the input graph. Cost: 1.
     - If orientation is 1 (reversed), the edge $u \to v$ in input becomes $v \to u$. So from $u$, we can move to $v$ if there was an edge $v \to u$ in the input graph. Cost: 1.
  2. **Reverse**:
     - From any state $(u, \text{orientation})$, we can switch to $(u, 1-\text{orientation})$ with cost $X$.

We use Dijkstra's algorithm starting from $(1, 0)$ with distance 0. The answer is $\min(\text{dist}[N][0], \text{dist}[N][1])$.
Complexity: $O((N+M) \log N)$, which fits within the constraints ($N, M \le 2 \times 10^5$).

## worker: Run the code against sample inputs to verify corre
The solution models the problem as a shortest path problem on a graph with $2N$ states. Each state is defined by the current vertex $u$ and the orientation of the graph (0 for original, 1 for reversed).
- **States**: $(u, 0)$ and $(u, 1)$ for $u \in \{1, \dots, N\}$.
- **Transitions**:
  1. **Move**: 
     - From $(u, 0)$, move to $(v, 0)$ if there is an edge $u \to v$ in the input graph. Cost: 1.
     - From $(u, 1)$, move to $(v, 1)$ if there is an edge $v \to u$ in the input graph (since edges are reversed, $v \to u$ becomes $u \to v$). Cost: 1.
  2. **Reverse**:
     - From $(u, 0)$, switch to $(u, 1)$ with cost $X$.
     - From $(u, 1)$, switch to $(u, 0)$ with cost $X$.
- **Algorithm**: Dijkstra's algorithm is used because edge weights are non-negative (1 and $X$). The priority queue stores tuples `(cost, u, orientation)`.
- **Complexity**: $O((N + M) \log N)$, which fits within the time limits for $N, M \le 2 \times 10^5$.
- **Edge Cases**: The code handles disconnected components implicitly (dist remains infinity), large $X$ (handled by `float('inf')` and integer arithmetic), and the guarantee that $N$ is reachable.

## worker: Run the provided code against Sample 1, Sample 2, 
The provided code implements Dijkstra's algorithm on a state graph with $2N$ nodes. Each node represents a vertex $u$ in either the original orientation (state 0) or the reversed orientation (state 1).
- **Transitions**:
  1. **Move**: If in state 0 at $u$, traverse original edges $u \to v$ (cost 1). If in state 1 at $u$, traverse reversed edges (which correspond to original edges $v \to u$), so we look up `rev_adj[u]` (cost 1).
  2. **Reverse**: Switch between state 0 and state 1 at the same vertex $u$ with cost $X$.
- **Complexity**: $O((N+M) \log N)$ due to the priority queue operations. Given $N, M \le 2 \times 10^5$, this fits well within typical time limits (usually 2 seconds).
- **Data Types**: The answer can exceed $2^{31}-1$ (as seen in Sample 3), so Python's arbitrary precision integers handle this automatically. `float('inf')` is used for initialization, which is safe for comparison with large integers.
- **Correctness**: The logic correctly models the problem constraints and operations. The guarantee that $N$ is reachable ensures `ans` will not be infinity.

## worker: Run the code against Sample 1, Sample 2, Sample 3,
The provided code implements Dijkstra's algorithm on a state graph with $2N$ nodes. Each node represents a vertex $u$ in either the original orientation (state 0) or the reversed orientation (state 1).
- **Transitions**:
  1. **Move**: If in state 0 at $u$, traverse original edges $u \to v$ (cost 1). If in state 1 at $u$, traverse reversed edges (which correspond to original edges $v \to u$), so we look up `rev_adj[u]` (cost 1).
  2. **Reverse**: Switch between state 0 and state 1 at the same vertex $u$ with cost $X$.
- **Complexity**: $O((N+M) \log N)$ due to the priority queue operations. Given $N, M \le 2 \times 10^5$, this fits well within typical time limits.
- **Data Types**: The answer can exceed $2^{31}-1$ (as seen in Sample 3), so Python's arbitrary precision integers handle this automatically. `float('inf')` is used for initialization, which is safe for comparison with large integers.
- **Correctness**: The logic correctly models the problem constraints and operations. The guarantee that $N$ is reachable ensures `ans` will not be infinity.

## worker: finalize
The solution models the problem as a shortest path problem on a graph with $2N$ states. Each state is defined by the current vertex $u$ and the orientation of the graph (0 for original, 1 for reversed).
- **Transitions**:
  1. **Move**: 
     - If in state 0 at $u$, traverse original edges $u \to v$ (cost 1).
     - If in state 1 at $u$, traverse reversed edges. Since reversing the graph turns an original edge $v \to u$ into $u \to v$, we can move from $u$ to $v$ if there was an original edge $v \to u$. This is handled by `rev_adj[u]`.
  2. **Reverse**:
     - Switch between state 0 and state 1 at the same vertex $u$ with cost $X$.
- **Algorithm**: Dijkstra's algorithm is used because edge weights are non-negative (1 and $X$). The priority queue stores tuples `(cost, u, orientation)`.
- **Complexity**: $O((N + M) \log N)$, which fits within the time limits for $N, M \le 2 \times 10^5$.
- **Data Types**: The answer can exceed $2^{31}-1$ (as seen in Sample 3), so Python's arbitrary precision integers handle this automatically. `float('inf')` is used for initialization, which is safe for comparison with large integers.
