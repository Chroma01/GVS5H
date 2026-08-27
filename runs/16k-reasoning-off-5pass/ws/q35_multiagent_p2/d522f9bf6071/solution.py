class Solution:
    def maximumWeight(self, intervals: List[List[int]]) -> List[int]:
        n = len(intervals)
        # Create a list of (end, start, weight, original_index)
        sorted_intervals = []
        for idx, (l, r, w) in enumerate(intervals):
            sorted_intervals.append((r, l, w, idx))
        sorted_intervals.sort()
        
        # Extract end points for binary search
        ends = [x[0] for x in sorted_intervals]
        
        # dp[k][i] = max weight using k intervals from first i sorted intervals
        # k ranges from 0 to 4, i ranges from 0 to n-1
        # We'll use a 2D array for dp, but to save space and time, we can use lists of lists.
        # dp[k][i] will store the max weight for k intervals using subset of first i intervals.
        # Initialize dp with zeros.
        dp = [[0] * n for _ in range(5)]
        
        # For each k from 1 to 4, we compute dp[k][i]
        # Also, we maintain a prefix max array for each k to quickly get max dp[k-1][j] for j < i
        # But note: the transition for dp[k][i] is:
        #   dp[k][i] = max(dp[k][i-1], weight_i + max_{j: end_j < start_i} dp[k-1][j])
        # To get max_{j: end_j < start_i} dp[k-1][j] efficiently, we can precompute for each k-1,
        # an array where for each index i, we have the max dp[k-1][j] for j from 0 to i.
        # However, since we process i from 0 to n-1, we can maintain a running max for k-1.
        
        # Instead, we can do:
        # Let best[k][i] = max(dp[k][0], dp[k][1], ..., dp[k][i])
        # Then for interval i (in sorted order), to compute dp[k][i]:
        #   Find the largest index j such that ends[j] < start_i. Then the best previous is best[k-1][j] (if j>=0, else 0).
        #   Then dp[k][i] = max(dp[k][i-1], weight_i + (best[k-1][j] if j>=0 else 0))
        #   And best[k][i] = max(best[k][i-1], dp[k][i])
        
        # We'll compute best[k][i] on the fly for k=1..4.
        # best[k] will be an array of length n, where best[k][i] is the max dp[k][0..i]
        best = [[0] * n for _ in range(5)]
        
        # For k=0, best[0][i] = 0 for all i, and dp[0][i]=0.
        # We'll iterate k from 1 to 4.
        for k in range(1, 5):
            # For each k, we'll compute dp[k][i] and best[k][i]
            # We can maintain a variable for the best value of dp[k-1] seen so far? 
            # Actually, no: because for each interval i, we need the best dp[k-1] for intervals ending before start_i.
            # So we need to use binary search to find the index j, and then use best[k-1][j] (which is the max dp[k-1][0..j]).
            
            # Initialize best[k][0] later, but we can compute iteratively.
            # Let prev_best = best[k-1]  # This is an array of length n
            prev_best = best[k-1]
            # current best for k, we'll build it
            cur_best = [0] * n
            # dp[k][i] is not stored separately, we only need best[k][i]
            # But for reconstruction, we might need the actual dp values? Actually, for reconstruction we need to know the max weight achievable from a state.
            # Actually, we can store dp[k][i] in a separate table if needed, but note: best[k][i] = max(best[k][i-1], dp[k][i])
            # And dp[k][i] = max(best[k][i-1], weight_i + (prev_best[j] if j found else 0))
            # So best[k][i] = max(best[k][i-1], weight_i + (prev_best[j] if j found else 0))
            # Therefore, we don't need to store dp[k][i] separately.
            
            # For i from 0 to n-1:
            for i in range(n):
                r_i, l_i, w_i, orig_i = sorted_intervals[i]
                # Find the largest j such that ends[j] < l_i
                # We can use bisect_left on ends for l_i, then j = pos - 1
                pos = bisect.bisect_left(ends, l_i)
                # pos is the first index where ends[pos] >= l_i, so j = pos - 1 is the last index with end < l_i
                if pos > 0:
                    prev_val = prev_best[pos-1]
                else:
                    prev_val = 0
                # The candidate value if we take interval i
                candidate = w_i + prev_val
                # The value if we don't take interval i is best[k][i-1] (if i>0, else 0)
                if i > 0:
                    not_take = best[k][i-1]
                else:
                    not_take = 0
                # dp[k][i] = max(not_take, candidate)
                # best[k][i] = max(not_take, candidate)  [because best[k][i] is the max of dp[k][0..i]]
                # Actually, best[k][i] = max(best[k][i-1], candidate)
                if i == 0:
                    cur_best[i] = candidate
                else:
                    cur_best[i] = max(best[k][i-1], candidate)
            best[k] = cur_best
        
        # The maximum weight is best[4][n-1] (if we use up to 4 intervals, the best is in best[4][n-1])
        # But note: we can use 1,2,3, or 4 intervals. The best[4][n-1] is the max weight using at most 4 intervals? 
        # Actually, our dp state: best[k][i] is the max weight using exactly k intervals? 
        # No: because we allow skipping intervals, so best[k][i] is the max weight using at most k intervals from first i.
        # Actually, the recurrence: 
        #   candidate = w_i + prev_best[pos-1]  -> this uses k intervals: k-1 from previous and 1 current.
        #   and we take max with not taking current, which is best[k][i-1] (which is at most k intervals from first i-1).
        # So best[k][i] is the max weight using at most k intervals from first i.
        # Therefore, the answer for maximum weight is best[4][n-1].
        
        max_weight = best[4][n-1]
        
        # Now reconstruct the lexicographically smallest set of indices.
        # We iterate through the original indices in increasing order.
        # We need to choose intervals such that:
        #   - They are non-overlapping.
        #   - The total weight is max_weight.
        #   - The set of indices is lexicographically smallest.
        #
        # How to check if an interval (with original index idx) can be chosen?
        # Let last_end be the end of the last chosen interval (initially -infinity).
        # Let rem_slots be the number of slots left (initially 4).
        # For an interval i (in original index order) with [l, r, w]:
        #   If l > last_end (non-overlapping with last chosen), then we can consider choosing it.
        #   If we choose it, then the remaining weight we need is max_weight - w.
        #   And we need to check if it is possible to get max_weight - w from intervals that end after r, using rem_slots - 1 slots.
        #
        # To check the "future" part efficiently, we can precompute a suffix max array for the DP table.
        # Specifically, for each k (from 0 to 4) and for each starting point (in terms of sorted index), what is the max weight achievable from intervals with sorted index >= j using at most k intervals?
        #
        # Let suf[k][j] = max weight achievable from sorted_intervals[j:] using at most k intervals.
        # We can compute suf[k][j] from right to left.
        # suf[k][j] = max( suf[k][j+1],  w_j + (suf[k-1][next_j] if next_j exists else 0) )
        # where next_j is the first index in sorted_intervals such that end >= start_j? Actually, no: for the future, we need intervals that start after the current interval ends.
        # Actually, when reconstructing, after choosing an interval with end r, the next interval must start > r.
        # So for the future part, we need: from the set of intervals that start > r, what is the max weight using at most k-1 intervals?
        #
        # We can precompute suf[k][j] for j from n-1 down to 0, where suf[k][j] is the max weight using at most k intervals from sorted_intervals[j:].
        # But note: the intervals in sorted_intervals[j:] are sorted by end time. However, the condition for non-overlapping is that the next interval must start > current end.
        # So for a given current interval i (in sorted order) with end r_i, the next interval must be chosen from indices j such that start_j > r_i.
        # We can use binary search to find the first index j0 such that start_j0 > r_i, then suf[k-1][j0] gives the max weight from intervals j0 to n-1 using at most k-1 intervals.
        #
        # Steps for reconstruction:
        # 1. Precompute suf[k][j] for k=0..4 and j=0..n-1.
        #    suf[0][j] = 0 for all j.
        #    For k from 1 to 4:
        #       suf[k][n-1] = max(0, weight of last interval)  [but actually, we take max of not taking and taking]
        #       Actually, we can compute:
        #         suf[k][j] = suf[k][j+1]   [not taking interval j]
        #         candidate = w_j + (suf[k-1][next_j] if next_j exists else 0)
        #         then suf[k][j] = max(suf[k][j+1], candidate)
        #       where next_j is the first index such that start_{next_j} > end_j.
        #
        # 2. Then, iterate original indices from 0 to n-1. For each interval, check if it can be part of the solution.
        #    Let last_end = -1 (since coordinates are at least 1, we can use -1)
        #    rem_slots = 4
        #    current_needed = max_weight
        #    result = []
        #    For idx from 0 to n-1:
        #        l, r, w = intervals[idx]
        #        If l > last_end:  # non-overlapping with last chosen
        #            # Check if choosing this interval can lead to the optimal solution
        #            # We need: w + (max weight from intervals that start > r using rem_slots-1 slots) == current_needed
        #            # But note: the max weight from intervals that start > r using rem_slots-1 slots is given by suf[rem_slots-1][first_index_with_start>r]
        #            # How to get first_index_with_start>r? We can precompute an array of starts and use bisect.
        #            # Actually, we have sorted_intervals, but we need to map the original index to the sorted index? 
        #            # Alternatively, we can precompute an array "starts" for the sorted intervals, and then for a given r, find the first sorted index j such that starts[j] > r.
        #            # Then suf[rem_slots-1][j] is the max weight achievable from sorted_intervals[j:] with rem_slots-1 slots.
        #            # Then if w + suf[rem_slots-1][j] == current_needed, then we can choose this interval.
        #            # But note: it might be that there are multiple ways, but we want the lexicographically smallest index, so the first one that satisfies the condition is chosen.
        #            # However, we must also update last_end, rem_slots, and current_needed.
        #            # But caution: it is possible that w + suf[rem_slots-1][j] >= current_needed? Actually, we know that the total max is current_needed, and if we choose this interval, the remaining must be exactly current_needed - w.
        #            # And suf[rem_slots-1][j] is the maximum possible from the future, so if w + suf[rem_slots-1][j] == current_needed, then it is valid.
        #            # But note: it is possible that w + suf[rem_slots-1][j] > current_needed? No, because current_needed is the global max, and suf[rem_slots-1][j] is computed from the same set, so it should be consistent.
        #            # Actually, we should check: if w + suf[rem_slots-1][j] == current_needed, then choose it.
        #            # But what if there are multiple intervals with same index? We are iterating by original index, so the first one that satisfies is the lexicographically smallest.
        #
        # Implementation details:
        #   Precompute starts for sorted_intervals: starts = [x[1] for x in sorted_intervals]
        #   Precompute suf[5][n]
        #
        # Let's do that.
        
        # Precompute starts for sorted intervals
        starts = [x[1] for x in sorted_intervals]
        
        # Initialize suf[5][n] with 0
        suf = [[0] * (n + 1) for _ in range(5)]
        # suf[k][n] = 0 for all k, meaning no intervals left.
        # Compute for k from 1 to 4, and j from n-1 down to 0.
        for k in range(1, 5):
            for j in range(n - 1, -1, -1):
                r_j, l_j, w_j, orig_j = sorted_intervals[j]
                # Find the first index next_j such that starts[next_j] > r_j
                # Use bisect_right on starts for r_j, then next_j = pos
                pos = bisect.bisect_right(starts, r_j)
                # Then the max weight from next_j to end with k-1 slots is suf[k-1][pos]
                if pos < n:
                    future_val = suf[k-1][pos]
                else:
                    future_val = 0
                candidate = w_j + future_val
                # suf[k][j] = max(suf[k][j+1], candidate)
                suf[k][j] = max(suf[k][j+1], candidate)
        
        # Now reconstruct
        last_end = -1
        rem_slots = 4
        current_needed = max_weight
        result = []
        
        # We need to iterate original indices from 0 to n-1.
        # But to use suf, we need to know the sorted index of the current interval? Actually, no: for the future part, we need the max weight from intervals that start > r, which is independent of the original index. But we are iterating by original index, so we must check the condition for each original interval.
        # However, the suf array is built on the sorted order. But the condition "intervals that start > r" is the same regardless of order. And suf[k][j] is defined as the max weight from sorted_intervals[j:] (which are sorted by end time) using at most k intervals. But note: the set of intervals that start > r is a subset of the entire set, and suf[k][j] for j being the first index with start > r is exactly the max weight from those intervals (because sorted_intervals is sorted by end time, but the condition for non-overlapping only depends on start and end, and the DP for suf is computed correctly for any subset that is contiguous in the sorted order? Actually, no: the intervals that start > r are not necessarily contiguous in the sorted order by end time. 
        #
        # Correction: The suf array is computed for the entire sorted_intervals array. But when we do bisect_right on starts for r_j, we get the first index in the sorted_intervals (which is sorted by end time) such that start > r_j. But the intervals from that index to the end are not necessarily all the intervals that start > r_j? Actually, yes: because starts is an array of the start times of the sorted_intervals (which are sorted by end time). The array "starts" is not sorted! 
        #
        # This is a critical error: the sorted_intervals is sorted by end time, so the starts array is not sorted. Therefore, we cannot use bisect on starts to find intervals with start > r.
        #
        # Alternative approach for reconstruction:
        # Instead of using suf on the sorted order, we can precompute a separate structure: for each possible end value, what is the max weight achievable from intervals that start > end, using at most k slots.
        # But the end values are large (up to 1e9), so we cannot use an array.
        #
        # Revised plan for reconstruction:
        # We can precompute an array "future_max[k][i]" which is the max weight achievable from intervals with original index >= i? But that doesn't help because the non-overlapping condition is on coordinates, not indices.
        #
        # Actually, a better approach for reconstruction is:
        # After computing the DP table (best[k][i] for sorted intervals), we can reconstruct by iterating the sorted intervals in reverse order? But we need lexicographical order of original indices.
        #
        # Standard technique for lexicographical smallest reconstruction:
        #   Iterate original indices from 0 to n-1.
        #   For each interval, check if it can be the next interval in the solution.
        #   To check: 
        #       Let the current interval be i (original index) with [l, r, w].
        #       It must be non-overlapping with the last chosen interval (last_end < l).
        #       Then, the remaining weight needed is current_needed - w.
        #       And we need to check if it is possible to achieve current_needed - w from intervals that start > r, using rem_slots - 1 slots.
        #
        # How to check the "possible" part efficiently?
        #   We can precompute a 2D array: max_future[k][end_val] = max weight achievable from intervals that start > end_val, using at most k slots.
        #   But end_val can be up to 1e9, so we cannot use an array.
        #
        # Instead, we can use the best[k] array from the forward DP, but in reverse? 
        #   Actually, we can compute a "reverse" DP: 
        #       rev_dp[k][i] = max weight achievable from intervals i..n-1 (in sorted order) using at most k slots, with the constraint that the first interval chosen must start after a given end? 
        #   This is complicated.
        #
        # Alternative: 
        #   Precompute for each k (1..4) and for each sorted index i, the value: 
        #       best_from[i][k] = max weight achievable from intervals i..n-1 (in sorted order) using at most k slots, without any constraint on the start of the first interval? 
        #   But then, when we choose an interval j (in sorted order) as the next interval, we need the max weight from intervals that start > end_j. 
        #   And that is not directly stored.
        #
        # Given the complexity, and since n is 5e4 and k is only 4, we can do the following for reconstruction:
        #   Precompute an array "next_best[k][i]" for k=1..4 and i=0..n-1, where next_best[k][i] is the max weight achievable from intervals with sorted index > i (i.e., from i+1 to n-1) using at most k slots, but with the additional constraint that the first interval chosen must start > end_i? 
        #   Actually, no: we need for a given end value r, the max weight from intervals that start > r.
        #
        # We can precompute an array "suf" as described, but using a separate sort by start time? 
        #   Let's create a list of intervals sorted by start time. Then for a given r, we can binary search for the first interval with start > r, and then use a suffix max array on that sorted list.
        #
        # Steps:
        #   1. Create a list of intervals sorted by start time: sorted_by_start = sorted(intervals, key=lambda x: x[0])
        #   2. Precompute a suffix max array for k=1..4 on this sorted_by_start list.
        #      Let suf_start[k][j] = max weight achievable from sorted_by_start[j:] using at most k slots.
        #      How to compute? 
        #          We can use a similar DP as before, but now the intervals are sorted by start time. 
        #          But the non-overlapping condition for the future intervals: when we pick an interval from sorted_by_start[j:], the next interval must start > end of current. 
        #          This is symmetric to the forward DP.
        #
        #   3. Then, for reconstruction:
        #        last_end = -1
        #        rem_slots = 4
        #        current_needed = max_weight
        #        result = []
        #        For idx from 0 to n-1:
        #            l, r, w = intervals[idx]
        #            if l > last_end:
        #                # Find the max weight achievable from intervals that start > r, using rem_slots-1 slots.
        #                # In sorted_by_start, find the first index j such that start > r.
        #                # Then suf_start[rem_slots-1][j] is the max weight from that point.
        #                if w + suf_start[rem_slots-1][j] == current_needed:
        #                    result.append(idx)
        #                    last_end = r
        #                    current_needed -= w
        #                    rem_slots -= 1
        #                    if rem_slots == 0:
        #                        break
        #
        #   This should work.
        #
        # Let's implement this.
        
        # Create sorted_by_start
        sorted_by_start = sorted(intervals, key=lambda x: x[0])
        # Extract starts and ends and weights for sorted_by_start
        starts_bs = [x[0] for x in sorted_by_start]
        ends_bs = [x[1] for x in sorted_by_start]
        weights_bs = [x[2] for x in sorted_by_start]
        n_bs = n
        
        # Precompute suf_start[5][n_bs+1]
        suf_start = [[0] * (n_bs + 1) for _ in range(5)]
        # suf_start[k][j] = max weight from sorted_by_start[j:] using at most k slots.
        # Compute for k=1 to 4, j from n_bs-1 down to 0.
        for k in range(1, 5):
            for j in range(n_bs - 1, -1, -1):
                l_j, r_j, w_j = sorted_by_start[j]
                # Find the first index next_j in sorted_by_start such that start > r_j.
                # Since sorted_by_start is sorted by start, we can use bisect_right on starts_bs for r_j.
                pos = bisect.bisect_right(starts_bs, r_j)
                if pos < n_bs:
                    future_val = suf_start[k-1][pos]
                else:
                    future_val = 0
                candidate = w_j + future_val
                suf_start[k][j] = max(suf_start[k][j+1], candidate)
        
        # Now reconstruct
        last_end = -1
        rem_slots = 4
        current_needed = max_weight
        result = []
        
        for idx in range(n):
            l, r, w = intervals[idx]
            if l > last_end:
                # Find the first index in sorted_by_start with start > r
                pos = bisect.bisect_right(starts_bs, r)
                if pos < n_bs:
                    future_val = suf_start[rem_slots-1][pos]
                else:
                    future_val = 0
                if w + future_val == current_needed:
                    result.append(idx)
                    last_end = r
                    current_needed -= w
                    rem_slots -= 1
                    if rem_slots == 0:
                        break
        
        return result