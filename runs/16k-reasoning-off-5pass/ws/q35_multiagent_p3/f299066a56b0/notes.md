
## ideation
The core difficulty is efficiently finding the maximum matching in a bipartite graph where edges exist if `top_size <= bottom_size / 2`. Since the array is sorted, we can use a greedy two-pointer approach. The key insight is that to maximize pairs, we should try to pair the smallest available "top" mochi with the smallest valid "bottom" mochi. This saves larger bottom mochi for potentially larger top mochi.

We can split the array into two halves: the first half (indices `0` to `N/2 - 1`) are candidates for the top mochi, and the second half (indices `N/2` to `N-1`) are candidates for the bottom mochi. This is because a top mochi must be smaller than its corresponding bottom mochi (since `a <= b/2` implies `a < b` for positive integers), so the top mochi must come from the smaller half of the sorted array.

Algorithm:
1. Initialize `left = 0` (pointer for top candidates) and `right = N // 2` (pointer for bottom candidates).
2. Initialize `count = 0`.
3. While `left < N // 2` and `right < N`:
   - If `A[left] <= A[right] // 2`, then we can form a pair. Increment `count`, `left`, and `right`.
   - Otherwise, the current bottom mochi is too small for the current top mochi. We need a larger bottom mochi, so increment `right`.
4. The result is `count`.

Pitfalls:
- Using integer division correctly: `a <= b / 2` is equivalent to `2 * a <= b` to avoid floating point issues.
- Ensuring the pointers stay within bounds.
- The split at `N // 2` is valid because we can have at most `N // 2` pairs, so we only need to consider the first `N // 2` elements as potential tops.

## worker: Implement the two-pointer greedy algorithm as desc
The algorithm uses a greedy two-pointer approach:
1. Since the array is sorted, we split it into two halves: the first `N//2` elements are candidates for the "top" mochi (smaller ones), and the remaining elements are candidates for the "bottom" mochi (larger ones).
2. We use `left` pointer starting at 0 (first element) and `right` pointer starting at `N//2` (first element of the second half).
3. For each `left`, we check if `2 * A[left] <= A[right]`. If true, we form a pair and move both pointers forward. If false, the current bottom is too small, so we move `right` forward to try a larger bottom.
4. This greedy strategy works because pairing the smallest valid top with the smallest valid bottom saves larger bottoms for potentially larger tops, maximizing the total number of pairs.
5. Time complexity is O(N) since each pointer moves at most N times. Space complexity is O(N) to store the input array.
