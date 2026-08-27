
## ideation
We need to simulate axis-aligned moves of Santa and count distinct houses that lie on any traversed segment (including endpoints). N, M up to 2e5, coordinates up to 1e9, distances up to 1e9, so we cannot step through points.

Core difficulty: efficiently find houses that lie on each segment without enumerating all intermediate points.

Candidate approaches:
1. **Coordinate bucketing + binary search**:
   - For vertical moves (U/D), we need houses with the same x-coordinate as the current x. Group houses by x: `x_to_houses[x] = sorted list of (y, index)`.
   - For horizontal moves (L/R), group by y: `y_to_houses[y] = sorted list of (x, index)`.
   - For each move, binary search the appropriate list to find houses whose other coordinate lies in the inclusive interval [min, max] of the move.
   - To avoid O(k log N) per move (k = number of houses on segment), we can repeatedly pop the leftmost (or rightmost) qualifying house using `bisect_left/right` and `pop(0)` (or maintain pointers). Since each house is processed at most once overall, total work is O(N log N + M log N + N) = O((N+M) log N).

2. **Sweep line / interval tree**: Overkill; coordinate bucketing is simpler.

3. **Brute force**: O(N * total distance) impossible.

Pitfalls:
- **Overflow**: Coordinates and distances up to 1e9, sum up to 2e5 * 1e9 = 2e14, fits in Python int (unbounded) but in C++ needs int64.
- **Inclusive endpoints**: Santa passes through the endpoint of each move; a house exactly at the endpoint must be counted.
- **Duplicate counting**: A house may be passed multiple times; must count only once.
- **Initial position**: Santa starts at (S_x, S_y); problem guarantees no house there, so we don't count it initially.
- **Direction handling**: For L/R, x changes; we look up houses with y = current y. For U/D, y changes; look up houses with x = current x.
- **Sorting**: Lists must be sorted by the varying coordinate to use bisect.
- **Pop efficiency**: Using `list.pop(0)` is O(k) per move; better to maintain an index pointer per bucket and slice, or use `deque`. Since each house is removed once, total pops = N, so O(N) overall is fine, but `pop(0)` on a Python list is O(N) per pop -> O(N^2) worst case. Better to use a pointer index and avoid actual removal, or use `bisect` and then mark indices as removed via `seen` array and skip them. Simpler: keep sorted list and a pointer `pos` that advances as we consume houses from the left (for increasing direction) or from the right (for decreasing direction). But direction may change; we need to handle both. We can store two pointers per bucket: one for left end, one for right end, and advance whichever side we are consuming. Or we can just use `bisect` to find the range and iterate over that slice, marking seen, but that would be O(k) per move and total O(N) houses processed, which is fine because each house is processed at most once across all moves. However, iterating over a slice of a Python list is O(k) and copying is O(k); total O(N) is acceptable. The main cost is the binary search per move: O(log N). So overall O((N+M) log N + N) is fine.

Implementation details:
- Read N, M, S_x, S_y.
- Read N houses; store in arrays `xs[i], ys[i]`.
- Build `x_map: dict[int, list[(y, i)]]` and `y_map: dict[int, list[(x, i)]]`.
- For each map, sort the list by the varying coordinate.
- `seen = [False]*N`, `count = 0`.
- Simulate moves:
  - For direction L: new_x = x - C; range_x = [new_x, x]; look up `y_map[y]`; find houses with x in [new_x, x].
  - For R: new_x = x + C; range_x = [x, new_x]; same lookup.
  - For D: new_y = y - C; range_y = [new_y, y]; look up `x_map[x]`.
  - For U: new_y = y + C; range_y = [y, new_y]; same lookup.
  - Use `bisect_left` and `bisect_right` to get indices `l, r` in the sorted list.
  - Iterate over `lst[l:r]`, for each (coord, idx): if not seen[idx], mark seen and increment count.
  - Update current position.
- Print final x, y, count.

Edge cases:
- No houses on a move: binary search returns empty range.
- House exactly at start or end: inclusive range includes it.
- Large coordinates: Python handles big ints.

Complexities: O(N log N + M log N) time, O(N) memory.

## worker: Implement the `solve()` function in Python using t
- Built dictionaries `by_x` and `by_y` mapping the fixed coordinate to a sorted list of `(varying_coord, index)` pairs.
- For each move, we locate the appropriate bucket (e.g., `by_y[current_y]` for horizontal moves) and use `bisect_left`/`bisect_right` to find the range of houses whose varying coordinate lies within the inclusive segment.
- We iterate over that range and mark unseen houses. Each house is inspected at most once across all moves, so total work is O(N) after the binary searches.
- Final position and count are printed. Python integers handle the large values without overflow.
