
## ideation
The problem asks to minimize the sum of bottleneck path weights between pairs of vertices $(A_i, B_{\pi(i)})$ for some permutation $\pi$. The bottleneck path weight $f(x, y)$ is the minimum possible maximum edge weight on a path between $x$ and $y$. This value is equal to the maximum edge weight on the unique path between $x$ and $y$ in the Minimum Spanning Tree (MST) of the graph.

We can solve this by constructing the MST and processing its edges in increasing order of weight. We maintain the connected components of the graph using a Disjoint Set Union (DSU) structure. For each component, we track the number of $A$ vertices and $B$ vertices it contains.

When an edge with weight $w$ connects two components $C_1$ and $C_2$, any $A$ vertex in $C_1$ can be matched with any $B$ vertex in $C_2$ (and vice versa) with a bottleneck cost of $w$. This is because $w$ is the weight of the edge that first connects their components in the MST construction process. To minimize the total cost, we greedily match as many pairs as possible using the current smallest edge weight. The number of such pairs we can form is $\min(|A \cap C_1|, |B \cap C_2|) + \min(|A \cap C_2|, |B \cap C_1|)$. We update the counts of $A$ and $B$ vertices in the merged component and add the cost to the total.

This approach has a time complexity of $O(M \log M)$ due to sorting the edges, and nearly linear time for DSU operations, which is efficient for the given constraints.

## worker: (none)
The problem asks to minimize the sum of bottleneck path weights between pairs $(A_i, B_{\pi(i)})$. The bottleneck distance $f(x, y)$ is equal to the maximum edge weight on the unique path between $x$ and $y$ in the Minimum Spanning Tree (MST). 

We can solve this by processing the MST edges in increasing order of weight using a Disjoint Set Union (DSU) structure. Initially, each vertex is in its own component, and we track the number of $A$ and $B$ vertices in each component. When an edge with weight $w$ connects two components $C_1$ and $C_2$, it becomes the bottleneck for any path between vertices in $C_1$ and $C_2$. To minimize the total cost, we greedily match as many pairs as possible using this edge weight. The number of pairs we can form is $\min(|A \cap C_1|, |B \cap C_2|) + \min(|A \cap C_2|, |B \cap C_1|)$. After matching, we update the counts of remaining $A$ and $B$ vertices in the merged component and add the cost to the total. This greedy strategy is optimal because any pair matched at this stage cannot be matched with a smaller bottleneck weight later.

Time Complexity: $O(M \log M)$ for sorting edges, plus nearly linear DSU operations. Overall $O(M \log M)$, which fits within the constraints.
Space Complexity: $O(N + M)$ for storing edges and DSU structures.
