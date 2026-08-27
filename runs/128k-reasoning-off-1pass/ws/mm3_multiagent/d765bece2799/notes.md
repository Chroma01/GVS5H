
## ideation
**Core difficulty:**  
We need `sum_{subarrays of length ≤ k} (min(subarray) + max(subarray))`. The naive approach enumerates O(n·k) subarrays (too slow when k ≈ n = 80,000). We need O(n) or O(n log n).

**Key observation — suffix view of a sliding window:**  
Fix the right endpoint `r` and consider all valid left endpoints `l ∈ [max(0, r-k+1), r]`. These correspond exactly to the suffixes of the window `[max(0, r-k+1), r]`. So we need, for every position `r`, the sum of mins and sum of maxs over all suffixes of the current window.

**Maintaining these sums incrementally:**  
When we extend right by adding `v = nums[r]`:
- A brand-new suffix `[r, r]` is created with min = max = v.
- Every old suffix gains `v` on the right. Its new min = `min(old_min, v)` and new max = `max(old_max, v)`.

Store in each deque entries of the form `(value, count)` ordered by **position** (front = oldest suffix, back = newest). For the min-deque, values are non-decreasing; for the max-deque, non-increasing.

**Adding a value v to the min-deque:**
- Pop from the back while `back.value > v`, accumulating their counts into `c`. These popped suffixes' mins become v.
- If the new back has value exactly v, merge by adding c to its count. Otherwise, push `(v, c)`.
- Update `total_min` by subtracting the popped contributions and adding the new ones.

**Adding a value v to the max-deque:** Same idea but with `<` and merging on equality for the maximum.

**Shrinking the window (when size > k):**
- The oldest suffix is the front entry in each deque. Decrement its count by 1 and subtract its value from the running total. Pop if count hits 0.

This is fully O(n) amortized because each element enters and leaves each deque at most once.

**Pitfalls avoided:**
- Forgetting that front = oldest suffix (not the global min/max) — verified safe because monotonic order guarantees front.value equals the min/max of the oldest suffix.
- Integer overflow — Python handles big ints, but for languages like C++ we'd need 64-bit.
- Off-by-one when the window is smaller than k at the start (loop only shrinks while `r - l + 1 > k`).

**Verification:**  
Traced both given examples by hand — got 20 and −6, matching expected output. Also tested k=1 case (only single elements).

## worker: Implement the `minMaxSubarraySum` method using two
The solution uses two monotonic deques that store `(value, count)` pairs ordered by position within the sliding window. Each deque represents the mins (non-decreasing values) or maxs (non-increasing values) of all suffixes of the current window. When extending right, elements with worse values are popped from the back and their counts merged. When shrinking left, the front entry's count is decremented. Running totals `total_min` and `total_max` are maintained throughout for O(1) access to the current contribution. Verified on both examples: `[1,2,3]` with k=2 yields 20, and `[1,-3,1]` with k=2 yields -6.
