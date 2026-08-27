
## ideation
**Core difficulty:**  
We need to simulate axis-aligned moves of Santa and count distinct houses visited (including endpoints). Naively checking each house per move is O(N·M) → too slow.

**Key observation:**  
A house is visited on a move only if it lies on the same horizontal line (same y) for L/R moves, or same vertical line (same x) for U/D moves, and its coordinate along the line lies within the segment (including endpoints). So we can group houses by coordinate:
- For horizontal moves: group by y-coordinate, store sorted x-values.
- For vertical moves: group by x-coordinate, store sorted y-values.

**Approach:**  
1. Build dictionaries:
   - `by_y`: y → sorted list of (x, house_index)
   - `by_x`: x → sorted list of (y, house_index)
2. Simulate moves. For each move:
   - Determine the range on the line (inclusive of both ends).
   - Binary search in the appropriate sorted list to find the subarray of houses whose coordinate lies in the range.
   - For each such house, if not yet visited, mark visited and increment counter.
3. Use a boolean list `visited` of size N to deduplicate.

**Complexities:**  
- Preprocessing: O(N log N) for sorting.
- Each move: O(log K + number_of_houses_in_range) where K is size of the group. Since each house is processed at most once, total O(N log N + M log N).

**Pitfalls:**  
- Coordinates can be up to 1e9 and C_i up to 1e9, but Python ints are unbounded → safe.
- Need to handle inclusive endpoints correctly.
- Moves can be negative direction (L, D). Use `min(start, end)` and `max(start, end)` for range.
- Use bisect for binary search.
- Input size up to 2e5 → use fast I/O (sys.stdin.buffer).

## worker: Implement the solve() function: read input, build 
- Built dictionaries `by_y` and `by_x` grouping houses by y and x respectively.
- For each group, sorted the positions and separated the coordinate list from the index list for efficient `bisect` usage.
- Simulated each move: for horizontal moves (L/R) looked up the list of houses on `y = cur_y`; for vertical moves (U/D) looked up houses on `x = cur_x`. Used `bisect_left/right` to find houses whose coordinate lies in the inclusive interval between start and end.
- Used a boolean `visited` array to deduplicate: each house is marked at most once, so total work is O(N + M log N) after sorting.
- Python's arbitrary-precision integers handle coordinates up to 3×10⁹ safely.
- Final position is printed along with the count of distinct houses visited.
