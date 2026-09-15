class Solution:
    def shortestMatchingSubstring(self, s: str, p: str) -> int:
        def kmp_occurrences(text: str, pat: str):
            n = len(text)
            m = len(pat)
            if m == 0:
                return []
            if m > n:
                return []

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
            for i, ch in enumerate(text):
                while j > 0 and ch != pat[j]:
                    j = pi[j - 1]
                if ch == pat[j]:
                    j += 1
                    if j == m:
                        occ.append(i - m + 1)
                        j = pi[j - 1]
            return occ

        parts = p.split('*')
        # The problem guarantees exactly two '*', but padding keeps the code
        # safe for patterns with fewer stars.
        if len(parts) < 3:
            parts += [''] * (3 - len(parts))

        A, B, C = parts[0], parts[1], parts[2]
        n = len(s)

        # Literal blocks cannot overlap, so their total length is a lower bound.
        if len(A) + len(B) + len(C) > n:
            return -1

        cache = {}
        pieces = []

        for part in (A, B, C):
            if part:
                occ = cache.get(part)
                if occ is None:
                    occ = kmp_occurrences(s, part)
                    cache[part] = occ
                if not occ:
                    return -1
                pieces.append((len(part), occ))

        m = len(pieces)

        if m == 0:
            return 0

        if m == 1:
            return pieces[0][0]

        INF = n + 1

        if m == 2:
            l0, occ0 = pieces[0]
            l1, occ1 = pieces[1]

            ans = INF
            i = 0
            last = -1
            len0 = len(occ0)
            min_possible = l0 + l1

            for start1 in occ1:
                while i < len0 and occ0[i] + l0 <= start1:
                    last = occ0[i]
                    i += 1

                if last != -1:
                    length = start1 + l1 - last
                    if length < ans:
                        ans = length
                        if ans == min_possible:
                            break

            return -1 if ans == INF else ans

        l0, occ0 = pieces[0]
        l1, occ1 = pieces[1]
        l2, occ2 = pieces[2]

        ans = INF
        i = 0
        last0 = -1
        j = 0
        len0 = len(occ0)
        len2 = len(occ2)
        min_possible = l0 + l1 + l2

        for start1 in occ1:
            while i < len0 and occ0[i] + l0 <= start1:
                last0 = occ0[i]
                i += 1

            end1 = start1 + l1
            while j < len2 and occ2[j] < end1:
                j += 1

            # Since B ends are nondecreasing, once no C remains, future B
            # occurrences cannot have a valid C either.
            if j == len2:
                break

            if last0 != -1:
                length = occ2[j] + l2 - last0
                if length < ans:
                    ans = length
                    if ans == min_possible:
                        break

        return -1 if ans == INF else ans