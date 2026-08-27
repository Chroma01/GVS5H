
## ideation
The core difficulty is that the chosen subgraph must remain connected while every selected vertex has degree exactly 1 or 4. A selected vertex’s allowable children depend on whether its parent edge is used: it may either be a leaf with no further selected neighbors, or a degree-4 vertex requiring exactly three additional branches. The requirement that at least one degree-4 vertex exists must also be handled explicitly. With \(N\) up to \(2\cdot 10^5\), recursion depth and avoiding quadratic child-combination work are important.

## worker: Derive and verify the high-degree-core reduction, 
Every degree-4 vertex in the alkane must have original degree at least 4. The degree-4 vertices form a connected subtree (the “core”): a degree-1 vertex cannot lie internally on a path between two degree-4 vertices. Conversely, any connected set of such eligible vertices whose induced core degree is at most 4 can be completed to an alkane by attaching `4 - core_degree` unused neighboring vertices as leaves.

If the core has `k` vertices and `L` leaves, the tree degree equation gives:
`4k + L = 2(k + L - 1)`, so `L = 2k + 2`. Therefore the total size is `k + L = 3k + 2`.

The DP maximizes the size of a connected eligible core with maximum degree 4. A directed branch message includes its endpoint and allows at most three continuation branches when the endpoint is attached to its parent. For a core center, the four largest incoming branch values may be combined. Downward and upward messages are computed iteratively, retaining only the largest four candidates per vertex, giving `O(N)` time and memory.
