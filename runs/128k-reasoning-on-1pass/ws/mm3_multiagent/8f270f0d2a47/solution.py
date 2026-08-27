import sys
from functools import lru_cache

# Maximum possible digit sum for a number up to 10^9 - 1 (9 digits)
MAX_SUM = 81

# Precompute the exponent requirements for each possible digit sum.
# need[s] = (a2, a3, a5, a7) meaning s = 2^a2 * 3^a3 * 5^a5 * 7^a7,
# or None if s contains a prime factor other than 2,3,5,7 (then no
# number without a zero digit can be beautiful).
need = [None] * (MAX_SUM + 1)
for s in range(1, MAX_SUM + 1):
    a2 = a3 = a5 = a7 = 0
    t = s
    possible = True
    for p in (2, 3, 5, 7):
        while t % p == 0:
            if p == 2:
                a2 += 1
            elif p == 3:
                a3 += 1
            elif p == 5:
                a5 += 1
            else:  # p == 7
                a7 += 1
            t //= p
    if t != 1:  # there is a prime factor > 7
        possible = False
    if possible:
        need[s] = (a2, a3, a5, a7)

# Mapping from digit (1-9) to increments of the prime exponents
# (2, 3, 5, 7) contributed by that digit.
digit_inc = [(0, 0, 0, 0) for _ in range(10)]
digit_inc[1] = (0, 0, 0, 0)
digit_inc[2] = (1, 0, 0, 0)
digit_inc[3] = (0, 1, 0, 0)
digit_inc[4] = (2, 0, 0, 0)
digit_inc[5] = (0, 0, 1, 0)
digit_inc[6] = (1, 1, 0, 0)
digit_inc[7] = (0, 0, 0, 1)
digit_inc[8] = (3, 0, 0, 0)
digit_inc[9] = (0, 2, 0, 0)

class Solution:
    def beautifulNumbers(self, l: int, r: int) -> int:
        """Return the number of beautiful integers in the interval [l, r]."""
        def count_upto(X: int) -> int:
            """Count beautiful numbers in [1, X]."""
            if X <= 0:
                return 0
            digits = list(map(int, str(X)))
            n = len(digits)

            @lru_cache(maxsize=None)
            def zero_dp(pos: int, tight: bool) -> int:
                """Count completions of the suffix when a zero digit has already appeared.
                The product is then zero, so the whole number is automatically beautiful."""
                if pos == n:
                    return 1
                if not tight:
                    # any digit 0..9 for each remaining position
                    return pow(10, n - pos)
                limit = digits[pos]
                total = 0
                for d in range(limit + 1):
                    ntight = tight and (d == limit)
                    total += zero_dp(pos + 1, ntight)
                return total

            @lru_cache(maxsize=None)
            def dfs(pos: int, tight: bool, started: bool,
                    s: int, e2: int, e3: int, e5: int, e7: int) -> int:
                """Count beautiful numbers that can be built from the current state."""
                if pos == n:
                    if not started:
                        return 0          # no positive number formed
                    # The product is non‑zero (otherwise we would have used zero_dp)
                    req = need[s]
                    if req is None:
                        return 0
                    a2, a3, a5, a7 = req
                    return 1 if (e2 >= a2 and e3 >= a3 and
                                 e5 >= a5 and e7 >= a7) else 0

                limit = digits[pos] if tight else 9
                total = 0
                for d in range(limit + 1):
                    ntight = tight and (d == limit)
                    if not started and d == 0:
                        # still only leading zeros
                        total += dfs(pos + 1, ntight, False, 0, 0, 0, 0, 0)
                    else:
                        if d == 0:
                            # a zero digit appears → product becomes 0 → always beautiful
                            total += zero_dp(pos + 1, ntight)
                        else:
                            de2, de3, de5, de7 = digit_inc[d]
                            ns = s + d
                            ne2 = e2 + de2
                            ne3 = e3 + de3
                            ne5 = e5 + de5
                            ne7 = e7 + de7
                            total += dfs(pos + 1, ntight, True,
                                         ns, ne2, ne3, ne5, ne7)
                return total

            # Start with an empty prefix
            return dfs(0, True, False, 0, 0, 0, 0, 0)

        # Numbers in [l, r] = count(r) - count(l-1)
        return count_upto(r) - count_upto(l - 1)