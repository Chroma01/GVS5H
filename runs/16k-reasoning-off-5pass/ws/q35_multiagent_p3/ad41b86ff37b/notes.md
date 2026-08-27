
## ideation
The problem asks us to find the minimum number of vertices to delete from a given tree $T$ so that the remaining graph is a "Snowflake Tree". A Snowflake Tree is defined by parameters $x, y \ge 1$ and consists of:
1. A center vertex.
2. $x$ intermediate vertices connected to the center.
3. $y$ leaf vertices connected to each intermediate vertex.

Total vertices in such a tree: $1 + x + x \cdot y = 1 + x(1+y)$.
We want to maximize the size of the Snowflake Tree subgraph found within $T$, because minimizing deleted vertices is equivalent to maximizing the kept vertices.

Key observations:
1. The structure is rooted at a center $c$.
2. The neighbors of $c$ in the Snowflake Tree are the $x$ intermediate nodes.
3. Each intermediate node $v$ must have at least $y$ leaf neighbors (other than $c$). In the original tree, if $v$ has degree $deg(v)$, it has $deg(v)-1$ neighbors other than $c$. So, $v$ can serve as an intermediate node for a given $y$ if $deg(v) - 1 \ge y$.
4. For a fixed center $c$ and fixed $y$, let $S_{c,y}$ be the set of neighbors $v$ of $c$ such that $deg(v) - 1 \ge y$. Let $k = |S_{c,y}|$. We can choose any $x \le k$ intermediate nodes. To maximize the size $1 + x(1+y)$, we should choose the largest possible $x$, which is $k$. Thus, the max size for fixed $c, y$ is $1 + k(1+y)$.

Algorithm:
1. Compute degrees of all vertices.
2. For each vertex $c$ (potential center):
   a. Collect the values $d_v = deg(v) - 1$ for all neighbors $v$ of $c$.
   b. Sort these values in descending order. Let the sorted list be $L$.
   c. Iterate through possible values of $y$. The maximum possible $y$ for this center is $\max(L)$ (if $L$ is not empty). The minimum is 1.
   d. For a given $y$, the number of qualifying neighbors $k$ is the count of elements in $L$ that are $\ge y$. Since $L$ is sorted descending, this is the largest index $i$ such that $L[i] \ge y$ (0-indexed, so count is $i+1$).
   e. We can optimize the iteration over $y$. Instead of iterating all $y$, we can iterate over the distinct values in $L$ and the ranges between them. Or simply, since we want to maximize $1 + k(1+y)$, and $k$ is a step function of $y$, we can check each "step".
      Specifically, if we pick the $j$-th largest value in $L$ (0-indexed) as the threshold, then for any $y \le L[j]$, we have at least $j+1$ neighbors. To maximize the term for a fixed count $k=j+1$, we should pick the largest possible $y$ such that we still have $k$ neighbors. That largest $y$ is $L[j]$ (assuming distinct values or handling ties carefully). Actually, if we fix the set of $k$ neighbors, the max $y$ is $\min_{v \in \text{set}} (deg(v)-1)$. To maximize $1 + k(1+y)$, for a fixed $k$, we want the largest $y$ such that there are at least $k$ neighbors with $deg(v)-1 \ge y$. This $y$ is exactly the $k$-th largest value in $L$ (1-indexed) or $L[k-1]$ (0-indexed).
      So, for each $k \in \{1, \dots, |L|\}$, let $y_k = L[k-1]$. The size is $1 + k(1 + y_k)$.
      We compute this for all $k$ and take the maximum.
3. The global maximum size over all centers $c$ and all valid $k$ is the answer for kept vertices.
4. Result is $N - \text{max\_size}$.

Complexity:
- Sum of degrees is $2(N-1)$.
- For each node $c$, we sort its neighbor's "leaf capacities". The sum of sizes of these lists is $N-1$ (each edge counted twice, once for each end, but we only process neighbors). Wait, the sum of degrees is $2N-2$. The sum of the lengths of the lists $L_c$ for all $c$ is $\sum_{c} deg(c) = 2N-2$.
- Sorting each list takes $O(deg(c) \log deg(c))$. Total time is $\sum O(deg(c) \log deg(c)) \le O(N \log N)$.
- This is efficient enough for $N \le 3 \times 10^5$.

Pitfalls:
- Ensure $y \ge 1$. If $L$ contains 0, we ignore it or handle it (since $y \ge 1$, a neighbor with $deg(v)-1=0$ can never be an intermediate node).
- Ensure $x \ge 1$. So $k \ge 1$.
- The center itself is always kept.

## worker: (None)
The problem requires finding a subgraph that forms a "Snowflake Tree" with maximum vertices. A Snowflake Tree is defined by a center, $x$ intermediate nodes connected to the center, and $y$ leaves connected to each intermediate node. The total size is $1 + x(1+y)$.

For a fixed center $c$, each neighbor $v$ can serve as an intermediate node if it has at least $y$ leaves attached to it (excluding the edge to $c$). The number of such leaves available in the original tree is $deg(v) - 1$. Let $cap(v) = deg(v) - 1$.

For a fixed center $c$ and a fixed number of intermediate nodes $k$, we want to maximize $y$. To have $k$ intermediate nodes each supporting $y$ leaves, we need to choose $k$ neighbors such that each has $cap(v) \ge y$. To maximize $y$ for a fixed $k$, we should pick the $k$ neighbors with the largest capacities. The limiting factor will be the $k$-th largest capacity among all neighbors. Thus, $y = \text{k-th largest capacity}$.

The algorithm:
1. Compute degrees of all nodes.
2. For each node $c$ considered as center:
   - Collect $cap(v) = deg(v) - 1$ for all neighbors $v$.
   - Filter out capacities $< 1$ (since $y \ge 1$).
   - Sort the capacities in descending order.
   - For each $k$ from $1$ to the number of valid neighbors:
     - $y = \text{sorted\_caps}[k-1]$
     - Current snowflake size $= 1 + k \times (1 + y)$
     - Update global maximum size.
3. The result is $N - \text{max\_snowflake\_size}$.

Complexity:
- Sum of degrees is $2(N-1)$.
- For each node, we sort its neighbor capacities. The sum of the lengths of these lists is $2N-2$.
- Sorting takes $O(D \log D)$ for a node with degree $D$. Total time is $\sum O(deg(c) \log deg(c)) \le O(N \log N)$.
- This fits within the time limits for $N \le 3 \times 10^5$.
