from bisect import bisect_left


class Solution:
    def shortestMatchingSubstring(self, s: str, p: str) -> int:
        parts = p.split("*")
        nonempty = [part for part in parts if part]

        if not nonempty:
            return 0

        def find_occurrences(pattern: str):
            m = len(pattern)
            lps = [0] * m

            j = 0
            for i in range(1, m):
                while j > 0 and pattern[i] != pattern[j]:
                    j = lps[j - 1]
                if pattern[i] == pattern[j]:
                    j += 1
                lps[i] = j

            result = []
            j = 0
            for i, ch in enumerate(s):
                while j > 0 and ch != pattern[j]:
                    j = lps[j - 1]
                if ch == pattern[j]:
                    j += 1
                if j == m:
                    result.append(i - m + 1)
                    j = lps[j - 1]

            return result

        occurrences = [find_occurrences(part) for part in nonempty]

        if any(not positions for positions in occurrences):
            return -1

        if len(nonempty) == 1:
            return len(nonempty[0])

        answer = len(s) + 1
        first_length = len(nonempty[0])

        for first_start in occurrences[0]:
            previous_end = first_start + first_length
            last_end = None
            valid = True

            for index in range(1, len(nonempty)):
                positions = occurrences[index]
                next_index = bisect_left(positions, previous_end)

                if next_index == len(positions):
                    valid = False
                    break

                next_start = positions[next_index]
                previous_end = next_start + len(nonempty[index])
                last_end = previous_end

            if valid:
                answer = min(answer, last_end - first_start)

        return -1 if answer == len(s) + 1 else answer