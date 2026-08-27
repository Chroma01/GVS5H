
## ideation
The core difficulty lies in correctly defining the DP state and transitions to ensure that the resulting subgraph satisfies the "alkane" properties: a tree where every vertex has degree 1 or 4, with at least one vertex of degree 4.

Key insights:
1. **Subgraph Structure**: Since the original graph is a tree, any subgraph is also a forest. We are looking for a connected component (a tree) that is an alkane.
2. **Degree Constraints**: In the alkane subgraph, every node has degree 1 or 4.
   - If a node is a leaf in the alkane, its degree is 1. In the context of rooting the alkane at some node, this leaf might be a child of its parent in the alkane tree, contributing 1 to the parent's degree count and having 0 children in the alkane.
   - If a node is an internal node in the alkane, its degree is 4. It connects to its parent (if not the root of the alkane) and 3 children, OR it is the root and connects to 4 children.
3. **DP State**: For each node `u` in the original tree, we want to compute the maximum size of a valid alkane-like subtree rooted at `u` where `u` has exactly `k` children connected in the subgraph.
   - `dp[u][k]` = maximum number of vertices in a subtree rooted at `u` with `k` children included in the alkane structure.
   - Valid `k` values for `u` to be part of a valid alkane:
     - If `u` is a leaf in the alkane, it has 0 children in the alkane (`k=0`). Its degree in the alkane is 1 (connected to parent).
     - If `u` is an internal node in the alkane, it has 3 children in the alkane (`k=3`) if it has a parent, or 4 children (`k=4`) if it is the root of the alkane component.
     - States `k=1` and `k=2` are invalid for any node that is not a root of the entire alkane? Actually, if a node has `k=1` or `k=2` children, its degree would be 2 or 3 (if it has a parent) or 1 or 2 (if it's a root). Degrees 2 and 3 are not allowed. Degree 1 is allowed only for leaves, but a leaf has 0 children. So `k=1` and `k=2` are never valid final states for any node in a valid alkane. They can be intermediate states? No, because we build from leaves up. A node with `k=1` child cannot form a valid degree. So we only care about `k=0, 3, 4`.
     - However, to compute `dp[u][3]` and `dp[u][4]`, we need to know the best values from children. A child `v` connected to `u` must be a leaf in the alkane structure relative to `u`? No, `v` can be the root of a larger alkane subtree that is attached to `u`. But if `v` is attached to `u`, then `v`'s degree in the alkane is 1 (only connected to `u`) plus whatever children it has. Wait, if `v` is connected to `u`, then `v` is a child of `u` in the alkane tree. For `v` to be valid, its degree in the alkane must be 1 or 4. Since it has a parent `u`, it must have degree 4 in total, meaning it must have 3 children in the alkane. So `v` must contribute a structure where it has 3 children. Thus, the value contributed by child `v` when connected to `u` is `dp[v][3]`.
     - What if `v` is a leaf in the alkane? Then `v` has 0 children, so `dp[v][0] = 1`. Its degree is 1 (connected to `u`). This is valid.
     - So, for a node `u` to have `k` children in the alkane, each child `v` must provide a valid alkane subtree where `v` has `k_v` children such that `v`'s total degree is 1 or 4.
       - If `v` is a leaf in the alkane, `k_v = 0`, degree = 1. Valid. Contribution: `dp[v][0]`.
       - If `v` is an internal node in the alkane, `k_v = 3`, degree = 4 (3 children + 1 parent `u`). Valid. Contribution: `dp[v][3]`.
     - Therefore, for each child `v`, we have two options to connect it to `u`:
       1. Don't connect: contribution 0.
       2. Connect: contribution `max(dp[v][0], dp[v][3])`. Note: `dp[v][0]` means `v` is a leaf in the alkane. `dp[v][3]` means `v` is an internal node with 3 children.
     - We want to choose `k` children to connect to `u` to maximize the total size.
     - `dp[u][k] = 1 + sum of the largest k values of {max(dp[v][0], dp[v][3]) for v in children(u)}`.
     - We compute this for `k=0, 1, 2, 3, 4`.
     - However, `dp[u][1]` and `dp[u][2]` are not valid final states for `u` to be a root of an alkane component (degree 1 or 2 is invalid for internal nodes, and degree 1 for a root with 1 child is invalid because the child would have degree 1+? No, if root has 1 child, root degree 1, child degree 1. But we need a degree 4 node. So a single edge is not an alkane. We need at least one degree 4 node.
     - The final answer is the maximum `dp[r][4]` over all nodes `r`. Why `dp[r][4]`? Because if `r` has 4 children in the alkane, its degree is 4. This satisfies the "at least one degree 4" condition. The children are valid alkane subtrees (each child `v` has `max(dp[v][0], dp[v][3])` structure, which is valid).
     - What if the alkane is just a single node? No, degree 0 is not 1 or 4.
     - What if the alkane has a root with degree 1? Then it's a leaf. But it must have a degree 4 node somewhere else. In that case, the degree 4 node would be a child of some node, and so on. Eventually, we can root the alkane at the degree 4 node. So checking `dp[r][4]` for all `r` covers all cases where the alkane has a degree 4 node.

Pitfalls:
- Forgetting that children can be either leaves (`dp[v][0]`) or internal nodes (`dp[v][3]`) in the alkane.
- Not handling the case where no alkane exists (output -1).
- Incorrectly computing the top-k sums.

## worker: (None)
The problem asks for the largest subgraph of a tree that is an "alkane": a tree where every vertex has degree 1 or 4, with at least one vertex of degree 4.

We use dynamic programming on trees. For each node `u`, we define `dp[u][k]` as the maximum number of vertices in a valid partial alkane structure rooted at `u` where `u` has exactly `k` children connected in the subgraph.

Key observations:
1. In the alkane subgraph, every node has degree 1 or 4.
2. If a node `v` is a child of `u` in the alkane subgraph, `v` has a parent (`u`). Thus, `v`'s degree in the alkane must be 4 (since degree 1 is only for leaves, which have no children in the alkane structure relative to their parent). This means `v` must have 3 children in the alkane. So, if we connect `v` to `u`, `v` must be in state `dp[v][3]`.
3. Alternatively, `v` could be a leaf in the alkane subgraph. In this case, `v` has 0 children in the alkane. So, if we connect `v` to `u`, `v` must be in state `dp[v][0]`.
4. Therefore, the value contributed by connecting child `v` to `u` is `max(dp[v][0], dp[v][3])`. If neither is valid, `v` cannot be connected.
5. For node `u` to have `k` children connected, we pick the `k` children with the largest contributions.
   - `dp[u][0] = 1` (just `u`).
   - `dp[u][k] = 1 + sum of top k contributions`.
6. A valid alkane must have at least one node of degree 4. If we root the alkane at a node `r` with degree 4, then `r` has 4 children in the alkane. This corresponds to `dp[r][4]`. Since `r` has degree 4, the "at least one degree 4" condition is satisfied.
7. We compute `dp[u][4]` for all `u` and take the maximum. If no node has `dp[u][4]` valid, the answer is -1.

Complexity:
- Tree traversal: O(N).
- For each node, sorting children's contributions: O(deg(u) log deg(u)). Sum of deg(u) is 2(N-1), so total sorting time is O(N log N) in worst case (star graph), but typically much faster.
- Overall time complexity: O(N log N) or O(N) depending on implementation of top-k. Given N=2e5, this is efficient.
