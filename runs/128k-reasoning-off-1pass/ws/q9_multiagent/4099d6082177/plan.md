The problem asks if a tree with $NK$ vertices can be decomposed into $N$ paths, each of length $K$ (containing $K$ vertices). A necessary condition is that the total number of vertices $NK$ matches the sum of vertices in all paths, which is trivially true by definition. The core constraint is structural: we need to partition the tree edges and vertices such that every component is a simple path of exactly $K$ vertices. This implies that in the decomposition, every internal vertex of a path has degree 2 within that path, and the endpoints have degree 1. In the original tree, vertices can have arbitrary degrees, but they must be "covered" by these paths. A key observation is that if we root the tree arbitrarily, we can try to greedily form paths from leaves upwards. Specifically, a path of length $K$ can be formed by extending a path from a leaf up to its ancestor at distance $K-1$. If a subtree has a "remainder" path that needs to be extended upwards, it must connect to the parent. If a subtree is fully covered by internal paths, it contributes nothing to the parent. The critical check is whether we can pair up "dangling" path ends from children with the parent to form valid paths or if the root ends up with a valid configuration. A simpler necessary and sufficient condition for this specific "path decomposition of fixed length" in a tree often relates to the ability to pair up leaves or satisfy degree constraints modulo path lengths. However, a constructive greedy approach from leaves is most robust: for each leaf, start a path of length $K$. If the path reaches the root or gets stuck, it's invalid. Actually, a more precise condition exists: we can view this as checking if the tree can be partitioned into paths of size $K$. This is possible if and only if for every subtree, the number of vertices is congruent to $0 \pmod K$ OR the subtree has a "dangling" path of length $L$ (where $1 \le L < K$) that must be extended to the parent. But wait, the paths don't have to be disjoint in terms of vertices? Yes, "decomposed" means partitioning the vertex set. So every vertex belongs to exactly one path.
Correct approach: Root the tree at vertex 1. For each node $u$, calculate the size of the subtree rooted at $u$. If the subtree size is a multiple of $K$, then the entire subtree can be perfectly partitioned into paths of length $K$ internally, contributing 0 "dangling" path ends to the parent. If the subtree size is not a multiple of $K$, say $S = qK + r$ ($0 < r < K$), then exactly one path of length $r$ must extend from the subtree to the parent. This means the subtree provides exactly one "open" end of a path at $u$ that needs to be connected to $u$'s parent to continue. If $r=0$, no path extends. If $r > 0$, one path extends. The condition is that for every node $u$ (except the root), if the child's subtree has remainder $r > 0$, we must be able to connect it to $u$. But actually, the path of length $r$ inside the child's subtree ends at some node in the child's subtree, and we extend it through the edge to $u$. The new length becomes $r+1$. We repeat this up the tree. The root must have a remainder of 0 (since the total $NK$ is divisible by $K$). However, simply checking subtree sizes modulo $K$ isn't enough because the "open" path must be extendable. The constraint is that if a child returns a path of length $r$, we attach it to $u$, making it length $r+1$. If $r+1 = K$, the path is complete and consumes $u$ (and the child's path end). If $r+1 < K$, the path continues to $u$'s parent. If $r+1 > K$, impossible.
Wait, the path length is fixed at $K$. If a child's subtree forms a path of length $r$ ending at the child (or rather, the path end is at the child), and we extend it to $u$, the length becomes $r+1$. If $r+1=K$, the path is done. If $r+1 < K$, it continues. The issue is: can we always form a path of length $r$ ending at the child? Not necessarily. The greedy strategy: For a leaf, if $K=1$, it's a path of length 1. If $K>1$, a leaf cannot start a path of length $K$ alone; it must be part of a path coming from above or going to a neighbor.
Actually, the standard solution for "partition tree into paths of length K" is:
1. Root the tree.
2. For each node, compute the size of the subtree.
3. If $size[u] \% K == 0$, the subtree is fully contained in paths.
4. If $size[u] \% K \neq 0$, then the subtree must have exactly one path extending to the parent. The length of this extension is $size[u] \% K$.
5. The condition is that for any node $u$, if a child $v$ has $size[v] \% K \neq 0$, we can connect the path from $v$ to $u$. The new length at $u$ from that child is $(size[v] \% K) + 1$. If this sum reaches $K$, the path closes at $u$. If it is less than $K$, it continues to $u$'s parent.
6. Crucially, a node $u$ can only accept one incoming path from its children? No, $u$ can be an internal node of a path (degree 2 in path) or an endpoint (degree 1). If $u$ is an internal node, it connects two path segments. If $u$ is an endpoint, it connects one.
Let's refine the state: Each node $u$ returns a value $rem[u] \in \{0, 1, \dots, K-1\}$. $rem[u]$ represents the length of the path segment ending at $u$ that extends to the parent.
- If $size[u] \% K == 0$, then $rem[u] = 0$.
- If $size[u] \% K \neq 0$, then $rem[u] = size[u] \% K$.
Is this sufficient? We need to ensure that we can actually form the path. The only constraint is that if we have multiple children with $rem[v] > 0$, we can't merge them all into one path ending at $u$ because that would require $u$ to have degree $>2$ in the path structure (which is impossible for a simple path).
Wait, if $u$ has two children $v1, v2$ with $rem[v1] > 0$ and $rem[v2] > 0$, can we connect them?
If we connect $v1$'s path to $u$, the path length becomes $rem[v1] + 1$. If we also connect $v2$, $u$ would have degree 3 in the union of paths, which is not allowed in a single path.
So, a node $u$ can have at most one child $v$ such that $rem[v] > 0$ (meaning a path comes from below and continues through $u$). All other children must have $rem[v] = 0$ (their subtrees are fully closed).
Therefore, the algorithm is:
1. Root at 1.
2. DFS post-order.
3. For each node $u$, calculate $S = size[u]$.
4. Check if $S \% K == 0$. If so, $rem[u] = 0$.
5. If $S \% K \neq 0$, we need to form a path of length $r = S \% K$ ending at $u$. This path must come from exactly one child $v$ such that $rem[v] = r-1$. All other children must have $rem[child] = 0$.
6. If there is no child with $rem[v] = r-1$, or if there are multiple children with $rem[v] > 0$ (which implies multiple paths coming up, impossible), then return "No".
7. Also, if $r=1$, we just need one child with $rem[v]=0$? No, if $r=1$, the path is just $u$ itself? No, the path length is $K$. The remainder logic is about the "dangling" part.
Let's re-evaluate the remainder logic.
Total vertices in subtree = $S$.
If $S$ is a multiple of $K$, we can partition the subtree completely. No path extends to parent. $rem[u] = 0$.
If $S = qK + r$ ($0 < r < K$), then exactly one path of length $r$ must extend from the subtree to the parent. This path consists of $r$ vertices in the subtree plus the parent and potentially more.
The path of length $r$ in the subtree must end at $u$. Why? Because if it ended at some descendant, the path would have to go through $u$ to reach the parent, making $u$ an internal node of that path. But if the path ends at a descendant, then the segment from that descendant to $u$ is part of the path. The "dangling" part is the segment from the leaf of the path up to $u$.
So, if $S \% K = r$, we need to find a child $v$ such that the path from $v$'s subtree extends to $v$ with length $r-1$. Then we add $u$ to make it length $r$.
Condition: There must be exactly one child $v$ with $rem[v] = r-1$. All other children must have $rem[child] = 0$.
If this holds, $rem[u] = r$.
If not, output No.
Base case: Leaf. $size[leaf] = 1$.
If $K=1$: $1 \% 1 = 0 \implies rem=0$. OK.
If $K>1$: $1 \% K = 1$. Need child with $rem=0$. Leaf has no children. So if $K>1$, leaf fails?
Wait, if $K>1$, a leaf cannot be the end of a path of length $K$ unless the path comes from the parent. But in the subtree of a leaf, the path of length 1 is just the leaf itself. It extends to the parent. So $rem[leaf] = 1$.
My logic "Need child with $rem=r-1$" assumes the path comes from a child. If $u$ is a leaf and $r=1$, there is no child. Does that mean it fails?
No. If $u$ is a leaf and $S=1, r=1$, the path of length 1 is just $u$. It extends to parent. We don't need a child to provide the path. The path starts at $u$.
So the rule is:
If $S \% K == 0$: $rem[u] = 0$.
Else ($r = S \% K$):
  We need to form a path of length $r$ ending at $u$.
  If $r == 1$: The path is just $u$. No child needed. Check that all children have $rem[child] == 0$. If any child has $rem > 0$, fail (multiple paths or path from child can't be merged into a length 1 path).
  If $r > 1$: We need exactly one child $v$ with $rem[v] == r-1$. All other children must have $rem[child] == 0$. If no such child or multiple such children, fail.
  Set $rem[u] = r$.
Finally, check root: $rem[root]$ must be 0.

This covers the constraints.