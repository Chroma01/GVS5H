
## ideation
The core difficulty is efficiently calculating the sum of maximums (and minimums) for all subarrays with length at most `k`, given the constraint `n <= 80,000`. A naive $O(n^2)$ approach is too slow.

The standard "contribution technique" for "Sum of Subarray Minimums/Maximums" calculates the total contribution of each element by finding the range `[L, R]` where it is the min/max. Specifically, for each index `i`, we find:
- `left[i]`: the number of contiguous elements to the left of `i` that are greater than (or less than) `nums[i]` (until a smaller/larger element is found).
- `right[i]`: the number of contiguous elements to the right of `i` that are greater than (or less than) `nums[i]`.

The total number of subarrays where `nums[i]` is the min/max is `left[i] * right[i]`. However, we only want subarrays of length $\le k$.

For a fixed `i`, a subarray starting at `s` and ending at `e` includes `i` and has `nums[i]` as min/max if:
- $i - left[i] + 1 \le s \le i$
- $i \le e \le i + right[i] - 1$
- $e - s + 1 \le k \implies e \le s + k - 1$

We need to count the number of pairs $(s, e)$ satisfying these conditions.
Let $L = left[i]$ and $R = right[i]$.
The valid start indices are $s \in [i - L + 1, i]$.
For a fixed $s$, the valid end indices are $e \in [i, \min(i + R - 1, s + k - 1)]$.
The number of valid ends for a given $s$ is $\max(0, \min(i + R - 1, s + k - 1) - i + 1)$.

Let $M = i + R - 1$ be the maximum possible end index.
Let $limit(s) = s + k - 1$.
The count for a fixed $s$ is $\max(0, \min(M, limit(s)) - i + 1)$.

We can split the range of $s$ into two parts:
1. Where $limit(s) \ge M \implies s + k - 1 \ge i + R - 1 \implies s \ge i + R - k$.
   In this case, $\min(M, limit(s)) = M$. The count is $M - i + 1 = R$.
   This applies for $s \in [\max(i - L + 1, i + R - k), i]$.
   
2. Where $limit(s) < M \implies s < i + R - k$.
   In this case, $\min(M, limit(s)) = limit(s) = s + k - 1$. The count is $(s + k - 1) - i + 1 = s + k - i$.
   This applies for $s \in [i - L + 1, \min(i, i + R - k - 1)]$.

We can compute the sum of counts in $O(1)$ using arithmetic series formulas for each element. Then multiply by `nums[i]` and add to the total.

We will implement a helper function `calculate_sum(nums, k, is_max)` that:
1. Uses a monotonic stack to compute `left` and `right` arrays.
   - For max: `left` is distance to previous greater element, `right` is distance to next greater or equal element (to handle duplicates consistently, usually one side is strict and the other non-strict).
   - For min: `left` is distance to previous smaller element, `right` is distance to next smaller or equal element.
2. Iterates through each element, calculates the number of valid subarrays where it is the extreme, and adds `nums[i] * count` to the result.

Finally, return `calculate_sum(nums, k, True) + calculate_sum(nums, k, False)`.

Pitfalls:
- Handling duplicates correctly in monotonic stack to avoid double counting or missing subarrays. Standard practice: for max, use `>=` on one side and `>` on the other. For min, use `<=` on one side and `<` on the other.
- Integer overflow: Python handles large integers automatically, but the result can be large.
- Edge cases: $k=1$, $k=n$.
- The arithmetic series calculation must be precise.

## worker: Implement a helper function `get_contribution_sum(
The solution decomposes the problem into two independent parts: sum of maximums and sum of minimums for all subarrays of length 1 to k.

For each part, we use the "contribution technique":
1. **Monotonic Stack**: For each element `nums[i]`, we find the range `[L, R]` where it is the maximum (or minimum). Specifically:
   - `left[i]` is the number of consecutive elements to the left (including itself) where `nums[i]` is the extreme.
   - `right[i]` is the number of consecutive elements to the right (including itself) where `nums[i]` is the extreme.
   - To handle duplicates consistently, we use strict inequality on one side and non-strict on the other. For maximums, we pop `<=` on the left (finding previous strictly greater) and `<` on the right (finding next greater or equal). For minimums, we pop `>=` on the left (finding previous strictly smaller) and `>` on the right (finding next smaller or equal).

2. **Counting Valid Subarrays with Length Constraint**: For each element `i`, the subarrays where it is the extreme start in `[i - left[i] + 1, i]` and end in `[i, i + right[i] - 1]`. We need to count pairs `(s, e)` such that `e - s + 1 <= k`.
   - For a fixed start `s`, the valid ends are `e \in [i, \min(i + right[i] - 1, s + k - 1)]`.
   - The count of valid ends for a given `s` is `\max(0, \min(M, s + k - 1) - i + 1)` where `M = i + right[i] - 1`.
   - We split the range of `s` into two parts based on whether `s + k - 1 >= M` or not, and compute the sum of counts using arithmetic series formulas in O(1) per element.

3. **Complexity**: The monotonic stack passes are O(n). The contribution calculation is O(n) with O(1) per element. Total time complexity is O(n), which fits within the constraints. Space complexity is O(n) for the stacks and arrays.
