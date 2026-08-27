
## ideation
The core difficulty is efficiently computing the maximum subarray sum after removing all occurrences of each unique element `x`. A naive approach of reconstructing the array and running Kadane's algorithm for each unique element would be $O(n \cdot U)$ where $U$ is the number of unique elements, which can be $O(n^2)$ in the worst case (e.g., all elements unique).

The key insight is that removing `x` splits the array into contiguous segments of non-`x` elements. The maximum subarray sum in the resulting array is the maximum of the maximum subarray sums within each of these segments.

To solve this efficiently:
1.  **Precompute Global Max Subarray Sum**: This covers the case of performing no operation.
2.  **Precompute `end_max` and `start_index`**:
    -   `end_max[i]`: The maximum subarray sum ending exactly at index `i`.
    -   `start_index[i]`: The starting index of the subarray that achieves `end_max[i]`.
3.  **Identify Segments**: For each unique element `x`, find all its indices. These indices define the boundaries of the segments. The segments are the ranges between consecutive occurrences of `x` (and the start/end of the array).
4.  **Query Max Subarray Sum in Segments**: For a segment `[l, r]`, we need $\max \{ \text{end\_max}[j] \mid l \le j \le r \text{ and } \text{start\_index}[j] \ge l \}$. This ensures the subarray ending at `j` is fully contained within `[l, r]`.
5.  **Efficient Query Processing**: Since there can be many segments, we process them offline. We can sort the segments by their left boundary `l` in descending order. We also sort the indices `j` by their `start_index[j]` in descending order. We iterate `l` from `n-1` down to `0`. As we decrease `l`, we add indices `j` into a data structure (like a Segment Tree or Fenwick Tree for Range Maximum Query) if `start_index[j] == l`. Then, for any segment starting at `l` (i.e., `[l, r]`), we query the data structure for the maximum value in the range `[l, r]`.

This approach ensures that each index is added to the data structure once and each segment is queried once, leading to an overall time complexity of $O(n \log n)$.

Pitfalls to avoid:
-   Handling empty segments (when `l > r`) correctly.
-   Ensuring the data structure supports range maximum queries.
-   Correctly initializing the `start_index` array (usually `start_index[i] = i` if `nums[i] > 0` or if it extends a previous positive sum, otherwise it might be `i` if `nums[i]` is the best start, but standard Kadane's logic applies: `start_index[i] = start_index[i-1]` if `end_max[i-1] > 0` else `i`).
-   The global maximum subarray sum must be considered as a candidate for the final answer.

## worker: <none>
The solution uses an offline processing technique with a segment tree to efficiently compute the maximum subarray sum after removing each unique element.

1.  **Precomputation**:
    -   `end_max[i]` and `start_index[i]` are computed using a modified Kadane's algorithm. `end_max[i]` stores the maximum subarray sum ending at index `i`, and `start_index[i]` stores the starting index of that subarray.
    -   The global maximum subarray sum (without any removal) is also computed.

2.  **Segment Identification**:
    -   For each unique element `x`, its occurrences split the array into contiguous segments of non-`x` elements. These segments are identified as ranges `[l, r]`.

3.  **Offline Query Processing**:
    -   The problem reduces to finding, for each segment `[l, r]`, the maximum value of `end_max[j]` for `j` in `[l, r]` such that `start_index[j] >= l`. This condition ensures the subarray ending at `j` is fully contained within `[l, r]`.
    -   We process segments by iterating `l` from `n-1` down to `0`.
    -   As we decrease `l`, we add indices `j` into a segment tree if `start_index[j] == l`. The segment tree stores `end_max[j]` at position `j`.
    -   For any segment `[l, r]` that starts at the current `l`, we query the segment tree for the maximum value in the range `[l, r]`.

4.  **Complexity**:
    -   Precomputation: $O(n)$.
    -   Segment tree operations: Each index is added once and each segment is queried once. With $O(\log n)$ per operation, the total time is $O(n \log n)$.
    -   Space complexity: $O(n)$ for arrays and the segment tree.

This approach efficiently handles the constraints and avoids the $O(n^2)$ worst-case of a naive solution.
