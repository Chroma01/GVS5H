class Solution:
    def generateString(self, str1: str, str2: str) -> str:
        n, m = len(str1), len(str2)
        L = n + m - 1
        word = ['a'] * L
        forced = [False] * L

        # Apply T constraints and detect conflicts
        for i, c in enumerate(str1):
            if c == 'T':
                for k in range(m):
                    j = i + k
                    if forced[j] and word[j] != str2[k]:
                        return ""
                    word[j] = str2[k]
                    forced[j] = True

        # Resolve F constraints
        for i, c in enumerate(str1):
            if c == 'F':
                # Check if window already differs from str2
                diff = False
                last_free = -1
                for k in range(m):
                    j = i + k
                    if word[j] != str2[k]:
                        diff = True
                    if not forced[j]:
                        last_free = j
                if diff:
                    continue
                # Window currently equals str2; must break it at a free position
                if last_free == -1:
                    return ""
                # Flip the rightmost free position to the smallest char != str2
                k = last_free - i
                word[last_free] = 'a' if str2[k] != 'a' else 'b'

        return ''.join(word)