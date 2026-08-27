from bisect import bisect_left
from typing import List, Tuple

class Solution:
    def maximumWeight(self, intervals: List[List[int]]) -> List[int]:
        n = len(intervals)
        # Attach original index, sort by end (r)
        sorted_intervals = sorted(
            ((l, r, w, idx) for idx, (l, r, w) in enumerate(intervals)),
            key=lambda x: x[1]
        )
        ends = [item[1] for item in sorted_intervals]
        
        # dp[k][i] = (weight, indices_tuple) for best using up to k intervals among first i+1 sorted intervals
        # We'll store dp as list of lists of tuples
        # k ranges 0..4
        dp = [[(0, ())] * n for _ in range(5)]
        
        for i in range(n):
            l_i, r_i, w_i, orig_i = sorted_intervals[i]
            # Find predecessor j: last interval with r < l_i
            # bisect_left returns first position where ends[pos] >= l_i
            j = bisect_left(ends, l_i) - 1
            
            for k in range(5):
                # Option 1: skip current interval
                if i > 0:
                    best_weight, best_indices = dp[k][i-1]
                else:
                    best_weight, best_indices = 0, ()
                
                # Option 2: take current interval (if k >= 1)
                if k >= 1 and j >= 0:
                    prev_weight, prev_indices = dp[k-1][j]
                    new_weight = prev_weight + w_i
                    # Build new indices tuple: merge and sort
                    # prev_indices is already sorted, orig_i is a single int
                    # Merge two sorted tuples
                    a = list(prev_indices)
                    b = [orig_i]
                    merged = []
                    ai, bi = 0, 0
                    while ai < len(a) and bi < len(b):
                        if a[ai] < b[bi]:
                            merged.append(a[ai])
                            ai += 1
                        else:
                            merged.append(b[bi])
                            bi += 1
                    merged.extend(a[ai:])
                    merged.extend(b[bi:])
                    new_indices = tuple(merged)
                    
                    # Compare: higher weight wins, if equal weight smaller indices tuple wins
                    if new_weight > best_weight:
                        best_weight, best_indices = new_weight, new_indices
                    elif new_weight == best_weight and new_indices < best_indices:
                        best_indices = new_indices
                elif k >= 1 and j < 0:
                    # No predecessor, just take this one
                    new_weight = w_i
                    new_indices = (orig_i,)
                    if new_weight > best_weight:
                        best_weight, best_indices = new_weight, new_indices
                    elif new_weight == best_weight and new_indices < best_indices:
                        best_indices = new_indices
                
                dp[k][i] = (best_weight, best_indices)
        
        # Find best among k=0..4
        best_weight = -1
        best_indices = None
        for k in range(5):
            w, ind = dp[k][n-1]
            if w > best_weight or (w == best_weight and (best_indices is None or ind < best_indices)):
                best_weight = w
                best_indices = ind
        
        return list(best_indices) if best_indices else []