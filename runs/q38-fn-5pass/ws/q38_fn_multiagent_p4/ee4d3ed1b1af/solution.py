from bisect import bisect_left, bisect_right

class Solution:
    def shortestMatchingSubstring(self, s: str, p: str) -> int:
        def kmp(text: str, pat: str):
            m = len(pat)
            if m == 0 or m > len(text):
                return []

            lps = [0] * m
            length = 0
            i = 1
            while i < m:
                if pat[i] == pat[length]:
                    length += 1
                    lps[i] = length
                    i += 1
                elif length:
                    length = lps[length - 1]
                else:
                    lps[i] = 0
                    i += 1

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

        A, B, C = p.split('*')

        if not A and not B and not C:
            return 0

        occA = kmp(s, A) if A else []
        occB = kmp(s, B) if B else []
        occC = kmp(s, C) if C else []

        if (A and not occA) or (B and not occB) or (C and not occC):
            return -1

        lenA, lenB, lenC = len(A), len(B), len(C)
        INF = 10**18
        ans = INF

        if B:
            for b in occB:
                if A:
                    ia = bisect_right(occA, b - lenA) - 1
                    if ia < 0:
                        continue
                    start = occA[ia]
                else:
                    start = b

                if C:
                    ic = bisect_left(occC, b + lenB)
                    if ic == len(occC):
                        continue
                    end = occC[ic] + lenC
                else:
                    end = b + lenB

                ans = min(ans, end - start)
        else:
            if C:
                for c in occC:
                    if A:
                        ia = bisect_right(occA, c - lenA) - 1
                        if ia < 0:
                            continue
                        start = occA[ia]
                    else:
                        start = c

                    end = c + lenC
                    ans = min(ans, end - start)
            else:
                ans = lenA if A else 0

        return -1 if ans == INF else ans