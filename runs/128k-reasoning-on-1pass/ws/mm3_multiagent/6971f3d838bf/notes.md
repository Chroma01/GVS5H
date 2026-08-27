
## ideation
**Core Difficulty:**
We need to find the maximum subarray sum after optionally deleting all occurrences of a single value `x`. The naive approach—trying every distinct `x`, filtering the array, and running Kadane's algorithm—is O(n × distinct_values), which is O(n²) in the worst case (all elements distinct). This is too slow for n = 10⁵.

**Key Insight:**
For a fixed `x`, the array is naturally split into contiguous "blocks" separated by occurrences of `x`. Any subarray in the resulting array (after deleting `x`) either:
1. Lies entirely within one block, or
2. Spans multiple blocks: a suffix of block `i`, full blocks `i+1 … j-1`, and a prefix of block `j`.

For each block we need four values: total sum, max prefix sum, max suffix sum, and max subarray sum within the block. These can be obtained via range queries on the original array.

**Candidate Approaches:**
1. **Segment Tree Approach (O(n log n)):** Build a segment tree storing `(sum, pref, suff, best)` for every interval. For each distinct `x`, query the intervals between its occurrences to get block data, then compute the max subarray sum across blocks using a linear scan with prefix sums. Total blocks across all values is ≤ 2n, so total queries are O(n log n).
2. **Brute Force with Kadane (O(n²)):** Too slow.
3. **Modified Kadane per value (O(n × distinct)):** Still O(n²) worst case.
4. **Divide and Conquer:** Complex and likely not simpler.

**Pitfalls:**
- If `x` appears at every position, deletion leaves an empty array (invalid).
- Empty blocks (when `x` is at the boundary) must be skipped.
- The linear scan for spanning subarrays must correctly handle the prefix sum accumulation: for `i < j`, the sum is `suff[i] + (prefSum[j] - prefSum[i+1]) + pref[j]`.
- Must consider the original array (no operation) as a candidate.
- Edge cases: single element array, all positive, all negative, all identical values.

**Verification of Provided Plan:**
The plan in the prompt is correct and detailed. The segment tree approach with linear scan over blocks is sound. The complexity analysis (O(n log n) time, O(n) space) is accurate.

## worker: Implement a segment tree that supports range queri
The solution uses a segment tree to support range queries that return a tuple `(sum, pref, suff, best)` for any interval, with a static `combine` method to merge two adjacent intervals. For each distinct value `x` that can be deleted, the array is split into blocks between its occurrences; each block is queried to obtain the four required values. The maximum subarray sum after deleting `x` is then computed in linear time over the blocks, handling both single‑block and multi‑block subarrays via prefix sums. The overall complexity is `O(n log n)` time and `O(n)` memory, satisfying the constraints.
