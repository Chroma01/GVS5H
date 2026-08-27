
## ideation
The core difficulty lies in correctly modeling the "alkane" constraints (degrees 1 or 4, at least one degree 4) within a tree subgraph using dynamic programming. The key insight is that any such subgraph is a tree where internal nodes have degree 4 and leaves have degree 1. We can root the original tree arbitrarily (e.g., at vertex 1) and compute DP states for each node representing the maximum size of a valid partial structure rooted at that node, characterized by the number of children connected to it in the subgraph.

Specifically, for a node `u`, `dp[u][k]` will store the maximum number of vertices in a subtree rooted at `u` where `u` has exactly `k` children connected to it in the subgraph. The constraints on `k` depend on whether `u` is a leaf or an internal node in the alkane:
- If `u` is a leaf in the alkane, it has degree 1 (connected only to its parent). In the rooted DP, this means `k=0` (no children connected). The size is 1.
- If `u` is an internal node in the alkane, it has degree 4.
  - If `u` is the root of the alkane, it has 4 children connected (`k=4`).
  - If `u` is not the root, it has 1 parent and 3 children connected (`k=3`).

Thus, we need to compute `dp[u][k]` for `k \in \{0, 1, 2, 3, 4\}`.
- `dp[u][0] = 1` (leaf in alkane, no children selected).
- `dp[u][k]` for `k > 0` is computed by selecting `k` children from `u`'s children such that the sum of their contributions plus `u` itself is maximized. For each child `v`, if we connect it to `u`, we can take the best valid structure from `v` where `v` has `k_v` children connected. However, note that if `v` is connected to `u`, `v`'s degree in the alkane will be `k_v + 1`. This must be either 1 or 4.
  - If `k_v + 1 = 1`, then `k_v = 0`. This means `v` is a leaf in the alkane.
  - If `k_v + 1 = 4`, then `k_v = 3`. This means `v` is an internal node with 3 children.
  - So, for each child `v`, the possible values to add to the sum are `dp[v][0]` (if we treat `v` as a leaf) or `dp[v][3]` (if we treat `v` as an internal node). We cannot use `dp[v][1]` or `dp[v][2]` or `dp[v][4]` directly as a child connection because those states imply `v` has degree 2 or 5 in the alkane, which is invalid. Wait, `dp[v][4]` implies `v` is a root of an alkane with 4 children. If `v` is connected to `u`, its degree becomes 5, which is invalid. So indeed, only `dp[v][0]` and `dp[v][3]` are valid contributions when `v` is a child of `u`.

Let `val[v] = max(dp[v][0], dp[v][3])`. If both are invalid (e.g., -infinity), then `v` cannot be connected to `u` in a valid alkane.
Then `dp[u][k]` is `1 + sum of the largest k values of `val[v]` among all children `v` of `u`.

Finally, the answer is the maximum `dp[u][4]` over all `u`. If no such `dp[u][4]` is valid, output -1.

Pitfalls:
- Ensuring that `dp[v][0]` and `dp[v][3]` are correctly computed. `dp[v][0]` is always 1 (if `v` is a leaf in the alkane). `dp[v][3]` requires `v` to have at least 3 children with valid contributions.
- Handling cases where no alkane exists.
- The constraint that the alkane must have at least one degree-4 vertex is satisfied by `dp[u][4]` since `u` has degree 4.

## worker: (None)
The solution uses dynamic programming on trees. We root the tree at vertex 1 and process nodes in bottom-up order. For each node `u`, we compute `dp[u][k]` which represents the maximum number of vertices in a valid partial alkane structure rooted at `u` where `u` has exactly `k` children connected to it in the subgraph.

Key observations:
1. In an alkane, every vertex has degree 1 or 4.
2. If a child `v` is connected to `u` in the alkane, then `v`'s degree in the alkane is `k_v + 1` where `k_v` is the number of children of `v` connected in the alkane.
3. For `v`'s degree to be valid (1 or 4), we must have `k_v + 1 = 1` (i.e., `k_v = 0`) or `k_v + 1 = 4` (i.e., `k_v = 3`).
4. Therefore, when connecting child `v` to `u`, the best contribution from `v` is `max(dp[v][0], dp[v][3])`.
5. `dp[u][0] = 1` (u is a leaf in the alkane).
6. `dp[u][k]` for `k > 0` is computed by selecting the `k` children with the largest contributions and adding them to 1 (for `u` itself).
7. The final answer is `max(dp[u][4])` over all `u`, since `dp[u][4]` represents an alkane rooted at `u` with degree 4, satisfying the condition of having at least one degree-4 vertex.

Time complexity: O(N log N) due to sorting child values for each node (each node's children are sorted, and the sum of degrees is 2(N-1), so the total sorting cost is bounded). Space complexity: O(N).
