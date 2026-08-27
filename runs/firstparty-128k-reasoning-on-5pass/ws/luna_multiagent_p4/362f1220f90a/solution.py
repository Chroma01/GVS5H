class Solution:
    def generateString(self, str1: str, str2: str) -> str:
        n = len(str1)
        m = len(str2)
        length = n + m - 1

        forced = [None] * length

        # Place all mandatory occurrences and detect conflicting assignments.
        for start in range(n):
            if str1[start] == 'T':
                for j, ch in enumerate(str2):
                    pos = start + j
                    if forced[pos] is not None and forced[pos] != ch:
                        return ""
                    forced[pos] = ch

        # For each F-window:
        # active[start] means it still needs at least one mismatch.
        # remaining[start] is the number of currently unassigned positions.
        active = [False] * n
        remaining = [0] * n

        for start in range(n):
            if str1[start] != 'F':
                continue

            mismatch = False
            unknown = 0

            for j, ch in enumerate(str2):
                value = forced[start + j]
                if value is None:
                    unknown += 1
                elif value != ch:
                    mismatch = True
                    break

            if mismatch:
                continue

            if unknown == 0:
                return ""

            active[start] = True
            remaining[start] = unknown

        # Assign free positions from left to right for lexicographic minimality.
        alphabet = "abcdefghijklmnopqrstuvwxyz"
        answer = forced[:]

        for pos in range(length):
            if answer[pos] is not None:
                continue

            left = max(0, pos - m + 1)
            right = min(n - 1, pos)

            forbidden = set()

            # If this is the last unassigned position of an active F-window,
            # matching str2 here would violate that window.
            for start in range(left, right + 1):
                if active[start] and remaining[start] == 1:
                    forbidden.add(str2[pos - start])

            chosen = None
            for ch in alphabet:
                if ch not in forbidden:
                    chosen = ch
                    break

            if chosen is None:
                return ""

            answer[pos] = chosen

            # Update all active windows containing this position.
            for start in range(left, right + 1):
                if not active[start]:
                    continue

                expected = str2[pos - start]
                if chosen != expected:
                    active[start] = False
                else:
                    remaining[start] -= 1
                    if remaining[start] == 0:
                        return ""

        result = "".join(answer)

        # Final verification guards against implementation mistakes.
        for start in range(n):
            window = result[start:start + m]
            if str1[start] == 'T':
                if window != str2:
                    return ""
            elif window == str2:
                return ""

        return result