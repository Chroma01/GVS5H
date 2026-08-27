
## ideation
**Core Difficulty**: The problem involves counting valid assignments under a set of inequality constraints $x_i \le x_{A_i}$. The structure of these constraints forms a functional graph (each node has exactly one outgoing edge). The key insight is recognizing that the graph decomposes into components, each containing exactly one cycle with trees rooted on the cycle nodes directing towards the cycle.

**Logical Deduction**:
1.  **Cycle Property**: In any cycle $c_1 \to c_2 \to \dots \to c_k \to c_1$, the constraints imply $x_{c_1} \le x_{c_2} \le \dots \le x_{c_k} \le x_{c_1}$. This forces all nodes in a cycle to have the same value, say $v$.
2.  **Tree Property**: For any node $u$ not in a cycle, it eventually leads to a cycle. The constraints propagate backwards: $x_u \le x_{parent(u)} \le \dots \le x_{cycle} = v$. Thus, if the cycle value is fixed to $v$, any node in the tree leading to that cycle can take any integer value from $1$ to $v$.
3.  **Component Calculation**: For a component with total size $S$ and cycle length $L$:
    *   The $L$ cycle nodes are fixed to value $v$.
    *   The remaining $S-L$ nodes can be any value in $[1, v]$.
    *   Number of ways for a fixed $v$ is $v^{S-L}$.
    *   Total ways for this component is $\sum_{v=1}^M v^{S-L}$.
4.  **Final Answer**: Since choices for different components are independent, the total answer is the product of the sums calculated for each component, modulo 998244353.

**Candidate Approaches**:
1.  **Graph Decomposition**: Use DFS or Union-Find to identify components, detect cycles, and calculate $(S-L)$ for each.
2.  **Power Summation**: Precompute powers or use modular exponentiation to calculate $\sum_{v=1}^M v^k$ efficiently. Since $M, N \le 2025$, an $O(M)$ loop per component is acceptable ($O(N \cdot M)$ total).
3.  **Implementation**: Read input, build adjacency list (or just follow pointers since out-degree is 1), traverse to find cycles and component sizes.

## worker: Implement the graph traversal to identify componen
1.  **Graph Structure**: The problem defines a functional graph where each node $i$ has exactly one outgoing edge to $A_i$. Such a graph decomposes into several connected components, each containing exactly one cycle with trees rooted on the cycle nodes (edges directed towards the cycle).
2.  **Constraints Analysis**:
    *   For a cycle $c_1 \to c_2 \to \dots \to c_k \to c_1$, the constraints $x_{c_i} \le x_{c_{i+1}}$ imply $x_{c_1} = x_{c_2} = \dots = x_{c_k} = v$.
    *   For any node $u$ in the tree leading to the cycle, $x_u \le x_{parent(u)} \le \dots \le v$. Thus, $x_u$ can be any integer in $[1, v]$.
    *   If a component has size $S$ and cycle length $L$, and the cycle value is $v$, there are $v^{S-L}$ ways to assign values to the tree nodes (since the $L$ cycle nodes are fixed to $v$).
    *   The total ways for a component is $\sum_{v=1}^M v^{S-L}$.
3.  **Algorithm**:
    *   **Cycle Detection**: Use Kahn's algorithm (topological sort) on the reverse graph logic or simply by in-degrees to identify nodes that are part of cycles. Nodes with in-degree > 0 after removing all nodes with in-degree 0 iteratively are part of cycles.
    *   **Component Size**: For each identified cycle, perform a BFS on the *reverse* graph (edges $u \to v$ become $v \to u$) starting from the cycle nodes to count all nodes that eventually flow into the cycle. This gives the total component size $S$.
    *   **Calculation**: For each component, compute $k = S - L$. Calculate $\sum_{v=1}^M v^k \pmod{998244353}$. Multiply these sums for all components to get the final answer.
4.  **Complexity**:
    *   Building reverse graph: $O(N)$.
    *   Topological sort: $O(N)$.
    *   Identifying cycles and BFS: $O(N)$.
    *   Summation: $O(N \cdot M)$ in worst case (if many components), but since $\sum (S-L) = N - \sum L$, and we sum over components, the total complexity is roughly $O(N \cdot M)$ which is acceptable for $N, M \le 2025$.
5.  **Edge Cases**:
    *   $k=0$ (pure cycle): The sum is $M$.
    *   $M=1$: The sum is 1 (if $k \ge 0$).
    *   Disconnected components.
