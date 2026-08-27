
## ideation
The problem asks for the maximum size of a subgraph of a given tree that forms an "alkane". An alkane is defined as a tree where every vertex has degree 1 or 4, and at least one vertex has degree 4.

Key observations:
1. **Subgraph Structure**: Since the original graph is a tree, any connected subgraph is also a tree. The problem implies we are looking for a connected subgraph (as "alkane" is a specific type of tree structure, typically connected). If disconnected components were allowed, we could just pick disjoint stars, but the definition "A graph is defined to be an alkane if... it is an undirected tree" implies connectivity.
2. **Degree Constraints**: In the subgraph, every node must have degree 1 or 4.
   - Leaves in the subgraph have degree 1.
   - Internal nodes in the subgraph have degree 4.
3. **Dynamic Programming on Trees**: We can root the original tree arbitrarily (e.g., at vertex 1) and use DP.
   - For each node `u`, we compute `dp[u][k][has4]`, which represents the maximum number of vertices in the subtree rooted at `u` such that:
     - `u` has exactly `k` children connected to it in the subgraph.
     - `has4` is a boolean indicating whether there is at least one vertex of degree 4 in the subtree (including `u`'s descendants). Note: `u`'s total degree in the subgraph will be `k` (if `u` is the root of the alkane) or `k+1` (if `u` has a parent in the subgraph).
   - The state `k` can range from 0 to 4 because `u` can have at most 4 connections in the subgraph (degree constraint). If `u` needs degree 4, it must connect to 4 children (if root) or 3 children + 1 parent. If `u` needs degree 1, it connects to 0 children (if root/leaf) or 1 child + 1 parent? No, if `u` is internal, it must have degree 4. If `u` is a leaf in the subgraph, it has degree 1.
   
   Let's refine the state and transitions:
   - `dp[u][k][h]`: Max vertices in `u`'s subtree, `u` has `k` selected children, `h` indicates if a degree-4 node exists in the subtree.
   - Base case: Leaf `u`.
     - `dp[u][0][0] = 1` (u is a leaf in subgraph, degree 1, no degree-4 node).
     - All other `dp[u][k][h] = -infinity`.
   - Recursive step:
     - For each child `v`, we decide whether to include it in the subgraph.
     - If we include `v`, the edge `(u,v)` is present. `v`'s degree in the subgraph will be `1 + (number of v's selected children)`.
     - `v` must satisfy the degree constraint: degree 1 or 4.
       - If `v`'s degree is 1, it must have 0 selected children. We look at `dp[v][0][0]` and `dp[v][0][1]`.
       - If `v`'s degree is 4, it must have 3 selected children. We look at `dp[v][3][1]` (since `v` itself is degree 4, `has4` must be true). `dp[v][3][0]` is invalid because `v` has degree 4, so `has4` must be 1.
     - So, for each child `v`, the possible contributions to `u`'s state are:
       - Exclude `v`: gain 0, `has4` unchanged.
       - Include `v` as degree 1: gain `dp[v][0][h_v]`, new `has4` is `h_u OR h_v`.
       - Include `v` as degree 4: gain `dp[v][3][1]`, new `has4` is `h_u OR 1 = 1`.
     - We need to select `k` children to include. This is a variation of the knapsack problem or simply picking the best `k` children. Since `k` is small (0-4), we can merge children one by one.
     - For each child, we compute the best gain for including it with `has4=0` or `has4=1`.
       - `gain_no4[v] = dp[v][0][0]` (if valid)
       - `gain_with4[v] = max(dp[v][0][1], dp[v][3][1])` (if valid)
     - Then, for node `u`, we iterate through children and update `dp[u][k][h]`.
   
   - Final Answer:
     - After computing DP for the root `r`, the root has no parent. So its degree in the subgraph is exactly `k`.
     - Valid roots must have degree 1 or 4.
     - Also, the entire subgraph must have at least one degree-4 node.
     - Answer is `max(dp[r][1][1], dp[r][4][1])`.
     - If both are `-infinity`, output `-1`.

Pitfalls:
- Invalid states should be initialized to a very small number (e.g., -1e9) to avoid being selected.
- Ensure that when `v` is included as degree 4, we only consider `dp[v][3][1]`.
- Ensure that when `v` is included as degree 1, we consider both `dp[v][0][0]` and `dp[v][0][1]`.
- The merging process must correctly handle the `has4` flag (logical OR).

Complexity:
- Each node processes its children. For each child, we do constant work (merging states of size 5x2).
- Total time complexity is O(N).

## worker: Implement tree DP with state `dp[u][k][has4]` wher
The solution uses dynamic programming on trees. We root the tree at vertex 1 and process nodes in bottom-up order.
For each node `u`, we compute `dp[u][k][h]`, where:
- `k` is the number of children of `u` included in the subgraph (0 to 4).
- `h` is a boolean flag (0 or 1) indicating whether there is at least one vertex of degree 4 in the subtree rooted at `u`.
- The value is the maximum number of vertices in such a valid subgraph configuration.

Transitions:
1. **Base Case**: For a leaf `u`, `dp[u][0][0] = 1` (the node itself, degree 1 in subgraph, no degree-4 node). All other states are `-infinity`.
2. **Recursive Step**: For a non-leaf `u`, we consider each child `v`.
   - If `v` is not included, it contributes 0.
   - If `v` is included, it must satisfy the degree constraint in the subgraph. Since `v` is connected to `u`, `v`'s degree is `1 + (number of v's selected children)`.
     - If `v`'s degree is 1, it must have 0 selected children. We take `max(dp[v][0][0], dp[v][0][1])`.
     - If `v`'s degree is 4, it must have 3 selected children. We take `dp[v][3][1]` (since `v` itself is degree 4, `h` must be 1).
   - We merge these choices for all children using a knapsack-like approach, updating `dp[u][k][h]` for `k` from 0 to 4.

Final Answer:
- The root `1` has no parent, so its degree in the subgraph is exactly `k`.
- We check `dp[1][1][1]` (root degree 1, has degree-4 node) and `dp[1][4][1]` (root degree 4, has degree-4 node).
- The maximum of these valid states is the answer. If no valid state exists, output -1.

Complexity: O(N) time and space, as each node processes a constant number of states (5x2) for each child.
