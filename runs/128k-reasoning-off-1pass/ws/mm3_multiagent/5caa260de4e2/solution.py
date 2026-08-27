from collections import deque
from typing import List

class Solution:
    def minimumCost(self, nums: List[int], cost: List[int], k: int) -> int:
        n = len(nums)
        # Prefix sums
        P = [0] * (n + 1)
        C = [0] * (n + 1)
        for i in range(n):
            P[i+1] = P[i] + nums[i]
            C[i+1] = C[i] + cost[i]
        
        INF = 10**18
        # dp_prev[i] = minimum cost to partition first i elements into g-1 subarrays
        dp_prev = [INF] * (n + 1)
        dp_prev[0] = 0  # base case: 0 elements, 0 cost, 0 subarrays
        
        ans = INF
        for g in range(1, n + 1):
            hull = deque()
            # Add line for j=0 if it represents a valid state
            if dp_prev[0] < INF:
                hull.append((0, 0))  # slope = -C[0] = 0, intercept = dp_prev[0] - C[0]*k*g = 0
            
            dp_curr = [INF] * (n + 1)
            for i in range(1, n + 1):
                if hull:
                    x = P[i]
                    # Query: while the first line is worse than the second, pop it
                    while len(hull) >= 2:
                        m1, b1 = hull[0]
                        m2, b2 = hull[1]
                        if m1 * x + b1 >= m2 * x + b2:
                            hull.popleft()
                        else:
                            break
                    m, b = hull[0]
                    val = m * x + b
                    dp_curr[i] = (P[i] + k * g) * C[i] + val
                
                # Add line for j=i based on dp_prev[i] for future queries
                if dp_prev[i] < INF:
                    new_m = -C[i]
                    new_b = dp_prev[i] - C[i] * k * g
                    # Maintain the lower convex hull
                    while len(hull) >= 2:
                        m1, b1 = hull[-2]
                        m2, b2 = hull[-1]
                        m3, b3 = new_m, new_b
                        # Remove m2 if intersection(m1,m2) >= intersection(m2,m3)
                        if (b2 - b1) * (m2 - m3) >= (b3 - b2) * (m1 - m2):
                            hull.pop()
                        else:
                            break
                    hull.append((new_m, new_b))
            
            ans = min(ans, dp_curr[n])
            dp_prev = dp_curr
        
        return ans