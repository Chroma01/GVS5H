import bisect
from typing import List

class Solution:
    def maximumWeight(self, intervals: List[List[int]]) -> List[int]:
        n = len(intervals)
        
        # Augment intervals with their original indices and sort by end point.
        # Each element is (r, l, weight, original_index).
        sorted_intervals = sorted([(r, l, w, i) for i, (l, r, w) in enumerate(intervals)])
        
        # Extract end points for binary search.
        ends = [iv[0] for iv in sorted_intervals]
        
        # Precompute predecessors. p[i] is the 1-based index of the rightmost interval
        # that ends before sorted_intervals[i-1] starts.
        p = [0] * (n + 1)
        for i in range(1, n + 1):
            # The interval being considered is sorted_intervals[i-1].
            # Its start time is at index 1 of the tuple.
            start_time = sorted_intervals[i-1][1]
            # Find the insertion point for start_time in ends.
            # bisect_left finds the first element >= start_time. We need the last element < start_time.
            # The number of such elements is the insertion point index.
            p[i] = bisect.bisect_left(ends, start_time, 0, i - 1)

        # dp[i][k] stores a tuple: (max_score, lexicographically_smallest_path)
        # considering the first i sorted intervals and choosing at most k.
        dp = [[(0, []) for _ in range(5)] for _ in range(n + 1)]

        for i in range(1, n + 1):
            # Current interval info (1-based index i)
            r_i, l_i, w_i, original_idx_i = sorted_intervals[i-1]
            
            for k in range(1, 5):
                # Option 1: Don't include the i-th interval.
                # The result is the same as for the first i-1 intervals.
                score1, path1 = dp[i-1][k]

                # Option 2: Include the i-th interval.
                # We must find the best solution for the first p[i] intervals with k-1 choices.
                prev_score, prev_path = dp[p[i]][k-1]
                score2 = prev_score + w_i
                
                # The new path is the previous path plus the current interval's original index.
                # The path must be sorted to maintain canonical lexicographical order.
                path2 = sorted(prev_path + [original_idx_i])

                # Compare the two options to find the better one.
                # A solution is better if its score is higher, or if scores are equal
                # and its path is lexicographically smaller.
                if score1 > score2:
                    dp[i][k] = (score1, path1)
                elif score2 > score1:
                    dp[i][k] = (score2, path2)
                else:  # Scores are equal
                    if path1 < path2:
                        dp[i][k] = (score1, path1)
                    else:
                        dp[i][k] = (score2, path2)
        
        # The final answer is the best among dp[n][1], dp[n][2], dp[n][3], dp[n][4].
        # We initialize with the k=0 case (score 0, empty path).
        best_score, best_path = 0, []
        for k in range(1, 5):
            current_score, current_path = dp[n][k]
            if current_score > best_score:
                best_score, best_path = current_score, current_path
            elif current_score == best_score:
                if current_path < best_path:
                    best_path = current_path
        
        return best_path