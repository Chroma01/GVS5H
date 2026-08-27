
## ideation
The core difficulty is efficiently calculating the sum of maximums and minimums for all subarrays of length 1 to `k`. A brute-force approach would be $O(n \cdot k)$, which is too slow given $n \le 80,000$. The standard "Sum of Subarray Minimums" problem can be solved in $O(n)$ using a monotonic stack to find the range where each element is the minimum. However, the constraint "at most `k` elements" complicates this because the standard approach considers all subarrays within the range $(prev\_smaller, next\_smaller)$.

To handle the `k` constraint, for each element `nums[i]`, we need to count how many subarrays of length $\le k$ include `i` and where `nums[i]` is the minimum (or maximum). 
Let `L` be the distance to the previous smaller element (for min) or larger element (for max), and `R` be the distance to the next smaller or equal element (for min) or larger or equal element (for max). The valid range for `i` being the min/max is `(prev_idx, next_idx)`.
The number of subarrays of length $\le k$ that include `i` and stay within this range is calculated by considering the left and right boundaries. Specifically, the left boundary can extend at most `L` positions to the left, and the right boundary can extend at most `R` positions to the right. However, the total length of the subarray must be $\le k$.
For each `i`, the contribution is `nums[i] * count`, where `count` is the number of valid subarrays.
The count can be computed as follows:
Let `left = min(L, k)` and `right = min(R, k)`. But we must ensure the total length doesn't exceed `k`.
Actually, a simpler way is:
For each `i`, find `P` (index of previous element strictly smaller for min, or strictly larger for max) and `N` (index of next element smaller or equal for min, or larger or equal for max).
The range is `(P, N)`. The number of subarrays of length $\le k$ containing `i` within this range is:
Iterate over possible left extensions `l` from `0` to `min(i - P, k - 1)` and right extensions `r` from `0` to `min(N - 1 - i, k - 1 - l)`. This is $O(k)$ per element, leading to $O(nk)$ worst case.

A better $O(n)$ approach:
For each `i`, let `left_dist = i - P` and `right_dist = N - i`.
The number of subarrays of length $\le k$ where `nums[i]` is the min/max is the number of pairs `(l, r)` such that $0 \le l \le left\_dist$, $0 \le r \le right\_dist$, and $l + r + 1 \le k$.
This can be computed in $O(1)$ using formulas.
Let `a = min(left_dist, k)` and `b = min(right_dist, k)`.
If `a + b + 1 <= k`, then all combinations are valid: count = `a * b + a + b + 1`? No, the formula is more complex.
Actually, we can split into cases:
1. If `left_dist + right_dist + 1 <= k`: all subarrays in the range are valid. Count = `(left_dist + 1) * (right_dist + 1)`.
2. If `left_dist + right_dist + 1 > k`: we need to count pairs `(l, r)` with $l \in [0, left\_dist]$, $r \in [0, right\_dist]$, $l + r \le k - 1$.
   This is equivalent to counting lattice points under a line.
   Let `limit = k - 1`.
   For `l` from `0` to `min(left_dist, limit)`, `r` can range from `0` to `min(right_dist, limit - l)`.
   Sum over `l`: $\sum_{l=0}^{min(left\_dist, limit)} min(right\_dist, limit - l)$.
   This sum can be computed in $O(1)$ by splitting the range of `l` where `limit - l >= right_dist` and where `limit - l < right_dist`.

We will implement a helper function `sum_extremes(nums, k, is_min=True)` that computes the sum of min (or max) for all subarrays of length $\le k$. Then return the sum of both.

Pitfalls:
- Handling equality correctly in monotonic stack (use strict inequality on one side and non-strict on the other to avoid double counting).
- Correctly computing the count of subarrays with length $\le k$.
- Large numbers: use 64-bit integers (Python handles this automatically).

## worker: Implement a helper function `sum_of_extremes(nums,
The solution computes the sum of maximums and minimums separately using a monotonic stack to determine the range where each element is the maximum (or minimum). For each element, we calculate the number of subarrays of length at most `k` where it is the extremum. This involves counting lattice points `(l, r)` such that `0 <= l <= left_dist - 1`, `0 <= r <= right_dist - 1`, and `l + r + 1 <= k`. The count is computed in O(1) by splitting the range of `l` into two parts where the upper bound for `r` is constant or linear. The monotonic stack ensures O(n) time complexity for finding the ranges. Equality handling is done by using strict inequality on one side and non-strict on the other to avoid double counting.
