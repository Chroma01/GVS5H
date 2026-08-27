class Solution:
    def maximumWeight(self, intervals: List[List[int]]) -> List[int]:
        n = len(intervals)
        # Store original indices and sort by end point
        sorted_intervals = []
        for i, (l, r, w) in enumerate(intervals):
            sorted_intervals.append((l, r, w, i))
        sorted_intervals.sort(key=lambda x: x[1])
        
        # Extract end points for binary search
        ends = [x[1] for x in sorted_intervals]
        
        # dp[k][i] = max weight using exactly k intervals from sorted_intervals[0..i]
        # k ranges from 0 to 4, i from 0 to n-1
        # Initialize dp table with 0
        # dp[0][i] = 0 for all i
        dp = [[0] * n for _ in range(5)]
        
        # Fill dp table
        for k in range(1, 5):
            for i in range(n):
                l_i, r_i, w_i, orig_i = sorted_intervals[i]
                # Option 1: skip interval i
                skip = dp[k][i-1] if i > 0 else 0
                # Option 2: include interval i
                # Find the largest j such that ends[j] < l_i
                # bisect_left returns the first index where ends[index] >= l_i
                # so j = bisect_left(ends, l_i) - 1
                import bisect
                j = bisect.bisect_left(ends, l_i) - 1
                include = 0
                if j >= 0:
                    include = dp[k-1][j] + w_i
                else:
                    if k == 1:
                        include = w_i
                    else:
                        include = 0
                dp[k][i] = max(skip, include)
        
        # Find the maximum weight achievable with at most 4 intervals
        max_w = 0
        max_k = 0
        for k in range(1, 5):
            if dp[k][n-1] > max_w:
                max_w = dp[k][n-1]
                max_k = k
        
        # If no intervals can be chosen (shouldn't happen given constraints), return empty
        if max_w == 0:
            return []
        
        # Reconstruction: find lexicographically smallest array of indices
        # We need to pick up to max_k intervals such that their original indices form the lexicographically smallest array.
        # Strategy: iterate through original indices in increasing order. For each original index, check if including the interval 
        # (if it doesn't overlap with the last chosen) can lead to an optimal solution.
        
        # To efficiently check feasibility, we need a way to query: given last_end and count of intervals chosen so far,
        # what is the max weight achievable from intervals that start after last_end?
        # We can precompute a suffix DP or use the existing dp table with binary search.
        
        # Let's define: best_after[k][end_time] = max weight using k intervals from intervals that start after end_time.
        # But end_time can be large. Instead, we can use the sorted_intervals array and the dp table.
        # Actually, we can compute a separate DP for "future" weights.
        # Let future_dp[k][i] = max weight using k intervals from sorted_intervals[i:] (i.e., from index i to n-1 in sorted order).
        # But note: the intervals in sorted_intervals are sorted by end time, not start time. So "from i onwards" doesn't necessarily mean "starting after some time".
        
        # Alternative: during reconstruction, for a candidate interval at sorted position pos with end time r, 
        # we need the max weight from k' intervals from intervals that start after r.
        # We can precompute an array: for each sorted index i, what is the max weight using k intervals from intervals that start after ends[i]?
        # Actually, we can compute a DP that is indexed by the sorted order, but conditioned on start time.
        
        # Given the small k (<=4), we can do the following:
        # Precompute for each k from 1 to 4, and for each sorted index i, the value:
        #   max_weight_from_start_after[k][i] = max weight using k intervals from intervals that start after sorted_intervals[i].end
        # But this is not straightforward because the intervals are sorted by end time.
        
        # Instead, let's use the following approach for reconstruction:
        # We'll maintain:
        #   result: list of chosen original indices
        #   current_sum: sum of weights of chosen intervals
        #   last_end: end time of last chosen interval (initially -1)
        #   count: number of intervals chosen so far
        #
        # For each slot from 0 to max_k-1:
        #   Iterate through original indices i from 0 to n-1.
        #   Let the interval be [l, r, w, orig_idx] = sorted_intervals[?] ... but we need to map original index to sorted position.
        #   Actually, we should iterate through the sorted_intervals in a way that we consider original indices in increasing order.
        #   So create a list of (original_index, sorted_position) and sort by original_index.
        
        orig_to_sorted = [0] * n
        for sorted_pos, (l, r, w, orig_idx) in enumerate(sorted_intervals):
            orig_to_sorted[orig_idx] = sorted_pos
        
        # Create a list of (original_index, sorted_position) sorted by original_index
        orig_sorted_positions = [(i, orig_to_sorted[i]) for i in range(n)]
        # They are already sorted by original_index since i goes from 0 to n-1
        
        # Precompute a "future" DP: 
        # Let future_dp[k][i] = max weight using k intervals from the set of intervals that start after sorted_intervals[i].end.
        # But the set of intervals that start after a given time is not a contiguous suffix in the sorted-by-end-time array.
        # 
        # Instead, we can precompute for each sorted index i, the value:
        #   max_future[k][i] = max weight using k intervals from intervals j such that sorted_intervals[j].start > sorted_intervals[i].end.
        # This can be computed by iterating backwards and using binary search to find the first interval that starts after a given end time? 
        # Actually, we can compute a separate DP on the sorted-by-end-time array for "future" weights, but conditioned on start time.
        #
        # Given the complexity, and since k is small, we can do the following during reconstruction:
        # For a candidate interval at sorted position pos with end time r, we need the max weight from k' intervals from intervals that start after r.
        # We can precompute an array: for each possible end time threshold, but end times are large.
        #
        # Better: Precompute an array `best_after` where best_after[k][i] is the max weight using k intervals from sorted_intervals[i:] (i.e., from index i to n-1 in sorted order).
        # But this doesn't account for the start time constraint.
        #
        # Actually, the standard weighted interval scheduling DP already computes the max weight for any prefix. 
        # For the "future" part, we can compute a similar DP backwards.
        # Let future_dp[k][i] = max weight using k intervals from sorted_intervals[i:].
        # Then, for a candidate interval at sorted position pos, the max weight from intervals that start after its end time r is:
        #   We need to find the smallest sorted index j such that sorted_intervals[j].start > r. Then future_dp[k'][j] is the answer.
        # But future_dp[k][i] is computed without considering start times of intervals in the suffix, only that they are in the suffix. 
        # However, because the array is sorted by end time, if we take a suffix starting at j, then all intervals in that suffix have end time >= sorted_intervals[j].end. 
        # But we need intervals that start after r. The condition is on start time, not end time.
        #
        # This is tricky. Given the time, I'll use a different approach for reconstruction:
        # Since k is at most 4, we can use recursion with memoization for the reconstruction, but that might be slow.
        #
        # Actually, a simpler method: 
        # After computing the main dp table, we can reconstruct by iterating through original indices in increasing order.
        # For each original index, if the interval doesn't overlap with the last chosen, check if including it is optimal by:
        #   Let pos = sorted position of this interval.
        #   Let k_needed = max_k - count - 1  (number of additional intervals needed after this one)
        #   We need to check if there exists a set of k_needed intervals from intervals that start after r (current interval's end) that sum to max_w - current_sum - w.
        #   To check this, we can use the dp table: 
        #       Find the largest sorted index j such that ends[j] < sorted_intervals[pos].start? No, we need intervals that start after r.
        #       Actually, we can precompute for each sorted index i, the value: 
        #           max_weight_from_start_after[k][i] = max weight using k intervals from intervals j with sorted_intervals[j].start > sorted_intervals[i].end.
        #       This can be computed by:
        #           For each i from n-1 down to 0:
        #               For k from 1 to 4:
        #                   Find the first sorted index j such that sorted_intervals[j].start > sorted_intervals[i].end. (Use binary search on start times)
        #                   Then max_weight_from_start_after[k][i] = future_dp[k][j] if j < n else 0
        #       But we need future_dp, which is the standard DP on the suffix.
        #
        # Let's compute future_dp[k][i] = max weight using k intervals from sorted_intervals[i:].
        # future_dp[k][i] = max( future_dp[k][i+1],  (dp-like recurrence) )
        # Actually, future_dp[k][i] can be computed as:
        #   future_dp[k][i] = max( future_dp[k][i+1],  w_i + future_dp[k-1][next_i] )
        #   where next_i is the smallest sorted index such that sorted_intervals[next_i].start > sorted_intervals[i].end.
        #
        # Steps for future_dp:
        #   future_dp = [[0]*(n+1) for _ in range(5)]
        #   For i from n-1 down to 0:
        #       l_i, r_i, w_i, orig_i = sorted_intervals[i]
        #       For k from 1 to 4:
        #           skip = future_dp[k][i+1]
        #           # find next_i: smallest index j such that sorted_intervals[j].start > r_i
        #           # We can precompute start times and use bisect
        #           starts = [x[0] for x in sorted_intervals]
        #           next_i = bisect.bisect_right(starts, r_i)  # first index where starts[index] > r_i
        #           include = 0
        #           if next_i < n:
        #               include = w_i + future_dp[k-1][next_i]
        #           future_dp[k][i] = max(skip, include)
        #
        # Then, during reconstruction:
        #   For a candidate interval at sorted position pos with end time r, and we need k' more intervals after this one:
        #       max_future = future_dp[k'][pos+1]  ??? Not exactly, because future_dp[k'][pos+1] considers intervals from pos+1 onwards, but we need intervals that start after r, which might include some intervals before pos+1 in sorted order? No, because the array is sorted by end time, and if an interval starts after r, its end time is > r, so it must appear after any interval that ends <= r. But since we are at sorted position pos, and the array is sorted by end time, all intervals from pos+1 onwards have end time >= sorted_intervals[pos].end = r. But we need start time > r. So we need to find the first interval in the entire array that starts after r, and then take future_dp from that index.
        #
        # Actually, the future_dp[k][i] as defined above (using next_i found by binary search on start times) already accounts for the start time constraint. So for a candidate interval at sorted position pos, the max weight from k' intervals that start after its end time r is future_dp[k'][next_i] where next_i is the first index with start > r.
        #
        # So the reconstruction algorithm:
        #   result = []
        #   current_sum = 0
        #   last_end = -1
        #   count = 0
        #   For slot in range(max_k):
        #       k_needed_after = max_k - count - 1  # number of intervals needed after this one
        #       best_orig_idx = -1
        #       best_interval = None
        #       For orig_idx, sorted_pos in orig_sorted_positions:
        #           l, r, w, orig = sorted_intervals[sorted_pos]
        #           if l <= last_end:  # overlaps with last chosen
        #               continue
        #           # Check if including this interval can lead to optimal solution
        #           # Find next_i: first sorted index with start > r
        #           next_i = bisect.bisect_right(starts, r)
        #           max_future = future_dp[k_needed_after][next_i] if next_i < n else 0
        #           if current_sum + w + max_future == max_w:
        #               best_orig_idx = orig_idx
        #               best_interval = (l, r, w, orig)
        #               break  # since we iterate in increasing original index, the first valid is the best
        #       If best_interval is None: break
        #       result.append(best_orig_idx)
        #       current_sum += best_interval[2]
        #       last_end = best_interval[1]
        #       count += 1
        #
        # Return result
        
        # Precompute starts for binary search
        starts = [x[0] for x in sorted_intervals]
        
        # Compute future_dp
        future_dp = [[0] * (n + 1) for _ in range(5)]
        # future_dp[k][i] = max weight using k intervals from sorted_intervals[i:]
        for i in range(n - 1, -1, -1):
            l_i, r_i, w_i, orig_i = sorted_intervals[i]
            for k in range(1, 5):
                skip = future_dp[k][i + 1]
                # find next_i: first index j such that starts[j] > r_i
                next_i = bisect.bisect_right(starts, r_i)
                include = 0
                if next_i < n:
                    include = w_i + future_dp[k - 1][next_i]
                future_dp[k][i] = max(skip, include)
        
        # Reconstruction
        result = []
        current_sum = 0
        last_end = -1
        count = 0
        
        for slot in range(max_k):
            k_needed_after = max_k - count - 1
            best_orig_idx = -1
            best_interval = None
            for orig_idx, sorted_pos in orig_sorted_positions:
                l, r, w, orig = sorted_intervals[sorted_pos]
                if l <= last_end:  # overlaps with last chosen
                    continue
                # Find next_i: first sorted index with start > r
                next_i = bisect.bisect_right(starts, r)
                max_future = future_dp[k_needed_after][next_i] if next_i < n else 0
                if current_sum + w + max_future == max_w:
                    best_orig_idx = orig_idx
                    best_interval = (l, r, w, orig)
                    break  # first valid in original index order is lexicographically smallest
            if best_interval is None:
                break
            result.append(best_orig_idx)
            current_sum += best_interval[2]
            last_end = best_interval[1]
            count += 1
            
        return result