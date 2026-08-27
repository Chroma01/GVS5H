class Solution:
    def shortestMatchingSubstring(self, s: str, p: str) -> int:
        parts = p.split('*')  # Exactly three parts: A, B, C
        literals = [part for part in parts if part]

        # Pattern "**" matches the empty substring.
        if not literals:
            return 0

        n = len(s)

        def find_occurrences(pattern):
            m = len(pattern)
            pi = [0] * m

            for i in range(1, m):
                j = pi[i - 1]
                while j > 0 and pattern[i] != pattern[j]:
                    j = pi[j - 1]
                if pattern[i] == pattern[j]:
                    j += 1
                pi[i] = j

            positions = []
            j = 0
            for i, ch in enumerate(s):
                while j > 0 and ch != pattern[j]:
                    j = pi[j - 1]
                if ch == pattern[j]:
                    j += 1
                if j == m:
                    positions.append(i - m + 1)
                    j = pi[j - 1]

            return positions

        occurrences = [find_occurrences(part) for part in literals]

        if not occurrences[0]:
            return -1

        # A single literal with stars around it can match that literal itself.
        if len(literals) == 1:
            return len(literals[0])

        def build_successor_array(positions):
            present = bytearray(n + 1)
            for pos in positions:
                present[pos] = 1

            nxt = [-1] * (n + 1)
            nearest = -1
            for i in range(n, -1, -1):
                if present[i]:
                    nearest = i
                nxt[i] = nearest
            return nxt

        successor_arrays = [None]
        for i in range(1, len(literals)):
            successor_arrays.append(build_successor_array(occurrences[i]))

        answer = float("inf")

        for start in occurrences[0]:
            current_end = start + len(literals[0])
            valid = True

            for i in range(1, len(literals)):
                next_start = successor_arrays[i][current_end]
                if next_start == -1:
                    valid = False
                    break
                current_end = next_start + len(literals[i])

            if valid:
                answer = min(answer, current_end - start)

        return -1 if answer == float("inf") else answer