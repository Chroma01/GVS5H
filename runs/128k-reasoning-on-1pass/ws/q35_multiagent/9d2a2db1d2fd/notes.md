
## ideation


## worker: (none)
The problem asks for the minimum stairs cost to move between two floors in a grid of buildings. The key observation is that moving between adjacent buildings at the same floor is free (cost 0), while moving up/down floors costs 1 per floor. This implies that for a path of buildings, the cost is determined by the "bottleneck" height of the path. Specifically, if the minimum height of buildings on a path is $H_{max}$, then the minimum stairs cost is $|Y - Z|$ if $H_{max} \ge \min(Y, Z)$, otherwise it is $|Y - H_{max}| + |Z - H_{max}|$.

To find $H_{max}$ for any pair of buildings, we need to find the path between them that maximizes the minimum building height. This is a classic "bottleneck path" problem, which can be solved using a Maximum Spanning Tree (MST). The bottleneck capacity between any two nodes in a graph is given by the minimum edge weight on the unique path between them in the MST.

The algorithm proceeds as follows:
1. Construct a graph where nodes are buildings and edge weights are $\min(F_u, F_v)$.
2. Compute the MST using Kruskal's algorithm (sorting edges descending).
3. Preprocess the MST for LCA (Lowest Common Ancestor) queries with binary lifting to efficiently find the minimum edge weight on the path between any two nodes.
4. For each query, find the bottleneck height $H_{max}$ using LCA, and compute the answer based on the formula derived.

Complexity:
- Graph construction and MST: $O(HW \log(HW))$.
- LCA preprocessing: $O(HW \log(HW))$.
- Query processing: $O(Q \log(HW))$.
Total time complexity is well within limits for $H, W \le 500$ and $Q \le 2 \times 10^5$. Memory usage is optimized using `array` module for LCA tables.
