import heapq
from typing import List

class SlidingWindowMedian:
    def __init__(self, size: int):
        self.size = size
        self.low = [] 
        self.high = []
        self.sum_low = 0
        self.sum_high = 0
        self.count = 0
        self.lazy_low = {}
        self.lazy_high = {}

    def _clean_low(self):
        while self.lazy_low and (-self.low[0] in self.lazy_low) and self.lazy_low[-self.low[0]] > 0:
            val = -heapq.heappop(self.low)
            self.lazy_low[val] -= 1
            if self.lazy_low[val] == 0:
                del self.lazy_low[val]
                
    def _clean_high(self):
        while self.lazy_high and (self.high[0] in self.lazy_high) and self.lazy_high[self.high[0]] > 0:
            val = heapq.heappop(self.high)
            self.lazy_high[val] -= 1
            if self.lazy_high[val] == 0:
                del self.lazy_high[val]

    def add(self, num: int):
        self.count += 1
        if not self.low or num <= -self.low[0]:
            heapq.heappush(self.low, -num)
            self.sum_low += num
        else:
            heapq.heappush(self.high, num)
            self.sum_high += num
            
        # Rebalance
        if len(self.low) > len(self.high) + 1:
            val = -heapq.heappop(self.low)
            self.sum_low -= val
            heapq.heappush(self.high, val)
            self.sum_high += val
        elif len(self.high) > len(self.low):
            val = heapq.heappop(self.high)
            self.sum_high -= val
            heapq.heappush(self.low, -val)
            self.sum_low += val
            
        self._clean_low()
        self._clean_high()
        
    def remove(self, num: int):
        # Determine which heap it logically belongs to based on current median
        # If low is empty, it must be in high (since count > 0)
        if not self.low:
            heapq.heappush(self.lazy_high, num)
            self.sum_high -= num
        elif num <= -self.low[0]:
            heapq.heappush(self.lazy_low, num)
            self.sum_low -= num
        else:
            heapq.heappush(self.lazy_high, num)
            self.sum_high -= num
            
        self.count -= 1
        
        # Clean heaps to get accurate sizes for rebalancing
        self._clean_low()
        self._clean_high()
        
        if len(self.low) > len(self.high) + 1:
            val = -heapq.heappop(self.low)
            self.sum_low -= val
            heapq.heappush(self.high, val)
            self.sum_high += val
        elif len(self.high) > len(self.low):
            val = heapq.heappop(self.high)
            self.sum_high -= val
            heapq.heappush(self.low, -val)
            self.sum_low += val
            
        self._clean_low()
        self._clean_high()

    def get_cost(self) -> int:
        if self.count == 0:
            return 0
        self._clean_low()
        self._clean_high()
        
        if not self.low:
            return 0
            
        median = -self.low[0]
        len_low = len(self.low)
        len_high = len(self.high)
        
        # Cost = sum(|x - median|)
        # = (len(low) * median - sum(low)) + (sum(high) - len(high) * median)
        # = (len_low - len_high) * median + sum_high - sum_low
        term1 = (len_low - len_high) * median
        term2 = self.sum_high - self.sum_low
        return term1 + term2

class Solution:
    def minOperations(self, nums: List[int], x: int, k: int) -> int:
        n = len(nums)
        # dp[j] = min cost to have j subarrays
        # Initialize with infinity, dp[0] = 0
        dp = [float('inf')] * (k + 1)
        dp[0] = 0
        
        window = SlidingWindowMedian(x)
        
        # We need to process windows ending at i from x-1 to n-1
        # We add nums[i] and remove nums[i-x]
        
        for i in range(n):
            window.add(nums[i])
            if i >= x:
                window.remove(nums[i-x])
            
            if i >= x - 1:
                # We have a full window ending at i
                cost = window.get_cost()
                # Update dp table in reverse to avoid using the same window for multiple subarrays in one step
                for j in range(k, 0, -1):
                    if dp[j-1] != float('inf'):
                        dp[j] = min(dp[j], dp[j-1] + cost)
                        
        return dp[k] if dp[k] != float('inf') else -1