
## ideation
The problem asks for the minimum number of vertices to delete to transform a given tree $T$ into a "Snowflake Tree". A Snowflake Tree is defined by parameters $x$ and $y$: a central node connected to $x$ intermediate nodes, each of which is connected to exactly $y$ leaf nodes. The total number of vertices is $1 + x + x \cdot y$.

Key observations:
1.  **Structure**: The Snowflake Tree has a specific hierarchy: Center -> Intermediate Nodes -> Leaves.
2.  **Rooting**: Since the tree is unrooted, any vertex can be the center. We can iterate over each vertex $c$ as a potential center.
3.  **Local Structure**: If $c$ is the center, its neighbors in the Snowflake Tree are the intermediate nodes. Let $v$ be a neighbor of $c$. In the Snowflake Tree, $v$ is connected to $c$ and exactly $y$ leaves. This means in the original tree (rooted at $c$), the subtree at $v$ must be pruned such that $v$ retains exactly $y$ children that are leaves in the final tree.
4.  **Feasibility of $y$ for a neighbor $v$**: For a neighbor $v$ of $c$ to serve as an intermediate node with parameter $y$, $v$ must have at least $y$ descendants in its subtree (when rooted at $c$) that can become leaves. Specifically, any child $u$ of $v$ can become a leaf by deleting all of $u$'s descendants. Thus, the maximum number of leaves $v$ can support is its number of children in the tree rooted at $c$. Let $deg_c(v)$ be the number of children of $v$ when the tree is rooted at $c$. Then $v$ can support any $y \in \{1, \dots, deg_c(v)\}$.
5.  **Global Constraint**: All intermediate nodes must share the same $y$.
6.  **Optimization for Fixed Center $c$**:
    -   Root the tree at $c$.
    -   For each neighbor $v$ of $c$, determine $d_v = deg_c(v)$ (number of children).
    -   If $d_v = 0$, $v$ cannot be an intermediate node (since $y \ge 1$).
    -   If $d_v \ge 1$, $v$ can support any $y \le d_v$.
    -   For a fixed $y$, the number of valid intermediate nodes is the count of neighbors $v$ with $d_v \ge y$. Let this count be $N_c(y)$.
    -   If $N_c(y) > 0$, the number of vertices kept is $1 + N_c(y) \cdot y$.
    -   We want to maximize $1 + N_c(y) \cdot y$ over all valid $y \ge 1$.
    -   The minimum deletions for center $c$ is $N - \max_{y \ge 1} (1 + N_c(y) \cdot y)$.
7.  **Efficient Calculation**:
    -   For each center $c$, we collect the degrees $d_v$ of its neighbors.
    -   We need to compute $\max_{y} y \cdot (\text{count of } d_v \ge y)$.
    -   This can be done efficiently by sorting the degrees or using a frequency array. Since the sum of degrees is $O(N)$, sorting the degrees for each node takes time proportional to the degree. The total time complexity will be $O(N \log N)$ or $O(N)$ depending on implementation.
    -   Specifically, for each node $c$, let $D_c$ be the list of children counts of its neighbors. Sort $D_c$ in descending order. Then for each distinct value $v$ in $D_c$, the count of neighbors with degree $\ge v$ is the number of elements $\ge v$. We calculate $v \cdot \text{count}$ and take the maximum.

Pitfalls:
-   The root $c$ itself is not a neighbor of itself. The neighbors are the adjacent vertices.
-   When rooting at $c$, the "children" of a neighbor $v$ are all adjacent vertices to $v$ except $c$.
-   $y$ must be at least 1.
-   If no neighbor can support any $y$ (i.e., all neighbors are leaves in the original tree rooted at $c$), then $c$ cannot be the center of a Snowflake Tree with $x \ge 1, y \ge 1$. However, the problem guarantees it's always possible.

## worker: (None)
The problem requires finding a subgraph that is a "Snowflake Tree" with minimum deletions. A Snowflake Tree is defined by a center, $x$ intermediate nodes, and each intermediate node connected to $y$ leaves. All intermediate nodes share the same $y$.

1.  **Structure Analysis**: For any vertex $c$ in the original tree, we can consider it as the potential center of the Snowflake Tree. If $c$ is the center, its neighbors in the Snowflake Tree must be a subset of its neighbors in the original tree.
2.  **Local Constraint**: For a neighbor $v$ of $c$ to be an intermediate node with parameter $y$, $v$ must be connected to $c$ and exactly $y$ leaves in the final tree. In the original tree rooted at $c$, $v$ has some number of children. Let $d_v$ be the number of children of $v$ in the tree rooted at $c$. Any child of $v$ can be turned into a leaf by deleting its subtree. Thus, $v$ can support any $y \in \{1, \dots, d_v\}$. If $d_v = 0$, $v$ cannot be an intermediate node.
3.  **Global Constraint**: The parameter $y$ must be the same for all chosen intermediate nodes.
4.  **Optimization for Fixed Center**: For a fixed center $c$, we collect the values $d_v$ for all neighbors $v$ where $d_v \ge 1$. We want to find a $y \ge 1$ that maximizes $1 + y \cdot (\text{count of } v \text{ such that } d_v \ge y)$.
5.  **Algorithm**:
    -   Iterate over each vertex $c$ from $1$ to $N$.
    -   For each $c$, determine the list of $d_v$ for all neighbors $v$. Note that $d_v = \text{degree}(v) - 1$ because $v$ is connected to $c$ and its other neighbors are its children in the tree rooted at $c$.
    -   Filter out neighbors with $d_v = 0$.
    -   Sort the list of $d_v$ in descending order.
    -   Iterate through the sorted list. For the $i$-th element (0-indexed) with value $d$, there are at least $i+1$ neighbors with degree $\ge d$. The number of kept vertices for this $y=d$ is $1 + (i+1) \cdot d$.
    -   Track the maximum number of kept vertices across all centers and all valid $y$.
    -   The answer is $N - \text{max\_kept}$.
6.  **Complexity**: For each node $c$, we process its neighbors. The total number of neighbors across all nodes is $2(N-1)$. Sorting the neighbors' degrees for each node takes $O(\text{deg}(c) \log \text{deg}(c))$. The sum of $\text{deg}(c) \log \text{deg}(c)$ over all $c$ is bounded by $O(N \log N)$. This fits within the time limits for $N \le 3 \times 10^5$.
