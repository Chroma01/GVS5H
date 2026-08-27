1. The problem asks us to split an array into three non-empty contiguous subarrays and maximize the sum of distinct elements in each subarray.
2. A naive O(N^2) approach checking all pairs (i,j) is too slow for N up to 3*10^5. We need an O(N) or O(N log N) solution.
3. Let the split points be i and j (1 <= i < j <= N-1). The three parts are A[0..i-1], A[i..j-1], A[j..N-1] (0-indexed).
4. We can precompute prefix distinct counts `pre[k]` = distinct elements in A[0..k-1] and suffix distinct counts `suf[k]` = distinct elements in A[k..N-1].
5. The middle part's distinct count is harder to query quickly. However, note that the total distinct count is `pre[i] + distinct(A[i..j-1]) + suf[j]`.
6. We can iterate over the first split point `i` from 1 to N-2. For a fixed `i`, we want to maximize `distinct(A[i..j-1]) + suf[j]` for `j` from `i+1` to N-1.
7. Alternatively, we can iterate over the middle part's right endpoint `j` or use a sweep-line approach. A common technique for this type of problem is to iterate `j` from 2 to N-1 (right split point) and maintain the best value for the left part + middle part as we move `j`.
8. Actually, a more efficient approach: Iterate `j` from 2 to N-1. As we increase `j`, the middle part A[i..j-1] grows. But `i` also varies.
9. Let's fix the right split point `j`. The third part is fixed: `suf[j]`. We need to maximize `pre[i] + distinct(A[i..j-1])` for `1 <= i <= j-1`.
10. Let `f(j) = max_{1<=i<=j-1} (pre[i] + distinct(A[i..j-1]))`. Then the answer is `max_{2<=j<=N-1} (f(j) + suf[j])`.
11. To compute `f(j)` efficiently, notice that when moving from `j` to `j+1`, the element `A[j]` is added to the middle part for all `i <= j`. This changes the distinct count for all intervals ending at `j`. This seems complex to update for all `i`.
12. Alternative: Iterate `i` from 1 to N-2. Precompute `pre[i]`. Then we need `max_{j=i+1}^{N-1} (distinct(A[i..j-1]) + suf[j])`.
13. Let's use the property that `distinct(A[i..j-1])` can be tracked. We can iterate `i` from N-2 down to 1. As we decrease `i`, we add `A[i]` to the middle part. But the middle part is A[i..j-1], so changing `i` changes the start of the middle part for all `j`.
14. Better approach: Iterate `j` from 2 to N-1. Maintain a data structure that allows querying `max(pre[i] + distinct(A[i..j-1]))`.
15. Actually, there is a known technique: The function `g(i, j) = distinct(A[i..j-1])` is not easy to maintain for all `i`.
16. Let's try iterating the middle part's end `j` and start `i`. Consider that `distinct(A[i..j-1]) = pre[j] - pre[i] + ...`? No, distinct counts don't subtract linearly.
17. Correct efficient approach: 
    - Precompute `pre[k]` for all k.
    - Precompute `suf[k]` for all k.
    - Iterate `j` from 2 to N-1. We want `max_{1<=i<=j-1} (pre[i] + distinct(A[i..j-1]))`.
    - Let `val[i] = pre[i] + distinct(A[i..j-1])`. When we move from `j` to `j+1`, the element `A[j]` is appended to the middle segment for all `i`. If `A[j]` was not present in `A[i..j-1]`, then `distinct(A[i..j]) = distinct(A[i..j-1]) + 1`. If it was present, it stays the same.
    - The condition "A[j] was not present in A[i..j-1]" depends on the last occurrence of `A[j]`. Let `last_pos[x]` be the last seen position of value `x`. If `last_pos[A[j]] < i`, then `A[j]` is new to the segment starting at `i`.
    - So, for all `i <= last_pos[A[j]]`, the distinct count doesn't change. For all `i > last_pos[A[j]]`, the distinct count increases by 1.
    - We can maintain an array `best[i] = pre[i] + distinct(A[i..current_j-1])`. When moving `j` to `j+1`, we update `best[i]` for `i > last_pos[A[j]]` by adding 1. Then query the max.
    - This can be done with a Segment Tree with lazy propagation. Range add 1 for `i` in `[last_pos[A[j]] + 1, j-1]`. Then query max in `[1, j-1]`.
    - Complexity: O(N log N).