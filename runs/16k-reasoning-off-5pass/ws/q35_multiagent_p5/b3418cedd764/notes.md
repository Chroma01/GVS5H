
## ideation
The problem asks for the number of sequences $x$ satisfying $x_i \leq x_{A_i}$ modulo 998244353.
1.  **Graph Structure**: The constraints define a functional graph where each node $i$ has exactly one outgoing edge to $A_i$. Such a graph consists of several connected components. Each component contains exactly one cycle, with trees rooted on the cycle nodes and edges directed towards the cycle.
2.  **Cycle Constraints**: For any node $u$ in a cycle, the condition $x_u \leq x_{A_u}$ implies that traversing the cycle leads to $x_u \leq x_u$, so all nodes in the same cycle must have equal values. Let this common value be $v$.
3.  **Tree Constraints**: For nodes not in the cycle, the condition $x_i \leq x_{A_i}$ defines a partial order. If we reverse the edges, we get a forest where the roots are the cycle nodes. The condition becomes $x_{child} \leq x_{parent}$.
4.  **Dynamic Programming**: For a fixed component, if we fix the cycle value to be $v$, the number of valid assignments for the trees attached to the cycle can be computed independently for each tree.
    -   Let $f(u, v)$ be the number of valid assignments for the subtree rooted at $u$ (in the reversed tree, i.e., $u$ is the parent in the functional graph sense? No, in the reversed tree, $u$ is the parent of its children in the original graph? Let's clarify: Original edge $i \to A_i$. Reversed edge $A_i \to i$. So $A_i$ is the parent of $i$ in the reversed tree. The condition is $x_i \leq x_{A_i}$. So for a node $u$ in the reversed tree, its children $c$ must satisfy $x_c \leq x_u$.
    -   Let $dp[u][v]$ be the number of valid assignments for the subtree rooted at $u$ in the reversed tree, given that $x_u = v$.
    -   The recurrence is: $dp[u][v] = \prod_{c \in children(u)} \left( \sum_{k=1}^v dp[c][k] \right)$.
    -   We can precompute prefix sums $S[c][v] = \sum_{k=1}^v dp[c][k]$ to evaluate this in $O(1)$ per node per $v$.
5.  **Component Aggregation**:
    -   Identify components and their cycle nodes.
    -   For each component, compute $G_c(v) = \prod_{c \in cycle} dp[c][v]$. Note that the trees attached to each cycle node are disjoint and cover all nodes in the component. The DP value $dp[c][v]$ already includes the contributions of the entire tree rooted at $c$ (in the reversed sense).
    -   The total number of valid sequences is $\sum_{v=1}^M \prod_{\text{components } c} G_c(v)$.
6.  **Complexity**:
    -   Computing $dp[u][v]$ for all $u, v$: $O(NM)$.
    -   Aggregating components and summing over $v$: $O(NM)$.
    -   Total time: $O(NM)$, which fits within limits ($2025^2 \approx 4 \times 10^6$).

## worker: [todo] Write a function to identify connected comp
The solution models the constraints as a functional graph. Each component has exactly one cycle, and all nodes in the cycle must have the same value. The trees attached to the cycle nodes are processed using dynamic programming. For each node $u$, $dp[u][v]$ represents the number of valid assignments for the subtree rooted at $u$ (in the reversed graph) given $x_u = v$. The recurrence is $dp[u][v] = \prod_{c \in children(u)} (\sum_{k=1}^v dp[c][k])$. Tree nodes are processed in topological order (leaves to cycle), and cycle nodes are processed after their tree children. For each component, the number of valid assignments with cycle value $v$ is the product of $dp[u][v]$ for all cycle nodes $u$ in the component. The final answer is the sum over $v \in [1, M]$ of the product of these values across all components. The complexity is $O(NM)$, which fits the constraints.
