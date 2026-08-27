class Solution:
    def minimumIncrements(self, nums: List[int], target: List[int]) -> int:
        n_nums = len(nums)
        n_target = len(target)
        
        # Precompute cost[t_idx][n_idx] = cost to make nums[n_idx] a multiple of target[t_idx]
        # cost = ceil(nums[n_idx] / target[t_idx]) * target[t_idx] - nums[n_idx]
        # which is equivalent to: (target[t_idx] - nums[n_idx] % target[t_idx]) % target[t_idx]
        cost_matrix = [[0] * n_nums for _ in range(n_target)]
        for t_idx in range(n_target):
            t = target[t_idx]
            for n_idx in range(n_nums):
                n = nums[n_idx]
                remainder = n % t
                if remainder == 0:
                    cost_matrix[t_idx][n_idx] = 0
                else:
                    cost_matrix[t_idx][n_idx] = t - remainder
        
        # dp[mask] = minimum cost to cover the set of targets in mask
        # mask is a bitmask where bit i is set if target[i] is covered
        INF = float('inf')
        dp = [INF] * (1 << n_target)
        dp[0] = 0
        
        # Iterate over all masks
        for mask in range(1, 1 << n_target):
            # Try all submasks of mask
            # For each submask, try to cover it with a single nums element
            sub = mask
            while sub > 0:
                # For the current submask, find the minimum cost to cover all targets in sub using one nums element
                # We need to compute LCM of targets in sub, then find min cost over all nums elements
                # But computing LCM for each submask might be expensive? With n_target <= 4, it's fine.
                
                # Extract targets in sub
                targets_in_sub = []
                for i in range(n_target):
                    if sub & (1 << i):
                        targets_in_sub.append(target[i])
                
                # Compute LCM of targets_in_sub
                from math import gcd
                lcm_val = 1
                for t in targets_in_sub:
                    lcm_val = lcm_val * t // gcd(lcm_val, t)
                
                # For each nums element, compute cost to make it a multiple of lcm_val
                min_cost_for_sub = INF
                for n_idx in range(n_nums):
                    n = nums[n_idx]
                    remainder = n % lcm_val
                    if remainder == 0:
                        c = 0
                    else:
                        c = lcm_val - remainder
                    if c < min_cost_for_sub:
                        min_cost_for_sub = c
                
                # Update dp[mask]
                prev_mask = mask ^ sub
                if dp[prev_mask] != INF:
                    new_cost = dp[prev_mask] + min_cost_for_sub
                    if new_cost < dp[mask]:
                        dp[mask] = new_cost
                
                sub = (sub - 1) & mask
        
        return dp[(1 << n_target) - 1]