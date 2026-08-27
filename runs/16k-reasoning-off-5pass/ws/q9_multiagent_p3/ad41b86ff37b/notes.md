
## ideation
**Core Difficulty**:
The problem requires finding a subgraph that matches a very specific structural pattern (a "Snowflake Tree") by deleting the minimum number of vertices. This is equivalent to finding the maximum size of a valid Snowflake Tree subgraph.
The key constraints of a Snowflake Tree are:
1. It has exactly one root node.
2. The root is connected to exactly $x$ "intermediate" nodes.
3. Each intermediate node is connected to exactly $y$ leaf nodes (and the root).
4. All other nodes in the tree must be leaves attached to the intermediate nodes.
This implies the total number of nodes is $1 + x + xy$. The degrees in the subgraph are: Root ($x$), Intermediates ($y+1$), Leaves ($1$).

**Candidate Approaches**:
1.  **Iterate Root**: Since the structure is defined by a root, we can iterate through every vertex $r$ in the original tree $T$ as the potential root of the Snowflake Tree.
2.  **Greedy Matching per Root**: For a fixed root $r$:
    *   The root must have degree $x$ in the subgraph. We need to select $x$ neighbors of $r$ to be the intermediate nodes.
    *   Each selected intermediate node $u$ must have degree $y+1$ in the subgraph. Since one edge connects to $r$, it needs $y$ edges connecting to leaves.
    *   The remaining neighbors of $u$ (excluding $r$) can be used as leaves. If a neighbor $v$ of $u$ has a subtree, we can only keep $v$ as a leaf if $v$ has no other connections in the subgraph (i.e., we prune its entire subtree except $v$).
    *   This suggests a greedy strategy: For a fixed root, try all combinations of $x$ neighbors? No, $x$ can be up to $N$. We need a more efficient way.
    *   Actually, for a fixed root, the choice of intermediate nodes is constrained. We should pick neighbors that can provide the most leaves. However, the "cost" of picking a neighbor is that it consumes 1 slot from the root's degree $x$. The "gain" is $1 + (\text{number of leaves attachable to it})$.
    *   Wait, the structure is rigid. The root connects to $x$ nodes. Those $x$ nodes connect to $y$ leaves each. The leaves cannot connect to anything else.
    *   So, for a fixed root $r$, we look at its neighbors. Each neighbor $u$ can potentially serve as an intermediate node. If we pick $u$, we get $1$ (the node $u$ itself) plus $\min(\text{degree}(u)-1, \text{available leaves})$. But actually, if we pick $u$, we must attach exactly $y$ leaves to it. The leaves must come from $u$'s neighbors. Any neighbor $v$ of $u$ (other than $r$) can be a leaf only if we delete all of $v$'s other neighbors. To maximize the count, we should pick $v$ as a leaf and delete everything below it. So each neighbor of $u$ (except $r$) contributes 1 to the leaf count if we choose to make it a leaf.
    *   Therefore, if we select $u$ as an intermediate node, the maximum number of leaves we can attach to it is the number of its neighbors excluding $r$. Let $L(u) = \text{deg}(u) - 1$. If $L(u) \ge y$, we can get $y$ leaves. If $L(u) < y$, we can only get $L(u)$ leaves (and we cannot form a valid snowflake with this $u$ as an intermediate node unless we accept fewer leaves, but the definition says "attach y leaves", implying exactly $y$. If we can't get $y$, this $u$ is useless as an intermediate node).
    *   So, for a fixed root $r$, we calculate for each neighbor $u$: `score(u) = 1 + min(deg(u)-1, y)`. Wait, if `deg(u)-1 < y`, we can't use $u$ as an intermediate node because we can't attach $y$ leaves. So valid intermediates must have `deg(u) - 1 >= y`.
    *   We need to choose exactly $x$ neighbors from the valid ones to maximize the sum of their contributions. Since the contribution of each valid neighbor is fixed ($1+y$), we just pick the top $x$ neighbors.
    *   Wait, is it possible that a neighbor $v$ of $u$ is part of a larger subtree that we could use differently? No, because in a Snowflake Tree, leaves have degree 1. If we keep $v$ as a leaf, we must delete all its other edges. Thus, the "subtree" rooted at $v$ (away from $u$) contributes exactly 1 node ($v$) to the count.
    *   So the algorithm for a fixed root $r$:
        1. Identify neighbors $N(r)$.
        2. For each $u \in N(r)$, calculate potential leaves: $k_u = \text{deg}(u) - 1$.
        3. If $k_u < y$, $u$ cannot be an intermediate node.
        4. If $k_u \ge y$, $u$ can be an intermediate node, contributing $1 + y$ nodes.
        5. Sort valid neighbors by contribution (all are $1+y$, so just count them).
        6. If we have fewer than $x$ valid neighbors, this root configuration is impossible.
        7. If we have $\ge x$ valid neighbors, the max nodes kept is $1 + x \times (1+y)$.
    *   Wait, this logic assumes we can always find $x$ intermediates. But what if we don't need to use the *maximum* possible leaves? The problem says "attach y leaves". It's a strict definition. So yes, we need exactly $y$ leaves per intermediate.
    *   Is there a case where we pick a neighbor $u$ with $k_u > y$? Yes, we just pick $y$ of its neighbors as leaves and delete the rest. The cost is deleting $k_u - y$ nodes. The gain is $1+y$.
    *   So for a fixed root, the max nodes is $1 + x(1+y)$ provided there are at least $x$ neighbors with degree $\ge y+1$.
    *   BUT, $x$ and $y$ are not fixed! We can choose any positive integers $x, y$.
    *   So for a fixed root $r$, we need to find $x, y$ such that:
        - There are at least $x$ neighbors with degree $\ge y+1$.
        - Maximize $1 + x(1+y)$.
    *   Let $D_r$ be the list of degrees of neighbors of $r$. We need to choose $x$ and $y$ such that count($d \in D_r$ where $d \ge y+1$) $\ge x$. Maximize $1 + x(1+y)$.
    *   This is a 2D optimization. We can iterate over possible values of $y$. Since max degree is $N$, $y$ can be up to $N$.
    *   For a fixed $y$, the maximum $x$ we can choose is the count of neighbors with degree $\ge y+1$. Let this be $cnt_y$. Then the score is $1 + cnt_y(1+y)$. We maximize this over all $y \ge 1$.
    *   This approach is $O(N^2)$ if we do it naively for each root. Total $O(N^3)$. Too slow. $N=3 \times 10^5$.
    *   We need a faster way. Notice that for a fixed root, the function $f(y) = (\text{count of neighbors with deg} \ge y+1) \times (1+y)$ is what we want to maximize.
    *   Can we optimize the calculation over all roots?
    *   Alternative perspective: The Snowflake Tree is defined by parameters $x, y$. Total nodes $M = 1 + x + xy$.
    *   Maybe we can iterate over possible $x$ and $y$? $x, y$ can be large. But note that if $x \ge N$, impossible. If $y \ge N$, impossible.
    *   Actually, the constraints on $x$ and $y$ are coupled with the tree structure.
    *   Let's reconsider the "fixed root" approach with optimization.
    *   For a root $r$, let the degrees of neighbors be $d_1, d_2, \dots, d_k$.
    *   We want $\max_{y \ge 1} (1 + (1+y) \cdot \text{count}(\{i \mid d_i \ge y+1\}))$.
    *   Let $S_r$ be the sorted list of neighbor degrees.
    *   The count is a step function. As $y$ increases, the count decreases.
    *   We can compute this efficiently for one root in $O(\text{deg}(r) \log \text{deg}(r))$ or $O(\text{deg}(r))$.
    *   Sum of degrees is $2(N-1)$. So summing over all roots: $\sum O(\text{deg}(r)) = O(N)$.
    *   Wait, sorting takes $O(d \log d)$. Sum of $d \log d$ is bounded by $O(N \log N)$.
    *   So the algorithm:
        1. Compute degrees of all nodes.
        2. For each node $r$ from 1 to $N$:
            a. Collect degrees of all neighbors: $L = [\text{deg}(v) \text{ for } v \in \text{adj}(r)]$.
            b. Sort $L$ in descending order.
            c. Iterate through possible $y$. The critical values for $y$ are related to the values in $L$. Specifically, if we pick $y$, the count is the number of elements $\ge y+1$.
            d. We can iterate $i$ from $0$ to $|L|-1$. Suppose we pick the first $i+1$ neighbors (the largest degrees) to be the intermediates. Then we must have $y+1 \le L[i]$ (if $i < |L|-1$) or just $y+1 \le L[i]$ generally?
            e. Actually, if we choose $x = i+1$ intermediates, we need $y$ such that at least $x$ neighbors have degree $\ge y+1$. To maximize $1+x(1+y)$, for a fixed $x$, we should pick the largest possible $y$. The largest $y$ is $L[x-1] - 1$ (since $L$ is 0-indexed sorted descending, $L[x-1]$ is the $x$-th largest degree).
            f. So for each $x \in [1, |L|]$, candidate $y = L[x-1] - 1$. If $y \ge 1$, calculate score $1 + x(1+y)$.
            g. Track global maximum.
        3. Result is $N - \text{max\_kept}$.

## worker: Write the final Python code enclosed in the specif
The problem asks for the minimum vertex deletions to form a "Snowflake Tree". A Snowflake Tree is defined by parameters $x$ and $y$, consisting of a root connected to $x$ intermediate nodes, each connected to $y$ leaves. The total number of nodes is $1 + x + xy$.

The algorithm iterates through every vertex in the original tree, treating it as the potential root of the Snowflake Tree. For a fixed root $r$:
1.  Identify the degrees of all its neighbors in the original tree.
2.  Sort these degrees in descending order.
3.  Iterate through possible values of $x$ (number of intermediate nodes), from 1 to the number of neighbors.
4.  For a chosen $x$, the $x$-th largest neighbor degree (let's call it $d$) dictates the maximum possible $y$. Specifically, to have $x$ neighbors with degree at least $y+1$, we must have $d \ge y+1$, so $y \le d-1$. To maximize the tree size, we pick the largest valid $y$, which is $y = d-1$.
5.  We only consider this configuration if $y \ge 1$ (since $y$ must be a positive integer).
6.  Calculate the size of the resulting Snowflake Tree: $1 + x(1+y)$.
7.  Track the maximum size found across all roots and all valid $(x, y)$ pairs.
8.  The result is $N$ minus this maximum size.

The complexity is dominated by sorting the neighbor degrees for each node. The sum of degrees is $2(N-1)$, and sorting takes $O(d \log d)$. The total time complexity is roughly $O(N \log N)$, which fits well within the limits for $N \le 3 \times 10^5$.
