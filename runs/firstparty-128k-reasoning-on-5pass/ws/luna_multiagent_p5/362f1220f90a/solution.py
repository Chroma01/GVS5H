class Solution:
    def generateString(self, str1: str, str2: str) -> str:
        n = len(str1)
        m = len(str2)
        total = n + m - 1

        forced = [None] * total

        # Propagate all exact-match constraints.
        for start in range(n):
            if str1[start] == "T":
                for offset, char in enumerate(str2):
                    pos = start + offset
                    if forced[pos] is not None and forced[pos] != char:
                        return ""
                    forced[pos] = char

        free_count = [0] * n
        has_mismatch = [False] * n

        # Initialize the state of every F-window.
        for start in range(n):
            if str1[start] != "F":
                continue

            free = 0
            mismatch = False

            for offset, expected in enumerate(str2):
                char = forced[start + offset]
                if char is None:
                    free += 1
                elif char != expected:
                    mismatch = True

            free_count[start] = free
            has_mismatch[start] = mismatch

            if free == 0 and not mismatch:
                return ""

        result = forced[:]

        # Fill unforced positions lexicographically from left to right.
        for pos in range(total):
            if forced[pos] is not None:
                continue

            forbidden = [False] * 26
            left = max(0, pos - m + 1)
            right = min(n - 1, pos)

            # If this is the final free position of an unsatisfied F-window,
            # it must differ from the corresponding character in str2.
            for start in range(left, right + 1):
                if (
                    str1[start] == "F"
                    and free_count[start] == 1
                    and not has_mismatch[start]
                ):
                    offset = pos - start
                    forbidden[ord(str2[offset]) - ord("a")] = True

            chosen = None
            for code in range(26):
                if not forbidden[code]:
                    chosen = chr(ord("a") + code)
                    break

            if chosen is None:
                return ""

            result[pos] = chosen

            # Update all F-windows containing this position.
            for start in range(left, right + 1):
                if str1[start] == "F":
                    free_count[start] -= 1
                    if chosen != str2[pos - start]:
                        has_mismatch[start] = True

        return "".join(result)