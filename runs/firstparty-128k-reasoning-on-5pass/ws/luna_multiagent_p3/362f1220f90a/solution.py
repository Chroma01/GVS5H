class Solution:
    def generateString(self, str1: str, str2: str) -> str:
        n = len(str1)
        m = len(str2)
        total = n + m - 1

        fixed = [''] * total

        # Overlay all mandatory ("T") occurrences.
        for start in range(n):
            if str1[start] == 'T':
                for offset, ch in enumerate(str2):
                    pos = start + offset
                    if fixed[pos] and fixed[pos] != ch:
                        return ""
                    fixed[pos] = ch

        # For each "F" window, determine its rightmost unfixed position.
        # If the window already differs, it needs no further action.
        # Otherwise, it must differ at or before that rightmost free position.
        mismatch = [False] * n
        deadlines = [[] for _ in range(total)]

        for start in range(n):
            if str1[start] != 'F':
                continue

            rightmost_free = -1
            already_different = False

            for offset in range(m):
                pos = start + offset
                if fixed[pos]:
                    if fixed[pos] != str2[offset]:
                        already_different = True
                        break
                else:
                    rightmost_free = pos

            if already_different:
                mismatch[start] = True
            elif rightmost_free == -1:
                # Every character is forced and the window equals str2.
                return ""
            else:
                deadlines[rightmost_free].append(start)

        answer = fixed[:]

        # Greedily assign characters from left to right.
        for pos in range(total):
            if fixed[pos]:
                ch = fixed[pos]
            else:
                forbidden = set()

                # Windows reaching their final free position must mismatch
                # at this position unless they already mismatched earlier.
                for start in deadlines[pos]:
                    if not mismatch[start]:
                        forbidden.add(str2[pos - start])

                ch = 'a'
                while ch in forbidden:
                    if ch == 'z':
                        return ""
                    ch = chr(ord(ch) + 1)

            answer[pos] = ch

            # Update all F-windows containing this position.
            left = max(0, pos - m + 1)
            right = min(n - 1, pos)
            for start in range(left, right + 1):
                if str1[start] == 'F' and not mismatch[start]:
                    if ch != str2[pos - start]:
                        mismatch[start] = True

        result = ''.join(answer)

        # Final validation.
        for start in range(n):
            equal = result[start:start + m] == str2
            if str1[start] == 'T':
                if not equal:
                    return ""
            elif equal:
                return ""

        return result