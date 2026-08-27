from collections import deque
from typing import List

class Solution:
    def minMaxSubarraySum(self, nums: List[int], k: int) -> int:
        n = len(nums)
        # Deques store (value, count) pairs
        # For minimum: non-decreasing values from front (oldest/longest subarrays) to back (newest/shortest)
        min_dq = deque()
        # For maximum: non-increasing values from front to back
        max_dq = deque()
        
        cur_min_sum = 0
        cur_max_sum = 0
        total_min = 0  # total number of subarrays (sum of counts) in min_dq
        total_max = 0
        
        ans = 0
        
        for i in range(n):
            x = nums[i]
            
            # Process minimum deque
            cnt_min = 1
            while min_dq and min_dq[-1][0] > x:
                val, c = min_dq.pop()
                cur_min_sum -= val * c
                total_min -= c
                cnt_min += c
            min_dq.append((x, cnt_min))
            cur_min_sum += x * cnt_min
            total_min += cnt_min
            
            # Trim from front if total exceeds k
            while total_min > k:
                val, c = min_dq[0]
                delta = total_min - k
                if c <= delta:
                    cur_min_sum -= val * c
                    total_min -= c
                    min_dq.popleft()
                else:
                    cur_min_sum -= val * delta
                    min_dq[0] = (val, c - delta)
                    total_min -= delta
            
            # Process maximum deque
            cnt_max = 1
            while max_dq and max_dq[-1][0] < x:
                val, c = max_dq.pop()
                cur_max_sum -= val * c
                total_max -= c
                cnt_max += c
            max_dq.append((x, cnt_max))
            cur_max_sum += x * cnt_max
            total_max += cnt_max
            
            # Trim from front if total exceeds k
            while total_max > k:
                val, c = max_dq[0]
                delta = total_max - k
                if c <= delta:
                    cur_max_sum -= val * c
                    total_max -= c
                    max_dq.popleft()
                else:
                    cur_max_sum -= val * delta
                    max_dq[0] = (val, c - delta)
                    total_max -= delta
            
            ans += cur_min_sum + cur_max_sum
        
        return ans