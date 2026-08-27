from typing import List
import bisect

class Solution:
    def maximumWeight(self, intervals: List[List[int]]) -> List[int]:
        n = len(intervals)
        if n == 0:
            return []
        
        # Store original indices to reconstruct the answer
        # Format: (l, r, w, original_index)
        indexed_intervals = []
        for i in range(n):
            indexed_intervals.append((intervals[i][0], intervals[i][1], intervals[i][2], i))
        
        # Sort by right endpoint (r_i) primarily, then by left endpoint (l_i) secondarily
        # This order is crucial for DP: if we pick interval i, the next interval must start > r_i.
        # Sorting by r_i allows us to process intervals in an order where "future" intervals
        # are always those with r_j >= r_i.
        sorted_by_end = sorted(indexed_intervals, key=lambda x: (x[1], x[0]))
        
        # Extract r_values for binary search in the forward DP
        r_values = [x[1] for x in sorted_by_end]
        
        # dp[k][i] will store the maximum weight of choosing exactly k intervals 
        # from the first i+1 intervals in the sorted list (indices 0 to i).
        # k ranges from 0 to 4.
        dp = [[0] * n for _ in range(5)]
        
        # Fill DP table
        for i in range(n):
            l, r, w, orig_idx = sorted_by_end[i]
            
            # For k=1, we can just take the current interval or inherit from previous
            prev = dp[1][i-1] if i > 0 else 0
            dp[1][i] = max(prev, w)
            
            # For k > 1, we try to extend a solution of k-1 intervals.
            # We need the best solution of k-1 intervals that ends strictly before l.
            # Since our array is sorted by r, we need to find the largest index j < i
            # such that sorted_by_end[j].r < l.
            # bisect_left returns the first index where r_values[idx] >= l.
            # So all indices < idx satisfy r_values < l.
            idx = bisect.bisect_left(r_values, l)
            
            if idx > 0:
                # We can extend from any j in [0, idx-1]
                # The max weight is dp[k-1][idx-1] because dp[k-1] is non-decreasing with i
                best_prev = dp[k-1][idx-1]
                current_val = best_prev + w
                prev_val = dp[k][i-1] if i > 0 else 0
                dp[k][i] = max(prev_val, current_val)
            else:
                # Cannot form k intervals ending at i (no valid previous interval)
                if i > 0:
                    dp[k][i] = dp[k][i-1]
                # else remains 0
        
        # Determine the maximum possible weight for each k
        max_weights = [0] * 5
        for k in range(1, 5):
            max_weights[k] = dp[k][n-1]
        
        global_max = max(max_weights[1:])
        
        # Identify all k that achieve global_max
        valid_counts = [k for k in range(1, 5) if max_weights[k] == global_max]
        
        # Prepare for reconstruction: Sort by start time
        # Format: (l, r, w, original_index)
        sorted_by_start = sorted(indexed_intervals, key=lambda x: (x[0], x[1]))
        l_values_start = [x[0] for x in sorted_by_start]
        
        # dp_start_suffix[k][i] = max weight of k intervals chosen from sorted_by_start[i:]
        # such that they are non-overlapping.
        # Transition: 
        #   Option 1: Skip i -> dp_start_suffix[k][i+1]
        #   Option 2: Pick i as the FIRST interval (in time). 
        #             Then we need k-1 intervals from the set { x | x.l > i.r }.
        #             So we need k-1 intervals from sorted_by_start starting after i.r.
        #             Find next_idx such that l_values_start[next_idx] > i.r.
        #             Then val = w + dp_start_suffix[k-1][next_idx].
        
        dp_start_suffix = [[0] * (n + 1) for _ in range(5)]
        
        for k in range(1, 5):
            for i in range(n - 1, -1, -1):
                l, r, w, orig_idx = sorted_by_start[i]
                
                # Option 1: Skip i
                res = dp_start_suffix[k][i+1]
                
                # Option 2: Pick i as first
                # Find next_idx such that l_values_start[next_idx] > r
                idx = bisect.bisect_right(l_values_start, r)
                # idx is the first index where l > r.
                if idx < n:
                    val = w + dp_start_suffix[k-1][idx]
                    if val > res:
                        res = val
                dp_start_suffix[k][i] = res
        
        # Reconstruction
        # We want the lexicographically smallest list of ORIGINAL indices.
        # We iterate through possible counts k in valid_counts.
        # For a fixed k, we try to build the solution by picking intervals with the smallest original indices.
        
        best_solution = None
        
        # Create a list of intervals in original order for iteration
        intervals_by_orig = []
        for i in range(n):
            intervals_by_orig.append((intervals[i][0], intervals[i][1], intervals[i][2], i))
            
        for k in valid_counts:
            current_time = -1
            current_weight = 0
            chosen = []
            rem_k = k
            rem_w = global_max
            possible = True
            
            # We need to iterate through original indices 0..n-1
            for u in intervals_by_orig:
                l, r, w, orig_idx = u
                if l > current_time:
                    # Check if we can complete the set
                    # We need (rem_k - 1) intervals starting > u.r
                    # Find idx in sorted_by_start such that sorted_by_start[idx].l > u.r
                    idx = bisect.bisect_right(l_values_start, r)
                    
                    if idx < n:
                        needed = w + dp_start_suffix[rem_k-1][idx]
                        if needed == rem_w:
                            chosen.append(orig_idx)
                            current_time = r
                            current_weight += w
                            rem_k -= 1
                            rem_w -= w
                            if rem_k == 0:
                                possible = True
                                break
                    else:
                        # No more intervals can be picked starting after r
                        pass
            
            if possible:
                if best_solution is None:
                    best_solution = chosen
                else:
                    # Lexicographical comparison
                    if chosen < best_solution:
                        best_solution = chosen
        
        return best_solution if best_solution else []