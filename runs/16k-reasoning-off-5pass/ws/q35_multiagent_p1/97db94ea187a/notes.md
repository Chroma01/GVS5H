
## ideation
The core difficulty is counting connected graphs with a specific BFS distance parity property. Since N ≤ 30, we cannot iterate over all graphs or use simple bitmask DP.

Key observations:
1. Vertex 1 is at distance 0 (even). We need exactly N/2 vertices at even distance and N/2 at odd distance.
2. Let S be the set of vertices at even distance (including vertex 1), so |S| = N/2. Let T be the set of vertices at odd distance, |T| = N/2.
3. For the BFS distances to be consistent:
   - There must be no edges within S that would create a path of odd length from 1 to some vertex in S (but actually, BFS distance is the shortest path, so we need to ensure that for v in S, dist(1,v) is even, and for v in T, dist(1,v) is odd).
   - This is complex because the presence of edges can create shorter paths.

Alternative approach: Use inclusion-exclusion on the connectivity constraint.
- First, count all graphs (connected or not) where the BFS distance parity condition holds.
- Then subtract disconnected graphs using inclusion-exclusion.

However, a more direct combinatorial approach:
For a fixed partition (S, T) with 1 ∈ S, |S| = |T| = N/2:
- Edges within S: Can exist, but must not create odd-length paths from 1 to any node in S that are shorter than the BFS distance. This is tricky.

Actually, let's think about it differently. The condition "number of vertices at even distance from 1 equals number at odd distance" is equivalent to saying that in the BFS tree, the levels alternate, and we need exactly N/2 nodes at even levels (0, 2, 4, ...) and N/2 at odd levels (1, 3, 5, ...).

For small N (≤ 30), we can use DP with state being the current vertex and the parity assignment. But this is still complex.

Given the constraints and the nature of the problem, I'll implement a solution that:
1. Iterates over all possible subsets S of size N/2 containing vertex 1.
2. For each such subset, counts the number of connected graphs where vertices in S are at even BFS distance and vertices in T are at odd BFS distance.
3. Uses inclusion-exclusion to handle connectivity.

But iterating over all subsets of size 15 from 30 is C(30,15) ≈ 155 million, which is feasible with optimization.

For each subset S, we need to count connected graphs where:
- All vertices in S are reachable via even-length paths.
- All vertices in T are reachable via odd-length paths.
- The graph is connected.

This requires that:
- There are no edges within S that would create an odd cycle affecting the parity? No, BFS distance is shortest path, so we need to ensure that the shortest path to any v in S is even, and to any v in T is odd.

This is equivalent to saying that the graph is bipartite with partition (S, T) and vertex 1 is in S? No, because non-bipartite graphs can still have well-defined BFS distances.

Actually, the condition is that for every vertex v, dist(1, v) mod 2 is fixed. This means that there are no edges within S that would create a path of odd length between two vertices in S (which would imply one has odd distance if the other has even, but they're both supposed to have even distance). Wait, no: if there's an edge within S, say between u and v both in S, and dist(1,u) is even, then dist(1,v) could be even or odd depending on the path. But we require dist(1,v) to be even. So if there's an edge within S, it must be that the shortest path to v is still even, which means there's no shorter odd-length path.

This is getting complex. Let me use a different strategy: for N ≤ 30, use brute force with pruning for small N, and for larger N, use the combinatorial approach with inclusion-exclusion.

Given the time constraints, I'll implement a solution that works for N ≤ 30 by iterating over all possible BFS layerings and counting graphs that satisfy the distance parity condition.
