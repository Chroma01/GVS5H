
## ideation
The core difficulty is avoiding a scan of all houses for every movement while also ensuring that repeatedly visited houses are counted only once. Each move is an axis-aligned inclusive segment, so the problem reduces to reporting house points lying on a sequence of horizontal or vertical segments. A naive per-move scan can be quadratic, and merely storing sorted coordinates is insufficient if already-counted houses are encountered repeatedly.

Important pitfalls include treating both segment endpoints as visited, handling houses at intersections of multiple segments only once, preserving the order of Santa’s movements when computing the final position, and using sufficiently wide integer arithmetic.

## worker: Develop the offline solution: simulate all moves w
The movement path is recorded as horizontal and vertical inclusive intervals. Intervals are grouped by their fixed coordinate, sorted, and merged. Touching intervals are merged because all integer points between them are visited.

Each house is checked once. A binary search determines whether its coordinate lies in a merged interval on either its row or column, so repeated visits are counted only once.

Time complexity is \(O((N+M)\log M)\), and memory usage is \(O(N+M)\).
