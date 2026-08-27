1. Read the input and construct the graph.
2. Build the Minimum Spanning Tree (MST) using Kruskal's algorithm.
3. Preprocess the MST for LCA queries to efficiently compute the bottleneck distance $f(u, v)$ for any pair $(u, v)$. This involves binary lifting to store the maximum edge weight on the path to the $2^k$-th ancestor.
4. Compute the cost matrix $C$ of size $K \times K$ where $C[i][j] = f(A_i, B_j)$.
5. Solve the minimum weight perfect matching problem on the bipartite graph defined by $C$ using the Hungarian algorithm (or Kuhn-Munkres algorithm).
6. Print the minimum sum.