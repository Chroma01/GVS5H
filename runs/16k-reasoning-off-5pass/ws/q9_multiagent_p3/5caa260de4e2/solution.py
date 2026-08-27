from typing import List
from collections import deque

class Solution:
    def minimumCost(self, nums: List[int], cost: List[int], k: int) -> int:
        n = len(nums)
        
        # Precompute prefix sums for nums and cost
        # P[i] = sum(nums[0]...nums[i-1])
        # C[i] = sum(cost[0]...cost[i-1])
        P = [0] * (n + 1)
        C = [0] * (n + 1)
        for i in range(n):
            P[i+1] = P[i] + nums[i]
            C[i+1] = C[i] + cost[i]
            
        # dp_prev[i] stores the minimum cost to partition the prefix of length i 
        # using exactly (c-1) subarrays.
        # Initialize for c=0: cost is 0 only for prefix 0, infinity otherwise.
        dp_prev = [float('inf')] * (n + 1)
        dp_prev[0] = 0
        
        ans = float('inf')
        
        # We will iterate c from 1 to n (number of subarrays)
        # For each c, we compute dp_curr[i] for i from 1 to n.
        # Transition: dp_curr[i] = min_{0 <= j < i} (dp_prev[j] + (P[i] + k*c) * (C[i] - C[j]))
        # Rewritten: dp_curr[i] = P[i]*C[i] + k*c*C[i] + min_{j < i} (dp_prev[j] - C[j]*(P[i] + k*c))
        # Let line j be: y = m_j * x + b_j
        # where m_j = -C[j]
        #       b_j = dp_prev[j] - C[j] * k * c
        #       x_i = P[i]
        # Constant term added at end: P[i]*C[i] + k*c*C[i]
        
        for c in range(1, n + 1):
            dp_curr = [float('inf')] * (n + 1)
            dq = deque()
            lines = [] # List to store (m, b) for each j added to deque
            
            for i in range(1, n + 1):
                # Add j = i-1 to the structure BEFORE querying for i
                # This is because a subarray can have length 1 (from i-1 to i)
                j = i - 1
                if dp_prev[j] != float('inf'):
                    m = -C[j]
                    b = dp_prev[j] - C[j] * k * c
                    lines.append((m, b))
                    
                    # Add line to deque maintaining convex hull (lower hull)
                    # Slopes m_j = -C[j] are strictly decreasing as j increases (since cost[i] >= 1).
                    # We remove lines from the back that become redundant.
                    while len(dq) >= 2:
                        m2, b2 = lines[dq[-1]]
                        m1, b1 = lines[dq[-2]]
                        m_new, b_new = m, b
                        
                        # Check intersection condition: (b2 - b1)/(m1 - m2) >= (b_new - b2)/(m2 - m_new)
                        # Cross multiply to avoid division: (b2 - b1) * (m2 - m_new) >= (b_new - b2) * (m1 - m2)
                        if (b2 - b1) * (m2 - m_new) >= (b_new - b2) * (m1 - m2):
                            dq.pop()
                        else:
                            break
                    dq.append(j)
                
                # Query for x = P[i]
                x = P[i]
                # Remove lines from front that are no longer optimal
                # Since x (P[i]) is strictly increasing, we can remove lines from the front
                # if the next line gives a smaller or equal value.
                while len(dq) >= 2:
                    j1 = dq[0]
                    j2 = dq[1]
                    m1, b1 = lines[j1]
                    m2, b2 = lines[j2]
                    
                    # If line j2 gives smaller or equal value at x, then j1 is useless
                    if m2 * x + b2 <= m1 * x + b1:
                        dq.popleft()
                    else:
                        break
                
                best_j = dq[0]
                m_best, b_best = lines[best_j]
                val = m_best * x + b_best
                dp_curr[i] = P[i] * C[i] + k * c * C[i] + val
            
            # Update global answer with the cost for partitioning entire array into c subarrays
            if dp_curr[n] < ans:
                ans = dp_curr[n]
            
            # Prepare for next iteration
            dp_prev = dp_curr
            
        return ans