
## ideation
The core difficulty is counting distinct houses visited during a sequence of axis-aligned straight-line moves, given up to 2e5 houses and moves. Santa’s path is a polyline; a house is counted if it lies on any segment of the path (including endpoints). We need the final position and the number of distinct houses.

Key observations:
- Moves are only vertical or horizontal, so a house (hx, hy) can be visited only when the moving coordinate matches Santa’s fixed coordinate at the start of the move and the other coordinate lies within the segment’s range.
- For a vertical move at fixed x = cx from y1 to y2, we need to query all houses with that x whose y is in [min(y1,y2), max(y1,y2)].
- For a horizontal move at fixed y = cy from x1 to x2, we need houses with that y whose x is in [min(x1,x2), max(x1,x2)].
- Each house is visited at most once, so we can remove it from future consideration after counting.

Data structure approach:
- Group houses by x-coordinate and by y-coordinate in two dictionaries of sorted lists (or balanced BSTs). Python `list` + `bisect` works.
- For a vertical move, get the list of y’s for that x, binary search the lower and upper bounds, collect all matching y’s, add to count, and rebuild the list without them. Do the same for the y‑coordinate map to remove the x.
- Total work over all moves is O((N+M) log N) because each house is removed once and each query uses binary search.

Pitfalls:
- Overflow: final coordinates can be up to 1e9 + sum of steps (up to 2e5·1e9 = 2e14) → need 64‑bit integers (Python int is fine, but be careful in C++/Java).
- Input format: first line has N, M, Sx, Sy. Then N lines of houses, then M lines of moves.
- The sample 2 shows that no houses are passed, output final coordinates 3000000000 0 0.
- No house at start, but it could be visited later.
- Avoid O(k^2) per move by using slice deletion (rebuilding the list) rather than repeated `pop` at an index.

Verification on sample 1: path passes (2,2) and (2,1) → count 2, final (2,3).

## worker: Implement the described algorithm in Python: parse
The solution processes the input by first building two maps: one from x‑coordinates to a sorted list of y‑coordinates of houses with that x, and one from y‑coordinates to a sorted list of x‑coordinates.  
During the simulation of each move we:
- Determine the segment's range on the moving axis.
- Use binary search (`bisect_left`/`bisect_right`) on the relevant list to find all houses whose other coordinate falls within that range.
- Collect the matched coordinates, increment the global count, and delete them from both maps to avoid double counting.  
Deletion is done with slice assignment (`del lst[i:j]`) or `pop` after binary search, keeping the total work over all moves linearithmic because each house is removed at most once.  
Python's arbitrary‑precision integers automatically handle the large coordinates (up to ~2·10¹⁴).  
The algorithm runs in O((N+M) log N) time and O(N) memory, well within the limits for N,M ≤ 2·10⁵.
