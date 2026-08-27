
## ideation
Core difficulty: For each distinct value v, deleting all occurrences of v splits the array into contiguous gaps (segments without v). The best subarray after deletion is the maximum subarray sum within any single gap (subarrays can't cross a deleted position). We need, for each gap, the max subarray sum = (max prefix sum in gap) − (min prefix sum at or before gap start). Doing this naively per value is O(n·distinct), too slow; we need O(1) or O(log n) range min/max queries on prefix sums (sparse table or segment tree), making total work O(total gaps · query) = O(n log n) since total gaps across all values ≤ n + distinct values.

Key details:
- Prefix sum P[0]=0, P[i+1]=P[i]+nums[i]. For a gap covering indices [l..r] (inclusive, 0-based, containing no v), max subarray sum = max(P[l+1..r+1]) − min(P[l..r]).
- For each value v with sorted occurrence positions p1<p2<...<pk, gaps are [0, p1−1], [p1+1, p2−1], ..., [pk+1, n−1]; skip empty gaps.
- Also consider not deleting at all (Kadane's on the whole array, or equivalently treat it as one gap).
- Edge cases: all elements equal to v → deleting v empties the array, which is disallowed (must remain non-empty), so skip values whose count == n. All-negative arrays: max subarray is the single largest element; formula handles this naturally since subarrays must be non-empty (using P[l+1..r+1] max minus P[l..r] min ensures non-empty).
- Answer could be negative; initialize answer carefully (e.g., with Kadane's result).

Pitfalls:
- Forgetting the "array must remain non-empty" constraint when a value appears n times.
- Off-by-one on prefix indices for gap [l..r].
- Empty gaps between consecutive equal values must be skipped.
- Sparse table for range min and max: build two tables over P (length n+1), O(n log n) memory is fine for n=1e5. Alternatively use a segment tree or just precompute with RMQ via `math.log2`.

## worker: Implement the full solution: prefix sums + sparse 
- Initial plan (max over individual gaps only) was flawed: after deleting all occurrences of x, the remaining segments concatenate, so subarrays can span multiple former gaps. Fixed by treating each gap as a composite item with stats (total sum S, max prefix MP, max suffix MS, max subarray MM) and combining gaps left-to-right with a Kadane-like scan per value: `best = max(best, MM(gap), best_suffix + MP(gap))`, `best_suffix = max(MS(gap), best_suffix + S(gap))`.
- Gap stats are derived from prefix sums via O(1) sparse-table range min/max queries: for gap [l..r], S = P[r+1]−P[l], MP = rmax(P,l+1..r+1)−P[l], MS = P[r+1]−rmin(P,l..r), MM = rmax(P,l+1..r+1)−rmin(P,l..r).
- Total work: O(n log n) build + O(Σ(freq_x)) queries = O(n) queries overall. Handles all-negative arrays (non-empty subarray guaranteed since MP/MS/MM use non-empty index ranges), skips values whose deletion would empty the array, and includes the no-operation case.
- Verified on Example 1 (→7: gaps [-3,2],[-1,3],[3] combine to 2+(-1)+3+3=7) and Example 2 (→10, no-op best).

## worker: Fix the current solution: it only takes the max ov
- Fixed the flaw identified in the plan: after deleting all occurrences of x, the surviving segments concatenate, so a maximum subarray can span multiple former gaps. The per-value loop now performs a Kadane-like scan over the gaps using composite stats (S, MP, MS, MM):
  - `best = max(best, MM, best_suffix + MP)` — best subarray is either inside one gap or a suffix of the concatenated previous gaps joined with a prefix of the current gap.
  - `best_suffix = max(MS, best_suffix + S)` — best subarray ending exactly at the current gap's end.
- Gap stats derived in O(1) from prefix sums via sparse-table range min/max: for gap [l..r], S = P[r+1]−P[l], MP = rmax(P,l+1..r+1)−P[l], MS = P[r+1]−rmin(P,l..r), MM = rmax(P,l+1..r+1)−rmin(P,l..r). All ranges are non-empty, so all-negative cases work (subarrays must be non-empty).
- Complexity: O(n log n) sparse-table build, O(Σ freq_x) = O(n) gap queries total, O(n) distinct-value scans.
- Verified:
  - Example 1: [-3,2,-2,-1,3,-2,3] → deleting -2 gives gaps [-3,2], [-1,3], [3]; scan combines (-1+3) + 3 etc. → 7. ✓
  - Example 2: [1,2,3,4] → no-op gives 10; deletions give less → 10. ✓
  - Single element [5]: no-op = 5; only value's deletion empties array → skipped → 5. ✓
  - All same value [2,2,2]: deletion disallowed → no-op = 6. ✓
  - All negative [-5,-1,-3]: no-op = -1; deleting -5 gives [-1,-3] → -1; deleting -1 gives [-5,-3] → -3; deleting -3 gives [-5,-1] → -1 → answer -1. ✓
  - Spanning case [1,-9,1]: deleting -9 yields [1,1] → 2 (spans both gaps) — correctly handled by the combining scan. ✓
