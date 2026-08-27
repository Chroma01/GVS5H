We need to find a connected subgraph (a tree) of the given tree T where all non-leaf nodes have degree exactly 4, leaves have degree 1, and at least one node has degree 4. This is a classic tree DP problem solved by rooting T and computing DP states for each node.

For each node u, we compute DP values based on the number of "occupied" child edges (edges included in the subgraph) that lead to a valid alkane subtree. Let deg(u) be the number of children of u in the rooted tree.

- `dp0[u]`: the maximum size of a valid alkane subtree within u's subtree, where the edge from u to its parent is NOT included (so u cannot be a degree-4 hub, and u may or may not be present).
- `dp1[u]`: the maximum size where the edge (parent, u) IS included, meaning u is present in the subgraph and acts as a leaf in the upward direction (so within its own subtree, u can only have 0 or 3 occupied child edges; if it has 0 child edges, it remains a leaf; if it has 3 child edges, u becomes a degree-4 node).
- `dp2[u]`: the maximum size where u is present, the parent edge is included, and u is an internal node of degree 4, meaning exactly 3 of its child edges must be included.

We use a greedy knapsack-style selection: sort children's dp1 values and take the best 3 for dp2, and best 1 for dp1. Base cases: leaf node (no children) gives dp0=0, dp1=1, dp2=-inf.

After computing DP for the root, the answer is the maximum of dp0[root] and dp1[root] (and dp2[root] if needed), with the constraint that we need at least one node of degree 4. A final `add` flag tracks whether at least one degree-4 node exists in the chosen subtree, and we only accept solutions where the total size ≥ 5 (minimum alkane: 1 hub + 4 leaves).