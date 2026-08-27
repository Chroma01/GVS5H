import sys
from functools import lru_cache

sys.setrecursionlimit(100000)

class Solution:
    def beautifulNumbers(self, l: int, r: int) -> int:
        def count_upto(X: int) -> int:
            if X < 1:
                return 0
            s = str(X)
            n = len(s)
            digits = list(map(int, s))
            
            total = 0
            for s_val in range(1, 82):  # max sum for 9 digits is 81
                @lru_cache(maxsize=None)
                def dp(pos: int, sum_so_far: int, prod_mod: int, tight: bool, started: bool) -> int:
                    if pos == n:
                        if started and sum_so_far == s_val and prod_mod == 0:
                            return 1
                        return 0
                    
                    max_digit = digits[pos] if tight else 9
                    res = 0
                    for d in range(0, max_digit + 1):
                        new_tight = tight and (d == max_digit)
                        if not started and d == 0:
                            res += dp(pos + 1, 0, 1, new_tight, False)
                        else:
                            new_started = True
                            new_sum = sum_so_far + d
                            if new_sum > s_val:
                                continue
                            if d == 0:
                                new_prod_mod = 0
                            else:
                                if not started:
                                    new_prod_mod = d % s_val
                                else:
                                    new_prod_mod = (prod_mod * d) % s_val
                            res += dp(pos + 1, new_sum, new_prod_mod, new_tight, new_started)
                    return res
                
                total += dp(0, 0, 1, True, False)
            
            return total
        
        return count_upto(r) - count_upto(l - 1)