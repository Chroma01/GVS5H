
## ideation
The core difficulty is recognizing that after deletions, the retained vertices need only form a layered tree around a chosen center. For a fixed center \(c\) and positive \(y\), a neighbor \(v\) of \(c\) can be retained as an intermediate vertex exactly when it has at least \(y\) neighbors besides \(c\), namely when \(\deg(v)-1\ge y\). Every eligible intermediate can be used, and exactly \(y\) of its other neighbors can be retained as leaves.

Thus, for fixed \(c,y\), the maximum retained size is \(1+(y+1)k\), where \(k\) is the number of eligible neighbors of \(c\). The tree structure prevents conflicts between selected layers: two neighbors of the center cannot be adjacent, and a leaf of one intermediate cannot also be adjacent to another intermediate without creating a cycle.

Important edge cases are that \(x\) and \(y\) must both be positive, so only thresholds \(y\ge1\) and centers with at least one eligible neighbor matter. Ties in degree thresholds must be processed together or otherwise handled consistently. The final deletion count is the original number of vertices minus the largest attainable Snowflake size.

## worker: Implement the global descending-threshold sweep: a
For a fixed center and leaf count `y`, a neighboring vertex can be used as an intermediate vertex exactly when its degree is at least `y + 1`. Thus, activating vertices in descending order of `degree - 1` maintains the number of eligible neighbors for every possible center.

After activating one complete equal-threshold group, if the maximum eligible-neighbor count is `x`, the largest snowflake has:

`1 + x * (y + 1)`

vertices. The tree property guarantees that the chosen leaves for different intermediate vertices are distinct, so all eligible intermediates can be used simultaneously.

The sweep is `O(N log N)` due to sorting, with `O(N)` additional memory.
