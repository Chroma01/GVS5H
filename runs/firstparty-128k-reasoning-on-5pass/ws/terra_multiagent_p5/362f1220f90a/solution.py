class Solution:
    def generateString(self, str1: str, str2: str) -> str:
        n = len(str1)
        m = len(str2)
        length = n + m - 1
        pat = [ord(c) - ord('a') for c in str2]

        # Apply all mandatory placements from T windows.
        forced = [-1] * length
        for i, flag in enumerate(str1):
            if flag == 'T':
                for j, c in enumerate(pat):
                    pos = i + j
                    if forced[pos] != -1 and forced[pos] != c:
                        return ""
                    forced[pos] = c

        # KMP prefix function.
        pi = [0] * m
        for i in range(1, m):
            j = pi[i - 1]
            while j > 0 and pat[i] != pat[j]:
                j = pi[j - 1]
            if pat[i] == pat[j]:
                j += 1
            pi[i] = j

        # A state is a matched prefix length in [0, m-1].
        # fail[state] is the failure state for a mismatch in that state.
        fail = [0] * m
        for state in range(1, m):
            fail[state] = pi[state - 1]

        # KMP transitions. A complete match immediately falls back to pi[m-1].
        trans = [[0] * 26 for _ in range(m)]
        for c in range(26):
            trans[0][c] = 1 if m > 1 and c == pat[0] else 0

        for state in range(1, m):
            for c in range(26):
                if c == pat[state]:
                    trans[state][c] = state + 1 if state + 1 < m else pi[m - 1]
                else:
                    trans[state][c] = trans[fail[state]][c]

        # dp[pos][state] is whether suffix pos..length-1 is feasible when
        # KMP state before consuming word[pos] is state.
        dp = [None] * (length + 1)
        dp[length] = bytearray([1]) * m
        all_letters = (1 << 26) - 1

        for pos in range(length - 1, -1, -1):
            nxt = dp[pos + 1]
            forbidden_end = pos >= m - 1 and str1[pos - m + 1] == 'F'
            fixed = forced[pos]
            cur = bytearray(m)

            if fixed != -1:
                # Failure links point to smaller states, permitting O(m).
                for state in range(m):
                    if fixed == pat[state]:
                        if state == m - 1:
                            cur[state] = 0 if forbidden_end else nxt[pi[m - 1]]
                        else:
                            cur[state] = nxt[state + 1]
                    elif state == 0:
                        cur[state] = nxt[0]
                    else:
                        cur[state] = cur[fail[state]]
            else:
                # Store feasible letters as a bit mask for each KMP state.
                masks = [0] * m
                for state in range(m):
                    if state == 0:
                        mask = all_letters if nxt[0] else 0
                    else:
                        mask = masks[fail[state]]

                    bit = 1 << pat[state]
                    if state == m - 1:
                        match_ok = not forbidden_end and nxt[pi[m - 1]]
                    else:
                        match_ok = nxt[state + 1]

                    if match_ok:
                        mask |= bit
                    else:
                        mask &= ~bit

                    masks[state] = mask
                    cur[state] = 1 if mask else 0

            dp[pos] = cur

        if not dp[0][0]:
            return ""

        # Select the first character that leaves a feasible suffix.
        result = []
        state = 0

        for pos in range(length):
            forbidden_end = pos >= m - 1 and str1[pos - m + 1] == 'F'

            if forced[pos] != -1:
                candidates = (forced[pos],)
            else:
                candidates = range(26)

            for c in candidates:
                complete_match = state == m - 1 and c == pat[m - 1]
                if forbidden_end and complete_match:
                    continue

                next_state = trans[state][c]
                if dp[pos + 1][next_state]:
                    result.append(chr(c + ord('a')))
                    state = next_state
                    break
            else:
                return ""

        return "".join(result)