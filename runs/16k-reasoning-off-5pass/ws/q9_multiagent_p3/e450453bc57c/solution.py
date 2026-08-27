import heapq
from typing import List

class Solution:
    def minOperations(self, nums: List[int], x: int, k: int) -> int:
        n = len(nums)
        # dp[j] stores the minimum cost to form j non-overlapping subarrays ending at or before the current index.
        # Initialize dp[0] = 0, others to infinity.
        dp = [0] + [float('inf')] * k
        
        # dp_states[i] will store a copy of the dp array after processing index i.
        # This allows us to access the state at index i-x when considering a subarray ending at i.
        dp_states = []
        
        # Two heaps to maintain the median of the sliding window of size x.
        # lo: max-heap (stores the smaller half of elements, stored as negatives)
        # hi: min-heap (stores the larger half of elements)
        lo = []
        hi = []
        
        # Sums of elements in lo and hi to calculate cost in O(1)
        sum_lo = 0
        sum_hi = 0
        
        # Dictionary to lazily remove elements that fall out of the sliding window
        to_remove = {}
        
        for i in range(n):
            val = nums[i]
            
            # Add current element to the appropriate heap
            if not lo or val <= -lo[0]:
                heapq.heappush(lo, -val)
                sum_lo += val
            else:
                heapq.heappush(hi, val)
                sum_hi += val
            
            # Balance heaps: len(lo) should be equal to len(hi) or len(hi) + 1
            while len(lo) > len(hi) + 1:
                m = -heapq.heappop(lo)
                sum_lo -= m
                heapq.heappush(hi, m)
                sum_hi += m
            while len(hi) > len(lo):
                m = heapq.heappop(hi)
                sum_hi -= m
                heapq.heappush(lo, -m)
                sum_lo += m
            
            # If we have a full window of size x ending at i
            if i >= x - 1:
                # The element leaving the window is nums[i-x]
                out_val = nums[i-x]
                to_remove[out_val] = to_remove.get(out_val, 0) + 1
                
                # Remove expired elements from the tops of the heaps
                while lo and lo[0] in to_remove and to_remove[lo[0]] > 0:
                    m = -heapq.heappop(lo)
                    sum_lo -= m
                    to_remove[m] -= 1
                while hi and hi[0] in to_remove and to_remove[hi[0]] > 0:
                    m = heapq.heappop(hi)
                    sum_hi -= m
                    to_remove[m] -= 1
                
                # Re-balance heaps after removal
                while len(lo) > len(hi) + 1:
                    m = -heapq.heappop(lo)
                    sum_lo -= m
                    heapq.heappush(hi, m)
                    sum_hi += m
                while len(hi) > len(lo):
                    m = heapq.heappop(hi)
                    sum_hi -= m
                    heapq.heappush(lo, -m)
                    sum_lo += m
                
                # Calculate the cost to make all elements in the current window equal to the median
                # Median is the top of lo (since len(lo) >= len(hi))
                median = -lo[0]
                # Cost = sum(|num - median|)
                #       = (median * count_lo - sum_lo) + (sum_hi - median * count_hi)
                cost = (median * len(lo) - sum_lo) + (sum_hi - median * len(hi))
                
                # Update DP table
                # We can form j subarrays ending at i if we had j-1 subarrays ending at or before i-x.
                # The state at i-x is stored in dp_states[i-x].
                prev_dp = dp_states[i-x]
                
                # Iterate backwards to update dp[j]
                for j in range(1, k + 1):
                    if prev_dp[j-1] != float('inf'):
                        dp[j] = min(dp[j], prev_dp[j-1] + cost)
            
            # Save the current state of dp for future reference (specifically for index i-x later)
            dp_states.append(list(dp))
        
        return dp[k]