class Solution:
    def maxProduct(self, nums: List[int], k: int, limit: int) -> int:
        n = len(nums)
        total_sum = sum(nums)
        SHIFT = total_sum
        D_SHIFT = n
        size_s = 2 * total_sum + 1
        
        # dp: key = d_idx * size_s + s_idx, value = max product
        dp = {}
        
        for v in nums:
            new_dp = {}
            # skip existing states
            for key, prod in dp.items():
                if key not in new_dp or new_dp[key] < prod:
                    new_dp[key] = prod
            
            # take v alone (A: d=1, s=v; B: d=-1, s=-v)
            if v <= limit:
                d_idx_a = 1 + D_SHIFT
                s_idx_a = v + SHIFT
                key_a = d_idx_a * size_s + s_idx_a
                if key_a not in new_dp or new_dp[key_a] < v:
                    new_dp[key_a] = v
                
                d_idx_b = -1 + D_SHIFT
                s_idx_b = -v + SHIFT
                key_b = d_idx_b * size_s + s_idx_b
                if key_b not in new_dp or new_dp[key_b] < v:
                    new_dp[key_b] = v
            
            # extend existing states
            for key, prod in dp.items():
                # decode d and s
                d_idx = key // size_s
                s_idx = key % size_s
                d = d_idx - D_SHIFT
                s = s_idx - SHIFT
                
                # add to A
                new_d = d + 1
                new_s = s + v
                new_prod = prod * v
                if new_prod <= limit:
                    nd_idx = new_d + D_SHIFT
                    ns_idx = new_s + SHIFT
                    if 0 <= nd_idx < 2 * n + 1 and 0 <= ns_idx < size_s:
                        nkey = nd_idx * size_s + ns_idx
                        if nkey not in new_dp or new_dp[nkey] < new_prod:
                            new_dp[nkey] = new_prod
                
                # add to B
                new_d = d - 1
                new_s = s - v
                new_prod = prod * v
                if new_prod <= limit:
                    nd_idx = new_d + D_SHIFT
                    ns_idx = new_s + SHIFT
                    if 0 <= nd_idx < 2 * n + 1 and 0 <= ns_idx < size_s:
                        nkey = nd_idx * size_s + ns_idx
                        if nkey not in new_dp or new_dp[nkey] < new_prod:
                            new_dp[nkey] = new_prod
            
            dp = new_dp
        
        # find max product for d=0 or 1, s=k
        ans = -1
        for d_target in [0, 1]:
            d_idx = d_target + D_SHIFT
            s_idx = k + SHIFT
            if 0 <= d_idx < 2 * n + 1 and 0 <= s_idx < size_s:
                key = d_idx * size_s + s_idx
                if key in dp:
                    if dp[key] > ans:
                        ans = dp[key]
        return ans