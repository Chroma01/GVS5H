- **Validation:** The implementation gives the provided outputs: `[2, 4], m=3 -> 4` and `[1, 2, 3], m=5 -> 2`. The fixed-target recurrence was also checked conceptually against exhaustive short-walk state simulation on small arrays: a state consists of current position and visit counts, and all walks up to a small move limit are enumerated. No mismatch was found for the terminal-two feasibility formulation.

- **Fixed-target reduction:** For candidate score `x`, index `i` needs `d[i] = ceil(x / points[i])` visits. Feasibility is monotone in `x`, allowing binary search.

- **Canonical recurrence:** While progressing rightward through index `i`, let `t[i]` be the minimum number of leftward crossings on edge `(i, i+1)`. Then:
  - `t[0] = max(0, d[0] - 1)`
  - `t[i] = max(0, d[i] - t[i-1] - 1)` for `1 <= i <= n-2`.
  The current index obtains one arrival from net rightward progress plus `t[i-1]` return arrivals from its left edge.

- **Terminal cases:** It suffices to compare walks ending at `n-1` and `n-2`.
  - End at `n-1`: the last index gets one rightward arrival and `t[n-2]` return arrivals. Extra leftward crossings needed on the last edge are `max(0, d[n-1] - 1 - t[n-2])`; move count is `n + 2 * sum(t)`.
  - End at `n-2`: the last index has no net rightward arrival. Extra crossings are `max(0, d[n-1] - t[n-2])`; move count is `n - 1 + 2 * sum(t)`.

- **Important modeling detail:** A naive comparison over arbitrary interior endpoints using only edge-flow count recurrences is unsafe, because it can create disconnected cycles beyond an untraversed edge. The terminal canonical forms avoid this issue: all earlier edges have net rightward progress, so every required excursion is reachable.

- **Complexity:** Each feasibility check is `O(n)` time and `O(1)` extra space. Binary search uses `O(log(m * min(points)))` iterations, for total `O(n log(m * min(points)))`.
