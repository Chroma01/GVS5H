The problem asks us to maximize the shortest path from vertex 1 to vertex N by setting exactly K edges to weight 1 (others remain 0). Since N is small (up to 30), we can use dynamic programming or binary search on the answer. However, a more direct approach is to use BFS/Dijkstra with state tracking. 

Actually, since we want to *maximize* the shortest path, this is equivalent to finding a path from 1 to N such that the number of edges on the path is at least some value D, and we can "block" (set to 1) K edges on all paths shorter than D. But wait, we set exactly K edges to 1 globally. The shortest path in the resulting graph is the minimum over all paths of (number of edges with weight 1 on that path). We want to choose K edges to maximize this minimum.

A better approach: Binary search on the answer D. For a fixed D, can we make the shortest path >= D? This means every path from 1 to N must have at least D edges with weight 1. Equivalently, no path from 1 to N has fewer than D edges with weight 1. This is hard to check directly.

Alternative: Since N is very small (N ≤ 30), we can use DP. Let dp[v][k] = the minimum number of edges with weight 1 on a path from vertex 1 to vertex v using exactly k edges set to 1? No, we choose which edges are set to 1 globally.

Actually, we can reframe: We want to assign weights w(e) ∈ {0,1} to exactly K edges such that the shortest path from 1 to N is maximized. This is equivalent to: find the maximum D such that there exists a set S of K edges where every path from 1 to N contains at least D edges from S.

This is a "bottleneck" problem. We can binary search on D. For a fixed D, we need to check if there exists a set S of K edges such that every path from 1 to N has at least D edges in S. This is equivalent to: the minimum number of edges from S on any path from 1 to N is at least D. 

We can model this as a min-cost flow or use DP. Since N is small, let's use DP: dp[v][j] = the minimum number of edges from S on a path from 1 to v, where we've used j edges from S so far? No, S is chosen globally.

Better approach: Binary search on the answer D. To check if answer >= D is possible: we need to choose K edges such that every path from 1 to N has at least D edges chosen. This is equivalent to saying that if we remove all edges NOT in S, the remaining graph (with only edges in S) has no path from 1 to N of length < D? No.

Actually, let's think differently. The shortest path distance is the minimum over all paths P of |P ∩ S|. We want to maximize this minimum. 

We can use binary search on D. For a fixed D, we need to check if there exists a set S of size K such that every path from 1 to N has at least D edges in S. This is equivalent to: the minimum cut in a certain graph? 

Let's use a different DP. Since N ≤ 30, we can iterate on all possible values of the answer. The answer is between 0 and K (and also bounded by the longest simple path, which is at most N-1).

For a fixed target D, we can check feasibility using min-cost max-flow or DP. Let's use DP: dp[v][j] = minimum number of edges from S on a path from 1 to v, where j is the number of edges from S used? No.

Actually, here's a cleaner approach: Binary search on D. To check if we can achieve shortest path >= D: we need to select K edges such that every path from 1 to N has at least D selected edges. This is equivalent to: in the graph, if we assign cost 1 to edges in S and 0 otherwise, the shortest path is >= D. 

We can check this by: for a fixed D, can we find a set S of size K such that the shortest path (with edges in S having weight 1, others 0) is >= D? This is hard.

Alternative: Since N is small, let's use DP with state (vertex, number of selected edges on the path). But the selection is global.

Let me reconsider: We can binary search on the answer D. For a fixed D, we need to verify if there exists a set S of K edges such that every path from 1 to N has at least D edges in S. This is equivalent to: the minimum number of edges from S on any path from 1 to N is at least D. 

This can be checked using min-cut: construct a graph where each edge has capacity 1. We want to find a set S of size K such that the min-cut from 1 to N in terms of edges in S is at least D. 

Actually, here's a standard approach: Binary search on D. For each D, we check if the minimum number of edges we need to "activate" (set to 1) to ensure all paths have at least D activated edges is <= K. This is complex.

Given the constraints (N ≤ 30, M ≤ 100), let's use a simpler DP. Let dp[v][k] = the maximum number of edges on a path from 1 to v using exactly k edges set to 1? No.

Let's try: dp[v][j] = the minimum number of edges with weight 1 on a path from 1 to v, where we have the freedom to choose which edges are 1. But the choice is global.

I think the best approach is binary search on D and use a min-cost flow or DP to check. For a fixed D, we can check if there's a set S of size K such that every path has at least D edges in S by solving a linear program or using DP on the graph structure.

Since N is small, let's use DP: dp[v][j] = the minimum number of edges from S on a path from 1 to v, where j is the number of edges from S that we've "committed" to on this path. But this doesn't capture the global choice.

Actually, here's a working approach: Binary search on the answer D. For a fixed D, we need to check if we can choose K edges such that every path from 1 to N has at least D edges chosen. This is equivalent to: the minimum number of chosen edges on any path is at least D. 

We can check this by: for each path, it must have at least D chosen edges. This is a covering problem. 

Given the time, let's implement binary search on D and for each D, use a DP that computes the minimum number of edges we must choose to ensure all paths have at least D edges chosen. This is complex, but with N=30, we can use DP with state (vertex, current path length in terms of chosen edges).

Let me just implement a solution using binary search on D and for each D, check if the minimum number of edges to select to block all paths of length < D (in terms of chosen edges) is <= K. 

Actually, I'll use a simpler observation: the answer is at most K and at most the length of the longest shortest path. Let's binary search on D from 0 to K. For each D, we check if there exists a set S of size K such that every path from 1 to N has at least D edges in S. 

To check this, we can use min-cost max-flow: create a graph where each edge has cost 1 if selected, 0 otherwise. We want the shortest path to have cost >= D. 

Given the complexity, let's just implement a brute-force DP since N is small. 

dp[v][j] = minimum number of edges with weight 1 on a path from 1 to v, where j is the number of edges with weight 1 on this path. But we need to ensure that globally, exactly K edges are set to 1.

I think the correct approach is: binary search on D. For each D, check if the minimum number of edges we need to set to 1 to make all paths have at least D edges set to 1 is <= K. This can be done with a DP that computes for each vertex v and each count j, the minimum number of edges set to 1 on a path from 1 to v.

Let's define dp[v][j] = the minimum number of edges set to 1 on a path from 1 to v that has exactly j edges total? No.

I'll implement binary search on D and for each D, use a BFS/DP to check if it's possible.