1. The problem asks us to split an array into three non-empty contiguous subarrays and maximize the sum of distinct counts in each.
2. A naive O(N^2) approach checking all pairs (i,j) is too slow for N up to 3*10^5. We need an O(N) or O(N log N) solution.
3. Key insight: The total distinct count is maximized when the three subarrays are "as distinct as possible". Note that the sum of distinct counts is at most N (if all elements are distinct) but can be less.
4. We can precompute prefix distinct counts `pre[i]` (distinct in A[0..i-1]) and suffix distinct counts `suf[i]` (distinct in A[i..N-1]).
5. For the middle subarray A[i+1..j], its distinct count is `total_distinct_in_A[i+1..j]`. The total score is `pre[i] + distinct(A[i+1..j]) + suf[j+1]`.
6. We can iterate over the right boundary `j` of the middle segment (from 1 to N-2, 0-indexed). For a fixed `j`, we want to maximize `pre[i] + distinct(A[i+1..j])` for `0 <= i < j`.
7. Let `mid[i][j]` be distinct count in A[i+1..j]. As we fix `j` and decrease `i`, `mid[i][j]` is non-decreasing. However, `pre[i]` is non-decreasing with `i`. This suggests we can't easily decouple.
8. Alternative approach: Iterate `j` from 1 to N-2. Maintain a data structure or running value for `max(pre[i] + distinct(A[i+1..j]))` for `i` from 0 to `j-1`.
9. Let `f(j) = max_{0<=i<j} (pre[i] + distinct(A[i+1..j]))`. Then answer is `max_{1<=j<=N-2} (f(j) + suf[j+1])`.
10. To compute `f(j)` efficiently: When moving from `j` to `j+1`, the middle segment extends. `distinct(A[i+1..j+1])` is either `distinct(A[i+1..j])` or `distinct(A[i+1..j]) + 1` depending on if `A[j+1]` is new in the range.
11. Specifically, let `last_pos[x]` be the last seen position of value `x`. For a fixed `j`, `distinct(A[i+1..j])` increases by 1 for all `i` such that `i+1 <= last_pos[A[j]]`? No. The distinct count in `A[i+1..j]` is the number of unique elements in that range.
12. Better: Use the fact that `distinct(A[i+1..j]) = pre[j+1] - pre[i]` is NOT true because of overlaps.
13. Let's use a different decomposition. Total distinct = `pre[i] + (distinct in A[i+1..j]) + suf[j+1]`.
14. We can iterate `j` from 1 to N-2. We need `max_i (pre[i] + distinct(A[i+1..j]))`.
15. Let `g(i, j) = distinct(A[i+1..j])`. Note `g(i, j) = g(i, j-1) + (1 if A[j] is not in A[i+1..j-1] else 0)`.
16. The condition "A[j] is not in A[i+1..j-1]" is equivalent to `i+1 > last_pos[A[j]]` (where `last_pos` is the last occurrence of `A[j]` before index `j`). Let `L = last_pos[A[j]]`. Then for `i >= L`, `A[j]` is NOT in `A[i+1..j-1]`? No. If `i+1 > L`, then the range `A[i+1..j-1]` does not include `L`, so `A[j]` is new. So for `i >= L`, the distinct count increases by 1. For `i < L`, it stays the same.
17. So, `g(i, j) = g(i, j-1) + 1` if `i >= L`, else `g(i, j-1)`.
18. Therefore, `pre[i] + g(i, j) = pre[i] + g(i, j-1) + (1 if i >= L else 0)`.
19. Let `M_j = max_{0<=i<j} (pre[i] + g(i, j))`.
    `M_j = max( max_{0<=i<L} (pre[i] + g(i, j-1)), max_{L<=i<j} (pre[i] + g(i, j-1) + 1) )`.
    `M_j = max( max_{0<=i<L} (pre[i] + g(i, j-1)), max_{L<=i<j} (pre[i] + g(i, j-1)) + 1 )`.
20. We can maintain the values `val[i] = pre[i] + g(i, j-1)` in a segment tree or two Fenwick trees / just track max with a variable? Since `L` changes, we need range max queries.
21. We can use a Segment Tree over indices `i` (0 to N-2). The segment tree stores `pre[i] + g(i, current_j)`. When moving from `j` to `j+1`, we update the segment tree: for all `i >= L_{j+1}`, add 1 to the value at `i`. Then query max over `0 <= i <= j`.
22. Segment tree with range add and range max query supports this in O(log N) per step. Total time O(N log N).