class Solution:
    def minOperations(self, queries: List[List[int]]) -> int:
        def count_depth(n: int) -> int:
            """
            Returns the sum of depths for numbers from 1 to n.
            Depth of x is floor(log4(x)) + 1 for x > 0, 0 for x = 0.
            """
            if n <= 0:
                return 0
            
            total = 0
            power = 1  # 4^0
            k = 1      # depth level
            
            while power <= n:
                next_power = power * 4
                upper = min(n, next_power - 1)
                count = upper - power + 1
                total += k * count
                power = next_power
                k += 1
            
            return total
        
        result = 0
        for l, r in queries:
            sum_depths = count_depth(r) - count_depth(l - 1)
            # Each operation can reduce total depth by at most 2.
            # Minimum operations = ceil(sum_depths / 2)
            ops = (sum_depths + 1) // 2
            result += ops
        
        return result