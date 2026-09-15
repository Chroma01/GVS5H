1. Model the two pieces as an ordered pair state and reduce the swap problem to finding the shortest cycle that can be used to exchange their order.
2. Run BFS from S and from T to compute the minimum distances dS[v] and dT[v] to every vertex.
3. Decompose the graph into biconnected components (blocks) using Tarjan's algorithm; if the graph is a tree (no cyclic block), the answer is -1.
4. For every cyclic block, compute the minimum cost to swap using that block: either both pieces enter at the same vertex v (cost = 2·dS[v] + 2·dT[v] + 4) or they enter at distinct vertices x, y on a cycle within the block (cost = 2·dS[x] + 2·dT[y] + cycle_length).
5. Take the minimum over all such candidates and output it.