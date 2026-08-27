
## ideation
The problem asks for the number of subarrays that can be made non-decreasing with at most `k` total increments. For a subarray `[l, r]`, the minimum cost to make it non-decreasing is the sum of deficits relative to the running maximum. This cost can be computed by scanning left to right: start with `cur = nums[l]`, and for each `i > l`, add `max(0, cur - nums[i])` to cost, then update `cur = max(cur, nums[i])`. The cost is non-decreasing in `r` for fixed `l`, and non-increasing in `l` for fixed `r`. We can precompute the "next greater element" for each index using a monotonic stack, which partitions the subarray into segments where the running max is constant. The cost to make a subarray non-decreasing is the sum of costs of these full segments plus a partial segment at the end. Using binary lifting on the `next` pointers, we can evaluate the cost for any `[l, r]` in O(log n). Then for each left endpoint `l`, we binary search the maximal right endpoint `r` such that cost ≤ `k`, and sum the counts. This gives an O(n log² n) algorithm.

## worker: Implement the full solution in Python: build next-
- The algorithm uses a monotonic stack to compute `next greater element` for each index, which partitions any subarray into segments with constant running max.
- For each index `i`, `seg_cost[i]` precomputes the cost to raise all elements between `i` and `nxt[i]` to `nums[i]`.
- Binary lifting allows jumping multiple segments in O(log n) time. The table stores both the ancestor and the accumulated cost of full segments.
- The `get_cost(l, r)` function uses binary lifting to find the last peak `≤ r` and sum the costs of all fully traversed segments, then adds the cost of the final partial segment.
- For each left endpoint `l`, a binary search finds the largest valid right endpoint `r` in O(log n), and we sum `r - l + 1` over all `l`. Total complexity: O(n log² n), which fits the constraints (n ≤ 10⁵).
- Verified with the two given examples and additional edge cases.
