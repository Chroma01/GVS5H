
## ideation
The core difficulty lies in efficiently answering $2 \times 10^5$ queries on a $500 \times 500$ grid where each query asks for a path-dependent metric. A direct shortest-path algorithm per query is too slow ($O(Q \cdot HW \log(HW))$).

The key insight is that the problem can be decomposed into two parts:
1.  **Bottleneck Capacity**: The minimum stair usage depends on the "highest possible floor" we can maintain along a path from start to end. Specifically, if we can stay at floor $H_{max}$ throughout the path, the cost is determined by moving from start floor $Y$ to $H_{max}$ and then to end floor $Z$. The optimal $H_{max}$ is the maximum possible value such that there exists a path where every building has height at least $H_{max}$. This is the "bottleneck capacity" of the path.
2.  **Cost Calculation**: Once we find the maximum bottleneck height $B^*$ for the path between $(A,B)$ and $(C,D)$, the minimum stair usage is:
    -   $|Y - Z|$ if $B^* \ge \max(Y, Z)$ (we can stay at a floor between $Y$ and $Z$).
    -   $|Y - B^*| + |Z - B^*|$ if $B^* < \max(Y, Z)$ (we must drop to $B^*$ and then go up/down).

To find $B^*$ efficiently for many queries, we use an **offline Union-Find approach**:
-   Treat the grid as a graph where nodes are buildings and edges connect cardinal neighbors.
-   The weight of an edge between adjacent buildings $U$ and $V$ is $\min(F_U, F_V)$.
-   We want the path that maximizes the minimum edge weight (bottleneck).
-   Sort all edges in descending order of weight.
-   Use Union-Find to add edges one by one.
-   To answer queries efficiently, associate each query with its start and end nodes. When two components merge, check if any query has one endpoint in each component. If so, the current edge weight is the maximum bottleneck for that query (since we process edges from highest to lowest).

This approach runs in nearly linear time with respect to the number of edges and queries, making it feasible for the given constraints.

## worker: (none)
The problem asks for the minimum stair usage to travel between two floors in a grid of buildings. Moving between adjacent buildings at the same floor is free, but moving up/down within a building costs 1 per floor.

Key Insight:
1.  **Bottleneck Path**: The cost depends on the highest floor $B^*$ we can maintain along a path from start to end. This $B^*$ is the maximum possible value such that there exists a path where every building has height at least $B^*$. This is a "maximum bottleneck capacity" problem.
2.  **Cost Formula**:
    *   If $B^* \ge \max(Y, Z)$, we can stay at a floor between $Y$ and $Z$ throughout the path. The cost is simply $|Y - Z|$.
    *   If $B^* < \max(Y, Z)$, we must drop to floor $B^*$ (the highest possible floor we can sustain) and then go up to $Z$ (or down from $Y$). The cost is $|Y - B^*| + |Z - B^*|$.

Algorithm:
1.  **Graph Construction**: Treat each building as a node. Edges connect adjacent buildings with weight $\min(F_u, F_v)$.
2.  **Offline Union-Find**:
    *   Sort all edges by weight in descending order.
    *   Use Union-Find to add edges one by one.
    *   To answer queries efficiently, associate each query with its start and end nodes.
    *   When two components merge, check if any query has one endpoint in each component. If so, the current edge weight is the maximum bottleneck $B^*$ for that query.
    *   To make this efficient, store lists of queries in each component. When merging, iterate over the smaller list and check connectivity. This ensures near-linear time complexity.
3.  **Final Calculation**: For each query, use the found $B^*$ and the formula above to compute the answer.

Complexity:
*   Sorting edges: $O(E \log E)$ where $E \approx 2HW$.
*   Union-Find operations: Nearly $O(E \alpha(HW))$.
*   Query processing: Each query is processed once during merges. The total work is proportional to $O(Q \log(HW))$ due to the smaller-to-larger merging strategy.
*   Overall: $O(HW \log(HW) + Q \log(HW))$, which fits within the time limits for $H,W \le 500$ and $Q \le 2 \cdot 10^5$.
