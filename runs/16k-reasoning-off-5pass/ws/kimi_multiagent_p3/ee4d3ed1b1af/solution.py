class Solution:
    def shortestMatchingSubstring(self, s: str, p: str) -> int:
        n = len(s)

        # Split p into A, B, C at the two '*'
        first = p.index('*')
        second = p.index('*', first + 1)
        A = p[:first]
        B = p[first + 1:second]
        C = p[second + 1:]
        la, lb, lc = len(A), len(B), len(C)

        # KMP: return list of start positions where pat occurs in s
        def kmp_occurrences(pat: str):
            m = len(pat)
            if m == 0:
                return list(range(n + 1))  # empty pattern matches everywhere
            # build prefix function
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
            for i in range(n):
                while j > 0 and s[i] != pat[j]:
                    j = pi[j - 1]
                if s[i] == pat[j]:
                    j += 1
                if j == m:
                    res.append(i - m + 1)
                    j = pi[j - 1]
            return res

        occA = kmp_occurrences(A)
        occB = kmp_occurrences(B)
        occC = kmp_occurrences(C)

        NEG = -10**18
        POS = 10**18

        # prevA[k] = latest A-start <= k, for k in 0..n
        prevA = [NEG] * (n + 1)
        for a in occA:
            if 0 <= a <= n:
                prevA[a] = a
        for k in range(1, n + 1):
            if prevA[k] < prevA[k - 1]:
                prevA[k] = prevA[k - 1]

        # nextC[k] = earliest C-start >= k, for k in 0..n
        nextC = [POS] * (n + 1)
        for c in occC:
            if 0 <= c <= n:
                nextC[c] = c
        for k in range(n - 1, -1, -1):
            if nextC[k] > nextC[k + 1]:
                nextC[k] = nextC[k + 1]

        ans = POS
        for b in occB:
            # A must end at or before B starts: a + la <= b  =>  a <= b - la
            ka = b - la
            if ka < 0:
                continue
            a = prevA[ka]
            if a == NEG:
                continue
            # C must start at or after B ends: c >= b + lb
            kc = b + lb
            if kc > n:
                continue
            c = nextC[kc]
            if c == POS:
                continue
            cand = c + lc - a
            if cand < ans:
                ans = cand

        return -1 if ans == POS else ans