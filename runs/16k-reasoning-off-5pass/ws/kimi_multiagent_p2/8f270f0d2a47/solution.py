from functools import lru_cache

class Solution:
    def beautifulNumbers(self, l: int, r: int) -> int:
        return self._count(r) - self._count(l - 1)

    def _count(self, n: int) -> int:
        # Count beautiful numbers in [1, n] (0 is not beautiful: digit sum is 0).
        if n <= 0:
            return 0
        digits = list(map(int, str(n)))
        L = len(digits)

        @lru_cache(maxsize=None)
        def dp(pos: int, s: int, p: int, started: bool) -> int:
            # pos: current index into digits
            # s: digit sum so far
            # p: digit product so far (0 means a zero digit has appeared)
            # started: whether a non-leading-zero digit has been placed
            if pos == L:
                if not started:
                    return 0  # the number 0
                return 1 if p % s == 0 else 0

            limit = digits[pos]
            total = 0
            for d in range(limit + 1):
                if not started and d == 0:
                    # still leading zeros
                    total += dp(pos + 1, s, p, False)
                else:
                    ns = s + d
                    np_ = p * d
                    if np_ == 0:
                        # product is 0 -> divisible by any positive sum.
                        # All completions of the remaining positions are beautiful.
                        total += 10 ** (L - pos - 1)
                    else:
                        total += dp(pos + 1, ns, np_, True)
            return total

        # Tight handling: we only memoize non-tight states. To keep it simple and
        # correct, we run the DP with the tight path explored via a wrapper that
        # does not cache tight states. Here we instead make the DP always free
        # (limit 9) and handle tightness by recursion on the prefix.
        dp.cache_clear()

        @lru_cache(maxsize=None)
        def free_dp(pos: int, s: int, p: int, started: bool) -> int:
            # Counts completions from position pos with digits 0..9 freely.
            if pos == L:
                if not started:
                    return 0
                return 1 if p % s == 0 else 0
            total = 0
            for d in range(10):
                if not started and d == 0:
                    total += free_dp(pos + 1, s, p, False)
                else:
                    ns = s + d
                    np_ = p * d
                    if np_ == 0:
                        total += 10 ** (L - pos - 1)
                    else:
                        total += free_dp(pos + 1, ns, np_, True)
            return total

        # Walk the tight path, branching into free_dp for smaller digits.
        s = 0
        p = 1
        started = False
        ans = 0
        for pos in range(L):
            limit = digits[pos]
            for d in range(limit):
                if not started and d == 0:
                    ans += free_dp(pos + 1, s, p, False)
                else:
                    ns = s + d
                    np_ = p * d
                    if np_ == 0:
                        ans += 10 ** (L - pos - 1)
                    else:
                        ans += free_dp(pos + 1, ns, np_, True)
            # advance the tight prefix with d == limit
            if not started and limit == 0:
                pass
            else:
                s += limit
                p *= limit
                started = True
                if p == 0:
                    # The tight number itself contains a zero -> beautiful (sum > 0).
                    ans += 1
                    return ans
        # Tight number itself, no zero encountered.
        if started and p % s == 0:
            ans += 1
        return ans