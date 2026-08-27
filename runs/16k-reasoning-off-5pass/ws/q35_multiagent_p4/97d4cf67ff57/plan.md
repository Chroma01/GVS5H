To solve this problem, we need to find the largest subgraph of a given tree that forms an "alkane" graph. An alkane is defined as a tree where every vertex has degree 1 or 4, and at least one vertex has degree 4. Since the subgraph must be a subgraph of the original tree, it must also be a tree.

We can use dynamic programming on trees. For each node `u`, we consider it as a potential "center" (degree 4) or part of the structure. However, a more direct approach is to root the tree arbitrarily and compute DP states for each subtree.

Let's define `dp[u][k]` as the maximum number of vertices in a valid alkane-like structure within the subtree of `u`, where `u` has degree `k` in the subgraph. The possible degrees for any node in an alkane are 1 or 4.
- If `u` is a leaf in the subgraph, its degree is 1.
- If `u` is a degree-4 node in the subgraph, it must have exactly 4 children in the subgraph (since it's a tree, the parent edge accounts for the 4th connection if `u` is not the root, or all 4 are children if `u` is the root).

Actually, a better state definition:
For each node `u`, we compute:
1. `dp1[u]`: The max size of a valid alkane component in `u`'s subtree where `u` has degree 1 in the subgraph (connected to its parent in the full tree context, so it acts as a leaf in the subgraph relative to the subtree, but will connect to parent). This component is essentially a "branch" ending at `u`.
2. `dp4[u]`: The max size of a valid alkane component in `u`'s subtree where `u` has degree 4 in the subgraph. This means `u` is a central node with 4 branches coming from its children.

Transitions:
- To compute `dp1[u]`: `u` connects to exactly one child `v`. The edge `(u,v)` is in the subgraph. `v` must have degree 1 or 4 in its subgraph. If `v` has degree 1, it's a valid end of a branch. If `v` has degree 4, it's a valid center. We take the max over all children `v` of `1 + max(dp1[v], dp4[v])`. Note: `u` itself is included.
- To compute `dp4[u]`: `u` connects to exactly 4 distinct children `v1, v2, v3, v4`. Each `vi` must be the root of a valid branch (degree 1 in subgraph relative to `vi`'s subtree, meaning `vi` connects to `u` and has degree 1 in the subgraph? No, `vi` can have degree 1 or 4 in the subgraph. But since `vi` is connected to `u`, if `vi` has degree 1 in the subgraph, it's a leaf. If `vi` has degree 4, it's a center. So for each child `v`, we can contribute `max(dp1[v], dp4[v])` if we treat the connection `(u,v)` as the single edge for `v`'s component. Wait, if `v` is a center (degree 4), it uses 4 edges in its subtree. The edge `(u,v)` is the 5th? No, in the subgraph, `v`'s degree is determined by edges in the subgraph. If `v` is a center, it has degree 4. One of those edges is `(u,v)`. So `v` needs 3 other children in the subgraph. This matches `dp4[v]` if `dp4[v]` is defined as the max size of a component rooted at `v` where `v` has degree 4 in the subgraph, using edges within the subtree. Yes.
So, `dp4[u]` is the sum of the largest 4 values of `max(dp1[v], dp4[v])` from children `v`, plus 1 (for `u`).

Finally, the answer is the maximum `dp4[u]` over all `u`. If no such structure exists, output -1.

Base case: For a leaf `u`, `dp1[u] = 1` (just the node itself, degree 0 in subtree, but will be degree 1 when connected to parent). `dp4[u] = -infinity` (cannot have degree 4).

Let's refine `dp1[u]`. If `u` is a leaf in the tree, `dp1[u] = 1`. If `u` has children, `dp1[u] = 1 + max(max(dp1[v], dp4[v]) for v in children)`. If no child can form a valid branch, `dp1[u]` might be invalid? Actually, a single node is a valid branch of length 1. So `dp1[u]` is always at least 1.

For `dp4[u]`, we need at least 4 children. If fewer than 4 children, `dp4[u] = -infinity`.