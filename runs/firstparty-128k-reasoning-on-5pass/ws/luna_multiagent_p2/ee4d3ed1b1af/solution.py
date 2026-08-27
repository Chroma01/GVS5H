from bisect import bisect_left


class Solution:
    def shortestMatchingSubstring(self, s: str, p: str) -> int:
        n = len(s)
        a, b, c = p.split("*")

        def find_occurrences(pattern: str):
            m = len(pattern)

            if m == 0:
                return list(range(n + 1))
            if m > n:
                return []

            prefix = [0] * m
            j = 0
            for i in range(1, m):
                while j > 0 and pattern[i] != pattern[j]:
                    j = prefix[j - 1]
                if pattern[i] == pattern[j]:
                    j += 1
                prefix[i] = j

            occurrences = []
            j = 0
            for i, ch in enumerate(s):
                while j > 0 and ch != pattern[j]:
                    j = prefix[j - 1]
                if ch == pattern[j]:
                    j += 1
                if j == m:
                    occurrences.append(i - m + 1)
                    j = prefix[j - 1]

            return occurrences

        starts_a = find_occurrences(a)
        starts_b = find_occurrences(b)
        starts_c = find_occurrences(c)

        len_a = len(a)
        len_b = len(b)
        len_c = len(c)

        best = n + 1

        for start_a in starts_a:
            end_a = start_a + len_a

            index_b = bisect_left(starts_b, end_a)
            if index_b == len(starts_b):
                continue
            start_b = starts_b[index_b]

            end_b = start_b + len_b

            index_c = bisect_left(starts_c, end_b)
            if index_c == len(starts_c):
                continue
            start_c = starts_c[index_c]

            candidate_length = start_c + len_c - start_a
            if candidate_length < best:
                best = candidate_length

        return -1 if best == n + 1 else best