from bisect import bisect_left


class Solution:
    def shortestMatchingSubstring(self, s: str, p: str) -> int:
        first = p.index('*')
        second = p.index('*', first + 1)

        a = p[:first]
        b = p[first + 1:second]
        c = p[second + 1:]

        def occurrences(pattern: str):
            if not pattern:
                return []

            m = len(pattern)
            lps = [0] * m
            j = 0
            for i in range(1, m):
                while j and pattern[i] != pattern[j]:
                    j = lps[j - 1]
                if pattern[i] == pattern[j]:
                    j += 1
                lps[i] = j

            result = []
            j = 0
            for i, ch in enumerate(s):
                while j and ch != pattern[j]:
                    j = lps[j - 1]
                if ch == pattern[j]:
                    j += 1
                if j == m:
                    result.append(i - m + 1)
                    j = lps[j - 1]
            return result

        la, lb, lc = len(a), len(b), len(c)

        # All parts are empty: "**"
        if not a and not b and not c:
            return 0

        occ_a = occurrences(a) if a else []
        occ_b = occurrences(b) if b else []
        occ_c = occurrences(c) if c else []

        best = float("inf")

        if a:
            for pos_a in occ_a:
                if b:
                    idx_b = bisect_left(occ_b, pos_a + la)
                    if idx_b == len(occ_b):
                        continue
                    pos_b = occ_b[idx_b]
                    end_after_b = pos_b + lb
                else:
                    end_after_b = pos_a + la

                if c:
                    idx_c = bisect_left(occ_c, end_after_b)
                    if idx_c == len(occ_c):
                        continue
                    end = occ_c[idx_c] + lc
                else:
                    end = end_after_b

                best = min(best, end - pos_a)

        elif b:
            # The substring can start exactly at the occurrence of B.
            if c:
                for pos_b in occ_b:
                    idx_c = bisect_left(occ_c, pos_b + lb)
                    if idx_c == len(occ_c):
                        continue
                    end = occ_c[idx_c] + lc
                    best = min(best, end - pos_b)
            else:
                # Pattern is "*B*"
                best = lb if occ_b else float("inf")

        else:
            # Pattern is "**C" or "*C*" with the first two fragments empty.
            best = lc if occ_c else float("inf")

        return -1 if best == float("inf") else best