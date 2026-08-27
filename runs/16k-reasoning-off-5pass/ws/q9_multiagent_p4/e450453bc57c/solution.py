import heapq
from typing import List

class Solution:
    def minOperations(self, nums: List[int], x: int, k: int) -> int:
        n = len(nums)
        # dp[j] will store the minimum cost to form exactly j subarrays ending at or before the current position.
        dp = [float('inf')] * (k + 1)
        dp[0] = 0
        
        # Fenwick Tree (Binary Indexed Tree) setup
        # Values are in range [-10^6, 10^6]. We map them to [1, 2000001].
        offset = 1000000
        size = 2000002
        freq_bit = [0] * (size + 1)
        sum_bit = [0] * (size + 1)
        
        def update(bit, idx, val):
            while idx <= size:
                bit[idx] += val
                idx += idx & (-idx)
        
        def query(bit, idx):
            s = 0
            while idx > 0:
                s += bit[idx]
                idx -= idx & (-idx)
            return s
        
        # Find the smallest index such that query(index) >= k using binary lifting
        def find_kth(k):
            idx = 0
            current_sum = 0
            # 2^20 = 1,048,576; 2^21 = 2,097,152. Size is ~2*10^6, so 21 bits is sufficient.
            for i in range(21, -1, -1):
                next_idx = idx + (1 << i)
                if next_idx <= size and current_sum + freq_bit[next_idx] < k:
                    idx = next_idx
                    current_sum += freq_bit[idx]
            return idx + 1
        
        window_sum = 0
        
        for i in range(n):
            val = nums[i]
            idx = val + offset + 1
            
            # Add current element
            update(freq_bit, idx, 1)
            update(sum_bit, idx, val)
            window_sum += val
            
            # Remove element that falls out of the window
            if i >= x:
                old_val = nums[i-x]
                old_idx = old_val + offset + 1
                update(freq_bit, old_idx, -1)
                update(sum_bit, old_idx, -old_val)
                window_sum -= old_val
            
            # If we have a full window, calculate cost and update DP
            if i >= x - 1:
                # Find median: the (x+1)//2 -th smallest element
                kth = (x + 1) // 2
                median_idx = find_kth(kth)
                median_val = median_idx - offset - 1
                
                # Calculate cost: sum(|a - median|)
                # = (median * count_le - sum_le) + (sum_gt - median * count_gt)
                count_le = query(freq_bit, median_idx)
                sum_le = query(sum_bit, median_idx)
                count_gt = x - count_le
                sum_gt = window_sum - sum_le
                
                cost = (median_val * count_le - sum_le) + (sum_gt - median_val * count_gt)
                
                # Update DP table backwards to avoid using the same subarray multiple times
                for j in range(k, 0, -1):
                    if dp[j-1] != float('inf'):
                        dp[j] = min(dp[j], dp[j-1] + cost)
        
        return dp[k]