class Solution:
    def minimumIncrements(self, nums: List[int], target: List[int]) -> int:
        n = len(nums)
        k = len(target)
        num_masks = 1 << k
        
        # Precompute min_cost_for_sub[mask]: minimum cost to satisfy all targets in mask
        # using a single nums element.
        # For a fixed mask and a fixed nums[i], the cost is max(cost(i, j) for j in mask)
        # where cost(i, j) = (target[j] - nums[i] % target[j]) % target[j]
        
        min_cost_for_sub = [float('inf')] * num_masks
        
        # For each nums element, compute the cost for each target
        # Then for each mask, compute the max cost for that mask for this nums element
        # and update min_cost_for_sub
        
        # Instead of iterating all masks for each nums (which is 16 * 50000 = 800k, acceptable),
        # we can do:
        for i in range(n):
            # Compute cost for each target for nums[i]
            costs = []
            for j in range(k):
                t = target[j]
                r = nums[i] % t
                c = (t - r) % t
                costs.append(c)
            
            # For each mask, compute the max cost for the targets in the mask
            for mask in range(1, num_masks):
                max_c = 0
                for j in range(k):
                    if mask & (1 << j):
                        if costs[j] > max_c:
                            max_c = costs[j]
                if max_c < min_cost_for_sub[mask]:
                    min_cost_for_sub[mask] = max_c
        
        # DP: dp[mask] = minimum cost to satisfy the subset of targets in mask
        dp = [float('inf')] * num_masks
        dp[0] = 0
        
        # Iterate over all masks from 1 to num_masks-1
        for mask in range(1, num_masks):
            # Iterate over all non-empty submasks of mask
            # We can iterate by: sub = mask; while sub > 0: ...; sub = (sub-1) & mask
            sub = mask
            while sub > 0:
                # The cost to satisfy sub using one nums element is min_cost_for_sub[sub]
                # The remaining targets are mask ^ sub
                prev = mask ^ sub
                if dp[prev] != float('inf'):
                    total = dp[prev] + min_cost_for_sub[sub]
                    if total < dp[mask]:
                        dp[mask] = total
                sub = (sub - 1) & mask
        
        return dp[num_masks - 1]