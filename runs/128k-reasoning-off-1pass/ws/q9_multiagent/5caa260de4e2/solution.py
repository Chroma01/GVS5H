from typing import List
from collections import deque

class Solution:
    def minimumCost(self, nums: List[int], cost: List[int], k: int) -> int:
        n = len(nums)
        
        # Precompute prefix sums for nums and cost
        # S_nums[i] = sum(nums[0]...nums[i-1])
        # S_cost[i] = sum(cost[0]...cost[i-1])
        S_nums = [0] * (n + 1)
        S_cost = [0] * (n + 1)
        
        for i in range(n):
            S_nums[i+1] = S_nums[i] + nums[i]
            S_cost[i+1] = S_cost[i] + cost[i]
            
        # dp[i] will store min cost to partition prefix of length i into 'm' subarrays
        # Initialize for m=0: cost is 0 for length 0, infinity otherwise
        prev_dp = [float('inf')] * (n + 1)
        prev_dp[0] = 0
        
        # Iterate over the number of subarrays m from 1 to n
        for m in range(1, n + 1):
            curr_dp = [float('inf')] * (n + 1)
            
            # Deque for Convex Hull Trick
            # Stores indices j such that lines y = S_cost[j] * x + prev_dp[j] form the lower hull
            hull = deque()
            
            # We iterate i from 1 to n to compute curr_dp[i]
            # For each i, we can transition from any j < i (specifically j = i-1 is added to hull)
            # The query point x = -(S_nums[i] + m*k) is strictly decreasing as i increases.
            
            for i in range(1, n + 1):
                # Calculate query x value
                K = S_nums[i] + m * k
                x = -K
                
                # Add the line corresponding to j = i-1 to the hull
                # This line becomes available for transitions ending at i and beyond
                new_slope = S_cost[i-1]
                new_intercept = prev_dp[i-1]
                
                # Maintain lower convex hull
                # Slopes are strictly increasing (S_cost is strictly increasing since cost[i] >= 1)
                # We remove lines from the back if the new line makes them redundant
                while len(hull) >= 2:
                    j1 = hull[-2]
                    j2 = hull[-1]
                    c1 = prev_dp[j1]
                    c2 = prev_dp[j2]
                    m1 = S_cost[j1]
                    m2 = S_cost[j2]
                    m_new = new_slope
                    c_new = new_intercept
                    
                    # Check intersection: (c2 - c1)/(m1 - m2) >= (c_new - c2)/(m2 - m_new)
                    # Cross multiply to avoid float issues (denominators are positive)
                    # Note: m1 < m2 < m_new, so (m1-m2) is negative and (m2-m_new) is negative.
                    # Inequality direction is preserved when multiplying by negatives? 
                    # Let's rewrite with positive denominators:
                    # Intersection x1 = (c2 - c1) / (m1 - m2)
                    # Intersection x2 = (c_new - c2) / (m2 - m_new)
                    # We want to remove j2 if x1 >= x2.
                    # (c2 - c1) / (m1 - m2) >= (c_new - c2) / (m2 - m_new)
                    # Since (m1-m2) < 0 and (m2-m_new) < 0, let's multiply by (m1-m2)*(m2-m_new) which is positive.
                    # (c2 - c1) * (m2 - m_new) >= (c_new - c2) * (m1 - m2)
                    if (c2 - c1) * (m2 - m_new) >= (c_new - c2) * (m1 - m2):
                        hull.pop()
                    else:
                        break
                
                hull.append(i - 1)
                
                # Query the hull for the minimum value at x
                # Since x is decreasing, the optimal line moves towards lines with larger slopes (towards the back)
                # We remove lines from the front if the next line gives a better value
                while len(hull) >= 2:
                    j1 = hull[0]
                    j2 = hull[1]
                    m1 = S_cost[j1]
                    c1 = prev_dp[j1]
                    m2 = S_cost[j2]
                    c2 = prev_dp[j2]
                    
                    # If line j2 is better than j1 at current x, j1 is no longer needed
                    if m2 * x + c2 <= m1 * x + c1:
                        hull.popleft()
                    else:
                        break
                
                best_j = hull[0]
                # Calculate min cost
                # Formula: (S_nums[i] + m*k) * S_cost[i] + (prev_dp[best_j] - (S_nums[i] + m*k) * S_cost[best_j])
                term1 = K * S_cost[i]
                term2 = prev_dp[best_j] - K * S_cost[best_j]
                curr_dp[i] = term1 + term2
            
            prev_dp = curr_dp
            
        return int(prev_dp[n])