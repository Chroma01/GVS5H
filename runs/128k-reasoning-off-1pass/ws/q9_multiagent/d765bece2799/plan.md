The problem requires summing the max and min of all valid subarrays (length ≤ k). A naive O(N^2) approach iterating all subarrays will time out given N up to 80,000. We need an O(N) or O(N log N) solution. We can iterate through each starting position `i` and maintain a sliding window of length at most `k` ending at `j`. However, a more efficient approach is to iterate through each element as the *end* of a subarray and use a monotonic deque to efficiently track the maximum and minimum in the valid window range `[i, j]` where `j - i + 1 <= k`. Specifically, for each `j` from 0 to N-1, the valid start indices `i` are in the range `[max(0, j-k+1), j]`. We can maintain two deques: one for the maximums and one for the minimums in the current window of valid starts. As we move `j`, we update the deques and add the sum of the current max and min for each valid window ending at `j`. Actually, a simpler O(N*k) might still be too slow if k is large, but constraints say k <= N. Let's re-evaluate: The total number of subarrays is O(N*k). If k is small, O(N*k) is fine. If k is large (close to N), O(N*k) is O(N^2) which is too slow.
Correct approach: Iterate `j` from 0 to N-1. The valid subarrays ending at `j` start at `i` where `j-k+1 <= i <= j`. We need sum of (max(nums[i:j+1]) + min(nums[i:j+1])) for all valid `i`.
We can use a monotonic deque to find the max/min for the current window. But we need the sum over all valid `i`.
Alternative: Use a segment tree or sparse table? Building sparse table is O(N log N), query is O(1). Total time O(N * k) queries -> O(N*k) worst case. Still potentially O(N^2).
Wait, is there an O(N) solution?
Yes. We can compute the contribution of each element as the maximum and minimum across all subarrays where it is the max/min.
For maximums: An element `nums[i]` is the maximum of a subarray `nums[l...r]` if `l <= i <= r` and `nums[i]` is the first maximum to the left and right (handling duplicates carefully). The range of `l` is `(prev_greater[i], i]` and `range of r` is `[i, next_greater[i])`. The length of the subarray is `r - l + 1`. We need to sum `nums[i]` for all subarrays `nums[l...r]` such that `r - l + 1 <= k`.
This transforms the problem into: for each `i`, find the number of pairs `(l, r)` such that `prev_greater[i] < l <= i <= r < next_greater[i]` and `r - l + 1 <= k`.
This can be solved in O(N) using two pointers or math.
Let `L = i - prev_greater[i]` and `R = next_greater[i] - i`. The valid `l` are in `(i-L, i]` (count L) and `r` are in `[i, i+R)` (count R).
We need to sum `nums[i]` for all `l, r` such that `l > i-L`, `r < i+R`, `l <= i <= r`, and `r - l + 1 <= k`.
Let `x = i - l` (distance to left, 0 to L-1) and `y = r - i` (distance to right, 0 to R-1). Condition: `x + y + 1 <= k` => `x + y <= k - 1`.
We need to count pairs `(x, y)` with `0 <= x < L`, `0 <= y < R`, `x + y <= k - 1`.
This is a standard counting problem solvable in O(1) per element.
Same logic applies for minimums.
Total complexity O(N).