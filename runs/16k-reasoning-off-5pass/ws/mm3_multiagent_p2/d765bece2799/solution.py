from typing import List

class Solution:
    def minMaxSubarraySum(self, nums: List[int], k: int) -> int:
        n = len(nums)
        if n == 0:
            return 0
        
        # L_min[i]: number of choices for left end when nums[i] is the minimum
        # R_min[i]: number of choices for right end when nums[i] is the minimum
        L_min = [0] * n
        R_min = [0] * n
        stack = []
        # Previous strictly smaller (pop >= to find last <)
        for i in range(n):
            while stack and nums[stack[-1]] >= nums[i]:
                stack.pop()
            prev = stack[-1] if stack else -1
            L_min[i] = i - prev
            stack.append(i)
        
        stack.clear()
        # Next smaller-or-equal (pop > to find first <=)
        for i in range(n - 1, -1, -1):
            while stack and nums[stack[-1]] > nums[i]:
                stack.pop()
            nxt = stack[-1] if stack else n
            R_min[i] = nxt - i
            stack.append(i)
        
        # L_max[i], R_max[i] for maximum
        L_max = [0] * n
        R_max = [0] * n
        stack.clear()
        # Previous strictly greater (pop <= to find last >)
        for i in range(n):
            while stack and nums[stack[-1]] <= nums[i]:
                stack.pop()
            prev = stack[-1] if stack else -1
            L_max[i] = i - prev
            stack.append(i)
        
        stack.clear()
        # Next greater-or-equal (pop < to find first >=)
        for i in range(n - 1, -1, -1):
            while stack and nums[stack[-1]] < nums[i]:
                stack.pop()
            nxt = stack[-1] if stack else n
            R_max[i] = nxt - i
            stack.append(i)
        
        def capped_count(L: int, R: int, k: int) -> int:
            """Count pairs (a,b) with 0<=a<L, 0<=b<R, a+b+1 <= k."""
            if k <= 0:
                return 0
            A = L if L < k else k
            if A <= 0:
                return 0
            if R >= k:
                # min(R, k-a) = k-a for all a
                return A * k - A * (A - 1) // 2
            split = k - R
            if split >= A:
                # min(R, k-a) = R for all a
                return A * R
            # split in [0, A-1]
            count_R = split + 1
            sum_R = count_R * R
            count_linear = A - 1 - split
            # sum_{a=split+1}^{A-1} (k - a)
            sum_linear = count_linear * k - (A * (A - 1) // 2 - split * (split + 1) // 2)
            return sum_R + sum_linear
        
        total = 0
        for i in range(n):
            c_min = capped_count(L_min[i], R_min[i], k)
            c_max = capped_count(L_max[i], R_max[i], k)
            total += nums[i] * (c_min + c_max)
        
        return total