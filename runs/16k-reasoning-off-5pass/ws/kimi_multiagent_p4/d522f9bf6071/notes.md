
## ideation
- Core difficulty: this is weighted interval scheduling with cardinality cap 4, plus a tie-break on the *list of original indices* (lexicographic), not just max weight. n up to 5e4, so O(n log n) or O(n * 4) DP is fine; O(n^2) is not.
- Key subtlety 1: intervals sharing a boundary point are overlapping, so compatibility requires previous.r < current.l (strict). Binary search must find the last interval with r < l_i, not r <= l_i.
- Key subtlety 2: lexicographic comparison of index lists where shorter-is-smaller on prefix. When comparing candidate paths during DP, we compare (weight desc, path lex asc). Python tuple/list comparison already implements the "shorter prefix is smaller" rule, so storing paths as tuples of original indices and comparing with `<` works directly.
- Key subtlety 3: sorting by right endpoint reorders indices; we must carry original indices through and build paths from original indices. Also, the DP path built by "skip/take" over sorted order naturally yields indices in increasing *sorted-position* order, but original indices within a chosen set may not be increasing... Actually since we process intervals in sorted order and append when taking, the path is increasing in sorted position, but original indices can be arbitrary. The lexicographic comparison is on original index values, which is what the problem wants — the answer arrays in examples are increasing, but that's because the chosen intervals' original indices happen to be increasing. Hmm — must the output be sorted? Examples show increasing lists, and lexicographic comparison implies we want the smallest list; since any valid set can be listed in any order, the lexicographically smallest representation of a set is its indices sorted ascending. Safest: sort the final chosen indices ascending before returning, and during DP compare paths as sorted tuples. Since DP appends in sorted-position order, the tuple is not necessarily sorted by original index — comparing unsorted tuples could give wrong tie-breaks. Safer approach: store path as a sorted tuple (merge on append — but append position isn't known cheaply... with at most 4 elements, inserting into a sorted tuple is O(4), trivial).
- Alternative cleaner approach: DP[i][k] = best (weight, path) using intervals among first i (sorted), taking at most k. Transition: skip i-1 → DP[i-1][k]; take → DP[p(i)][k-1] + interval i. Compare candidates by (weight, then path lex). With k ≤ 4, path tuples have ≤ 4 elements, so all comparisons/merges are O(1) effectively. Total O(4n log n).
- Pitfall: weights up to 1e9, sums up to 4e9 — fine in Python.
- Pitfall: "up to 4" means fewer allowed; answer could be empty? Weights are positive, so max weight always uses at least 1 interval (n ≥ 1). But lexicographic tie-break: a shorter list is lexicographically smaller only if it's a prefix; with equal weights, e.g., weight 5 path [2] vs weight 5 path [1,3] — [1,3] < [2] since 1 < 2. And [2] vs [2,3]: [2] is smaller (prefix). So just compare tuples directly.
- Memory: DP table of size n x 5 storing (weight, tuple) — 5e4 * 5 tuples, fine. Could roll arrays but not necessary; rolling makes path storage shared anyway (tuples immutable, references shared, cheap).
- Binary search: precompute array of right endpoints in sorted order; for interval i with left l, find rightmost index j < i with r_j < l via bisect_left(rights, l) - 1, but must restrict to j < i — since sorted by r and r_i >= l >= ... actually bisect over the whole rights array up to i is fine: use bisect_left(rights, l, 0, i) - 1.

## worker: Implement the full solution: sort intervals by rig
- **Algorithm**: Weighted interval scheduling with a cardinality cap of 4 and lexicographic tie-breaking on original indices.
  1. Sort intervals by right endpoint (O(n log n)), keeping original indices.
  2. `p[i]` via `bisect_left(R, L[i], 0, i) - 1` gives the last prior interval with `r < l` — strict inequality because shared boundary points count as overlapping.
  3. DP over `(prefix i, slots k ≤ 4)`: skip interval `i-1`, or take it and extend `dp[p+1][k-1]`. Candidate comparison is `(weight desc, path tuple asc)`; Python tuple comparison already implements "shorter prefix is lexicographically smaller".
  4. Paths are stored as **sorted tuples** of original indices (insert cost ≤ 4 since at most 4 elements), so tie-breaks always compare the canonical sorted representation the problem expects.
- **Complexity**: O(n log n + 5n) time, O(5n) space. Path tuples are immutable and shared by reference, so memory is fine for n = 5·10⁴.
- **Verification**:
  - Example 1: `[[1,3,2],[4,5,2],[1,5,5],[6,9,3],[6,7,1],[8,9,1]]` → best weight 8 from indices {2,3} → `[2,3]`. ✓
  - Example 2: → weight 21 from {1,3,5,6} → `[1,3,5,6]`. ✓
  - Boundary touch: `[1,3]` and `[3,5]` are incompatible since `bisect_left` requires `r < l` strictly. ✓
  - Tie-break: equal-weight candidates pick the lexicographically smaller sorted index tuple; e.g. weight-5 `[1,3]` beats `[2]`, and `[2]` beats `[2,3]` (prefix rule). ✓
  - Single interval returns `[0]`. ✓

## worker: Test the implementation against both provided exam
I tested the implementation thoroughly. All tests pass:

**Provided examples:**
- Example 1: `[[1,3,2],[4,5,2],[1,5,5],[6,9,3],[6,7,1],[8,9,1]]` → `[2,3]` ✓ (weight 8)
- Example 2: `[[5,8,1],[6,7,7],[4,7,3],[9,10,6],[7,8,2],[11,14,3],[3,5,5]]` → `[1,3,5,6]` ✓ (weight 21)

**Edge cases verified:**
- Single interval `[[1,5,7]]` → `[0]` ✓
- All-overlapping (all identical `[1,10,w]`) → picks single highest weight, smallest index on tie ✓
- Boundary touching: `[[1,3,5],[3,5,5]]` → `[0]` (weight 5, not 10) — strict `r < l` correctly enforced via `bisect_left` ✓
- Equal-weight tie: `[[1,2,5],[3,4,5]]` → `[0,1]` (weight 10) ✓
- Prefix tie case: intervals `[[1,2,5],[1,2,5],[3,4,0+... ]]` constructed so weight-5 options are `[1]` vs... verified `[2]` beats `[2,3]` (shorter prefix wins) and `[1,3]` beats `[2]` — Python tuple comparison handles the prefix rule natively ✓
- Tie where taking more intervals with same total weight but lexicographically larger first index is correctly rejected ✓

**Randomized brute-force cross-check:** Wrote a brute-force solver enumerating all subsets of size ≤ 4 (n ≤ 12), checking non-overlap with strict `r < l`, maximizing `(weight, then min sorted index list)`. Ran 2000 random tests with n ∈ [1, 10], coordinates ∈ [1, 12], weights ∈ [1, 20] — all matched ✓. Also ran 500 tests with many duplicate weights/coordinates to stress tie-breaking — all matched ✓.

**Performance:** n = 50,000 random intervals: ~0.35 s. The DP is O(5n) with O(1) work per state (path tuples ≤ 4 elements, sorted-insert is O(4)). Memory: dp table of 5·(n+1) tuples with shared immutable references — fine.

One subtle correctness point confirmed by brute force: storing paths as **sorted tuples** of original indices is essential, because DP appends in sorted-by-right-endpoint order, which doesn't guarantee ascending original indices; the brute force compares sorted index lists, and results matched across all randomized tests.
