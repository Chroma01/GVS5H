class Solution:
    def generateString(self, str1: str, str2: str) -> str:
        n = len(str1)
        m = len(str2)

        # Outside the official constraints, but keeps the code safe.
        if m == 0:
            return ""
        if n == 0:
            return "a" * (m - 1)

        L = n + m - 1
        pat = [ord(ch) - 97 for ch in str2]
        is_T = [ch == 'T' for ch in str1]

        # Force every 'T' window to equal str2.
        fixed = [-1] * L
        for i, t in enumerate(is_T):
            if t:
                for j in range(m):
                    p = i + j
                    c = pat[j]
                    old = fixed[p]
                    if old == -1:
                        fixed[p] = c
                    elif old != c:
                        return ""

        # KMP prefix function.
        pi = [0] * m
        for i in range(1, m):
            j = pi[i - 1]
            while j > 0 and pat[i] != pat[j]:
                j = pi[j - 1]
            if pat[i] == pat[j]:
                j += 1
            pi[i] = j

        fallback = pi[m - 1]

        # Automaton states are 0..m. State m means a match just ended.
        # From state m, the next character is processed from fallback.
        trans = [[0] * 26 for _ in range(m + 1)]
        for q in range(m + 1):
            start = fallback if q == m else q
            row = trans[q]
            for c in range(26):
                if c == pat[start]:
                    row[c] = start + 1
                elif start == 0:
                    row[c] = 0
                else:
                    row[c] = trans[pi[start - 1]][c]

        # src[c][t] is a bitmask of states q such that trans[q][c] == t.
        src = [[0] * (m + 1) for _ in range(26)]
        for q in range(m + 1):
            bit = 1 << q
            row = trans[q]
            for c in range(26):
                src[c][row[c]] |= bit

        # Precompute non-empty target/source pairs for fast DP transitions.
        src_lists = []
        for c in range(26):
            lst = []
            row = src[c]
            for t in range(m + 1):
                sm = row[t]
                if sm:
                    lst.append((1 << t, sm))
            src_lists.append(lst)

        # combined[t] is the union over all characters of src[c][t].
        combined = [0] * (m + 1)
        for c in range(26):
            row = src[c]
            for t in range(m + 1):
                combined[t] |= row[t]

        combined_list = []
        for t in range(m + 1):
            sm = combined[t]
            if sm:
                combined_list.append((1 << t, sm))

        state_bits = [1 << q for q in range(m + 1)]
        all_states = (1 << (m + 1)) - 1
        not_m_mask = all_states ^ state_bits[m]

        # forbidden[pos] is true when position pos ends an 'F' window.
        forbidden = [False] * L
        for pos in range(m - 1, L):
            forbidden[pos] = not is_T[pos - m + 1]

        # dp[pos] is a bitmask of automaton states before position pos
        # from which the suffix pos..L-1 can be completed legally.
        dp = [0] * (L + 1)
        dp[L] = all_states

        src_lists_local = src_lists
        combined_list_local = combined_list

        for pos in range(L - 1, -1, -1):
            allowed = dp[pos + 1]

            # A transition into state m means the window ending here equals str2.
            # That is forbidden exactly at 'F' window ends.
            if forbidden[pos]:
                allowed &= not_m_mask

            if not allowed:
                return ""

            fc = fixed[pos]
            mask = 0

            if fc != -1:
                for bit, sm in src_lists_local[fc]:
                    if allowed & bit:
                        mask |= sm
            else:
                for bit, sm in combined_list_local:
                    if allowed & bit:
                        mask |= sm

            if not mask:
                return ""
            dp[pos] = mask

        if not (dp[0] & 1):
            return ""

        # Greedily reconstruct the lexicographically smallest valid string.
        letters = "abcdefghijklmnopqrstuvwxyz"
        res = []
        state = 0

        for pos in range(L):
            fc = fixed[pos]
            forb = forbidden[pos]

            if fc != -1:
                ns = trans[state][fc]
                if ns == m and forb:
                    return ""
                if not (dp[pos + 1] & state_bits[ns]):
                    return ""
                state = ns
                res.append(letters[fc])
            else:
                chosen = -1
                row = trans[state]
                for c in range(26):
                    ns = row[c]
                    if ns == m and forb:
                        continue
                    if dp[pos + 1] & state_bits[ns]:
                        chosen = c
                        break

                if chosen == -1:
                    return ""

                state = row[chosen]
                res.append(letters[chosen])

        return "".join(res)