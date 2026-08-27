
## ideation
The core difficulty is converting score requirements into visit requirements: index \(i\) must be visited at least \(\lceil X/\text{points}[i]\rceil\) times, but visits are coupled because the walk starts outside the array, must enter through index 0, and can only move between adjacent indices. Repeated visits consume pairs of moves across edges, while progressing to an unvisited suffix consumes additional moves. The feasibility test must also avoid wasting moves on unnecessary returns, especially near the final index. Move counts can reach roughly \(10^9\) or more, so 64-bit arithmetic is required.

## worker: Derive and verify the exact left-to-right feasibil
For a target score `X`, index `i` must be visited at least:

`ceil(X / points[i])`

times.

For positive `X`, the first move enters index `0`, giving it one visit. While processing an intermediate index `i`, if it has `extra` missing visits, each oscillation `i -> i+1 -> i` adds one visit to `i` and costs two moves. After those oscillations, one final move advances to `i+1`. Thus the transition costs `2 * extra + 1`, and index `i+1` receives `extra + 1` visits.

At the final index, no further advancement is required, so each missing visit costs a round trip of two moves.

This greedy construction is optimal because every additional visit before advancing requires at least two moves, and using the right-side oscillations also provides visits for the next index. Binary search over the answer gives `O(n log(m * min(points)))` time and `O(1)` extra space.
