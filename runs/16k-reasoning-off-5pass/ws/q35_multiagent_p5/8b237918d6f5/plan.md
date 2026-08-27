1. Since N is small (up to 30), we can use dynamic programming or BFS-based approaches. The key insight is that we want to maximize the shortest path from 1 to N by setting exactly K edges to weight 1 (others remain 0). This is equivalent to finding a path from 1 to N such that the number of "expensive" edges (weight 1) on the shortest path is minimized, but we need to choose which K edges are expensive to maximize the shortest path distance.

2. We can reframe the problem: For each possible shortest path distance d (from 0 to N-1), check if it's possible to assign weights to exactly K edges such that the shortest path from 1 to N is at least d. We want the maximum such d.

3. Alternatively, we can use binary search on the answer d. For a given d, we need to check if there exists a way to set exactly K edges to weight 1 such that all paths from 1 to N have length >= d. This is complex.

4. A better approach: Use DP where dp[v][k] = minimum number of weight-1 edges on a path from vertex 1 to vertex v using exactly k edges of weight 1... but we need to choose which edges are weight 1 globally.

5. Actually, the standard approach for this problem is: binary search on the answer d. For a fixed d, we need to verify if we can choose K edges to be weight 1 such that the shortest path from 1 to N is >= d. This can be checked by finding the minimum number of edges we need to set to weight 1 so that all paths from 1 to N have length >= d. If this minimum is <= K, then d is achievable (we can set additional edges to weight 1 arbitrarily).

6. To check if shortest path >= d is achievable with at most K weight-1 edges: We can use a BFS/DP where for each vertex, we track the minimum "cost" (number of weight-1 edges needed) to ensure all paths to that vertex have length >= current level. This is tricky. 

7. Simpler approach: Since N is small, we can iterate on the answer d from N-1 down to 0. For each d, we check if it's possible. To check if answer >= d: We need to ensure that every path from 1 to N has at least d edges that are set to weight 1? No, the distance is the sum of weights. So a path of length L (number of edges) with w edges having weight 1 has total weight w. We need all paths to have weight >= d.

8. Let me reconsider: The shortest path distance is the minimum over all paths of the sum of weights on that path. We set exactly K edges to weight 1, rest to 0. We want to maximize this minimum.

9. Binary search on d. For a fixed d, can we choose K edges to be 1 such that every path from 1 to N has at least d edges with weight 1? This is equivalent to: find the minimum number of edges that must be set to 1 to ensure all paths have length >= d in terms of count of weight-1 edges. If min_needed <= K, then yes.

10. To compute min_needed for a fixed d: Use DP. dp[v] = minimum number of weight-1 edges on any path from 1 to v, but we're choosing which edges are weight-1. This is still complex.

11. Actually, a cleaner formulation: For binary search on d, we want to know if there exists a subset S of K edges such that for every path P from 1 to N, |P ∩ S| >= d. This is a hitting set type problem.

12. Given the constraints (N ≤ 30, M ≤ 100), we can try a different DP: dp[v][k] = the minimum number of weight-1 edges on the shortest path from 1 to v when we've used k weight-1 edges globally... but this doesn't work because the choice is global.

13. Let me use the approach: Binary search on d. For each d, construct a graph and use BFS to find the shortest path in terms of number of edges. If the shortest path has length L, and L < d, we need to "break" this path by setting some of its edges to weight 1. But we need to break ALL paths.

14. Final approach: Since N is very small, we can enumerate all simple paths? No, there can be exponentially many.

15. Correct approach: Binary search on d. For a fixed d, we need to check if we can choose K edges such that every path from 1 to N has at least d edges with weight 1. This is equivalent to checking if the minimum number of edges to set to 1 to ensure all paths have at least d weight-1 edges is <= K.

16. To compute this minimum: Use DP where dp[v] = a pair (min_weight, min_edges) but this is complex. 

17. Alternative: For each path, the number of weight-1 edges on it must be >= d. We want to minimize the total number of weight-1 edges chosen. This is a linear programming problem, but with integer constraints.

18. Given the small constraints, let's use a different DP: Let's define f[v] as the minimum number of weight-1 edges that must be placed on edges incident to or before v to ensure... 

Actually, let me just implement the binary search with a feasibility check using min-cost flow or simple DP.

For feasibility of d: We can use DP. Let dp[v] = the minimum number of weight-1 edges on a path from 1 to v, where we're trying to minimize this to see if it's < d. If for all paths, the min weight-1 edges >= d, then d is feasible.

Wait, I think the correct check is: For a fixed d, can we assign weights to K edges such that the shortest path is >= d? This means every path has at least d edges with weight 1. The minimum number of edges we need to set to 1 to achieve this is what we need to compute.

Let me use: dp[v] = minimum number of weight-1 edges on any path from 1 to v. We want dp[N] >= d. But we choose which edges are weight-1. 

I'll implement binary search on d, and for each d, use a BFS-like DP where we compute the minimum number of weight-1 edges needed on paths to ensure all paths to v have at least some property. This is getting complex. Let me just code a solution that works for small N.