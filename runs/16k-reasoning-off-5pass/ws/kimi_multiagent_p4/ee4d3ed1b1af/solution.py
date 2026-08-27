import bisect
from typing import List


class Solution:
    def shortestMatchingSubstring(self, s: str, p: str) -> int:
        # Split pattern into three literal parts around the two '*'
        star1 = p.index('*')
        star2 = p.index('*', star1 + 1)
        A = p[:star1]
        B = p[star1 + 1:star2]
        C = p[star2 + 1:]

        n = len(s)

        def occurrences(pat: str) -> List[int]:
            """All start indices where pat occurs in s (KMP)."""
            m = len(pat)
            if m == 0:
                return list(range(n + 1))  # empty string occurs everywhere
            # Build prefix function
            pi = [0] * m
            k = 0
            for i in range(1, m):
                while k > 0 and pat[i] != pat[k]:
                    k = pi[k - 1]
                if pat[i] == pat[k]:
                    k += 1
                pi[i] = k
            res = []
            k = 0
            for i, ch in enumerate(s):
                while k > 0 and ch != pat[k]:
                    k = pi[k - 1]
                if ch == pat[k]:
                    k += 1
                if k == m:
                    res.append(i - m + 1)
                    k = pi[k - 1]
            return res

        la, lb, lc = len(A), len(B), len(C)
        INF = float('inf')
        ans = INF

        if lb > 0:
            startsA = occurrences(A)
            startsB = occurrences(B)
            startsC = occurrences(C)
            if not startsA or not startsB or not startsC:
                return -1
            for j in startsB:
                # largest A-start i with i + la <= j
                idx = bisect.bisect_right(startsA, j - la) - 1
                if idx < 0:
                    continue
                i = startsA[idx]
                # smallest C-start k with k >= j + lb
                idx2 = bisect.bisect_left(startsC, j + lb)
                if idx2 == len(startsC):
                    continue
                k = startsC[idx2]
                cur = k + lc - i
                if cur < ans:
                    ans = cur
        else:
            # B is empty: match = A + x + C, need A_end <= C_start
            if la == 0 and lc == 0:
                return 0  # p == "**"
            startsA = occurrences(A)
            startsC = occurrences(C)
            if not startsA or not startsC:
                return -1
            if la == 0:
                # p == "**C": shortest match is C itself
                return lc
            if lc == 0:
                # p == "A**": shortest match is A itself
                return la
            for i in startsA:
                idx = bisect.bisect_left(startsC, i + la)
                if idx == len(startsC):
                    break  # later i only makes it worse / equally impossible
                cur = startsC[idx] + lc - i
                if cur < ans:
                    ans = cur

        return -1 if ans == INF else ans