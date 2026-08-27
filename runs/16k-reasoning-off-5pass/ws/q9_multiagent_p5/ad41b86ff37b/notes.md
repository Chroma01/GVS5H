
## ideation
**Core Difficulty**:
The problem requires finding a subgraph isomorphic to a "Snowflake Tree" with the maximum number of vertices. A Snowflake Tree $S(x, y)$ has a specific rigid structure:
1. One central root (degree $x$).
2. $x$ immediate children (degree $y+1$ in the full tree, but in the subgraph, they connect to the root and $y$ leaves).
3. $x \times y$ leaves (degree 1).
Total vertices = $1 + x + xy$.
The challenge is that $x$ and $y$ are not given; we must find the optimal $x, y$ and the optimal root position in the input tree $T$ that maximizes the size of the valid subgraph. Since $N$ is up to $3 \times 10^5$, an $O(N^2)$ approach is too slow. We need something close to $O(N)$.

**Candidate Approaches**:
1.  **Iterate Root + Greedy/DFS Check**:
    - Iterate through every vertex $r$ in $T$ as the potential center.
    - For a fixed root $r$, we need to select $x$ neighbors to be the "branch nodes".
    - Each selected branch node $u$ must have at least $y$ neighbors (excluding $r$) that can serve as leaves.
    - To maximize the size for a fixed $r$ and fixed $x$, we should greedily pick the $x$ neighbors that have the highest degree (excluding $r$). Let these degrees be $d_1, d_2, \dots, d_x$.
    - Then, we need to find the largest $y$ such that $d_i \ge y$ for all $i=1\dots x$. This means $y = \min(d_1, \dots, d_x)$.
    - The size of the snowflake would be $1 + x + x \cdot y$.
    - However, iterating all $r$ and sorting neighbors takes $O(N \log N)$ or $O(N)$ if optimized, but checking all pairs $(x, y)$ might be tricky.
    - Actually, for a fixed root $r$, let the degrees of neighbors be $D = \{deg(u) - 1 \mid u \in neighbors(r)\}$.
    - We want to choose a subset of size $x$ from $D$, say $D'$, such that $y = \min(D')$ maximizes $1 + x + x \cdot y$.
    - Note that if we fix $y$, we should pick all neighbors with degree $\ge y$. Let $count(y)$ be the number of neighbors with degree $\ge y$. Then we can form a snowflake with $x = count(y)$ and parameter $y$. The size is $1 + count(y) + count(y) \cdot y$.
    - So for each root $r$, we just need to compute the degrees of its neighbors, sort them (or use a frequency array), and iterate possible values of $y$ (which must be one of the neighbor degrees) to find the max.
    - Complexity: Sum of degrees is $2(N-1)$. Sorting neighbors for each node takes $\sum deg(v) \log deg(v) \le N \log N$. This is efficient enough.

2.  **Refinement of Approach 1**:
    - For each vertex $v$:
        - Calculate $d_u = deg(u) - 1$ for all neighbors $u$.
        - Sort these values in descending order: $v_1 \ge v_2 \ge \dots \ge v_k$.
        - Iterate $i$ from $1$ to $k$. Let $x = i$. The best $y$ we can support with these $x$ branches is $v_i$ (since $v_1 \dots v_i$ are all $\ge v_i$).
        - Calculate score: $1 + i + i \cdot v_i$.
        - Track global maximum.
    - This covers all valid configurations where the chosen branches are the "best" ones for a given $y$. Is it possible that picking a worse branch allows a larger $y$? No, because $y$ is limited by the *minimum* degree in the chosen set. To maximize $x \cdot y$, if we fix the minimum element to be $Y$, we should include *all* available neighbors with degree $\ge Y$. Picking fewer would reduce $x$ without increasing $y$. Picking a neighbor with degree $< Y$ would reduce $y$. Thus, the greedy strategy of "for a fixed minimum degree $Y$, take all neighbors with degree $\ge Y$" is optimal for a fixed root.

3.  **Pitfalls**:
    - **Root Degree 0**: If a node is isolated (not possible in a tree with $N \ge 3$ unless $N=1$), handle gracefully.
    - **Small Trees**: $N=3$, $x=1, y=1$. Logic holds.
    - **Data Types**: Scores can be up to $N$, fits in integer.
    - **Input Parsing**: Standard adjacency list construction.
    - **Time Limit**: $O(N \log N)$ is safe for $3 \times 10^5$. Python might be slow with heavy I/O or object creation, so use fast I/O and efficient lists.

**Algorithm Steps**:
1. Read $N$ and edges. Build adjacency list. Compute degrees.
2. Initialize `max_kept = 0`.
3. Loop `root` from 1 to $N$:
    a. Collect `neighbor_degrees = [deg(u) - 1 for u in adj[root]]`.
    b. Sort `neighbor_degrees` descending.
    c. Iterate `i` from 0 to `len(neighbor_degrees) - 1`:
        i. `x = i + 1`
        ii. `y = neighbor_degrees[i]`
        iii. `current_kept = 1 + x + x * y`
        iv. `max_kept = max(max_kept, current_kept)`
4. Result is `N - max_kept`.

**Edge Cases**:
- If `neighbor_degrees` is empty (leaf node as root), loop doesn't run, `max_kept` remains 0? Wait, a snowflake tree must have at least $x \ge 1, y \ge 1$. If no neighbors, we can't form a snowflake. The problem says "always possible", implying there exists at least one valid configuration. Since $N \ge 3$, there is at least one internal node with degree $\ge 2$, so `max_kept` will be updated.
- Constraints: $x, y$ positive integers. So $x \ge 1, y \ge 1$. Our loop ensures $x \ge 1$. We need $y \ge 1$. If `neighbor_degrees[i]` is 0, then $y=0$, which is invalid. We should only consider $i$ where `neighbor_degrees[i] >= 1`.

## worker: Implement the solution in Python using the greedy 
The solution implements the greedy strategy derived in the thought process:
1.  **Input Parsing**: Efficiently reads $N$ and edges using `sys.stdin.read` and an iterator to handle large inputs ($3 \times 10^5$) quickly.
2.  **Graph Representation**: Uses an adjacency list and a separate degree array. The degree array is crucial because we need the total degree of a neighbor to calculate how many leaves it can support ($deg(u) - 1$).
3.  **Core Logic**:
    -   Iterates through every vertex $r$ as a candidate for the central root of the Snowflake Tree.
    -   For each root, it calculates the potential number of leaves each neighbor can provide ($deg(u) - 1$).
    -   It sorts these values in descending order. This allows us to efficiently determine the optimal set of branches for any given $x$.
    -   For each possible count of branches $x$ (from 1 to the number of neighbors), the algorithm sets $y$ to the leaf capacity of the $x$-th best neighbor (which is the minimum among the top $x$).
    -   It calculates the total vertices kept ($1 + x + x \cdot y$) and updates the global maximum.
    -   It stops checking for a specific root if the minimum leaf capacity drops below 1, as $y$ must be a positive integer.
4.  **Complexity**:
    -   Building the graph: $O(N)$.
    -   Outer loop runs $N$ times.
    -   Inside the loop: collecting neighbors is $O(deg(r))$, sorting is $O(deg(r) \log deg(r))$, and the inner loop is $O(deg(r))$.
    -   Total complexity: $\sum_{r} O(deg(r) \log deg(r))$. Since $\sum deg(r) = 2(N-1)$, the worst-case complexity is bounded by $O(N \log N)$, which fits well within the time limits for $N=300,000$.
5.  **Edge Cases**: Handles cases where a root has no neighbors (leaf nodes) by skipping them. The problem guarantees a solution exists, so `max_kept` will be updated at least once.

## worker: Run the code against the provided sample inputs to
The code implements the greedy strategy derived in the thought process:
1.  **Input Parsing**: Efficiently reads $N$ and edges using `sys.stdin.read` and an iterator to handle large inputs ($3 \times 10^5$) quickly.
2.  **Graph Representation**: Uses an adjacency list and a separate degree array. The degree array is crucial because we need the total degree of a neighbor to calculate how many leaves it can support ($deg(u) - 1$).
3.  **Core Logic**:
    -   Iterates through every vertex $r$ as a candidate for the central root of the Snowflake Tree.
    -   For each root, it calculates the potential number of leaves each neighbor can provide ($deg(u) - 1$).
    -   It sorts these values in descending order. This allows us to efficiently determine the optimal set of branches for any given $x$.
    -   For each possible count of branches $x$ (from 1 to the number of neighbors), the algorithm sets $y$ to the leaf capacity of the $x$-th best neighbor (which is the minimum among the top $x$).
    -   It calculates the total vertices kept ($1 + x + x \cdot y$) and updates the global maximum.
    -   It stops checking for a specific root if the minimum leaf capacity drops below 1, as $y$ must be a positive integer.
4.  **Complexity**:
    -   Building the graph: $O(N)$.
    -   Outer loop runs $N$ times.
    -   Inside the loop: collecting neighbors is $O(deg(r))$, sorting is $O(deg(r) \log deg(r))$, and the inner loop is $O(deg(r))$.
    -   Total complexity: $\sum_{r} O(deg(r) \log deg(r))$. Since $\sum deg(r) = 2(N-1)$, the worst-case complexity is bounded by $O(N \log N)$, which fits well within the time limits for $N=300,000$.
5.  **Edge Cases**: Handles cases where a root has no neighbors (leaf nodes) by skipping them. The problem guarantees a solution exists, so `max_kept` will be updated at least once.

## worker: Run the code against Sample 1, Sample 2, and Sampl
The code implements the greedy strategy derived in the thought process:
1.  **Input Parsing**: Efficiently reads $N$ and edges using `sys.stdin.read` and an iterator to handle large inputs ($3 \times 10^5$) quickly.
2.  **Graph Representation**: Uses an adjacency list and a separate degree array. The degree array is crucial because we need the total degree of a neighbor to calculate how many leaves it can support ($deg(u) - 1$).
3.  **Core Logic**:
    -   Iterates through every vertex $r$ as a candidate for the central root of the Snowflake Tree.
    -   For each root, it calculates the potential number of leaves each neighbor can provide ($deg(u) - 1$).
    -   It sorts these values in descending order. This allows us to efficiently determine the optimal set of branches for any given $x$.
    -   For each possible count of branches $x$ (from 1 to the number of neighbors), the algorithm sets $y$ to the leaf capacity of the $x$-th best neighbor (which is the minimum among the top $x$).
    -   It calculates the total vertices kept ($1 + x + x \cdot y$) and updates the global maximum.
    -   It stops checking for a specific root if the minimum leaf capacity drops below 1, as $y$ must be a positive integer.
4.  **Complexity**:
    -   Building the graph: $O(N)$.
    -   Outer loop runs $N$ times.
    -   Inside the loop: collecting neighbors is $O(deg(r))$, sorting is $O(deg(r) \log deg(r))$, and the inner loop is $O(deg(r))$.
    -   Total complexity: $\sum_{r} O(deg(r) \log deg(r))$. Since $\sum deg(r) = 2(N-1)$, the worst-case complexity is bounded by $O(N \log N)$, which fits well within the time limits for $N=300,000$.
5.  **Edge Cases**: Handles cases where a root has no neighbors (leaf nodes) by skipping them. The problem guarantees a solution exists, so `max_kept` will be updated at least once.

## worker: finalize
The solution implements a greedy strategy to find the maximum size of a "Snowflake Tree" subgraph.
1.  **Problem Analysis**: A Snowflake Tree $S(x, y)$ consists of a central root, $x$ children (branches), and each branch having exactly $y$ leaves. The total vertices are $1 + x + xy$.
2.  **Strategy**: Iterate through every vertex in the input tree as a candidate for the central root. For a fixed root $r$, the potential branches are its neighbors. A neighbor $u$ can support at most $deg(u) - 1$ leaves (since one edge connects to $r$).
3.  **Optimization**: To maximize the size for a fixed root, we should select the $x$ neighbors with the highest leaf capacities. Let these capacities be sorted in descending order: $v_1 \ge v_2 \ge \dots \ge v_k$. If we choose $x$ branches, the limiting factor for $y$ is the minimum capacity among them, which is $v_x$. Thus, for a chosen $x$, the optimal $y$ is $v_x$. The size is $1 + x + x \cdot v_x$.
4.  **Complexity**: We iterate $N$ times. Inside, we collect neighbor degrees ($O(deg(r))$), sort them ($O(deg(r) \log deg(r))$), and iterate ($O(deg(r))$). The sum of degrees is $2(N-1)$, so the total time complexity is roughly $O(N \log N)$, which fits within the limits for $N=3 \times 10^5$.
5.  **Edge Cases**: The code handles cases where a root has no neighbors (leaves) by skipping them. It also ensures $y \ge 1$ as required by the problem statement.
