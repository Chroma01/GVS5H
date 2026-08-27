from typing import List
import bisect

class Solution:
    def maximumWeight(self, intervals: List[List[int]]) -> List[int]:
        n = len(intervals)
        if n == 0:
            return []
        
        # Store intervals with original indices: (l, r, weight, original_index)
        indexed_intervals = [(l, r, w, i) for i, (l, r, w) in enumerate(intervals)]
        
        # Sort by start time for efficient suffix computation
        sorted_intervals = sorted(indexed_intervals, key=lambda x: x[0])
        
        # Map original index to position in sorted_intervals
        pos_in_sorted = [0] * n
        for idx, (l, r, w, orig_idx) in enumerate(sorted_intervals):
            pos_in_sorted[orig_idx] = idx
            
        # Precompute next_start for each position in sorted_intervals
        # next_start[i] = smallest j > i such that sorted_intervals[j][0] > sorted_intervals[i][1]
        # If no such j, -1
        next_start = [-1] * n
        start_times = [x[0] for x in sorted_intervals]
        for i in range(n):
            # Find first j > i such that start_times[j] > sorted_intervals[i][1]
            idx = bisect.bisect_right(start_times, sorted_intervals[i][1], lo=i+1)
            if idx < n:
                next_start[i] = idx
            else:
                next_start[i] = -1
                
        # Precompute S[k][i]: max weight using AT MOST k intervals from sorted_intervals[i:]
        # S[k][i] = max(S[k][i+1], intervals[i].weight + S[k-1][next_start[i]])
        # Initialize with 0
        S = [[0] * (n + 1) for _ in range(5)]
        for k in range(1, 5):
            for i in range(n - 1, -1, -1):
                val_skip = S[k][i+1]
                # If next_start[i] is -1, we use index n (which is 0)
                next_idx = next_start[i] if next_start[i] != -1 else n
                val_pick = sorted_intervals[i][2] + S[k-1][next_idx]
                S[k][i] = max(val_skip, val_pick)
                
        # Global max weight
        W = 0
        for k in range(1, 5):
            W = max(W, S[k][0])
            
        # Prepare for DFS: list of (l, r, original_index) sorted by original index
        intervals_by_orig = [(x[0], x[1], x[3]) for x in indexed_intervals]
        l_by_orig = [x[0] for x in intervals_by_orig]
        
        best_indices = []
        
        def dfs(last_end, count, current_weight, current_indices, start_index):
            nonlocal best_indices
            # If we reached the global max weight, we found the lexicographically smallest set
            # because we iterate in increasing order of original indices.
            if current_weight == W:
                best_indices = current_indices[:]
                return True
            
            if count == 4:
                return False
                
            # Find the first j >= start_index such that intervals_by_orig[j][0] > last_end
            idx = bisect.bisect_right(l_by_orig, last_end, lo=start_index)
            
            # Iterate from idx to n-1
            for j in range(idx, n):
                # Pruning: check if we can still reach W
                # We need to pick at most (4 - count) more intervals.
                # The max weight we can get from there is S[4-count][pos_in_sorted[j]]
                # Note: S[k][i] is "at most k", so this is an upper bound.
                # If current + weight + upper_bound < W, we can't reach W.
                if current_weight + intervals_by_orig[j][2] + S[4-count][pos_in_sorted[j]] < W:
                    continue
                
                # Recurse
                if dfs(intervals_by_orig[j][1], count + 1, current_weight + intervals_by_orig[j][2], 
                      current_indices + [j], j + 1):
                    return True
            
            return False
        
        dfs(0, 0, 0, [], 0)
        return best_indices