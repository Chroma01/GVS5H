from typing import List

class Solution:
    def minimumCost(self, nums: List[int], cost: List[int], k: int) -> int:
        n = len(nums)
        # Precompute prefix sums for nums and cost
        P = [0] * (n + 1)
        Q = [0] * (n + 1)
        for i in range(n):
            P[i+1] = P[i] + nums[i]
            Q[i+1] = Q[i] + cost[i]
        
        # dp[i] will store a list of tuples (total_cost, num_subarrays)
        # representing Pareto optimal states for prefix i.
        # A state (c1, cnt1) is dominated by (c2, cnt2) if c1 >= c2 and cnt1 >= cnt2.
        # We maintain the list sorted by cost (ascending), and count will be descending.
        dp = [[] for _ in range(n + 1)]
        dp[0].append((0, 0))
        
        for i in range(1, n + 1):
            candidates = []
            # Try all possible start points j for the last subarray
            for j in range(i):
                # Current subarray is nums[j...i-1]
                sum_nums = P[i] - P[j]
                sum_cost = Q[i] - Q[j]
                
                # For each state in dp[j]
                for c_prev, cnt_prev in dp[j]:
                    # The current subarray is the (cnt_prev + 1)-th subarray
                    current_subarray_cost = (sum_nums + k * (cnt_prev + 1)) * sum_cost
                    total_cost = c_prev + current_subarray_cost
                    total_cnt = cnt_prev + 1
                    candidates.append((total_cost, total_cnt))
            
            # Prune candidates to keep only Pareto optimal states
            # Sort by cost ascending, then by count ascending
            candidates.sort(key=lambda x: (x[0], x[1]))
            
            pruned = []
            min_cnt = float('inf')
            # Iterate and keep states that are not dominated
            # Since sorted by cost, a state is dominated if there exists a previous state
            # with cost <= current_cost and count <= current_count.
            # Because we process in increasing cost order, we just need to track the minimum count seen so far.
            for c, cnt in candidates:
                if cnt < min_cnt:
                    pruned.append((c, cnt))
                    min_cnt = cnt
            
            dp[i] = pruned
        
        # The answer is the minimum cost in dp[n]
        return dp[n][0][0]