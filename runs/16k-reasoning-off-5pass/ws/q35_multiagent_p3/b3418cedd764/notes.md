
## ideation
The problem asks for the number of sequences $x$ satisfying $x_i \le x_{A_i}$ for all $i$. This defines a functional graph where each node $i$ has a directed edge to $A_i$.
1.  **Graph Structure**: The graph consists of several connected components. Each component contains exactly one cycle, with trees rooted on the cycle nodes and edges directed towards the cycle.
2.  **Cycle Constraints**: For any node in a cycle, the constraints form a loop $x_i \le x_{A_i} \le \dots \le x_i$, implying all nodes in the same cycle must have equal values. Let's call the value of a cycle $v_C$.
3.  **Tree Constraints**: For a node $u$ in a tree attached to the cycle (or another tree node), $x_u \le x_{A_u}$. This means the value of a node is bounded above by its parent. The "root" of each tree is a node on the cycle.
4.  **Decomposition**: We can process each connected component independently. The total answer is the product of the number of valid assignments for each component.
5.  **Component Calculation**:
    *   Identify the cycle in the component. All nodes in the cycle must take the same value $v \in \{1, \dots, M\}$.
    *   For each node $c$ in the cycle, there is a tree rooted at $c$ (consisting of nodes that eventually point to $c$). Let $T_c$ be this tree.
    *   For a fixed value $v$ for the cycle, the number of ways to assign values to the tree $T_c$ such that all constraints are satisfied and the root $c$ has value $v$ can be computed via DP.
    *   Let $W(u, v)$ be the number of ways to assign values to the subtree rooted at $u$ such that $x_u = v$ and all internal constraints are satisfied.
    *   For a leaf $u$, $W(u, v) = 1$.
    *   For a non-leaf $u$ with children $c_1, \dots, c_k$, $W(u, v) = \prod_{j=1}^k \left( \sum_{k=1}^v W(c_j, k) \right)$. Note that the constraint is $x_{c_j} \le x_u = v$.
    *   The total ways for the component given cycle value $v$ is $\prod_{c \in \text{cycle}} W(c, v)$.
    *   The total ways for the component is $\sum_{v=1}^M \prod_{c \in \text{cycle}} W(c, v)$.
6.  **Complexity**:
    *   Computing $W(u, v)$ for all $u$ and $v \in \{1, \dots, M\}$ takes $O(N \cdot M)$ time if we use prefix sums to compute $\sum_{k=1}^v W(c, k)$ efficiently.
    *   Since $N, M \le 2025$, $N \cdot M \approx 4 \times 10^6$, which is well within time limits.
    *   We need to handle the graph structure: find cycles, identify tree nodes, and process them in bottom-up order (leaves to roots).

## worker: [todo] Parse input and build the functional graph 
The solution models the problem as a functional graph where each node $i$ has an edge to $A_i$. The constraints $x_i \le x_{A_i}$ imply that for any cycle in the graph, all nodes in the cycle must have equal values. The graph consists of several connected components, each containing exactly one cycle with trees rooted on the cycle nodes.

1.  **Graph Processing**: We first identify which nodes are part of cycles using a topological sort (Kahn's algorithm) to peel off tree nodes. Nodes remaining with in-degree > 0 are part of cycles.
2.  **Dynamic Programming**: For each node $u$, we compute $DP[u][v]$, which represents the number of ways to assign values to the tree attached to $u$ (excluding other cycle nodes) such that $x_u = v$. The recurrence is $DP[u][v] = \prod_{c \in \text{children}(u)} \left( \sum_{k=1}^v DP[c][k] \right)$, where children are nodes $c$ such that $A_c = u$. This is computed in bottom-up order (leaves to roots) using prefix sums for efficiency.
3.  **Cycle Handling**: For each cycle, all nodes must have the same value $v$. The number of ways to assign the trees attached to the cycle nodes given $x_c = v$ for all $c$ in the cycle is $\prod_{c \in \text{cycle}} DP[c][v-1]$. We sum this product over all possible values $v \in \{1, \dots, M\}$ to get the total ways for the component.
4.  **Final Answer**: The total number of valid sequences is the product of the ways for each connected component, modulo 998244353.

The time complexity is $O(N \cdot M)$ due to the DP computation, which is feasible given $N, M \le 2025$.
