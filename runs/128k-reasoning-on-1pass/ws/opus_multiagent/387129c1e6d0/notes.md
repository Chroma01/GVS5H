
## ideation
**What's being asked.** Simulate M axis‑parallel moves from a start point, output the final position and the number of *distinct* houses lying on any of the M closed segments (endpoints included, start point has no house so it doesn't matter whether we include it).

**Core difficulty.** N, M ≤ 2·10⁵ and C_i ≤ 10⁹, so a segment can span up to 10⁹ lattice points — you cannot walk step by step. You need, per move, the set of houses on a given axis‑parallel segment, but with a total (not per‑query) bound on the enumeration work. Coordinates grow to ~1e9 + 2e5·1e9 ≈ 2·10¹⁴ (Python ints are fine; the "overflow" warning targets C++/64‑bit-vs-32-bit users).

**Key observation that simplifies everything.** The answer is just |{houses covered by the *union* of the M segments}|. Order of traversal is irrelevant, and re‑visits are irrelevant. So the problem is fully offline:

- A vertical move at x = a covers houses with X_i = a and Y_i ∈ [ylo, yhi].
- A horizontal move at y = b covers houses with Y_i = b and X_i ∈ [xlo, xhi].

Hence: group segments into `vert: x -> list of (ylo,yhi)` and `horiz: y -> list of (xlo,xhi)`; merge intervals per key; then for each house test membership by binary search in the merged list for key X_i (vertical) and key Y_i (horizontal). Total cost O((N+M) log(N+M)), no deletion/DSU machinery needed. This is strictly simpler and less bug‑prone than the DSU "next alive pointer" plan in the sketch (which is also correct but requires careful amortization: each node removable once per structure, iterative path compression, bucket-boundary care).

**Alternative (online) approaches, for comparison.**
1. DSU/next‑pointer over two globally sorted house arrays (the drafted plan). Correct, amortized O((N+M)α + M log N), but more code and needs iterative `find`, lazy skipping of houses already visited via the other structure.
2. Per‑bucket sorted lists with physical `del lst[i:j]`. Risky: up to N delete operations each memmoving up to O(bucket size) — worst case (all houses same x) too slow / borderline.
3. Bucket + `visited` set with no deletion: a segment repeatedly crossing a dense bucket re‑enumerates the same houses → O(M·N) worst case. **Wrong complexity — avoid.**

**Pitfalls / edge cases.**
- Must still simulate the walk to get the final coordinates and each segment's endpoints — accumulate with Python ints; don't clamp.
- Segments' endpoints inclusive: use `min/max` to normalize each segment before storing.
- Zero‑length segments impossible (C_i ≥ 1), but a segment may be a single point after merging? No — but merged intervals must handle touching/overlapping intervals (merge when `next_lo <= cur_hi`, not `<`).
- Houses coordinates bounded by 1e9 while positions may be far outside — binary search naturally returns empty, fine.
- A house can be covered by both a vertical and horizontal segment — count once (short‑circuit the check).
- Distinct houses guaranteed by constraints, so no dedup of input needed.
- Fast IO: `sys.stdin.buffer.read().split()`; direction tokens are bytes (`b'U'`, …); build lookup rather than decoding strings.
- Output format: `X Y C` space separated on one line.
- Don't use recursion (DSU) if going that route; recursion limit + speed.
- Memory: M segments in dicts of lists is fine; consider grouping by sorting a list of (key, lo, hi) tuples instead of dict-of-lists if memory/speed matters.

**Sanity check with sample 1.** Segments: vertical/horizontal from (3,2)→(1,2) [horiz y=2, x∈[1,3]], (1,2)→(1,1) [vert x=1], (1,1)→(2,1) [horiz y=1, x∈[1,2]], (2,1)→(2,3) [vert x=2, y∈[1,3]]. Houses: (2,2) covered by horiz y=2; (3,3) not; (2,1) covered by horiz y=1 and vert x=2. Count 2, final (2,3). ✔

**Sample 2.** Final x = 3·10⁹, house (1,1) not on y=0 line → 0. ✔

## worker: Implement the full offline union-of-segments solut
- Implemented the fully offline union-of-segments solution as planned.
- Simulation uses Python big ints (positions can reach ~2·10¹⁴), emitting each move as a normalized closed interval on its line: vertical moves keyed by x with [min(y,ny), max(y,ny)], horizontal keyed by y with [min(x,nx), max(x,nx)].
- Both segment lists are sorted (tuples sort by key then lo) and merged in a single pass; intervals that touch (`lo <= ce`) are merged, so a house exactly at a junction of two segments is still detected.
- Per key we keep parallel `starts`/`ends` arrays; coverage test is `i = bisect_right(starts, v) - 1; i >= 0 and ends[i] >= v`, which is valid since merged intervals are disjoint and increasing.
- Each house counted once: vertical test first, `continue` on hit, else horizontal test.
- Complexity O((N+M) log(N+M)) time, O(N+M) memory. Direction tokens compared as bytes to avoid decoding.
- Sample checks (by hand): sample 1 → `2 3 2`; sample 2 → `3000000000 0 0`.
