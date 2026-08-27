from functools import lru_cache

class Solution:
    def beautifulNumbers(self, l: int, r: int) -> int:
        caps = (6, 4, 2, 2)
        primes = (2, 3, 5, 7)

        digit_exp = [
            (0, 0, 0, 0),  # 0
            (0, 0, 0, 0),  # 1
            (1, 0, 0, 0),  # 2
            (0, 1, 0, 0),  # 3
            (2, 0, 0, 0),  # 4
            (0, 0, 1, 0),  # 5
            (1, 1, 0, 0),  # 6
            (0, 0, 0, 1),  # 7
            (3, 0, 0, 0),  # 8
            (0, 2, 0, 0),  # 9
        ]

        def required_exponents(x: int):
            if x == 0:
                return None
            t = [0, 0, 0, 0]
            for i, p in enumerate(primes):
                while x % p == 0:
                    t[i] += 1
                    x //= p
            if x != 1:
                return None
            return tuple(t)

        req = [None] * 91
        for s in range(1, 91):
            req[s] = required_exponents(s)

        def count_bad(n: int) -> int:
            if n <= 0:
                return 0

            digits = list(map(int, str(n)))
            zero_e = (0, 0, 0, 0)

            @lru_cache(maxsize=None)
            def dp(pos: int, tight: bool, started: bool, s: int, e: tuple) -> int:
                if pos == len(digits):
                    if not started:
                        return 0

                    need = req[s] if s < len(req) else required_exponents(s)
                    if need is None:
                        return 1

                    return 1 if (
                        need[0] > e[0] or
                        need[1] > e[1] or
                        need[2] > e[2] or
                        need[3] > e[3]
                    ) else 0

                total = 0
                upper = digits[pos] if tight else 9

                for d in range(upper + 1):
                    ntight = tight and d == digits[pos]

                    if not started:
                        if d == 0:
                            total += dp(pos + 1, ntight, False, 0, zero_e)
                        else:
                            de = digit_exp[d]
                            ne = (
                                min(caps[0], de[0]),
                                min(caps[1], de[1]),
                                min(caps[2], de[2]),
                                min(caps[3], de[3]),
                            )
                            total += dp(pos + 1, ntight, True, d, ne)
                    else:
                        if d == 0:
                            continue

                        de = digit_exp[d]
                        ne = (
                            min(caps[0], e[0] + de[0]),
                            min(caps[1], e[1] + de[1]),
                            min(caps[2], e[2] + de[2]),
                            min(caps[3], e[3] + de[3]),
                        )
                        total += dp(pos + 1, ntight, True, s + d, ne)

                return total

            return dp(0, True, False, 0, zero_e)

        return (r - l + 1) - (count_bad(r) - count_bad(l - 1))