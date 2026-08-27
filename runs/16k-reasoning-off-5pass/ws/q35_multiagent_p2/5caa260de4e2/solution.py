class Solution:
    def minimumCost(self, nums: List[int], cost: List[int], k: int) -> int:
        n = len(nums)
        
        # Precompute prefix sums for nums and cost
        # P_nums[i] = sum(nums[0]...nums[i-1])
        # P_cost[i] = sum(cost[0]...cost[i-1])
        P_nums = [0] * (n + 1)
        P_cost = [0] * (n + 1)
        
        for i in range(n):
            P_nums[i+1] = P_nums[i] + nums[i]
            P_cost[i+1] = P_cost[i] + cost[i]
            
        # dp[m][i] = min cost to partition first i elements into exactly m subarrays
        # We only need the previous layer (m-1) to compute layer m.
        # Initialize dp for m=1
        # dp_prev[i] corresponds to dp[1][i]
        
        # For m=1, the only subarray is nums[0...i-1], which is the 1st subarray.
        # Cost = (P_nums[i] + k*1) * (P_cost[i] - P_cost[0])
        # dp_prev[i] = (P_nums[i] + k) * P_cost[i]
        
        dp_prev = [float('inf')] * (n + 1)
        for i in range(1, n + 1):
            dp_prev[i] = (P_nums[i] + k) * P_cost[i]
            
        # We'll store the final answer as min over all m of dp[m][n]
        ans = dp_prev[n]
        
        # For m from 2 to n
        for m in range(2, n + 1):
            dp_curr = [float('inf')] * (n + 1)
            
            # We want to compute dp_curr[i] for i from m to n
            # dp_curr[i] = min_{j from m-1 to i-1} { dp_prev[j] + (P_nums[i] + k*m) * (P_cost[i] - P_cost[j]) }
            # Let A = P_nums[i] + k*m
            # Let B = P_cost[i]
            # Term = dp_prev[j] + A * (B - P_cost[j])
            #      = A * B + (dp_prev[j] - A * P_cost[j])
            # For a fixed m, as i increases, A increases.
            # The term to minimize over j is: dp_prev[j] - A * P_cost[j]
            # This is a line: y = m_j * x + c_j, where x = A, m_j = -P_cost[j], c_j = dp_prev[j]
            # We want min_y for a given x.
            
            # Since A is increasing with i, and slopes -P_cost[j] are decreasing with j (because P_cost is increasing),
            # we can use a monotonic queue for CHT.
            
            # Lines are added in order of j from m-1 to n-1.
            # Slopes: -P_cost[j] are strictly decreasing (since cost[i] >= 1, P_cost is strictly increasing).
            # Queries: x = P_nums[i] + k*m are strictly increasing with i.
            
            # CHT using a deque
            from collections import deque
            dq = deque()
            
            # Helper to check if line l2 is better than l1 at intersection with l3
            # We maintain lower hull.
            # Line l: y = m*x + c
            # Intersection of l1 and l2: x = (c2 - c1) / (m1 - m2)
            # l2 is redundant if intersection(l1, l2) >= intersection(l2, l3)
            
            def is_redundant(l1, l2, l3):
                # l1, l2, l3 are tuples (m, c)
                # Check if l2 is above or at the intersection of l1 and l3
                # (c2 - c1)/(m1 - m2) >= (c3 - c2)/(m2 - m3)
                # Cross multiply to avoid division
                # (c2 - c1) * (m2 - m3) >= (c3 - c2) * (m1 - m2)
                return (l2[1] - l1[1]) * (l2[0] - l3[0]) >= (l3[1] - l2[1]) * (l1[0] - l2[0])
            
            # Add lines for j from m-1 to n-1
            # But we add them one by one as we iterate i? 
            # Actually, for a fixed m, we can add all valid j lines first, then query for all i.
            # But the query x depends on i, and the lines depend on j.
            # Since both x and the set of lines are fixed for a given m, we can build the hull first.
            
            # However, note that for dp_curr[i], j can range from m-1 to i-1.
            # So when computing dp_curr[i], we can only use lines from j < i.
            # Since we iterate i from m to n, we can add line for j = i-1 before querying for i?
            # No, j goes up to i-1. So for i=m, j can only be m-1.
            # For i=m+1, j can be m-1, m.
            # So we can add lines incrementally.
            
            # Clear deque
            dq.clear()
            
            # We'll iterate i from m to n
            # Before processing i, add line for j = i-1 to the CHT structure.
            # But wait, for i=m, we need line for j=m-1.
            # So we can add line for j=m-1 before the loop, then for each i, add line for j=i-1? 
            # No, for i=m, we add j=m-1. Then query for i=m.
            # For i=m+1, we add j=m. Then query for i=m+1.
            
            # Add line for j = m-1
            # Line: m_j = -P_cost[m-1], c_j = dp_prev[m-1]
            # But dp_prev[m-1] must be valid. It is, since we computed dp_prev for all indices.
            
            # Actually, let's just add lines as we go.
            # For i from m to n:
            #   j_candidate = i - 1
            #   Add line for j_candidate to dq
            #   Query dq for x = P_nums[i] + k*m
            #   dp_curr[i] = A * B + min_val
            
            # But we need to add lines in order of decreasing slope.
            # Slopes are -P_cost[j]. As j increases, P_cost[j] increases, so slope decreases.
            # So adding lines for j = m-1, m, m+1, ... is in decreasing slope order. Correct.
            
            # Add line for j = m-1
            j_start = m - 1
            # Line for j_start
            m_line = -P_cost[j_start]
            c_line = dp_prev[j_start]
            dq.append((m_line, c_line))
            
            for i in range(m, n + 1):
                # Add line for j = i - 1
                j_add = i - 1
                if j_add > j_start:
                    m_new = -P_cost[j_add]
                    c_new = dp_prev[j_add]
                    
                    # Maintain lower hull
                    while len(dq) >= 2:
                        l1 = dq[-2]
                        l2 = dq[-1]
                        l3 = (m_new, c_new)
                        if is_redundant(l1, l2, l3):
                            dq.pop()
                        else:
                            break
                    dq.append((m_new, c_new))
                
                # Query for x = P_nums[i] + k * m
                x = P_nums[i] + k * m
                
                # Remove lines from front that are not optimal for current x
                # Since x is increasing, the optimal line moves to the right (lower slope)
                while len(dq) >= 2:
                    l1 = dq[0]
                    l2 = dq[1]
                    # If l2 gives lower value than l1 at x, pop l1
                    # l1: y1 = m1*x + c1
                    # l2: y2 = m2*x + c2
                    if l1[0] * x + l1[1] >= l2[0] * x + l2[1]:
                        dq.popleft()
                    else:
                        break
                        
                best_line = dq[0]
                min_val = best_line[0] * x + best_line[1]
                
                A = x
                B = P_cost[i]
                dp_curr[i] = A * B + min_val
                
            dp_prev = dp_curr
            ans = min(ans, dp_prev[n])
            
        return ans