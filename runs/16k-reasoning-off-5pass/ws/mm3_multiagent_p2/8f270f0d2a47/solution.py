class Solution:
    def beautifulNumbers(self, l: int, r: int) -> int:
        def count_up_to(x):
            if x <= 0:
                return 0
            s = str(x)
            n = len(s)
            digits = [int(c) for c in s]
            
            from functools import lru_cache
            
            # Exponents of (2,3,5,7) for digits 1..9
            digit_exps = [
                (0,0,0,0), # 1
                (1,0,0,0), # 2
                (0,1,0,0), # 3
                (2,0,0,0), # 4
                (0,0,1,0), # 5
                (1,1,0,0), # 6
                (0,0,0,1), # 7
                (3,0,0,0), # 8
                (0,2,0,0)  # 9
            ]
            
            @lru_cache(None)
            def dfs_not_started(pos, tight):
                if pos == n:
                    return 0
                limit = digits[pos] if tight else 9
                total = 0
                for d in range(0, limit + 1):
                    new_tight = tight and (d == limit)
                    if d == 0:
                        total += dfs_not_started(pos + 1, new_tight)
                    else:
                        e2, e3, e5, e7 = digit_exps[d - 1]
                        total += dfs_no_zero(pos + 1, new_tight, d, e2, e3, e5, e7)
                return total
            
            @lru_cache(None)
            def dfs_no_zero(pos, tight, sum_val, e2, e3, e5, e7):
                if pos == n:
                    prod = (2 ** e2) * (3 ** e3) * (5 ** e5) * (7 ** e7)
                    return 1 if (sum_val > 0 and prod % sum_val == 0) else 0
                limit = digits[pos] if tight else 9
                total = 0
                for d in range(0, limit + 1):
                    new_tight = tight and (d == limit)
                    if d == 0:
                        total += dfs_has_zero(pos + 1, new_tight)
                    else:
                        de2, de3, de5, de7 = digit_exps[d - 1]
                        total += dfs_no_zero(
                            pos + 1, new_tight,
                            sum_val + d,
                            e2 + de2, e3 + de3, e5 + de5, e7 + de7
                        )
                return total
            
            @lru_cache(None)
            def dfs_has_zero(pos, tight):
                if pos == n:
                    return 1
                limit = digits[pos] if tight else 9
                total = 0
                for d in range(0, limit + 1):
                    new_tight = tight and (d == limit)
                    total += dfs_has_zero(pos + 1, new_tight)
                return total
            
            return dfs_not_started(0, True)
        
        return count_up_to(r) - count_up_to(l - 1)