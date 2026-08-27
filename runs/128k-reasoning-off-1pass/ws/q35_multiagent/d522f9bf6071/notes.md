
## ideation
The core difficulty lies in two aspects:
1.  **Maximizing Weight**: We need to select up to 4 non-overlapping intervals with the maximum total weight. This is a classic variation of the Weighted Interval Scheduling problem, but limited to at most 4 intervals.
2.  **Lexicographically Smallest Indices**: Among all sets of intervals that achieve the maximum weight, we must return the one whose indices (sorted in ascending order) are lexicographically smallest.

The plan suggests sorting by end time for DP, which is standard for interval scheduling. However, sorting destroys the original index order. The reconstruction step needs to be careful.

A robust approach:
1.  **Sort Intervals**: Sort the intervals by their end times. If end times are equal, sort by start times (or original index, though end time is the primary key for non-overlapping checks). Let's call this sorted list `sorted_intervals`. We need to keep track of original indices.
2.  **Precompute Previous Non-Overlapping**: For each interval in the sorted list, find the index of the latest interval that ends strictly before the current interval starts. This can be done using binary search (`bisect_left` on end times).
3.  **Dynamic Programming**:
    -   Define `dp[k][i]` as the maximum weight achievable using `k` intervals from the first `i` intervals in the sorted list.
    -   `k` ranges from 0 to 4. `i` ranges from 0 to `n` (number of intervals).
    -   Base case: `dp[0][i] = 0` for all `i`.
    -   Transition: For `k` from 1 to 4, and `i` from 1 to `n`:
        -   Let `idx = i - 1` (0-based index in sorted list).
        -   Option 1: Don't include interval `idx`. `dp[k][i] = dp[k][i-1]`.
        -   Option 2: Include interval `idx`. Find `prev` such that `sorted_intervals[prev]` is the last interval ending before `sorted_intervals[idx].start`. If no such interval exists, `prev = -1` (which maps to `dp[k-1][0]`).
        -   `dp[k][i] = max(dp[k][i-1], dp[k-1][prev + 1] + weight[idx])`. Note: `prev + 1` is used because `dp` is 1-indexed with respect to the count of intervals considered.
4.  **Reconstruction for Lexicographical Order**:
    -   The maximum weight is `max(dp[1..4][n])`. Let `max_w` be this value.
    -   To get the lexicographically smallest indices, we should iterate through the original intervals in increasing order of their original indices.
    -   However, the DP was built on sorted intervals. A better reconstruction strategy:
        -   Iterate through the original indices `0` to `n-1`.
        -   For each original index `i`, check if including this interval can lead to an optimal solution.
        -   To do this efficiently, we can re-run a "greedy-like" check or use the DP table.
        -   Actually, a simpler way for lexicographical smallest:
            -   We want the smallest index `i` such that there exists a valid set of 4 (or fewer) intervals including `i` that sums to `max_w`.
            -   We can iterate `i` from 0 to `n-1` (original indices).
            -   For a candidate interval `i`, we need to check:
                1.  Is it possible to pick `k` more intervals after `i` (non-overlapping) such that the total weight is `max_w - weight[i]`?
                2.  Is it possible to pick `k'` intervals before `i` (non-overlapping) such that the total weight is `max_w - weight[i] - weight_of_later_intervals`?
            -   This bidirectional check is complex.
    
    Alternative Reconstruction Strategy:
    -   Since `K` is small (4), we can reconstruct by iterating through the sorted intervals in a specific order? No, lexicographical order is on original indices.
    -   Correct Strategy:
        1.  Compute `dp_forward[k][i]`: Max weight using `k` intervals from the first `i` intervals in the sorted list.
        2.  Compute `dp_backward[k][i]`: Max weight using `k` intervals from the last `n-i` intervals in the sorted list (i.e., intervals from index `i` to `n-1` in sorted list).
        3.  Iterate through original indices `i` from 0 to `n-1`.
        4.  For each original index `i`, let `j` be its position in the sorted list.
        5.  Check if including interval `j` is part of an optimal solution:
            -   We need to find if there exist `k1` intervals before `j` and `k2` intervals after `j` such that `k1 + 1 + k2 <= 4` and `dp_forward[k1][j] + weight[j] + dp_backward[k2][j+1] == max_w`.
            -   Actually, `dp_forward[k][j]` uses intervals from `0` to `j-1` in sorted list. `dp_backward[k][j+1]` uses intervals from `j+1` to `n-1` in sorted list.
            -   We iterate `k1` from 0 to 4-1 and `k2` from 0 to 4-1-k1.
            -   If `dp_forward[k1][j] + weight[j] + dp_backward[k2][j+1] == max_w`, then including interval `j` is valid.
            -   Since we iterate original indices in increasing order, the first one we find is the lexicographically smallest first element.
            -   Once we pick interval `j`, we update our constraints: we need `k2` intervals after `j` and `k1` before. But since we picked `j`, we effectively reduce the problem to finding `k2` intervals after `j` with weight `max_w - weight[j] - dp_forward[k1][j]`.
            -   However, `k1` and `k2` are not fixed. We just need *some* combination.
            -   To ensure lexicographical smallest, once we pick the first interval `j`, we then need to pick the next smallest original index `i'` that is compatible.
            -   This suggests a recursive or iterative selection:
                -   Current required weight `rem_w = max_w`.
                -   Current allowed count `rem_k = 4`.
                -   Current lower bound for end time `min_end = -inf`.
                -   Iterate original indices `i` from 0 to `n-1`.
                -   Let `j` be the sorted index of interval `i`.
                -   Check if interval `i` can be part of a solution:
                    -   It must not overlap with the previously selected interval (if any).
                    -   We need to check if `weight[i] + max_possible_weight_from_intervals_after_j_with_count_rem_k-1 == rem_w`.
                    -   The "max possible weight from intervals after j with count k" is `dp_backward[k][j+1]`.
                    -   So, if `weight[i] + dp_backward[rem_k - 1][j+1] == rem_w`, then we can pick this interval.
                    -   Why? Because `dp_backward[rem_k - 1][j+1]` gives the max weight of `rem_k - 1` intervals from the sorted list starting after `j`. Since the sorted list contains all intervals, and we are iterating in original index order, the first `i` that satisfies this condition is the lexicographically smallest choice for the current slot.
                    -   Update `rem_w -= weight[i]`, `rem_k -= 1`, `min_end = sorted_intervals[j].end`.
                    -   Add `i` to result.
                    -   Break the inner loop (move to next slot).
                -   Stop when `rem_k == 0` or `rem_w == 0`.

    This approach works because:
    1.  `dp_backward[k][j]` is precomputed correctly.
    2.  Iterating original indices ensures lexicographical order.
    3.  The condition `weight[i] + dp_backward[rem_k - 1][j+1] == rem_w` ensures that picking `i` allows completing the solution with the remaining weight and count.
    4.  We also need to ensure the interval doesn't overlap with the previous one. We can check `sorted_intervals[j].start > min_end`.

    Pitfalls:
    -   `dp_backward` definition: `dp_backward[k][j]` should be max weight of `k` intervals from sorted indices `j` to `n-1`.
    -   Initialization of `dp_backward`: `dp_backward[0][j] = 0` for all `j`. `dp_backward[k][n] = -inf` for `k > 0`.
    -   Transition for `dp_backward`: `dp_backward[k][j] = max(dp_backward[k][j+1], weight[j] + dp_backward[k-1][next_non_overlap])`. Here `next_non_overlap` is the first index in sorted list that starts after `sorted_intervals[j].end`.
    -   Binary search for `next_non_overlap`: Find smallest index `p` in `sorted_intervals` such that `sorted_intervals[p].start > sorted_intervals[j].end`.

    Complexity:
    -   Sorting: O(N log N).
    -   Precomputing next non-overlap: O(N log N).
    -   DP Forward/Backward: O(K * N) = O(N).
    -   Reconstruction: O(N * K) in worst case, but effectively O(N) as we pick at most 4.
    -   Total: O(N log N).

```python
class Solution:
    def maximumWeight(self, intervals: List[List[int]]) -> List[int]:
        n = len(intervals)
        # Store original indices
        sorted_intervals = sorted(range(n), key=lambda i: (intervals[i][1], intervals[i][0]))
        
        # Create a list of (start, end, weight, original_index) sorted by end time
        sorted_data = []
        for idx in sorted_intervals:
            l, r, w = intervals[idx]
            sorted_data.append((l, r, w, idx))
            
        # Precompute next non-overlapping interval index for each interval in sorted_data
        # next_non_overlap[i] = smallest index j > i such that sorted_data[j][0] > sorted_data[i][1]
        # If no such j, then next_non_overlap[i] = n
        end_times = [x[1] for x in sorted_data]
        next_non_overlap = [n] * n
        for i in range(n):
            # Find first index j where end_times[j] > sorted_data[i][1]
            # Since end_times is sorted, we can use bisect
            import bisect
            # bisect_right returns insertion point after all elements <= value
            # We want first element > value, which is exactly bisect_right
            j = bisect.bisect_right(end_times, sorted_data[i][1])
            if j < n:
                next_non_overlap[i] = j
            else:
                next_non_overlap[i] = n
                
        # dp_forward[k][i] = max weight using k intervals from sorted_data[0...i-1]
        # k from 0 to 4, i from 0 to n
        dp_forward = [[0] * (n + 1) for _ in range(5)]
        for k in range(1, 5):
            for i in range(1, n + 1):
                # Option 1: skip interval i-1
                dp_forward[k][i] = dp_forward[k][i-1]
                # Option 2: take interval i-1
                idx = i - 1
                l, r, w, orig = sorted_data[idx]
                # Find previous non-overlapping
                # We need largest index p < i such that sorted_data[p][1] < l
                # In sorted_data, indices 0 to i-1 are considered.
                # We can use bisect_left on end_times for values < l
                # bisect_left returns first index where end_times[index] >= l
                # So the interval before that index is the last one with end < l
                p = bisect.bisect_left(end_times, l, 0, i)
                # p is the count of intervals in 0..i-1 that end < l
                # So dp_forward[k-1][p] is the max weight for k-1 intervals from first p intervals
                prev_val = dp_forward[k-1][p]
                if prev_val + w > dp_forward[k][i]:
                    dp_forward[k][i] = prev_val + w
                    
        # dp_backward[k][i] = max weight using k intervals from sorted_data[i...n-1]
        # k from 0 to 4, i from 0 to n
        dp_backward = [[0] * (n + 1) for _ in range(5)]
        # Initialize dp_backward[k][n] = -inf for k > 0, but since weights are positive, 0 is fine for k=0
        # Actually, for k>0, if no intervals available, weight should be -inf to indicate invalid
        # But we can handle it by checking if we can actually pick k intervals.
        # Let's use a very small number for invalid states.
        INF = float('inf')
        for k in range(1, 5):
            dp_backward[k][n] = -INF
            
        for k in range(1, 5):
            for i in range(n - 1, -1, -1):
                # Option 1: skip interval i
                dp_backward[k][i] = dp_backward[k][i+1]
                # Option 2: take interval i
                l, r, w, orig = sorted_data[i]
                nxt = next_non_overlap[i]
                # nxt is the first index in sorted_data that starts after r
                # So we can take k-1 intervals from nxt onwards
                if dp_backward[k-1][nxt] != -INF:
                    val = w + dp_backward[k-1][nxt]
                    if val > dp_backward[k][i]:
                        dp_backward[k][i] = val
                        
        # Find max weight
        max_w = 0
        for k in range(1, 5):
            if dp_backward[k][0] > max_w:
                max_w = dp_backward[k][0]
                
        # Reconstruct lexicographically smallest indices
        result = []
        rem_w = max_w
        rem_k = 4
        min_end = -1  # End time of last selected interval, initially -1 (no constraint)
        
        # We iterate through original indices in increasing order
        # But we need to map original index to sorted index
        # Create a map: original_index -> sorted_index
        orig_to_sorted = [0] * n
        for s_idx, o_idx in enumerate(sorted_intervals):
            orig_to_sorted[o_idx] = s_idx
            
        # We need to select up to 4 intervals
        # In each step, we try to pick the smallest original index that can be part of an optimal solution
        # given the remaining weight and count, and non-overlapping constraint.
        
        # Note: We might pick fewer than 4 intervals if that yields max_w.
        # The condition for picking an interval at sorted index `s` with original index `o`:
        # 1. It must not overlap with the previous selection: sorted_data[s][0] > min_end
        # 2. It must be possible to complete the solution:
        #    weight[s] + dp_backward[rem_k - 1][next_non_overlap[s]] == rem_w
        #    But wait, dp_backward[rem_k - 1][next_non_overlap[s]] is the max weight of rem_k-1 intervals from sorted_data[next_non_overlap[s]:]
        #    This assumes we pick exactly rem_k-1 more intervals. But we can pick up to rem_k-1.
        #    Actually, dp_backward[k][i] is defined as max weight using *up to* k intervals? 
        #    No, our DP definition was *exactly* k intervals? 
        #    Let's check: 
        #    dp_forward[k][i] = max(dp_forward[k][i-1], ...) -> this allows skipping, so it's *at most* k intervals from first i.
        #    Similarly, dp_backward[k][i] = max(dp_backward[k][i+1], ...) -> allows skipping, so it's *at most* k intervals from i to end.
        #    So dp_backward[k][i] is max weight using *at most* k intervals.
        #    Therefore, the condition is:
        #    weight[s] + dp_backward[rem_k - 1][next_non_overlap[s]] == rem_w
        #    is correct if we want to use *exactly* the remaining weight with *at most* rem_k-1 more intervals.
        #    But since dp_backward[rem_k-1] is the max weight with *at most* rem_k-1, if the sum equals rem_w, it means we can achieve rem_w.
        
        # However, there's a subtle point: 
        # If we pick an interval, we reduce rem_k by 1. But we might not need to use all 4.
        # The DP table dp_backward[k][i] stores the max weight using *at most* k intervals.
        # So if we have rem_k left, and we pick one, we need to achieve rem_w - weight[s] with *at most* rem_k - 1 intervals from the remaining valid intervals.
        # This is exactly dp_backward[rem_k - 1][next_non_overlap[s]].
        
        # One more thing: min_end constraint.
        # The dp_backward table does not account for min_end. It assumes we can pick any non-overlapping intervals from the sorted list starting from next_non_overlap[s].
        # But next_non_overlap[s] ensures that the next interval starts after sorted_data[s][1].
        # And since sorted_data is sorted by end time, and we are moving forward, the non-overlapping condition is handled by next_non_overlap.
        # The min_end check is only needed to ensure the current interval doesn't overlap with the *previous* selected interval.
        # The dp_backward part ensures that the *future* intervals don't overlap with the *current* interval.
        
        # So the algorithm:
        for _ in range(4):  # Try to pick up to 4 intervals
            if rem_w == 0:
                break
            found = False
            for o_idx in range(n):
                s_idx = orig_to_sorted[o_idx]
                l, r, w, orig = sorted_data[s_idx]
                
                # Check non-overlap with previous
                if l <= min_end:
                    continue
                    
                # Check if picking this interval can lead to optimal solution
                # We need to achieve rem_w - w with at most rem_k - 1 intervals from sorted_data[next_non_overlap[s_idx]:]
                nxt = next_non_overlap[s_idx]
                # dp_backward[rem_k - 1][nxt] is the max weight with at most rem_k-1 intervals from nxt onwards
                if dp_backward[rem_k - 1][nxt] == rem_w - w:
                    # Pick this interval
                    result.append(o_idx)
                    rem_w -= w
                    rem_k -= 1
                    min_end = r
                    found = True
                    break  # Move to next slot (next iteration of outer loop)
                    
            if not found:
                # Should not happen if max_w is correct
                break
                
        return result
```

## worker: (none)
The solution uses dynamic programming to solve the weighted interval scheduling problem with a limit of 4 intervals. 
1. **Sorting**: Intervals are sorted by end time to facilitate efficient non-overlapping checks.
2. **Precomputation**: For each interval, we precompute the index of the next non-overlapping interval using binary search on end times.
3. **DP Tables**: 
   - `dp_forward[k][i]` stores the maximum weight using at most `k` intervals from the first `i` intervals in the sorted list.
   - `dp_backward[k][i]` stores the maximum weight using at most `k` intervals from the last `n-i` intervals in the sorted list.
4. **Reconstruction**: To ensure lexicographically smallest indices, we iterate through original indices in increasing order. For each interval, we check if including it allows us to achieve the remaining required weight with the remaining allowed count, using the `dp_backward` table. The first such interval found is added to the result, and we update the remaining weight, count, and minimum end time constraint.

Complexity:
- Sorting: O(N log N)
- Precomputation: O(N log N)
- DP Tables: O(K * N) = O(N) since K=4
- Reconstruction: O(N * K) = O(N)
- Total: O(N log N)
