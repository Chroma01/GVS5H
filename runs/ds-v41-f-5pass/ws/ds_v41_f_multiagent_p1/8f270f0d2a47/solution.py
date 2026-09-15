from functools import lru_cache


class Solution:
    def beautifulNumbers(self, l: int, r: int) -> int:
        # free(rem, started, s, p) = number of ways to fill `rem` free
        # decimal digits (0-9) so that, starting from prefix state
        # (started, s = digit sum, p = digit product), the final number is
        # beautiful.  Independent of n, so it is shared by both count calls.
        @lru_cache(maxsize=None)
        def free(rem: int, started: bool, s: int, p: int) -> int:
            if rem == 0:
                return 1 if (started and s > 0 and p % s == 0) else 0
            total = 0
            if started:
                for d in range(10):
                    total += free(rem - 1, True, s + d, p * d)
            else:
                # leading zero: still unstarted (counts shorter numbers)
                total += free(rem - 1, False, 0, 1)
                for d in range(1, 10):
                    total += free(rem - 1, True, d, d)
            return total

        def count(n: int) -> int:
            # number of beautiful integers in [1, n]
            if n <= 0:
                return 0
            digits = list(map(int, str(n)))
            L = len(digits)
            res = 0
            started = False
            s = 0
            p = 1
            for i in range(L):
                di = digits[i]
                # branch off with a strictly smaller digit; the rest is free
                for d in range(di):
                    if not started:
                        if d == 0:
                            res += free(L - 1 - i, False, 0, 1)
                        else:
                            res += free(L - 1 - i, True, d, d)
                    else:
                        res += free(L - 1 - i, True, s + d, p * d)
                # stay tight with the actual digit
                if not started:
                    if di != 0:
                        started = True
                        s = di
                        p = di
                else:
                    s += di
                    p *= di
            if started and s > 0 and p % s == 0:
                res += 1
            return res

        return count(r) - count(l - 1)