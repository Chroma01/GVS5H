from bisect import bisect_left, bisect_right

class Solution:
    def shortestMatchingSubstring(self, s: str, p: str) -> int:
        A, B, C = p.split('*', 2)
        n = len(s)

        def occurrences(pat: str):
            m = len(pat)
            if m == 0:
                return None
            if m > n:
                return []

            t = pat + '#' + s
            z = [0] * len(t)
            l = r = 0
            lt = len(t)

            for i in range(1, lt):
                if i <= r:
                    zi = min(r - i + 1, z[i - l])
                else:
                    zi = 0

                while i + zi < lt and t[zi] == t[i + zi]:
                    zi += 1

                z[i] = zi
                if i + zi - 1 > r:
                    l = i
                    r = i + zi - 1

            off = m + 1
            return [i for i in range(n - m + 1) if z[off + i] >= m]

        occA = occurrences(A)
        occB = occurrences(B)
        occC = occurrences(C)

        if (A and not occA) or (B and not occB) or (C and not occC):
            return -1

        la, lb, lc = len(A), len(B), len(C)
        lower = la + lb + lc

        if lower == 0:
            return 0
        if lower > n:
            return -1

        ans = n + 1
        bl = bisect_left
        br = bisect_right

        a_empty = (A == '')
        c_empty = (C == '')
        b_iter = range(n + 1) if B == '' else occB

        for b in b_iter:
            if a_empty:
                a = b
            else:
                idx = br(occA, b - la) - 1
                if idx < 0:
                    continue
                a = occA[idx]

            start_c = b + lb
            if c_empty:
                if start_c > n:
                    continue
                c = start_c
            else:
                idx = bl(occC, start_c)
                if idx == len(occC):
                    continue
                c = occC[idx]

            length = c + lc - a
            if length < ans:
                ans = length
                if ans == lower:
                    break

        return -1 if ans == n + 1 else ans