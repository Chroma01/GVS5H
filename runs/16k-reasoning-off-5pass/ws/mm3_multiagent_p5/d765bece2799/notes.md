
## ideation
The problem asks for the sum of (min + max) over all subarrays of `nums` whose length is at most `k`. Brute-forcing all O(n^2) subarrays is infeasible for `n ≤ 80000`.

**Core idea:** For each element `nums[i]`, determine how many subarrays of length ≤ k have `nums[i]` as the minimum, and how many have it as the maximum. Then sum `nums[i] * (count_as_min + count_as_max)`.

**Standard technique:** Use monotonic stacks to find, for each index `i`:
- `left_smaller[i]`: distance to the previous smaller element (strictly smaller). The number of subarrays ending at `i` where `nums[i]` is the minimum equals `left_smaller[i]` (when extending leftward until hitting a smaller element). Similarly for `left_larger[i]` for maximum.
- `right_smaller[i]` / `right_larger[i]`: distance to the next smaller/larger element for counting subarrays starting at `i`.

The total number of subarrays where `nums[i]` is the minimum is `left_smaller[i] * right_smaller[i]` (or use either left or right counts, not both). Since we want subarrays of length ≤ k, we must clamp the count.

**Clamping approach:** When extending leftward, we can go at most `k` elements back. So the contribution of `nums[i]` as min in subarrays ending at `i` is `min(left_smaller[i], k)`. But this only counts subarrays ending at `i`; to count all subarrays of any length ≤ k where `nums[i]` is min, we'd typically multiply left and right distances. A cleaner approach:

- For each `i`, find `prev_smaller[i]` (previous index with value < nums[i]) and `next_smaller[i]` (next index with value ≤ nums[i]) to avoid double-counting (standard technique for "subarrays where this is the unique minimum").
- Number of subarrays where `nums[i]` is the min: `(i - prev_smaller[i]) * (next_smaller[i] - i)`.
- To restrict length ≤ k: we need both dimensions ≤ k. Specifically, for a subarray `[l, r]` containing `i` where `nums[i]` is min, the length is `r - l + 1`. The number of valid choices is constrained by both sides.

**Simpler clamping:** Iterate `i` from 0 to n-1. Maintain a monotonic increasing stack for minimums. As we extend, for each `i`, the number of subarrays ending at `i` of length ≤ k with `nums[i]` as the minimum can be computed using the stack. Specifically, if we look at the stack and clamp the "left bound" to `max(0, i - k + 1)`, we get the count.

Actually, a clean O(n) approach:
- Precompute `left[i]` = distance to previous strictly smaller element (or start of array, capped at k for minimum contributions).
- For each i, the number of subarrays ending at i where nums[i] is the minimum AND length ≤ k is `min(left[i], k)`.
- Wait — this isn't quite right because `left[i]` counts all valid left extensions, but we cap at k. The count of subarrays ending at i of length ≤ k where nums[i] is the min: the left boundary `l` can be anything in `[max(0, i-k+1), i]` such that no element in `[l, i-1]` is < nums[i]. If `prev_smaller[i] = j`, then for `l > j`, nums[i] is the min. So valid `l` values are `max(j+1, i-k+1)` to `i`, giving count `min(i - j, k)`. ✓

So:
- For minimums: `count_min[i] = min(i - prev_smaller[i], k)` where `prev_smaller[i]` is the last index < i with `nums[prev_smaller[i]] < nums[i]` (or -1 if none). Use a monotonic increasing stack.
- For maximums: `count_max[i] = min(i - prev_larger[i], k)` where `prev_larger[i]` is the last index < i with `nums[prev_larger[i]] > nums[i]`. Use a monotonic decreasing stack.

But this only counts subarrays ending at i. However, summing `nums[i] * count_min[i]` over all i gives the total contribution of each element as the minimum across all subarrays of length ≤ k. Because every subarray has exactly one minimum, and that minimum is counted once when we process its rightmost (or in this formulation, the element as the right endpoint). 

Wait, we need to be careful. The standard trick: sum over i of (nums[i] * number of subarrays where nums[i] is the min) = total of mins over all subarrays. And "subarrays where nums[i] is the min" can be counted as: subarrays ending at i where nums[i] is the min = `min(i - prev_smaller[i], k)`. Summing this over all i gives the total of min values across all subarrays of length ≤ k. ✓

Same for max with `prev_larger[i]`.

**Pitfalls:**
- Stack indices: ensure `prev_smaller` uses strictly smaller (use `<` for popping when current ≤ top's value for prev_smaller; for prev_larger, pop when current ≥ top's value).
- For minimum: we want previous strictly smaller, so pop while `nums[stack_top] >= nums[i]`. The new top (or -1) is `prev_smaller[i]`.
- For maximum: pop while `nums[stack_top] <= nums[i]`. New top is `prev_larger[i]`.
- `k` can be up to n, so `min(..., k)` is safe.
- Sum can be large: up to 80000 * 10^6 * 80000 ≈ 6.4e15, needs 64-bit (Python int handles this fine).
- Negative numbers: no special handling needed.

## worker: Implement the solution in the `Solution` class usi
**Approach:** Use two monotonic stack passes to compute, for each index `i`:
- `prev_smaller[i]`: the last index before `i` where `nums[j] < nums[i]` (or `-1` if none). The number of subarrays ending at `i` of length ≤ k where `nums[i]` is the minimum equals `min(i - prev_smaller[i], k)`.
- `prev_larger[i]`: the last index before `i` where `nums[j] > nums[i]` (or `-1` if none). Similarly for maximums.

**Why this counts correctly:** Every subarray has a unique minimum and maximum. By considering subarrays that *end* at `i`, we count each subarray exactly once. For a subarray `[l, i]` to have `nums[i]` as its minimum, no element in `[l, i-1]` can be smaller than `nums[i]`, so `l > prev_smaller[i]`. The number of valid `l` values is `i - prev_smaller[i]`. Restricting to length ≤ k means `l ≥ i - k + 1`, so the count is `min(i - prev_smaller[i], k)`. Symmetric argument for maximums.

**Verification with examples:**
- `nums = [1,2,3], k=2`: Total = 20 ✓
- `nums = [1,-3,1], k=2`: Total = -6 ✓

**Complexity:** O(n) time and O(n) space.

**Edge cases handled:**
- All negative numbers
- k = 1 (only single-element subarrays)
- k = n (all subarrays)
- Duplicate values: strictly smaller/larger comparisons prevent double-counting in `prev_smaller` (uses `>=` to pop) and `prev_larger` (uses `<=` to pop).
