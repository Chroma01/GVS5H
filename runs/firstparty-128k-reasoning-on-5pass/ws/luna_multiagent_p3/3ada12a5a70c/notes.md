- **Perimeter mapping:** Each boundary point is mapped exactly once to a counter-clockwise coordinate in `[0, 4 * side)`. Corners are assigned using ordered edge checks to avoid duplication.

- **Distance bound:** Since `k >= 4`, among any selected points one cyclic perimeter gap is at most one quarter of the perimeter, hence at most `side`. Therefore the answer never exceeds `side`.

- **Distance reduction:** For candidate distances at most `side`, two boundary points whose shorter perimeter separation is below the candidate have Manhattan distance equal to that separation. If both perimeter arcs are at least `side`, their Manhattan distance is also at least `side`. Thus requiring every cyclic gap between consecutive selected perimeter positions to be at least the candidate is equivalent to the Manhattan-distance condition.

- **Greedy feasibility:** Fix the first selected point. The earliest possible next point at least `distance` farther along the perimeter is always optimal, because it leaves at least as much room for all later points and maximizes the final wraparound gap.

- **Successor construction:** A doubled sorted perimeter array represents cyclic movement. A monotone two-pointer scan computes every greedy successor in `O(n)` time per feasibility check.

- **Binary lifting:** Applying the greedy successor `k - 1` times is done with binary lifting. Since `k <= 25`, each starting point requires only `O(log k)` transitions. A candidate sequence is valid only if all selected points remain within one perimeter copy and the final gap back to the first point is at least the candidate distance.

- **Complexity:** Each feasibility check costs `O(n log k)` time and memory, where `n = len(points)`. Binary search adds `O(log side)` checks, giving total complexity `O(n log k log side)`.
