1.  **Understand $f(x, y)$**: The value $f(x, y)$ is the minimax path weight between $x$ and $y$. This is equivalent to the weight of the heaviest edge on the unique path between $x$ and $y$ in the Minimum Spanning Tree (MST) of the graph. We can construct the MST using Kruskal's or Prim's algorithm.
2.  **Precompute Pairwise Distances**: Since $K$ is small ($K \le N \le 2 \cdot 10^5$, but typically $K$ is the number of query points), we need $f(A_i, B_j)$ for all $i, j$. However, $K$ can be up to $N$, so $O(K^2 \log N)$ or $O(K^2)$ might be too slow if $K$ is large. Wait, $K \le N$. If $K$ is large, we cannot compute all pairs naively.
    *   Actually, let's re-read constraints. $K \le N$. If $K$ is large (e.g., $10^5$), $O(K^2)$ is TLE.
    *   However, the problem asks to minimize $\sum f(A_i, B_{\pi(i)})$. This is a minimum weight perfect matching in a bipartite graph with parts $A$ and permuted $B$. The cost matrix is $C_{ij} = f(A_i, B_j)$.
    *   Is there a structure to $f(x,y)$? Yes, it's determined by the MST.
    *   If $K$ is small, we can compute all pairs. If $K$ is large, we need a faster approach.
    *   Let's check the constraints again. $N, M \le 2 \cdot 10^5$. $K \le N$.
    *   Computing all $K^2$ distances is $O(K^2 \log N)$ or $O(K^2)$. If $K=10^5$, this is $10^{10}$, which is too slow.
    *   We need a more efficient way to find the minimum weight perfect matching.
    *   Observation: The function $f(x,y)$ satisfies the ultrametric inequality on the MST leaves? Not exactly.
    *   Alternative approach: Since the costs are derived from an MST, we can use the property that $f(x,y)$ is the maximum edge weight on the path in the MST.
    *   Can we use the fact that we want to match $A$'s to $B$'s?
    *   If $K$ is small, we use min-cost max-flow or Hungarian algorithm? No, $K$ is up to $2 \cdot 10^5$.
    *   Wait, is it possible that the optimal matching is simply sorting $A$ and $B$ based on some property? No, the graph structure matters.
    *   Let's reconsider the size. If $K$ is large, maybe the graph is a tree? No, it's a general graph.
    *   Actually, there is a known result: For minimax paths on a tree (MST), the cost $f(x,y)$ is related to the Lowest Common Ancestor (LCA).
    *   If we root the MST, $f(x,y) = \max_{e \in path(x,y)} w(e)$.
    *   This problem is equivalent to finding a minimum weight perfect matching in a bipartite graph where edge weights are defined by MST distances.
    *   However, general min-cost perfect matching is too slow.
    *   Let's look at the constraints and problem type again. This is likely a competitive programming problem.
    *   Key Insight: If we process edges of the MST in increasing order, we can determine connectivity.
    *   Actually, if $K$ is large, maybe we don't need all pairs.
    *   Let's consider the case where $A$ and $B$ are just sets of vertices.
    *   If we sort the vertices in $A$ and $B$ based on their DFS entry times or some other traversal order, does that help?
    *   There is a greedy strategy for matching on trees?
    *   Let's try a different angle. The cost $f(x,y)$ is the smallest $W$ such that $x$ and $y$ are connected using only edges with weight $\le W$.
    *   We can use a "Union-Find" approach processing edges in increasing order.
    *   However, we need to match specific nodes.
    *   Let's assume $K$ is small enough for $O(K^2)$? No, $K$ up to $2 \cdot 10^5$.
    *   Is it possible that the optimal matching is unique or has a simple structure?
    *   Actually, for general graphs, this problem is hard. But on a tree (MST), is it easier?
    *   Yes, on a tree, $f(x,y)$ is the max edge on the path.
    *   There is a greedy algorithm for minimum weight perfect matching on a tree for specific metrics?
    *   Let's look at similar problems. "Minimum weight perfect matching on a tree with minimax distance".
    *   If we root the MST, we can use a DFS. For each subtree, we count the number of available nodes from $A$ and $B$.
    *   Greedy Strategy: Process the tree from leaves up. In each subtree, if there are unmatched nodes from $A$ and $B$, we can potentially match them. But the cost depends on the edge connecting the subtree to the parent.
    *   Actually, a known greedy approach for this specific problem (minimizing sum of minimax distances) on a tree is:
        1.  Build MST.
        2.  Root the MST arbitrarily (e.g., at vertex 1).
        3.  Use DFS to process subtrees.
        4.  Maintain counts of unmatched $A$ nodes and unmatched $B$ nodes in the current subtree.
        5.  When moving up from a child to parent via edge $e$ with weight $w$, any match formed *within* the subtree doesn't involve $e$. Any match that crosses the edge $e$ (one node in subtree, one outside) will have cost at least $w$.
        6.  To minimize total cost, we should maximize the number of matches that happen "deep" in the tree (with smaller edge weights) and defer matches that cross heavier edges.
        7.  Specifically, in a subtree, if we have $cntA$ unmatched $A$'s and $cntB$ unmatched $B$'s, we can match $\min(cntA, cntB)$ pairs *within* the subtree using edges strictly inside the subtree (which have weights $\le$ current edge weight? No, edges inside are processed first if we go bottom-up? No, bottom-up means we process small edges first? No, bottom-up processes local structure. The edge connecting to parent is the "bottleneck" for any path leaving the subtree).
        8.  Actually, the standard greedy for this is:
            -   For each node, calculate the number of $A$ nodes and $B$ nodes in its subtree.
            -   Let $S_A(u)$ be the count of $A$-nodes in subtree of $u$, $S_B(u)$ be the count of $B$-nodes.
            -   The edge connecting $u$ to its parent will be part of the path for any pair $(a, b)$ where $a$ is in $u$'s subtree and $b$ is outside, or vice versa.
            -   The number of such pairs that *must* cross the edge $(u, parent(u))$ is $|S_A(u) - S_B(u)|$? No.
            -   Let $diff(u) = S_A(u) - S_B(u)$.
            -   If $diff(u) > 0$, there are $diff(u)$ more $A$'s than $B$'s in the subtree. These $A$'s must be matched with $B$'s outside the subtree. Thus, at least $diff(u)$ paths must cross the edge to the parent.
            -   If $diff(u) < 0$, there are $|diff(u)|$ more $B$'s than $A$'s. These $B$'s must be matched with $A$'s outside.
            -   So, the number of paths crossing the edge $e=(u, parent(u))$ is exactly $|S_A(u) - S_B(u)|$.
            -   Each such path has a cost at least $w(e)$.
            -   Can we achieve this lower bound? Yes. We can match the "excess" nodes from the subtree with nodes from outside. The internal matches (within the subtree) will use edges with weights $\le w(e)$? Not necessarily.
            -   Wait, the cost of a path is the *maximum* edge weight. If we match two nodes within the subtree, their path lies entirely within the subtree. The maximum edge weight on that path is determined by edges inside the subtree.
            -   If we match a node in the subtree with a node outside, the path *must* cross $e=(u, parent(u))$. Therefore, the max edge weight is at least $w(e)$. It could be larger if there's a heavier edge elsewhere on the path.
            -   However, if we process edges in increasing order (Kruskal's style), we can determine the contribution.
            -   Actually, the formula $\sum_{e \in MST} w(e) \times |S_A(u_e) - S_B(u_e)|$ gives the minimum total weight?
            -   Let's verify with Sample 1.
                -   MST Edges: (3,4,1), (1,3,2), (1,4,4) is not in MST?
                -   Edges sorted: (3,4,1), (1,3,2), (1,4,4), (2,4,5).
                -   MST: 3-4 (1), 1-3 (2), 2-4 (5).
                -   Tree structure: 2-4-3-1.
                -   Root at 1.
                -   Children of 1: 3. Child of 3: 4. Child of 4: 2.
                -   $A = \{1, 1, 3\}$, $B = \{4, 4, 2\}$.
                -   Counts in subtrees:
                    -   Node 2: $S_A=0, S_B=1$ (if 2 is in B). $diff = -1$. Edge to parent (4-2) has weight 5. Contribution: $5 \times |-1| = 5$.
                    -   Node 4: Subtree includes 2. $S_A=0, S_B=1$ (from 2) + 1 (if 4 is in B? No, 4 is in B twice? $B=\{4,4,2\}$. So 4 is in B twice. 2 is in B once.
                    -   Let's map indices.
                    -   $A_1=1, A_2=1, A_3=3$.
                    -   $B_1=4, B_2=4, B_3=2$.
                    -   Nodes in A: 1, 1, 3. (Vertex 1 has count 2, Vertex 3 has count 1).
                    -   Nodes in B: 4, 4, 2. (Vertex 4 has count 2, Vertex 2 has count 1).
                    -   Subtree 2: $S_A=0, S_B=1$. $diff = -1$. Edge (4,2) w=5. Contrib $5 \times 1 = 5$.
                    -   Subtree 4: Contains 2. $S_A=0, S_B=1 (from 2) + 2 (node 4 itself) = 3$. $diff = -3$. Edge (3,4) w=1. Contrib $1 \times 3 = 3$.
                    -   Subtree 3: Contains 4,2. $S_A=1 (node 3), S_B=3$. $diff = 1-3 = -2$. Edge (1,3) w=2. Contrib $2 \times 2 = 4$.
                    -   Subtree 1: Root. $S_A=2 (node 1) + 1 = 3, S_B=3$. $diff=0$.
                    -   Total Sum = $5 + 3 + 4 = 12$.
                    -   Sample output is 8. My formula gave 12. Why?
                    -   The formula $\sum w(e) |S_A - S_B|$ calculates the cost if *every* path crossing the edge contributes $w(e)$ to the sum. But the cost of a path is the *maximum* edge on it.
                    -   If a path crosses multiple edges, it only "pays" for the heaviest one.
                    -   The formula above assumes each crossing adds $w(e)$ to the cost, which is incorrect for minimax.
                    -   Correct logic for Minimax Matching on Tree:
                        -   We want to minimize $\sum \max_{e \in path} w(e)$.
                        -   This is equivalent to: For each edge $e$, how many paths have $e$ as the *maximum* edge?
                        -   This is complex.

    *   Alternative Insight:
        -   Since $K$ is small in many cases, but can be large, is there a simpler observation?
        -   If we sort $A$ and $B$ by their "depth" or "entry time" in the MST, does greedy matching work?
        -   Actually, for the minimax metric on a tree, the optimal matching can be found by a greedy strategy:
            1.  Root the MST.
            2.  For each node, maintain a list of unmatched $A$ and $B$ nodes in its subtree.
            3.  When merging lists from children, match as many $A$'s and $B$'s as possible *locally* (within the subtree) using the current edge weight? No, local matches use edges strictly below.
            4.  The key is that if we match two nodes in the same subtree, the cost is determined by edges inside that subtree. If we match across subtrees, the cost is determined by the LCA edge.
            5.  Greedy: Always match nodes that are "closest" in the tree structure?
            6.  Actually, a known result is that for this problem, we can simply compute the cost by iterating edges in increasing order and using Union-Find to track components.
            7.  For each component, track the number of available $A$ nodes and $B$ nodes.
            8.  When merging two components with an edge of weight $w$, any $A$ in one component matched with a $B$ in the other will have cost $w$ (since this is the smallest edge connecting them, and thus the minimax path will use this edge or a heavier one? No, if we process in increasing order, this is the *first* time they connect. So the minimax path weight is exactly $w$).
            9.  So, we can match $\min(countA_1, countB_2)$ pairs between component 1 and 2, and $\min(countA_2, countB_1)$ pairs between component 2 and 1?
            10. We want to maximize the number of matches formed at smaller weights.
            11. Algorithm:
                -   Sort MST edges by weight.
                -   Initialize Union-Find. Each node is a component.
                -   For each node, if it is in $A$, increment $compA[root]$. If in $B$, increment $compB[root]$.
                -   Iterate edges $(u, v)$ with weight $w$ in increasing order:
                    -   Find roots $r_u, r_v$.
                    -   If $r_u \neq r_v$:
                        -   We can match some $A$'s from $r_u$ with $B$'s from $r_v$, and vice versa.
                        -   To minimize total cost, we should match as many as possible now because future edges will be heavier.
                        -   Number of matches between $r_u$ and $r_v$:
                            -   $match1 = \min(compA[r_u], compB[r_v])$
                            -   $match2 = \min(compA[r_v], compB[r_u])$
                            -   Add $w \times (match1 + match2)$ to answer.
                            -   Update counts:
                                -   $compA[r_u] -= match1$
                                -   $compB[r_v] -= match1$
                                -   $compA[r_v] -= match2$
                                -   $compB[r_u] -= match2$
                            -   Merge components:
                                -   $newA = compA[r_u] + compA[r_v]$
                                -   $newB = compB[r_u] + compB[r_v]$
                                -   Union $r_u, r_v$ and set counts.
                -   This greedy works because any pair matched later will have a cost $\ge w$. By matching now, we "lock in" the lower cost $w$.