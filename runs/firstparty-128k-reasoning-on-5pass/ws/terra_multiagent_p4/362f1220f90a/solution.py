class Solution:
    def generateString(self, str1: str, str2: str) -> str:
        n, m = len(str1), len(str2)
        length = n + m - 1

        # Overlay every required occurrence from T positions.
        forced = [-1] * length
        for i, flag in enumerate(str1):
            if flag == 'T':
                for j, ch in enumerate(str2):
                    pos = i + j
                    value = ord(ch) - ord('a')
                    if forced[pos] != -1 and forced[pos] != value:
                        return ""
                    forced[pos] = value

        # KMP prefix function.
        pi = [0] * m
        k = 0
        for i in range(1, m):
            while k > 0 and str2[k] != str2[i]:
                k = pi[k - 1]
            if str2[k] == str2[i]:
                k += 1
            pi[i] = k

        # go[c][state]: KMP state after adding character c.
        # States range from 0 to m - 1; a full match falls back to pi[m - 1].
        go = [[0] * m for _ in range(26)]
        first_char = ord(str2[0]) - ord('a')

        for c in range(26):
            go[c][0] = 1 if m > 1 and c == first_char else 0

        for state in range(1, m):
            expected = ord(str2[state]) - ord('a')
            fallback = pi[state - 1]
            for c in range(26):
                if c == expected:
                    go[c][state] = pi[m - 1] if state == m - 1 else state + 1
                else:
                    go[c][state] = go[c][fallback]

        last_char = ord(str2[-1]) - ord('a')
        full_mask = (1 << m) - 1

        # Masks of possible next states, with and without allowing a full match.
        out_all = [0] * m
        out_nonmatch = [0] * m
        for state in range(m):
            all_targets = 0
            nonmatch_targets = 0
            for c in range(26):
                target = go[c][state]
                all_targets |= 1 << target
                if not (state == m - 1 and c == last_char):
                    nonmatch_targets |= 1 << target
            out_all[state] = all_targets
            out_nonmatch[state] = nonmatch_targets

        # feasible[pos] contains KMP states that can complete positions pos..end.
        feasible = [0] * (length + 1)
        feasible[length] = full_mask

        for pos in range(length - 1, -1, -1):
            next_states = feasible[pos + 1]
            req = str1[pos - m + 1] if pos >= m - 1 else None
            fixed_char = forced[pos]

            if req == 'T':
                # A match ending here requires prior state m - 1 and last pattern char.
                if (fixed_char == -1 or fixed_char == last_char) and (
                    (next_states >> pi[m - 1]) & 1
                ):
                    feasible[pos] = 1 << (m - 1)
                else:
                    feasible[pos] = 0
                continue

            current = 0

            if fixed_char != -1:
                transitions = go[fixed_char]
                forbidden_match = req == 'F' and fixed_char == last_char
                for state in range(m):
                    if forbidden_match and state == m - 1:
                        continue
                    if (next_states >> transitions[state]) & 1:
                        current |= 1 << state
            else:
                allowed_targets = out_nonmatch if req == 'F' else out_all
                for state in range(m):
                    if allowed_targets[state] & next_states:
                        current |= 1 << state

            feasible[pos] = current

        if (feasible[0] & 1) == 0:
            return ""

        # Greedily reconstruct the lexicographically smallest feasible answer.
        answer = []
        state = 0

        for pos in range(length):
            req = str1[pos - m + 1] if pos >= m - 1 else None

            if forced[pos] != -1:
                candidates = (forced[pos],)
            else:
                candidates = range(26)

            chosen = -1
            for c in candidates:
                matched = state == m - 1 and c == last_char

                if req == 'T' and not matched:
                    continue
                if req == 'F' and matched:
                    continue

                nxt = go[c][state]
                if (feasible[pos + 1] >> nxt) & 1:
                    chosen = c
                    state = nxt
                    answer.append(chr(c + ord('a')))
                    break

            if chosen == -1:
                return ""

        return "".join(answer)