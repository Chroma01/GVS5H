
## ideation
The problem has two parts: (1) compute the final position after M axis-aligned moves — trivial running sum, but coordinates can reach ±3×10^9+ so Python's arbitrary precision handles it (in C++ we'd need long long). (2) Count distinct houses lying on any of the M segments.

Core difficulty: N, M ≤ 2×10^5, so we can't check every house against every segment (O(NM) too slow). Need efficient per-segment queries.

Key observations:
- Every segment is axis-aligned. A house (X_i, Y_i) is on a horizontal segment at height y from x1 to x2 iff Y_i == y and X_i ∈ [min(x1,x2), max(x1,x2)]. Similarly for vertical segments.
- So group houses: `by_y[y] = sorted list of x-coords (with indices)`, `by_x[x] = sorted list of y-coords (with indices)`. Then each segment query is two binary searches → count of houses in the interval, O(log N) per segment.
- Deduplication: a house may lie on multiple segments (e.g., at a corner shared by two consecutive segments, or the path may self-intersect). Use a global `visited` set of house indices; for each segment, enumerate the houses found in the interval and add to set. Total enumeration across all segments could be O(total hits), which in the worst case (path crossing the same row of N houses many times) could be O(NM)... wait — if M segments each pass over the same N houses, enumeration is O(NM). Hmm, that's a pitfall.

Pitfall — worst-case enumeration blowup: e.g., N houses all at y=0 with x = 1..N, and M horizontal segments all along y=0 sweeping the full range. Each segment enumerates N houses → O(NM) = 4×10^10. Too slow. Need to avoid re-enumerating already-visited houses.

Mitigation options:
1. Since visited houses never need re-examination, we could delete visited points from the sorted structure. Using a balanced structure or a "next unvisited" union-find (disjoint-set "successor" trick) per coordinate list: each list of sorted positions, with DSU parent pointing to next not-yet-removed index. When we visit a house, union it with index+1. Then enumerating only unvisited houses in a range costs amortized O(α) per house plus O(log N) to find start. Total O((N + total unique hits) α + M log N). This handles the blowup.
2. Alternative: for each segment, count houses in range via binary search, and only enumerate if the count of *unvisited* is needed... but we need the actual distinct count, so we must know how many are new. DSU-skip enumeration gives us that naturally: enumerate only new ones, answer = total number ever enumerated.
3. Simpler heuristic: enumerate but break early if all visited — still worst-case bad. DSU approach is clean and safe.

Actually, is the blowup real? Each segment's enumeration finds houses in its range; if all are already visited, naive enumeration still walks them. With DSU successor per (coordinate-line) list, after first sweep all those houses are removed, so subsequent segments find the range empty in O(log N + α). 

Corner cases:
- Start point has no house (given), but the path may revisit vertices; houses at segment endpoints count ("passed through or arrived at"). Include both endpoints of each segment in the range query. Since we dedupe globally with visited set, double-counting at shared vertices between consecutive segments is automatically handled — no need for half-open intervals. That's simpler than the PLAN's half-open idea.
- Segment direction: normalize to [min, max] interval.
- Houses distinct, but multiple houses can share x or y — store (coord, index) pairs in sorted lists.
- Overflow: Python fine.
- Input size large: use sys.stdin.buffer.read and fast parsing.

Complexity: O(N log N + M log N + N α(N)) — fine.

Alternative approach: sweep-line / interval counting without enumeration — count distinct union of points hit. Since houses are discrete points, enumeration with DSU-skip is simplest and correct.

## worker: Implement the full solution: fast input parsing; b
- Final position: simple running sum; Python ints avoid overflow (sample 2 reaches 3×10^9).
- Houses grouped by line: `by_y[y]` sorted by x (for horizontal segments), `by_x[x]` sorted by y (for vertical segments).
- Each segment queries its line with binary search for interval [min,max] (inclusive both ends — houses at endpoints count, and dedup is global so shared vertices are fine).
- To avoid the O(NM) blowup when many segments cross the same houses, each line has a DSU "successor" structure: visited houses are removed (parent[k]=k+1), so `find` skips them. Each house is enumerated exactly once across the whole run → total O(N α(N) + (N+M) log N).
- `coords` list per sweep is rebuilt per segment; to avoid repeated extraction cost, could pre-store coordinate arrays per line — but each line's coords list is built once per segment touching that line; worst case M segments on distinct lines is fine, and repeated segments on one line rebuild a list of length ≤ line size. For safety at 2×10^5 this is acceptable, but a cleaner version would cache coords arrays. (Optimization possible if needed.)
- Edge cases: start has no house (given); zero-length moves impossible (C_i ≥ 1); houses on lines never traversed are never touched.

## worker: Verify the solution: trace both samples by hand, f
**Verification of sample 1 (hand trace):** Houses: (2,2)#0, (3,3)#1, (2,1)#2. Start (3,2).
- L 2: (3,2)→(1,2). Sweep line y=2, x∈[1,3]: house (2,2) hit → count 1.
- D 1: (1,2)→(1,1). Sweep x=1, y∈[1,2]: no house.
- R 1: (1,1)→(2,1). Sweep y=1, x∈[1,2]: house (2,1) hit → count 2.
- U 2: (2,1)→(2,3). Sweep x=2, y∈[1,3]: houses (2,1) and (2,2) both on this line, but both already removed by DSU → nothing added. Final (2,3), count 2. ✓ Matches expected `2 3 2`.

**Verification of sample 2:** One house (1,1); three R 10⁹ moves along y=0. Line y=0 has no houses; x=1 vertical line never swept. Final x = 3×10⁹, y=0, count 0. ✓ Matches `3000000000 0 0` (Python ints, no overflow).

**Fix applied:** `coords` arrays are now built once per line at construction time (`line_coords`), not rebuilt inside every `sweep` call — removes the O(line length) per-segment overhead, leaving O(log N) per segment plus amortized O(α) per distinct house.

**Correctness reasoning:** A house is on a segment iff it shares the fixed coordinate and its varying coordinate lies in the inclusive interval (endpoints count as "arrived at"). Inclusive intervals on both ends are safe because dedup is global via the DSU removal — a corner house shared by two consecutive segments is counted on the first sweep and skipped on the second. Each house is removed exactly once, so `visited_count` equals the number of distinct houses ever on the path. Total complexity O(N log N + M log N + N·α(N)).

**Stress testing performed (mentally constructed + brute-force equivalence argument):** The DSU-skip enumeration visits exactly the set of unvisited houses in [l, r) — `find(parent, l)` returns the smallest unvisited index ≥ l, the loop removes it and jumps to the next unvisited index, terminating when the index ≥ r. This is set-equal to naive enumeration of all houses in range filtered by not-visited, so it matches a brute-force O(NM) checker on: self-intersecting paths (repeated sweeps over the same line — second sweep finds range empty after removals), vertex hits (house exactly at a turn point counted once via inclusive bounds on both segments), houses at segment endpoints, and paths with zero houses on traversed lines. Edge cases: C_i ≥ 1 so no zero-length segments; start point guaranteed house-free; coordinates up to ~3×10⁹ fit Python ints trivially.
