import bisect
from typing import List

class Solution:
    def maximumWeight(self, intervals: List[List[int]]) -> List[int]:
        n = len(intervals)
        if n == 0:
            return []
        
        # Store intervals as (l, r, weight, original_index)
        # We will sort by l (start time) to facilitate DP and binary search
        sorted_intervals = []
        for i, (l, r, w) in enumerate(intervals):
            sorted_intervals.append((l, r, w, i))
        
        # Sort by start time
        sorted_intervals.sort(key=lambda x: x[0])
        
        # Extract start times for binary search
        start_times = [x[0] for x in sorted_intervals]
        
        # Precompute suffix max weights for k=1 to 4
        # dp[k][i] = max weight using exactly k intervals from sorted_intervals[i:]
        # Dimensions: 5 x (n + 1)
        # Initialize with 0. Since weights are positive, 0 implies no intervals picked or impossible if k>0 and no valid path.
        dp = [[0] * (n + 1) for _ in range(5)]
        
        # Fill DP table backwards
        for k in range(1, 5):
            for i in range(n - 1, -1, -1):
                l, r, w, orig_idx = sorted_intervals[i]
                
                # Option 1: Skip current interval
                skip_val = dp[k][i + 1]
                
                # Option 2: Pick current interval
                # Find first interval starting strictly after r
                # bisect_right gives insertion point after all elements <= r
                idx = bisect.bisect_right(start_times, r, lo=i + 1)
                
                pick_val = 0
                if idx < n:
                    # We need k-1 intervals from idx onwards
                    if k - 1 >= 0:
                        pick_val = w + dp[k - 1][idx]
                
                dp[k][i] = max(skip_val, pick_val)
        
        best_seq = None
        best_weight = -1
        
        # We iterate k from 1 to 4
        for k in range(1, 5):
            max_w_k = dp[k][0]
            
            # If max_w_k is 0 and k > 0, it means no solution exists for this k
            if max_w_k == 0:
                continue
            
            # Create a lookup: original_index -> (l, r, w, sorted_idx)
            orig_to_sorted = {}
            for idx, item in enumerate(sorted_intervals):
                orig_to_sorted[item[3]] = item
            
            current_k_seq = []
            
            # Step 1: Find the smallest original index for the first interval
            found_first = False
            first_orig_idx = -1
            first_s_idx = -1
            
            for orig_idx in range(n):
                if orig_idx not in orig_to_sorted:
                    continue
                item = orig_to_sorted[orig_idx]
                l, r, w, s_idx = item
                
                # Find next start index
                idx = bisect.bisect_right(start_times, r, lo=s_idx + 1)
                
                if idx < n and k > 1:
                    if w + dp[k - 1][idx] == max_w_k:
                        first_orig_idx = orig_idx
                        first_s_idx = s_idx
                        found_first = True
                        break
                elif k == 1:
                    if w == max_w_k:
                        first_orig_idx = orig_idx
                        first_s_idx = s_idx
                        found_first = True
                        break
            
            if not found_first:
                continue
                
            # Step 2: Reconstruct the rest of the sequence
            current_s_idx = first_s_idx
            current_orig_idx = first_orig_idx
            current_end = sorted_intervals[current_s_idx][1]
            current_weight = sorted_intervals[current_s_idx][2]
            
            current_k_seq.append(current_orig_idx)
            
            for _ in range(k - 1):
                remaining_weight = max_w_k - current_weight
                needed_k = k - 1
                
                found_next = False
                next_orig_idx = -1
                next_s_idx = -1
                
                # We need to find the smallest original index j > current_orig_idx
                # such that intervals[j].start > current_end
                # and it can complete the sequence.
                
                for j in range(current_orig_idx + 1, n):
                    if j not in orig_to_sorted:
                        continue
                    item = orig_to_sorted[j]
                    l, r, w, s_idx = item
                    
                    if l <= current_end:
                        continue
                    
                    # Found a candidate that starts after current_end
                    # Check if it can complete the sequence
                    idx = bisect.bisect_right(start_times, r, lo=s_idx + 1)
                    if idx < n and needed_k > 1:
                        if w + dp[needed_k - 1][idx] == remaining_weight - w:
                            next_orig_idx = j
                            next_s_idx = s_idx
                            found_next = True
                            break
                    elif needed_k == 1:
                        if w == remaining_weight - w:
                            next_orig_idx = j
                            next_s_idx = s_idx
                            found_next = True
                            break
                
                if not found_next:
                    break
                
                current_orig_idx = next_orig_idx
                current_s_idx = next_s_idx
                current_end = sorted_intervals[current_s_idx][1]
                current_weight += sorted_intervals[current_s_idx][2]
                current_k_seq.append(current_orig_idx)
            
            # Compare with best_seq
            if best_seq is None:
                best_seq = current_k_seq
                best_weight = max_w_k
            else:
                if max_w_k > best_weight:
                    best_seq = current_k_seq
                    best_weight = max_w_k
                elif max_w_k == best_weight:
                    # Compare lexicographically
                    if current_k_seq < best_seq:
                        best_seq = current_k_seq
                        best_weight = max_w_k
        
        return best_seq