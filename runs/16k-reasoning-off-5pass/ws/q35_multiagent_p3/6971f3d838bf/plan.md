1. First, compute the maximum subarray sum of the original array using Kadane's algorithm. This covers the case where we perform no operations.
2. Identify all unique elements in the array. For each unique element x, removing all occurrences of x creates a new array. We need to find the max subarray sum in that new array efficiently.
3. Instead of simulating removal for each x (which would be O(n^2)), we can precompute prefix and suffix max subarray sums. Specifically, for each index i, compute the max subarray sum ending at or before i (from the left) and starting at or after i (from the right), but only considering segments that do not contain the removed element.
4. A better approach: For each unique value x, the array is split into segments separated by x. The max subarray sum in the resulting array is the max of: (a) the max subarray sum entirely within one segment, and (b) the sum of adjacent segments if they are positive (but since we remove x, segments are independent, so we just take the max subarray sum within any single segment).
5. To do this efficiently: Precompute for each position, the max subarray sum ending at that position (from left) and starting at that position (from right). Then, for each unique x, iterate through its positions. The segments are between consecutive occurrences of x. The max subarray sum in the segment between two occurrences (or start/end) can be derived from precomputed left and right arrays, but we must ensure the subarray doesn't cross the removed elements.
6. Actually, a more efficient method: Use the idea that after removing x, the array consists of contiguous blocks. For each block, the max subarray sum is independent. We can precompute a "left" array where left[i] is the max subarray sum ending at index i (using Kadane's from left), and a "right" array where right[i] is the max subarray sum starting at index i (using Kadane's from right). Then for each unique x, we consider all positions where x occurs. The gaps between these positions define segments. For each segment [l, r], the max subarray sum is the max of: max subarray sum entirely within [l, r]. This can be computed by taking the max of left[k] for k in [l, r] but only if the subarray ending at k is fully within [l, r]... This is complex.
7. Alternative efficient approach: For each unique x, the problem reduces to finding the max subarray sum in an array with some elements removed. We can use a segment tree or sparse table, but that's heavy. Instead, note that the number of unique elements can be up to n. But we can process each unique x by scanning the array and computing max subarray sum on the fly for the segments. However, worst-case O(n^2).
8. Better insight: Precompute prefix max subarray sums and suffix max subarray sums. Define:
   - `prefix_max[i]` = max subarray sum in nums[0..i]
   - `suffix_max[i]` = max subarray sum in nums[i..n-1]
   But this doesn't directly help for arbitrary removals.
9. Correct efficient approach: For each unique value x, we want to compute the max subarray sum of the array with all x's removed. We can do this by iterating through the array and maintaining a running Kadane's sum, skipping elements equal to x. But doing this for each unique x is O(n * unique_count) which can be O(n^2).
10. We need a smarter way. Notice that the answer is the maximum over:
    - The original max subarray sum (no removal)
    - For each unique x, the max subarray sum after removing x.
    
    We can precompute for each index i, the max subarray sum ending at i (call it `end_at[i]`) and starting at i (call it `start_at[i]`). Then, for a removal of x, the segments are defined by the positions of x. For a segment from l to r (exclusive of x's), the max subarray sum within that segment is not simply derived from `end_at` and `start_at` because those values might include elements outside the segment.
    
    Actually, we can use a different precomputation: For each index i, let `left_max[i]` be the maximum subarray sum in nums[0..i], and `right_max[i]` be the maximum subarray sum in nums[i..n-1]. These are standard prefix/suffix max subarray sums.
    
    Then, for each unique x, let the positions of x be p1, p2, ..., pk. The segments are [0, p1-1], [p1+1, p2-1], ..., [pk+1, n-1]. For each segment [a, b], the max subarray sum within that segment is:
    - If a > b, skip.
    - Otherwise, it is the max subarray sum in nums[a..b].
    
    To get the max subarray sum in nums[a..b] quickly, we can use a sparse table or segment tree for range max subarray sum queries. Build a segment tree that supports range max subarray sum queries in O(1) or O(log n) after O(n log n) build. Then for each unique x, iterate through its positions, identify segments, and query the segment tree for each segment. The total time would be O(n log n + U * k) where U is unique count and k is average occurrences. In worst case, this is still O(n^2).
    
    Given constraints n <= 10^5, O(n^2) is too slow. We need a better approach.
    
    Insight: The max subarray sum after removing x is the max of:
    - The max subarray sum of the original array that does not contain any occurrence of x.
    
    We can compute for each index i, the nearest occurrence of x to the left and right. But x varies.
    
    Alternative: Use the fact that we only remove one type of element. Precompute for each index i, the max subarray sum ending at i that does not include any "bad" element. But the bad element changes.
    
    Given the complexity, and since the number of unique elements might be large, but in practice, if an element appears many times, the number of segments is large but the segments are small. If an element appears few times, the number of segments is small.
    
    Worst-case: all elements are unique. Then removing any x leaves n-1 elements, and we need max subarray sum of that. But if all elements are unique, we have n unique elements, and for each, we remove one element. The resulting array is almost the same. We can compute the max subarray sum for the original array, and then for each single-element removal, the max subarray sum might change slightly. But computing it naively is O(n) per removal, leading to O(n^2).
    
    However, note that if all elements are positive, removing any element just reduces the total sum, so the max subarray sum is the total sum minus the removed element. But with negatives, it's complex.
    
    Given the time constraints, I'll implement the O(n^2) approach but optimize by only considering unique elements and using efficient Kadane's for each removal. For n=10^5, if there are many unique elements, this might TLE. But let's try to optimize:
    
    - If the number of unique elements is large, but each appears few times, we can still do it.
    - Precompute the list of positions for each unique element.
    - For each unique element x, create a list of segments (defined by positions of x).
    - For each segment, run Kadane's algorithm.
    - Track the global maximum.
    
    This is O(n * U) in worst-case, which is O(n^2). But in practice, if U is large, the segments are short. If U is small, the number of segments is small.
    
    Let's implement this.