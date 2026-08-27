
## ideation
The problem can be modeled as a system of linear equations over GF(2) for each bit position, but since the constraints are given as XOR differences on a graph, we can solve it using graph connectivity and component-wise analysis.

1.  **Graph Construction**: Create an undirected graph with $N$ nodes. For each constraint $(X_i, Y_i, Z_i)$, add an edge between $X_i$ and $Y_i$ with weight $Z_i$. This represents $A_{X_i} \oplus A_{Y_i} = Z_i$.

2.  **Connected Components**: Decompose the graph into connected components. The constraints within a connected component are interdependent. Nodes in different components are independent.

3.  **Consistency Check**: For each connected component:
    *   Pick an arbitrary root node (e.g., the first node encountered in BFS/DFS).
    *   Assign the root a relative value of 0.
    *   Traverse the component (BFS/DFS). For each edge $(u, v)$ with weight $w$, if $v$ is visited, check if $A_u \oplus A_v = w$. If not, the system is inconsistent, and we output -1. If $v$ is not visited, set $A_v = A_u \oplus w$.
    *   Note: The values $A_i$ computed here are relative to the root's value. Let $R$ be the actual value of the root. Then the actual value of any node $i$ is $A_i \oplus R$.

4.  **Minimization per Bit**:
    *   The total sum $\sum A_i$ is minimized by minimizing each bit position independently because there are no carries between bit positions in XOR operations when considering the sum of integers? Wait, no. The sum of integers is $\sum_i A_i$. The $k$-th bit of $A_i$ contributes $2^k$ to the sum if it is 1.
    *   Let $b_{i,k}$ be the $k$-th bit of $A_i$. If we fix the $k$-th bit of the root to be $r_k \in \{0, 1\}$, then the $k$-th bit of any node $i$ is determined: $b_{i,k} = \text{relative\_bit}_{i,k} \oplus r_k$.
    *   For a fixed bit position $k$ and a fixed component, let $C_0$ be the count of nodes in the component where $\text{relative\_bit}_{i,k} = 0$, and $C_1$ be the count where $\text{relative\_bit}_{i,k} = 1$.
    *   If we choose $r_k = 0$, the number of 1s at bit $k$ in this component is $C_1$. The contribution to the sum is $C_1 \cdot 2^k$.
    *   If we choose $r_k = 1$, the number of 1s at bit $k$ in this component is $C_0$. The contribution to the sum is $C_0 \cdot 2^k$.
    *   We choose $r_k$ to minimize this contribution: if $C_1 < C_0$, choose $r_k=0$; else choose $r_k=1$. (If equal, either is fine).
    *   This choice is independent for each bit position $k$ and each connected component.

5.  **Reconstruction**:
    *   After determining the optimal root bit $r_{c,k}$ for each component $c$ and bit $k$, we can compute the final value for each node.
    *   For each node $i$ in component $c$, $A_i = \bigoplus_{k} ( (\text{relative\_bit}_{i,k} \oplus r_{c,k}) \ll k )$.
    *   Alternatively, we can just compute the final integer value for each node by combining the bits.

6.  **Edge Cases**:
    *   $M=0$: All $A_i=0$ is the minimal sum.
    *   Disconnected nodes: Handled by the component logic.
    *   Self-loops: $X_i = Y_i$ implies $0 = Z_i$. If $Z_i \neq 0$, it's inconsistent.

7.  **Implementation Details**:
    *   Use adjacency list for the graph.
    *   Use BFS or DFS to traverse components.
    *   Store `relative_val[i]` for each node.
    *   Check consistency during traversal.
    *   For each component, for each bit $0 \dots 30$, count nodes with relative bit 0 and 1.
    *   Determine optimal root bit for each component/bit.
    *   Construct the result array.

## worker: (None)
The problem is modeled as a system of XOR equations on a graph. Each constraint $A_{X_i} \oplus A_{Y_i} = Z_i$ is an edge between $X_i$ and $Y_i$ with weight $Z_i$.

1.  **Graph Decomposition**: The graph is decomposed into connected components. Constraints within a component are linked, while components are independent.
2.  **Relative Values**: For each component, we pick a root and assign it a relative value of 0. We then traverse the component (using DFS/BFS) to assign relative values to all other nodes such that $A_u \oplus A_v = Z_{uv}$ holds for all edges. If a conflict is found (i.e., a cycle where the XOR sum of weights is not 0), the system is inconsistent, and we output -1.
3.  **Minimization**: The actual value of any node $i$ in a component is $A_i = \text{relative\_val}[i] \oplus R$, where $R$ is the actual value of the root. To minimize $\sum A_i$, we minimize each bit position independently. For each bit $k$ and each component, we count how many nodes have the $k$-th bit set in their relative value. Let $C_0$ be the count of nodes with bit 0 and $C_1$ be the count with bit 1.
    *   If we choose the root's $k$-th bit to be 0, the number of nodes with $k$-th bit 1 is $C_1$.
    *   If we choose the root's $k$-th bit to be 1, the number of nodes with $k$-th bit 1 is $C_0$.
    *   We choose the root bit that results in fewer 1s (i.e., $\min(C_0, C_1)$).
4.  **Reconstruction**: After determining the optimal root bits for all components and all bit positions, we compute the final value for each node by combining the bits.

The time complexity is $O(N + M + N \cdot B)$ where $B$ is the number of bits (31), which is efficient enough for $N, M \le 2 \cdot 10^5$.
