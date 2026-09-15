class Solution:
    def shortestMatchingSubstring(self, s: str, p: str) -> int:
        A, B, C = p.split('*')          # exactly two '*', so exactly 3 parts
        n = len(s)
        la, lb, lc = len(A), len(B), len(C)

        def kmp_all(text, pat):
            """All (overlapping) start indices of pat in text."""
            m = len(pat)
            lps = [0] * m
            j = 0
            for i in range(1, m):
                while j and pat[i] != pat[j]:
                    j = lps[j - 1]
                if pat[i] == pat[j]:
                    j += 1
                lps[i] = j
            res = []
            j = 0
            for i, ch in enumerate(text):
                while j and ch != pat[j]:
                    j = lps[j - 1]
                if ch == pat[j]:
                    j += 1
                if j == m:
                    res.append(i - m + 1)
                    j = lps[j - 1]
            return res

        # p == "**"  -> empty substring matches
        if la == 0 and lb == 0 and lc == 0:
            return 0

        INF = 10 ** 15
        occA = kmp_all(s, A) if la else None
        occB = kmp_all(s, B) if lb else None
        occC = kmp_all(s, C) if lc else None

        # nextC[x] = smallest C start >= x  (INF if none)
        if lc:
            nextC = [INF] * (n + 1)
            for c in occC:
                nextC[c] = c
            for x in range(n - 1, -1, -1):
                if nextC[x + 1] < nextC[x]:
                    nextC[x] = nextC[x + 1]

        # bestAend[x] = largest A end <= x, else -1
        if la:
            bestAend = [-1] * (n + 1)
            present = [False] * (n + 1)
            for a in occA:
                present[a + la] = True
            cur = -1
            for x in range(n + 1):
                if present[x]:
                    cur = x
                bestAend[x] = cur

        best = INF

        if la and lb and lc:
            # start = A_start, end = C_end; for fixed b take latest A before b
            # and earliest C after b+lb
            for b in occB:
                aEnd = bestAend[b]
                if aEnd < 0:
                    continue
                c = nextC[b + lb]
                if c >= INF:
                    continue
                cand = c + lc - aEnd + la
                if cand < best:
                    best = cand
            return best if best < INF else -1

        if not la and lb and lc:
            # start = b, end = c+lc
            for b in occB:
                c = nextC[b + lb]
                if c >= INF:
                    continue
                cand = c + lc - b
                if cand < best:
                    best = cand
            return best if best < INF else -1

        if la and lb and not lc:
            # start = a, end = b+lb
            for b in occB:
                aEnd = bestAend[b]
                if aEnd < 0:
                    continue
                cand = b + lb - aEnd + la
                if cand < best:
                    best = cand
            return best if best < INF else -1

        if la and not lb and lc:
            # B empty: A then C in order, start = a, end = c+lc
            for a in occA:
                c = nextC[a + la]
                if c >= INF:
                    continue
                cand = c + lc - a
                if cand < best:
                    best = cand
            return best if best < INF else -1

        # exactly one non-empty segment
        if la:
            return la if occA else -1
        if lb:
            return lb if occB else -1
        return lc if occC else -1