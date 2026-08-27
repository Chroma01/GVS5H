
## ideation
The problem asks for the minimum sum of bottleneck distances $f(A_i, B_{\pi(i)})$ over all permutations $\pi$. The bottleneck distance $f(u, v)$ corresponds to the maximum edge weight on the unique path between $u$ and $v$ in the Minimum Spanning Tree (MST) of the graph.

Key observations:
1.  **MST Property**: The value $f(u, v)$ is determined by the MST. Specifically, if we process MST edges in increasing order of weight, $f(u, v)$ is the weight of the edge that first connects the connected components containing $u$ and $v$.
2.  **Greedy Matching**: Since we want to minimize the sum of these weights, we should try to match pairs $(A_i, B_j)$ that are connected by small-weight edges. This suggests a greedy strategy using the structure of the MST.
3.  **Algorithm**:
    *   Construct the MST of the graph.
    *   Sort the edges of the MST by weight in ascending order.
    *   Use a Disjoint Set Union (DSU) data structure to maintain connected components.
    *   For each component, keep track of the number of unmatched vertices from set $A$ (let's call it `cntA`) and set $B` (let's call it `cntB`). Initially, for each vertex $v$, if $v \in A$, `cntA[v] = 1`, else 0; similarly for $B$.
    *   Iterate through the sorted MST edges. For an edge connecting components $C_u$ and $C_v$ with weight $w$:
        *   We can match any unmatched $A$ in $C_u$ with any unmatched $B$ in $C_v$, and vice versa.
        *   The number of such matches is $\min(\text{cntA}[C_u], \text{cntB}[C_v]) + \min(\text{cntA}[C_v], \text{cntB}[C_u])$.
        *   Add `matches * w` to the total answer.
        *   Update the counts for the merged component:
            *   New `cntA` = `cntA[C_u] + cntA[C_v] - matches`
            *   New `cntB` = `cntB[C_u] + cntB[C_v] - matches`
        *   Merge the two components in DSU.
    *   This greedy approach works because matching at a lower weight edge is always preferable to matching at a higher weight edge, and the "bottleneck" nature ensures that once two nodes are connected, their distance is fixed by the heaviest edge on the path, which is the current edge in the sorted iteration.

Complexity:
*   MST construction: $O(M \log M)$ or $O(M \alpha(N))$.
*   Sorting MST edges: $O(N \log N)$.
*   DSU operations: $O(N \alpha(N))$.
*   Total time complexity: $O(M \log M + N \log N)$, which fits within the limits for $N, M \le 2 \times 10^5$.

Pitfalls:
*   Ensure the graph is connected (guaranteed by constraints).
*   Handle the case where $A_i$ and $B_j$ might have duplicate vertices correctly by counting occurrences.
*   Use 64-bit integers for the sum to avoid overflow.

## worker: Implement Kruskal's algorithm to build the MST.
The solution leverages the property that the bottleneck distance $f(u, v)$ in a graph is equal to the maximum edge weight on the unique path between $u$ and $v$ in the Minimum Spanning Tree (MST). 

To minimize the sum $\sum f(A_i, B_{\pi(i)})$, we use a greedy strategy based on the MST structure:
1.  **Construct MST**: Using Kruskal's algorithm, we build the MST. This ensures that we consider edges in increasing order of weight, which is crucial for the bottleneck property.
2.  **Greedy Matching with DSU**: We maintain connected components using a Disjoint Set Union (DSU) structure. For each component, we track the number of unmatched vertices from set $A$ (`cntA`) and set $B` (`cntB`).
3.  **Process Edges**: As we iterate through the sorted MST edges, each edge connects two previously disjoint components. Any unmatched $A$-node in one component can be matched with any unmatched $B$-node in the other component. Since we process edges in increasing order of weight, matching them now incurs the smallest possible cost for these pairs.
4.  **Update State**: The number of matches is calculated as $\min(\text{cntA}[C_u], \text{cntB}[C_v]) + \min(\text{cntA}[C_v], \text{cntB}[C_u])$. These matched nodes are effectively removed from the pool of unmatched nodes in the new merged component. The cost contribution is `matches * edge_weight`.

This approach efficiently computes the minimum sum without explicitly solving the general assignment problem, which would be too slow. The time complexity is dominated by sorting the edges, $O(M \log M)$, and DSU operations, nearly linear.
