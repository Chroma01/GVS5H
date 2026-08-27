
## ideation
The core difficulty is to partition the tree into vertex-disjoint paths of exactly $K$ vertices. This can be solved with a greedy Depth-First Search (DFS) on the tree.
1. Root the tree arbitrarily (e.g., at node 1).
2. Process nodes in post-order. Each node returns the length of the "dangling" path segment (including the node itself) that extends upwards to its parent.
3. If a child's returned length is exactly $K$, that path is complete and is discarded. Otherwise, it must be connected through the current node.
4. At each node, we collect the incomplete lengths from its children. Since a path can only pass through a node once, we can pair up at most two child paths. A pair $(a, b)$ forms a complete path of length $K$ if $a + b + 1 = K$ (i.e., $a + b = K - 1$). We greedily remove all such pairs.
5. After removing all complete pairs, there can be AT MOST ONE remaining incomplete child path, because the current node can only extend a single path upwards to its parent. If more than one remains, a valid partition is impossible.
6. If exactly one remains with length $x$, the node returns $x + 1$. If zero remain, the node starts a new dangling path of length $1$.
7. At the root, the final returned length must be exactly $K$ (completing the final path), otherwise it's impossible.
8. Edge case: $K=1$ works perfectly with this logic, as leaves return 1, which equals $K$, so they are immediately discarded by their parents, leaving every node to form its own path of length 1.
9. Complexity is $O(NK)$ time and space. Recursion depth needs to be increased to handle $NK \le 2 \times 10^5$.

## worker: Write the final Python code implementing the greed
Implemented the greedy post-order DFS algorithm. 
- The tree is rooted arbitrarily at node 1.
- Each node returns the length of the incomplete path extending upwards to its parent.
- Completed paths of length exactly $K$ are discarded and not passed up.
- At each node, pairs of child paths that sum to $K-1$ are matched and completed using a `Counter` for $O(\text{deg})$ efficiency.
- If more than one incomplete path remains at a node, it is impossible to route them all through the parent, triggering a global failure flag.
- The root must return exactly $K$ to complete the final path.
- Recursion limit is safely increased to handle the maximum constraint of $2 \times 10^5$ nodes.
