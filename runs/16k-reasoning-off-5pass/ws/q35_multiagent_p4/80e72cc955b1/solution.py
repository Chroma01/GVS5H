class Solution:
    def minOperations(self, queries: List[List[int]]) -> int:
        def get_cost(x: int) -> int:
            if x <= 0:
                return 0
            # cost is floor(log4(x)) + 1
            # We can compute this by repeated division or using log
            # Since x <= 10^9, log4(x) <= 15, so a loop is fine
            c = 0
            while x > 0:
                x //= 4
                c += 1
            return c
        
        def count_cost(n: int, k: int) -> int:
            """Count numbers in [1, n] with cost exactly k."""
            if n <= 0:
                return 0
            # Range for cost k is [4^(k-1), 4^k - 1]
            low = 1 << (2 * (k - 1))  # 4^(k-1)
            high = (1 << (2 * k)) - 1  # 4^k - 1
            
            if n < low:
                return 0
            return min(n, high) - low + 1
        
        total_ops = 0
        for l, r in queries:
            # Maximum cost is the cost of r (since cost is non-decreasing)
            M = get_cost(r)
            
            # Calculate total sum of costs S
            S = 0
            # Costs range from 1 to about 15 for r <= 10^9
            # We can iterate k from 1 to M (since higher costs won't appear in [l, r] if M is max)
            # Actually, we should iterate up to M, but to be safe, up to 16
            for k in range(1, M + 1):
                cnt = count_cost(r, k) - count_cost(l - 1, k)
                S += cnt * k
            
            # The answer is max(M, ceil(S/2))
            ops = max(M, (S + 1) // 2)
            total_ops += ops
            
        return total_ops