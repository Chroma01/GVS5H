
## ideation
The core difficulty is efficiently finding the maximum number of disjoint pairs (top, bottom) such that `top_size <= bottom_size / 2`. Since the array is sorted, we can use a greedy two-pointer approach. The key insight is that to maximize pairs, we should try to pair the smallest available mochi as "tops" with the smallest possible valid mochi as "bottoms". This saves larger mochi for other potential pairs.

A standard efficient strategy:
1. Use two pointers: `i` starting at 0 (for potential tops) and `j` starting at `N // 2` (for potential bottoms). Why `N // 2`? Because we can have at most `N // 2` pairs, so the bottom candidates must come from the second half of the sorted array to ensure we have enough distinct elements.
2. If `A[i] <= A[j] // 2`, we can form a pair. Increment both `i` and `j` and increment the count.
3. If not, increment `j` to try a larger bottom for the same top `i`.
4. Stop when either `i` reaches `N // 2` (no more tops to try) or `j` reaches `N` (no more bottoms to try).

This greedy approach works because:
- We always use the smallest available top, which is the easiest to satisfy the condition.
- We use the smallest available valid bottom, which saves larger bottoms for potentially larger tops.
- Since the array is sorted, if `A[i]` cannot be paired with `A[j]`, it cannot be paired with any `A[k]` where `k < j` (since those are smaller or equal and already considered or skipped).

Pitfalls:
- Starting `j` at 0 would be incorrect because we might pair small elements with small elements that could have been used as tops. Starting at `N // 2` ensures we don't use elements that could be tops as bottoms unnecessarily.
- Integer division: `A[j] // 2` is correct since we need `A[i] <= A[j] / 2`, which is equivalent to `2 * A[i] <= A[j]` using integer arithmetic.

## worker: none
The solution uses a greedy two-pointer approach. Since the mochi are sorted by size, we can efficiently find the maximum number of valid pairs. 

Key insights:
1. We can have at most `N // 2` pairs, so we only need to consider the first `N // 2` elements as potential "tops" and the remaining elements as potential "bottoms".
2. We start pointer `i` at 0 (smallest mochi, easiest to satisfy the condition as a top) and pointer `j` at `N // 2` (smallest possible bottom that doesn't overlap with top candidates).
3. If `2 * A[i] <= A[j]`, we form a pair and move both pointers forward. This is optimal because we're using the smallest valid bottom for the current smallest top, saving larger bottoms for potentially larger tops.
4. If the condition isn't met, we increment `j` to try a larger bottom for the same top `i`.
5. The algorithm runs in O(N) time since each pointer moves at most N times, and O(1) extra space.
