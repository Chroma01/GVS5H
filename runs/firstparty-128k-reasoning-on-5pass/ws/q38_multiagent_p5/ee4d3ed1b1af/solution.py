from bisect import bisect_left, bisect_right


class Solution:
    def shortestMatchingSubstring(self, s: str, p: str) -> int:
        A, B, C = p.split('*')

        # Only the pattern "**" can match the empty substring.
        if not A and not B and not C:
            return 0

        n = len(s)
        lenA, lenB, lenC = len(A), len(B), len(C)

        def find_occurrences(pat: str):
            """Return all start positions of pat in s using KMP."""
            m = len(pat)
            if m == 0 or m > n:
                return []

            # Prefix function for KMP.
            pi = [0] * m
            for i in range(1, m):
                j = pi[i - 1]
                while j > 0 and pat[i] != pat[j]:
                    j = pi[j - 1]
                if pat[i] == pat[j]:
                    j += 1
                pi[i] = j

            occ = []
            j = 0
            for i, ch in enumerate(s):
                while j > 0 and ch != pat[j]:
                    j = pi[j - 1]
                if ch == pat[j]:
                    j += 1
                if j == m:
                    occ.append(i - m + 1)
                    j = pi[j - 1]
            return occ

        A_occ = find_occurrences(A) if A else []
        B_occ = find_occurrences(B) if B else []
        C_occ = find_occurrences(C) if C else []

        INF = 10**18
        ans = INF

        # Case 1: middle literal block B is non-empty.
        if B:
            if A and not A_occ:
                return -1
            if C and not C_occ:
                return -1
            if not B_occ:
                return -1

            for b in B_occ:
                # Choose the latest A occurrence ending before B starts.
                if A:
                    ia = bisect_right(A_occ, b - lenA) - 1
                    if ia < 0:
                        continue
                    start = A_occ[ia]
                else:
                    start = b

                # Choose the earliest C occurrence starting after B ends.
                if C:
                    ic = bisect_left(C_occ, b + lenB)
                    if ic == len(C_occ):
                        # Later B starts only need even later C starts.
                        break
                    end = C_occ[ic] + lenC - 1
                else:
                    end = b + lenB - 1

                cur = end - start + 1
                if cur < ans:
                    ans = cur

            return -1 if ans == INF else ans

        # Case 2: B is empty, so the pattern is effectively A * C.
        if not A:
            return lenC if C_occ else -1
        if not C:
            return lenA if A_occ else -1
        if not A_occ or not C_occ:
            return -1

        for a in A_occ:
            # Earliest C occurrence that does not overlap A.
            ic = bisect_left(C_occ, a + lenA)
            if ic == len(C_occ):
                # Later A starts only need even later C starts.
                break
            end = C_occ[ic] + lenC - 1
            cur = end - a + 1
            if cur < ans:
                ans = cur

        return -1 if ans == INF else ans