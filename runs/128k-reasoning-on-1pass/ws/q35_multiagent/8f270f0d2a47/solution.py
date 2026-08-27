class Solution:
    def beautifulNumbers(self, l: int, r: int) -> int:
        def count(X):
            if X == 0: return 0
            s = list(map(int, str(X)))
            n = len(s)
            
            from functools import lru_cache
            
            @lru_cache(None)
            def dp(idx, current_sum, current_prod, tight, started):
                if idx == n:
                    if not started: return 0
                    return 1 if current_prod % current_sum == 0 else 0
                
                limit = s[idx] if tight else 9
                total = 0
                for d in range(limit + 1):
                    new_tight = tight and (d == limit)
                    new_started = started or (d != 0)
                    
                    if not started and d == 0:
                        total += dp(idx + 1, 0, 1, new_tight, False)
                    else:
                        new_sum = current_sum + d
                        new_prod = current_prod * d
                        total += dp(idx + 1, new_sum, new_prod, new_tight, True)
                return total

            return dp(0, 0, 1, True, False)
            
        return count(r) - count(l - 1)