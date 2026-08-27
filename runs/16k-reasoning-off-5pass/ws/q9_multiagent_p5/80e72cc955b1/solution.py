from typing import List

class Solution:
    def minOperations(self, queries: List[List[int]]) -> int:
        def get_sum_depths(n: int) -> int:
            """
            Calculates the sum of depths for numbers from 1 to n.
            Depth of x is the number of times we need to divide by 4 to get 0.
            Depth(x) = k if 4^(k-1) <= x < 4^k.
            Specifically:
            Depth 1: [1, 3]
            Depth 2: [4, 15]
            Depth 3: [16, 63]
            ...
            Depth k: [4^(k-1), 4^k - 1]
            
            We sum the depths. This is equivalent to summing (number of elements with depth >= k) for k >= 1.
            Number of elements with depth >= k in range [1, n] is max(0, n - 4^(k-1) + 1).
            We iterate k until 4^(k-1) > n.
            """
            if n <= 0:
                return 0
            
            total_depth = 0
            power_of_4 = 1  # Represents 4^(k-1)
            
            while power_of_4 <= n:
                # Count of numbers in [1, n] that have depth >= k
                # These are numbers >= power_of_4
                count = n - power_of_4 + 1
                if count > 0:
                    total_depth += count
                # Prepare next power of 4
                # Check for overflow before multiplying, though constraints say n <= 10^9
                if n // 4 < power_of_4:
                    break
                power_of_4 *= 4
            
            return total_depth

        total_ops = 0
        for l, r in queries:
            # Sum of depths for [l, r] = get_sum_depths(r) - get_sum_depths(l - 1)
            sum_depths = get_sum_depths(r) - get_sum_depths(l - 1)
            # Minimum operations is ceil(sum_depths / 2)
            total_ops += (sum_depths + 1) // 2
            
        return total_ops