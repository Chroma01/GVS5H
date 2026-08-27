1. First, compute the maximum subarray sum of the original array using Kadane's algorithm. This covers the case where we perform no operation.
2. Identify all unique elements in the array. For each unique element x, we need to compute the maximum subarray sum of the array after removing all occurrences of x.
3. To efficiently compute the max subarray sum after removal, we can precompute prefix and suffix max subarray sums. Specifically, for each index i, compute the max subarray sum ending at or before i (prefix) and starting at or after i (suffix).
4. When removing x, the array is split into segments that do not contain x. The max subarray sum in the resulting array is the maximum of:
   - The max subarray sum entirely within any contiguous segment of non-x elements.
   - We can use the precomputed prefix and suffix arrays: for each occurrence of x at index i, the gap between previous x and current x (or start) and current x and next x (or end) forms a segment. The max subarray sum in that segment can be derived from prefix/suffix values.
5. Actually, a simpler approach: precompute for each index i, the max subarray sum in nums[0..i] (call it left_max[i]) and in nums[i..n-1] (call it right_max[i]). Also, compute the max subarray sum ending at i (ending_here[i]) and starting at i (starting_here[i]).
6. For each unique x, iterate through the positions where x occurs. The array is broken into segments. For each segment [l, r] (inclusive, where no x exists), the max subarray sum within that segment is max(ending_here[k] for k in [l,r] if the subarray ending at k is within [l,r]) which is complex.
7. Alternative efficient approach: Use the idea that removing x means we skip all x's. We can compute for each index, the max subarray sum that does not include any x. But doing this for each x is O(n * unique) which is too slow.
8. Better approach: Precompute global prefix max subarray sums and suffix max subarray sums. Also, for each value x, we can store the indices where it occurs. Then, for each x, the segments are defined by consecutive occurrences. For a segment from index a to b (exclusive of x's), the max subarray sum within that segment can be computed if we have precomputed for each index the max subarray sum in ranges. 
9. Actually, we can use a segment tree or sparse table for range max queries on the "max subarray sum" but that's complex.
10. Simpler insight: The max subarray sum after removing x is the maximum over all contiguous segments of non-x elements of the max subarray sum within that segment. We can precompute for each index i, the max subarray sum ending at i (let's call it `end_max[i]`) and the max subarray sum starting at i (`start_max[i]`). Also, let `global_prefix_max[i]` be the max subarray sum in nums[0..i] and `global_suffix_max[i]` be the max subarray sum in nums[i..n-1].
11. For a segment [l, r] (no x in between), the max subarray sum within it is not directly available. Instead, we can iterate through each unique x, and for each gap between consecutive x's (or boundaries), we need the max subarray sum in that gap. 
12. To avoid O(n * unique), note that the total number of gaps across all x is O(n + unique). But computing max subarray sum for each gap naively is O(n) per gap, leading to O(n^2).
13. We can precompute for each index i, the max subarray sum in the range [0, i] that ends at or before i and doesn't cross any "barrier". But barriers depend on x.
14. Final efficient approach: 
    - Compute `left[i]` = max subarray sum in nums[0..i]
    - Compute `right[i]` = max subarray sum in nums[i..n-1]
    - Compute `end_max[i]` = max subarray sum ending at index i
    - Compute `start_max[i]` = max subarray sum starting at index i
    - For each unique x, get all indices where x occurs: idx_1, idx_2, ..., idx_k.
    - The segments are: [0, idx_1-1], [idx_1+1, idx_2-1], ..., [idx_k+1, n-1].
    - For each segment [l, r], if l > r, skip. Otherwise, we need the max subarray sum within nums[l..r].
    - To get this quickly, we can precompute a 2D structure? No.
    - Instead, note that the max subarray sum in [l, r] is max( end_max[j] for j in [l, r] such that the subarray ending at j starts >= l ). This is equivalent to: max( end_max[j] - prefix_sum[start-1] ) which is hard.
15. Alternative: Use the fact that for a segment [l, r], the max subarray sum is max(0, max_{j=l}^{r} (end_max[j] - min_{k=l-1}^{j-1} prefix_sum[k]) ) if we use prefix sums. But this is still complex per segment.
16. Given constraints, the number of unique elements can be up to n. But the total number of segments across all x is sum_{x} (count(x) + 1) = n + unique. If we can compute the max subarray sum for a segment in O(1) or O(log n), we are good.
17. We can precompute a sparse table for range maximum query on an array that represents the "contribution" but it's not straightforward.
18. Practical approach: Since n is 10^5, and the sum of counts is n, we can afford O(n log n) or O(n). 
19. Let's precompute `prefix_max[i]` = max subarray sum in nums[0..i] and `suffix_max[i]` = max subarray sum in nums[i..n-1]. Also, let `max_ending_at[i]` be the max subarray sum ending at i, and `max_starting_at[i]` be the max subarray sum starting at i.
20. For a segment [l, r], the max subarray sum within it is: max( max_ending_at[j] for j in [l, r] where the subarray ending at j is within [l, r] ). The subarray ending at j is within [l, r] if the start of that subarray is >= l. The start can be found by tracking the start index of the max subarray ending at j. Let `start_index[j]` be the starting index of the max subarray ending at j. Then for j in [l, r], if `start_index[j] >= l`, then `max_ending_at[j]` is a candidate.
21. So for each segment [l, r], we need max{ max_ending_at[j] : j in [l, r] and start_index[j] >= l }.
22. This can be solved by processing segments for a fixed x. For each x, we have segments. For each segment, we want the max of max_ending_at[j] for j in [l, r] with start_index[j] >= l.
23. We can use a segment tree or a Fenwick tree? Or since we process each x independently, and the total length of all segments for all x is O(n), we can do a sweep.
24. Actually, for a fixed x, the segments are disjoint in terms of the original indices. We can iterate through each segment [l, r] and do a linear scan? That would be O(n) per x, leading to O(n * unique) worst-case.
25. Given the constraints and typical test cases, the number of unique elements might be large but the sum of segment lengths is n. However, scanning each segment is O(length) and total over all segments for one x is O(n). Summed over all x, it's O(n * unique) which is O(n^2) worst-case.
26. We need a better way. Let's use a different precomputation: 
    - Let `dp[i]` = max subarray sum in nums[0..i]
    - Let `rev_dp[i]` = max subarray sum in nums[i..n-1]
    - For each x, the answer after removal is the max of:
        a. The max subarray sum in any segment between x's.
        b. We can combine prefix and suffix: for each occurrence of x at index i, the max subarray sum that crosses the gap before i and after i is not possible since x is removed. So it's just the max within each contiguous non-x segment.
27. Insight: The max subarray sum in the array after removing x is the maximum over all i of: 
    - If we consider the array without x, it's a concatenation of segments. The max subarray sum is the max of the max subarray sums of each segment.
28. To compute the max subarray sum of a segment [l, r] quickly, we can precompute a sparse table for the `max_ending_at` array but with the constraint on start index. This is difficult.
29. Given time, I'll implement a solution that:
    - Computes the global max subarray sum (no removal).
    - For each unique x, computes the max subarray sum after removal by iterating through segments and using a precomputed structure. 
    - To make it efficient, precompute for each index i, the value `max_ending_at[i]` and `start_index[i]`.
    - Then for each segment [l, r] for a given x, we want max{ max_ending_at[j] for j in [l, r] with start_index[j] >= l }.
    - We can process all segments for all x by sorting segments by l and using a Fenwick tree or segment tree on the `max_ending_at` values, keyed by j, but filtered by start_index[j] >= l.
    - This is complex. 
30. Simpler: Since the constraints are 10^5, and in Python, we might get away with an O(n) per unique element if the number of unique elements is small. But worst-case, all elements are unique, so n unique elements, each with one occurrence, leading to n segments of length 0 or 1. Then it's O(n). 
    - Actually, if all elements are unique, then for each x, there is one occurrence, so two segments: [0, i-1] and [i+1, n-1]. The max subarray sum in [0, i-1] is `prefix_max[i-1]` (if i>0) and in [i+1, n-1] is `suffix_max[i+1]` (if i<n-1). So for each x, the answer is max(prefix_max[i-1], suffix_max[i+1]) (with appropriate bounds). And we take the max over all x and also the global max.
    - This works for unique elements. For duplicates, we have more segments.
31. Generalizing: For a given x, with indices idx_1, idx_2, ..., idx_k, the segments are [0, idx_1-1], [idx_1+1, idx_2-1], ..., [idx_k+1, n-1].
    - For a segment [l, r], if l > r, skip.
    - If l == r, the max subarray sum is nums[l] (if we consider non-empty, and the segment has one element).
    - Otherwise, we need the max subarray sum in nums[l..r].
    - We can precompute a 2D RMQ? No.
    - Instead, we can precompute `global_max_in_range[l][r]`? O(n^2) space.
32. Given the complexity, I'll use the following approach which is O(n) per unique element but hope that in practice it's fast enough, or optimize by noting that the total work is sum_{x} (number of segments for x) * (average segment length) which is not bounded well.
33. Actually, a known solution for this problem uses the following:
    - Precompute `left[i]` = max subarray sum in nums[0..i]
    - Precompute `right[i]` = max subarray sum in nums[i..n-1]
    - Precompute `end_max[i]` = max subarray sum ending at i
    - Precompute `start_max[i]` = max subarray sum starting at i
    - For each unique x, let indices be p_1, p_2, ..., p_k.
    - The answer for removing x is the maximum of:
        - For each gap between p_i and p_{i+1} (i.e., from p_i+1 to p_{i+1}-1), the max subarray sum in that gap.
        - The gap from 0 to p_1-1 and from p_k+1 to n-1.
    - To get the max subarray sum in a gap [l, r] quickly, we can use the following: 
        max_subarray_in_gap = max( end_max[j] for j in [l, r] if the subarray ending at j starts >= l )
    - We can precompute for each j, the value `end_max[j]` and `start_index[j]`.
    - Then for a gap [l, r], we want max{ end_max[j] : j in [l, r] and start_index[j] >= l }.
    - We can process all gaps for all x by creating a list of queries: for each gap [l, r], query max end_max[j] for j in [l, r] with start_index[j] >= l.
    - This is a 2D range query. We can offline process by sorting gaps by l descending, and using a Fenwick tree on the indices j, storing end_max[j], and only adding j when l <= start_index[j]. 
    - Steps:
        a. Collect all gaps from all x. Each gap is (l, r).
        b. Sort gaps by l in descending order.
        c. Also, sort indices j by start_index[j] in descending order.
        d. Iterate l from n-1 down to 0. For each j with start_index[j] == l, add end_max[j] to a Fenwick tree at position j.
        e. For each gap [l, r] with this l, query the Fenwick tree for max in [l, r].
    - This is O(n log n).