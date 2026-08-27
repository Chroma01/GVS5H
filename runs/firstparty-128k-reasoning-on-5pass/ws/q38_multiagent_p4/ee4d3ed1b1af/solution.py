class Solution:
    def shortestMatchingSubstring(self, s: str, p: str) -> int:
        def occurrences(text, pat):
            m = len(pat)
            if m == 0 or m > len(text):
                return []
            pi = [0] * m
            for i in range(1, m):
                j = pi[i - 1]
                while j > 0 and pat[i] != pat[j]:
                    j = pi[j - 1]
                if pat[i] == pat[j]:
                    j += 1
                pi[i] = j

            res = []
            j = 0
            for i, ch in enumerate(text):
                while j > 0 and ch != pat[j]:
                    j = pi[j - 1]
                if ch == pat[j]:
                    j += 1
                if j == m:
                    res.append(i - m + 1)
                    j = pi[j - 1]
            return res

        A, B, C = p.split('*')

        if not A and not B and not C:
            return 0

        occA = occurrences(s, A) if A else []
        occB = occurrences(s, B) if B else []
        occC = occurrences(s, C) if C else []

        if A and not occA:
            return -1
        if B and not occB:
            return -1
        if C and not occC:
            return -1

        la, lb, lc = len(A), len(B), len(C)
        INF = 10**18
        ans = INF

        if A and B and C:
            pa = -1
            pc = 0
            for b in occB:
                while pa + 1 < len(occA) and occA[pa + 1] + la <= b:
                    pa += 1
                if pa < 0:
                    continue

                while pc < len(occC) and occC[pc] < b + lb:
                    pc += 1
                if pc == len(occC):
                    continue

                cand = occC[pc] + lc - occA[pa]
                if cand < ans:
                    ans = cand

        elif A and B:
            pa = -1
            for b in occB:
                while pa + 1 < len(occA) and occA[pa + 1] + la <= b:
                    pa += 1
                if pa < 0:
                    continue

                cand = b + lb - occA[pa]
                if cand < ans:
                    ans = cand

        elif A and C:
            pa = -1
            for c in occC:
                while pa + 1 < len(occA) and occA[pa + 1] + la <= c:
                    pa += 1
                if pa < 0:
                    continue

                cand = c + lc - occA[pa]
                if cand < ans:
                    ans = cand

        elif B and C:
            pc = 0
            for b in occB:
                while pc < len(occC) and occC[pc] < b + lb:
                    pc += 1
                if pc == len(occC):
                    continue

                cand = occC[pc] + lc - b
                if cand < ans:
                    ans = cand

        elif A:
            return la
        elif B:
            return lb
        elif C:
            return lc

        return -1 if ans == INF else ans