
## ideation


## worker: finalize
The problem asks whether a tree with $NK$ vertices can be partitioned into $N$ paths, each of length $K$ (i.e., $K$ vertices). We can solve this using a greedy bottom-up traversal (post-order DFS).

1.  **Root the tree** arbitrarily (e.g., at vertex 1).
2.  For each node $u$, we determine if the subtree rooted at $u$ can be fully covered by complete paths of length $K$, except possibly for one "open" path segment ending at $u$.
3.  An **open path segment** ending at $u$ has length $L < K$ and means that $u$ is an endpoint of this segment and is available to connect to its parent to extend the path.
4.  If a node $u$ has children that return open paths, $u$ must connect to them. Since $u$ can have degree at most 2 in the path decomposition, it can connect to at most 2 children.
5.  If $u$ connects to 2 children, it becomes an internal node of a path. The resulting path must be closed (length exactly $K$) because $u$ cannot connect to its parent (degree would be 3).
6.  If $u$ connects to 1 child, it becomes an endpoint. The new length is $L_{child} + 1$. If this equals $K$, the path is closed (return 0). If less than $K$, it remains open (return new length). If greater, fail.
7.  If $u$ connects to 0 children, it starts a new path of length 1. If $K=1$, it's closed (return 0). Else, it's open (return 1).
8.  Finally, check if the root returns 0 (fully covered).

The algorithm runs in $O(NK)$ time and space, which is efficient given the constraints $NK \le 2 \times 10^5$.
