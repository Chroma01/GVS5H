import bisect

class Solution:
    def maximumWeight(self, intervals: List[List[int]]) -> List[int]:
        n = len(intervals)
        # Store original indices and sort by end time, then by start time
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
            j = bisect.bisect_right(end_times, sorted_data[i][1])
            if j < n:
                next_non_overlap[i] = j
            else:
                next_non_overlap[i] = n
                
        # dp_forward[k][i] = max weight using at most k intervals from sorted_data[0...i-1]
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
                # bisect_left returns first index where end_times[index] >= l
                # So the interval before that index is the last one with end < l
                p = bisect.bisect_left(end_times, l, 0, i)
                # p is the count of intervals in 0..i-1 that end < l
                # So dp_forward[k-1][p] is the max weight for at most k-1 intervals from first p intervals
                prev_val = dp_forward[k-1][p]
                if prev_val + w > dp_forward[k][i]:
                    dp_forward[k][i] = prev_val + w
                    
        # dp_backward[k][i] = max weight using at most k intervals from sorted_data[i...n-1]
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
                # So we can take at most k-1 intervals from nxt onwards
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