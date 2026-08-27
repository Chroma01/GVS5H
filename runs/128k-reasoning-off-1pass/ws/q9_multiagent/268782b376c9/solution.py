from typing import List

class Solution:
    def maxScore(self, points: List[int], m: int) -> int:
        # The maximum possible minimum score cannot exceed the maximum value in points.
        # If x > max(points), then for some i, points[i] < x, so gameScore[i] can never reach x.
        # Thus, the answer is bounded by max(points).
        max_val = max(points)
        
        # Binary search for the maximum x such that we can achieve min(gameScore) >= x.
        # Range: [0, max_val]
        low = 0
        high = max_val
        ans = 0
        
        while low <= high:
            mid = (low + high) // 2
            
            if mid == 0:
                # A minimum of 0 is always achievable (do nothing).
                ans = max(ans, mid)
                low = mid + 1
                continue
            
            # Check if it's possible to achieve minimum score 'mid'
            # We must visit every index i at least ceil(mid / points[i]) times.
            # Total moves required:
            # 1. Traverse the entire array from 0 to n-1 (and back if needed, but optimal path covers all).
            #    Starting at -1, to cover [0, n-1] optimally:
            #    Go -1 -> 0 -> ... -> n-1. Cost = (0 - (-1)) + (n-1 - 0) = 1 + n - 1 = n.
            #    This covers every index exactly once.
            # 2. For each index i, if we need k_i visits, we have already done 1.
            #    We need (k_i - 1) extra visits. Each extra visit costs 1 move (oscillate).
            #    Total extra moves = sum(k_i - 1) for all i.
            # Total moves = n + sum(ceil(mid / points[i]) - 1).
            
            n = len(points)
            current_moves = n
            possible = True
            
            for p in points:
                # Calculate visits needed: ceil(mid / p)
                # Using integer arithmetic: (mid + p - 1) // p
                visits = (mid + p - 1) // p
                if visits > 1:
                    current_moves += (visits - 1)
                # Optimization: if current_moves already exceeds m, break
                if current_moves > m:
                    possible = False
                    break
            
            if possible and current_moves <= m:
                ans = mid
                low = mid + 1
            else:
                high = mid - 1
                
        return ans