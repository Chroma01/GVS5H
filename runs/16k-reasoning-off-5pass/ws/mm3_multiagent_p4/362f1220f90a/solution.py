class Solution:
    def generateString(self, str1: str, str2: str) -> str:
        n = len(str1)
        m = len(str2)
        L = n + m - 1

        # 1. Apply 'T' constraints; detect conflicts
        forced = [None] * L  # forced[pos] = char if forced by a 'T', else None
        for i, ch in enumerate(str1):
            if ch == 'T':
                for j in range(m):
                    p = i + j
                    cur = forced[p]
                    if cur is None:
                        forced[p] = str2[j]
                    elif cur != str2[j]:
                        return ""

        is_free = [forced[i] is None for i in range(L)]

        # 2. Identify critical 'F' windows.
        # A window is critical if all its free positions correspond to 'a' in str2.
        # For such windows, setting all free positions to 'a' would make the window
        # equal to str2 (which is forbidden for an 'F'). We must set at least one
        # free position in each critical window to a character != 'a' (the smallest
        # possible is 'b'). For non-critical windows, setting free positions to 'a'
        # already breaks the window because str2 has a non-'a' character at some
        # free position offset.
        critical_windows = []  # list of (max_free_pos, list_of_free_positions)
        pos_to_critical = [[] for _ in range(L)]  # reverse map for efficient coverage

        for i in range(n):
            if str1[i] == 'F':
                free_positions = []
                is_critical = True
                for j in range(m):
                    p = i + j
                    if is_free[p]:
                        free_positions.append(p)
                        if str2[j] != 'a':
                            is_critical = False
                if not free_positions:
                    # Window is entirely forced to str2; for an 'F' this is invalid.
                    return ""
                if is_critical:
                    max_free = free_positions[-1]
                    w_idx = len(critical_windows)
                    critical_windows.append((max_free, free_positions))
                    for p in free_positions:
                        pos_to_critical[p].append(w_idx)

        # 3. If there are no critical windows, we can fill all free positions with 'a'.
        if not critical_windows:
            word = [forced[i] if forced[i] is not None else 'a' for i in range(L)]
            return "".join(word)

        # 4. Solve the hitting set problem for critical windows.
        # Greedy: sort critical windows by their rightmost free position.
        # For each window, if it is not yet covered by a chosen position,
        # add its rightmost free position to the chosen set. This yields
        # the rightmost possible set of positions, which corresponds to
        # the lexicographically smallest string.
        critical_windows.sort(key=lambda x: x[0])
        chosen = set()
        covered = [False] * len(critical_windows)

        for idx, (max_pos, free_list) in enumerate(critical_windows):
            if covered[idx]:
                continue
            # This window is not covered; choose its rightmost free position.
            chosen.add(max_pos)
            # Mark all critical windows that contain max_pos as covered.
            for w_idx in pos_to_critical[max_pos]:
                covered[w_idx] = True

        # 5. Construct the final string.
        # Forced positions keep their values.
        # Free positions in 'chosen' are set to 'b' (smallest char != 'a').
        # All other free positions are set to 'a'.
        word = [''] * L
        for i in range(L):
            if forced[i] is not None:
                word[i] = forced[i]
            elif i in chosen:
                word[i] = 'b'
            else:
                word[i] = 'a'

        return "".join(word)