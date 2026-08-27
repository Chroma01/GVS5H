class Solution:
    def minOperations(self, queries: List[List[int]]) -> int:
        def count_ops(n: int) -> int:
            """
            Returns the sum of ops(x) for x from 1 to n.
            ops(x) is the number of times x must be divided by 4 (floor) to become 0.
            """
            if n <= 0:
                return 0
            
            total = 0
            power_low = 1  # 4^0
            k = 1
            
            while power_low <= n:
                power_high = power_low * 4 - 1  # Upper bound for current k
                if power_high > n:
                    power_high = n
                
                count = power_high - power_low + 1
                total += k * count
                
                power_low = power_high + 1
                k += 1
            
            return total
        
        total_result = 0
        for l, r in queries:
            s = count_ops(r) - count_ops(l - 1)
            # Each operation handles two numbers, so min operations is ceil(s / 2)
            ops_needed = (s + 1) // 2
            total_result += ops_needed
        
        return total_result