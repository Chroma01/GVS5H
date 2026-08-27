
## ideation
The problem asks for the maximum number of vertices in a subgraph of a given tree $T$ that forms an "alkane". An alkane is defined as a tree where every vertex has degree 1 or 4, and there is at least one vertex of degree 4.

Key observations:
1.  **Structure**: The subgraph must be a connected subgraph (a subtree) of $T$.
2.  **Degrees**: In the subgraph, every node must have degree 1 or 4.
3.  **Existence of Degree 4**: There must be at least one node with degree 4. This implies the subgraph must have at least 5 vertices (a central node of degree 4 connected to 4 leaves).
4.  **Dynamic Programming**: We can use tree DP to find the largest valid substructure rooted at each node.
    *   For a node $u$, we consider the subtrees rooted at its children.
    *   A node $u$ in the alkane can have degree 1 (leaf) or 4 (internal).
    *   If $u$ is a leaf in the alkane, it has degree 1. In the context of the subtree rooted at $u$ (in the original tree), this means $u$ is connected to exactly one child in the alkane, and that child must be an internal node (degree 4) of the alkane (or a leaf if the alkane is just an edge, but edges are not alkanes). Actually, if $u$ is a leaf in the alkane, it connects to one neighbor. If that neighbor is in the subtree, it must have degree 4 in the alkane (since $u$ has degree 1). If the neighbor is the parent, $u$ cannot connect to parent. So a leaf in the alkane must be connected to a child that is an internal node (degree 4) or simply a valid partial structure that becomes degree 4 when connected to $u$.
    *   If $u$ is an internal node in the alkane, it has degree 4. It must be connected to 4 neighbors. These neighbors can be children or the parent.
    *   We can define DP states based on the number of edges $u$ uses to connect to its children in the alkane.
        *   State 0: $u$ has 0 edges to children. (Degree 0 in partial). If connected to parent, degree becomes 1 (valid leaf).
        *   State 3: $u$ has 3 edges to children. (Degree 3 in partial). If connected to parent, degree becomes 4 (valid internal).
        *   State 4: $u$ has 4 edges to children. (Degree 4 in partial). This forms a valid alkane component rooted at $u$ (since it cannot connect to parent).
        *   State 1: $u$ has 1 edge to child. (Degree 1 in partial). This forms a valid alkane where $u$ is a leaf, provided the child is in a state that allows it to be degree 4 (i.e., child was in State 3).
    *   Actually, we only need to track the max size of a valid partial subgraph where $u$ has 0 or 3 connections to children (to be extended upwards) and check for completed alkanes (4 connections to children, or 1 connection to a child that is "complete" in a specific way).
    *   Specifically:
        *   `dp3[u]`: Max size of a subgraph in $u$'s subtree containing $u$, where $u$ has degree 3 (connected to 3 children). This is a valid partial structure that can be extended to degree 4 by connecting to parent.
        *   To form `dp3[u]`, we pick 3 children. Each child $v$ can contribute a subgraph where $v$ has degree 0 (just $v$, size 1) or degree 3 (size `dp3[v]`). We take the best contribution.
        *   To form an alkane where $u$ is internal (degree 4), we pick 4 children. Size = $1 + \sum$ top 4 contributions. Update global max.
        *   To form an alkane where $u$ is a leaf (degree 1), $u$ must connect to exactly 1 child, and that child must become degree 4. This means the child must be in state 3 (degree 3 in partial). Size = $1 + \text{dp3}[child]$. Update global max.

Algorithm:
1.  Root the tree at vertex 1.
2.  Perform a post-order traversal (bottom-up).
3.  For each node $u$, collect values from children. The value of a child $v$ is $\max(1, \text{dp3}[v])$. (1 represents $v$ as a leaf in the partial structure, $\text{dp3}[v]$ represents $v$ as an internal node in a partial structure).
4.  Sort these values descending.
5.  Compute `dp3[u]` using the top 3 values.
6.  Check for alkane with $u$ as internal node (top 4 values).
7.  Check for alkane with $u$ as leaf (best child with `dp3[v]` valid).
8.  Track global maximum.

Complexity: $O(N \log N)$ due to sorting children values, or $O(N)$ if using linear selection for top 4. Given constraints, sorting is acceptable.

## worker: Implement the solution in Python using iterative D
The problem asks for the maximum size of a subgraph that is an "alkane", defined as a tree where every vertex has degree 1 or 4, and there is at least one vertex of degree 4.
We use dynamic programming on trees. We root the tree at vertex 1 and process nodes in post-order.
For each node $u$, we compute `dp3[u]`, which is the maximum size of a partial alkane structure in $u$'s subtree where $u$ has degree 3 (connected to 3 children). This structure can be extended to degree 4 by connecting to the parent.
The value of a child $v$ is `max(1, dp3[v])`. If `dp3[v]` is undefined (-1), we use 1 (representing $v$ as a leaf in the partial structure).
We sort the values of children descending.
- `dp3[u]` is computed using the top 3 values.
- We check for a complete alkane where $u$ is an internal node (degree 4) using the top 4 values.
- We check for a complete alkane where $u$ is a leaf (degree 1) by connecting to a child $v$ that has `dp3[v]` defined (so $v$ becomes degree 4).
We track the global maximum size.
Complexity is $O(N \log N)$ due to sorting children values, which is acceptable for $N \le 2 \times 10^5$.
