
## ideation
The core difficulty lies in handling the cyclic dependencies in the functional graph defined by $i \to A_i$. The graph decomposes into disjoint components, each containing exactly one cycle with trees rooted on the cycle nodes and directing towards the cycle.

Key insights:
1. **Component Decomposition**: Each weakly connected component has exactly one cycle. Nodes not in the cycle form trees where edges point towards the cycle.
2. **Tree Contribution**: For any node $u$ not in a cycle, if its parent $A_u$ has value $v$, then $x_u$ can be any value in $[1, v]$. This choice is independent for each node given the parent's value. If we define $cnt[u]$ as the number of nodes in the subtree rooted at $u$ (in the reversed graph, i.e., all nodes that flow into $u$), then fixing $x_{A_u} = v$ contributes a factor of $v^{cnt[u]}$ to the total count for that branch.
3. **Cycle Constraints**: For a cycle $c_1 \to c_2 \to \dots \to c_k \to c_1$, the constraints are $x_{c_1} \le x_{c_2}, x_{c_2} \le x_{c_3}, \dots, x_{c_k} \le x_{c_1}$. This chain of inequalities implies $x_{c_1} = x_{c_2} = \dots = x_{c_k} = V$ for some integer $V \in [1, M]$.
4. **Total Count per Component**: For a fixed $V$, the number of ways to assign values to the entire component is $V^K$, where $K$ is the sum of $cnt[c_i]$ for all cycle nodes $c_i$ in the component. The total number of valid assignments for the component is $\sum_{V=1}^M V^K$.
5. **Final Answer**: Since components are independent, the total answer is the product of the results for each component modulo 998244353.

Algorithm:
1. Build the graph and compute in-degrees to identify nodes not in cycles (using topological sort/Kahn's algorithm to peel off tree nodes).
2. For each node, compute $cnt[u]$, the size of the subtree rooted at $u$ in the reversed graph (nodes flowing into $u$). This can be done by processing nodes in reverse topological order (from leaves up to cycle nodes).
3. Identify cycles by finding nodes with in-degree > 0 after peeling trees. For each cycle, compute $K = \sum_{c \in \text{cycle}} cnt[c]$.
4. For each component with parameter $K$, compute $S_K = \sum_{V=1}^M V^K \pmod{998244353}$.
5. Multiply all $S_K$ together modulo 998244353.

Pitfalls:
- Incorrectly computing $cnt[u]$ or handling the direction of edges.
- Failing to correctly identify cycles after peeling trees.
- Modulo arithmetic errors when summing powers.

## worker: Implement graph construction and in-degree calcula
The solution models the problem using a functional graph where each node $i$ has an edge to $A_i$. This graph decomposes into disjoint components, each containing exactly one cycle with trees rooted on the cycle nodes and directing towards the cycle.

1.  **Graph Construction**: We build the adjacency list and compute in-degrees.
2.  **Cycle Detection**: Using Kahn's algorithm (topological sort), we peel off all nodes that are not part of any cycle. The remaining nodes with in-degree > 0 form the cycles.
3.  **Tree Contribution Calculation**: For each node $u$, we calculate $cnt[u]$, which represents the number of nodes in the "subtree" rooted at $u$ in the reversed graph (i.e., all nodes that eventually flow into $u$). This is done by processing the topologically sorted nodes in reverse order, adding the count of each node to its parent.
4.  **Cycle Processing**: For each cycle, we sum the $cnt$ values of all nodes in the cycle to get a total exponent $K$. The constraints on the cycle imply all cycle nodes must have the same value $V$. The number of ways to assign values to the entire component (cycle + attached trees) for a fixed $V$ is $V^K$. Summing over all possible $V \in [1, M]$ gives $\sum_{V=1}^M V^K$.
5.  **Final Answer**: The total number of valid sequences is the product of the results for each component modulo 998244353.

The complexity is $O(N + M \cdot N)$ in the worst case for computing power sums, but since $N, M \le 2025$, this is well within limits. The topological sort and cycle detection are $O(N)$.
