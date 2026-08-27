- **Cost characterization:** For subarray `nums[l..r]`, the minimum final value at index `i` is `max(nums[l..i])`. Therefore the required operation count is `sum(max(nums[l..i]) - nums[i])`.

- **Window representation:** Consecutive positions having the same prefix maximum are stored as blocks `[target, count, original_sum]`. Their contribution is `target * count - original_sum`. Targets are strictly increasing from left to right.

- **Processing direction:** Iterate left endpoints from right to left. Prepending value `x` merges every leading block whose target is at most `x`, because those positions now have prefix maximum `x`.

- **Right deletion:** Removing the rightmost element does not alter prefix maxima of remaining positions. Its cost contribution is simply `last_block_target - nums[right]`.

- **Two-pointer property:** For a fixed left endpoint, extending the right endpoint cannot decrease cost. When moving leftward, prepending can only increase or preserve costs for existing suffix positions, so the greatest valid right endpoint never moves right.

- **Counting:** After shrinking, all endpoints from `left` through `right` are valid, contributing `right - left + 1`.

- **Correctness:** The maintained block sum equals the exact minimum increment cost of the current subarray. The shrink loop restores cost at most `k`; monotonicity makes `right` maximal. Thus every valid subarray is counted exactly once by its left endpoint.

- **Complexity:** Each block/element is inserted, merged, and removed at most once. Time is `O(n)` and space is `O(n)`.

- **Bounds:** Cost can reach below `n * 10^9`, about `10^14`, and the answer can reach `n(n+1)/2`, about `5 * 10^9`. Python integers safely handle both.
