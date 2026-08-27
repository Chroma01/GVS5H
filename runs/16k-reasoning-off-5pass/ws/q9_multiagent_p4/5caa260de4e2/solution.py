from typing import List

class Solution:
    def minimumCost(self, nums: List[int], cost: List[int], k: int) -> int:
        n = len(nums)
        # Precompute prefix sums
        # P_num[i] = sum(nums[0]...nums[i-1])
        # P_cost[i] = sum(cost[0]...cost[i-1])
        P_num = [0] * (n + 1)
        P_cost = [0] * (n + 1)
        
        for i in range(n):
            P_num[i+1] = P_num[i] + nums[i]
            P_cost[i+1] = P_cost[i] + cost[i]
            
        # dp[i] will store a list of tuples (num_segments, min_cost) for prefix i
        # We prune the list to keep only non-dominated states:
        # If we have (c1, v1) and (c2, v2) with c1 < c2 and v1 <= v2, then (c2, v2) is dominated.
        # So we keep states where c increases and v strictly decreases.
        dp = []
        
        # Base case: 0 elements, 0 segments, 0 cost
        dp.append([(0, 0)])
        
        for i in range(1, n + 1):
            current_states = []
            
            # Try all possible start positions j for the last subarray (nums[j...i-1])
            # j ranges from 0 to i-1
            for j in range(i):
                if not dp[j]:
                    continue
                
                sum_nums_seg = P_num[i] - P_num[j]
                sum_cost_seg = P_cost[i] - P_cost[j]
                
                # We want to minimize: v + c * (k * sum_cost_seg)
                # Let slope = k * sum_cost_seg
                slope = k * sum_cost_seg
                
                states_j = dp[j]
                
                # Ternary search for the minimum of v + c * slope
                # The function f(c) = v(c) + c * slope is convex-like because v(c) is strictly decreasing
                # and the trade-off curve typically forms a convex shape.
                
                low = 0
                high = len(states_j) - 1
                
                while high - low > 2:
                    m1 = low + (high - low) // 3
                    m2 = high - (high - low) // 3
                    
                    val1 = states_j[m1][1] + states_j[m1][0] * slope
                    val2 = states_j[m2][1] + states_j[m2][0] * slope
                    
                    if val1 < val2:
                        high = m2
                    else:
                        low = m1
                
                best_val = float('inf')
                best_idx = -1
                
                # Check the small range [low, high] to find the exact minimum
                for idx in range(low, high + 1):
                    val = states_j[idx][1] + states_j[idx][0] * slope
                    if val < best_val:
                        best_val = val
                        best_idx = idx
                
                if best_idx != -1:
                    c_val = states_j[best_idx][0]
                    v_val = states_j[best_idx][1]
                    
                    # Calculate total cost for the new segment
                    # Cost = (sum_nums_seg + k * (c_val + 1)) * sum_cost_seg
                    # Total = v_val + Cost
                    new_cost = v_val + (sum_nums_seg + k * (c_val + 1)) * sum_cost_seg
                    new_c = c_val + 1
                    
                    current_states.append((new_c, new_cost))
            
            # Prune current_states
            # Sort by c (number of segments)
            current_states.sort(key=lambda x: x[0])
            
            pruned = []
            min_v = float('inf')
            for c, v in current_states:
                if v < min_v:
                    pruned.append((c, v))
                    min_v = v
            
            dp.append(pruned)
        
        # The answer is the minimum cost in dp[n]
        return min(v for c, v in dp[n])