We model this problem using a state-space graph where each state is (vertex, orientation). Orientation 0 means the original graph, and orientation 1 means all edges are reversed. We have two types of transitions:
1. Moving along an edge in the current orientation costs 1.
2. Reversing the orientation costs X.

We can use 0-1 BFS (or Dijkstra's algorithm since edge weights are 1 and X, but X can be large so Dijkstra is safer) to find the shortest path from (1, 0) to any state (N, 0) or (N, 1). The graph has 2N vertices and 2M + 2N edges (M edges in each orientation, plus N reverse operations from each vertex). Since N, M <= 2*10^5, Dijkstra with a priority queue will run in O((N+M) log N), which is efficient enough.