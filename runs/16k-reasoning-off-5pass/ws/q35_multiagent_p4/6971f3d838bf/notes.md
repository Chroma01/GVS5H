
## ideation
The core difficulty is efficiently computing the maximum subarray sum for the array after removing all occurrences of each unique element $x$, without physically reconstructing the array for each $x$ (which would be too slow).

Key insights:
1.  **Global Max**: The answer is at least the max subarray sum of the original array (case: no removal).
2.  **Segments**: Removing all occurrences of $x$ splits the array into independent segments. The max subarray sum in the resulting array is the maximum of the max subarray sums of these individual segments.
3.  **Total Segments**: The total number of segments across all unique elements is $O(N)$. Specifically, if an element $x$ appears $k$ times, it creates $k+1$ segments. The sum of $k$ over all unique elements is $N$. Thus, the total number of segments is $N + (\text{number of unique elements}) \le 2N$.
4.  **Efficient Querying**: To compute the max subarray sum of a segment $[l, r]$ in $O(1)$ time, we can use a **Sparse Table** (or Segment Tree) that supports Range Maximum Subarray Sum queries. A standard sparse table can be built for this "max subarray sum" problem by storing four values for each range:
    *   `total_sum`: Sum of all elements in the range.
    *   `max_prefix`: Maximum prefix sum in the range.
    *   `max_suffix`: Maximum suffix sum in the range.
    *   `max_sub`: Maximum subarray sum in the range.
    These can be merged in $O(1)$ time. Building the sparse table takes $O(N \log N)$ time.
5.  **Algorithm**:
    *   Compute the global max subarray sum (Kadane's).
    *   Build the Sparse Table for range max subarray sum queries.
    *   Group indices by value to quickly get positions of each unique element.
    *   For each unique element $x$, get its sorted positions. Define the segments as the ranges between consecutive positions (and before the first/after the last).
    *   For each valid segment $[l, r]$, query the sparse table for the max subarray sum.
    *   Track the global maximum.

Pitfalls:
*   Handling edge cases where segments are empty (e.g., if $x$ is at index 0, the first segment is empty).
*   Ensuring the sparse table merge logic is correct (especially for `max_prefix` and `max_suffix` which depend on the left child's total sum).
*   The constraints allow negative numbers, so initial max values should be set to negative infinity.

## worker: Implement a function to build a sparse table for r
The solution uses a Sparse Table to efficiently answer Range Maximum Subarray Sum queries. 
1. **Global Max**: We first compute the maximum subarray sum of the original array using Kadane's algorithm. This covers the case where no element is removed.
2. **Sparse Table Construction**: We build a sparse table where each entry `st[k][i]` represents the range `[i, i + 2^k - 1]`. Each entry stores a tuple `(total_sum, max_prefix, max_suffix, max_sub)`. The merge operation combines two adjacent ranges by considering:
   - `total_sum`: Sum of both ranges.
   - `max_prefix`: Either the max prefix of the left range, or the entire left range plus the max prefix of the right range.
   - `max_suffix`: Either the max suffix of the right range, or the entire right range plus the max suffix of the left range.
   - `max_sub`: The maximum of the max subarray of the left range, the max subarray of the right range, or a subarray crossing the boundary (max suffix of left + max prefix of right).
3. **Querying**: For any range `[l, r]`, we decompose it into two overlapping ranges from the sparse table (of lengths $2^k$ and $2^j$ such that $2^k + 2^j \ge r-l+1$ and they cover the range). We merge these two nodes to get the result.
4. **Processing Removals**: We group indices by value. For each unique value $x$, we get its positions. Removing $x$ splits the array into segments between consecutive occurrences of $x$. We query the sparse table for each segment and update the global maximum.
5. **Complexity**: Building the sparse table takes $O(N \log N)$ time and space. Querying takes $O(1)$ time. The total number of segments across all unique elements is $O(N)$, so the total time complexity is $O(N \log N)$. This fits within the constraints.
