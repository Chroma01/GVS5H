from functools import lru_cache


class Solution:
    def beautifulNumbers(self, l: int, r: int) -> int:
        return self._count(r) - self._count(l - 1)

    def _count(self, n: int) -> int:
        if n <= 0:
            return 0
        # Every positive number containing a zero digit has product 0,
        # so it is beautiful. Count those, plus beautiful no-zero numbers.
        return n - self._count_no_zero(n) + self._count_no_zero_beautiful(n)

    def _count_no_zero(self, n: int) -> int:
        if n <= 0:
            return 0

        s = str(n)
        m = len(s)

        # All no-zero numbers with fewer digits.
        ans = 0
        p = 1
        for _ in range(1, m):
            p *= 9
            ans += p

        # Same length, digit by digit.
        for i, ch in enumerate(s):
            d = ord(ch) - 48
            if d == 0:
                break
            ans += (d - 1) * (9 ** (m - i - 1))
        else:
            # n itself has no zero digit.
            ans += 1

        return ans

    def _count_no_zero_beautiful(self, n: int) -> int:
        s = str(n)
        m = len(s)
        digits = [ord(ch) - 48 for ch in s]

        # Caps are enough because the final digit sum is at most 9 * m.
        max_sum = 9 * m
        caps = []
        for p in (2, 3, 5, 7):
            e = 0
            x = 1
            while x * p <= max_sum:
                x *= p
                e += 1
            caps.append(e)

        c2, c3, c5, c7 = caps
        c3p = c3 + 1
        c5p = c5 + 1
        c7p = c7 + 1

        # Exact prime exponents for each digit 1..9.
        digit_exp = [
            None,
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

        # Product table for all capped exponent combinations.
        prod_table = [1] * ((c2 + 1) * c3p * c5p * c7p)
        for e2 in range(c2 + 1):
            p2 = 1 << e2
            for e3 in range(c3 + 1):
                p3 = p2 * (3 ** e3)
                for e5 in range(c5 + 1):
                    p5 = p3 * (5 ** e5)
                    for e7 in range(c7 + 1):
                        idx = ((e2 * c3p + e3) * c5p + e5) * c7p + e7
                        prod_table[idx] = p5 * (7 ** e7)

        @lru_cache(maxsize=None)
        def dp(pos: int, tight: bool, started: bool, sm: int,
               e2: int, e3: int, e5: int, e7: int) -> int:
            if pos == m:
                if not started:
                    return 0
                idx = ((e2 * c3p + e3) * c5p + e5) * c7p + e7
                return 1 if prod_table[idx] % sm == 0 else 0

            limit = digits[pos] if tight else 9
            total = 0

            if not started:
                # Leading zero: still not started.
                total += dp(pos + 1, tight and limit == 0, False,
                            0, 0, 0, 0, 0)

                # Start the number with a nonzero digit.
                for d in range(1, limit + 1):
                    de2, de3, de5, de7 = digit_exp[d]
                    total += dp(pos + 1, tight and d == limit, True,
                                d, de2, de3, de5, de7)
            else:
                # Once started, zero digits are not allowed.
                for d in range(1, limit + 1):
                    de2, de3, de5, de7 = digit_exp[d]

                    ne2 = e2 + de2
                    if ne2 > c2:
                        ne2 = c2
                    ne3 = e3 + de3
                    if ne3 > c3:
                        ne3 = c3
                    ne5 = e5 + de5
                    if ne5 > c5:
                        ne5 = c5
                    ne7 = e7 + de7
                    if ne7 > c7:
                        ne7 = c7

                    total += dp(pos + 1, tight and d == limit, True,
                                sm + d, ne2, ne3, ne5, ne7)

            return total

        return dp(0, True, False, 0, 0, 0, 0, 0)