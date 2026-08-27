from typing import List

class Solution:
    def minOperations(self, nums: List[int], x: int, k: int) -> int:
        n = len(nums)
        if k * x > n:
            return -1
        
        # Coordinate Compression
        sorted_unique = sorted(list(set(nums)))
        rank_map = {val: i + 1 for i, val in enumerate(sorted_unique)}
        m = len(sorted_unique)
        
        # BIT for counts
        bit_count = [0] * (m + 1)
        # BIT for sums
        bit_sum = [0] * (m + 1)
        
        def update(bit, idx, val):
            while idx <= m:
                bit[idx] += val
                idx += idx & (-idx)
        
        def query(bit, idx):
            res = 0
            while idx > 0:
                res += bit[idx]
                idx -= idx & (-idx)
            return res
        
        def find_kth(k):
            idx = 0
            current_count = 0
            bit_mask = 1
            while bit_mask <= m:
                bit_mask <<= 1
            bit_mask >>= 1
            
            while bit_mask > 0:
                t_idx = idx + bit_mask
                if t_idx <= m:
                    if current_count + bit_count[t_idx] < k:
                        idx = t_idx
                        current_count += bit_count[t_idx]
                bit_mask >>= 1
            return idx + 1
        
        # Initialize first window
        for i in range(x):
            val = nums[i]
            r = rank_map[val]
            update(bit_count, r, 1)
            update(bit_sum, r, val)
        
        def get_window_cost():
            total = x
            if total % 2 == 1:
                median_rank = find_kth((total + 1) // 2)
            else:
                median_rank = find_kth(total // 2)
            
            sum_less = query(bit_sum, median_rank - 1)
            count_less = query(bit_count, median_rank - 1)
            
            total_sum = query(bit_sum, m)
            count_total = x
            
            sum_ge = total_sum - sum_less
            count_ge = count_total - count_less
            
            median_val = sorted_unique[median_rank - 1]
            
            cost = (sum_ge - count_ge * median_val) + (count_less * median_val - sum_less)
            return cost
        
        window_costs = [0] * (n - x + 1)
        window_costs[0] = get_window_cost()
        
        for i in range(1, n - x + 1):
            out_val = nums[i - 1]
            in_val = nums[i + x - 1]
            
            r_out = rank_map[out_val]
            r_in = rank_map[in_val]
            
            update(bit_count, r_out, -1)
            update(bit_sum, r_out, -out_val)
            
            update(bit_count, r_in, 1)
            update(bit_sum, r_in, in_val)
            
            window_costs[i] = get_window_cost()
        
        INF = float('inf')
        # dp[j][i] = min cost to have j subarrays ending at or before index i
        # We only need the previous row and the value at i-x, but for simplicity and clarity 
        # given k is small, we use a 2D array.
        dp = [[INF] * n for _ in range(k + 1)]
        
        for i in range(n):
            dp[0][i] = 0
        
        for i in range(n):
            for j in range(1, k + 1):
                # Option 1: Don't end a subarray at i (inheriting from i-1)
                if i > 0:
                    dp[j][i] = min(dp[j][i], dp[j][i-1])
                
                # Option 2: End a subarray at i (requires i >= x-1)
                if i >= x - 1:
                    # The subarray is nums[i-x+1 ... i]
                    # Previous j-1 subarrays must end at or before i-x
                    prev_cost = dp[j-1][i-x]
                    if prev_cost != INF:
                        current_cost = prev_cost + window_costs[i-x+1]
                        dp[j][i] = min(dp[j][i], current_cost)
        
        return dp[k][n-1]