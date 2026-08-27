from math import ceil
from typing import List

class Solution:
    def maxScore(self, points: List[int], m: int) -> int:
        n = len(points)
        
        # Helper function to check if a minimum score of 'x' is achievable
        def check(x: int) -> bool:
            # Calculate required visits for each index
            # req[i] = ceil(x / points[i])
            # We need to find the range [L, R] of indices that need visits
            # and the total number of visits K
            
            k = 0
            l = -1
            r = -1
            
            # Using integer arithmetic for ceil: (x + points[i] - 1) // points[i]
            for i in range(n):
                req = (x + points[i] - 1) // points[i]
                if req > 0:
                    k += req
                    if l == -1:
                        l = i
                    r = i
            
            if k == 0:
                return True
            
            # Calculate minimum moves
            # Case 1: The total visits K is small enough that we just traverse once
            # from -1 to R (covering L to R).
            # The path -1 -> L -> ... -> R visits every node in [L, R] exactly once.
            # Number of visits provided = R - L + 1.
            # Cost = R - (-1) = R + 1.
            
            # Case 2: We need more visits. We must oscillate between L and R.
            # The formula derived is: cost = K + (R - L) - 1
            
            if k <= (r - l + 1):
                cost = r + 1
            else:
                cost = k + (r - l) - 1
                
            return cost <= m

        # Binary search for the maximum x
        # Lower bound: 0
        # Upper bound: m * max(points) is a safe upper bound.
        # Max points[i] is 10^6, m is 10^9. Max possible score is 10^15.
        
        low = 0
        high = m * max(points) if points else 0
        ans = 0
        
        while low <= high:
            mid = (low + high) // 2
            if check(mid):
                ans = mid
                low = mid + 1
            else:
                high = mid - 1
                
        return ans