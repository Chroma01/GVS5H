To solve this problem, we need to select up to 4 non-overlapping intervals such that their total weight is maximized, and among those with the maximum weight, the indices are lexicographically smallest. Since the number of intervals to pick is small (at most 4), we can iterate through all possible combinations of 1 to 4 intervals. For each combination, we check if they are non-overlapping, calculate the total weight, and track the best solution based on weight first, then lexicographical order of indices. To efficiently check non-overlapping conditions and compute weights, we can sort the intervals by their start times or simply rely on the fact that n is up to 50,000 but the combination count C(n, 4) is too large for brute force. Instead, we can use dynamic programming or a more efficient approach: since we need the lexicographically smallest indices, we should consider iterating through the intervals in the order of their original indices. However, a better approach given the constraints and the small k=4 is to use a DP where `dp[i][j]` represents the maximum weight achievable using exactly `j` intervals from the first `i` intervals, but we also need to handle the non-overlapping constraint. Actually, a simpler and more direct approach for small k is to iterate over all possible sets of 4 intervals? No, that's O(n^4). We need a smarter way.
Correct approach: Since k is small (4), we can iterate through all possible "gaps" or use a sweep-line with DP. Alternatively, we can precompute for each interval the best set of j intervals ending before it.
Let's refine: We want the lexicographically smallest index array. This suggests we should try to include smaller indices first. But the optimal set might not include small indices if they have low weight.
Actually, the standard solution for "select k non-overlapping intervals with max weight" uses DP: `dp[i][j]` = max weight using j intervals from intervals[0...i]. To reconstruct the lexicographically smallest solution, we can store not just the max weight but also the actual set of indices or enough info to reconstruct. Given n=50,000, storing sets is too heavy.
Better strategy:
1. Sort intervals by start time? No, we need original indices for the answer.
2. We can compute `max_weight[i][j]` = max weight using j intervals from the suffix starting at i? Or prefix?
Let's define `dp[j]` as the max weight using j intervals found so far. But we need to know the end time of the last interval to extend.
Standard technique:
- Sort intervals by end time? Or start time?
- Let's sort by start time to process in order of indices? No, indices are arbitrary.
- We need to consider all subsets of size 1..4.
Given the constraints and the requirement for lexicographically smallest indices, the most robust method is:
Iterate `k` from 1 to 4.
For a fixed `k`, we want to find the lexicographically smallest index array `[i1, i2, ..., ik]` such that `i1 < i2 < ... < ik` (since we sort the result indices), they are non-overlapping, and sum of weights is maximized.
Wait, the output requires the indices in increasing order? The problem says "lexicographically smallest array of at most 4 indices". Usually, this implies the indices in the array should be sorted. Example 1 output: [2, 3]. Example 2: [1, 3, 5, 6]. Yes, indices are sorted.
So we are looking for a sequence of indices `idx1 < idx2 < ... < idxk` (where k <= 4) such that intervals are non-overlapping, total weight is max, and the sequence is lexicographically smallest.
Algorithm:
1. Precompute `best[j][i]`: the maximum weight achievable using exactly `j` intervals from the first `i` intervals (0 to i-1), ending with an interval that finishes before or at some point? No.
Let's use a DP state: `dp[j]` = a list of tuples `(end_time, weight, last_index)`? No, we need to reconstruct the full path.
Actually, since k is very small (4), we can do the following:
- Iterate `i` from 0 to n-1 (original index).
- Maintain `dp[j]` = max weight using `j` intervals ending at or before current position?
Let's flip it.
Sort intervals by their end times? No, we need original indices.
Let's keep intervals in original order but process them.
Define `dp[j]` as a dictionary or list mapping `(end_time)` -> `(max_weight, last_index)`. But end times can be large.
Actually, we only care about the end time of the last interval added.
Let `dp[j]` be a list of pairs `(end_time, (weight, last_index))` representing the best way to pick `j` intervals ending with an interval that ends at `end_time`.
But we need to maximize weight first, then minimize the index sequence.
Since we need the lexicographically smallest index sequence, we should prioritize picking smaller indices.
Strategy:
1. Iterate `k` from 1 to 4.
2. For each `k`, we want to find the lexicographically smallest sequence of indices.
3. We can use a DP where `dp[i][j]` = max weight using `j` intervals from the first `i` intervals (indices 0 to i-1).
   But to reconstruct the lexicographically smallest solution, we need to know which interval was picked last.
   Actually, we can compute `dp[j]` = max weight using `j` intervals from the entire set, but we need to know the end time to extend.
   Let's define `f[j]` as a list of `(end_time, weight, last_index)` for the best solution of size `j`. But there might be multiple solutions with same weight and same end time? No, we want the one that allows extending to a lexicographically smaller full sequence? This is tricky.
   
Alternative approach (simpler for k=4):
Since k is small, we can iterate over all possible "first" intervals, then "second", etc., but that's O(n^4).
We need O(n * k) or O(n * k * log n).
Let's define `dp[j]` = a list of `(end_time, weight, last_original_index)` representing the best solution of size `j` ending with an interval that ends at `end_time`.
But we want to maximize weight, then minimize the index sequence.
Actually, the lexicographical comparison is on the sequence of indices.
If we have two solutions of size 4: [a, b, c, d] and [e, f, g, h] with a < e, then [a, ...] is smaller.
So we should try to pick the smallest possible first index, then the smallest possible second index, etc., while maximizing the total weight.
This suggests a greedy approach with backtracking or DP.
Let `dp[j]` be the maximum weight achievable using `j` intervals from the suffix of intervals starting after some point?
Let's define `dp[i][j]` = max weight using `j` intervals from intervals `i` to `n-1`.
Then we can iterate `i` from 0 to n-1, and for each `i`, try to pick interval `i` as the next interval in our sequence.
If we pick interval `i` (which has weight `w` and ends at `r`), then the remaining `j-1` intervals must be chosen from intervals that start after `r`.
We can precompute `suffix_max[j][start_index]` = max weight using `j` intervals from intervals with start index >= `start_index`.
But the condition is non-overlapping, so we need intervals that start > `r`.
So, let `best[j][r]` = max weight using `j` intervals from intervals that start > `r`.
We can compute this by iterating `r` from max_coordinate down to min. But coordinates are up to 10^9.
Instead, we can compress coordinates or just iterate over the intervals.
Let's sort intervals by start time? No, we need original indices.
Let's keep intervals in original order.
Precompute `suffix[j][i]` = max weight using `j` intervals from the subarray `intervals[i:]`.
To compute `suffix[j][i]`:
Option 1: Don't pick `intervals[i]`. Then `suffix[j][i] = suffix[j][i+1]`.
Option 2: Pick `intervals[i]`. Then we need `j-1` intervals from intervals that start > `intervals[i].end`.
We need to find the smallest index `k > i` such that `intervals[k].start > intervals[i].end`.
Then `suffix[j][i] = max(suffix[j][i+1], weight[i] + suffix[j-1][k])`.
We can find `k` using binary search (since we can sort intervals by start time? No, we need to preserve original indices for the DP state? No, the DP state `suffix[j][i]` depends on the index `i` in the original array).
Wait, if we sort intervals by start time to compute the DP, we lose the original indices.
But we can store the original index in the interval.
So:
1. Create a list of intervals with original indices.
2. Sort this list by start time. Let's call this `sorted_intervals`.
3. Precompute `suffix[j][idx]` for `sorted_intervals`, where `idx` is the index in `sorted_intervals`.
   `suffix[j][idx]` = max weight using `j` intervals from `sorted_intervals[idx:]`.
   Transition:
   - Skip `sorted_intervals[idx]`: `val1 = suffix[j][idx+1]`
   - Pick `sorted_intervals[idx]`: find the first `next_idx` in `sorted_intervals` such that `sorted_intervals[next_idx].start > sorted_intervals[idx].end`. Then `val2 = weight[idx] + suffix[j-1][next_idx]`.
   - `suffix[j][idx] = max(val1, val2)`
   We also need to handle the lexicographical requirement. The DP gives max weight, but we need the lexicographically smallest original index sequence.
   The DP state only gives the max weight. To get the lexicographically smallest sequence, we need to reconstruct the solution carefully.
   Since we need the lexicographically smallest sequence of original indices, and the sequence must be sorted (i1 < i2 < ... < ik), we should try to pick the smallest possible original index for the first interval, then the smallest for the second, etc., while ensuring the total weight is the global maximum.
   
   Revised Plan:
   1. Compute `max_total_weight` for each `k` (1 to 4) using the DP described above (on sorted intervals by start time).
      Actually, the DP on sorted intervals by start time gives the max weight for a fixed `k`. Let `global_max[k]` be this value.
   2. Once we know `global_max[k]` for k=1..4, we can reconstruct the lexicographically smallest sequence for each `k`.
      To reconstruct:
      - We want the smallest original index `i1`. Iterate `i` from 0 to n-1 (original index).
      - Check if there exists a valid sequence starting with `i` that achieves `global_max[1]` (or `global_max[k]` if we are building a sequence of length k).
      - To check efficiently:
        - If we pick original index `i` (interval `I`), we need to find if there exists a sequence of `k-1` intervals from intervals starting after `I.end` that sums to `global_max[k] - weight[I]`.
        - We can use the precomputed `suffix` table (on sorted intervals) to check this in O(1) or O(log n).
        - Specifically, find the smallest index `next_idx` in `sorted_intervals` such that `sorted_intervals[next_idx].start > I.end`.
        - Check if `suffix[k-1][next_idx] == required_weight`.
        - If yes, then `i` is a candidate for the first element. Since we iterate `i` from 0 upwards, the first `i` we find is the smallest.
        - Then recursively find the next element.
   3. We do this for `k` from 1 to 4. For each `k`, we find the best sequence.
   4. Compare the sequences for different `k` based on total weight (maximize) and then lexicographically (minimize).
      Note: The problem says "up to 4". So we compare sequences of length 1, 2, 3, 4.
      First, maximize total weight. If weights are equal, choose the lexicographically smallest sequence.
      Also, a sequence of length 4 with weight W is compared with length 3 with weight W? Yes, lexicographically.
      But typically, adding an interval increases weight (weights >= 1), so max weight will likely be for k=4. But if no 4 non-overlapping intervals exist, we take k=3, etc.
      Actually, we should compute `global_max[k]` for k=1..4.
      Then find the best `k` (max weight, then lex smallest).
      Then reconstruct the sequence for that `k`.

   Complexity:
   - Sorting: O(n log n).
   - Precomputing `suffix`: O(n * 4 * log n) because for each state we do a binary search.
   - Reconstruction: O(4 * n * 4) = O(n).
   Total: O(n log n). This fits within constraints.