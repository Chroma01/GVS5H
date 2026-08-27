
## ideation
The core difficulty lies in efficiently computing the minimum weight perfect matching where the cost between two nodes is the minimax path weight (bottleneck distance) in a graph.

1.  **Minimax Path Property**: The value $f(x, y)$ is equal to the weight of the heaviest edge on the unique path between $x$ and $y$ in the Minimum Spanning Tree (MST) of the graph. This allows us to reduce the problem to a tree structure.
2.  **Greedy Matching on MST**: Instead of computing all pairwise distances (which is $O(K^2)$ and too slow for $K \approx 2 \cdot 10^5$), we can use a Union-Find (Disjoint Set Union) approach processing the MST edges in increasing order of weight.
3.  **Union-Find Strategy**:
    *   Construct the MST using Kruskal's algorithm.
    *   Initialize each vertex as a separate component. Track the count of unmatched $A$-nodes ($cntA$) and $B$-nodes ($cntB$) in each component.
    *   Iterate through MST edges from smallest to largest weight $w$.
    *   For an edge connecting components $C_u$ and $C_v$, we can form matches between $A$-nodes in $C_u$ and $B$-nodes in $C_v$, and vice versa.
    *   Since we process edges in increasing order, any match formed now has a cost of exactly $w$ (as this is the first time these two sets of nodes are connected in the MST, making $w$ the bottleneck).
    *   To minimize the total sum, we should maximize the number of matches formed at smaller weights. Thus, we greedily match as many pairs as possible between the two components using the current edge weight $w$.
    *   Update the counts of remaining unmatched nodes and merge the components.
4.  **Complexity**: Sorting edges takes $O(M \log M)$. The Union-Find operations take nearly linear time. The matching logic is $O(1)$ per edge. Total complexity is $O(M \log M + N \alpha(N))$, which fits well within the constraints.

## worker: Read input: N, M, K, edges, A sequence, B sequence
The problem asks to minimize the sum of minimax path weights between pairs $(A_i, B_{\pi(i)})$. The minimax path weight $f(x, y)$ is determined by the Maximum Spanning Tree (or rather, the path in the Minimum Spanning Tree where the cost is the max edge weight). Specifically, $f(x, y)$ is the weight of the heaviest edge on the unique path between $x$ and $y$ in the MST.

We can solve this using a greedy approach with Union-Find (Disjoint Set Union):
1.  **MST Construction**: Sort all edges by weight. We don't need to explicitly build the MST if we just process edges in increasing order, as Kruskal's algorithm effectively builds it.
2.  **Component Tracking**: Maintain disjoint sets of vertices. For each set (component), track the number of available $A$-nodes and $B$-nodes.
3.  **Greedy Matching**: Iterate through edges from smallest weight to largest. When an edge connects two previously disconnected components $C_u$ and $C_v$ with weight $w$:
    *   Any $A$-node in $C_u$ matched with a $B$-node in $C_v$ will have a path whose bottleneck is at least $w$. Since this is the first time they are connected in the MST, the bottleneck is exactly $w$.
    *   To minimize the total cost, we should maximize the number of matches formed at smaller weights.
    *   Therefore, we greedily match $\min(cntA[C_u], cntB[C_v])$ pairs and $\min(cntA[C_v], cntB[C_u])$ pairs.
    *   Add $w \times (\text{number of matches})$ to the total cost.
    *   Update the counts of remaining unmatched nodes and merge the two components.
4.  **Complexity**: Sorting edges takes $O(M \log M)$. The Union-Find operations are nearly constant time. The matching logic is $O(1)$ per edge. Total time complexity is $O(M \log M + N \alpha(N))$, which is efficient enough for $N, M \le 2 \cdot 10^5$.
