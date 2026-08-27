
## ideation
The core difficulty: for each distinct value x, deleting all x's splits the array into gaps (segments between consecutive occurrences of x), and the answer for that x is the max subarray sum over all those gaps. We need max over all x plus the no-deletion case. The naive approach (scan the whole array per distinct x) is O(n · distinct), which is 10^10 in the worst case.

Key structural facts:
- After deleting x, any valid subarray lies entirely within one gap (a maximal run of positions with value ≠ x).
- If x occurs k times, there are ≤ k+1 gaps, and we can run Kadane per gap. Cost for value x is O(n − k) since we scan everything except x's... that's still O(n) per x. BUT there's a crucial amortization: cost per x = total gap length = n − count(x). Summed over all distinct x: distinct·n − n. Worst case distinct ≈ n/2 (each value appears twice) → O(n²/2). Too slow.
- However, there's a smarter observation: we don't need to scan gaps fully per x if we precompute. For a gap [l..r], the max subarray sum within it can't be answered in O(1) from simple prefix Kadane arrays, but we can use a segment tree where each node stores (sum, best prefix, best suffix, best subarray) — a range query gives a gap's max subarray in O(log n). Then per x: (count(x)+1) gap queries → total O((n + distinct) log n) = O(n log n). This is clean and safe for n=10^5.
- Alternative: per x, run Kadane only over gaps but skip gaps smartly — the segment tree approach dominates in simplicity.
- Edge cases: all-negative arrays (max subarray = max element; deleting the most negative value helps); x being the only value (can't delete — array would become empty); single element array (answer is that element, no deletion possible); deletion of x where remaining array is empty is disallowed — check count(x) < n.
- Also must consider NOT deleting (equivalently, answer ≥ original Kadane).
- Note: deleting x can only change things if x appears; also deleting a positive-only value never helps but we just take max anyway.
- Segment tree query per gap: gaps are [prev+1, cur-1] between consecutive occurrences, plus [0, first-1] and [last+1, n-1]. Skip empty gaps.
- Alternative simpler implementation: iterative segment tree (size 2n arrays) with a combine function; query(l, r) inclusive with left/right accumulation (like standard non-commutative range query — order matters! combine(left_res, right_res)). Must be careful: the combine operation is associative but NOT commutative, so the iterative query needs separate left-accumulator and right-accumulator, combined at the end as combine(accL, accR).
- Identity element: sum=0, pref=suff=best=-inf works (combine(identity, node) = node since max(-inf, ...) picks node's values, and sums: pref = max(id.pref, id.sum + node.pref) = max(-inf, node.pref) ✓).
- Answer must be at least the max element (non-empty subarray required); using -inf identity and only querying non-empty gaps handles this.

## worker: Implement the full solution in the starter code: i
**Key insight (corrected from initial draft):** after deleting all `x`'s, the gaps between occurrences become *contiguous*, so a subarray of the resulting array can span multiple consecutive gaps. Therefore for each `x` we must Kadane-merge the gap segment-tree nodes **in order** and take the merged node's `best` field — not just take the max over individual gaps. Example 1 confirms: deleting `-2` merges gaps `[-3,2]`, `[-1,3]`, `[3]` → merged array `[-3,2,-1,3,3]` with best subarray `2-1+3+3 = 7`. ✓

**Algorithm:**
1. Build an iterative segment tree; each node stores `(total, best_prefix, best_suffix, best_subarray)` — the standard mergeable Kadane summary. `combine` is associative but non-commutative, so range queries use left/right accumulators.
2. Candidate 1: no deletion → `query(0, n-1).best`.
3. Candidate 2: for each distinct value `x` with `count(x) < n` (deletion must leave a non-empty array), walk its sorted occurrence indices, query each non-empty gap `[prev+1, idx-1]` plus the tail, merge the gap nodes in order, and take `merged.best`.

**Complexity:** Build `O(n)`. Per value `x`: `count(x)+1` gap queries at `O(log n)` each → total `O((n + distinct)·log n) = O(n log n)`, fine for `n = 10^5`.

**Correctness argument:** Any subarray of the array after deleting `x` corresponds to a contiguous range covering parts of consecutive gaps; the merged Kadane summary over the full gap sequence computes exactly the max subarray sum of that concatenated array (standard exchange argument: `combine` preserves the four quantities needed to compute max subarray of a concatenation). Taking the max over all valid `x` and the no-deletion case covers all allowed operations.

**Edge cases handled:**
- `n = 1`: only the no-deletion case applies (the single value has `count == n`, skipped) → returns `nums[0]`.
- All same value: no valid deletion → original Kadane (the single element).
- All negatives: Kadane returns the max element; deleting the most-negative value is explored and correctly improves the answer (e.g., `[-5,-1,-5]` → delete `-5` → `-1`).
- Identity node `(0, -inf, -inf, -inf)` is a true identity for `combine`, and only non-empty gaps are queried, so `-inf` never leaks into a real answer.

**Trace on examples:**
- Ex 1: no-op → 4; `x=-2` → merged best 7; others ≤ 4 → answer **7** ✓
- Ex 2: `[1,2,3,4]` → no-op = 10; any deletion removes a positive → ≤ 9 → answer **10** ✓

## worker: Test the implementation against the provided examp
Tested the implementation thoroughly (traces + brute-force differential testing):

**Provided examples:**
- `[-3,2,-2,-1,3,-2,3]` → no-op = 4; x=-2 merges gaps `[-3,2]`, `[-1,3]`, `[3]` → best = 2-1+3+3 = 7; others ≤ 4 → **7** ✓
- `[1,2,3,4]` → no-op = 10; deletions give ≤ 9 → **10** ✓

**Edge cases:**
- `[-5,-1,-5]` → delete -5 → **-1** ✓
- `[7]` → only value has count == n, skipped → **7** ✓
- `[2,2,2]` → deletion disallowed (would empty), no-op Kadane = **6** ✓
- `[-1]` → **-1** ✓ (all-negative single element)
- Alternating values (e.g., `[3,-1,3,-1,3]` → delete -1 → 9) ✓
- All negatives with distinct values, value appearing in long runs, x at array boundaries (empty leading/trailing gaps correctly skipped) ✓

**Brute-force differential test:** wrote a checker that, for each distinct x with count < n, builds the filtered array and runs Kadane directly, taking the max including no-op. Ran on 2000+ random small arrays (n ∈ [1,12], values in [-5,5], plus all-negative and all-same biased distributions). All matched the segment-tree solution exactly.

Key correctness points verified:
- `combine` is associative; the iterative query's left/right accumulators handle non-commutativity correctly (tested against direct Kadane on random ranges).
- IDENTITY `(0, -inf, -inf, -inf)` never leaks into answers since only non-empty gaps are queried and `merged` always ends up covering ≥ 1 element (count(x) < n).
- Gaps merge in order, so subarrays spanning multiple consecutive gaps (the crucial insight) are captured via the merged node's `best` field.

Complexity: O(n log n) total — build O(n), and Σ over distinct x of (count(x)+1) gap queries = O((n + distinct) log n).
