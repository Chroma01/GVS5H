from typing import List

class Solution:
    def minOperations(self, queries: List[List[int]]) -> int:
        MAXV = 10**9
        # c(x) = number of divisions by 4 to reach 0 = floor(log_4 x) + 1.
        # c is constant = k on [4^(k-1), 4^k - 1].
        lows, highs, ks = [], [], []
        p, k = 1, 1
        while p <= MAXV:
            lows.append(p)
            highs.append(p * 4 - 1)
            ks.append(k)
            p *= 4
            k += 1
        m = len(lows)
        # pre[i] = sum of c(x) over [1, lows[i]-1]
        pre = [0] * (m + 1)
        for i in range(m):
            pre[i + 1] = pre[i] + ks[i] * (highs[i] - lows[i] + 1)

        def idx_of(x):
            lo, hi, idx = 0, m - 1, 0
            while lo <= hi:
                mid = (lo + hi) // 2
                if lows[mid] <= x:
                    idx = mid
                    lo = mid + 1
                else:
                    hi = mid - 1
            return idx

        def F(n):
            if n <= 0:
                return 0
            i = idx_of(n)
            return pre[i] + ks[i] * (n - lows[i] + 1)

        total = 0
        for l, r in queries:
            D = F(r) - F(l - 1)   # total divisions required
            M = ks[idx_of(r)]     # c nondecreasing => max is c(r)
            half = (D + 1) // 2
            total += M if M > half else half
        return total