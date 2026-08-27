class Solution:
    def beautifulNumbers(self, l: int, r: int) -> int:
        def count_upto(N):
            if N <= 0:
                return 0
            s = str(N)
            n = len(s)
            from functools import lru_cache

            @lru_cache(maxsize=None)
            def dfs(pos, tight, started, counts):
                # counts is a tuple of 10 ints (c0..c9)
                if pos == n:
                    if not started:
                        return 0
                    if counts[0] > 0:
                        return 1
                    total = 0
                    prod = 1
                    for i in range(1, 10):
                        cnt = counts[i]
                        total += i * cnt
                        prod *= i ** cnt
                    if total == 0:
                        return 0
                    return 1 if prod % total == 0 else 0
                limit = int(s[pos]) if tight else 9
                res = 0
                for d in range(0, limit + 1):
                    ntight = tight and (d == limit)
                    nstarted = started or (d != 0)
                    if not nstarted:
                        res += dfs(pos + 1, ntight, False, (0,)*10)
                    else:
                        lst = list(counts) if started else [0]*10
                        lst[d] += 1
                        res += dfs(pos + 1, ntight, True, tuple(lst))
                return res

            return dfs(0, True, False, (0,)*10)

        return count_upto(r) - count_upto(l - 1)