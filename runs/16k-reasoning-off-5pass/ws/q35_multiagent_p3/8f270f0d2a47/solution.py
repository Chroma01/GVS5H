class Solution:
    def beautifulNumbers(self, l: int, r: int) -> int:
        def count_up_to(n, s):
            if n <= 0:
                return 0
            digits = list(map(int, str(n)))
            n_len = len(digits)
            
            # dp[pos][tight][current_sum][current_prod_mod_s][started]
            # We use memoization with a dictionary or lru_cache
            # Since s is fixed for this call, we can use a closure
            
            from functools import lru_cache
            
            @lru_cache(maxsize=None)
            def dp(pos, tight, current_sum, current_prod_mod_s, started):
                if current_sum > s:
                    return 0
                if pos == n_len:
                    # Check if we have a valid number
                    if started and current_sum == s and current_prod_mod_s == 0:
                        return 1
                    else:
                        return 0
                
                total = 0
                limit = digits[pos] if tight else 9
                
                for d in range(0, limit + 1):
                    new_tight = tight and (d == limit)
                    if not started and d == 0:
                        # Leading zero, don't update sum or product
                        new_started = False
                        new_sum = 0
                        new_prod_mod = 0
                    else:
                        new_started = True
                        new_sum = current_sum + d
                        # If new_sum exceeds s, we can skip, but we check at start of next call or here
                        if new_sum > s:
                            continue
                        new_prod_mod = (current_prod_mod_s * d) % s
                    
                    total += dp(pos + 1, new_tight, new_sum, new_prod_mod, new_started)
                
                return total
            
            return dp(0, True, 0, 0, False)
        
        total = 0
        for s in range(1, 82):  # max sum for 10^9 is 9*9=81
            total += count_up_to(r, s) - count_up_to(l - 1, s)
        
        return total