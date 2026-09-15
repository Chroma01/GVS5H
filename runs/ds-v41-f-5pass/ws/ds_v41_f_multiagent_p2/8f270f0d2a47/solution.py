class Solution:
    def beautifulNumbers(self, l: int, r: int) -> int:
        import sys
        sys.setrecursionlimit(10000)

        def count_up_to(x: int) -> int:
            if x <= 0:
                return 0
            digits = [int(c) for c in str(x)]
            n = len(digits)
            memo = {}

            def dp(pos, tight, started, s, p):
                # p == 0 sentinel: a zero digit has appeared -> product 0 -> beautiful
                if pos == n:
                    if not started:
                        return 0            # number 0 is not positive
                    if p == 0:
                        return 1            # product 0 divisible by any positive sum
                    return 1 if p % s == 0 else 0
                if not tight:
                    key = (pos, started, s, p)
                    cached = memo.get(key)
                    if cached is not None:
                        return cached
                limit = digits[pos] if tight else 9
                total = 0
                for d in range(limit + 1):
                    nt = tight and (d == limit)
                    if not started and d == 0:
                        total += dp(pos + 1, nt, False, 0, 1)
                    elif d == 0:
                        total += dp(pos + 1, nt, True, s, 0)
                    else:
                        total += dp(pos + 1, nt, True, s + d,
                                    0 if p == 0 else p * d)
                if not tight:
                    memo[key] = total
                return total

            return dp(0, True, False, 0, 1)

        return count_up_to(r) - count_up_to(l - 1)