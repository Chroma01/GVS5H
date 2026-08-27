class Solution:
    def minMaxSubarraySum(self, nums: List[int], k: int) -> int:
        from collections import deque
        
        minDeque = deque()  # (value, count) for minimums, non-decreasing
        maxDeque = deque()  # (value, count) for maximums, non-increasing
        total_min = 0
        total_max = 0
        
        l = 0
        ans = 0
        n = len(nums)
        
        for r in range(n):
            v = nums[r]
            
            # Add v to minDeque
            c = 1
            while minDeque and minDeque[-1][0] > v:
                val, cnt = minDeque.pop()
                c += cnt
                total_min -= val * cnt
            if minDeque and minDeque[-1][0] == v:
                val, cnt = minDeque[-1]
                cnt += c
                minDeque[-1] = (val, cnt)
                total_min += val * c
            else:
                minDeque.append((v, c))
                total_min += v * c
            
            # Add v to maxDeque
            c = 1
            while maxDeque and maxDeque[-1][0] < v:
                val, cnt = maxDeque.pop()
                c += cnt
                total_max -= val * cnt
            if maxDeque and maxDeque[-1][0] == v:
                val, cnt = maxDeque[-1]
                cnt += c
                maxDeque[-1] = (val, cnt)
                total_max += val * c
            else:
                maxDeque.append((v, c))
                total_max += v * c
            
            # Shrink window from left if size > k
            while r - l + 1 > k:
                l += 1
                val, cnt = minDeque[0]
                cnt -= 1
                total_min -= val
                if cnt == 0:
                    minDeque.popleft()
                else:
                    minDeque[0] = (val, cnt)
                val, cnt = maxDeque[0]
                cnt -= 1
                total_max -= val
                if cnt == 0:
                    maxDeque.popleft()
                else:
                    maxDeque[0] = (val, cnt)
            
            ans += total_min + total_max
        
        return ans