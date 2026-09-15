class Solution:
    def shortestMatchingSubstring(self, s: str, p: str) -> int:
        n = len(s)
        A, B, C = p.split('*')          # exactly two '*', so exactly three parts
        INF = float('inf')

        # KMP: return start indices of all (overlapping) occurrences of pat in text
        def kmp_occ(text, pat):
            m = len(pat)
            lps = [0] * m
            k = 0
            for i in range(1, m):
                c = pat[i]
                while k and c != pat[k]:
                    k = lps[k - 1]
                if c == pat[k]:
                    k += 1
                    lps[i] = k
            occ = []
            j = 0
            for i, c in enumerate(text):
                while j and c != pat[j]:
                    j = lps[j - 1]
                if c == pat[j]:
                    j += 1
                if j == m:
                    occ.append(i - m + 1)
                    j = lps[j - 1]
            return occ

        lenA, lenB, lenC = len(A), len(B), len(C)

        # nextB[i] = smallest start >= i of an occurrence of B (INF if none)
        if B:
            nxtB = [INF] * (n + 2)
            for o in kmp_occ(s, B):
                nxtB[o] = o
            for i in range(n, -1, -1):
                if nxtB[i + 1] < nxtB[i]:
                    nxtB[i] = nxtB[i + 1]
        else:
            nxtB = None   # empty B "occurs" at every position i, handled inline

        if C:
            nxtC = [INF] * (n + 2)
            for o in kmp_occ(s, C):
                nxtC[o] = o
            for i in range(n, -1, -1):
                if nxtC[i + 1] < nxtC[i]:
                    nxtC[i] = nxtC[i + 1]
        else:
            nxtC = None

        starts = kmp_occ(s, A) if A else range(n + 1)
        best = -1
        for l in starts:
            p1 = l + lenA                 # position right after A (end of first star)
            if p1 > n:
                continue
            if nxtB is not None:
                b = nxtB[p1]
                if b == INF:
                    continue
            else:
                b = p1                    # B empty, place it at p1
            p2 = b + lenB                 # position right after B
            if p2 > n:
                continue
            if nxtC is not None:
                c = nxtC[p2]
                if c == INF:
                    continue
            else:
                c = p2                    # C empty, place it at p2
            length = c + lenC - l
            if best < 0 or length < best:
                best = length
        return best