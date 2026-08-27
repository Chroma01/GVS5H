
## ideation
The problem asks for the minimum number of vertices to delete to leave a "Snowflake Tree". A Snowflake Tree is defined by a center node connected to $x$ intermediate nodes, where each intermediate node is connected to $y$ leaf nodes. $x, y \ge 1$.
The structure implies:
1. Center node $C$.
2. $x$ neighbors of $C$, say $I_1, \dots, I_x$, are intermediate nodes.
3. Each $I_j$ has exactly $y$ leaf neighbors.
4. No other nodes exist in the remaining tree.

Key observations:
- An intermediate node $I$ in the original tree must have degree $y+1$ in the Snowflake Tree (1 edge to center, $y$ edges to leaves).
- In the original tree, if $I$ is to be an intermediate node for a specific $y$, it must have exactly $y$ leaf neighbors and exactly 1 non-leaf neighbor (which will be the center $C$).
- If a node $v$ has exactly $y$ leaf neighbors and exactly 1 non-leaf neighbor $u$, then $v$ can serve as an intermediate node for center $u$ with parameter $y$.
- For a fixed center $C$ and fixed parameter $y$, the number of kept nodes is $1 + x(1+y)$, where $x$ is the number of valid intermediate nodes connected to $C$ with parameter $y$.
- To minimize deletions, we maximize kept nodes. Thus, for a fixed $C$ and $y$, we should take all valid intermediate nodes connected to $C$.
- Algorithm:
  1. Identify all leaf nodes.
  2. For each node $v$, count its leaf neighbors ($L_v$) and non-leaf neighbors ($N_v$).
  3. If $|N_v| == 1$ and $|L_v| = y \ge 1$, then $v$ is a candidate intermediate node for its unique non-leaf neighbor $u$ with parameter $y$.
  4. We can aggregate these candidates. For each non-leaf node $u$, and for each possible $y$, count how many neighbors $v$ satisfy the condition. Let this count be $x_{u,y}$.
  5. The max kept nodes for center $u$ and parameter $y$ is $1 + x_{u,y}(1+y)$.
  6. Iterate over all non-leaf nodes $u$ (potential centers) and all possible $y$ values to find the global maximum kept nodes.
  7. Result is $N - \text{max\_kept}$.

Complexity:
- Counting leaf/non-leaf neighbors for each node takes $O(N)$.
- Grouping candidates by $(u, y)$ can be done by iterating over all nodes $v$ that are candidates. For each such $v$, we identify $u$ and $y$, and increment a counter for $(u, y)$.
- The number of such candidates is at most $N$.
- The possible values of $y$ are up to $N$. We can use a hash map or a 2D array (if memory permits, but $N^2$ is too big) or a dictionary of dictionaries. Since the total number of candidate entries is $O(N)$, the aggregation is efficient.
- Finally, iterate over the aggregated counts to find the max.

Pitfalls:
- $y$ must be positive.
- Center must have at least one intermediate node ($x \ge 1$).
- Ensure we only consider non-leaf nodes as potential centers? Actually, a leaf cannot be a center because it has no non-leaf neighbors to serve as intermediates (unless $N=1$, but $N \ge 3$ and $x,y \ge 1$ implies min nodes $1+1+1=3$). If a node is a leaf, it has 0 non-leaf neighbors, so it can't be a center.
- The "non-leaf neighbor" check must be robust. A node might have multiple non-leaf neighbors, in which case it can't be an intermediate node for any single center.

## worker: (None)
The problem asks for the minimum number of vertices to delete to leave a "Snowflake Tree". A Snowflake Tree is defined by a center node connected to `x` intermediate nodes, where each intermediate node is connected to `y` leaf nodes. `x, y >= 1`.

The key insight is that for a fixed center `C` and fixed parameter `y`, each neighbor `v` of `C` can independently be chosen as an intermediate node if it has at least `y` other neighbors (which will become its leaves). If `v` is chosen as an intermediate node with parameter `y`, we keep `v` and `y` of its other neighbors, and delete the remaining `deg(v) - 1 - y` neighbors. If `v` is not chosen, we delete `v` and all its other neighbors.

To minimize deletions (maximize kept nodes), for a fixed `C` and `y`, we should choose all neighbors `v` with `deg(v) - 1 >= y` as intermediate nodes. The number of kept nodes is `1 + x * (1 + y)`, where `x` is the count of such neighbors.

Since `x` is a non-increasing function of `y`, and the kept nodes function `1 + x * (1 + y)` is increasing in `y` for a fixed `x`, the maximum for a given `x` is achieved at the largest possible `y` for that `x`. This occurs when `y` is equal to one of the `deg(v) - 1` values.

Thus, for each center `C`, we collect `k_v = deg(v) - 1` for all neighbors `v`. We sort these values in descending order. For each value `k` in this sorted list, we consider `y = k`. The number of intermediates `x` is the number of neighbors with `k_v >= k`. We calculate the kept nodes and update the global maximum.

The complexity is dominated by sorting the neighbor degrees for each node, which sums to `O(N log N)` over all nodes.
