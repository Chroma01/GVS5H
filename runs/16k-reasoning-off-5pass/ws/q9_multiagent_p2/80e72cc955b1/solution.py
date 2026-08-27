from typing import List

class Solution:
    def minOperations(self, queries: List[List[int]]) -> int:
        total_ops = 0
        
        for l, r in queries:
            current_sum = 0
            start = 1
            k = 1
            
            # Iterate through intervals where steps(x) is constant.
            # Interval k corresponds to x in [4^(k-1), 4^k - 1]
            # start holds 4^(k-1)
            while start <= r:
                # Calculate the end of the current interval: 4^k - 1
                # Since start = 4^(k-1), end = start * 4 - 1
                end = start * 4 - 1
                
                # Determine intersection with [l, r]
                low = max(l, start)
                high = min(r, end)
                
                if low <= high:
                    count = high - low + 1
                    current_sum += count * k
                
                # Prepare for next iteration
                start = end + 1
                k += 1
                
                # Optimization: if start exceeds r, we can stop
                if start > r:
                    break
            
            # Each operation reduces the total "steps" by 2 (handles 2 numbers)
            # Total operations = ceil(current_sum / 2)
            total_ops += (current_sum + 1) // 2
            
        return total_ops