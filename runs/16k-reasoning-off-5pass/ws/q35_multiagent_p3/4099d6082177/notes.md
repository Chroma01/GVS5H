
## ideation
The problem asks whether a tree with $NK$ vertices can be decomposed into $N$ disjoint paths, each containing exactly $K$ vertices.

Key insights:
1. **Structure of Decomposition**: Since the paths are vertex-disjoint and cover all vertices, every edge in the tree either belongs to one of the paths or connects two different paths. However, the condition is purely about finding a set of vertex-disjoint paths of length $K$ (i.e., $K$ vertices) that partition the vertex set.
2. **Greedy Strategy from Leaves**: We can root the tree arbitrarily (e.g., at vertex 1) and process it bottom-up. For each node, we need to determine if the subtree rooted at that node can be fully decomposed into complete paths of length $K$, except possibly for one "pending" path segment that ends at the current node and extends upward to the parent.
3. **State Definition**: Let $f(u)$ be the length of the pending path segment ending at node $u$ that extends toward its parent. If the subtree at $u$ is perfectly decomposed (no pending segment), $f(u) = 0$. Otherwise, $f(u)$ is the number of vertices in the incomplete path segment ending at $u$ (including $u$).
4. **Transition**:
   - For a leaf $u$, if $K=1$, it forms a complete path, so $f(u)=0$. If $K>1$, it starts a pending path of length 1, so $f(u)=1$.
   - For an internal node $u$, consider all children $v$. Each child returns a value $f(v)$.
     - If $f(v) = 0$, the child's subtree is fully decomposed.
     - If $f(v) > 0$, there is a pending path of length $f(v)$ ending at $v$ that needs to be extended to $u$.
   - Node $u$ can extend at most ONE pending path from its children to itself (since $u$ has only one parent edge to continue a path upward).
   - Therefore, if more than one child has $f(v) > 0$, it's impossible to decompose the tree (we can't merge two pending paths at $u$ and still have a valid single path going upward, nor can we leave both pending as they would require two upward edges). So, if count of children with $f(v) > 0$ is $> 1$, return invalid.
   - If exactly one child $v$ has $f(v) > 0$, we extend that path: new length at $u$ is $f(v) + 1$.
   - If no child has $f(v) > 0$, $u$ starts a new pending path of length 1.
   - After computing the new length $L$ at $u$:
     - If $L == K$, the path is complete. Set $f(u) = 0$.
     - If $L > K$, it's invalid (path too long).
     - If $L < K$, set $f(u) = L$.
5. **Root Check**: After processing the root, $f(root)$ must be 0, meaning all paths are complete.

Pitfalls:
- $K=1$ is a special case where every vertex is a path of length 1. The logic should handle this naturally (any node with children will see $f(v)=0$ if $K=1$, so it starts a new path of length 1, which immediately completes to 0).
- The condition "more than one child with pending path" is critical.
- Need to handle large inputs efficiently ($NK \le 2 \times 10^5$), so recursion depth might be an issue in Python. Use `sys.setrecursionlimit` or iterative DFS.

## worker: [todo] Implement a DFS function that computes the 
The solution uses a bottom-up DFS approach to determine if the tree can be decomposed into $N$ disjoint paths of $K$ vertices each.

**Key Algorithm:**
1. Root the tree at vertex 1 and process nodes in bottom-up order (leaves to root).
2. For each node $u$, we compute $f(u)$, the length of the pending path segment ending at $u$ that extends toward its parent.
3. For each child $v$ of $u$, if $f(v) > 0$, it means there's an incomplete path of length $f(v)$ ending at $v$ that needs to be extended to $u$.
4. **Critical Constraint**: Node $u$ can extend at most ONE pending path from its children (since $u$ has only one parent edge). If more than one child has a pending path, decomposition is impossible.
5. If exactly one child has a pending path, we extend it: $f(u) = f(v) + 1$. If no child has a pending path, $u$ starts a new path: $f(u) = 1$.
6. If $f(u) == K$, the path is complete, so $f(u) = 0$. If $f(u) > K$, it's invalid.
7. At the root, $f(root)$ must be 0 (all paths complete).

**Complexity:**
- Time: $O(NK)$ for building the tree and processing each node once.
- Space: $O(NK)$ for adjacency list, parent array, and pending path array.

**Edge Cases:**
- $K = 1$: Every vertex is a path, always possible.
- Star graphs, line graphs, etc.: Handled naturally by the algorithm.
