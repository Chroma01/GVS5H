To solve this problem, we need to find the largest subgraph of a given tree T that satisfies the "alkane" properties: it must be a tree, every vertex must have degree 1 or 4, and at least one vertex must have degree 4. Since the subgraph must be a subgraph of a tree, it is itself a tree. The key insight is that any such alkane subgraph is rooted at a "center" vertex (which will have degree 4 in the subgraph) and consists of 4 disjoint branches extending from it. Each branch is a path or a subtree where internal nodes have degree 3 in the original tree's context but map to degree 1 or 3 in the subgraph structure? No, in the subgraph, every node must have degree 1 or 4. The center has degree 4. The neighbors of the center in the subgraph must have degree 1 or 4. If a neighbor has degree 4, it becomes another center? No, the definition says "at least one vertex of degree 4". It doesn't restrict others. However, if we have multiple degree-4 nodes, they must be connected.

Actually, a simpler dynamic programming approach on trees works. For each vertex `u`, we can compute the maximum size of an alkane-like structure rooted at `u` where `u` has a specific degree in the subgraph. However, the constraint is global: degrees must be 1 or 4.
Let's define `dp[u][d]` as the maximum number of vertices in a subtree rooted at `u` (in the original tree, rooted arbitrarily, say at 1) such that `u` has degree `d` in the subgraph, and all other nodes in the subtree have degree 1 or 4 (except `u` which might have degree < 4 if it's not the final root, or exactly 4 if it is).
Wait, the subgraph doesn't have to be a "rooted subtree" in the traditional sense. But we can root the original tree at vertex 1 and use DP.
For a vertex `u`, in the subgraph, its degree comes from its parent (0 or 1 edge) and its children (0 to 4 edges).
Let `f[u][k]` be the max vertices in the subtree of `u` where `u` has `k` children selected in the subgraph. The total degree of `u` in the subgraph will be `k` (if no parent edge) or `k+1` (if parent edge).
The condition is that every node in the subgraph must have degree 1 or 4.
So, for any node `v` in the subgraph:
- If `v` is a leaf in the subgraph, degree is 1.
- If `v` is internal, degree is 4.

This implies that any node with degree 4 in the subgraph must have exactly 4 neighbors in the subgraph.
We can compute for each node `u` and for each possible number of selected children `k` (0 to 4), the maximum size of the valid configuration in the subtree, ensuring that all nodes *below* `u` satisfy the degree constraint. For `u` itself, we don't enforce the degree constraint yet, or we enforce it conditionally.

Let `dp[u][k]` = max vertices in the subtree rooted at `u` such that `u` has exactly `k` children connected in the subgraph, and all nodes in the subtree (including `u`'s descendants) satisfy the degree constraint (degree 1 or 4), EXCEPT possibly `u` whose final degree depends on its parent.
Actually, if `u` has `k` children selected, and we assume `u` is NOT the root of the alkane (or even if it is), `u`'s degree in the subgraph is `k` (if no parent) or `k+1` (if parent).
If `u` is not the root of the alkane, it must eventually have degree 1 or 4.
If `u` is a leaf in the subgraph, `k=0` and no parent -> degree 1. Valid.
If `u` is internal, it needs degree 4.

Let's refine:
`dp[u][k]`: Maximum number of vertices in the subtree of `u` (in the rooted original tree) such that:
1. `u` has exactly `k` children connected to it in the subgraph.
2. All nodes in the subtree of `u` (descendants) satisfy the degree constraint (degree 1 or 4 in the subgraph).
3. `u`'s degree in the subgraph is currently `k` (pending parent connection).

Base case: Leaf `u`.
`dp[u][0] = 1` (u is a leaf in subgraph, degree 1).
`dp[u][k] = -inf` for k > 0.

Recursive step for non-leaf `u`:
We need to choose `k` children to connect to. For each child `v`, we can either:
- Not connect: contributes 0 to `u`'s degree, and `v` must be the root of a valid alkane-like structure where `v` has degree 1 or 4? No. If we don't connect `u` to `v`, then `v` is the root of a separate component in the subtree? No, the subgraph must be connected? "A subgraph... is an alkane". An alkane is a tree. So the subgraph must be connected.
Therefore, if we select a child `v` to be connected to `u`, `v` becomes part of the same component. If we don't select `v`, `v` cannot be in the subgraph at all? Or can `v` be in a different branch? No, if `v` is in the subgraph, it must be connected to `u` or its descendants. Since it's a tree, the path to `u` is unique. So if `v` is in the subgraph, the edge `(u,v)` MUST be in the subgraph.
Thus, for each child `v`, we have two choices:
1. `v` is NOT in the subgraph. Contribution 0.
2. `v` IS in the subgraph. Then edge `(u,v)` is present. `v` will have degree `d_v` in the subgraph. Since `v` is a child, it has one parent (`u`) in the subgraph. So `v` needs `d_v - 1` children connected.
   For `v` to be valid, its total degree must be 1 or 4.
   - If `v`'s total degree is 1, then it has 0 children connected. This means `v` is a leaf in the subgraph. In this case, we take `dp[v][0]`.
   - If `v`'s total degree is 4, then it has 3 children connected. In this case, we take `dp[v][3]`.
   
   So, for each child `v`, the "gain" if we include `v` is `max(dp[v][0], dp[v][3])`. Let this be `val[v]`. If `dp[v][0]` or `dp[v][3]` is invalid (-inf), we can't take that option.

Now, for node `u`, we want to compute `dp[u][k]` for `k` in 0..4.
`dp[u][k]` is the sum of `val[v]` for `k` chosen children, plus 1 (for `u` itself).
We need to pick the `k` children with the largest `val[v]`.
So, `dp[u][k] = 1 + sum of k largest val[v]`.
If we can't pick `k` children (e.g., not enough children or some vals are -inf), then `dp[u][k] = -inf`.

After computing `dp[u][k]` for all `u`, we check the root of the entire tree (say vertex 1).
For the root, it has no parent. So its degree in the subgraph is exactly `k`.
The root must have degree 1 or 4.
So the answer is `max(dp[1][1], dp[1][4])`.
However, the problem requires "at least one vertex of degree 4".
If the max comes from `dp[1][1]`, we must ensure that somewhere in the tree, there is a node with degree 4.
If the max comes from `dp[1][4]`, the root has degree 4, so the condition is satisfied.
If `dp[1][1]` is the global maximum, we need to check if there exists a valid alkane of that size with a degree-4 node elsewhere.
This suggests we need to track whether a degree-4 node exists in the subtree.

Revised DP state:
`dp[u][k][has4]`: Max vertices in subtree of `u` with `u` having `k` children connected, and `has4` is boolean indicating if any node in the subtree has degree 4 in the subgraph.
`k` in 0..4, `has4` in {0, 1}.

Transitions:
For each child `v`, we can include it if we take `max(dp[v][0][0], dp[v][0][1], dp[v][3][0], dp[v][3][1])`.
Wait, if we include `v`, `v`'s degree is `0+1=1` or `3+1=4`.
- If we take `dp[v][0][...]`, `v` has degree 1. `v` does not contribute a degree-4 node itself, but the subtree might have one (`has4` from child).
- If we take `dp[v][3][...]`, `v` has degree 4. So `has4` becomes 1 for this branch.

Let `best[v][deg_v]` = max over `h` of `dp[v][deg_v][h]`.
Actually, we need to know if `has4` is true.
Let `inc[v]` be a pair `(max_val_with_4, max_val_without_4)` for including `v`.
- Option 1: `v` has degree 1 in subgraph. We use `dp[v][0][0]` and `dp[v][0][1]`.
  - `val0_no4 = dp[v][0][0]`
  - `val0_with4 = dp[v][0][1]`
- Option 2: `v` has degree 4 in subgraph. We use `dp[v][3][0]` and `dp[v][3][1]`.
  - `val3_no4 = dp[v][3][0]` (Invalid if no 4 in subtree, but v itself is 4, so this state is contradictory? No, `dp[v][3][0]` means v has 3 children, total degree 4, but `has4` flag is 0. This is impossible because v has degree 4. So `dp[v][3][0]` should be -inf. `dp[v][3][1]` is valid.)
  - So if we pick degree 4 for v, the resulting `has4` for the branch is 1.
  - `val3_with4 = dp[v][3][1]`

So for each child `v`, we have two choices:
1. Don't include `v`: contribution 0, has4=0.
2. Include `v`:
   - Sub-choice 2a: `v` degree 1. Gain `dp[v][0][1]` (has4=1) or `dp[v][0][0]` (has4=0).
   - Sub-choice 2b: `v` degree 4. Gain `dp[v][3][1]` (has4=1). Note `dp[v][3][0]` is invalid.

We need to select `k` children to include. This is a knapsack-like selection.
For each child, we have options:
- Exclude: (0, 0)
- Include deg 1, no 4: (dp[v][0][0], 0)
- Include deg 1, has 4: (dp[v][0][1], 1)
- Include deg 4, has 4: (dp[v][3][1], 1)

We combine these for all children to compute `dp[u][k][h]`.
Since N is 2e5, we need an efficient merge. For each node, we merge children one by one. The state size is small (k=0..4, h=0..1). Merging two states takes constant time. Total time O(N).

Finally, for the root `r`:
Answer is `max(dp[r][1][1], dp[r][4][1])`.
If both are -inf, output -1.