class Solution:
    def minOperations(self, queries: List[List[int]]) -> int:
        def count_ops(n: int) -> int:
            if n <= 0:
                return 0
            total = 0
            power = 1
            k = 0
            while power <= n:
                next_power = power * 4
                # Numbers in [power, min(n, next_power - 1)] have depth k+1
                upper = min(n, next_power - 1)
                count = upper - power + 1
                total += count * (k + 1)
                power = next_power
                k += 1
            return total
        
        total_sum = 0
        for l, r in queries:
            s = count_ops(r) - count_ops(l - 1)
            # Each operation handles two "depth units"
            ops = (s + 1) // 2
            total_sum += ops
        
        return total_sum