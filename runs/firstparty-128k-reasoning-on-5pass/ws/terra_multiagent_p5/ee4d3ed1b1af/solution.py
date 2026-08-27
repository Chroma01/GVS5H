from bisect import bisect_left


class Solution:
    def shortestMatchingSubstring(self, s: str, p: str) -> int:
        a, b, c = p.split('*')
        n = len(s)

        def occurrences(pattern: str):
            if not pattern:
                return list(range(n + 1))

            m = len(pattern)
            lps = [0] * m
            length = 0

            for i in range(1, m):
                while length > 0 and pattern[i] != pattern[length]:
                    length = lps[length - 1]
                if pattern[i] == pattern[length]:
                    length += 1
                    lps[i] = length

            result = []
            matched = 0

            for i, ch in enumerate(s):
                while matched > 0 and ch != pattern[matched]:
                    matched = lps[matched - 1]
                if ch == pattern[matched]:
                    matched += 1
                if matched == m:
                    result.append(i - m + 1)
                    matched = lps[matched - 1]

            return result

        occ_a = occurrences(a)
        occ_b = occurrences(b)
        occ_c = occurrences(c)

        len_a = len(a)
        len_b = len(b)
        len_c = len(c)
        answer = float("inf")

        for start_a in occ_a:
            end_a = start_a + len_a

            index_b = bisect_left(occ_b, end_a)
            if index_b == len(occ_b):
                continue

            start_b = occ_b[index_b]
            end_b = start_b + len_b

            index_c = bisect_left(occ_c, end_b)
            if index_c == len(occ_c):
                continue

            end_c = occ_c[index_c] + len_c
            answer = min(answer, end_c - start_a)

        return -1 if answer == float("inf") else answer