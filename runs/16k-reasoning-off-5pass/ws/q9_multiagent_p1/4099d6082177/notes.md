
## ideation
**Core Difficulty**: The problem requires decomposing a tree into $N$ disjoint paths of length $K$ (containing $K$ vertices). This is equivalent to partitioning the vertex set into $N$ sets, where each set induces a simple path of $K$ vertices.
The key insight is that in a tree, any path decomposition can be viewed as "growing" paths from the leaves up to the root. When processing a subtree, if the number of vertices in that subtree is not a multiple of $K$, there must be exactly one "open" path segment extending from the root of that subtree into the parent. If there are multiple such segments, they cannot be merged into a single path of length $K$ because they would branch out, violating the path property. If there are zero segments, the subtree is perfectly partitioned internally.

**Candidate Approaches**:
1.  **Bottom-Up DP / Subtree Size Check**:
    - Root the tree at vertex 1.
    - Perform a DFS/post-order traversal.
    - For each node $u$, calculate the size of its subtree $S_u$.
    - Determine the "remainder" $R_u = S_u \pmod K$.
    - The condition for a valid decomposition is: For every node $u$, the number of children $v$ such that $R_v \neq 0$ must be $\le 1$.
    - If $R_u \neq 0$, it means the path starting from $u$ (going down into one of the children's subtrees) extends upwards to $u$'s parent.
    - If $R_u = 0$, the subtree rooted at $u$ is completely filled with paths of length $K$ that do not extend to $u$'s parent.
    - Finally, check the root: $R_{root}$ must be $0$ (which is guaranteed if total nodes $NK$ is divisible by $K$, but good to verify logic).
    - Wait, is $S_u \pmod K$ the correct metric?
      Let's refine: A path of length $K$ has $K$ vertices.
      If a child $v$ has a remainder $r_v = S_v \pmod K$, it means $S_v = m \cdot K + r_v$. The $m$ paths are closed inside $v$'s subtree. The remaining $r_v$ vertices must form a single path segment that ends at $v$ and extends to $u$.
      So, $u$ receives $r_v$ vertices from child $v$. Since $r_v \in [1, K-1]$, this forms a partial path of length $r_v$ ending at $v$.
      $u$ itself adds 1 vertex.
      The total "partial path length" accumulating at $u$ from children + itself must be handled.
      Actually, the standard logic for this specific problem (often seen in competitive programming contexts like AtCoder) is:
      Count how many children $v$ have $S_v \pmod K \neq 0$.
      If count $> 1$, impossible (multiple dangling paths meet at $u$, cannot merge).
      If count $== 1$, let that child be $v$. The path from $v$ extends to $u$. The new remainder at $u$ becomes $(S_v \pmod K) + 1 + \sum (S_{other\_children} \pmod K)$? No.
      
      Correct Logic Refinement:
      Let $rem[u]$ be the number of vertices in the "dangling" path segment ending at $u$ that needs to be extended upwards.
      Initially for leaves, $rem[u] = 1$.
      When processing $u$:
      Sum the $rem[v]$ for all children $v$.
      If any child $v$ has $rem[v] > 0$, it contributes a path segment.
      Actually, simpler view:
      $S_u$ is the total size of subtree.
      Number of full paths inside subtree = $S_u // K$.
      Remaining vertices = $S_u \% K$.
      If $S_u \% K == 0$, no path extends from $u$ to parent.
      If $S_u \% K \neq 0$, exactly one path extends from $u$ to parent.
      Constraint: For any $u$, the number of children $v$ where $S_v \% K \neq 0$ must be $\le 1$.
      Why? Because if two children have non-zero remainders, we have two path segments coming into $u$ from below. We can't merge two paths into one path (that would create a branching point or require skipping vertices). We can only extend one path upwards. The other would have to be closed, but it's not full length $K$.
      So the condition is strictly: $\forall u, \text{count}(\{v \in children(u) \mid S_v \% K \neq 0\}) \le 1$.
      Also, total $NK$ is divisible by $K$ by definition, so root remainder is 0.

2.  **Implementation Details**:
    - Adjacency list for graph.
    - DFS to compute subtree sizes.
    - During DFS, check the condition.
    - Handle recursion depth (Python limit) if $N$ is large ($2 \cdot 10^5$). Use `sys.setrecursionlimit` or iterative DFS. Given constraints, iterative or increased recursion limit is needed.

## worker: Implement the solution using an iterative DFS (sta
1.  **Algorithm**: The solution uses a bottom-up approach on the tree. We root the tree at vertex 1.
2.  **Traversal**: To avoid recursion depth issues with Python's default limit (which is usually 1000, insufficient for $2 \cdot 10^5$ nodes), we use an iterative BFS to establish a processing order (topological sort from root to leaves). We then process nodes in reverse order (leaves to root) to simulate post-order traversal.
3.  **Subtree Size**: For each node $u$, we calculate the size of its subtree ($S_u$).
4.  **Condition Check**: For every node $u$, we count the number of children $v$ such that $S_v \pmod K \neq 0$.
    - If $S_v \pmod K \neq 0$, it means the subtree rooted at $v$ has a "dangling" path segment of length $S_v \pmod K$ that must extend to $u$.
    - If a node $u$ has more than one such child, it implies multiple path segments are trying to merge at $u$. Since paths cannot branch, this is impossible. Thus, if count $> 1$, output "No".
    - If count $\le 1$, the segments can be merged or extended upwards.
5.  **Complexity**:
    - Building adjacency list: $O(NK)$.
    - BFS: $O(NK)$.
    - Reverse iteration and checking children: Each edge is visited twice (once from each end), so $O(NK)$.
    - Total Time Complexity: $O(NK)$, which fits within the limit ($2 \cdot 10^5$).
    - Space Complexity: $O(NK)$ for adjacency list and arrays.
6.  **Edge Cases**:
    - $K=1$: Every node is a path of length 1. Condition $S_v \% 1 \neq 0$ is never true (always 0). Count is always 0. Always "Yes". Correct.
    - $N=1$: Single path of length $K$. Correct.
