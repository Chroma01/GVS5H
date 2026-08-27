
## ideation
Core difficulty: counting distinct houses lying on the union of M axis-aligned segments, with N, M up to 2e5 and coordinates up to 1e9 (final position can reach 3e9, so use Python ints / 64-bit). A naive per-segment scan of all houses is O(NM) — too slow. The key structure: group houses by row (y → sorted list of x) and by column (x → sorted list of y), then each move becomes a 1D range query answered via bisect.

Pitfalls:
1. Duplicate counting: a house at a corner where two consecutive segments meet can be found by both segments (e.g., sample 1, house (2,2) found twice). Need dedup via a visited set of house indices.
2. Duplicate query cost: if a segment passes over many already-visited houses repeatedly, bisect-range queries still scan them. Worst case: M segments each crossing the same row containing N houses → O(NM) work. To guarantee O((N+M) log N), physically delete found houses from the index structures. Deleting from Python lists is O(k) per deletion which is fine amortized (each house deleted once), but bisect + list.pop per element is O(list length) shifts — total O(N^2) worst case if we pop from the middle of a long list repeatedly... Actually each pop from a list of length L is O(L); popping all N elements one at a time from a single row costs O(N^2) = 4e10 — too slow. Better: instead of deleting, extract the whole contiguous slice of matched indices at once (bisect_left/bisect_right give the range), mark them visited, and delete the slice in one operation `del lst[l:r]` which is O(L) once per row per query. But a row could be queried many times with small slices each time — each `del` shifts the tail, worst case O(N) per query → O(NM). Hmm.

   Alternative: don't delete; just mark visited and accept that queries may rescan visited houses. Worst case blow-up: M horizontal segments all on the same row with N houses → each query scans N houses → O(NM). Is this reachable? Yes: N houses at (i, 0), M moves alternating L/R along y=0. So we need deletion or a smarter structure.

   Robust option: per row/column keep a sorted list plus a pointer-based "next unvisited" union-find (disjoint set "successor" structure). When we visit house at position p in the row's sorted array, union p with p+1 so future queries skip it in near-O(α) amortized. Query: find leftmost index ≥ lo via bisect, then repeatedly use find() to get next unvisited index, check if within range, visit and union. Total cost O((N + total query endpoints) α + M log N). This is clean and safe.

   Simpler alternative that also works: since each house is removed once, use `sortedcontainers.SortedList`? Not allowed (no external libs). Use the DSU-successor trick — standard and pure Python.

3. Endpoint inclusion: segments are closed intervals; houses at endpoints count ("passed through or arrived at"). Both bisect bounds inclusive.
4. The start point has no house (guaranteed), but later positions may coincide with houses — handled naturally since each segment includes its endpoints.
5. Overflow: Python ints fine; in other languages need 64-bit (sample 2: 3e9).
6. Input speed: use sys.stdin.buffer.read and split; 4e5 lines fine.

Complexity target: O((N + M) log N + N α(N)) ≈ O((N+M) log N).

Implementation sketch:
- Read houses; assign index i. Build rows: dict y → list of (x, idx) sorted by x; cols: dict x → list of (y, idx) sorted by y. Store parallel arrays xs[y] = sorted x list, and for DSU successor we need per-row parent array of size len+1. Keep dicts: row_x[y] = sorted list of x; row_id[y] = parallel list of house indices; row_parent[y] = list(range(len+1)).
- find(parent, i): path compression; parent[i] = i if i is "next candidate", else points to next. Standard "next unvisited" DSU: parent[i] = i initially; when visiting i, set parent[i] = find(i+1). Sentinel index len means "end".
- For a horizontal move from (x1,y) to (x2,y): lo,hi = sorted(x1,x2). If y in row_x: l = bisect_left(row_x[y], lo); then j = find(l); while j < len and row_x[y][j] <= hi: mark house row_id[y][j] visited (count++), union j→j+1, j = find(j). Note: visited houses are removed from DSU so no double count even across row/col structures — but a house belongs to both a row and a column; if found via row first, later a column query could find it again via its own DSU. So also keep a global visited boolean array; when found via either structure, check visited before counting, and union in *both* structures? Union in both requires knowing the house's position in the column structure too. Simpler: keep global visited[]; when a query finds house idx: if not visited, count++, mark visited, and union it out of *both* its row and column DSU. To do that, precompute for each house its position in row list and column list: pos_in_row[idx], pos_in_col[idx]. Then union row_parent[y] at that pos, and col_parent[x] at its pos. That keeps both structures clean, total unions 2N.
- Vertical moves symmetric.
- Track position with plain Python ints; apply move, then query.

Edge cases: row/col dicts only contain coordinates that have houses; moves on empty rows skip quickly. M, N up to 2e5 — recursion-free find with path compression (iterative) to avoid recursion limits.

## worker: Write the complete Python solution: fast input par
- **Algorithm**: Simulate each of the M axis-aligned moves. For each move, the swept segment is a horizontal or vertical closed interval. Houses on it are found via per-row (y → sorted x's) and per-column (x → sorted y's) indexes using `bisect_left` for the range start.
- **Dedup + amortized efficiency**: A global `visited` bytearray ensures each house is counted once. To avoid rescanning already-visited houses (which could degrade to O(NM), e.g., many moves along one row full of houses), each row/column has a DSU "successor" structure: `find(j)` returns the next unvisited index ≥ j; visiting j unions it with j+1. When a house is first found (via either structure), it is unioned out of **both** its row and column DSU (positions precomputed in `pos_row`/`pos_col`), so every house is processed exactly once across all queries.
- **Complexity**: O((N + M) log N + N·α(N)) time, O(N) memory. Each query costs one bisect plus near-constant amortized work per newly found house.
- **Overflow**: Python ints are arbitrary precision, so positions up to 3×10⁹ (sample 2) are fine.
- **Edge cases handled**: inclusive endpoints (houses at segment endpoints count, per "passed through or arrived at"); moves on rows/columns with no houses are skipped via dict membership; the guaranteed house-free start needs no special casing; iterative path-compression `find` avoids recursion limits.
- Verified logic against sample 1: moves hit (2,2) on segment 1, (2,1) on segment 3, and (2,2) again on segment 4 (skipped as visited) → count 2, final position (2,3). Sample 2: house (1,1) never lies on the x-axis path → count 0, final (3×10⁹, 0).

## worker: Verify the solution: fix the garbled parsing line 
- Fixed the garbled parsing line to `Sx = int(data[p+2]); Sy = int(data[p+3])`.
- **Sample 1 trace**: Houses: (2,2)#0, (3,3)#1, (2,1)#2. Start (3,2).
  - L 2: (3,2)→(1,2), horizontal y=2, x∈[1,3]. Row y=2 has x=2 → house #0 counted (count=1), removed from both DSUs.
  - D 1: (1,2)→(1,1), vertical x=1, no column at x=1 → skip.
  - R 1: (1,1)→(2,1), horizontal y=1, x∈[1,2]. Row y=1 has x=2 → house #2 counted (count=2).
  - U 2: (2,1)→(2,3), vertical x=2, y∈[1,3]. Column x=2 has y=1 (#2, visited→skipped via DSU since it was unioned out) and y=2 (#0, also unioned out). `find` skips both → nothing counted.
  - Final: (2,3), count=2 → output `2 3 2`. ✓
- **Sample 2 trace**: House (1,1). Moves R 1e9 three times along y=0. Row y=0 doesn't exist → no hits. Final x=3e9 → `3000000000 0 0`. ✓ Python ints handle 3e9 natively.
- **Endpoint inclusion**: `bisect_left(keys, lo)` + `keys[j] <= hi` includes both endpoints, so a house exactly at a segment endpoint (e.g., arrival point) is counted. Verified in sample 1 where (2,1) is the arrival point of segment 3.
- **Empty rows/cols**: dict membership check (`if y in row_key`) skips instantly.
- **DSU dedup blowup test**: N houses at (i, 0), M alternating L/R moves along y=0. First pass unions each house out of the row DSU (and column DSUs). Subsequent passes: `bisect_left` + one `find` returns the sentinel (len) immediately → O(log N) per move. Total O((N+M) log N). No O(NM) blowup. ✓
- **Cross-structure dedup**: when a house is found via a row query, it's unioned out of its column DSU too (and vice versa), using precomputed `pos_row`/`pos_col`. The `visited` bytearray guards the count; the DSU unions guarantee the house is never even iterated again in either structure.
- **DSU successor invariant**: `parent[j] = find(parent, j+1)` after processing j; sentinel index `len` terminates the while loop via `j < L`. Path compression is iterative (no recursion limit issues).
- Complexity: O((N + M) log N + N·α(N)) time, O(N) memory.
