
## ideation
The problem asks to simulate Santa’s path consisting of axis-aligned segments and count distinct houses visited (including endpoints). Constraints: N, M ≤ 2e5, coordinates up to 1e9 (and intermediate coordinates can be up to 1e14 due to moves). Straightforward per-point checking is too slow.

**Core difficulty:** Efficiently count houses lying on each segment without iterating over all houses each time.

**Candidate approaches:**
- **Coordinate compression + map by coordinate:** For each distinct y-coordinate that appears among houses, store the sorted list of x-values of houses with that y. For each distinct x-coordinate, store sorted y-values. Then for a horizontal segment at y = Y with x in [x_low, x_high], binary search the list for that y to find indices of houses whose x is in the range, and mark them counted. Similarly for vertical segments.
- **Sweep line / interval tree:** Overkill; mapping by coordinate is simpler and sufficient.
- **Global set of visited houses:** Use a set of (x, y) tuples to avoid double counting. When a house is found on a segment, check if it’s already in the set; if not, insert and increment counter. Since coordinates can be up to ~3e9, Python tuples hash fine.

**Pitfalls:**
- The starting point is guaranteed to have no house, so we don’t need to check it.
- Endpoints of a segment must be included in the range check (binary search inclusive on both ends).
- Must handle 64-bit integers correctly; Python int is arbitrary.
- For a vertical/horizontal move, the y or x coordinate remains constant; ensure we look up the correct key.
- Complexity: Preprocessing O(N log N) (sorting lists). Each query O(log K + number of houses on segment) total O((N+M) log N) amortized because each house is examined at most once.

## worker: Implement the full solution in Python: read input,
- Preprocessed houses into two dictionaries: `y_to_xs` mapping y-coordinate to sorted list of x's, and `x_to_ys` mapping x-coordinate to sorted list of y's.
- For each movement:
  - Horizontal moves look up `y_to_xs[current y]` and binary search for x in `[x_low, x_high]`.
  - Vertical moves look up `x_to_ys[current x]` and binary search for y in `[y_low, y_high]`.
  - Iterated over matching indices, adding new houses to a `visited` set and incrementing `count`.
- Endpoints of segments are included naturally because the search range is inclusive on both ends via `bisect_left` (>= low) and `bisect_right` (<= high).
- Starting point has no house by constraint, so no need to check it.
- Python integers are arbitrary precision, so no overflow issues.
- Complexity: O(N log N + M log N + total houses visited) ≤ O((N+M) log N). Each house is processed at most once.
