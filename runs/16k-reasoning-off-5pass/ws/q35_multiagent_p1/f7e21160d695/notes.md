
## ideation
The core difficulty lies in efficiently computing the minimum weight perfect matching between two sets of vertices $A$ and $B$ in a graph where the cost between two vertices is defined as the "bottleneck" distance (minimum possible maximum edge weight on a path).

1.  **Bottleneck Distance Property**: The value $f(x, y)$ is determined by the Minimum Spanning Tree (MST) of the graph. Specifically, $f(x, y)$ is the maximum edge weight on the unique path between $x$ and $y$ in the MST. This allows us to reduce the problem to a tree structure.
2.  **Matching on Tree**: We need to pair each node in $A$ with a unique node in $B$ to minimize the sum of bottleneck distances. Since the bottleneck distance corresponds to the weight of the edge that first connects two components in a Kruskal's-like process (processing MST edges from smallest to largest), we can use a greedy strategy.
3.  **Greedy Strategy with DSU**:
    *   Construct the MST of the graph.
    *   Sort the MST edges by weight in ascending order.
    *   Use a Disjoint Set Union (DSU) structure to maintain connected components.
    *   For each component, track the count of unmatched vertices from set $A$ ($cntA$) and set $B$ ($cntB$).
    *   When merging two components with an edge of weight $w$, we can form pairs between $A$-nodes in one component and $B$-nodes in the other. To minimize the total weight, we should form as many pairs as possible at the current smallest weight $w$.
    *   The number of pairs formed is $\min(cntA_{comp1}, cntB_{comp2}) + \min(cntA_{comp2}, cntB_{comp1})$.
    *   Add $pairs \times w$ to the total answer.
    *   Update the counts for the new merged component by subtracting the matched nodes.
4.  **Complexity**: Building the MST takes $O(M \log M)$ or $O(M \alpha(N))$. Sorting MST edges takes $O(N \log N)$. The DSU operations take nearly linear time. Total complexity is dominated by sorting, $O(M \log M)$, which fits within the constraints ($N, M \le 2 \times 10^5$).

## worker: Read input and build the graph.
The problem asks to minimize the sum of bottleneck distances between pairs of vertices from set $A$ and set $B$. The bottleneck distance $f(x, y)$ is the minimum possible maximum edge weight on a path between $x$ and $y$. This is a classic property of the Minimum Spanning Tree (MST): the path between any two nodes in the MST minimizes the maximum edge weight among all paths in the original graph.

Thus, the problem reduces to finding a minimum weight perfect matching in a bipartite graph where the cost is the bottleneck distance in the MST. Since $K$ can be up to $2 \times 10^5$, general matching algorithms are too slow. However, the bottleneck distance has a hierarchical structure. We can process the edges of the MST in increasing order of weight. When two components are merged by an edge of weight $w$, any pair of nodes $(a, b)$ with $a$ in one component and $b$ in the other will have their bottleneck distance determined by this edge $w$ (since it's the first time they are connected in the increasing weight order).

To minimize the total sum, we should greedily match as many pairs as possible at the current smallest weight $w$. For two components being merged, we can form pairs between $A$-nodes in the first component and $B$-nodes in the second, and vice versa. The number of such pairs is $\min(cntA_1, cntB_2) + \min(cntA_2, cntB_1)$. We add $pairs \times w$ to the answer and update the remaining counts of unmatched $A$ and $B$ nodes in the new merged component. This greedy approach works because matching a pair at a smaller weight is always better than or equal to matching it at a larger weight.

The complexity is dominated by sorting the edges for Kruskal's algorithm, which is $O(M \log M)$. The DSU operations are nearly linear. This fits within the time limits.
