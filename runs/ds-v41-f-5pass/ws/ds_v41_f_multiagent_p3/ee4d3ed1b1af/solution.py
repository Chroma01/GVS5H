from bisect import bisect_left, bisect_right


class Solution:
    def shortestMatchingSubstring(self, s: str, p: str) -> int:
        # p has exactly two '*', so it splits into exactly three literal parts
        A, B, C = p.split('*')

        def kmp(text, pat):
            """Return sorted list of all (overlapping) start indices of pat in text."""
            m = len(pat)
            if m == 0:
                return []
            # build lps
            lps = [0] * m
            j = 0
            for i in range(1, m):
                while j and pat[i] != pat[j]:
                    j = lps[j - 1]
                if pat[i] == pat[j]:
                    j += 1
                lps[i] = j
            # search
            res = []
            j = 0
            n = len(text)
            for i in range(n):
                while j and text[i] != pat[j]:
                    j = lps[j - 1]
                if text[i] == pat[j]:
                    j += 1
                    if j == m:
                        res.append(i - m + 1)
                        j = lps[j - 1]
            return res

        # Collect nonempty literal segments in order, with their occurrences
        segments = []
        for lit in (A, B, C):
            if lit:
                segments.append((lit, kmp(s, lit)))

        k = len(segments)
        if k == 0:
            # pattern "**" -> empty substring
            return 0

        if k == 1:
            lit, occ = segments[0]
            return len(lit) if occ else -1

        if k == 2:
            (l1, o1), (l2, o2) = segments
            # pattern: first-literal * second-literal *
            best = -1
            for y in o2:
                idx = bisect_right(o1, y - l1) - 1
                if idx >= 0:
                    cand = y + l2 - o1[idx]
                    if best < 0 or cand < best:
                        best = cand
            return best

        # three segments: A * B * C
        (lA, oA), (lB, oB), (lC, oC) = segments
        best = -1
        for b in oB:
            ia = bisect_right(oA, b - lA) - 1
            if ia < 0:
                continue
            ic = bisect_left(oC, b + lB)
            if ic >= len(oC):
                continue
            cand = oC[ic] + lC - oA[ia]
            if best < 0 or cand < best:
                best = cand
        return best