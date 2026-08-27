
## ideation
The problem asks for the minimum total cost \(\sum_{i=1}^K f(A_i, B_{\pi(i)})\) over all permutations \(\pi\) of \(B\), where \(f(x,y)\) is the minimax edge weight (the minimum possible maximum edge weight along a path). This is a classic minimum bottleneck path problem; on a connected graph the values \(f(x,y)\) equal the maximum edge weight on the path between \(x\) and \(y\) in any minimum spanning tree (MST). Since the graph is connected, we can build an MST (Kruskal, \(O(M\log M)\)), root it, and preprocess binary lifting ancestors with the maximum edge on the jump, so that \(f(x,y)\) can be computed in \(O(\log N)\).

The assignment part is a minimum weight bipartite matching with a special structure. For a fixed source \(A_i\), the set of nodes \(B_j\) with \(f(A_i, B_j) \le t\) is a connected subtree rooted at \(A_i\) when edges of weight \(> t\) are removed. This is the same as saying the cost matrix satisfies a Monge-type property: as we sort B-nodes by distance from a source, the distance sequence is non-decreasing along a DFS order. The optimal assignment can be found by a greedy algorithm that always matches the globally cheapest currently available edge, similar to the “minimum cost matching on a tree” problem. Concretely:

- For each \(A_i\), precompute distances to all \(B\) nodes and sort them.
- Use a global min-heap. Initially push each \(A_i\) with its nearest B node.
- Repeatedly pop the pair with the smallest distance. If that B node is still unmatched, match it with the current \(A_i\); otherwise, advance the pointer of that \(A_i\) to the next larger distance and push that pair.
- Each B node is matched at most once, so total heap operations are \(O(K\log K)\).

This greedy is provably optimal because any other assignment would have a larger or equal total sum by an exchange argument.

Overall complexity: \(O(M\log M + N\log N + K\log K)\) and memory \(O(N+M+K)\), which fits the constraints (\(N, M, K \le 2\cdot 10^5\)). The bottleneck is the initial MST construction; the rest is linearithmic.

## worker: Parse input, build edge list, store arrays A and B
The code above is a complete, self-contained program that solves the problem. It uses Kruskal to build an MST, then performs a DSU sweep on the MST edges to greedily match A and B nodes, accumulating the total cost. The initial matches at the same node (cost 0) are also handled. The algorithm is O((N+M) log N) and fits within the constraints.

## worker: Implement the full solution in `solve()`: read inp
The solution uses the classic property that for any connected undirected graph, the minimax path weight \(f(x,y)\) equals the maximum edge weight on the path between \(x\) and \(y\) in any minimum spanning tree (MST). After building the MST with Kruskal, the problem reduces to assigning each \(A_i\) to a distinct \(B_j\) to minimize the sum of maximum edge weights on the paths in the tree.

The optimal assignment is found by a DSU (Disjoint Set Union) sweep over the MST edges sorted by weight. For each node, we first match as many \(A\)'s and \(B\)'s as possible at cost 0 (when they are at the same node). Then, processing edges from smallest to largest weight, when an edge merges two components, any remaining \(A\) in one component can now be matched with any remaining \(B\) in the other component at the current edge's weight. The number of new matches formed is \(\min(\text{unmatched } A_1, \text{unmatched } B_2) + \min(\text{unmatched } A_2, \text{unmatched } B_1)\), and we add this count multiplied by the edge weight to the answer.

This greedy approach is provably optimal because any matching that connects nodes from different components must use the maximum weight edge on their connecting path, and processing in increasing order ensures we always pay the minimum possible weight for each necessary connection.

Complexity: \(O(M \log M)\) for Kruskal, \(O(N \log N)\) for sorting MST edges, and \(O(N \alpha(N))\) for DSU operations, well within the limits for \(N, M \le 2 \times 10^5\).
