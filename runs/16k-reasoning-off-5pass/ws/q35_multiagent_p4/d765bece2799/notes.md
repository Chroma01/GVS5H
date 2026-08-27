
## ideation
The core difficulty is efficiently calculating the contribution of each element to the sum of maximums and minimums for all subarrays of length at most $k$. A naive approach is $O(N^2)$, which is too slow for $N=80,000$. We need an $O(N)$ or $O(N \log N)$ approach.

The standard technique for "sum of subarray maximums/minimums" uses monotonic stacks to find the range $(L, R)$ where a specific element `nums[i]` is the maximum (or minimum). For the "at most k" constraint, the range of valid subarrays containing `i` is restricted not just by the values (monotonic stack boundaries) but also by the length constraint $k$.

For each element `nums[i]`:
1.  Find `left[i]`: the index of the previous element that is strictly greater than `nums[i]` (for max calculation). If none, -1.
2.  Find `right[i]`: the index of the next element that is greater than or equal to `nums[i]` (for max calculation). If none, $N$.
    *   Note: Using strict inequality on one side and non-strict on the other avoids double-counting when duplicates exist.
3.  The natural range where `nums[i]` is the maximum is `(left[i], right[i])`. Let `l = left[i] + 1` and `r = right[i] - 1`.
4.  The subarrays containing `i` within this range have start index `s` in `[l, i]` and end index `e` in `[i, r]`.
5.  The constraint is `e - s + 1 <= k`, or `e - s <= k - 1`.
6.  We need to count pairs `(s, e)` such that `l <= s <= i`, `i <= e <= r`, and `s + k - 1 >= e`.
    *   This is equivalent to counting pairs in a rectangle defined by `s \in [l, i]`, `e \in [i, r]` that lie below the line `e = s + k - 1`.
7.  This count can be computed in $O(1)$ using arithmetic series logic by splitting the range of `s` based on whether the constraint `e <= min(r, s + k - 1)` is active.
8.  We do this for both max and min contributions. For min, we find `prev_less` and `next_less_equal`.

Pitfalls:
-   Double counting with duplicates: Ensure strict/non-strict inequalities are consistent.
-   Off-by-one errors in range boundaries.
-   Complexity of the counting logic: It must be $O(1)$ per element.

## worker: Implement a helper function `get_contribution(nums
The solution decomposes the problem into two independent calculations: the sum of maximums and the sum of minimums for all subarrays of length at most $k$.

1.  **Monotonic Stack for Range Identification**: For each element `nums[i]`, we determine the range `(l, r)` where it is the maximum (or minimum). 
    -   For **maximums**: We find the previous index with a strictly greater value (`prev_greater`) and the next index with a greater or equal value (`next_greater_equal`). This ensures that if there are duplicate maximums, each subarray's maximum is attributed to exactly one element (the leftmost one in case of ties, due to the strict/non-strict combination).
    -   For **minimums**: Similarly, we find the previous index with a strictly smaller value and the next index with a smaller or equal value.
    -   The range where `nums[i]` is the dominant element is `(prev[i] + 1, next_idx[i] - 1)`.

2.  **Counting Valid Subarrays with Length Constraint**: Within the identified range, a subarray containing `i` is defined by its start `s` and end `e` such that `l <= s <= i` and `i <= e <= r`. The constraint is that the length `e - s + 1 <= k`, which simplifies to `e <= s + k - 1`.
    -   For a fixed `s`, the number of valid `e`'s is `min(r, s + k - 1) - i + 1`.
    -   We split the range of `s` into two parts to compute the sum efficiently in $O(1)$:
        -   **Part 1**: `s` is large enough such that `s + k - 1 >= r`. Here, `e` can go up to `r`. The count per `s` is constant (`r - i + 1`).
        -   **Part 2**: `s` is small such that `s + k - 1 < r`. Here, `e` is limited by `s + k - 1`. The count per `s` increases linearly with `s`. This forms an arithmetic series.

3.  **Complexity**: The monotonic stack passes are $O(N)$. The counting loop is $O(N)$ with $O(1)$ work per element. Total time complexity is $O(N)$, which fits within the constraints for $N=80,000$. Space complexity is $O(N)$ for the stack and auxiliary arrays.
