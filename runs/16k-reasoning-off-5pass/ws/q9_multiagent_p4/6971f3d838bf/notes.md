
## ideation
**Core Difficulty**: The problem asks for the maximum subarray sum after removing *all* occurrences of a specific value $x$. A naive approach of simulating the removal for every unique $x$ and running Kadane's algorithm would be $O(N^2)$ in the worst case (e.g., all elements are unique), which exceeds the time limit for $N=10^5$. The key challenge is to efficiently calculate the new maximum subarray sum without re-scanning the array for each candidate $x$.

**Candidate Approaches**:
1.  **Prefix/Suffix Arrays (Optimal)**:
    *   Precompute two arrays: `prefix_max[i]` storing the maximum subarray sum in `nums[0...i]` and `suffix_max[i]` storing the maximum subarray sum in `nums[i...n-1]`.
    *   For each unique number $x$, find the range of indices `[first_occurrence, last_occurrence]`.
    *   The resulting array consists of `nums[0...first-1]`, `nums[last+1...n-1]`, and potentially a combination where the subarray crosses the gap.
    *   Calculate the max sum as: `max(prefix_max[first-1], suffix_max[last+1], max_suffix_of_prefix_part + max_prefix_of_suffix_part)`. Note: If the prefix part is empty or suffix part is empty, handle edge cases.
    *   This approach is $O(N)$ time and $O(N)$ space.

2.  **Dynamic Programming with State**:
    *   Try to maintain DP states that account for "removing current element if it equals $x$". This is tricky because $x$ is chosen globally at the start, not element-by-element. This approach is likely more complex and less intuitive than the prefix/suffix method.

## worker: Implement the Prefix/Suffix array solution. Specif
1.  **Prefix/Suffix Arrays**: I computed four arrays:
    *   `prefix_max_subarray[i]`: Maximum subarray sum in `nums[0...i]`.
    *   `prefix_max_ending_here[i]`: Maximum subarray sum ending exactly at index `i`.
    *   `suffix_max_subarray[i]`: Maximum subarray sum in `nums[i...n-1]`.
    *   `suffix_max_ending_here[i]`: Maximum subarray sum starting exactly at index `i`.
2.  **Auxiliary Arrays**: To efficiently calculate the "crossing" case (max suffix of left part + max prefix of right part), I added:
    *   `max_suffix_prefix[i]`: The maximum value in `suffix_max_ending_here[0...i]`. This gives the max suffix sum for any prefix ending at `i`.
    *   `max_prefix_suffix[i]`: The maximum value in `prefix_max_ending_here[i...n-1]`. This gives the max prefix sum for any suffix starting at `i`.
3.  **Iteration**: I iterate through each unique element `x`. For each `x`, I find its first and last occurrence. The removal splits the array into `[0, first-1]` and `[last+1, n-1]`. The new max subarray sum is the maximum of:
    *   Best subarray in the left part.
    *   Best subarray in the right part.
    *   Best suffix of left part + Best prefix of right part.
4.  **Complexity**:
    *   Time: $O(N)$ for precomputing arrays and $O(N)$ for iterating unique elements (since there are at most $N$ unique elements). Total $O(N)$.
    *   Space: $O(N)$ for storing the arrays.
5.  **Edge Cases**: Handled empty ranges (e.g., if `first == 0`, left part is empty) by initializing candidates to `-inf`.

## worker: Verify the solution logic against the provided exa
The previous solution failed to handle cases where the removed element `x` appears multiple times, leaving a "middle" segment between the first and last occurrence. The new solution uses a Segment Tree to efficiently query the maximum subarray sum, prefix sum, suffix sum, and total sum for any range in $O(\log N)$.
1.  **Segment Tree**: Each node stores `max_sub`, `max_pref`, `max_suff`, and `total`. Merging two nodes combines these values correctly.
2.  **Querying**: For each unique `x`, we identify the ranges `L` (before first `x`), `M` (between first and last `x`), and `R` (after last `x`). We query the segment tree for these ranges.
3.  **Combining**: The resulting array is `L + M + R`. We merge the nodes for `L`, `M`, and `R` sequentially to get the max subarray sum of the combined array.
4.  **Complexity**: Building the tree is $O(N)$. Iterating over unique elements is $O(N)$ (at most $N$ unique elements). Each query is $O(\log N)$. Total time complexity is $O(N \log N)$, which fits within the limits. Space complexity is $O(N)$.

## worker: [todo] Check constraints and potential integer ove
The solution implements an $O(N)$ approach using precomputed prefix and suffix arrays.
1.  **Prefix Arrays**: `prefix_max_subarray` stores the maximum subarray sum in `nums[0...i]`, and `prefix_max_ending_here` stores the maximum subarray sum ending exactly at `i`.
2.  **Suffix Arrays**: `suffix_max_subarray` stores the maximum subarray sum in `nums[i...n-1]`, and `suffix_max_ending_here` stores the maximum subarray sum starting exactly at `i`.
3.  **Auxiliary Arrays**:
    *   `max_suffix_prefix[i]`: The maximum value in `suffix_max_ending_here[0...i]`. This allows $O(1)$ retrieval of the max suffix sum for any prefix ending at `i`.
    *   `max_prefix_suffix[i]`: The maximum value in `prefix_max_ending_here[i...n-1]`. This allows $O(1)$ retrieval of the max prefix sum for any suffix starting at `i`.
4.  **Iteration**: For each unique element $x$, we find its first and last occurrence. Removing $x$ splits the array into a left part (`0` to `first-1`) and a right part (`last+1` to `n-1`). The new maximum subarray sum is the maximum of:
    *   The best subarray entirely in the left part.
    *   The best subarray entirely in the right part.
    *   The sum of the best suffix of the left part and the best prefix of the right part (crossing the gap).
5.  **Edge Cases**: The code handles cases where the left or right parts are empty by initializing candidates to negative infinity. Python handles large integers automatically, so overflow is not an issue.

## worker: Refactor the solution to use the Segment Tree appr
Refactored the solution to use a Segment Tree approach as identified in the worker notes. The previous prefix/suffix logic failed to correctly handle the "middle" segment between the first and last occurrence of the removed element $x$. 

The new approach:
1.  **Segment Tree Construction**: Builds a tree where each node stores `max_sub` (maximum subarray sum), `max_pref` (maximum prefix sum), `max_suff` (maximum suffix sum), and `total` (sum of the range). This allows efficient merging of arbitrary ranges.
2.  **Querying**: For each unique element $x$, the code identifies the ranges:
    *   Left: `[0, first-1]`
    *   Middle: `[first+1, last-1]` (elements strictly between the first and last occurrence)
    *   Right: `[last+1, n-1]`
3.  **Combination**: It queries the segment tree for these ranges and merges them sequentially (`Left -> Middle -> Right`). The merge logic correctly computes the new `max_sub` by considering subarrays entirely in the left, entirely in the right, or crossing the boundaries (e.g., `left.suff + mid.pref`, `mid.suff + right.pref`, etc.).
4.  **Complexity**: Building the tree is $O(N)$. Iterating over unique elements is $O(N)$ (at most $N$ unique elements). Each query and merge is $O(\log N)$. Total time complexity is $O(N \log N)$, which fits within the limits for $N=10^5$. Space complexity is $O(N)$.

## worker: finalize
The solution implements a Segment Tree approach to efficiently handle the problem constraints ($N \le 10^5$).
1.  **Segment Tree Construction**: Each node in the tree stores four values: `max_sub` (maximum subarray sum within the range), `max_pref` (maximum prefix sum), `max_suff` (maximum suffix sum), and `total` (sum of all elements in the range). This allows merging two adjacent ranges in $O(1)$ time to compute the properties of the combined range.
2.  **Handling Removal**: For each unique element $x$ in the array, we identify its first and last occurrence indices. Removing all occurrences of $x$ splits the array into three potential segments:
    *   Left segment: indices before the first occurrence.
    *   Middle segment: indices strictly between the first and last occurrence.
    *   Right segment: indices after the last occurrence.
3.  **Querying and Merging**: We query the segment tree for these three segments. If a segment is empty, it is skipped. The remaining segments are merged sequentially (Left -> Middle -> Right) using the `merge` function to compute the maximum subarray sum of the resulting array.
4.  **Complexity**:
    *   Building the tree takes $O(N)$.
    *   Iterating through unique elements takes $O(N)$ (at most $N$ unique elements).
    *   Each query and merge operation takes $O(\log N)$.
    *   Total time complexity is $O(N \log N)$, which fits well within the time limits.
    *   Space complexity is $O(N)$ for the tree and auxiliary arrays.
5.  **Edge Cases**: The code handles cases where the left, middle, or right segments are empty by checking bounds before querying and initializing `current_node` appropriately. The initial answer is set to the max subarray sum of the original array (representing the case where no operation is performed or the operation doesn't improve the result).
