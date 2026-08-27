
## ideation
The core difficulty is maintaining, for every root-to-current-node path, the longest suffix whose node values are all distinct. The tree branches, so state must be correctly restored when DFS backtracks or represented persistently. Edge lengths mean the best path ending at a node is determined by the earliest valid ancestor, while ties require comparing the number of nodes rather than only distances.

For an endpoint at depth d, if the latest occurrence depth of every value on the current root path is known, the valid starting depth is one greater than the maximum relevant previous occurrence. The path length is the cumulative-distance difference between that start and the endpoint, and its node count is the corresponding depth difference plus one. The main implementation hazards are handling the current value before versus after querying its previous occurrence, restoring state on sibling subtrees, and avoiding recursion depth failures on a path-shaped tree.

## worker: Implement the complete iterative DFS solution usin
The DFS maintains the active root-to-current path. For each value, `latest` stores its most recent depth on that path. The valid suffix lower bound is updated when the current node repeats a value.

Because all edge lengths are positive, the earliest valid start depth gives the longest special path ending at the current node. Prefix distances allow its length to be computed in constant time, while the depth difference gives the node count. Enter/exit events rollback both the latest-value state and the active distance path for sibling subtrees.
