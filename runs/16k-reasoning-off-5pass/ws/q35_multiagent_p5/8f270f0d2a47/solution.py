class Solution:
    def beautifulNumbers(self, l: int, r: int) -> int:
        def count(n: int) -> int:
            if n <= 0:
                return 0
            digits = list(map(int, str(n)))
            m = len(digits)
            
            # Memoization dictionary
            memo = {}
            
            def dfs(idx: int, tight: bool, current_sum: int, current_product: int) -> int:
                # Base case: all digits placed
                if idx == m:
                    # A number is beautiful if product % sum == 0
                    # Note: current_sum is always > 0 for positive integers
                    # current_product can be 0 (if any digit was 0)
                    if current_sum > 0 and current_product % current_sum == 0:
                        return 1
                    else:
                        return 0
                
                state = (idx, tight, current_sum, current_product)
                if state in memo:
                    return memo[state]
                
                limit = digits[idx] if tight else 9
                res = 0
                
                for d in range(0, limit + 1):
                    new_tight = tight and (d == limit)
                    new_sum = current_sum + d
                    new_product = current_product * d
                    
                    # Optimization: if current_product is 0, it stays 0
                    # But we still need to track it because 0 % s == 0 is true for s > 0
                    
                    res += dfs(idx + 1, new_tight, new_sum, new_product)
                
                memo[state] = res
                return res
            
            # Start DFS: index 0, tight True, sum 0, product 1
            # Note: product starts at 1 because it's multiplicative identity
            return dfs(0, True, 0, 1)
        
        return count(r) - count(l - 1)