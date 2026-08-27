from functools import lru_cache

class Solution:
    def beautifulNumbers(self, l: int, r: int) -> int:
        def countBeautiful(n: int) -> int:
            if n == 0:
                return 0
            
            s = str(n)
            length = len(s)
            
            # Helper to count numbers in [1, n] with no '0'
            # This is a standard digit DP counting numbers using digits 1-9
            def count_no_zero(idx: int, tight: bool) -> int:
                if idx == length:
                    return 1
                
                limit = int(s[idx]) if tight else 9
                res = 0
                for digit in range(1, limit + 1):
                    new_tight = tight and (digit == limit)
                    res += count_no_zero(idx + 1, new_tight)
                return res
            
            # Helper to count numbers in [1, n] with no '0' that are beautiful
            # State: (idx, tight, current_sum, current_product)
            # We use lru_cache for memoization. 
            # Note: current_product can be large, but the number of reachable states 
            # for n < 10^9 is manageable due to the tight constraint and digit limits.
            @lru_cache(maxsize=None)
            def dfs(idx: int, tight: bool, current_sum: int, current_product: int) -> int:
                if idx == length:
                    # Check condition: product % sum == 0
                    # Since we only use digits 1-9, sum >= 1 and product >= 1
                    return 1 if (current_product % current_sum == 0) else 0
                
                limit = int(s[idx]) if tight else 9
                res = 0
                for digit in range(1, limit + 1):
                    new_tight = tight and (digit == limit)
                    new_sum = current_sum + digit
                    new_product = current_product * digit
                    res += dfs(idx + 1, new_tight, new_sum, new_product)
                return res

            total_no_zero = count_no_zero(0, True)
            beautiful_no_zero = dfs(0, True, 0, 1)
            
            # Total beautiful = (Numbers with '0') + (Numbers without '0' and beautiful)
            # Numbers with '0' = n - total_no_zero
            return (n - total_no_zero) + beautiful_no_zero

        return countBeautiful(r) - countBeautiful(l - 1)