from bisect import bisect_left


class Solution:
    def shortestMatchingSubstring(self, s: str, p: str) -> int:
        n = len(s)
        a, b, c = p.split("*")

        def find_occurrences(pattern: str):
            if not pattern:
                return None

            m = len(pattern)
            prefix = [0] * m
            j = 0

            for i in range(1, m):
                while j and pattern[i] != pattern[j]:
                    j = prefix[j - 1]
                if pattern[i] == pattern[j]:
                    j += 1
                prefix[i] = j

            occurrences = []
            j = 0
            for i, ch in enumerate(s):
                while j and ch != pattern[j]:
                    j = prefix[j - 1]
                if ch == pattern[j]:
                    j += 1

                if j == m:
                    occurrences.append(i - m + 1)
                    j = prefix[j - 1]

            return occurrences

        occ_a = find_occurrences(a)
        occ_b = find_occurrences(b)
        occ_c = find_occurrences(c)

        if occ_a is None:
            first_positions = range(n + 1)
        else:
            first_positions = occ_a

        answer = n + 1

        for start_a in first_positions:
            end_a = start_a + len(a)

            if occ_b is None:
                start_b = end_a
            else:
                index_b = bisect_left(occ_b, end_a)
                if index_b == len(occ_b):
                    continue
                start_b = occ_b[index_b]

            end_b = start_b + len(b)

            if occ_c is None:
                start_c = end_b
            else:
                index_c = bisect_left(occ_c, end_b)
                if index_c == len(occ_c):
                    continue
                start_c = occ_c[index_c]

            answer = min(answer, start_c + len(c) - start_a)

        return -1 if answer == n + 1 else answer