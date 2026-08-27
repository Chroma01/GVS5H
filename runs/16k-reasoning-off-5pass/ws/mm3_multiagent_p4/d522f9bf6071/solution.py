from typing import List
from bisect import bisect_left

class Solution:
    def maximumWeight(self, intervals: List[List[int]]) -> List[int]:
        n = len(intervals)
        if n == 0:
            return []
        
        K = 4
        
        # Pair each interval with its original index and sort by end time
        indexed = [(i, intervals[i][0], intervals[i][1], intervals[i][2]) for i in range(n)]
        indexed.sort(key=lambda x: x[2])  # sort by r (end)
        
        # Extract arrays for binary search
        starts = [x[1] for x in indexed]
        ends = [x[2] for x in indexed]
        weights = [x[3] for x in indexed]
        orig_idx = [x[0] for x in indexed]
        
        # Compute p[i]: the last index (0-based) in sorted order with end < start_i
        p = [-1] * n
        for i in range(n):
            pos = bisect_left(ends, starts[i]) - 1
            p[i] = pos
        
        # DP table: dp[k][i] = best (weight, indices_tuple) using up to k intervals from first i intervals
        dp = [[(0, ()) for _ in range(n + 1)] for _ in range(K + 1)]
        
        # Helper: determine if candidate is better than current
        def is_better(cand, cur):
            wc, ic = cand
            wu, iu = cur
            if wc != wu:
                return wc > wu
            lc = len(ic)
            lu = len(iu)
            if lc != lu:
                return lc < lu
            return ic < iu
        
        # Fill DP
        for i in range(1, n + 1):
            idx = i - 1
            wi = weights[idx]
            oi = orig_idx[idx]
            pi = p[idx]
            
            for k in range(1, K + 1):
                best = dp[k][i - 1]
                
                if pi != -1:
                    prev_dp = dp[k - 1][pi + 1]
                else:
                    prev_dp = dp[k - 1][0]
                
                take_weight = wi + prev_dp[0]
                take_indices = prev_dp[1] + (oi,)
                candidate = (take_weight, take_indices)
                
                if is_better(candidate, best):
                    best = candidate
                
                dp[k][i] = best
        
        result_indices = dp[K][n][1]
        return sorted(result_indices)


# Test cases
if __name__ == "__main__":
    sol = Solution()
    
    # Example 1
    intervals1 = [[1,3,2],[4,5,2],[1,5,5],[6,9,3],[6,7,1],[8,9,1]]
    print("Example 1:", sol.maximumWeight(intervals1), "Expected: [2, 3]")
    
    # Example 2
    intervals2 = [[5,8,1],[6,7,7],[4,7,3],[9,10,6],[7,8,2],[11,14,3],[3,5,5]]
    print("Example 2:", sol.maximumWeight(intervals2), "Expected: [1, 3, 5, 6]")
    
    # Single interval
    print("Single:", sol.maximumWeight([[1,5,10]]), "Expected: [0]")
    
    # Empty
    print("Empty:", sol.maximumWeight([]), "Expected: []")
    
    # Fewer than 4 intervals
    print("Two intervals:", sol.maximumWeight([[1,2,5],[3,4,10]]), "Expected: [0,1]")
    
    # All overlapping (pick max weight, smallest index)
    print("All overlap:", sol.maximumWeight([[1,5,10],[2,6,20],[3,7,15]]), "Expected: [1]")
    
    # Tie-breaking: same weight, shorter list preferred
    # Interval 0: [1,2,10], Interval 1: [3,4,10] -> both length 1 with same weight? No, need same total weight.
    # Two single intervals with same weight, pick smallest index
    print("Same weight singles:", sol.maximumWeight([[1,2,10],[3,4,10]]), "Expected: [0]")
    
    # Tie-breaking: same weight, same length, lex smallest indices
    # Interval 0: [1,2,5], Interval 1: [3,4,5] -> sum=10, indices [0,1] vs maybe [0,1] is only option
    # Let's create: [1,2,5] (idx 0), [3,4,5] (idx 1), [5,6,5] (idx 2) -> all weight 5
    # Best is 2 intervals: weight 10. Options: [0,1], [1,2] (0,1 overlapping? 2<3 ok), [0,2] (2<5 ok)
    # Lex smallest is [0,1]
    print("Three equal weights:", sol.maximumWeight([[1,2,5],[3,4,5],[5,6,5]]), "Expected: [0,1]")
    
    # Boundary: intervals sharing endpoint overlap
    # [1,3] and [3,5] overlap at 3
    print("Boundary overlap:", sol.maximumWeight([[1,3,10],[3,5,20]]), "Expected: [1]")
    
    # Boundary: can pick non-overlapping around
    print("Boundary no overlap:", sol.maximumWeight([[1,2,10],[3,4,20]]), "Expected: [0,1]")
    
    # Large weight tie
    # Intervals: [1,2,100] (0), [3,4,100] (1), [1,4,150] (2)
    # Best is [2] weight 150, or [0,1] weight 200. So [0,1]
    print("Mixed:", sol.maximumWeight([[1,2,100],[3,4,100],[1,4,150]]), "Expected: [0,1]")
    
    # All same start/end
    print("All same:", sol.maximumWeight([[1,5,1],[1,5,2],[1,5,3]]), "Expected: [2]")
    
    # 4 intervals possible
    # [1,2,1],[3,4,1],[5,6,1],[7,8,1] -> all 4
    print("Four non-overlap:", sol.maximumWeight([[1,2,1],[3,4,1],[5,6,1],[7,8,1]]), "Expected: [0,1,2,3]")
    
    # Lex tie with longer list
    # [1,2,5] (0), [3,4,5] (1), [5,6,10] (2) -> weight 20 with all 3, or weight 10 with just [2]
    # All 3 better
    print("Three optimal:", sol.maximumWeight([[1,2,5],[3,4,5],[5,6,10]]), "Expected: [0,1,2]")