
## ideation
**Core difficulty:**  
We need to match K vertices from two groups A and B (with possibly repeated vertices) to minimize the sum of bottleneck distances. The bottleneck distance between any two vertices is the minimum possible maximum edge weight on a path connecting them. This is a classic MST property: the minimum bottleneck path between any two vertices lies within the MST, and the bottleneck value equals the maximum edge weight on the unique MST path.

**Key insight (Kruskal tree / Boruvka tree):**  
Build a binary tree via Kruskal's algorithm: sort edges by weight, and when joining two components with an edge of weight w, create a new node with weight w that becomes the parent of the two component roots. The final tree has 2N−1 nodes, leaves are the original vertices, internal nodes have a weight. For any two original vertices, the weight of their lowest common ancestor (LCA) in this tree equals their bottleneck distance f(x,y).

**Reduction:**  
The problem becomes: on a rooted tree where each leaf has a label (either A or B), pair up A-leaves and B-leaves. For each pair, the cost is the weight of their LCA. We want to minimize the total cost over all K pairs (each leaf used exactly once, but the multiset of B can be permuted freely).

**DP on the tree:**  
At each node, we consider its children. Let `cntA` and `cntB` be the net surplus of A-leaves and B-leaves from the children’s subtrees. The node itself may also be a leaf (if it’s an original vertex). We can match a surplus A from one child with a surplus B from another child at cost equal to the node's weight. Greedily, we match as many cross pairs as possible. The number of matches at this node is `min(cntA, cntB)`. The unmatched surplus propagates to the parent. The total cost is the sum over all internal nodes of `weight * matches`.

**Pitfalls:**  
- K can be up to N, and vertices can repeat in A and B sequences.  
- The graph has up to 2×10^5 edges, so the Kruskal tree has up to 4×10^5 nodes.  
- Need efficient LCA preprocessing for the tree to compute matches, or more efficiently, we can process bottom-up with the DP described above without explicit LCA queries (since we just propagate counts).  
- The DP described automatically computes the sum of LCA weights when matching pairs greedily by always pairing as early (deep) as possible.

**Final algorithm:**  
1. Read the graph.  
2. Build the Kruskal tree using a DSU: sort edges by weight, for each edge (u, v, w), if u and v are in different components, create a new node with weight w, set its two children to the current roots of u and v, update the DSU parent to the new node.  
3. Read arrays A and B of length K.  
4. Perform a DFS on the Kruskal tree. For each node, if it is a leaf (original vertex), add its contribution to `cntA` or `cntB` according to its membership in the A-list or B-list. For internal nodes, let `a = sum of cntA from children`, `b = sum of cntB from children`. The node contributes `min(a, b) * weight` to the answer. Then propagate the surplus: `cntA = a - min(a, b)`, `cntB = b - min(a, b)` upward.  
5. Output the total sum.

The algorithm runs in O((N+M) log N) due to sorting, and O(N+M) for the DFS. It uses O(N+M) memory.

## worker: Implement the solution in Python: read input, buil
The Kruskal tree construction correctly creates a binary tree where internal nodes have weights. The DSU tracks which tree node represents each component. The bottom-up DFS computes the answer by greedily matching A and B leaves at each internal node at minimum cost.
