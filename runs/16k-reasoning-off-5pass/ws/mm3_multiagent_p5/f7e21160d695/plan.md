We need to minimize sum of f(A_i, B_{perm(i)}) where f(x,y) is the minimax edge weight along any path between x and y. This is exactly the bottleneck distance: in any connected undirected graph, f(x,y) equals the minimum possible value T such that x and y are connected using only edges with weight ≤ T. Equivalently, f(x,y) is the maximum edge weight on the unique path between x and y inside a minimum spanning forest (a minimum spanning tree for connected graph).

1. Build a Minimum Spanning Tree (MST) using Kruskal sorted by edge weight. Since the graph is connected, MST has N-1 edges and preserves the minimax distances for all pairs: for any x,y, f(x,y) equals the maximum edge weight on the path between them in the MST.
2. Root the MST at an arbitrary node (node 1). Preprocess binary lifting ancestors and the maximum edge weight on the upward jump (max_edge[u][k]).
3. For any query (x,y), compute f(x,y) in O(log N) by LCA with maximum edge on the path.
4. For the optimization: we must pair each A_i with a distinct B_j to minimize total sum. Observe that the MST has a crucial structural property: the minimax distance between two nodes equals the maximum weight edge on their path. Hence for a fixed source A_i, the function g_i(t) = number of B_j with f(A_i, B_j) ≤ t is non-decreasing, stepwise, and g_i(t) counts the B nodes lying in the connected component of A_i when we consider only edges of weight ≤ t (which corresponds to a subtree/clique in the MST). This is exactly a "minimum weight bipartite matching" of a special form that can be solved greedily by sorting.

Algorithm for assignment:
- Compute for each A_i the list of (distance, B_node) pairs.
- Sort each A_i's pairs by distance ascending.
- Use a global min-heap (priority queue). For each A_i, we push into the heap pairs (distance, A_index, B_index) iteratively: start with smallest distance for each A_i. Also we track for each A_i the current pointer.
- The heap is ordered by distance. Repeatedly pop the smallest (dist, i, j). If B_node j is still free, match A_i with B_node j and add dist to answer; else, we must advance A_i's pointer to the next larger distance and push that.
- Since each B_node can be matched at most once, total pushes are O(K log K).

This greedy is correct because the problem is a minimum weight bipartite matching on a tree-like cost matrix that satisfies a Monge / quadrangle inequality; the greedy works because it mimics a priority-based augmentation: we always take the globally cheapest available match and never need to undo it.

Overall complexity: O(M log M) for Kruskal, O(N log N) for binary lifting, O(K log K) for the heap, well within limits.