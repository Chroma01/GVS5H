
## ideation
The core difficulty is efficiently computing the maximum subarray sum for the array after removing all occurrences of each unique element `x`. A naive approach of physically removing elements and running Kadane's algorithm for each unique `x` would be O(n * u) where u is the number of unique elements, which can be up to O(n^2) in the worst case (e.g., all elements unique). This will TLE given n <= 10^5.

The key insight is that removing all occurrences of `x` breaks the array into several contiguous segments that do not contain `x`. The maximum subarray sum in the resulting array is simply the maximum of the maximum subarray sums within each of these segments.

To implement this efficiently:
1. Precompute the maximum subarray sum for the original array (case where no operation is performed).
2. For each unique value `x`, identify all indices where `x` occurs. These indices partition the array into segments.
3. For each segment, we need to quickly query the maximum subarray sum. Since the segments are static (they depend only on the positions of `x`), we can precompute a data structure that supports range maximum subarray sum queries.
4. A Segment Tree is suitable here. Each node in the segment tree will store:
   - `max_sub`: the maximum subarray sum in the range.
   - `prefix_max`: the maximum prefix sum in the range.
   - `suffix_max`: the maximum suffix sum in the range.
   - `total_sum`: the total sum of the range.
   This allows merging two nodes in O(1) time.
5. Build the segment tree in O(n) time.
6. For each unique `x`, get its positions, determine the segments, and query the segment tree for each segment. Take the maximum over all segments for this `x`, and update the global maximum.
7. The total time complexity will be O(n log n) for building the segment tree and O(u * log n) for queries, where u is the number of unique elements. In the worst case, u can be O(n), so total time is O(n log n), which is acceptable.

Pitfalls to avoid:
- Not handling the case where no operation is performed (original array max subarray sum).
- Incorrectly merging segment tree nodes (must correctly compute prefix, suffix, and max subarray from children).
- Forgetting that a segment might be empty (when two occurrences of `x` are adjacent), in which case the query should return a very small number (or be skipped).
- The segment tree should be built on the original array indices.

## worker: Implement a Segment Tree class that supports range
The solution uses a segment tree to efficiently query the maximum subarray sum in any range. The segment tree nodes store four values: the maximum subarray sum in the range, the maximum prefix sum, the maximum suffix sum, and the total sum of the range. This allows merging two nodes in O(1) time.

1. **Segment Tree Construction**: The tree is built in O(n) time. Each leaf represents a single element, and internal nodes are computed by merging their children.
2. **Query**: The query function returns the merged result for the range [l, r] in O(log n) time.
3. **Handling Removals**: For each unique value `x`, the positions of `x` partition the array into segments. The maximum subarray sum after removing `x` is the maximum of the max subarray sums of these segments.
4. **Original Array**: The case where no operation is performed is covered by querying the entire array initially.
5. **Complexity**: Building the segment tree takes O(n). For each unique value `x`, if it occurs `k` times, we do `k+1` queries, each taking O(log n). Summing over all unique values, the total number of queries is O(n) (since each index is part of exactly one segment for each removal, but actually, the sum of occurrences of all unique values is n, so the total number of segments across all removals is O(n)). Thus, the total time complexity is O(n log n), which is efficient for n <= 10^5.
