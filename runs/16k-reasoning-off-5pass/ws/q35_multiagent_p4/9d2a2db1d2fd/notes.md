
## ideation
The core difficulty lies in efficiently answering connectivity queries for a grid graph where connectivity depends on a threshold height $h$. Specifically, for each query, we need to find the maximum height $H_{max}$ such that the start and end buildings are connected via a path of buildings all having height $\ge H_{max}$. This is known as the "bottleneck capacity" or "widest path" problem.

Given the constraints ($H, W \le 500$, $Q \le 2 \cdot 10^5$), a per-query BFS or Dijkstra is too slow ($O(Q \cdot HW)$). We need an offline approach.

The key insight is to process the grid edges in descending order of their "capacity" (where the capacity of an edge between adjacent buildings is $\min(F_{u}, F_{v})$). As we add edges, we maintain connected components using a Disjoint Set Union (DSU) data structure. We can determine the $H_{max}$ for each query by finding the specific edge that first connects the start and end components.

To efficiently track which queries become connected, we can associate each DSU component with a list of "pending queries" that have one endpoint in that component. When two components merge, we check for queries present in both lists (indicating the start and end are now connected). Using small-to-large merging for these lists ensures the total complexity is nearly linear in the number of edges and queries.

Once $H_{max}$ is found for a query $(A, B, Y) \to (C, D, Z)$:
1. If $H_{max} \ge \min(Y, Z)$, the optimal strategy is to go to a floor $h$ between $Y$ and $Z$ (which is reachable), so the cost is $|Y - Z|$.
2. If $H_{max} < \min(Y, Z)$, we must go up to $H_{max}$ to cross the bottleneck, so the cost is $(Y - H_{max}) + (Z - H_{max}) = Y + Z - 2 H_{max}$.

Pitfalls to avoid:
- Incorrectly defining edge weights (must be $\min(F_u, F_v)$).
- Inefficiently merging query lists (must use small-to-large).
- Handling queries where start and end are already in the same component initially (though the problem states distinct locations, they might be in the same component if $H_{max}$ is effectively infinite or very high; however, since we process descending, if they are already connected, $H_{max}$ is effectively $\infty$ or the max possible height, so the condition $H_{max} \ge \min(Y,Z)$ will hold). Note: If start and end are the same node, cost is 0, but constraints say distinct. If they are in the same component from the start (before any edges? No, initially each node is its own component), we need to handle the case where they are already connected. Actually, initially no two distinct nodes are connected. So we always find a finite $H_{max}$ unless the grid is disconnected even at height 1? No, the grid is connected at height 1 if all $F_{i,j} \ge 1$. So $H_{max} \ge 1$.

## worker: (None)
The solution uses an offline approach with Disjoint Set Union (DSU) to solve the "widest path" or "bottleneck capacity" problem for each query.
1.  **Graph Construction**: The grid is treated as a graph where nodes are buildings and edges connect adjacent buildings. The weight of an edge is the minimum height of the two connected buildings, representing the maximum floor level at which one can walk between them.
2.  **Processing Order**: Edges are sorted in descending order of their weights. This allows us to process the "strongest" connections first.
3.  **DSU with Query Tracking**: We maintain connected components using DSU. Each component tracks a list of "pending queries" that have one endpoint in that component. When two components merge via an edge of weight $w$, we check if any pending query has its other endpoint in the newly merged component. If so, that query is now connected, and $w$ is the maximum bottleneck height $H_{max}$ for that query. Small-to-large merging ensures this step is efficient ($O(Q \log Q)$ or similar).
4.  **Answer Calculation**: For each query, once $H_{max}$ is determined:
    *   If $H_{max} \ge \min(Y, Z)$, we can transit at a floor between $Y$ and $Z$, so the cost is simply $|Y - Z|$.
    *   If $H_{max} < \min(Y, Z)$, we must go up to $H_{max}$ to cross the bottleneck, so the cost is $(Y - H_{max}) + (Z - H_{max})$.
5.  **Complexity**: Sorting edges takes $O(HW \log(HW))$. DSU operations are nearly linear. The merging of query lists takes $O(Q \log(HW))$ due to small-to-large merging. Total complexity is dominated by sorting and DSU, well within limits for $H,W \le 500$ and $Q \le 2 \cdot 10^5$.
