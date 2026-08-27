class Solution:
    def beautifulNumbers(self, l: int, r: int) -> int:
        def count_upto(x: int) -> int:
            # Count beautiful numbers in [1, x] (0 is never counted).
            if x <= 0:
                return 0
            digits = list(map(int, str(x)))
            n = len(digits)
            total = 0
            # Digit sum of any number <= x (< 10^9) is in [1, 81].
            # For each target sum s, count numbers with digit sum == s
            # and digit product % s == 0, tracking product mod s.
            for s in range(1, 82):
                memo = {}

                def dp(pos: int, cur_sum: int, prod_mod: int, started: bool, tight: bool) -> int:
                    if cur_sum > s:
                        return 0
                    if pos == n:
                        return 1 if (started and cur_sum == s and prod_mod == 0) else 0
                    if not tight:
                        key = (pos, cur_sum, prod_mod, started)
                        if key in memo:
                            return memo[key]
                    limit = digits[pos] if tight else 9
                    res = 0
                    for d in range(limit + 1):
                        nstarted = started or d != 0
                        if nstarted:
                            nsum = cur_sum + d
                            nprod = (prod_mod * d) % s if started else (d % s)
                        else:
                            nsum = cur_sum
                            nprod = prod_mod  # placeholder 0 until the number starts
                        res += dp(pos + 1, nsum, nprod, nstarted, tight and d == limit)
                    if not tight:
                        memo[(pos, cur_sum, prod_mod, started)] = res
                    return res

                total += dp(0, 0, 0, False, True)
            return total

        return count_upto(r) - count_upto(l - 1)