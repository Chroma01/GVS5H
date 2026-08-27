class Solution:
    def shortestMatchingSubstring(self, s: str, p: str) -> int:
        n = len(s)

        # Split p into three literal parts around the two '*'
        star1 = p.index('*')
        star2 = p.index('*', star1 + 1)
        A = p[:star1]
        B = p[star1 + 1:star2]
        C = p[star2 + 1:]
        la, lb, lc = len(A), len(B), len(C)

        # KMP prefix function
        def prefix_function(t: str):
            pi = [0] * len(t)
            k = 0
            for i in range(1, len(t)):
                while k > 0 and t[i] != t[k]:
                    k = pi[k - 1]
                if t[i] == t[k]:
                    k += 1
                pi[i] = k
            return pi

        # occ[i] = True if literal `lit` occurs in s starting at index i.
        # Valid start positions: 0..n-len(lit); empty literal occurs at 0..n.
        def occurrences(lit: str):
            L = len(lit)
            if L == 0:
                return [True] * (n + 1)
            occ = [False] * (n + 1)
            if L > n:
                return occ
            pi = prefix_function(lit)
            k = 0
            for i in range(n):
                while k > 0 and s[i] != lit[k]:
                    k = pi[k - 1]
                if s[i] == lit[k]:
                    k += 1
                if k == L:
                    occ[i - L + 1] = True
                    k = pi[k - 1]
            return occ

        occA = occurrences(A)
        occB = occurrences(B)
        occC = occurrences(C)

        INF = n + 5

        # nextB[x] = smallest start position >= x where B occurs (INF if none)
        nextB = [INF] * (n + 2)
        nxt = INF
        for x in range(n, -1, -1):
            if occB[x]:
                nxt = x
            nextB[x] = nxt

        # nextC[x] = smallest start position >= x where C occurs (INF if none)
        nextC = [INF] * (n + 2)
        nxt = INF
        for x in range(n, -1, -1):
            if occC[x]:
                nxt = x
            nextC[x] = nxt

        ans = INF
        # For each occurrence of A starting at i, greedily take the earliest
        # valid B then earliest valid C; this minimizes the substring length
        # for that i.
        for i in range(0, n - la + 1 if la > 0 else n + 1):
            if not occA[i]:
                continue
            b = nextB[i + la]
            if b == INF:
                continue
            c = nextC[b + lb]
            if c == INF:
                continue
            cand = c + lc - i
            if cand < ans:
                ans = cand
                if ans == 0:
                    break

        return -1 if ans == INF else ans