class Solution:
    def generateString(self, str1: str, str2: str) -> str:
        n, m = len(str1), len(str2)
        total = n + m - 1

        ans = ['a'] * total
        fixed = [False] * total

        # Apply all required matching occurrences.
        for i, flag in enumerate(str1):
            if flag != 'T':
                continue
            for j, ch in enumerate(str2):
                pos = i + j
                if fixed[pos] and ans[pos] != ch:
                    return ""
                ans[pos] = ch
                fixed[pos] = True

        # Non-forced positions can be used once as witnesses for F windows.
        usable = [not value for value in fixed]

        # Process forbidden occurrences from left to right.
        for i, flag in enumerate(str1):
            if flag != 'F':
                continue

            matches = True
            for j, ch in enumerate(str2):
                if ans[i + j] != ch:
                    matches = False
                    break

            if not matches:
                continue

            # A matching F window must be broken. Every usable position in a
            # currently matching window is aligned to an 'a' in str2, so 'b'
            # is the smallest valid replacement. Choose the latest position
            # to preserve lexicographic minimality.
            chosen = -1
            for pos in range(i + m - 1, i - 1, -1):
                if usable[pos]:
                    chosen = pos
                    break

            if chosen == -1:
                return ""

            ans[chosen] = 'b'
            usable[chosen] = False

        result = ''.join(ans)

        # Defensive verification.
        for i, flag in enumerate(str1):
            equal = result[i:i + m] == str2
            if (flag == 'T' and not equal) or (flag == 'F' and equal):
                return ""

        return result