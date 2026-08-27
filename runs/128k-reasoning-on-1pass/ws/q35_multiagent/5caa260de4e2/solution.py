from collections import deque
from typing import List

class Solution:
    def minimumCost(self, nums: List[int], cost: List[int], k: int) -> int:
        n = len(nums)
        # Prefix sums for nums and cost
        P = [0] * (n + 1)
        C = [0] * (n + 1)
        for i in range(n):
            P[i+1] = P[i] + nums[i]
            C[i+1] = C[i] + cost[i]
            
        INF = 10**18
        # dp[j] stores the minimum cost to partition prefix nums[0...j-1] into i subarrays
        dp = [INF] * (n + 1)
        dp[0] = 0
        
        ans = INF
        
        # Iterate over the number of subarrays i from 1 to n
        for i in range(1, n + 1):
            new_dp = [INF] * (n + 1)
            hull = deque()
            
            # Add the initial line corresponding to l = i-1
            if dp[i-1] != INF:
                # Line equation: y = m*x + b, where m = -C[l], b = dp[i-1][l]
                hull.append((-C[i-1], dp[i-1]))
                
            for j in range(i, n + 1):
                # Query point x = P[j] + k * i
                x = P[j] + k * i
                
                # Remove lines from the front that are no longer optimal
                while len(hull) >= 2:
                    m0, b0 = hull[0]
                    m1, b1 = hull[1]
                    # If line 0 is worse than line 1 at x, remove line 0
                    if x * (m0 - m1) >= b1 - b0:
                        hull.popleft()
                    else:
                        break
                        
                # Get the minimum value from the best line
                best = hull[0][0] * x + hull[0][1]
                new_dp[j] = x * C[j] + best
                
                # Add a new line for l = j to the hull for future queries in this i-loop
                if j < n and dp[j] != INF:
                    m, b = -C[j], dp[j]
                    # Maintain the lower convex hull by removing redundant lines from the back
                    while len(hull) >= 2:
                        m0, b0 = hull[-2]
                        m1, b1 = hull[-1]
                        # Check if line 1 is redundant
                        if (b1 - b0) * (m1 - m) >= (b - b1) * (m0 - m1):
                            hull.pop()
                        else:
                            break
                    hull.append((m, b))
                    
            dp = new_dp
            # Track the minimum cost across all possible numbers of subarrays
            ans = min(ans, dp[n])
            
        return ans