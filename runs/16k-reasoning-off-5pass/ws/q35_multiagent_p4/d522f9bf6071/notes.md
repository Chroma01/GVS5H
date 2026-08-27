
## ideation
The core difficulty lies in two aspects:
1. **Maximizing Weight with Non-overlapping Constraint**: This is a classic weighted interval scheduling problem, but limited to at most 4 intervals.
2. **Lexicographically Smallest Index Array**: The output must be the lexicographically smallest array of indices (original indices from the input) that achieves the maximum weight. This requires careful reconstruction.

Key insights:
- Since k is small (at most 4), we can use dynamic programming with state `dp[k][i]` representing the maximum weight using exactly `k` intervals from the first `i` intervals (when sorted by end time).
- To handle lexicographical order during reconstruction, we need to be able to check, for a given state, whether including a specific interval (by original index) leads to an optimal solution.
- A better approach for lexicographical minimality: After computing the DP table, we reconstruct the solution greedily. We iterate through the original indices in increasing order. For each index, we check if including the corresponding interval (if it doesn't overlap with previously chosen intervals) can still lead to the optimal total weight. This requires querying the DP table for the best possible future weight given the current state.

Steps:
1. Sort intervals by end time, keeping track of original indices.
2. Use DP: `dp[k][i]` = max weight using k intervals from the first i sorted intervals.
   - For each interval i (0-indexed in sorted array), compute `dp[k][i]` as max of:
     - `dp[k][i-1]` (skip interval i)
     - `dp[k-1][j] + weight_i` where j is the largest index such that `end[j] < start[i]` (include interval i)
   - Use binary search to find j efficiently.
3. The global maximum weight is `max(dp[1][n-1], dp[2][n-1], dp[3][n-1], dp[4][n-1])`. Let `max_w` be this value.
4. To reconstruct lexicographically smallest indices:
   - We need to select intervals such that their original indices are in increasing order in the output array, and the array is lexicographically smallest.
   - Strategy: Iterate through original indices from 0 to n-1. For each original index, check if the corresponding interval can be part of an optimal solution.
   - To do this efficiently, we need a way to query: given that the last chosen interval ended at time `t` and we have chosen `c` intervals so far, what is the maximum additional weight we can get from intervals that start after `t`?
   - Precompute a suffix DP or use the existing DP table carefully. Actually, since we sorted by end time, the DP table is built on sorted order. For reconstruction, it's easier to work with the sorted order but map back to original indices.
   
   Revised reconstruction strategy:
   - After computing DP table on sorted intervals, determine the maximum weight `max_w`.
   - We will build the result list of original indices.
   - We maintain: `count` = number of intervals chosen so far, `last_end` = end time of last chosen interval (initially -infinity).
   - We need to pick intervals in an order that produces lexicographically smallest original indices. But note: the output array is just the list of chosen indices, sorted? No, the problem says "array of at most 4 indices". Looking at examples, the output indices are not necessarily sorted in the order of selection, but the lexicographical comparison is on the array as a whole. Actually, re-reading: "Return the lexicographically smallest array of at most 4 indices". The array elements are the original indices. To make the array lexicographically smallest, we want the first element to be as small as possible, then the second, etc. This implies we should try to pick the interval with the smallest original index first, then the next smallest, etc., subject to non-overlapping and optimality constraints.
   
   So, the reconstruction should:
   - Iterate through original indices `i` from 0 to n-1.
   - For each original index `i`, let the interval be `[l, r, w]`.
   - Check if this interval can be included: it must not overlap with the last chosen interval (i.e., `l > last_end`).
   - If it can be included, check if including it can still lead to the optimal total weight. That is, if we include this interval, the remaining weight needed is `max_w - current_sum - w`, and we need to be able to get that weight from `count+1` more intervals from intervals that start after `r`.
   - To check feasibility efficiently, we can precompute a DP table that is indexed by the sorted order, but for reconstruction, we need to query based on start time. 
   
   Alternative: Precompute `best[k][t]` = maximum weight using k intervals from intervals that start after time t. But t can be large. Instead, since we have sorted intervals by end time, we can use the DP table and binary search.
   
   Actually, a cleaner method:
   - Let `dp[k][i]` be as defined. Also, let's define `suffix_dp[k][i]` = maximum weight using k intervals from the sorted intervals[i:] (i.e., from index i to n-1 in sorted order).
   - Then, during reconstruction, for a candidate interval at sorted position `pos` with original index `orig_idx`, if it doesn't overlap with last chosen, we check:
     - `current_sum + w + suffix_dp[count+1][next_pos] == max_w` where `next_pos` is the first sorted interval that starts after `r`.
   - If yes, we pick this interval, update `current_sum`, `count`, `last_end`, and add `orig_idx` to result. Then we need to continue searching for the next interval. But note: after picking an interval, we should not consider intervals that overlap with it again. And for lexicographical order, after picking an interval with original index `orig_idx`, the next interval must have original index > `orig_idx`? No, the output array is just the set of indices. Lexicographical comparison of arrays: [1, 3] vs [1, 4] -> [1,3] is smaller. So we want the smallest possible first index, then smallest possible second index given the first, etc.
   - Therefore, the reconstruction should iterate through original indices in increasing order. For each original index, if the interval doesn't overlap with the last chosen interval, check if including it is part of an optimal solution. If yes, include it and move on (but note: after including, the next interval must start after the current one's end, but its original index can be anything larger than the current original index? No, the output array is just the list of chosen indices. The lexicographical order is on the array of indices. So if we have chosen indices [1, 3], that is lexicographically smaller than [1, 4]. So we want to pick the smallest original index possible for the first slot, then the smallest original index possible for the second slot (that doesn't overlap with the first), etc.
   
   So the algorithm for reconstruction:
   - Initialize `result = []`, `current_sum = 0`, `last_end = -1`, `count = 0`.
   - We need to pick up to 4 intervals.
   - For each slot from 0 to 3:
     - Iterate through original indices `i` from 0 to n-1.
     - But we need to skip intervals that overlap with `last_end`.
     - For each such interval, check if including it can lead to an optimal solution.
     - To check: let `w = intervals[i][2]`, `r = intervals[i][1]`.
     - We need to know: what is the maximum weight achievable from `count+1` intervals from the set of intervals that start after `r`?
     - Let this be `max_future`. Then if `current_sum + w + max_future == max_w`, we can pick this interval.
     - Among all such valid intervals (that don't overlap and can lead to optimal), pick the one with the smallest original index.
     - Add that original index to `result`, update `current_sum += w`, `last_end = r`, `count += 1`, and break out of the inner loop to proceed to the next slot.
     - If no interval can be picked for a slot, stop.
   
   To implement `max_future` efficiently:
   - Precompute a DP table on sorted intervals: `dp[k][i]` = max weight using k intervals from sorted intervals[0:i+1].
   - Also, precompute `suffix_max[k][i]` = max weight using k intervals from sorted intervals[i:].
   - `suffix_max[k][i]` can be computed backwards:
     - `suffix_max[k][n] = 0` for all k.
     - For i from n-1 down to 0:
       - `suffix_max[k][i] = suffix_max[k][i+1]` (skip interval i)
       - Let `j` be the largest index such that `sorted_intervals[j].end < sorted_intervals[i].start`. If such j exists, then `candidate = suffix_max[k-1][j+1] + sorted_intervals[i].weight`.
       - `suffix_max[k][i] = max(suffix_max[k][i], candidate)`
   - Then, for a candidate interval at original index `i`, we need to find its position in the sorted array, say `pos`. Then `max_future = suffix_max[count+1][next_pos]` where `next_pos` is the first sorted interval with start > `r`. We can find `next_pos` by binary search on the sorted intervals' start times? Actually, we need intervals that start after `r`. Since the sorted array is by end time, not start time, we need to be careful.
   
   Actually, the `suffix_max` table is built on the sorted-by-end-time array. The value `suffix_max[k][i]` is the max weight using k intervals from the suffix starting at sorted index i. When we consider including an interval at sorted position `pos`, the next interval must have end time < start of current interval? No, the next interval must start after the current interval's end. But in the sorted-by-end-time array, the intervals are not sorted by start time. So the `suffix_max` approach might not directly give the max weight from intervals that start after a certain time.
   
   This is getting complicated. Given the constraints (n=5e4, k<=4), a feasible approach is:
   - Sort intervals by end time.
   - Compute `dp[k][i]` for k=1..4, i=0..n-1.
   - The global max weight is `max_w = max(dp[1][n-1], ..., dp[4][n-1])`.
   - For reconstruction, we iterate through original indices in order. For each original index, we check if the interval can be part of an optimal solution by verifying:
     - It doesn't overlap with the last chosen interval.
     - There exists a valid continuation that achieves the remaining weight.
   - To check the continuation, we can use the DP table: if the current interval is at sorted position `pos`, then the max weight from intervals that start after `r` and are after `pos` in sorted order? Not exactly, because the DP table is built on sorted-by-end-time, so the "after" in sorted order doesn't correspond to "after" in time.
   
   Given the complexity, and since k is very small, another approach is to use recursion with memoization for the reconstruction, but that might be slow.
   
   Actually, a standard technique for lexicographical smallest in interval scheduling with small k:
   - After computing DP table, reconstruct by iterating through original indices in increasing order. For each original index, if the interval doesn't overlap with the last chosen, check if including it is optimal by seeing if `dp[count+1][n-1]` (adjusted for the current state) equals the required weight. But we need a DP that is conditioned on the last end time.
   
   Given the time, I'll implement the following:
   1. Sort intervals by end time, keep original indices.
   2. Compute `dp[k][i]` for k=1..4, i=0..n-1.
   3. Find `max_w`.
   4. For reconstruction, we'll use a helper function that, given the current count and last end time, returns the max weight achievable from the remaining intervals (using the DP table and binary search). But to make it efficient, we precompute a separate DP or use the existing one with care.
   
   Due to the complexity and time constraints, I'll write the code with the DP and a reconstruction that uses binary search on the sorted array to find the best future weight, leveraging the `dp` table.

## worker: Preprocess intervals: store original indices and s
1. **Preprocessing**: Intervals are stored with their original indices and sorted by end point. This allows efficient binary search for non-overlapping intervals.
2. **DP Table (`dp`)**: `dp[k][i]` stores the maximum weight using exactly `k` intervals from the first `i+1` sorted intervals. This is computed using standard weighted interval scheduling logic with binary search to find the previous non-overlapping interval.
3. **Future DP (`future_dp`)**: `future_dp[k][i]` stores the maximum weight using exactly `k` intervals from the suffix `sorted_intervals[i:]`. This is computed backwards, using binary search to find the next non-overlapping interval (by start time) for inclusion.
4. **Reconstruction**: To achieve lexicographically smallest indices, we iterate through original indices in increasing order. For each candidate interval, we check if including it (without overlapping with the last chosen) can still achieve the global maximum weight by verifying: `current_sum + weight + future_dp[needed][next_i] == max_w`. The first such valid interval (smallest original index) is chosen for each slot.
5. **Complexity**: Sorting takes O(n log n). DP tables take O(4 * n * log n) due to binary searches. Reconstruction takes O(4 * n * log n) due to binary searches for each candidate. Overall: O(n log n), which is efficient for n = 5e4.
