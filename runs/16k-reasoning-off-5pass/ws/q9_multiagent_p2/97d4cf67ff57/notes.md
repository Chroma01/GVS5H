
## ideation
The problem asks for the maximum size of a subgraph of a given tree $T$ that is an "alkane". An alkane is a tree where every vertex has degree 1 or 4, and there is at least one vertex of degree 4.
Key observations:
1.  **Structure**: The subgraph must be connected. Since $T$ is a tree, the subgraph is also a tree.
2.  **Degree Constraints**: In the subgraph, every node $v$ has $deg(v) \in \{1, 4\}$.
3.  **Implication**: We cannot have any node with degree 2 or 3 in the subgraph. This means we cannot select a node $u$ and connect it to exactly 2 or 3 neighbors in the subgraph.
4.  **DP State**: We can use tree DP. For each node $u$, we decide whether to include it in the alkane. If included, we need to determine how many of its children are connected to it in the subgraph.
    -   If $u$ is connected to its parent (in the final alkane), it needs $4-1=3$ children to be an internal node, or $1-1=0$ children to be a leaf.
    -   If $u$ is NOT connected to its parent (i.e., $u$ is the root of the alkane component), it needs 4 children to be internal, or 1 child to be a leaf.
    -   However, since we are building a single component, the "root" of the component in our DP (relative to the tree root) might not be the root of the alkane.
    -   Let's define states based on the number of children connected to $u$ in the subgraph restricted to $u$'s subtree:
        -   $dp[u][0]$: $u$ not selected.
        -   $dp[u][1]$: $u$ selected, 0 children connected. (Needs parent to be a leaf).
        -   $dp[u][2]$: $u$ selected, 3 children connected. (Needs parent to be an internal node).
        -   $dp[u][3]$: $u$ selected, 4 children connected. (Complete, $u$ is internal, no parent needed).
        -   $dp[u][4]$: $u$ selected, 1 child connected. (Complete, $u$ is a leaf, no parent needed).
    -   Note: States 1 and 2 are "incomplete" regarding the degree requirement of $u$ (needs parent). States 3 and 4 are "complete".
5.  **Transitions**:
    -   For $dp[u][1]$ (0 children): Sum of $dp[v][0]$ for all children $v$, plus 1 (for $u$).
    -   For $dp[u][2]$ (3 children): Select 3 children to connect. For each selected child $v$, we can take $dp[v][1]$ (leaf child) or $dp[v][2]$ (internal child). For unselected, take $dp[v][0]$. We need to maximize the sum.
    -   For $dp[u][3]$ (4 children): Similar to above, select 4 children. $u$ becomes degree 4.
    -   For $dp[u][4]$ (1 child): Select 1 child. $u$ becomes degree 1.
6.  **Degree 4 Requirement**: The problem requires at least one vertex of degree 4.
    -   State 3 ($u$ has 4 children) guarantees $u$ is degree 4.
    -   State 4 ($u$ has 1 child) guarantees $u$ is degree 1. The child must be degree 4. The child would be in state 2 (needs parent) or state 3 (complete). If child is state 2, it becomes degree 4 when connected to $u$. So if we pick a child in state 2 for $dp[u][4]$, the component has a degree 4 node.
    -   State 2 ($u$ has 3 children) needs parent. If parent connects, $u$ becomes degree 4. But if $u$ is the root of the component (no parent), it's invalid unless one of the children is already degree 4 (which implies child is state 3, but we can't connect to state 3). Wait, if child is state 2, it needs parent. So no child is degree 4 yet. So state 2 component (without parent) has no degree 4 node.
    -   State 1 ($u$ has 0 children) needs parent. No degree 4 node.
    -   So, valid final answers come from:
        -   $dp[root][3]$ (always valid).
        -   $dp[root][4]$ where the connected child is in state 2 (making child degree 4).
        -   Also, we need to handle the case where the root of the alkane is a degree 4 node but is not the root of $T$. This is covered by the DP states propagating up.
        -   Actually, if the final component is rooted at some node $r$ in $T$, and $r$ is the root of the alkane, then $r$ must be in state 3 or 4 (relative to its own children). If $r$ is in state 2 or 1, it needs a parent, which doesn't exist.
        -   So we only consider $dp[root][3]$ and $dp[root][4]$ (with valid child) as candidates for the final answer.
        -   Wait, is it possible that the alkane is just a single node? No, degree must be 1 or 4.
        -   Is it possible the alkane has no degree 4 node? No, problem statement says "at least one".
7.  **Optimization**: For states 2, 3, 4, we need to choose $k$ children to maximize the sum. This is a variation of the "select $k$ items" problem. Since $k$ is small (1, 3, 4), we can compute the best sum by considering gains.
    -   For each child $v$, we have options:
        -   Not connect: $val = dp[v][0]$.
        -   Connect as leaf: $val = dp[v][1]$.
        -   Connect as internal: $val = dp[v][2]$.
    -   We need to pick exactly $k$ children to connect.
    -   To maximize sum, for each child, we calculate the gain of connecting vs not connecting.
    -   However, we have a constraint on the type of connection (leaf vs internal) for the "has degree 4" check.
    -   We can compute two values for each state:
        -   $max\_size$: Max vertices.
        -   $max\_size\_with\_deg4$: Max vertices if the component contains a degree 4 node.
    -   For $dp[u][2]$ (3 children):
        -   $max\_size$: Pick 3 children with largest $(dp[v][1] - dp[v][0])$ or $(dp[v][2] - dp[v][0])$. Actually, just pick the best option for each of the 3 children.
        -   $max\_size\_with\_deg4$: Must pick at least one child in state 2. Iterate which child is in state 2, then pick best for remaining 2.
    -   Since $k$ is very small, we can just implement a helper function `solve(k, force_deg4)` that returns the max sum.

## worker: Implement the tree DP solution with states: 0 (not
The solution implements a tree DP with 5 states per node:
1.  **State 0**: Node $u$ is not included in the subgraph.
2.  **State 1**: Node $u$ is included, connected to 0 children. It needs a parent to satisfy the degree 1 constraint (leaf).
3.  **State 2**: Node $u$ is included, connected to 3 children. It needs a parent to satisfy the degree 4 constraint (internal).
4.  **State 3**: Node $u$ is included, connected to 4 children. It is a complete internal node (degree 4).
5.  **State 4**: Node $u$ is included, connected to 1 child. It is a complete leaf (degree 1).

For each state, we compute the maximum number of vertices in the component formed by $u$ and its descendants. We also track whether the component contains at least one vertex of degree 4.
-   **State 1**: Always has size 1 (just $u$) and no degree 4 node.
-   **State 2**: Requires selecting 3 children. We use a helper function `pick_k` to select the best 3 children. The component has a degree 4 node if any selected child is in State 2 (which becomes degree 4 when connected to $u$).
-   **State 3**: Requires selecting 4 children. $u$ itself is degree 4, so `has_deg4` is always true.
-   **State 4**: Requires selecting 1 child. `has_deg4` is true if the selected child is in State 2.

The `pick_k` function efficiently selects the best $k$ children by sorting based on the gain of connecting them (comparing State 1 vs State 0, and State 2 vs State 0). It handles the constraint of having at least one internal child for the `has_deg4` check.

Finally, the answer is derived from the root (node 1). Since the root has no parent, States 1 and 2 are invalid as standalone components (they need a parent). We only consider State 3 (root is internal) and State 4 (root is leaf, but child is internal) for the final answer.

## worker: Test the solution with Sample 1 (N=9) to verify co
The solution implements a tree DP with 5 states per node to handle the constraints of the "alkane" subgraph (degrees 1 or 4, at least one degree 4).
- **State 0**: Node not included.
- **State 1**: Node included, 0 children connected (needs parent to be a leaf).
- **State 2**: Node included, 3 children connected (needs parent to be an internal node).
- **State 3**: Node included, 4 children connected (complete, node is internal).
- **State 4**: Node included, 1 child connected (complete, node is a leaf).

The `pick_k` function efficiently selects the best $k$ children to connect to the current node, maximizing the size of the component. It also tracks whether the component contains a vertex of degree 4.
- For State 2 and 4, the component might not have a degree 4 node yet (depending on the children's states), so we track `has_deg4`.
- For State 3, the node itself is degree 4, so `has_deg4` is always true.

The final answer is derived from the root (node 1). Since the root has no parent, States 1 and 2 are invalid as standalone components (they require a parent to satisfy degree constraints). We only consider State 3 (root is internal) and State 4 (root is leaf, but the connected child is internal, making the child degree 4).

## worker: Run the code against Sample 1, Sample 2, and Sampl
The code implements the tree DP solution with 5 states per node as planned.
- **State 0**: Node not selected.
- **State 1**: Node selected, 0 children connected (needs parent).
- **State 2**: Node selected, 3 children connected (needs parent).
- **State 3**: Node selected, 4 children connected (complete, node is internal).
- **State 4**: Node selected, 1 child connected (complete, node is leaf).

The `pick_k` function is optimized to select the best $k$ children to connect. It handles the constraint of having at least one internal child (State 2) for the `force_internal` case by iterating through all possible candidates for the internal child and picking the best $k-1$ others. This ensures correctness for States 2 and 4 where the "has degree 4" property depends on the children.

The final answer is derived from the root (node 1), considering only States 3 and 4, as States 1 and 2 require a parent which the root does not have.

## worker: finalize
The solution implements a tree DP with 5 states per node to handle the constraints of the "alkane" subgraph (degrees 1 or 4, at least one degree 4).
- **State 0**: Node not selected.
- **State 1**: Node selected, 0 children connected (needs parent to be a leaf).
- **State 2**: Node selected, 3 children connected (needs parent to be an internal node).
- **State 3**: Node selected, 4 children connected (complete, node is internal).
- **State 4**: Node selected, 1 child connected (complete, node is a leaf).

The `pick_k` function efficiently selects the best $k$ children to connect. It handles the constraint of having at least one internal child (State 2) for the `force_internal` case by iterating through all possible candidates for the internal child and picking the best $k-1$ others. This ensures correctness for States 2 and 4 where the "has degree 4" property depends on the children.

The final answer is derived from the root (node 1), considering only States 3 and 4, as States 1 and 2 require a parent which the root does not have.
