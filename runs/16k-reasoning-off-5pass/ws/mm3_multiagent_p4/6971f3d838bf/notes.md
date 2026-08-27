
## ideation
The problem asks for the maximum subarray sum after optionally deleting all occurrences of one distinct integer `x` from the array. The key observation is that deleting `x` is equivalent to treating `x` as 0 when computing subarray sums, because a subarray in the resulting array corresponds to an interval in the original array with all `x`'s removed, and its sum equals the original interval sum minus `count_x * x`. Thus, for each candidate `x`, we need the maximum subarray sum of the array with all `x` replaced by 0. The answer is the maximum over all `x` (including the original array, i.e., no deletion).

A naive approach would run Kadane for each unique `x`, leading to O(n * unique) time, which is O(n²) in the worst case. Instead, we can use a segment tree that supports point updates and queries the maximum subarray sum. For each unique `x`, we update all its positions to 0, query the tree, then revert the updates. Since each position is updated twice (to 0 and back), the total time is O(n log n). We must skip `x` if it appears in every element (deleting it would empty the array).

Pitfalls:
- The segment tree must correctly handle negative numbers and all-negative arrays.
- The combination logic for prefix/suffix/max subarray must be accurate.
- We must consider the case of no operation (original max subarray sum).
- Edge case: if all elements are the same and we delete that value, the array becomes empty, which is invalid.

## worker: Implement the segment tree class with methods to b
The solution uses a segment tree to efficiently compute the maximum subarray sum after zeroing all occurrences of a candidate value `x`. For each unique value `v`, we temporarily set its positions to 0, query the tree for the best subarray sum, then restore the original values. Each position is updated twice (to 0 and back), so the total time is O(n log n). The case of no operation is handled by the initial query. Values that appear in every element are skipped to avoid emptying the array.

The segment tree nodes store total sum, maximum prefix, maximum suffix, and maximum subarray sum, combined using standard formulas. The iterative implementation avoids recursion depth issues.

The algorithm correctly handles negative numbers and all-negative arrays because the segment tree's combination logic works for any integer values.
