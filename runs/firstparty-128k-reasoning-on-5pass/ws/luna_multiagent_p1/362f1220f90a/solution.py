class Solution:
    def generateString(self, str1: str, str2: str) -> str:
        n = len(str1)
        m = len(str2)
        total = n + m - 1

        result = ['a'] * total
        fixed = [False] * total

        # Apply all required occurrences.
        for start in range(n):
            if str1[start] != 'T':
                continue

            for offset, ch in enumerate(str2):
                pos = start + offset
                if fixed[pos] and result[pos] != ch:
                    return ""
                result[pos] = ch
                fixed[pos] = True

        # Repair forbidden occurrences from left to right.
        for start in range(n):
            if str1[start] != 'F':
                continue

            matches = True
            for offset, ch in enumerate(str2):
                if result[start + offset] != ch:
                    matches = False
                    break

            if not matches:
                continue

            # Change the latest non-fixed position to preserve
            # lexicographic minimality.
            chosen = -1
            for offset in range(m - 1, -1, -1):
                pos = start + offset
                if not fixed[pos]:
                    chosen = pos
                    break

            if chosen == -1:
                return ""

            pattern_char = str2[chosen - start]
            result[chosen] = 'b' if pattern_char == 'a' else 'a'
            fixed[chosen] = True

        return ''.join(result)