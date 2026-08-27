
## ideation
The problem asks us to simulate Santa's path consisting of axis-aligned moves and count the number of distinct houses that lie on the path (including intermediate points and the final point after each move).  
The naive approach of enumerating every point on the path is impossible because steps can be up to 1e9. Instead, we must work geometrically.

Core difficulty: efficiently find, for each move, which houses lie on the line segment traversed (not just endpoints). Because the path is Manhattan (axis-aligned), each move is either a vertical or horizontal segment.

Observations / candidate approaches:
1. **Coordinate compression + sweep**: For horizontal moves, group houses by their y-coordinate. For a move from (x1, y) to (x2, y), we need to count houses with that y where the x coordinate lies between min(x1, x2) and max(x1, x2). Use a dictionary `hor[y] = sorted list of x`. Then for each horizontal segment, binary search in that list to get the range of indices — O(log N) per move.
2. Same idea for vertical moves: group houses by x-coordinate, sort y.
3. Total time O((N + M) log N). Space O(N).
4. Need 64-bit arithmetic for final coordinates since coordinates can exceed 1e9 (up to 1e9 + 2e5 * 1e9 ≈ 2e14). Python ints are unbounded, but watch for overflow in other languages.

Pitfalls:
- We must include the final position after each move (if a house sits there) and also the starting point of a move? The starting point of a move is the ending point of the previous move (or the initial S). The problem says "passed through or arrived at during his actions". A house at the exact start point (S) is not a house per problem statement ("There is no house at (S_x,S_y)"). For subsequent moves, the starting point of a move is the ending point of the previous move. That point has already been considered if a house is there. To avoid double counting, we can just insert all points we encounter (including intermediate houses and the final point after each move) into a set. Since the starting point of a move (except the very first) is the final point of the previous move, and we already added that final point (or intermediate houses on previous move) to the set, duplicates are automatically handled.
- The path includes the endpoints of each segment. A house coinciding with the start of a move (which equals the end of previous move) will be added to the set anyway. So we can just for each segment add the final point, and add all houses strictly inside the segment. But including the final point is easy — just add it. For horizontal moves, we need all houses with that y and x in (min(x1, x2), max(x1, x2)). We can do binary search on the sorted list to find indices l = left_bound(min_x) and r = right_bound(max_x), then add those x's (or the points (x, y)) to the set.
- We need to add the house points (x, y), not just one coordinate, to the set to ensure uniqueness across different segments (though two different segments can only share a point if the path crosses itself, but that doesn't matter — set will dedup).
- Complexity: O(N log N + M log N) fits constraints (2e5). Memory: O(N).

Edge cases:
- No houses in a segment: set unchanged.
- Move length 0? Not possible since C_i >= 1.
- Negative coordinates and steps: handled with signed addition; careful with min/max.
- Large coordinates: Python fine.

## worker: Implement the solution in Python: read input, prep
- The path is simulated by updating the current position with 64‑bit safe arithmetic (Python ints are unbounded, so no overflow).
- For each move we:
  - Determine the coordinate that stays constant (`x` for vertical, `y` for horizontal).
  - Binary‑search the pre‑sorted list of houses sharing that coordinate to find those whose other coordinate lies strictly between the old and new positions (or inclusive of the new position for `U`/`R`).
  - Add those houses to a `set` for automatic deduplication.
  - Add the final point of the segment to the set as well; this catches the case where a house coincides with the endpoint.
- Two dictionaries are used: `by_y[y] = sorted list of x` for horizontal moves, and `by_x[x] = sorted list of y` for vertical moves. Construction is `O(N log N)`, each query is `O(log N + k)` where `k` is the number of houses matched, but since every house is processed at most once, total is `O((N+M) log N)`.
- Edge cases: negative coordinates, zero‑length moves (impossible because `C_i ≥ 1`), no house on a segment, and self‑intersecting paths are all handled by the set.
- Final output: final x, final y, and the size of the set of distinct visited houses.
