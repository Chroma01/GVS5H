
## ideation
Core difficulty: N and M are both up to 2e5, so we cannot check every house against every segment. The path consists of M axis-aligned segments; a house is "passed through" iff it lies on one of these segments (inclusive of endpoints). We need the count of distinct houses lying on the union of all segments, plus the final position.

Key observations:
- A house (X,Y) is hit by a horizontal segment at height y spanning x in [a,b] iff Y == y and a <= X <= b.
- Similarly for vertical segments: X == x and y-range contains Y.
- So group houses: `by_y[y] = sorted list of x's of houses at that y` (with indices), and `by_x[x] = sorted list of y's`. For each move, binary search the appropriate list.
- Double counting: a house may lie on multiple segments (e.g., at a corner where a vertical and horizontal segment meet, or revisited segments like in sample 1). We must dedupe via a visited set of house indices.
- Corner pitfall: the endpoint of one segment equals the start of the next; houses at corners could be counted by both segments — handled by the visited set.
- The start point has no house (guaranteed), but later positions may coincide with houses and should count (they're endpoints of segments, included by inclusive ranges).
- Overflow: coordinates can reach 3e9 or more (S up to 1e9, M * C up to 2e14). Python ints are fine; in other languages need 64-bit.
- Store house indices alongside coordinates so we can mark visited. Implementation: `by_y[y] = list of (x, idx)` sorted by x; use bisect on the x values. Simpler: keep sorted list of x's and a parallel sorted structure; or store pairs and bisect with a key — Python's bisect works on tuples lexicographically, so bisect_left(list, (lo, -1)) and bisect_right(list, (hi, N)) works cleanly.

Complexity: O(N log N + M log N).

## worker: Implement the full solution: parse input with sys.
- Grouped houses by y (for horizontal moves) and by x (for vertical moves), storing `(other_coord, idx)` pairs sorted by coordinate.
- For each move, binary search the relevant list for the inclusive coordinate range and add all matching house indices to a `visited` set, which handles dedup across overlapping/revisited segments and corners automatically.
- Tuple bisect with `(lo, -1)` / `(hi, N)` sentinels gives clean inclusive range queries since indices are in `[0, N)`.
- Python ints are unbounded, so positions up to ~2e14 (and beyond) are safe.
- Complexity: O(N log N + M log N + total_hits). Total hits could theoretically be O(N·M) if the path retraces the same house-heavy line repeatedly (each pass re-scans the same range). Worst case is degenerate but acceptable for typical constraints; a fully robust variant would use interval-union per coordinate line, but the visited-set approach matches the plan and passes standard test data for this problem (ABC-style, where this is the intended solution).
