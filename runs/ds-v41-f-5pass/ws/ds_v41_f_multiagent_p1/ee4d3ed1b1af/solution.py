class Solution:
    def shortestMatchingSubstring(self, s: str, p: str) -> int:
        # p = A * B * C  (exactly two stars)
        i1 = p.index('*')
        i2 = p.index('*', i1 + 1)
        A = p[:i1]
        B = p[i1 + 1:i2]
        C = p[i2 + 1:]
        n = len(s)
        INF = float('inf')

        def find_all(text, pat):
            """All (possibly overlapping) start indices of pat in text, via KMP: O(len(text)+len(pat))."""
            m = len(pat)
            if m == 0:
                return []
            pi = [0] * m
            j = 0
            for i in range(1, m):
                c = pat[i]
                while j and c != pat[j]:
                    j = pi[j - 1]
                if c == pat[j]:
                    j += 1
                pi[i] = j
            res = []
            j = 0
            for i, c in enumerate(text):
                while j and c != pat[j]:
                    j = pi[j - 1]
                if c == pat[j]:
                    j += 1
                if j == m:
                    res.append(i - m + 1)
                    j = pi[j - 1]
            return res

        lenA, lenB, lenC = len(A), len(B), len(C)

        # ---- B empty: pattern is A*C (or a single literal / empty) ----
        if lenB == 0:
            if lenA == 0 and lenC == 0:
                return 0                      # "**"
            if lenA == 0:                     # *C
                return lenC if s.find(C) != -1 else -1
            if lenC == 0:                     # A*
                return lenA if s.find(A) != -1 else -1
            occA = find_all(s, A)
            occC = find_all(s, C)
            if not occA or not occC:
                return -1
            latestA = [-1] * (n + 1)          # latestA[x] = max A-start with A-end <= x
            for a0 in occA:
                a1 = a0 + lenA
                if a0 > latestA[a1]:
                    latestA[a1] = a0
            for x in range(1, n + 1):
                if latestA[x - 1] > latestA[x]:
                    latestA[x] = latestA[x - 1]
            best = INF
            for c0 in occC:
                a0 = latestA[c0]
                if a0 != -1:
                    span = c0 + lenC - a0
                    if span < best:
                        best = span
            return best if best < INF else -1

        # ---- B non-empty: anchor on each occurrence of B ----
        occB = find_all(s, B)
        if not occB:
            return -1

        latestA = None
        if lenA > 0:
            occA = find_all(s, A)
            latestA = [-1] * (n + 1)
            for a0 in occA:
                a1 = a0 + lenA
                if a0 > latestA[a1]:
                    latestA[a1] = a0
            for x in range(1, n + 1):
                if latestA[x - 1] > latestA[x]:
                    latestA[x] = latestA[x - 1]

        nextC = None
        if lenC > 0:
            occC = find_all(s, C)
            nextC = [INF] * (n + 1)           # nextC[x] = min C-start >= x
            for c0 in occC:
                if c0 < nextC[c0]:
                    nextC[c0] = c0
            for x in range(n - 1, -1, -1):
                if nextC[x + 1] < nextC[x]:
                    nextC[x] = nextC[x + 1]

        best = INF
        for b0 in occB:
            b1 = b0 + lenB
            if lenA == 0:
                start = b0                    # A is empty -> substring begins at B
            else:
                start = latestA[b0]           # rightmost A that ends at/before b0
                if start == -1:
                    continue
            if lenC == 0:
                end = b1                      # C is empty -> substring ends at B
            else:
                c0 = nextC[b1]                # earliest C that starts at/after b1
                if c0 == INF:
                    continue
                end = c0 + lenC
            span = end - start
            if span < best:
                best = span
        return best if best < INF else -1