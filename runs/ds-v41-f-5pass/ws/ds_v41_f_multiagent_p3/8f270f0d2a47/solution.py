from collections import defaultdict

class Solution:
    def beautifulNumbers(self, l: int, r: int) -> int:
        MAXL = 9  # r < 10^9 => at most 9 digits

        # suffix[j][(s, p)] = number of exactly-j-digit strings (each digit 0..9,
        # leading zeros allowed) whose digit-sum is s and digit-product is p.
        # product 0 is absorbing (any zero digit).  Built incrementally.
        suffix = [{(0, 1): 1}]
        for _ in range(MAXL):
            prev = suffix[-1]
            cur = defaultdict(int)
            for (s, p), c in prev.items():
                for d in range(10):
                    cur[(s + d, p * d)] += c
            suffix.append(dict(cur))

        def count_upto(n: int) -> int:
            if n <= 0:
                return 0
            digits = [int(ch) for ch in str(n)]
            L = len(digits)
            total = 0

            # numbers with 1 .. L-1 digits (first digit 1..9)
            for k in range(1, L):
                suf = suffix[k - 1]
                for d in range(1, 10):
                    for (s0, p0), c in suf.items():
                        s = s0 + d
                        p = p0 * d
                        if p == 0 or p % s == 0:   # s >= 1 here
                            total += c

            # numbers with exactly L digits and <= n (tight prefix walk)
            psum, pprod = 0, 1
            for i in range(L):
                suf = suffix[L - i - 1]
                low = 1 if i == 0 else 0
                for d in range(low, digits[i]):
                    s = psum + d
                    p = pprod * d
                    for (s0, p0), c in suf.items():
                        ss = s + s0
                        pp = p * p0
                        if pp == 0 or pp % ss == 0:
                            total += c
                psum += digits[i]
                pprod *= digits[i]

            # n itself
            if pprod == 0 or pprod % psum == 0:
                total += 1
            return total

        return count_upto(r) - count_upto(l - 1)