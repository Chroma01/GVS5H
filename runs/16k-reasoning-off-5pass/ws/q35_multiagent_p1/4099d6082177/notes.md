
## ideation
The problem asks if a tree with $NK$ vertices can be decomposed into $N$ paths of length $K$ (i.e., each path has $K$ vertices and $K-1$ edges).

The core difficulty lies in efficiently checking if such a decomposition exists. A naive backtracking approach is too slow ($O(N!)$ or similar). We need a greedy or dynamic programming approach.

Key Insight:
1. In any valid decomposition, every leaf of the current tree (or original tree, considering used nodes) must be an endpoint of one of the paths.
2. If we root the tree arbitrarily (e.g., at node 1), we can process nodes from the deepest to the shallowest.
3. The deepest uncovered node *must* be an endpoint of a path. Since it's the deepest, the path must go upwards towards the root. There is no other choice for the direction of the path starting from this leaf-like node.
4. Therefore, for each deepest uncovered node $u$, we must form a path of $K$ nodes starting at $u$ and going up $K-1$ ancestors.
5. If at any point we cannot find $K-1$ valid ancestors (either because they don't exist or are already covered), the decomposition is impossible.
6. We mark all $K$ nodes in the path as covered.
7. If we successfully cover all nodes, the answer is "Yes".

Algorithm:
1. Root the tree at node 1. Compute parent pointers and depths for all nodes using BFS/DFS.
2. Sort all nodes by depth in descending order.
3. Maintain a set or boolean array `covered` to track which nodes are part of a path.
4. Iterate through the sorted nodes. If a node $u$ is not covered:
   a. Trace up $K-1$ steps from $u$ using parent pointers.
   b. If we hit the root (parent is null) before collecting $K$ nodes, or if any node in the path is already covered, return "No".
   c. Mark all $K$ nodes in this path as covered.
5. If the loop completes successfully, return "Yes".

Complexity:
- Sorting nodes by depth: $O(NK \log(NK))$.
- Processing each node: Each node is covered exactly once. Tracing up takes $O(K)$ per path, but since each node is visited a constant number of times (once as a start, and potentially as an ancestor), the total work is proportional to the number of nodes. Specifically, we only start a path from an uncovered node. The tracing up might visit covered nodes? No, if we hit a covered node, we fail. So we only traverse uncovered nodes. Each node is part of exactly one path. So total time is $O(NK)$.
- Overall: $O(NK \log(NK))$ due to sorting, which is acceptable for $NK \le 2 \times 10^5$.

Pitfalls:
- $K=1$: Each node is a path of length 1. Always possible.
- $K > NK$: Impossible, but constraints say $NK \ge 1$, and $N \ge 1, K \ge 1$. If $K=1$, $N=NK$.
- The parent pointer approach requires careful handling of the root.
- We must ensure that when we trace up, we don't go beyond the root.

Let's refine the "trace up" step. For a node $u$, we need $u, parent(u), parent(parent(u)), \dots$ for $K$ nodes. If $K=1$, we just mark $u$ as covered.

Implementation details:
- Adjacency list for the tree.
- BFS from root (node 1) to compute `parent` and `depth`.
- List of nodes sorted by depth descending.
- Boolean array `covered`.

## worker: <none>
The algorithm uses a greedy strategy based on processing nodes from deepest to shallowest. The key insight is that the deepest uncovered node must be an endpoint of one of the K-length paths. Since it's the deepest, the path must go upwards towards the root. We trace up K-1 ancestors to form the path. If at any point we can't find K valid uncovered ancestors (either because we hit the root or encounter a covered node), the decomposition is impossible.

Complexity:
- BFS for parent/depth: O(NK)
- Sorting nodes by depth: O(NK log(NK))
- Processing each node: Each node is covered exactly once, and we only trace up through uncovered nodes. Total work is O(NK).
- Overall: O(NK log(NK)), which is efficient for NK ≤ 2×10^5.

Edge cases handled:
- K=1: Always possible (each node is its own path)
- Root handling: Parent of root is 0, which is checked during tracing
