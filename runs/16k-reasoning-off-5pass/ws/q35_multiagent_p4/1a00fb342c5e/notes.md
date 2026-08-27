
## ideation
The problem asks us to find a sequence $A$ satisfying XOR constraints $A_{X_i} \oplus A_{Y_i} = Z_i$ such that the sum of elements is minimized. If no such sequence exists, output -1.

1.  **Graph Representation**: The constraints form a system of equations over a graph with $N$ nodes and $M$ edges. Each edge $(X_i, Y_i)$ with weight $Z_i$ implies $A_{X_i} \oplus A_{Y_i} = Z_i$.
2.  **Connected Components**: The variables in different connected components are independent. We can solve for each component separately.
3.  **Relative Values**: For each connected component, pick a root node and assign it a temporary value (e.g., 0). Using BFS or DFS, we can determine the relative value $V_u$ for every node $u$ in the component such that $A_u = V_u \oplus C$, where $C$ is an unknown constant specific to that component.
4.  **Consistency Check**: During traversal, if we encounter an already visited node, we check if the current path's implied XOR difference matches the edge weight. If $V_u \oplus V_v \neq Z_i$ for an edge $(u, v)$ with weight $Z_i$, then the system is inconsistent, and we output -1.
5.  **Minimizing Sum**: For a component, the actual values are $A_u = V_u \oplus C$. We want to minimize $\sum_{u \in \text{component}} (V_u \oplus C)$. Since XOR operates independently on each bit, we can determine the optimal bits of $C$ independently. For each bit position $k$ (from 0 to ~29):
    *   Count how many $V_u$ in the component have the $k$-th bit set. Let this count be `cnt`.
    *   Let `size` be the number of nodes in the component.
    *   If we set the $k$-th bit of $C$ to 0, the contribution to the sum from this bit is `cnt * 2^k`.
    *   If we set the $k$-th bit of $C$ to 1, the contribution is `(size - cnt) * 2^k`.
    *   We choose the bit for $C$ that results in the smaller contribution. Specifically, if `cnt > size - cnt` (i.e., `cnt > size / 2`), we set the bit to 1; otherwise, 0.
6.  **Construction**: After determining the optimal $C$ for each component, compute $A_u = V_u \oplus C$ for all nodes and print the result.

## worker: (none)
The solution models the problem as a system of XOR equations on a graph. Each constraint $A_{X_i} \oplus A_{Y_i} = Z_i$ is an edge between nodes $X_i$ and $Y_i$ with weight $Z_i$.

1.  **Graph Traversal & Consistency Check**: We iterate through all nodes. For each unvisited node, we start a BFS/DFS to explore its connected component. We assign a relative value $V_u$ to each node $u$ such that $A_u = V_u \oplus C$, where $C$ is a constant for the entire component. During traversal, if we encounter an already visited node, we verify that the existing relative values are consistent with the edge weight. If $V_u \oplus V_v \neq Z_i$ for an edge $(u, v)$ with weight $Z_i$, the system is inconsistent, and we output `-1`.

2.  **Minimizing Sum per Component**: For each connected component, the values are determined up to a global XOR constant $C$. The actual value of node $u$ is $A_u = V_u \oplus C$. We want to minimize $\sum_{u \in \text{component}} A_u = \sum_{u \in \text{component}} (V_u \oplus C)$. Since XOR operates independently on each bit, we can optimize each bit of $C$ separately. For a specific bit position $k$:
    *   Let `cnt` be the number of nodes in the component where the $k$-th bit of $V_u$ is 1.
    *   If we choose the $k$-th bit of $C$ to be 0, the $k$-th bit of $A_u$ will be 1 for `cnt` nodes.
    *   If we choose the $k$-th bit of $C$ to be 1, the $k$-th bit of $A_u$ will be 1 for `size - cnt` nodes (where `size` is the number of nodes in the component).
    *   To minimize the sum, we choose the bit for $C$ that results in fewer 1s. Specifically, if `cnt > size - cnt`, we set the $k$-th bit of $C$ to 1; otherwise, 0.

3.  **Complexity**: The graph traversal takes $O(N + M)$ time. For each component, we iterate through its nodes to count bits. The total number of nodes across all components is $N$, and we check 30 bits for each node, so this step takes $O(30N)$. The overall time complexity is $O(N + M)$, which fits within the constraints ($N, M \le 2 \times 10^5$).
