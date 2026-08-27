1. First, compute the maximum subarray sum of the original array using Kadane's algorithm. This covers the case where we perform no operation.
2. Identify all unique elements in the array. For each unique element x, we need to compute the maximum subarray sum of the array with all occurrences of x removed.
3. Instead of physically removing elements (which is O(n) per unique element and too slow), we can use a prefix/suffix approach. Precompute prefix max subarray sums and suffix max subarray sums for the original array.
4. For each unique element x, the array after removal consists of segments that are between occurrences of x. The maximum subarray sum in the removed array is the maximum of:
   - The maximum subarray sum entirely within any segment between two consecutive occurrences of x (or before the first/after the last).
   - We can precompute for each position, the max subarray sum ending at or before that position (prefix) and starting at or after that position (suffix).
5. Actually, a more efficient approach: For each unique x, the "gaps" between its occurrences are independent. We can precompute an array `left_max[i]` = max subarray sum in nums[0..i] and `right_max[i]` = max subarray sum in nums[i..n-1]. But this doesn't directly help because removing x creates multiple segments.
6. Better approach: Use the idea that the answer is the max over all x of (max subarray sum in the array without x). We can iterate over each unique x, and for each x, the array is split into segments by the positions of x. The max subarray sum in the resulting array is the max of the max subarray sums of each segment. To compute this efficiently, we can precompute for each index i, the max subarray sum ending at i (from left) and starting at i (from right). Then for each x, we iterate through its positions and combine adjacent segments. However, this is still complex.
7. Alternative: Since the number of unique elements can be up to n, we need an O(n) or O(n log n) solution. We can use the following: 
   - Compute the global max subarray sum (no removal).
   - For each unique element x, the problem reduces to finding the max subarray sum in the array with x removed. We can precompute prefix and suffix arrays where `prefix[i]` is the max subarray sum in nums[0:i] and `suffix[i]` is the max subarray sum in nums[i:n]. But again, removing x creates multiple segments.
8. Insight: We can use a segment tree or a sweep-line approach. However, a simpler method: 
   - Precompute `max_ending_here` and `max_so_far` for the entire array.
   - For each unique x, we can compute the max subarray sum in the array without x by considering the segments between occurrences of x. We can precompute for each index, the max subarray sum that ends at that index (from the left) and starts at that index (from the right). Then for each x, we iterate through its positions and for each gap, the max subarray sum in that gap can be computed if we have precomputed information.
9. Actually, the most straightforward efficient method: 
   - Let `dp[i]` be the max subarray sum ending at index i.
   - Let `rev_dp[i]` be the max subarray sum starting at index i.
   - Let `prefix_max[i]` = max(dp[0], dp[1], ..., dp[i])
   - Let `suffix_max[i]` = max(rev_dp[i], rev_dp[i+1], ..., rev_dp[n-1])
   - For each unique x, the array without x has segments. The max subarray sum in the resulting array is the max of:
     - `prefix_max[first_occurrence_of_x - 1]` (if first_occurrence > 0)
     - For each consecutive pair of occurrences of x at indices i and j, the max subarray sum in nums[i+1:j-1] which is `prefix_max[j-1] - ...` but this doesn't work directly because prefix_max is global.
10. Correct approach: 
    - Precompute `left[i]` = max subarray sum in nums[0..i]
    - Precompute `right[i]` = max subarray sum in nums[i..n-1]
    - Also, for each index i, compute `max_ending_at[i]` and `max_starting_at[i]`.
    - For each unique x, let the positions be p1, p2, ..., pk.
    - The segments are: [0, p1-1], [p1+1, p2-1], ..., [pk+1, n-1].
    - For each segment [a, b], the max subarray sum can be found if we have a way to query. But we can precompute a sparse table or use the fact that we only need to check the segments defined by x.
    - Since the total number of segments across all x is O(n) (each element is in one segment for each x that doesn't appear there, but actually, the sum of the number of occurrences of all x is n, so the total number of segments is O(n)), we can afford to iterate.
    - For each segment [a, b], we need the max subarray sum. We can precompute this using a segment tree or by precomputing `max_subarray[a][b]` which is O(n^2) and too slow.
11. Final efficient approach:
    - Compute the global max subarray sum.
    - For each unique x, we want to compute the max subarray sum in the array without x.
    - We can use the following: 
      - Precompute `L[i]` = max subarray sum ending at i (from left)
      - Precompute `R[i]` = max subarray sum starting at i (from right)
      - Precompute `P[i]` = max(L[0], L[1], ..., L[i])
      - Precompute `S[i]` = max(R[i], R[i+1], ..., R[n-1])
    - For a segment [a, b], the max subarray sum is not directly P[b] because P[b] includes subarrays that start before a.
    - Instead, for each segment [a, b], the max subarray sum is the max of:
      - The max subarray sum entirely within [a, b].
    - We can use a different precomputation: 
      - Let `seg_max[i]` be the max subarray sum in nums[0..i] that ends at or before i and is entirely within some segment? No.
12. Actually, we can do this: 
    - For each unique x, iterate through its positions. The segments are defined by consecutive positions of x.
    - For each segment [l, r], we need the max subarray sum in nums[l..r].
    - We can precompute a 2D structure? No, O(n^2).
    - Instead, note that the total number of segments across all x is O(n) because each occurrence of x defines a boundary, and the sum of the number of occurrences of all x is n. So the total number of segments is at most n + number of unique elements, which is O(n).
    - For each segment [l, r], we can compute the max subarray sum in O(r-l+1) time. But the sum of (r-l+1) over all segments for a fixed x is O(n), and over all x, it is O(n * number of unique elements) which is O(n^2) in worst case.
13. We need a faster way. Use the following trick:
    - Precompute `max_ending_here[i]` and `max_so_far_prefix[i]` for the entire array.
    - Similarly, `max_starting_here[i]` and `max_so_far_suffix[i]`.
    - For a segment [l, r], the max subarray sum is:
        max( max_so_far_prefix[r] - (some adjustment), ... ) -> not straightforward.
14. Correct and efficient method:
    - We can use a segment tree that supports point updates. But we are not updating, we are removing.
    - Alternative: 
      - Compute the max subarray sum for the original array.
      - For each unique x, the answer is the max of the max subarray sums of the segments between occurrences of x.
      - We can precompute for each index i, the value `best[i]` which is the max subarray sum in the array nums[0..i] that does not include any occurrence of x? But x varies.
15. Given the constraints, the intended solution is likely:
    - Precompute prefix and suffix max subarray sums.
    - For each unique x, the segments are known. For each segment [l, r], the max subarray sum can be computed in O(1) if we have a sparse table for range max subarray sum queries. Building a sparse table for range max subarray sum is possible in O(n log n) and query in O(1).
    - Steps:
      a. Compute the global max subarray sum.
      b. Build a sparse table for range max subarray sum queries. This requires storing for each range [i, j]:
          - max_sub: the max subarray sum in [i, j]
          - prefix_max: the max prefix sum in [i, j]
          - suffix_max: the max suffix sum in [i, j]
          - total_sum: the sum of the range
      c. For each unique x, get its positions. The segments are [0, p1-1], [p1+1, p2-1], ..., [pk+1, n-1].
      d. For each segment [l, r] (if l <= r), query the sparse table for the max subarray sum in [l, r].
      e. Take the max over all segments and all x, and also the global max.
    - This is O(n log n) for building the sparse table and O(n) for processing all segments (since total number of segments is O(n)).