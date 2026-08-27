
## ideation
The core difficulty lies in efficiently computing the maximum subarray sum after removing all occurrences of each unique element `x`. A naive approach of simulating the removal and running Kadane's algorithm for each unique element would result in O(n * U) time complexity, where U is the number of unique elements. In the worst case (all elements are unique), this becomes O(n²), which is too slow for n = 10⁵.

However, we can optimize by observing that:
1. The answer is the maximum of:
   a. The max subarray sum of the original array (no removal).
   b. For each unique element `x`, the max subarray sum of the array with all `x`'s removed.

2. When removing `x`, the array is split into contiguous segments separated by `x`. The max subarray sum in the resulting array is simply the maximum of the max subarray sums of these individual segments.

3. To avoid O(n) per unique element, we can precompute the positions of each unique element. Then, for each unique element `x`, we iterate through its positions to define the segments. For each segment, we run Kadane's algorithm. 

4. The total work across all unique elements is proportional to the sum of the lengths of all segments for all unique elements. Note that each element in the array is part of a segment for a unique element `x` only if that element is not `x`. But when we process `x`, we skip all occurrences of `x`. The key insight is that the total number of elements processed in Kadane's across all unique elements is bounded by O(n * U) in the worst case, but in practice, if an element appears frequently, the segments are short, and if it appears rarely, the number of segments is small.

5. However, worst-case O(n²) is still a concern. But note: if an element appears k times, then we have k+1 segments. The total length of all segments for this element is n - k. So the work for element `x` is O(n). Summed over all unique elements, it is O(n * U). Since U can be up to n, worst-case is O(n²).

6. Given the constraints and typical test cases, this approach might pass if the constant factor is small. But we can try to optimize further by noticing that if the number of unique elements is large, many elements appear only once. For an element that appears once, removing it splits the array into two segments. We can precompute prefix and suffix max subarray sums to answer the max subarray sum in a range [l, r] quickly? Actually, no standard precomputation allows O(1) range max subarray sum queries without a segment tree.

7. Alternative: Use a segment tree that supports range max subarray sum queries. Build a segment tree in O(n). Then for each unique element `x`, for each segment defined by consecutive occurrences of `x`, query the segment tree for the max subarray sum in that segment. The total queries would be sum_{x} (count(x) + 1). The sum of count(x) over all x is n, so total queries is n + U. Each query is O(log n). Total time: O(n log n + U log n) = O(n log n). This is efficient.

8. Implementation of segment tree for range max subarray sum:
   - Each node stores: max_prefix, max_suffix, max_subarray, total_sum.
   - Merge two nodes: 
        total_sum = left.total + right.total
        max_prefix = max(left.max_prefix, left.total + right.max_prefix)
        max_suffix = max(right.max_suffix, right.total + left.max_suffix)
        max_subarray = max(left.max_subarray, right.max_subarray, left.max_suffix + right.max_prefix)

9. Steps:
   a. Build a segment tree over the array for range max subarray sum queries.
   b. Compute the max subarray sum of the entire array (from the root of the segment tree) as the initial answer.
   c. Group indices by value: pos_map = {value: [list of indices]}.
   d. For each unique value x in pos_map:
        - Get the sorted list of positions: p = pos_map[x]
        - The segments are: [0, p[0]-1], [p[0]+1, p[1]-1], ..., [p[-1]+1, n-1]
        - For each segment [l, r] (if l <= r), query the segment tree for max subarray sum in [l, r] and update the global answer.
   e. Return the global answer.

10. Edge case: If after removal the array is empty, skip (but the problem states nums remains non-empty, and we only remove if non-empty remains; but our segment queries will naturally handle empty segments by skipping).

This approach runs in O(n log n) time and O(n) space, which is efficient.

## worker: Implement a segment tree that supports range max s
The solution uses a segment tree to efficiently compute range maximum subarray sum queries. The segment tree is built in O(n) time, and each query takes O(log n) time. 

1. **Segment Tree Construction**: Each node in the segment tree stores four values:
   - `max_prefix`: Maximum prefix sum in the range.
   - `max_suffix`: Maximum suffix sum in the range.
   - `max_subarray`: Maximum subarray sum in the range.
   - `total_sum`: Total sum of all elements in the range.
   
   The merge operation combines two nodes by computing these values based on the left and right children.

2. **Query Function**: The query function retrieves the max subarray sum for a given range [l, r] by combining the relevant nodes from the segment tree.

3. **Processing Unique Elements**: For each unique element `x`, the array is split into segments separated by occurrences of `x`. The max subarray sum for each segment is queried from the segment tree, and the global maximum is updated.

4. **Complexity**: 
   - Building the segment tree: O(n)
   - Number of queries: O(n + U) where U is the number of unique elements (since each element's positions define segments, and the total number of segments across all unique elements is O(n + U)).
   - Each query: O(log n)
   - Total time: O(n log n)
   - Space: O(n) for the segment tree.

This approach efficiently handles the constraints and avoids the O(n²) worst-case of a naive solution.
