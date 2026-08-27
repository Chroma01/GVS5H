class Solution:
    def generateString(self, str1: str, str2: str) -> str:
        n = len(str1)
        m = len(str2)
        total = n + m - 1

        # Prefix function for str2.
        pi = [0] * m
        for i in range(1, m):
            j = pi[i - 1]
            while j > 0 and str2[i] != str2[j]:
                j = pi[j - 1]
            if str2[i] == str2[j]:
                j += 1
            pi[i] = j

        # KMP automaton. States 0..m-1 represent the longest suffix
        # that is also a proper prefix of str2.
        trans = [[0] * 26 for _ in range(m)]
        for state in range(m):
            for c in range(26):
                ch = chr(ord('a') + c)

                if ch == str2[state]:
                    nxt = state + 1
                elif state > 0:
                    nxt = trans[pi[state - 1]][c]
                else:
                    nxt = 0

                if nxt == m:
                    nxt = pi[m - 1]

                trans[state][c] = nxt

        last_char = ord(str2[-1]) - ord('a')

        # Reachable next-state masks for unconstrained and F positions.
        all_masks = [0] * m
        f_masks = [0] * m

        for state in range(m):
            all_mask = 0
            f_mask = 0

            for c in range(26):
                nxt = trans[state][c]
                bit = 1 << nxt
                all_mask |= bit

                # This character creates an exact match only when the
                # previous state represents str2[:-1].
                if not (state == m - 1 and c == last_char):
                    f_mask |= bit

            all_masks[state] = all_mask
            f_masks[state] = f_mask

        # good[p] is the set of KMP states from which positions p..total-1
        # can be completed while satisfying all constraints.
        good = [0] * (total + 1)
        good[total] = (1 << m) - 1

        for p in range(total - 1, -1, -1):
            suffix_states = good[p + 1]

            if p < m - 1:
                # No complete window ends at this position.
                reachable = 0
                for state in range(m):
                    if all_masks[state] & suffix_states:
                        reachable |= 1 << state
                good[p] = reachable
                continue

            constraint = str1[p - m + 1]

            if constraint == 'T':
                # The current window equals str2 exactly iff the previous
                # state is m-1 and the appended character is str2[-1].
                forced_next = pi[m - 1]
                if (suffix_states >> forced_next) & 1:
                    good[p] = 1 << (m - 1)
                else:
                    good[p] = 0
            else:
                reachable = 0
                for state in range(m):
                    if f_masks[state] & suffix_states:
                        reachable |= 1 << state
                good[p] = reachable

        if not (good[0] & 1):
            return ""

        # Greedily reconstruct the lexicographically smallest valid string.
        answer = []
        state = 0

        for p in range(total):
            constraint = None
            if p >= m - 1:
                constraint = str1[p - m + 1]

            for c in range(26):
                if constraint == 'T':
                    if state != m - 1 or c != last_char:
                        continue
                elif constraint == 'F':
                    if state == m - 1 and c == last_char:
                        continue

                next_state = trans[state][c]
                if (good[p + 1] >> next_state) & 1:
                    answer.append(chr(ord('a') + c))
                    state = next_state
                    break
            else:
                return ""

        return ''.join(answer)