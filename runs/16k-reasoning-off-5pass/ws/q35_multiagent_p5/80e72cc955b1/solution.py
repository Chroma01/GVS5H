class Solution:
    def minOperations(self, queries: List[List[int]]) -> int:
        def count_digits_sum(n: int) -> int:
            if n <= 0:
                return 0
            total = 0
            k = 0
            low = 1  # 4^0
            while low <= n:
                high = low * 4 - 1  # 4^(k+1) - 1
                # Count numbers in [low, min(n, high)]
                upper = min(n, high)
                count = upper - low + 1
                total += count * (k + 1)
                k += 1
                low = high + 1  # next power of 4
            return total
        
        result = 0
        for l, r in queries:
            s = count_digits_sum(r) - count_digits_sum(l - 1)
            result += (s + 1) // 2
        return result