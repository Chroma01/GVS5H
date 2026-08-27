
## ideation
The problem asks us to minimize the sum of bottleneck distances $f(A_i, B_i)$ by optimally permuting $B$. The function $f(u, v)$ is the minimum possible maximum edge weight on a path between $u$ and $v$. This value is determined by the Minimum Spanning Tree (MST) of the graph; specifically, $f(u, v)$ is the maximum weight of an edge on the unique path between $u$ and $v$ in the MST.

The core difficulty is that we need to find a permutation of $B$ that minimizes the sum of these bottleneck distances. Since $N, K \le 2 \times 10^5$, an $O(N^2)$ matching algorithm is too slow. We need a more efficient approach, likely related to the structure of the MST.

Key insights:
1.  **MST Property**: The bottleneck distance $f(u, v)$ depends only on the MST. We can first construct the MST using Kruskal's or Prim's algorithm.
2.  **Edge Contribution**: The total cost can be viewed as the sum of contributions of each edge in the MST. An edge $e$ with weight $w$ contributes $w$ to the cost of a pair $(A_i, B_j)$ if $e$ is the maximum weight edge on the path between $A_i$ and $B_j$.
3.  **Greedy Strategy with DSU**: We can process the edges of the MST in increasing order of weight. When we consider an edge $e=(u, v)$ with weight $w$, it merges two components $C_u$ and $C_v$.
    -   Any pair $(A_i, B_j)$ where $A_i \in C_u$ and $B_j \in C_v$ (or vice versa) will have $f(A_i, B_j) \ge w$. Since we process edges in increasing order, $w$ will be the maximum weight on the path for these pairs *unless* they are already connected by a heavier edge (which is impossible as we process in increasing order) or if they are matched within the components before this step.
    -   To minimize the total sum, we want to maximize the number of pairs that are matched *within* the components $C_u$ and $C_v$ before they are merged. This avoids paying the cost $w$ for those pairs.
    -   Let $cntA_x$ and $cntB_x$ be the number of $A$'s and $B$'s in component $x$.
    -   The maximum number of pairs we can form within $C_u$ is $\min(cntA_u, cntB_u)$. Similarly for $C_v$.
    -   The remaining $A$'s and $B$'s in $C_u$ and $C_v$ must be matched across the cut defined by $e$.
    -   Specifically, let $remA_u$ be the number of $A$'s in $C_u$ that are not matched with a $B$ in $C_u$, and $remB_u$ be the number of $B$'s in $C_u$ not matched with an $A$ in $C_u$. Note that $remA_u = \max(0, cntA_u - cntB_u)$ and $remB_u = \max(0, cntB_u - cntA_u)$.
    -   The number of pairs that *must* cross the cut (i.e., one endpoint in $C_u$ and one in $C_v$) is determined by how many unmatched $A$'s in $C_u$ can be matched with unmatched $B$'s in $C_v$, and vice versa.
    -   The number of crossing pairs is $\min(remA_u, remB_v) + \min(remA_v, remB_u)$.
    -   Each such crossing pair contributes $w$ to the total cost.
    -   After calculating the cost, we merge the components and update the counts.

This approach runs in $O(M \log M)$ or $O(M \alpha(N))$ due to sorting edges and DSU operations, which fits within the time limits.

## worker: Implement the solution in Python using the derived
The solution implements the greedy strategy derived in the thought process:
1.  **MST Construction**: The bottleneck distance $f(u, v)$ is determined by the Maximum Spanning Tree (or rather, the path in the Minimum Spanning Tree where the max edge is the bottleneck). We use Kruskal's algorithm to build the MST.
2.  **Greedy Matching with DSU**: We process MST edges in increasing order of weight. For each edge $e=(u, v)$ with weight $w$, it connects two components $C_u$ and $C_v$.
    -   We maintain the count of $A$'s and $B$'s in each component.
    -   Within each component, we can greedily match as many $A$'s and $B$'s as possible (min(countA, countB)).
    -   The remaining unmatched $A$'s and $B$'s must be matched across the cut defined by $e$ or in other components.
    -   Specifically, the number of pairs that *must* have $e$ as their bottleneck (i.e., one endpoint in $C_u$ and one in $C_v$) is calculated as $\min(\text{unmatched } A_u, \text{unmatched } B_v) + \min(\text{unmatched } A_v, \text{unmatched } B_u)$.
    -   We add $w \times \text{cross\_pairs}$ to the total cost.
    -   Finally, we merge the components and update the counts.
3.  **Complexity**: Sorting edges takes $O(M \log M)$. DSU operations take nearly constant time on average. The overall complexity is dominated by sorting, $O(M \log M)$, which fits well within the limits ($N, M \le 2 \times 10^5$).

## worker: Run the code against the provided sample inputs to
The solution implements the greedy strategy derived in the thought process:
1.  **MST Construction**: The bottleneck distance $f(u, v)$ is determined by the Maximum Spanning Tree (or rather, the path in the Minimum Spanning Tree where the max edge is the bottleneck). We use Kruskal's algorithm to build the MST.
2.  **Greedy Matching with DSU**: We process MST edges in increasing order of weight. For each edge $e=(u, v)$ with weight $w$, it connects two components $C_u$ and $C_v$.
    -   We maintain the count of $A$'s and $B$'s in each component.
    -   Within each component, we can greedily match as many $A$'s and $B$'s as possible (min(countA, countB)).
    -   The remaining unmatched $A$'s and $B$'s in $C_u$ and $C_v$ must be matched across the cut defined by $e$ or in other components.
    -   Specifically, the number of pairs that *must* have $e$ as their bottleneck (i.e., one endpoint in $C_u$ and one in $C_v$) is calculated as $\min(\text{unmatched } A_u, \text{unmatched } B_v) + \min(\text{unmatched } A_v, \text{unmatched } B_u)$.
    -   We add $w \times \text{cross\_pairs}$ to the total cost.
    -   Finally, we merge the components and update the counts.
3.  **Complexity**: Sorting edges takes $O(M \log M)$. DSU operations take nearly constant time on average. The overall complexity is dominated by sorting, $O(M \log M)$, which fits well within the limits ($N, M \le 2 \times 10^5$).

The logic handles the sample cases correctly:
-   Sample 1: MST edges (3,4,1), (1,3,2), (2,4,5).
    -   Edge (3,4,1): C3(A=1,B=0), C4(A=0,B=2). remA_u=1, remB_u=0. remA_v=0, remB_v=1. cross=min(1,1)+min(0,0)=1. Cost+=1. Merge -> C34(A=1,B=2).
    -   Edge (1,3,2): C1(A=2,B=0), C34(A=1,B=2). remA_u=2, remB_u=0. remA_v=0, remB_v=1. cross=min(2,1)+min(0,0)=1. Cost+=2. Merge -> C134(A=3,B=2).
    -   Edge (2,4,5): C2(A=0,B=1), C134(A=3,B=2). remA_u=0, remB_u=1. remA_v=1, remB_v=0. cross=min(0,0)+min(1,1)=1. Cost+=5.
    -   Total = 1 + 2 + 5 = 8. Correct.
-   Sample 2: MST edges (1,3,1), (2,3,2).
    -   Edge (1,3,1): C1(A=1,B=0), C3(A=0,B=1). remA_u=1, remB_u=0. remA_v=0, remB_v=1. cross=1. Cost+=1. Merge -> C13(A=1,B=1).
    -   Edge (2,3,2): C2(A=0,B=1), C13(A=1,B=1). remA_u=0, remB_u=1. remA_v=0, remB_v=0. cross=0. Cost+=0.
    -   Total = 1. Wait, Sample 2 output is 3.
    -   Let's re-trace Sample 2.
    -   Input: 3 3 2. Edges: (1,2,5), (2,3,2), (1,3,1). A=[1,1], B=[2,3].
    -   MST: (1,3,1), (2,3,2). (1,2,5) is skipped.
    -   Counts: A has 1 twice. B has 2 once, 3 once.
    -   Node 1: A=2, B=0. Node 2: A=0, B=1. Node 3: A=0, B=1.
    -   Edge (1,3,1): C1(A=2,B=0), C3(A=0,B=1).
        -   remA_u = max(0, 2-0) = 2. remB_u = 0.
        -   remA_v = 0. remB_v = 1.
        -   cross = min(2, 1) + min(0, 0) = 1.
        -   Cost += 1 * 1 = 1.
        -   Merge C1, C3 -> C13(A=2, B=1).
    -   Edge (2,3,2): C2(A=0,B=1), C13(A=2,B=1).
        -   remA_u = 0. remB_u = 1.
        -   remA_v = max(0, 2-1) = 1. remB_v = 0.
        -   cross = min(0, 0) + min(1, 1) = 1.
        -   Cost += 1 * 2 = 2.
        -   Total = 1 + 2 = 3. Correct.
