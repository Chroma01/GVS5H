
## ideation
The core difficulty lies in correctly modeling the movement of balls and determining the minimum set of operations required to consolidate all balls into box $X$.

1.  **Graph Representation**:
    -   Red balls move according to permutation $P$. This defines a functional graph where each node $i$ has exactly one outgoing edge $i \to P_i$. Since $P$ is a permutation, this graph is a collection of disjoint cycles.
    -   Blue balls move according to permutation $Q$. Similarly, this defines a functional graph with edges $i \to Q_i$, also a collection of disjoint cycles.

2.  **Reachability Condition**:
    -   For a ball to end up in box $X$, it must be possible to reach $X$ from its starting box via the respective graph.
    -   In a functional graph composed of cycles, a node $i$ can reach node $X$ if and only if $i$ and $X$ are in the same cycle.
    -   Therefore, for the goal to be achievable:
        -   Every box $i$ containing red balls ($A_i=1$) must be in the same cycle as $X$ in the $P$-graph.
        -   Every box $j$ containing blue balls ($B_j=1$) must be in the same cycle as $X$ in the $Q$-graph.
    -   If any ball is in a different cycle than $X$, it can never reach $X$, making the goal impossible (output -1).

3.  **Minimum Operations**:
    -   An operation on box $k$ clears all balls from box $k$ and moves red balls to $P_k$ and blue balls to $Q_k$.
    -   Once a box is operated on, it becomes empty. Operating on an empty box is useless.
    -   We want to move all balls to $X$. We never need to operate on $X$ itself because the goal is to have all balls *in* $X$ and empty elsewhere. Operating on $X$ would move balls out of $X$, which is counter-productive.
    -   Consider the set of all boxes that initially contain at least one ball (red or blue). Let this set be $S_{initial}$.
    -   When we operate on a box $i \in S_{initial}$, the balls move to $P_i$ (red) and $Q_i$ (blue). If $P_i \neq X$, the red balls are now in box $P_i$. If box $P_i$ was not initially in $S_{initial}$, it now contains balls and must be operated on later (unless $P_i = X$).
    -   Essentially, we need to operate on every box that *ever* contains a ball, except $X$.
    -   Since the graphs are permutations (cycles), the path from any box $i$ in the same cycle as $X$ to $X$ is unique and consists of all nodes in that cycle.
    -   Specifically, if we operate on boxes in reverse order of their distance to $X$ (i.e., furthest first), we can funnel balls towards $X$.
    -   The set of boxes that will contain balls at some point are exactly the boxes in the cycles containing the initial balls.
    -   However, we don't necessarily need to operate on *every* box in the cycle. We only need to operate on boxes that *currently hold balls*.
    -   Let's trace the process:
        -   Start with balls in some set of boxes.
        -   Operate on a box $i$ holding balls. Balls move to $P_i$ and $Q_i$.
        -   If $P_i \neq X$, box $P_i$ now holds red balls. We must eventually operate on $P_i$ to move them closer to $X$ (or to $X$).
        -   This implies that for each red ball starting at $i$, we must operate on every box on the path from $i$ to $X$ in the $P$-graph, excluding $X$.
        -   Similarly for blue balls in the $Q$-graph.
        -   The total set of boxes we must operate on is the union of:
            -   All boxes on the paths from all red-ball sources to $X$ in the $P$-graph (excluding $X$).
            -   All boxes on the paths from all blue-ball sources to $X$ in the $Q$-graph (excluding $X$).
    -   Since the graph is a collection of cycles, the "path" from $i$ to $X$ is the sequence of nodes traversed from $i$ to $X$ along the cycle.
    -   If multiple balls start in the same cycle, their paths to $X$ overlap. We only count each box once.
    -   So, the algorithm is:
        1.  Identify the cycle containing $X$ in the $P$-graph. Check if all $i$ with $A_i=1$ are in this cycle. If not, return -1.
        2.  Identify the cycle containing $X$ in the $Q$-graph. Check if all $j$ with $B_j=1$ are in this cycle. If not, return -1.
        3.  Collect all nodes in the $P$-cycle of $X$. From these, exclude $X$. This is the set $S_P$.
        4.  Collect all nodes in the $Q$-cycle of $X$. From these, exclude $X$. This is the set $S_Q$.
        5.  Wait, is it the entire cycle?
            -   Consider Sample 1: $N=5, X=3$.
            -   $P$: $1\to4\to3\to2\to5\to1$. Cycle: $(1,4,3,2,5)$. All nodes are in the cycle.
            -   $Q$: $1\to3\to5\to1$ and $2\to4\to2$. Two cycles. $X=3$ is in $(1,3,5)$.
            -   Red balls at 2, 4. $P$-cycle of 3 is $\{1,2,3,4,5\}$. Path from 2 to 3 in $P$: $2\to5\to1\to4\to3$. Nodes: $\{2,5,1,4\}$.
            -   Path from 4 to 3 in $P$: $4\to3$. Nodes: $\{4\}$.
            -   Union for red: $\{1,2,4,5\}$.
            -   Blue balls at 3, 5. $Q$-cycle of 3 is $\{1,3,5\}$.
            -   Path from 3 to 3: empty (already there).
            -   Path from 5 to 3 in $Q$: $5\to1\to3$. Nodes: $\{5,1\}$.
            -   Union for blue: $\{1,5\}$.
            -   Total union: $\{1,2,4,5\} \cup \{1,5\} = \{1,2,4,5\}$. Size 4. Matches sample output.
            -   Note: The "path" is defined as the nodes visited *before* reaching $X$. If a ball starts at $X$, it doesn't need any operations.
    -   So, the answer is the size of the union of:
        -   For each $i$ with $A_i=1$: the nodes on the path from $i$ to $X$ in $P$-graph, excluding $X$.
        -   For each $j$ with $B_j=1$: the nodes on the path from $j$ to $X$ in $Q$-graph, excluding $X$.
    -   Optimization: Instead of tracing paths for each ball, we can just take the entire cycle containing $X$ in $P$ and $Q$, but we must be careful.
        -   In Sample 1, the $P$-cycle is the whole graph. The union of paths from all red sources (2 and 4) to 3 is $\{1,2,4,5\}$. This is the entire cycle minus $X$.
        -   Is it always the entire cycle minus $X$?
        -   Suppose red balls are only at $X$. Then the set is empty.
        -   Suppose red balls are at $i$ and $j$ in the same cycle. The union of paths from $i$ to $X$ and $j$ to $X$ covers all nodes in the cycle except $X$ IF and ONLY IF the paths cover the whole cycle.
        -   Actually, the path from $i$ to $X$ is unique. The union of paths from a subset of nodes in a cycle to a target node $X$ is the set of all nodes in the cycle that are "upstream" from $X$ relative to at least one source.
        -   In a cycle, "upstream" means following edges backwards from $X$.
        -   Let the cycle be $C_X$. The nodes in $C_X$ can be ordered by distance to $X$.
        -   The union of paths from a set of sources $S$ to $X$ is simply the set of all nodes in $C_X$ that appear before $X$ in the cycle traversal starting from any $s \in S$.
        -   Actually, it's simpler: In a functional graph (cycle), to move a ball from $i$ to $X$, we must operate on every node on the path from $i$ to $X$ (excluding $X$).
        -   The set of required operations for red balls is $\bigcup_{i: A_i=1} \text{Path}_P(i \to X) \setminus \{X\}$.
        -   The set of required operations for blue balls is $\bigcup_{j: B_j=1} \text{Path}_Q(j \to X) \setminus \{X\}$.
        -   We can compute this by:
            1.  Finding the cycle containing $X$ in $P$. Let this cycle be $C_P$.
            2.  If any $i$ with $A_i=1$ is not in $C_P$, return -1.
            3.  Similarly for $Q$ and $B$.
            4.  For the $P$-graph, identify all nodes in $C_P$ that are reachable from any $i$ with $A_i=1$ by following edges backwards from $X$? No, forward from $i$.
            5.  Actually, just simulate the "backward" reachability from $X$ in the cycle?
                -   In a cycle, the path from $i$ to $X$ consists of all nodes $v$ such that traversing from $v$ leads to $X$ before wrapping around? No.
                -   Let's just collect all nodes in the cycle $C_P$.
                -   If there are no red balls, the set is empty.
                -   If there are red balls, the union of paths from all red sources to $X$ is the set of all nodes in $C_P$ except $X$, **unless** the red balls are clustered such that some nodes in the cycle are never on a path from a red ball to $X$.
                -   Example: Cycle $1\to2\to3\to1$. $X=3$. Red ball at 2. Path $2\to3$. Nodes: $\{2\}$. Node 1 is not used.
                -   Red ball at 1. Path $1\to2\to3$. Nodes: $\{1,2\}$.
                -   Red balls at 1 and 2. Union: $\{1,2\}$.
                -   So, we need to find the "upstream" nodes in the cycle relative to the sources.
                -   In a cycle, if we fix $X$, the nodes are ordered $v_1, v_2, \dots, v_k$ where $v_k \to X$ is the last step? No.
                -   Let's define the path from $i$ to $X$ as the sequence of nodes $u$ such that $u$ is an ancestor of $X$ and a descendant of $i$ (including $i$, excluding $X$).
                -   In a cycle, this is a contiguous segment of the cycle ending at the node preceding $X$.
                -   The union of such segments for all $i$ with $A_i=1$ is the segment from the "furthest" source (in terms of path length to $X$) to the node preceding $X$.
                -   "Furthest" means the one that requires the most steps to reach $X$.
                -   So, for the $P$-cycle, find the maximum distance from any $i$ with $A_i=1$ to $X$. Let this max distance be $D_P$. The number of nodes is $D_P$.
                -   Wait, is it just the max distance?
                -   In a cycle, the path from $i$ to $X$ is unique. The length is $d(i, X)$. The nodes are the $d(i, X)$ nodes preceding $X$ in the cycle order starting from $i$.
                -   The union of paths from a set of sources is the path from the source with the largest distance to $X$ to $X$.
                -   Why? Because if $i$ has distance $d_i$ and $j$ has distance $d_j$ with $d_i > d_j$, the path from $i$ includes the path from $j$ if $j$ is on the path from $i$. In a cycle, if $j$ is on the path from $i$ to $X$, then $d_i = d_j + \text{dist}(i,j)$. If $j$ is not on the path, they are in different "branches" but in a simple cycle, there's only one path.
                -   Actually, in a simple cycle, for any two nodes $i, j$, one is on the path from the other to $X$ if and only if they are in the correct order.
                -   If we have multiple sources, the union of their paths to $X$ is the path from the source that is "furthest upstream" to $X$.
                -   So, for $P$, we find $\max \{ \text{dist}_P(i, X) \mid A_i = 1 \}$. If no red balls, 0.
                -   Similarly for $Q$, find $\max \{ \text{dist}_Q(j, X) \mid B_j = 1 \}$. If no blue balls, 0.
                -   The answer is the sum of these two maximums?
                -   Let's check Sample 1.
                    -   $P$-cycle: $1\to4\to3\to2\to5\to1$. $X=3$.
                    -   Distances to 3 in $P$:
                        -   $3\to2$: dist 0 (start at X)
                        -   $2\to5\to1\to4\to3$: dist 4? No.
                        -   Path $2 \to 5 \to 1 \to 4 \to 3$. Length 4. Nodes: 2,5,1,4.
                        -   Path $4 \to 3$. Length 1. Node: 4.
                        -   Red balls at 2, 4. Max dist is 4 (from node 2).
                    -   $Q$-cycle containing 3: $1\to3\to5\to1$.
                    -   Distances to 3 in $Q$:
                        -   $3\to5\to1\to3$.
                        -   Path $5 \to 1 \to 3$. Length 2. Nodes: 5,1.
                        -   Path $1 \to 3$. Length 1. Node: 1.
                        -   Blue balls at 3, 5.
                        -   Node 3 has dist 0.
                        -   Node 5 has dist 2.
                        -   Max dist is 2.
                    -   Total = $4 + 2 = 6$. But sample output is 4.
    -   Where is the error?
        -   The sets of nodes might overlap? No, $P$ and $Q$ are different graphs. The operations are on the same boxes, but the movement is different.
        -   Wait, the operation on box $i$ moves BOTH red and blue balls.
        -   If we operate on box $i$, we clear it.
        -   The cost is the number of unique boxes operated on.
        -   In Sample 1, the set of boxes operated on was $\{1, 2, 4, 5\}$.
        -   My calculation for $P$ gave nodes $\{2,5,1,4\}$.
        -   My calculation for $Q$ gave nodes $\{5,1\}$.
        -   The union is $\{1,2,4,5\}$. Size 4.
        -   So the answer is the size of the union of the two sets of nodes.
        -   Set $S_P = \{ v \in C_P \mid \exists i \text{ s.t. } A_i=1 \text{ and } v \text{ is on path } i \to X \}$.
        -   Set $S_Q = \{ v \in C_Q \mid \exists j \text{ s.t. } B_j=1 \text{ and } v \text{ is on path } j \to X \}$.
        -   Answer = $|S_P \cup S_Q|$.
        -   Since $S_P$ is a contiguous segment of the cycle $C_P$ ending at the node before $X$, and $S_Q$ is a contiguous segment of $C_Q$ ending at the node before $X$, we can compute the size of the union by iterating over the nodes in the cycles.
        -   However, $C_P$ and $C_Q$ are different cycles (or same nodes, different edges). The union is over the set of box indices.
        -   Algorithm:
            1.  Find cycle $C_P$ containing $X$. Check all $A_i=1$ are in $C_P$.
            2.  Find cycle $C_Q$ containing $X$. Check all $B_j=1$ are in $C_Q$.
            3.  Identify nodes in $C_P$ that are on the path from any red source to $X$. This is the set of nodes $v$ in $C_P$ such that the distance from $v$ to $X$ is $\le$ max distance from any red source to $X$. Actually, it's simpler: it's the set of nodes $v$ in $C_P$ such that $v$ is an ancestor of $X$ in the functional graph restricted to the cycle, and $v$ is reachable from some red source.
            4.  In a cycle, the path from $i$ to $X$ is unique. The union of paths from all red sources is the path from the "furthest" red source to $X$. Let $max\_dist_P$ be the maximum distance from any $i$ with $A_i=1$ to $X$. Then $S_P$ is the set of nodes on the path from that furthest source to $X$ (excluding $X$).
            5.  Similarly, $S_Q$ is the set of nodes on the path from the furthest blue source to $X$ (excluding $X$).
            6.  Compute $|S_P \cup S_Q|$.

## worker: Implement the solution: read input, build permutat
The problem involves moving balls from various boxes to a target box $X$ using two permutations $P$ and $Q$. Each operation on box $i$ moves red balls to $P_i$ and blue balls to $Q_i$. The goal is to empty all boxes except $X$.

1.  **Graph Structure**: Since $P$ and $Q$ are permutations, the graphs formed by edges $i \to P_i$ and $i \to Q_i$ are collections of disjoint cycles.
2.  **Reachability**: A ball can reach $X$ if and only if its starting box is in the same cycle as $X$ in the respective graph. If any ball is in a different cycle, it's impossible to move it to $X$, so we output -1.
3.  **Minimum Operations**:
    -   We never need to operate on box $X$.
    -   For red balls, if a ball starts at box $i$ in the same cycle as $X$, we must operate on every box on the unique path from $i$ to $X$ (excluding $X$).
    -   In a cycle, the path from $i$ to $X$ is a contiguous segment of the cycle ending at the node immediately preceding $X$ in the cycle order.
    -   If there are multiple red balls, the union of their paths is the path from the "furthest" red ball (the one with the longest path to $X$, or equivalently, the one with the smallest index in the cycle list starting from $X$) to $X$.
    -   Specifically, if we list the cycle nodes as $c_0=X, c_1, c_2, \dots, c_{m-1}$ where $c_{k+1} = P[c_k]$, then the path from $c_i$ to $X$ involves nodes $c_i, c_{i+1}, \dots, c_{m-1}$.
    -   The union of paths from all red balls is the path from the red ball with the minimum index $i_{min}$ to $X$. The set of nodes is $\{c_k \mid i_{min} \le k < m\}$.
    -   The same logic applies to blue balls with permutation $Q$.
    -   The total minimum operations is the size of the union of the sets of nodes required for red and blue balls.

The algorithm:
1.  Find the cycle containing $X$ for $P$ and $Q$.
2.  Check if all boxes with red/blue balls are in the respective cycles. If not, return -1.
3.  Find the minimum index in the cycle list for any box with a red ball (for $P$) and any box with a blue ball (for $Q$).
4.  Construct the sets of nodes required for red and blue operations.
5.  Return the size of the union of these two sets.

Complexity: $O(N)$ for finding cycles and processing balls.
