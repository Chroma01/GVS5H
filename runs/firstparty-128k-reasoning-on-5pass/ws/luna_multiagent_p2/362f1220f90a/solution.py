class Solution:
    def generateString(self, str1: str, str2: str) -> str:
        n = len(str1)
        m = len(str2)
        length = n + m - 1

        fixed = [None] * length

        # Propagate all required occurrences.
        for start, flag in enumerate(str1):
            if flag == 'T':
                for offset, ch in enumerate(str2):
                    pos = start + offset
                    if fixed[pos] is not None and fixed[pos] != ch:
                        return ""
                    fixed[pos] = ch

        # For each F-window, register its rightmost unfixed position.
        # The window must be made different from str2 at that position.
        force_at = [[] for _ in range(length)]

        for start, flag in enumerate(str1):
            if flag != 'F':
                continue

            last_free = -1
            already_different = False

            for pos in range(start, start + m):
                if fixed[pos] is None:
                    last_free = pos
                elif fixed[pos] != str2[pos - start]:
                    already_different = True
                    break

            if already_different:
                continue

            if last_free == -1:
                # This forbidden window is already forced to equal str2.
                return ""

            force_at[last_free].append(start)

        result = [None] * length

        for pos in range(length):
            if fixed[pos] is not None:
                result[pos] = fixed[pos]
                continue

            forbidden = set()

            # These windows have no unfixed positions after pos.
            # If their prefix currently matches str2, this character
            # cannot also match the corresponding character of str2.
            for start in force_at[pos]:
                if ''.join(result[start:pos]) == str2[:pos - start]:
                    forbidden.add(str2[pos - start])

            for code in range(ord('a'), ord('z') + 1):
                ch = chr(code)
                if ch not in forbidden:
                    result[pos] = ch
                    break
            else:
                return ""

        return ''.join(result)