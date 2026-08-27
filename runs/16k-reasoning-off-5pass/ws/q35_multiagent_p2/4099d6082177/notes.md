
## ideation
The problem asks whether a tree with $NK$ vertices can be decomposed into $N$ disjoint paths, each of length $K$ (i.e., containing $K$ vertices).

A greedy strategy processing the tree from leaves to the root (post-order traversal) is effective. For each node $u$, we determine if the subtrees rooted at its children can be decomposed into complete paths of length $K$, possibly leaving one "pending" path ending at $u$ that needs to be extended upwards.

Let $L_v$ be the length of the pending path ending at child $v$ (if any). If the subtree at $v$ is fully decomposed into complete paths, we can consider $L_v = 0$.
At node $u$, we collect the pending lengths from all children. Let $S$ be the list of non-zero pending lengths from the children.
The node $u$ can extend at most one of these pending paths. All other pending paths must be "completed" at $u$. A pending path of length $L$ from a child $v$ is completed at $u$ if connecting $v-u$ makes the path length $K$. This requires $L + 1 = K$, i.e., $L = K - 1$.

Thus, the conditions at node $u$ are:
1. Let $M$ be the set of pending lengths from children that are NOT equal to $K-1$. These paths cannot be completed at $u$ unless they are extended.
2. We can extend at most one path. Therefore, if $|M| > 1$, it's impossible to complete all non-extended paths (since they aren't $K-1$), so the decomposition fails.
3. If $|M| == 0$, all children have pending paths of length $K-1$. We can extend exactly one of them to complete it (length becomes $K$). The other children's paths are not extended, so they remain length $K-1$ and cannot be completed. This is only valid if there are no other children, i.e., $|S| == 1$. If $|S| > 1$, it fails. If $|S| == 1$, the path is completed, and $u$ returns 0 (no pending path).
4. If $|M| == 1$, let the single value in $M$ be $L$. We MUST extend this path. All other children (if any) must have length $K-1$ and will be completed. The extended path becomes length $L+1$.
   - If $L+1 == K$, the path is completed, and $u$ returns 0.
   - If $L+1 < K$, a new pending path of length $L+1$ is passed up from $u$.
   - If $L+1 > K$, it's invalid (though $L < K-1$ ensures $L+1 < K$).
5. If $S$ is empty, $u$ starts a new path of length 1, so it returns 1.

After processing the root, if it returns 0, the answer is "Yes". If it returns a positive integer, it means there's an incomplete path at the root, so "No". If any node fails the conditions, "No".

Complexity: $O(NK)$ vertices, each processed once. $O(NK)$ time.

## worker: None
The algorithm uses a greedy bottom-up approach. For each node, it collects the lengths of pending paths from its children. A pending path from a child can either be extended to the current node or completed at the current node. A path of length $L$ from a child can be completed at the current node only if $L + 1 = K$, i.e., $L = K - 1$. The current node can extend at most one pending path. Therefore, all other pending paths from children must have length $K - 1$. If there are multiple pending paths with length not equal to $K - 1$, it's impossible to complete them all, so the answer is "No". If all pending paths have length $K - 1$, we can extend one to complete it, but the others will remain incomplete unless there's only one such path. The root must have no pending path (pending value 0) for a valid decomposition.

Complexity: $O(NK)$ time and space, as each vertex and edge is processed a constant number of times.
