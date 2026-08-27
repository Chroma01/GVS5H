class Solution:
    def generateString(self, str1: str, str2: str) -> str:
        n = len(str1)
        m = len(str2)
        total = n + m - 1
        pattern = [ord(ch) - 97 for ch in str2]

        # KMP prefix function.
        pi = [0] * m
        for i in range(1, m):
            j = pi[i - 1]
            while j > 0 and pattern[i] != pattern[j]:
                j = pi[j - 1]
            if pattern[i] == pattern[j]:
                j += 1
            pi[i] = j

        # States are matched-prefix lengths 0..m-1 after fallback from a match.
        # transition[state][character] = (next_state, occurrence_completed)
        transition = [[None] * 26 for _ in range(m)]
        all_dest_masks = [0] * m
        nonmatch_dest_masks = [0] * m

        for state in range(m):
            any_mask = 0
            nonmatch_mask = 0
            for c in range(26):
                k = state
                while k > 0 and pattern[k] != c:
                    k = pi[k - 1]
                if pattern[k] == c:
                    k += 1

                hit = (k == m)
                if hit:
                    k = pi[m - 1]

                transition[state][c] = (k, hit)
                any_mask |= 1 << k
                if not hit:
                    nonmatch_mask |= 1 << k

            all_dest_masks[state] = any_mask
            nonmatch_dest_masks[state] = nonmatch_mask

        # dp[pos] is a bitmask of KMP states from which positions pos..total-1
        # can be completed while satisfying all already-completed window rules.
        dp = [0] * (total + 1)
        dp[total] = (1 << m) - 1

        for pos in range(total - 1, -1, -1):
            next_states = dp[pos + 1]

            if pos < m - 1:
                masks = all_dest_masks
                current = 0
                for state, dest_mask in enumerate(masks):
                    if dest_mask & next_states:
                        current |= 1 << state
                dp[pos] = current
            else:
                rule = str1[pos - m + 1]

                if rule == 'T':
                    fallback_state = pi[m - 1]
                    dp[pos] = (1 << (m - 1)) if (next_states & (1 << fallback_state)) else 0
                else:
                    current = 0
                    for state, dest_mask in enumerate(nonmatch_dest_masks):
                        if dest_mask & next_states:
                            current |= 1 << state
                    dp[pos] = current

        if not (dp[0] & 1):
            return ""

        result = []
        state = 0

        for pos in range(total):
            rule = None if pos < m - 1 else str1[pos - m + 1]

            for c in range(26):
                next_state, hit = transition[state][c]

                if rule == 'T' and not hit:
                    continue
                if rule == 'F' and hit:
                    continue
                if dp[pos + 1] & (1 << next_state):
                    result.append(chr(c + 97))
                    state = next_state
                    break

        return "".join(result)