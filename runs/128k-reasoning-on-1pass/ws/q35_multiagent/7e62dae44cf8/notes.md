
## ideation


## worker: (none)
The problem can be modeled as finding the maximum weight connected subgraph containing the starting cell $(P, Q)$ such that there exists a valid absorption order. The condition $S_{target} < S_{current} / X$ implies that we can only absorb slimes weaker than our current strength scaled by $1/X$. Since absorbing a slime always increases our strength and expands our reachable area, we should greedily absorb the weakest available adjacent slime. 

Using a min-priority queue to always process the weakest adjacent slime ensures that we check the most likely candidates first. If the weakest candidate fails the condition, all stronger candidates will also fail, allowing us to terminate early. This approach guarantees finding the maximum possible strength because:
1. Absorbing any valid slime is always beneficial (increases strength and reach).
2. The feasibility of a set of slimes depends only on their strengths and connectivity, not the order, provided we process them in non-decreasing order of strength.
3. The priority queue efficiently manages the frontier of reachable slimes.

Time Complexity: $O(HW \log(HW))$ due to heap operations for each cell.
Space Complexity: $O(HW)$ for storing the grid, state array, and priority queue.
Constraints $H, W \le 500$ are well within limits for this approach.
