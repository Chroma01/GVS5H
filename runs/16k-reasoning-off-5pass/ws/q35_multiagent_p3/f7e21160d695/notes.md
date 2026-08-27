
## ideation
The core difficulty lies in efficiently computing the minimum weight perfect matching between two sets of nodes $A$ and $B$ in a graph where the cost between nodes is the minimax path weight.
1.  **Minimax Path Property**: The value $f(x, y)$ is determined by the Minimum Spanning Tree (MST). Specifically, it is the maximum edge weight on the unique path between $x$ and $y$ in the MST.
2.  **Matching on Tree Metric**: The problem reduces to matching nodes in $A$ to nodes in $B$ on the MST. A naive $O(K^2)$ or $O(K^3)$ approach is too slow given $K \le 2 \cdot 10^5$.
3.  **Greedy Strategy with DSU**: We can process the edges of the MST in increasing order of weight. Using a Disjoint Set Union (DSU) structure, we maintain the count of unmatched $A$ nodes and unmatched $B$ nodes in each connected component. When merging two components via an edge of weight $w$, we greedily match as many $A$ nodes from one component with $B$ nodes from the other (and vice versa) as possible. Since we process edges from smallest to largest, any match formed at this step incurs cost $w$, which is minimal for any pair that must cross this edge to connect. Unmatched nodes are carried over to larger components to be matched against nodes from higher up in the tree (or other branches) via heavier edges.
4.  **Complexity**: Building the MST takes $O(M \log M)$ or $O(M \alpha(N))$. Sorting edges takes $O(M \log M)$. The DSU operations take nearly constant time. The total complexity is dominated by sorting, $O(M \log M)$, which fits well within the time limits for $N, M \le 2 \cdot 10^5$.

## worker: (None)
The problem asks to minimize the sum of minimax path weights between pairs $(A_i, B_{\pi(i)})$.
1.  **Minimax Path**: The minimax path weight between two nodes in a graph is equal to the maximum edge weight on the unique path between them in the Minimum Spanning Tree (MST). Thus, we first construct the MST.
2.  **Matching on Tree**: We need to match nodes in set $A$ to nodes in set $B$ on the MST. The cost of a match is the max edge weight on the path.
3.  **Greedy Strategy**: We process the edges of the MST in increasing order of weight. We use a Disjoint Set Union (DSU) to maintain connected components. For each component, we track the number of unmatched $A$ nodes and unmatched $B$ nodes.
4.  **Merging Components**: When an edge of weight $w$ connects two components $C_1$ and $C_2$, any path between a node in $C_1$ and a node in $C_2$ must use this edge (or a heavier one if we wait, but we process smallest first). To minimize cost, we greedily match as many $A$ nodes from $C_1$ with $B$ nodes from $C_2$ and vice versa as possible. Each such match incurs a cost of $w$.
5.  **Updating Counts**: The matched nodes are removed from the pool of unmatched nodes. The remaining unmatched $A$ and $B$ nodes are carried over to the merged component. These will be matched against nodes from other branches via heavier edges later.
6.  **Complexity**: Sorting edges takes $O(M \log M)$. DSU operations are nearly constant time. The total time complexity is $O(M \log M)$, which is efficient enough for $N, M \le 2 \cdot 10^5$.
