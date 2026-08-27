
## ideation
The core difficulty is efficiently calculating the contribution of each element to the total sum of maximums and minimums for all subarrays of length at most $k$. A naive $O(N^2)$ approach is too slow. The key insight is to decompose the problem into two independent subproblems: sum of maximums and sum of minimums. For each element, we determine how many valid subarrays (length $\le k$) have this element as the maximum (or minimum). This requires finding the nearest greater/smaller elements to the left and right, but constrained by the window size $k$. Specifically, for an element at index $i$, the left boundary is the first index to the left where the value is strictly greater (for max) or strictly smaller (for min), or $i-k$ if no such element exists within $k$ distance. Similarly for the right boundary, using non-strict inequalities to avoid double counting. The number of subarrays where `nums[i]` is the max/min is `(i - left_bound) * (right_bound - i)`. We use monotonic stacks to find these boundaries in $O(N)$ time.

Pitfalls:
1. Handling the constraints of subarray length $\le k$ correctly when determining boundaries.
2. Avoiding double counting by using strict/non-strict inequalities appropriately (e.g., for max, use strict on one side and non-strict on the other).
3. Ensuring the monotonic stack logic correctly identifies the nearest greater/smaller elements within the $k$-distance constraint.

## worker: Implement a helper function to calculate the sum o
The solution decomposes the problem into two independent parts: sum of maximums and sum of minimums for all subarrays of length at most $k$. 

For each part, we use a monotonic stack to find, for each element, the range of subarrays where it is the maximum (or minimum). The key is handling the constraint that subarray length must be at most $k$. This is done by setting the left/right boundaries to `i - k` and `i + k` respectively when no closer "blocking" element is found. The number of subarrays where `nums[i]` is the max/min is `(i - left_bound) * (right_bound - i)`, where `left_bound` is the exclusive left boundary index and `right_bound` is the exclusive right boundary index.

To avoid double counting when there are duplicate values, we use strict inequality on one side and non-strict on the other. For maximums: left uses strict greater (`>`), right uses non-strict greater (`>=`). For minimums: left uses strict smaller (`<`), right uses non-strict smaller (`<=`).

The time complexity is $O(N)$ for each helper function (two passes with monotonic stacks), and space complexity is $O(N)$ for the stacks and boundary arrays.
