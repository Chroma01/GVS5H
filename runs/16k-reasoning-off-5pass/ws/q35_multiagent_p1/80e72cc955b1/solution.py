class Solution:
    def minOperations(self, queries: List[List[int]]) -> int:
        def sum_depths(n: int) -> int:
            if n <= 0:
                return 0
            total = 0
            # Depth k corresponds to numbers in [4^(k-1), 4^k - 1]
            # We iterate k starting from 1
            power4 = 1  # 4^0
            k = 1
            while power4 <= n:
                # The upper bound for depth k is min(n, 4^k - 1)
                next_power4 = power4 * 4
                upper = min(n, next_power4 - 1)
                count = upper - power4 + 1
                total += count * k
                power4 = next_power4
                k += 1
            return total
        
        result = 0
        for l, r in queries:
            total_depth = sum_depths(r) - sum_depths(l - 1)
            # Minimum operations is ceil(total_depth / 2)
            ops = (total_depth + 1) // 2
            result += ops
        return result