from typing import List

class Solution:
    def minOperations(self, queries: List[List[int]]) -> int:
        # powers of 4 up to 1e9
        powers = []
        p = 1
        while p <= 10**9:
            powers.append(p)
            p *= 4

        # d(x) = number of powers 1,4,16,... that are <= x  (for x >= 1)
        # F(n) = sum_{x=1}^{n} d(x) = sum_{j>=1} max(0, n - 4^{j-1} + 1)
        def F(n: int) -> int:
            if n <= 0:
                return 0
            s = 0
            for pw in powers:
                if pw > n:
                    break
                s += n - pw + 1
            return s

        def d(x: int) -> int:
            # smallest k with 4^k > x  -> equals count of powers <= x
            c = 0
            for pw in powers:
                if pw > x:
                    break
                c += 1
            return c

        total = 0
        for l, r in queries:
            S = F(r) - F(l - 1)
            # min ops = max(max single-element cost, ceil(total cost / 2))
            total += max(d(r), (S + 1) // 2)
        return total