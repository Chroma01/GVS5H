from typing import List

class Solution:
    def minOperations(self, queries: List[List[int]]) -> int:
        def calc_sum(n: int) -> int:
            if n <= 0:
                return 0
            
            total = 0
            current_power = 1  # Represents 4^k
            k = 0              # Represents the value h(i) for the current interval [4^k, 4^(k+1)-1]
            
            # We iterate while the start of the current interval is <= n
            while current_power <= n:
                # The interval for value (k+1) is [current_power, next_power - 1]
                next_power = current_power * 4
                
                # Determine the intersection of [current_power, next_power - 1] and [1, n]
                start = current_power
                end = min(next_power - 1, n)
                
                if start <= end:
                    count = end - start + 1
                    # The value h(i) for this range is k + 1
                    total += count * (k + 1)
                
                # Move to the next interval
                current_power = next_power
                k += 1
            
            return total

        total_ops = 0
        for l, r in queries:
            # Sum of h(i) for i in [l, r]
            sum_h = calc_sum(r) - calc_sum(l - 1)
            # Minimum operations is ceil(sum_h / 2)
            ops = (sum_h + 1) // 2
            total_ops += ops
            
        return total_ops