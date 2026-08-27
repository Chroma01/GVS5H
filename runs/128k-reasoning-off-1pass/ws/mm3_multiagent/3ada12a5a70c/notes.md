
## ideation
[analysis of the problem, identifying that it's a circle selection problem after mapping to ring, etc.]

## worker: Implement the ring coordinate mapping and the feas
The key insight is that Manhattan distance between points on the boundary of a square is equivalent to the distance along the perimeter (since the boundary is a 1D path). By mapping each point to a ring coordinate (0 to 4·side), the problem becomes selecting k points on a circle to maximize the minimum circular distance.

The feasibility check uses binary search on D: given minimum distance D, we check if we can place k points on the circle with all consecutive distances ≥ D. This is done by:
1. Building a "next" pointer array where `nxt[i]` is the first index ≥ i with coordinate difference ≥ D
2. Trying each starting point and greedily jumping k-1 times
3. Verifying the k-th point's position satisfies the circular constraint (span ≤ perimeter - D)

The greedy approach is optimal here because we always pick the earliest possible next point, leaving maximum room for remaining points. This runs in O(n·k) per check, which is efficient given n ≤ 15000 and k ≤ 25.

## worker: Test the implementation against the three provided
The solution correctly maps boundary points to a 1D ring coordinate and reduces the problem to selecting k points on a circle to maximize the minimum circular distance. The feasibility check uses a greedy approach with precomputed next-pointers, which is optimal for circular distance maximization. Binary search finds the maximum feasible D.

Verified against the three examples:
- Example 1: All 4 corners → distance 2 ✓
- Example 2: Points (0,0),(1,2),(2,0),(2,2),(2,1) with k=4 → distance 1 ✓
- Example 3: Points with k=5 → distance 1 ✓

The algorithm runs in O(n log(perim) + n·k) per check, which is efficient for the given constraints (n ≤ 15000, k ≤ 25).
