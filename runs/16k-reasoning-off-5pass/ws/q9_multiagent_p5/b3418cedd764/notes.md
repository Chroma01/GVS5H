
## ideation
The problem asks for the number of sequences $x$ satisfying $x_i \leq x_{A_i}$ for all $i$.
1.  **Graph Structure**: The condition defines a directed graph where each node $i$ has exactly one outgoing edge to $A_i$. This graph is a collection of components. Each component consists of exactly one cycle with some trees rooted on the cycle nodes, where edges in the trees point towards the cycle (i.e., $child \to parent \to \dots \to cycle$).
2.  **Cycle Constraint**: Traversing a cycle implies $x_{c_1} \leq x_{c_2} \leq \dots \leq x_{c_k} \leq x_{c_1}$, which forces all nodes in a cycle to have the same value. Let this value be $v$.
3.  **Tree Constraint**: For any node $u$ not in the cycle, there is a unique path to the cycle. The condition $x_u \leq x_{A_u}$ implies that values must be non-decreasing as we move from leaves towards the cycle (or non-increasing from the cycle to leaves in the reversed graph).
4.  **Decomposition**: The problem can be decomposed by components. For a fixed value $v$ assigned to the cycle of a component, the number of valid assignments for the rest of the component is the product of the number of valid assignments for each tree attached to the cycle nodes, given that the root of each tree (the cycle node) has value $v$.
5.  **Dynamic Programming**:
    -   Reverse the edges of the graph to get a forest of trees rooted at the cycle nodes (edges $A_i \to i$).
    -   For each node $u$, define $dp[u][val]$ as the number of ways to assign values to the subtree rooted at $u$ (in the reversed graph) such that $x_u = val$ and $x_{child} \leq x_u$ for all children.
    -   Recurrence: $dp[u][val] = \prod_{v \in children(u)} (\sum_{k=1}^{val} dp[v][k])$.
    -   Base case: For leaves, $dp[leaf][val] = 1$ for all $val \geq 1$.
    -   The values for cycle nodes are fixed to $v$. The number of ways for a component given cycle value $v$ is $\prod_{c \in cycle} dp[c][v]$.
6.  **Final Calculation**: Sum the product of ways for all components over all possible cycle values $v \in [1, M]$.
7.  **Complexity**: $O(NM)$ time and space. Given $N, M \leq 2025$, this is feasible ($\approx 4 \times 10^6$ operations).

## worker: Implement the solution in Python: Read inputs, bui
The solution implements the following steps:
1.  **Graph Construction**: Reads input and builds the reversed graph where an edge $A_i \to i$ exists. This transforms the problem into counting non-decreasing assignments on trees rooted at cycle nodes (in the reversed graph).
2.  **Cycle Detection**: Uses in-degree peeling (Kahn's algorithm variant) to identify cycle nodes. Nodes with in-degree 0 in the original graph are tree nodes and are removed iteratively. The remaining nodes form the cycles.
3.  **Topological Sort**: Computes the topological order of the reversed graph starting from leaves (nodes with out-degree 0 in the reversed graph) to ensure children are processed before parents.
4.  **Dynamic Programming**:
    -   Computes `dp[u][v]`: the number of valid assignments for the subtree rooted at `u` (in the reversed graph) given `x[u] = v`.
    -   Recurrence: `dp[u][v] = product(S[c][v])` for all children `c`, where `S[c][v]` is the prefix sum of `dp[c]`.
    -   For cycle nodes, the child corresponding to the cycle predecessor is excluded to avoid circular dependency, as all cycle nodes must share the same value.
    -   `S[u][v]` is computed as the prefix sum of `dp[u]`.
5.  **Aggregation**: Groups cycle nodes into their respective cycles. For each cycle, computes the product of `dp[c][v]` for all `c` in the cycle for each `v`, and sums these products over all `v` to get the contribution of the component.
6.  **Output**: Prints the total sum modulo 998244353.

Complexity: $O(N \cdot M)$ time and space, which fits within the constraints ($N, M \le 2025$).
