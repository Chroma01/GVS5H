
## ideation
The problem asks for the number of sequences $x$ satisfying $x_i \le x_{A_i}$. This defines a functional graph where each node $i$ has exactly one outgoing edge to $A_i$. Such a graph decomposes into several connected components, each consisting of exactly one cycle with some trees rooted on the cycle nodes and directing towards the cycle.

Key observations:
1. **Component Independence**: The choices for $x_i$ in different connected components are independent. Thus, the total answer is the product of the answers for each component.
2. **Cycle Constraint**: Within a component, all nodes in the cycle must have the same value. Let this common value be $c$.
3. **Tree Constraint**: For any node $u$ not in the cycle, its value is constrained by its parent. Specifically, if we view the edges as $i \to A_i$, then $x_i \le x_{A_i}$. This means values decrease (or stay same) as we move towards the cycle. Conversely, if we reverse the edges to form trees rooted at cycle nodes (edges $A_i \to i$), then $x_{A_i} \ge x_i$. So, for a tree rooted at $r$ (where $r$ is on the cycle), if $x_r = c$, then for any node $u$ in the tree, $x_u \le c$.
4. **DP on Trees**: For a tree rooted at $r$, let $W_u(v)$ be the number of valid assignments for the subtree rooted at $u$ given $x_u = v$.
   - If $u$ is a leaf, $W_u(v) = 1$ for all $v \ge 1$.
   - If $u$ has children $v_1, v_2, \dots$, then $W_u(v) = \prod_{j} (\sum_{k=1}^v W_{v_j}(k))$.
   - Let $S_u(v) = \sum_{k=1}^v W_u(k)$. Then $W_u(v) = \prod_{j} S_{v_j}(v)$.
   - Note that $S_u(v) = S_u(v-1) + W_u(v)$.
5. **Polynomial Structure**: It can be shown that $W_u(v)$ is a polynomial in $v$ of degree equal to the size of the subtree at $u$. More importantly, the sum $S_u(v)$ is also a polynomial-like function. However, since $N, M \le 2025$, we can compute the values $W_u(v)$ for $v=1 \dots M$ directly using DP.
   - Process nodes in reverse topological order (leaves to root). For a tree, this means processing children before parents.
   - For each node $u$, compute $W_u(v)$ for $v=1 \dots M$.
     - $W_u(1) = \prod_{j} S_{v_j}(1)$.
     - $W_u(v) = W_u(v-1) \times \frac{\prod_{j} S_{v_j}(v)}{\prod_{j} S_{v_j}(v-1)}$? No, division is tricky with modulo.
     - Better: Compute prefix sums $S_{v_j}(v)$ for each child. Then $W_u(v) = \prod_{j} S_{v_j}(v)$.
     - Then $S_u(v) = S_u(v-1) + W_u(v)$.
6. **Combining for Cycle**: For a component with cycle nodes $C = \{c_1, c_2, \dots, c_k\}$, if the common value is $v$, the number of ways is $\prod_{i=1}^k W_{c_i}(v)$.
   - The total ways for this component is $\sum_{v=1}^M \prod_{i=1}^k W_{c_i}(v)$.
7. **Algorithm**:
   - Build the graph. Identify components and cycles.
   - For each component, identify the cycle nodes and the trees attached to them.
   - For each tree (rooted at a cycle node), compute $W_u(v)$ for all $v \in [1, M]$ for all nodes $u$ in the tree.
     - Use BFS/DFS to determine processing order (reverse topological).
     - For each node $u$, compute $W_u(v)$ based on children's $S_{child}(v)$.
   - For each component, compute the product $P(v) = \prod_{c \in Cycle} W_c(v)$ for each $v \in [1, M]$.
   - Sum $P(v)$ for $v=1 \dots M$ to get the component's answer.
   - Multiply answers of all components modulo 998244353.

Pitfalls:
- Modulo arithmetic for products and sums.
- Correctly identifying cycles and trees.
- Handling the case where a node is part of a cycle vs part of a tree.
- Efficiency: $O(N \cdot M)$ is acceptable since $N, M \le 2025$.

## worker: Implement the solution in Python, reading from std
The solution models the constraints as a functional graph where each node $i$ has an edge to $A_i$. This graph decomposes into components, each containing exactly one cycle with trees rooted at the cycle nodes.

1. **Graph Decomposition**: We identify cycles and tree structures. Nodes in a cycle must have the same value $x_i = c$. For each cycle node $u$, we consider the tree of nodes that flow into $u$ (excluding the cycle edges).
2. **Dynamic Programming on Trees**: For each node $u$, we compute $W_u(v)$, the number of valid assignments for the subtree rooted at $u$ given $x_u = v$. The recurrence is $W_u(v) = \prod_{c \in children(u)} S_c(v)$, where $S_c(v) = \sum_{k=1}^v W_c(k)$.
3. **Processing Order**: We process nodes in reverse topological order (leaves to root) to ensure children are computed before parents.
4. **Combining Results**: For each component, the number of valid assignments with cycle value $c$ is $\prod_{u \in cycle} W_u(c)$. We sum this product over $c=1 \dots M$ to get the component's answer.
5. **Final Answer**: The total answer is the product of the answers for all components, modulo 998244353.

The time complexity is $O(N \cdot M)$, which is efficient for $N, M \le 2025$.
