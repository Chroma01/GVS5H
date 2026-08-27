
## ideation
The problem asks for the minimum stair moves between two floors in two different buildings (or the same building) in a grid. We can move vertically within a building (cost = floor difference) or horizontally to an adjacent building if the current floor $X$ is $\le$ the height of the adjacent building (cost = 0).

**Core Difficulty:**
The cost function involves both vertical movement and horizontal transitions. The key insight is that horizontal transitions are "free" but constrained by the minimum height of the buildings involved. If we decide to switch between a sequence of buildings, we must do so at a floor level $h$ that is valid for all buildings in the sequence (i.e., $h \le \min(\text{heights})$). To minimize the total stair cost $|Y - h| + |Z - h|$, we want to maximize $h$. Thus, the problem reduces to finding a path of buildings between the start and end buildings that maximizes the minimum height of any adjacent pair on the path. This is the "bottleneck capacity" of the path.

**Candidate Approaches:**
1.  **Maximum Spanning Tree (MST):** Construct a graph where nodes are buildings and edges between adjacent buildings have weight equal to the minimum of their heights. The maximum bottleneck capacity between any two nodes is determined by the path in the Maximum Spanning Tree.
    *   Build the graph ($HW$ nodes, $4HW$ edges).
    *   Run Kruskal's algorithm to find the MST.
    *   Preprocess the MST for LCA (Lowest Common Ancestor) queries to find the minimum edge weight on the path between any two nodes efficiently.
    *   For each query, calculate the bottleneck $B$. If $B \ge \min(Y, Z)$, the answer is $|Y - Z|$. Otherwise, the answer is $|Y - B| + |Z - B|$.
    *   Complexity: $O(HW \log(HW) + Q \log(HW))$. Given constraints ($HW \le 250,000$, $Q \le 200,000$), this is efficient enough.

2.  **Dijkstra/BFS:** Since we need to answer many queries, running a shortest path algorithm per query is too slow ($O(Q \cdot HW)$). We would need to precompute all-pairs shortest paths, which is $O((HW)^2)$, too slow.

**Pitfalls:**
*   **Recursion Depth:** The DFS for LCA preprocessing might hit recursion limits on large grids ($500 \times 500$). Need to increase recursion limit or use an iterative DFS/BFS.
*   **Node Mapping:** Correctly mapping $(r, c)$ to a unique integer $0 \dots HW-1$.
*   **Edge Cases:** Start and end in the same building ($|Y-Z|$). Start and end in adjacent buildings.
*   **Input Parsing:** Efficiently reading large inputs in Python.

## worker: Implement the solution using the MST + LCA approac
1.  **Algorithm Selection**: The problem is modeled as finding a path between two nodes in a grid graph that maximizes the minimum edge weight (bottleneck capacity). This is solved using a Maximum Spanning Tree (MST). The MST ensures that the path between any two nodes has the maximum possible bottleneck capacity.
2.  **Graph Construction**: Nodes represent buildings $(i, j)$. Edges connect adjacent buildings with weight $\min(F_{i,j}, F_{neighbor})$.
3.  **MST Construction**: Kruskal's algorithm is used with Union-Find to build the MST efficiently.
4.  **Query Processing**: For each query, we find the bottleneck capacity between the start and end buildings using LCA (Lowest Common Ancestor) on the MST.
    *   If the bottleneck $B \ge \min(Y, Z)$, the cost is simply $|Y - Z|$.
    *   If $B < \min(Y, Z)$, the cost is $|Y - B| + |Z - B|$.
5.  **Complexity**:
    *   Sorting edges: $O(HW \log(HW))$.
    *   MST Construction: $O(HW \alpha(HW))$.
    *   Preprocessing (LCA): $O(HW \log(HW))$.
    *   Queries: $O(Q \log(HW))$.
    *   Total time complexity fits well within limits for $H, W \le 500$ and $Q \le 2 \times 10^5$.
6.  **Edge Cases**: Handled same building case explicitly. Used BFS for tree traversal to avoid recursion depth issues.

## worker: Run the code against the provided sample input to 
The solution implements the Maximum Spanning Tree (MST) approach to solve the problem efficiently.
1.  **Graph Construction**: The grid is treated as a graph where each building is a node. Edges connect adjacent buildings with a weight equal to the minimum height of the two buildings involved. This weight represents the maximum floor level at which one can switch between these two buildings.
2.  **MST**: Using Kruskal's algorithm, we build the Maximum Spanning Tree. The path between any two nodes in the MST maximizes the bottleneck capacity (the minimum edge weight on the path). This is crucial because to minimize stair usage, we want to traverse as high as possible to minimize the vertical distance $|Y-h| + |Z-h|$.
3.  **LCA & Binary Lifting**: To answer queries efficiently ($O(\log N)$), we preprocess the MST using Binary Lifting to support LCA (Lowest Common Ancestor) queries and finding the minimum edge weight on the path between any two nodes.
4.  **Query Logic**: For a query starting at floor $Y$ in building $u$ and ending at floor $Z$ in building $v$:
    *   Calculate the bottleneck capacity $B$ between $u$ and $v$.
    *   If $B \ge \min(Y, Z)$, it means we can reach a common floor level that is at least as high as the lower of the two starting/ending floors. In this case, the optimal path cost is simply $|Y - Z|$.
    *   If $B < \min(Y, Z)$, we are forced to drop down to floor $B$ to switch buildings. The cost becomes $|Y - B| + |Z - B| = (Y - B) + (Z - B)$.
5.  **Complexity**:
    *   Sorting edges: $O(HW \log(HW))$.
    *   MST Construction: $O(HW \alpha(HW))$.
    *   Preprocessing: $O(HW \log(HW))$.
    *   Queries: $O(Q \log(HW))$.
    *   Given constraints ($H, W \le 500$, $Q \le 2 \times 10^5$), this approach is well within the time limits.

## worker: finalize
The solution implements the Maximum Spanning Tree (MST) approach to solve the problem efficiently.
1.  **Graph Construction**: The grid is treated as a graph where each building is a node. Edges connect adjacent buildings with a weight equal to the minimum height of the two buildings involved. This weight represents the maximum floor level at which one can switch between these two buildings.
2.  **MST**: Using Kruskal's algorithm, we build the Maximum Spanning Tree. The path between any two nodes in the MST maximizes the bottleneck capacity (the minimum edge weight on the path). This is crucial because to minimize stair usage, we want to traverse as high as possible to minimize the vertical distance $|Y-h| + |Z-h|$.
3.  **LCA & Binary Lifting**: To answer queries efficiently ($O(\log N)$), we preprocess the MST using Binary Lifting to support LCA (Lowest Common Ancestor) queries and finding the minimum edge weight on the path between any two nodes.
4.  **Query Logic**: For a query starting at floor $Y$ in building $u$ and ending at floor $Z$ in building $v$:
    *   Calculate the bottleneck capacity $B$ between $u$ and $v$.
    *   If $B \ge \min(Y, Z)$, it means we can reach a common floor level that is at least as high as the lower of the two starting/ending floors. In this case, the optimal path cost is simply $|Y - Z|$.
    *   If $B < \min(Y, Z)$, we are forced to drop down to floor $B$ to switch buildings. The cost becomes $|Y - B| + |Z - B| = (Y - B) + (Z - B)$.
5.  **Complexity**:
    *   Sorting edges: $O(HW \log(HW))$.
    *   MST Construction: $O(HW \alpha(HW))$.
    *   Preprocessing: $O(HW \log(HW))$.
    *   Queries: $O(Q \log(HW))$.
    *   Given constraints ($H, W \le 500$, $Q \le 2 \times 10^5$), this approach is well within the time limits.
