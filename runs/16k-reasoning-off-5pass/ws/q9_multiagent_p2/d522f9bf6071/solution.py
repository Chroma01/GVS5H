from typing import List
import bisect

class Solution:
    def maximumWeight(self, intervals: List[List[int]]) -> List[int]:
        n = len(intervals)
        if n == 0:
            return []
        
        # Coordinate compression
        # We need points: l_i and r_i + 1
        points = set()
        for l, r, w in intervals:
            points.add(l)
            points.add(r + 1)
        sorted_points = sorted(list(points))
        point_to_idx = {p: i for i, p in enumerate(sorted_points)}
        m = len(sorted_points)
        
        # dp[k][t_idx] = max weight using k intervals from intervals starting >= sorted_points[t_idx]
        # k ranges from 0 to 4
        dp = [[0] * m for _ in range(5)]
        
        # Pre-group intervals by start time for O(1) access during DP
        intervals_by_start = [[] for _ in range(m)]
        for i, (l, r, w) in enumerate(intervals):
            if l in point_to_idx:
                idx = point_to_idx[l]
                intervals_by_start[idx].append((i, r, w))
        
        # Fill DP table
        # Iterate backwards through time points
        for t_idx in range(m - 1, -1, -1):
            start_time = sorted_points[t_idx]
            
            # Determine next_t_idx
            if t_idx < m - 1:
                next_t_idx = t_idx + 1
            else:
                next_t_idx = m # Represents infinity, dp[k][m] = 0
            
            # Option 1: Pick no interval starting exactly at this time point (carry over from next)
            # This effectively means we skip all intervals starting at 'start_time' and look further right.
            for k in range(5):
                dp[k][t_idx] = dp[k][next_t_idx]
            
            # Option 2: Pick an interval starting at this time point
            for i, r, w in intervals_by_start[t_idx]:
                for k in range(1, 5):
                    if next_t_idx < m:
                        val = w + dp[k-1][next_t_idx]
                        if val > dp[k][t_idx]:
                            dp[k][t_idx] = val
                    else:
                        # If next_t_idx is m, we can only pick this interval if k=1
                        if k == 1:
                            val = w
                            if val > dp[k][t_idx]:
                                dp[k][t_idx] = val
        
        # Helper to reconstruct lexicographically smallest array for a given k and start time
        def get_lexicographically_smallest(k, start_time):
            if k == 0:
                return []
            
            # Find the index in sorted_points corresponding to start_time
            # start_time is guaranteed to be in points set if it comes from r+1 or initial l
            # However, if start_time is larger than any point, we handle it.
            idx = bisect.bisect_left(sorted_points, start_time)
            if idx < m and sorted_points[idx] == start_time:
                t_idx = idx
            else:
                # If start_time is not found, it means no intervals can start >= start_time
                return None
            
            # If dp[k][t_idx] is 0 (and weights are positive), then no solution exists for this k
            if dp[k][t_idx] == 0:
                return None
            
            # We need to find the smallest index i such that:
            # 1. intervals[i].l >= start_time
            # 2. weight[i] + dp[k-1][next_t_idx] == dp[k][t_idx]
            # where next_t_idx is the index of the smallest point > intervals[i].r
            
            # Iterate i from 0 to n-1 to find the lexicographically smallest first element
            for i in range(n):
                l, r, w = intervals[i]
                if l >= start_time:
                    # Check if this interval can be part of an optimal solution
                    # We need to look up dp[k-1] at the time corresponding to r + 1
                    if r + 1 in point_to_idx:
                        next_t_idx = point_to_idx[r + 1]
                    else:
                        # Should not happen if r+1 is in points set, which it is by construction
                        next_t_idx = m
                    
                    if next_t_idx < m:
                        current_val = w + dp[k-1][next_t_idx]
                    else:
                        current_val = w
                    
                    if current_val == dp[k][t_idx]:
                        # Found the smallest index i
                        # Recursively find the rest
                        rest = get_lexicographically_smallest(k - 1, r + 1)
                        if rest is not None:
                            return [i] + rest
            
            return None

        # We need to consider all possible start times?
        # Actually, the global maximum weight is max(dp[k][0] for k in 1..4).
        # But we need the lexicographically smallest array among ALL solutions with that max weight.
        # A solution is defined by its indices.
        # We can iterate k from 1 to 4.
        # For a fixed k, the maximum weight is dp[k][0] (since 0 corresponds to min(l_i) or the smallest point).
        # Wait, sorted_points[0] is the minimum l_i. So dp[k][0] is the max weight using k intervals from the whole set.
        # So for each k, the max weight is dp[k][0].
        # We collect all (weight, solution) pairs for k=1..4.
        # Then we pick the one with max weight. If ties, pick lexicographically smallest solution.
        
        candidates = []
        for k in range(1, 5):
            w = dp[k][0]
            if w > 0:
                sol = get_lexicographically_smallest(k, sorted_points[0])
                if sol is not None:
                    candidates.append((w, sol))
        
        # Sort candidates: primary key weight (desc), secondary key solution (asc)
        # Python's sort is stable, but we want max weight first.
        # We can sort by (-weight, solution)
        candidates.sort(key=lambda x: (-x[0], x[1]))
        
        if candidates:
            return candidates[0][1]
        return []