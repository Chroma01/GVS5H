from typing import List

class Solution:
    def minOperations(self, queries: List[List[int]]) -> int:
        def calculate_sum(n: int) -> int:
            if n <= 0:
                return 0
            
            total_cost = 0
            power = 1  # Represents 4^k
            k = 0       # Represents the exponent, cost is k+1
            
            while power <= n:
                # Define the current block range [start, end]
                start = power
                end = power * 4 - 1
                
                # Determine the intersection of [start, end] and [1, n]
                # Since power <= n, start is always <= n.
                # The end of the block might exceed n.
                block_end = min(end, n)
                
                # Number of elements in this intersection
                count = block_end - start + 1
                
                # Cost for each element in this block is (k + 1)
                total_cost += count * (k + 1)
                
                # Move to the next block
                power *= 4
                k += 1
            
            return total_cost

        total_ops = 0
        for l, r in queries:
            # Calculate sum of costs for range [l, r]
            # Sum(l, r) = Sum(1, r) - Sum(1, l-1)
            sum_r = calculate_sum(r)
            sum_l_minus_1 = calculate_sum(l - 1)
            total_cost_range = sum_r - sum_l_minus_1
            
            # Minimum operations is ceil(total_cost_range / 2)
            # Using integer arithmetic: (total_cost_range + 1) // 2
            ops = (total_cost_range + 1) // 2
            total_ops += ops
            
        return total_ops