1.  **Model the Problem**: The cost is purely the vertical movement (stairs). Horizontal movement (walkways) is free but constrained by building heights. We can view this as a shortest path problem on a graph where nodes are `(row, col, floor)`. However, the state space is too large ($500 \times 500 \times 10^6$).
2.  **Key Insight**: Notice that if we are at floor $X$ in building $(i,j)$, we can reach any adjacent building $(i',j')$ at floor $X$ if $F_{i',j'} \ge X$. This means we can effectively "teleport" horizontally at any floor $X$ to any building in the same connected component of buildings that all have height $\ge X$.
3.  **Reformulate**: For a query $(A, B, Y) \to (C, D, Z)$, we want to minimize $|Y - X_{start}| + |Z - X_{end}| + \text{cost to change floor between } X_{start} \text{ and } X_{end}$. Wait, actually, we can change floors anywhere. The total stair cost is the sum of absolute differences of floors used in each building.
4.  **Optimal Strategy**: The optimal path will involve going from $(A,B,Y)$ to some floor $h_1$ in $(A,B)$, then moving through a sequence of buildings, possibly changing floors in intermediate buildings, and finally arriving at $(C,D)$ at floor $Z$. Crucially, if we enter a building at floor $h$ and leave at floor $h$, the cost is 0 for that building. If we enter at $h_{in}$ and leave at $h_{out}$, the cost is $|h_{in} - h_{out}|$.
5.  **Simplified View**: We can think of this as finding a "common floor" $h$ that is reachable from both the start and end via walkways, such that the cost is $|Y - h| + |Z - h|$. However, we might change floors multiple times. Actually, it's more general: we can view the grid as a graph where edges exist between adjacent cells if they share a floor. But since walkways are free, we can stay at floor $h$ and move freely among all buildings with height $\ge h$.
6.  **Algorithm**: For a fixed floor $h$, let $S_h$ be the set of buildings with $F_{i,j} \ge h$. If the start and end buildings are in the same connected component of $S_h$, then we can travel from start to end staying at floor $h$ (after adjusting to $h$). The cost would be $|Y - h| + |Z - h|$. We want to minimize this over all valid $h$.
7.  **Efficiency**: $H, W \le 500$, $Q \le 2 \cdot 10^5$. We cannot iterate all $h$ for each query. Note that the optimal floor $h$ must be one of the floor values present in the buildings on the path, or specifically, related to $Y$ and $Z$. Actually, the function $f(h) = |Y - h| + |Z - h|$ is convex. The minimum is achieved when $h$ is between $Y$ and $Z$. If there exists a floor $h$ between $\min(Y,Z)$ and $\max(Y,Z)$ such that start and end are connected in $S_h$, the answer is $|Y-Z|$. If not, we might need to go to a higher floor.
8.  **Refined Algorithm**: 
    - For each query, we want to find $\min_h (|Y - h| + |Z - h|)$ subject to: $F_{A,B} \ge h$, $F_{C,D} \ge h$, and $(A,B)$ and $(C,D)$ are connected in the graph of buildings with height $\ge h$.
    - Since $|Y-h| + |Z-h|$ is minimized when $h$ is in $[ \min(Y,Z), \max(Y,Z) ]$, if there is any such $h$ where they are connected, the answer is $|Y-Z|$.
    - If they are not connected for any $h \in [\min(Y,Z), \max(Y,Z)]$, we must go to an $h > \max(Y,Z)$ or $h < \min(Y,Z)$. Given the structure, going higher is usually the way to connect components.
    - We can precompute connected components for each distinct height? No, too many heights.
    - Alternative: Use BFS/Dijkstra on the grid? The state is just $(i,j)$. The cost to move from $(i,j)$ to $(i',j')$ is 0 if we can walk. But we can change floors.
    - Let's define $D[i][j]$ as the minimum "adjusted floor" or something? No.
    - Let's reverse the thinking. For a fixed query, the answer is $\min_{h} (|Y-h| + |Z-h|)$ where $h$ is a "valid transit floor". A floor $h$ is valid if start and end are in the same component of buildings with height $\ge h$.
    - Let $H_{min}$ be the maximum floor $h$ such that start and end are connected in $S_h$. If $H_{min} \ge \min(Y,Z)$, then we can pick $h = \max(\min(Y,Z), \text{something})$. Actually, if they are connected at $H_{min}$, they are connected at all $h \le H_{min}$. So if $H_{min} \ge \min(Y,Z)$, we can choose $h$ in $[\min(Y,Z), \min(H_{min}, \max(Y,Z))]$. The cost is $|Y-Z|$.
    - If $H_{min} < \min(Y,Z)$, then for any $h \le H_{min}$, the cost is $(Y-h) + (Z-h) = Y+Z - 2h$. This is minimized by maximizing $h$, so $h = H_{min}$. Cost: $Y+Z - 2 H_{min}$.
    - So the answer is: if connected at $\min(Y,Z)$, answer is $|Y-Z|$. Else, answer is $Y+Z - 2 H_{max\_conn}$, where $H_{max\_conn}$ is the highest floor where they are connected.
    - How to find $H_{max\_conn}$? It is the maximum $h$ such that $(A,B)$ and $(C,D)$ are in the same component of $\{ (i,j) : F_{i,j} \ge h \}$. This is equivalent to finding the "bottleneck" capacity of the path. We can use a variant of Kruskal's or BFS. Specifically, we can binary search on $h$ and check connectivity. Or, we can precompute the "maximum bottleneck path" between all pairs? No, too many pairs.
    - However, $Q$ is large. We need a fast query.
    - Notice that connectivity at height $h$ is monotonic. We can binary search for the largest $h$ such that start and end are connected. The range of $h$ is $1$ to $10^6$. Binary search takes $O(\log(10^6))$ steps. Each step is a BFS/DFS on $500 \times 500$ grid, which is $2.5 \cdot 10^5$ nodes. $2 \cdot 10^5 \times 20 \times 2.5 \cdot 10^5$ is too slow.
    - We need a faster way. We can precompute connected components for all relevant heights? No.
    - Alternative: Use a Disjoint Set Union (DSU) approach. Sort all buildings by height descending. Add buildings one by one. But we have queries.
    - We can process queries offline. Sort queries by $\min(Y_i, Z_i)$? No.
    - Let's use the property: $H_{max\_conn}$ is the maximum value $h$ such that there is a path from start to end where every building on the path has height $\ge h$. This is the "bottleneck capacity" of the path. We can compute this for all pairs? No.
    - But we can run a multi-source BFS? No.
    - We can use Dijkstra-like algorithm to compute the "bottleneck distance" from a single source to all other nodes. But we have $Q$ queries.
    - Wait, $H, W \le 500$. Total nodes $250,000$. We can't run Dijkstra for each query.
    - However, note that the "bottleneck" between two nodes is determined by the minimum height on the path. We want the path that maximizes this minimum height. This is the "widest path" problem.
    - We can precompute the widest path from every node? No, $N^2$ is too big.
    - But we only have $Q$ queries. Can we answer them faster?
    - Actually, we can binary search the answer for each query. To check if two nodes are connected at height $h$, we do a BFS. $2 \cdot 10^5$ queries $\times 20$ steps $\times 2.5 \cdot 10^5$ ops is $10^{12}$, too slow.
    - We need a better approach.
    - Observation: The answer is either $|Y-Z|$ (if connected at $\min(Y,Z)$) or $Y+Z - 2 H_{max}$ (if not).
    - $H_{max}$ is the maximum height $h$ such that start and end are connected in $G_{\ge h}$.
    - We can use a Union-Find data structure. If we process heights in descending order, we can maintain connected components.
    - Offline processing:
        1. Collect all unique building heights. Sort them descending.
        2. Also collect all queries. For each query, we want to know the highest $h$ where start and end are connected.
        3. This is still hard because we need the specific $h$ for each pair.
    - Alternative: For each query, binary search $h$. To speed up connectivity check, we can use the fact that we only care about the component of the start node.
    - Actually, we can precompute the "component ID" for each node at each "critical" height? No.
    - Let's look at constraints again. $H,W \le 500$. $Q \le 2 \cdot 10^5$.
    - Maybe we can just run BFS for each query but optimize? No.
    - Let's use the DSU offline approach.
        - Create a list of events: building activations.
        - Sort buildings by $F_{i,j}$ descending.
        - Sort queries by... what?
        - We want to find the max $h$ such that start and end are connected.
        - This is equivalent to finding the max $h$ such that start and end are in the same component in the graph of buildings with height $\ge h$.
        - We can iterate $h$ from max possible down to 1. Add buildings with $F_{i,j} == h$. Union with neighbors.
        - But we have many queries. We can store queries and check if start and end are connected.
        - If we process all queries at each step, it's slow.
        - Instead, we can store for each query the current component of start and end. When they become same, record $h$.
        - But a query might become connected at a high $h$ and stay connected. We want the *first* time they become connected as we decrease $h$ (i.e., the highest $h$).
        - So, sort queries by nothing? Just process heights descending.
        - Maintain DSU. For each query, check if `find(start) == find(end)`. If yes, and we haven't recorded an answer for this query, record $h$ as the answer for $H_{max}$.
        - There are $Q$ queries. In each step of height, we might check $Q$ queries. Total steps = number of unique heights (up to $250,000$). $250,000 \times 200,000$ is too big.
    - Optimization: Only check queries that are not yet answered. Use a list of active queries.
    - But a query might be answered at a very high height.
    - This approach is $O(\text{Unique Heights} \times Q)$ in worst case.
    - However, note that once a query is answered, we remove it.
    - Is there a bound on total checks? Each query is checked until it is answered.
    - But we check all active queries at each height level.
    - This is still potentially slow.
    - Let's try a different perspective.
    - The "widest path" value between two nodes in a grid can be computed using a modified Dijkstra or BFS.
    - `max_bottleneck[u][v]`? No.
    - We can run a "Multi-Source Widest Path" from all nodes? No.
    - Given the time limit, perhaps the binary search per query with a fast connectivity check is the intended solution if the constant factor is small? Or maybe the number of unique heights is small? No, up to $10^6$.
    - Wait, we only care about heights that are present in the grid. There are at most $H \times W = 250,000$ distinct heights.
    - Let's stick with the offline DSU. To optimize, we can group buildings by height.
    - For each query, we want the largest $h$ such that they are connected.
    - We can binary search the answer for each query independently. The check is BFS.
    - $2 \cdot 10^5$ queries. Binary search 20 steps. BFS $2.5 \cdot 10^5$ nodes.
    - $2 \cdot 10^5 \times 20 \times 2.5 \cdot 10^5$ is way too big.
    - There must be a faster way.
    - What if we precompute the connected components for all "critical" heights?
    - Critical heights are the values of $F_{i,j}$.
    - We can use a Segment Tree or similar?
    - Actually, this problem is equivalent to finding the minimum of $|Y-h| + |Z-h|$ over $h$ in the set of "valid transit floors".
    - The set of valid transit floors for a pair $(S, E)$ is $\{ h \mid S \text{ and } E \text{ are connected in } G_{\ge h} \}$. This set is an interval $[1, H_{max}]$.
    - So we just need $H_{max}$.
    - How to compute $H_{max}$ for all queries fast?
    - This is the "maximum capacity path" problem.
    - We can use a variant of Kruskal's algorithm.
    - Sort all edges (adjacent buildings) by the minimum height of the two buildings.
    - Add edges to DSU.
    - When start and end of a query become connected, the current edge weight is $H_{max}$.
    - This is perfect!
    - Steps:
        1. Create edges between adjacent cells. Weight of edge $((i,j), (i',j'))$ is $\min(F_{i,j}, F_{i',j'})$.
        2. Sort all edges by weight descending.
        3. Initialize DSU with $H \times W$ nodes.
        4. Store queries. For each query, we want to know the weight of the edge that connects the component of start and end.
        5. We can process queries offline. For each query, we can check if start and end are connected.
        6. But we need to know *when* they become connected.
        7. We can iterate through sorted edges. After adding an edge, we check if any pending query has its start and end in the same component.
        8. To do this efficiently, we can maintain a list of queries per component? Or just check all queries?
        9. Checking all queries after each edge addition is too slow ($E \times Q$).
        10. Instead, for each query, we can just check if `find(start) == find(end)` after each union. But we only need to check queries that are not yet answered.
        11. We can use a "query list" for each component. When two components merge, we merge the query lists. If a query appears in both lists (i.e., its start is in one and end in the other), then it is now connected. The current edge weight is the answer for $H_{max}$.
        12. This is efficient. Total complexity $O(E \alpha(N) + Q \log Q)$ or similar.
    - Algorithm:
        - Nodes $0 \dots HW-1$.
        - Edges: for each adjacent pair, weight $w = \min(F_u, F_v)$.
        - Sort edges descending.
        - DSU with sets of queries. Each query $k$ is initially in the set of its start node $S_k$ and end node $E_k$? No, a query is associated with a pair.
        - Better: Each node in DSU maintains a list of "active queries" that have their start node in this component but not yet connected to their end node.
        - Actually, simpler: For each query $k$, let $u = S_k, v = E_k$. We want to find the first time $u$ and $v$ are in the same component.
        - We can store for each component a set of "pending queries" that have one endpoint in this component.
        - When merging component A and B with edge weight $w$:
            - For each query in A's list that is also in B's list? No.
            - A query $k$ has endpoints $u, v$. Initially, $u$ is in comp $C_u$, $v$ is in comp $C_v$.
            - If $C_u == C_v$, it's already connected (weight infinity? No, we process descending, so if they are connected, $H_{max}$ is at least the current max weight processed so far? No, we process descending, so the first time they connect is the MAX weight).
            - So, if $C_u == C_v$ at the start, $H_{max} = \infty$ (or effectively $10^6+1$).
            - Otherwise, we add query $k$ to the list of $C_u$ and $C_v$? No, we add it to a global list of pending queries?
            - Standard technique: "DSU with small-to-large merging of query lists".
            - Each component stores a map/dict: `query_id -> endpoint_in_this_component`.
            - When merging A and B:
                - For each query in the smaller list:
                    - If the query is also in the larger list, then this query is now connected. The answer for $H_{max}$ is the current edge weight.
                    - Otherwise, add the query to the larger list with the endpoint being the one in the current component.
            - This ensures each query is processed $O(\log N)$ times.
    - After finding $H_{max}$ for each query:
        - If $H_{max} \ge \min(Y, Z)$, answer is $|Y - Z|$.
        - Else, answer is $Y + Z - 2 H_{max}$.