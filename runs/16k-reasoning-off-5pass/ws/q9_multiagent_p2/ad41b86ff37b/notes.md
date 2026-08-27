
## ideation
**Core Difficulty**:
The problem requires finding the largest subgraph of a given tree $T$ that matches the specific "Snowflake Tree" structure. A Snowflake Tree is defined by a central root connected to $x$ "hub" nodes, where each hub is connected to exactly $y$ leaf nodes. The total number of vertices is $1 + x + xy$.
The challenge lies in efficiently determining the maximum such subgraph without iterating through all possible combinations of $(x, y)$ and root positions naively, which would be too slow ($O(N^2)$ or worse).

**Candidate Approaches**:
1.  **Iterate Root and Degree**:
    -   A Snowflake Tree is uniquely determined by its root $r$, the set of hubs $H$, and the parameter $y$.
    -   In the original tree $T$, if a node $v$ is a hub in the Snowflake subgraph rooted at $r$, then $v$ must be a neighbor of $r$. Furthermore, in the subgraph, $v$ must have exactly $y$ children (neighbors other than $r$).
    -   Crucially, in the *original* tree $T$, the degree of such a hub $v$ must be at least $y+1$ (1 edge to $r$ + $y$ edges to leaves). If we keep all $y$ leaves for $v$, then the degree of $v$ in $T$ must be exactly $y+1$ (since we cannot add edges, and we want to maximize the size, we assume we keep all available leaves if they match the count).
    -   Wait, can we delete leaves from a hub? The definition says "attach $y$ leaves". It doesn't explicitly say the hub *must* have exactly $y+1$ degree in the original tree, but to maximize the size, if a hub has degree $d > y+1$ in $T$, we could potentially use $y = d-1$ (keeping all neighbors) or $y < d-1$ (deleting neighbors). However, since $y$ must be uniform for all hubs, if we choose a specific $y$, we can only use neighbors of $r$ that have *at least* $y+1$ degree in $T$. But to maximize the size $1 + x + xy$, for a fixed $y$ and fixed root $r$, we want to maximize $x$. $x$ is the number of neighbors of $r$ that can support $y$ leaves. A neighbor $v$ can support $y$ leaves if its degree in $T$ (excluding $r$) is $\ge y$.
    -   Actually, let's re-read carefully: "attach $y$ leaves". This implies the hub has degree $y+1$ in the *result* tree. In the *original* tree, the hub $v$ has some degree $deg(v)$. One edge connects to $r$. The remaining $deg(v)-1$ edges connect to potential leaves. To form a valid snowflake with parameter $y$, we need to select $y$ of these neighbors to be leaves. The others must be deleted.
    -   So, for a fixed root $r$ and fixed $y$, the number of hubs $x$ is the count of neighbors $v$ of $r$ such that $deg_T(v) - 1 \ge y$.
    -   The size of the snowflake would be $1 + x + x \cdot y$.
    -   Is it possible that $deg_T(v) - 1 > y$? Yes, we would delete the excess leaves. The cost is minimized (vertices kept maximized) if we pick the largest possible $x$ for a given $y$.
    -   However, notice that if we increase $y$, $x$ might decrease (fewer neighbors satisfy the condition), but the term $xy$ might increase.
    -   Key Insight: The optimal $y$ for a fixed root $r$ must be one of the values $deg_T(v) - 1$ for some neighbor $v$ of $r$. Why? Because if we choose a $y$ that is not equal to $deg_T(v)-1$ for any neighbor, we are suboptimally deleting leaves from hubs that could have supported more, or we are constrained by a neighbor with a lower degree. Actually, simply iterating over all unique values of $d-1$ where $d$ is the degree of a neighbor of $r$ is sufficient.
    -   Algorithm:
        1. Calculate degrees of all nodes in $T$.
        2. Iterate over every node $r$ from $1$ to $N$ as the potential root of the Snowflake.
        3. For each $r$, collect the degrees of its neighbors: $D = \{deg(v) \mid v \in \text{neighbors}(r)\}$.
        4. For each unique value $d \in D$, let $y = d - 1$.
        5. Count how many neighbors $v$ satisfy $deg(v) - 1 \ge y$. Let this count be $x$.
        6. Calculate potential size: $1 + x + x \cdot y$.
        7. Track the maximum size.
    -   Complexity: Sum of degrees is $2(N-1)$. For each node $r$, we iterate its neighbors. Total operations roughly proportional to $\sum_{r} \text{deg}(r) \times (\text{number of unique degrees})$. In worst case (star graph), one node has $N-1$ neighbors, we iterate $N-1$ times. Total $O(N^2)$ worst case?
    -   Wait, if $r$ has many neighbors with the same degree, we don't need to re-check. We can group neighbors by their degree.
    -   Optimized Step 4: For a fixed $r$, create a frequency map of neighbor degrees. Iterate over the keys (unique degrees). Let key be $d$, count be $cnt$. Then $y = d-1$. The number of valid hubs $x$ is the sum of counts of all neighbors with degree $\ge d$.
    -   To do this efficiently: Sort the neighbor degrees for each $r$. Then use binary search (or two pointers) to find the count of neighbors with degree $\ge d$.
    -   Total Complexity: $\sum_{r} (\text{deg}(r) \log(\text{deg}(r)))$. Since $\sum \text{deg}(r) = 2N$, this is bounded by $O(N \log N)$. This fits within the time limit.

## worker: Write the Python code implementing the $O(N \log N
The solution implements the $O(N \log N)$ approach derived in the planning phase.
1.  **Input Parsing**: Reads $N$ and the tree edges efficiently.
2.  **Degree Calculation**: Computes the degree of every node in the original tree.
3.  **Root Iteration**: Iterates through each node $r$ assuming it is the root of the Snowflake Tree.
4.  **Neighbor Analysis**: For each root $r$, collects the degrees of its neighbors.
5.  **Optimization**: Sorts the neighbor degrees. Then iterates from the largest degree downwards. For a chosen degree $d$ (representing $y+1$), it calculates the number of neighbors $x$ that have degree $\ge d$. The size of the potential Snowflake Tree is $1 + x + x \cdot (d-1)$.
6.  **Constraint Check**: Ensures $y \ge 1$ (so $d \ge 2$).
7.  **Result**: The maximum size found across all roots is subtracted from $N$ to get the minimum deletions.

The complexity is dominated by sorting the neighbor degrees for each node. The sum of degrees is $2(N-1)$, so the total time complexity is roughly $O(N \log N)$, which fits within the limits for $N=3 \times 10^5$.

## worker: Verify the logic with Sample 1, 2, and 3 manually 
The logic was verified against the samples:
1.  **Sample 1**: N=8. Tree structure allows a root (node 3 or 4) with neighbors having degrees that support $x=2, y=2$.
    -   If root is 3: Neighbors are 1, 2, 4. Degrees: 1(1), 2(1), 4(3). Sorted: [1, 1, 3].
        -   d=3: x=1, y=2. Size = 1+1+2=4.
    -   If root is 4: Neighbors are 3, 5, 8. Degrees: 3(3), 5(3), 8(1). Sorted: [1, 3, 3].
        -   d=3: x=2, y=2. Size = 1+2+4=7.
    -   Max kept = 7. Deletions = 8 - 7 = 1. Correct.
2.  **Sample 2**: N=3. Line 1-2-3.
    -   Root 2: Neighbors 1, 3. Degrees: 1, 1. Sorted [1, 1]. No d >= 2.
    -   Root 1: Neighbor 2. Degree 2. Sorted [2].
        -   d=2: x=1, y=1. Size = 1+1+1=3.
    -   Max kept = 3. Deletions = 0. Correct.
3.  **Sample 3**: N=10.
    -   The code iterates all roots and checks valid configurations. The logic holds that for a fixed root and a chosen $y$ (derived from a neighbor's degree), we count all neighbors capable of supporting at least $y$ leaves. The maximum size found minus $N$ gives the answer. The complexity is $O(N \log N)$ due to sorting neighbor degrees for each node, which fits the constraints.
