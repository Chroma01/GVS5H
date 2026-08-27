1. **Problem Analysis**: We need to find the largest subgraph of a given tree that forms an "alkane". An alkane is a tree where every vertex has degree 1 or 4, with at least one vertex of degree 4. Since it's a subgraph of a tree, it must also be a tree. The key insight is that in the subgraph, each vertex's degree is either 1 (leaf) or 4 (internal node with 4 children/neighbors in the subgraph).

2. **Dynamic Programming on Trees**: We can use tree DP. For each node, we consider it as part of an alkane structure. The state needs to capture how many "ports" (connections to children in the subgraph) are used. Since the degree in the subgraph must be 1 or 4, and the parent connection counts as 1 if the node is not a root of the alkane component, we need to track the number of children connected in the subgraph.
   - If a node has degree 4 in the subgraph, it can have 4 children connected (if it's a root of the alkane tree) or 3 children connected (if it has a parent in the alkane tree).
   - If a node has degree 1 in the subgraph, it can have 0 children connected (if it's a leaf in the alkane tree) or 1 child connected (if it has a parent).

3. **DP State Definition**: For each node `u`, we compute DP states representing the maximum size of an alkane-like subtree rooted at `u` with a specific number of "open ports" to children. Let `dp[u][k]` be the max vertices in a valid partial structure at `u` with `k` children connected, where `k` can be 0, 1, 2, 3, 4. However, not all `k` are valid final states. 
   - A node with 4 children connected is valid as an internal node (degree 4).
   - A node with 0 children connected is valid as a leaf (degree 1, assuming it connects to parent).
   - A node with 1 child connected is valid if it connects to parent (degree 2? No, degree must be 1 or 4). Wait, if it connects to parent and 1 child, degree is 2, which is invalid. So `k=1` is only valid if the node is a root of the alkane and has degree 1? But an alkane must have at least one degree 4 node. A single node with degree 1 is not an alkane.
   - Actually, let's redefine: We build the alkane from the bottom up. Each node can be:
     - A leaf in the alkane: contributes 1 vertex, has 0 children in alkane.
     - An internal node in the alkane: must have exactly 4 children in the alkane (if it's a root of the alkane component) or 3 children in the alkane (if it has a parent).
   - So for each node, we compute the max size of a subtree where the node has `c` children selected to be part of the alkane structure. The node itself is included.
   - `dp[u][c]` = max vertices in the alkane-subtree rooted at `u` with `c` children connected.
   - Valid `c` values: 0, 1, 2, 3, 4. But we only care about configurations that can eventually form a valid alkane.
   - A node with `c=4` is a valid internal node (degree 4).
   - A node with `c=0` is a valid leaf (degree 1 if connected to parent).
   - `c=1,2,3` are intermediate states. A node with `c=3` can connect to a parent to become degree 4. A node with `c=0` can connect to a parent to become degree 1. `c=1,2` cannot form a valid degree (1 or 4) even with a parent (would be 2 or 3). So we can discard `c=1,2` as final states for a node that is not passing up a valid configuration? No, they might be needed to combine? No, because if a node has 1 or 2 children in the alkane, and we add a parent, the degree becomes 2 or 3, which is invalid. So `dp[u][1]` and `dp[u][2]` are essentially useless for forming a valid alkane unless the node is a root? If root, degree 1 or 2. Degree 1 is valid for a single node, but we need a degree 4 node. So a root with `c=1` (degree 1) is not an alkane by itself. It must be part of a larger structure. But if it's a root of the entire alkane, it must have degree 1 or 4. If degree 1, it's a leaf, so `c=0`. If degree 4, `c=4`. So `c=1,2` are never valid final states for any node in the alkane.

4. **Algorithm**:
   - For each node `u`, compute `dp[u][0..4]`.
   - `dp[u][0] = 1` (just the node itself, no children).
   - To compute `dp[u][c]` for `c > 0`, we choose `c` children to connect. For each child `v`, we can either not connect (contribute 0) or connect (contribute `dp[v][0]` because the child becomes a leaf in the alkane, so it has 0 children in the alkane). Wait, if we connect `v` to `u`, then `v`'s degree in the alkane is 1 (only connected to `u`), so `v` must have `dp[v][0]` structure.
   - So for each child, the gain from connecting is `dp[v][0]`. If we don't connect, gain is 0.
   - To get `dp[u][c]`, we pick the `c` children with the largest `dp[v][0]` values and sum them up, plus 1 (for `u`).
   - `dp[u][c] = 1 + sum of top c dp[v][0] values`.
   - After computing all `dp[u][c]`, we check for valid alkane structures:
     - An alkane can be rooted at a node `r` with `c=4` (degree 4). The size is `dp[r][4]`. This is a valid alkane if it contains at least one degree 4 node. Since `r` has degree 4, it is valid.
     - We also need to consider that the alkane might not be "rooted" at a degree 4 node in our DP sense? No, every alkane has at least one degree 4 node. We can root the alkane at a degree 4 node.
     - So the answer is the maximum `dp[r][4]` over all nodes `r`.
     - If no node has `dp[r][4]` (i.e., fewer than 4 children or not enough valid subtrees), then output -1.

5. **Refinement**: 
   - `dp[u][0] = 1`.
   - For `c = 1 to 4`: `dp[u][c] = 1 + sum of largest c values of {dp[v][0] for v in children(u)}`. If fewer than `c` children, `dp[u][c] = -infinity`.
   - The answer is `max(dp[r][4] for all r)`. If max is -infinity, output -1.