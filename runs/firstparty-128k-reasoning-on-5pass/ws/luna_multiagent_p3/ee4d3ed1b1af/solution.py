from bisect import bisect_left


class Solution:
    def shortestMatchingSubstring(self, s: str, p: str) -> int:
        n = len(s)
        a, b, c = p.split("*")

        def occurrences(pattern: str):
            m = len(pattern)

            if m == 0:
                return range(n + 1)

            prefix = [0] * m
            j = 0
            for i in range(1, m):
                while j > 0 and pattern[i] != pattern[j]:
                    j = prefix[j - 1]
                if pattern[i] == pattern[j]:
                    j += 1
                prefix[i] = j

            result = []
            j = 0
            for i, ch in enumerate(s):
                while j > 0 and ch != pattern[j]:
                    j = prefix[j - 1]
                if ch == pattern[j]:
                    j += 1

                if j == m:
                    result.append(i - m + 1)
                    j = prefix[j - 1]

            return result

        starts_a = occurrences(a)
        starts_b = occurrences(b)
        starts_c = occurrences(c)

        len_a = len(a)
        len_b = len(b)
        len_c = len(c)

        answer = n + 1

        for start_a in starts_a:
            start_b_index = bisect_left(starts_b, start_a + len_a)
            if start_b_index == len(starts_b):
                continue

            start_b = starts_b[start_b_index]
            start_c_index = bisect_left(starts_c, start_b + len_b)
            if start_c_index == len(starts_c):
                continue

            start_c = starts_c[start_c_index]
            answer = min(answer, start_c + len_c - start_a)

            if answer == 0:
                return 0

        return -1 if answer == n + 1 else answer