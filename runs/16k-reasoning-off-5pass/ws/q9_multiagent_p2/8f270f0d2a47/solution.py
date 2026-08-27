class Solution:
    def beautifulNumbers(self, l: int, r: int) -> int:
        def count(n: int) -> int:
            if n == 0:
                return 0
            
            digits = list(map(int, str(n)))
            num_digits = len(digits)
            
            from functools import lru_cache
            
            @lru_cache(None)
            def dfs(idx: int, current_sum: int, current_product: int, is_started: bool, is_tight: bool) -> int:
                if idx == num_digits:
                    if not is_started:
                        return 0
                    
                    if current_product == 0:
                        return 1
                    else:
                        return 1 if current_product % current_sum == 0 else 0
                
                limit = digits[idx] if is_tight else 9
                total_count = 0
                
                for digit in range(10):
                    new_tight = is_tight and (digit == limit)
                    
                    if not is_started:
                        if digit == 0:
                            total_count += dfs(idx + 1, 0, 1, False, new_tight)
                        else:
                            total_count += dfs(idx + 1, digit, digit, True, new_tight)
                    else:
                        new_sum = current_sum + digit
                        if digit == 0:
                            new_prod = 0
                        else:
                            new_prod = current_product * digit
                        total_count += dfs(idx + 1, new_sum, new_prod, True, new_tight)
                
                return total_count

            return dfs(0, 0, 1, False, True)

        return count(r) - count(l - 1)