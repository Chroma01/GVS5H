
## ideation
**Core Difficulty:**
The problem asks for the minimum number of vertices to delete to leave a "Snowflake Tree". A Snowflake Tree has a very specific structure:
1. A central root (Step 2).
2. Exactly $x$ neighbors of the root (Step 3).
3. Each of those $x$ neighbors must have exactly $y$ leaf children attached (Step 4).
4. The total number of vertices in such a tree is $1 + x + x \cdot y$.

The constraints are $N \le 3 \times 10^5$, so an $O(N^2)$ solution is too slow. We need something close to $O(N)$.

**Candidate Approaches:**
1.  **Iterate over the Root:** Since the structure is defined by a unique root (the node with degree $x$ in the subgraph, or degree $x$ in the original tree if we keep all its neighbors), we can iterate through every vertex $r$ in the original tree and assume it is the root of our Snowflake Tree.
2.  **Analyze Neighbors:** For a fixed root $r$, let its neighbors in the original tree be $v_1, v_2, \dots, v_k$.
    *   To form a Snowflake Tree with root $r$, we must select a subset of these neighbors to be the "intermediate" nodes (the $x$ nodes). Let the size of this subset be $x$.
    *   For each selected intermediate node $v_i$, we must keep exactly $y$ of its neighbors (excluding $r$) as leaves, and delete all others.
    *   Nodes that are not selected as intermediate nodes must be deleted entirely (along with their subtrees).
    *   Nodes that are leaves attached to intermediate nodes but exceed the count $y$ must be deleted.
3.  **Optimization per Root:**
    *   For a fixed root $r$ and a fixed number of leaves $y$, the cost calculation is straightforward:
        *   Cost = (Total nodes) - (Nodes kept).
        *   Nodes kept = $1$ (root) + $x$ (intermediates) + $x \cdot y$ (leaves).
        *   However, we don't know $x$ and $y$ beforehand.
    *   Actually, the problem says "Choose positive integers x, y". So for a fixed root $r$, we need to find the pair $(x, y)$ that maximizes the number of kept nodes.
    *   For a specific neighbor $v$ of $r$, let $deg(v)$ be its degree in the original tree. If we choose $v$ as an intermediate node, we can keep at most $deg(v) - 1$ leaves (since one edge goes to $r$). To be a valid intermediate node for a specific $y$, we must have $deg(v) - 1 \ge y$. If we choose $v$, we contribute $1 + y$ kept nodes.
    *   Wait, the definition says "attach y leaves". It implies we *must* attach exactly $y$. If a neighbor $v$ has $d' = deg(v)-1$ available neighbors, and we pick it as an intermediate node, we can keep $\min(d', y)$? No, the definition says "attach y leaves". This usually means the resulting structure must have exactly $y$ leaves attached. If $d' < y$, we can't form a valid intermediate node for that $y$ (unless we delete nodes to reduce degree? No, we delete vertices to *form* the tree. We can't add edges. We can only keep a subset of existing edges).
    *   Re-reading: "attach y leaves to it". In the context of deleting vertices, if we select $v$ as an intermediate node, we must select exactly $y$ of its neighbors (excluding $r$) to be leaves in the final tree. If $v$ has fewer than $y$ neighbors available, we cannot make $v$ an intermediate node for that $y$.
    *   So, for a fixed root $r$ and fixed $y$:
        *   Identify all neighbors $v$ of $r$ such that $deg(v) - 1 \ge y$.
        *   Let $S_y$ be the count of such neighbors.
        *   We can choose any $x$ from $1$ to $S_y$. To maximize kept nodes, we should choose $x = S_y$ (since adding an intermediate node adds $1+y$ nodes, which is positive).
        *   Max kept nodes for fixed $r, y$ = $1 + S_y + S_y \cdot y = 1 + S_y(1+y)$.
    *   We need to maximize this over all possible $y$.
    *   What is the range of $y$? $y$ can be from $1$ up to $\max(deg(v)-1)$. Since $N$ is large, we can't iterate all $y$ naively for each root if the check is slow.
    *   However, notice that $S_y$ is a non-increasing function of $y$. Specifically, $S_y$ is the number of neighbors with degree $\ge y+1$.
    *   We can precompute the degrees of all neighbors for a root $r$. Sort them. Then for each unique degree value present, we can calculate the potential $S_y$.
    *   Actually, simpler: For a fixed root $r$, collect the degrees of all its neighbors: $d_1, d_2, \dots, d_k$.
    *   For a chosen $y$, $S_y = \text{count}(d_i \ge y+1)$.
    *   We want to maximize $1 + S_y(1+y)$.
    *   Since $S_y$ changes only at values $y = d_i - 1$, we only need to check $y \in \{1, 2, \dots, \max(d_i)-1\}$. But checking every $y$ is still potentially $O(N)$ per root, leading to $O(N^2)$.
    *   Optimization: Sort the neighbor degrees for root $r$. Let sorted degrees be $D_1 \le D_2 \le \dots \le D_k$.
    *   If we pick $y$, then $S_y$ is the number of $D_i \ge y+1$. This is equivalent to finding the largest index $j$ such that $D_j \ge y+1$, so $S_y = k - j + 1$.
    *   We want to maximize $(k - j + 1)(y+1) + 1$.
    *   Note that if we choose $y = D_j - 1$, then the count of neighbors with degree $\ge y+1$ is at least $j$ (since $D_j \ge D_j$). Actually, if we set $y = D_j - 1$, then any neighbor with degree $\ge D_j$ works.
    *   Let's refine: For a sorted list of degrees $D_1 \le \dots \le D_k$.
    *   Consider choosing $y$ such that exactly $j$ neighbors satisfy the condition (i.e., we pick the $j$ neighbors with the largest degrees). Then we must have $y \le D_j - 1$ (to include the $j$-th largest) and $y > D_{j-1} - 1$ (to exclude the $(j-1)$-th largest, if we want exactly $j$).
    *   To maximize $(j)(y+1)$, given $j$ fixed, we should pick the largest possible $y$, which is $D_j - 1$.
    *   So for each $j \in \{1, \dots, k\}$, the best $y$ to include exactly $j$ neighbors (the ones with largest degrees) is $y = D_j - 1$.
    *   The score for this $j$ is $1 + j \cdot (1 + (D_j - 1)) = 1 + j \cdot D_j$.
    *   We just need to iterate $j$ from $1$ to $k$, calculate $1 + j \cdot D_j$, and take the maximum.
    *   This reduces the check for one root to $O(\text{deg}(r) \log (\text{deg}(r)))$ due to sorting.
    *   Sum of degrees is $2(N-1)$, so total time complexity is $\sum \text{deg}(r) \log \text{deg}(r)$, which is bounded by $O(N \log N)$. This fits within the time limit.

**Pitfalls:**
1.  **Degree definition**: The degree of a neighbor $v$ in the context of being a leaf-attacher is its degree in the original tree minus 1 (the edge to root). My logic above used $D_j$ as the original degree. Let's verify:
    *   If neighbor $v$ has original degree $d$, it has $d-1$ other neighbors.
    *   We need $y$ leaves. So we need $d-1 \ge y \implies y \le d-1$.
    *   If we fix $j$ neighbors (the ones with largest original degrees), and set $y = D_j - 1$, then for the $j$-th neighbor, $y = D_j - 1$, which satisfies $D_j - 1 \le D_j - 1$. For the $(j-1)$-th neighbor (smaller degree), $D_{j-1} < D_j \implies D_{j-1} - 1 < y$, so it fails. Correct.
    *   The number of kept nodes is $1$ (root) + $j$ (intermediates) + $j \cdot y$ (leaves).
    *   Substitute $y = D_j - 1$: $1 + j + j(D_j - 1) = 1 + j + j D_j - j = 1 + j D_j$.
    *   Wait, is it possible that a smaller $y$ allows more neighbors?
        *   Suppose we have degrees 2, 2, 2. $k=3$.
        *   $j=1$: $y = 2-1=1$. Score $1 + 1\cdot 2 = 3$. (Root + 1 int + 1 leaf).
        *   $j=2$: $y = 2-1=1$. Score $1 + 2\cdot 2 = 5$. (Root + 2 int + 2 leaves).
        *   $j=3$: $y = 2-1=1$. Score $1 + 3\cdot 2 = 7$.
        *   What if we chose $y=0$? Not allowed ($y$ positive integer).
        *   What if degrees are 3, 3, 3?
        *   $j=1, y=2 \to 1+3=4$.
        *   $j=2, y=2 \to 1+6=7$.
        *   $j=3, y=2 \to 1+9=10$.
        *   Seems correct. The function $f(j) = 1 + j \cdot D_j$ (where $D_j$ is the $j$-th largest degree) is what we maximize.
2.  **Edge cases**: $N=3$, line graph. Root in middle, neighbors degree 2. $D_1=2, D_2=2$.
    *   $j=1, y=1 \to 1+2=3$.
    *   $j=2, y=1 \to 1+4=5$. Wait, $N=3$, max nodes 3.
    *   Ah, $D_j$ is the original degree. If root is center of 1-2-3, root is 2. Neighbors 1 and 3.
    *   Deg(1)=1, Deg(3)=1. Sorted: 1, 1.
    *   $j=1, D_1=1 \to y=0$ (invalid).
    *   So we must ensure $y \ge 1$. Thus we only consider $j$ where $D_j \ge 2$.
    *   In sample 2: 1-2-3. Root 2. Neighbors 1, 3. Degrees 1, 1. No neighbor has degree $\ge 2$. So no valid $y \ge 1$.
    *   But Sample 2 output is 0. "Snowflake Tree with x=1, y=1".
    *   Let's re-read the definition carefully.
    *   "Prepare x more vertices... attach y leaves".
    *   If $x=1, y=1$: Root -> 1 intermediate. Intermediate -> 1 leaf. Total 3 nodes.
    *   In 1-2-3, if root is 1? Neighbors: 2. Deg(2)=2.
    *   $j=1, D_1=2 \to y=1$. Score $1 + 1\cdot 2 = 3$. Correct.
    *   So we must iterate all vertices as potential roots.
    *   If a vertex has no neighbors with degree $\ge 2$, it can't be a root for $y \ge 1$. But maybe it can be a leaf? No, the root is the unique node with degree $x$ in the Snowflake structure.
    *   Wait, if $x=1, y=1$, the root has degree 1. The intermediate has degree 2.
    *   My logic assumes the root is the center.
    *   In 1-2-3, if we pick 2 as root: Neighbors 1, 3. Degrees 1, 1. Max $y$ possible is 0. Invalid.
    *   If we pick 1 as root: Neighbor 2. Degree 2. $j=1, D_1=2 \to y=1$. Valid. Kept = 3. Deleted = 0.
    *   So the algorithm must try every node as root.
3.  **Data Structures**: Adjacency list. Sorting degrees for each node.
4.  **Constraints**: $N$ up to $3 \times 10^5$. Python might be slow if not careful with I/O and loops. Use `sys.stdin.read`.

**Algorithm Steps:**
1. Read input, build adjacency list.
2. Compute degree of each node.
3. Initialize `max_kept = 0`.
4. For each node `u` from 1 to N:
    a. Get list of neighbors `adj[u]`.
    b. Get degrees of these neighbors: `degrees = [deg[v] for v in adj[u]]`.
    c. Sort `degrees` in descending order.
    d. Iterate `j` from 1 to `len(degrees)`:
        i. `d_val = degrees[j-1]`
        ii. If `d_val < 2`: break (since $y$ must be $\ge 1$, we need $d\_val - 1 \ge 1 \implies d\_val \ge 2$).
        iii. `kept = 1 + j * d_val`
        iv. `max_kept = max(max_kept, kept)`
5. Result is `N - max_kept`.

Wait, is it possible that for a fixed $j$, picking a smaller $y$ is better?
Score = $1 + j(1+y)$. Since $j \ge 1$ and $y \ge 1$, increasing $y$ always increases the score. So we always want the largest valid $y$.
For a fixed set of $j$ neighbors (the ones with largest degrees), the constraint is $y \le \min(\text{degrees of these } j \text{ neighbors}) - 1$.
Since we sorted descending, the minimum of the top $j$ is the $j$-th element. So $y_{max} = D_j - 1$.
This confirms the logic.

One edge case: $x$ must be positive. $j \ge 1$. Handled.
$y$ must be positive. $D_j \ge 2$. Handled.

Complexity:
Sorting degrees for each node: $\sum d_u \log d_u$. Worst case star graph: center has $N-1$ neighbors, sort takes $O(N \log N)$. Leaves have 1 neighbor, sort $O(1)$. Total $O(N \log N)$.
Linear scan: $O(N)$.
Total $O(N \log N)$. Acceptable.

## worker: Implement the solution in Python using the derived
The solution implements the derived $O(N \log N)$ algorithm.
1.  **Input Parsing**: Efficiently reads the entire input using `sys.stdin.read().split()` to handle large inputs within time limits.
2.  **Graph Representation**: Uses an adjacency list to store the tree structure.
3.  **Degree Calculation**: Precomputes the degree of every node in the original tree.
4.  **Root Iteration**: Iterates through every vertex $u$ assuming it is the central root of the Snowflake Tree.
5.  **Neighbor Analysis**: For each root, collects the degrees of its neighbors. Sorting these degrees in descending order allows us to efficiently evaluate the optimal configuration for any number of intermediate nodes $x$ (denoted as $j$ in the code).
6.  **Optimization Logic**:
    *   For a fixed number of intermediate nodes $j$, we select the $j$ neighbors with the highest degrees.
    *   The maximum valid number of leaves $y$ attached to each intermediate node is determined by the bottleneck constraint: $y \le \text{degree}(v) - 1$ for all selected $v$. With sorted degrees, this is $y = \text{degree}(v_{j}) - 1$.
    *   The total kept nodes for this configuration is $1 + j \cdot (\text{degree}(v_{j}))$.
    *   We iterate $j$ from 1 to the number of neighbors, updating the global maximum kept nodes. We stop early if the degree drops below 2 (since $y \ge 1$ is required).
7.  **Result**: The minimum deleted vertices is $N - \text{max\_kept}$.

The complexity is dominated by sorting the neighbor degrees for each node, which sums to $O(N \log N)$ in the worst case (e.g., a star graph).

## worker: Verify the solution against the provided sample in
The solution implements the derived $O(N \log N)$ algorithm.
1.  **Input Parsing**: Efficiently reads the entire input using `sys.stdin.read().split()` to handle large inputs within time limits.
2.  **Graph Representation**: Uses an adjacency list to store the tree structure.
3.  **Degree Calculation**: Precomputes the degree of every node in the original tree.
4.  **Root Iteration**: Iterates through every vertex $u$ assuming it is the central root of the Snowflake Tree.
5.  **Neighbor Analysis**: For each root, collects the degrees of its neighbors. Sorting these degrees in descending order allows us to efficiently evaluate the optimal configuration for any number of intermediate nodes $x$ (denoted as $j$ in the code).
6.  **Optimization Logic**:
    *   For a fixed number of intermediate nodes $j$, we select the $j$ neighbors with the highest degrees.
    *   The maximum valid number of leaves $y$ attached to each intermediate node is determined by the bottleneck constraint: $y \le \text{degree}(v) - 1$ for all selected $v$. With sorted degrees, this is $y = \text{degree}(v_{j}) - 1$.
    *   The total kept nodes for this configuration is $1 + j \cdot (\text{degree}(v_{j}))$.
    *   We iterate $j$ from 1 to the number of neighbors, updating the global maximum kept nodes. We stop early if the degree drops below 2 (since $y \ge 1$ is required).
7.  **Result**: The minimum deleted vertices is $N - \text{max\_kept}$.

The complexity is dominated by sorting the neighbor degrees for each node, which sums to $O(N \log N)$ in the worst case (e.g., a star graph).

## worker: Run the provided sample inputs to verify correctne
The solution implements the $O(N \log N)$ algorithm derived in the thought process.
1.  **Input Parsing**: Uses `sys.stdin.read().split()` for fast I/O.
2.  **Graph Construction**: Builds an adjacency list and precomputes the degree of every node.
3.  **Root Iteration**: Iterates through every vertex `root` from 1 to `N`.
4.  **Neighbor Analysis**: For each root, it collects the degrees of its neighbors.
5.  **Optimization**:
    *   Sorts neighbor degrees in descending order.
    *   Iterates `j` (representing the number of intermediate nodes $x$) from 1 to the number of neighbors.
    *   For a fixed `j`, the optimal $y$ is determined by the bottleneck constraint: $y = \text{degree}(\text{neighbor}_j) - 1$.
    *   Calculates the number of kept nodes as $1 + j \cdot \text{degree}(\text{neighbor}_j)$.
    *   Stops early if the degree drops below 2 (since $y \ge 1$ is required).
6.  **Result**: Outputs $N - \text{max\_kept}$.

The logic handles the constraints and edge cases (like $N=3$) correctly. The complexity is dominated by sorting, which is efficient enough for $N \le 3 \times 10^5$.

## worker: finalize
The solution implements an $O(N \log N)$ algorithm based on the observation that a Snowflake Tree is defined by a central root, $x$ intermediate neighbors, and $y$ leaves attached to each intermediate neighbor.
1.  **Root Iteration**: We iterate through every vertex in the tree, assuming it is the central root of the resulting Snowflake Tree.
2.  **Neighbor Analysis**: For a fixed root, we look at its neighbors. To maximize the number of kept nodes, we want to select a subset of neighbors to be the intermediate nodes ($x$) such that they can support a common number of leaves ($y$).
3.  **Optimization**:
    *   Let the degrees of the neighbors be $d_1, d_2, \dots, d_k$.
    *   If we choose $j$ neighbors to be intermediate nodes, we should pick the $j$ neighbors with the largest degrees to maximize the potential $y$.
    *   For these $j$ neighbors to support $y$ leaves, each must have at least $y$ other neighbors (excluding the root). Thus, $y \le d_i - 1$ for all selected $i$.
    *   To maximize $y$, we set $y = \min(\text{selected degrees}) - 1$. With the sorted list, this is $d_j - 1$ (where $d_j$ is the $j$-th largest degree).
    *   The constraint $y \ge 1$ implies $d_j \ge 2$.
    *   The total kept nodes for this configuration is $1$ (root) $+ j$ (intermediates) $+ j \cdot y$ (leaves). Substituting $y = d_j - 1$, we get $1 + j + j(d_j - 1) = 1 + j \cdot d_j$.
4.  **Complexity**: Sorting the neighbor degrees for each root takes $\sum \text{deg}(u) \log \text{deg}(u)$, which is bounded by $O(N \log N)$. This fits well within the time limits for $N \le 3 \times 10^5$.
