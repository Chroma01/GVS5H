from typing import List

class Solution:
    def maxScore(self, points: List[int], m: int) -> int:
        # Binary search for the maximum possible minimum value k.
        # The range of possible answers is [0, m].
        # Explanation: Even if all points[i] are 1, the maximum score we can achieve 
        # for any index is m (since we have at most m moves). If points[i] > 1, 
        # the score per move is higher, so the maximum possible minimum score is <= m.
        low = 0
        high = m
        ans = 0
        
        while low <= high:
            mid = (low + high) // 2
            
            if mid == 0:
                # A minimum score of 0 is always achievable with 0 moves.
                ans = max(ans, mid)
                low = mid + 1
                continue
            
            # Check if it's possible to achieve a minimum score of 'mid' for all elements
            # with at most 'm' moves.
            moves_needed = 0
            possible = True
            
            for p in points:
                # Calculate the number of visits required for the current element 
                # to reach a score of at least 'mid'.
                # Since each visit adds 'p' to the score, we need ceil(mid / p) visits.
                # Using integer arithmetic: ceil(a / b) = (a + b - 1) // b
                visits = (mid + p - 1) // p
                moves_needed += visits
                
                # Optimization: If moves_needed exceeds m, this 'mid' is not achievable.
                if moves_needed > m:
                    possible = False
                    break
            
            if possible:
                ans = mid
                low = mid + 1
            else:
                high = mid - 1
                
        return ans