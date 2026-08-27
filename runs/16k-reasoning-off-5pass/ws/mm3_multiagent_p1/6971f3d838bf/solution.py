from typing import List
from collections import defaultdict

class Solution:
    def maxSubarraySum(self, nums: List[int]) -> int:
        n = len(nums)
        if n == 0:
            return 0
        
        # M0: standard Kadane max subarray sum (no deletion case)
        M0 = nums[0]
        cur = nums[0]
        for i in range(1, n):
            cur = max(nums[i], cur + nums[i])
            M0 = max(M0, cur)
        
        # Group indices by value
        positions = defaultdict(list)
        for i, v in enumerate(nums):
            positions[v].append(i)
        
        answer = M0
        
        # Compute prefix sum of original array once
        prefix = [0] * (n + 1)
        for i in range(n):
            prefix[i+1] = prefix[i] + nums[i]
        
        for x, pos_list in positions.items():
            if x >= 0:
                # For x >= 0, f(x) <= M0, so skipping is safe
                continue
            
            # Special case: if all elements are x, cannot delete (array becomes empty)
            if len(pos_list) == n:
                continue
            
            k = len(pos_list)
            
            # Compute gap sums and their prefix sums PS[0..k]
            # gap 0: [0, pos_list[0]-1]
            # gap t (1<=t<k): [pos_list[t-1]+1, pos_list[t]-1]
            # gap k: [pos_list[-1]+1, n-1]
            PS = [0] * (k + 1)
            s = 0
            for t in range(k + 1):
                if t == 0:
                    l, r = 0, pos_list[0] - 1
                elif t == k:
                    l, r = pos_list[-1] + 1, n - 1
                else:
                    l, r = pos_list[t-1] + 1, pos_list[t] - 1
                if l <= r:
                    s += prefix[r+1] - prefix[l]
                PS[t] = s
            
            # f(x) = max_{0<=i<=j<=k} (PS[j] - PS[i-1] + |x|*(j-i))
            # For fixed j: max over i is -min of (PS[i-1] + |x|*i) for 0<=i<=j
            # PS[-1] is defined as 0
            abs_x = -x
            # min_val tracks min(PS[i-1] + |x|*i) for i from 0 to j
            # For i=0: PS[-1] + 0 = 0
            min_val = 0
            best_f = float('-inf')
            for j in range(k + 1):
                # Try all i <= j, but we maintain min over i <= j
                val = PS[j] + abs_x * j - min_val
                if val > best_f:
                    best_f = val
                # Update min_val to include i=j+1 for next j
                # Value for i=j+1 is PS[j] + |x|*(j+1)
                candidate = PS[j] + abs_x * (j + 1)
                if candidate < min_val:
                    min_val = candidate
            
            if best_f > answer:
                answer = best_f
        
        return answer