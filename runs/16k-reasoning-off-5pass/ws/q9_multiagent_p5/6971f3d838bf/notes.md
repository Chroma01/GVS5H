
## ideation
**Core Difficulty**: The constraint $N \le 10^5$ prohibits an $O(N^2)$ solution where we simulate removing each unique element and run Kadane's algorithm. We need an approach that allows us to evaluate the effect of removing a specific value $x$ in $O(1)$ or $O(\log N)$ time after some preprocessing.

**Candidate Approaches**:
1.  **Prefix/Suffix Arrays (Optimal)**:
    *   Precompute `max_subarray[i]`: Maximum subarray sum in `nums[0...i]`.
    *   Precompute `max_subarray_suffix[i]`: Maximum subarray sum in `nums[i...n-1]`.
    *   Precompute `prefix_sum[i]` and `suffix_sum[i]` to handle cases where the optimal subarray is formed by joining a prefix ending before $x$'s last occurrence and a suffix starting after $x$'s first occurrence.
    *   For each unique $x$, find its first and last indices. The new max subarray sum is the maximum of:
        *   `max_subarray[last_idx - 1]` (if valid)
        *   `max_subarray_suffix[first_idx + 1]` (if valid)
        *   `prefix_sum[last_idx - 1] + max_subarray_suffix[first_idx + 1]` (if both sides exist and we choose to connect them, though strictly speaking, the "join" logic is slightly more complex because we just need the max of the left part, right part, or left+right. Actually, since we remove *all* occurrences, the array splits into two independent parts. The max subarray is simply `max(left_max, right_max)` unless the original array had a negative sum everywhere and we are forced to pick something? No, the problem says "non-empty". So if one side is empty, we take the other. If both exist, we take `max(left_max, right_max)`. Wait, is it possible the optimal is the sum of the whole remaining array? Yes, if all numbers are positive. But Kadane's covers that. The key is that the remaining array is just `nums[0...first-1]` + `nums[last+1...n-1]`. The max subarray is either entirely in the left part, entirely in the right part, or... wait, can it span across the gap? No, because the gap is removed. So it's strictly `max(max_subarray(left), max_subarray(right))`.
        *   Correction: The remaining array is contiguous in the original indices except for the removed block. The subarray cannot cross the removed block. So yes, it is `max(max_subarray(left_part), max_subarray(right_part))`.
    *   We also need to consider the case where we don't remove anything (original max subarray).
    *   Edge case: If removing $x$ leaves an empty array, skip that $x$.

2.  **Segment Tree**:
    *   Build a segment tree where each node stores: `max_sub`, `max_prefix`, `max_suffix`, `total_sum`.
    *   To remove $x$, we would need to update the tree by setting all leaves corresponding to $x$ to $-\infty$ (or effectively removing them). However, updating all occurrences of $x$ takes $O(K \log N)$ where $K$ is the count of $x$. Summing over all unique $x$ could still be $O(N \log N)$ in worst case (if all elements are unique). This is feasible but more complex to implement than the prefix/suffix array approach.

3.  **Two Passes with Tracking**:
    *   Similar to approach 1, but maybe optimize space? No, $O(N)$ space is fine.

## worker: Implement the solution using the Prefix/Suffix max
The solution uses a prefix/suffix array approach to achieve $O(N)$ time complexity.
1.  **Precomputation**:
    *   `pre_max[i]` stores the maximum subarray sum in the prefix `nums[0...i]`.
    *   `suf_max[i]` stores the maximum subarray sum in the suffix `nums[i...n-1]`.
    *   These arrays are built in $O(N)$ using a modified Kadane's algorithm.
2.  **Tracking Occurrences**:
    *   We store the first and last index of each unique number in hash maps (`first_occ`, `last_occ`).
3.  **Evaluation**:
    *   For each unique number $x$, we determine the indices of its first and last occurrence.
    *   Removing $x$ splits the array into a left part (indices $0$ to $first-1$) and a right part (indices $last+1$ to $n-1$).
    *   The maximum subarray sum of the resulting array is the maximum of the max subarray sums of the left and right parts (if they exist).
    *   We update the global answer with this value.
4.  **Edge Cases**:
    *   If removing $x$ leaves an empty array (only possible if $n=1$), we skip that $x$.
    *   If one side is empty, we only consider the other side.
    *   The initial answer is set to the max subarray sum of the original array (case where no operation is performed).

This approach ensures we evaluate every possible removal in $O(1)$ time after $O(N)$ preprocessing, satisfying the constraints.
