class Solution:
    def shortestMatchingSubstring(self, s: str, p: str) -> int:
        def kmp_search(text: str, pat: str):
            m = len(pat)
            if m == 0:
                return []
            n = len(text)
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

            res = []
            j = 0
            for i in range(n):
                while j > 0 and text[i] != pat[j]:
                    j = pi[j - 1]
                if text[i] == pat[j]:
                    j += 1
                if j == m:
                    res.append(i - m + 1)
                    j = pi[j - 1]
            return res

        A, B, C = p.split('*')

        if not A and not B and not C:
            return 0

        occ = {}
        if A:
            occ['A'] = kmp_search(s, A)
            if not occ['A']:
                return -1
        if B:
            occ['B'] = kmp_search(s, B)
            if not occ['B']:
                return -1
        if C:
            occ['C'] = kmp_search(s, C)
            if not occ['C']:
                return -1

        INF = 10**18

        if B:
            b_occ = occ['B']
            a_occ = occ.get('A', [])
            c_occ = occ.get('C', [])
            la, lb, lc = len(A), len(B), len(C)

            ans = INF
            a_ptr = 0
            best_a = -1
            c_ptr = 0

            for b_start in b_occ:
                b_end = b_start + lb

                if A:
                    while a_ptr < len(a_occ) and a_occ[a_ptr] + la <= b_start:
                        best_a = a_occ[a_ptr]
                        a_ptr += 1
                    if best_a < 0:
                        continue
                    start = best_a
                else:
                    start = b_start

                if C:
                    while c_ptr < len(c_occ) and c_occ[c_ptr] < b_end:
                        c_ptr += 1
                    if c_ptr == len(c_occ):
                        break
                    end = c_occ[c_ptr] + lc
                else:
                    end = b_end

                length = end - start
                if length < ans:
                    ans = length

            return -1 if ans == INF else ans

        if A and C:
            a_occ = occ['A']
            c_occ = occ['C']
            la, lc = len(A), len(C)

            ans = INF
            a_ptr = 0
            best_a = -1

            for c_start in c_occ:
                while a_ptr < len(a_occ) and a_occ[a_ptr] + la <= c_start:
                    best_a = a_occ[a_ptr]
                    a_ptr += 1
                if best_a < 0:
                    continue

                end = c_start + lc
                length = end - best_a
                if length < ans:
                    ans = length

            return -1 if ans == INF else ans

        if A:
            return len(A)
        if C:
            return len(C)
        return 0