
## ideation
Core difficulty: deleting all occurrences of `x` removes scattered indices, so the resulting array is the concatenation of the maximal gaps between positions where `nums[i] == x`. We need the maximum subarray sum after this filtered concatenation for every distinct `x`, plus the no-operation case, without recomputing from scratch each time.

The proposed segment-tree approach is promising: each node stores `(total, best_prefix, best_suffix, best_subarray)` for an interval, so a gap query is O(log n), and concatenating gap aggregates is O(1) with the usual merge. Since value `x` with frequency `f` creates at most `f + 1` gaps, total gap work over all distinct values is `sum(f + 1) = n + distinct <= 2n`, giving O(n log n).

Key correctness question: merging gap aggregates must exactly represent subarrays that may span across deleted positions. A subarray after deletion can include multiple original gaps joined together, but cannot include any deleted `x`; concatenating gap summaries in order should capture this if empty gaps are handled with a true identity and no fake “empty subarray” is allowed.

Pitfalls:
- “At most once” means include original array’s Kadane result.
- Operation is only allowed if removing `x` leaves non-empty, i.e. `freq[x] < n`; if all elements equal, no deletion is allowed.
- Answer may be negative; subarrays must be non-empty, so identity/empty handling must not incorrectly yield 0.
- Empty gaps before first occurrence, after last occurrence, and between consecutive occurrences must be skipped safely.
- Values are large range, so use hash map from value to sorted positions, not array by value.
- Python segment tree should be iterative or carefully bounded; recursion over n=1e5 can be risky.
- Need distinguish “no elements” aggregate from valid negative aggregates; use `-inf` sentinels carefully.
- Verify merge formula: `best = max(left.best, right.best, left.suffix + right.prefix)`, `prefix = max(left.prefix, left.total + right.prefix)`, `suffix = max(right.suffix, right.total + left.suffix)`, `total = left.total + right.total`.

## worker: Implement an iterative segment tree with associati
- **Node design**: each segment-tree node stores `(total, pref, suff, best)` for its range. Merge of left `L` and right `R`:
  - `total = L.total + R.total`
  - `pref = max(L.pref, L.total + R.pref)`
  - `suff = max(R.suff, R.total + L.suff)`
  - `best = max(L.best, R.best, L.suff + R.pref)`
- **Empty identity**: `(0, -inf, -inf, -inf)` with `NEG = -(1<<60)`. Merging identity with any node returns that node exactly (verified both sides), and since real sums are bounded by ~1e11, `NEG` can never win a `max` against a real value — so all-negative arrays stay correct and no fake "empty subarray = 0" leaks in.
- **Query**: standard iterative inclusive-range query with separate left/right accumulators (combine is associative but not commutative, so right-side nodes are prepended via `merge(node, right_acc)`).
- **Per value x**: the post-deletion array is the concatenation of gaps between consecutive occurrences. Endpoint gaps use precomputed prefix/suffix aggregates in O(1); interior gaps use the segment tree in O(log n). Total interior-gap queries = `sum(max(0, freq-1)) = n - distinct <= n`, so overall O(n log n).
- **Edge cases**: skip `x` with `freq == n` (deletion must leave non-empty); answer initialized with the whole-array best (the "at most once" / no-op case, which also covers deleting a value not present); `n = 1` works (no deletion allowed, returns `nums[0]`).
- Verified against Example 1 (trace gives 7 via `x = -2`) and Example 2 (10, no operation), plus hand-checked all-negative and consecutive-occurrence cases.
