class Solution:
    def generateString(self, str1: str, str2: str) -> str:
        n = len(str1)
        m = len(str2)
        total = n + m - 1

        # Stamp all required occurrences and reject conflicting overlaps.
        word = [''] * total
        forced = [False] * total

        for i, flag in enumerate(str1):
            if flag == 'T':
                for j, ch in enumerate(str2):
                    pos = i + j
                    if forced[pos] and word[pos] != ch:
                        return ""
                    word[pos] = ch
                    forced[pos] = True

        # KMP prefix function.
        pi = [0] * m
        for i in range(1, m):
            j = pi[i - 1]
            while j > 0 and str2[i] != str2[j]:
                j = pi[j - 1]
            if str2[i] == str2[j]:
                j += 1
            pi[i] = j

        # KMP transitions. States are matched prefix lengths 0..m-1.
        next_state = [[0] * 26 for _ in range(m)]
        completes = [[False] * 26 for _ in range(m)]

        for state in range(m):
            for c in range(26):
                ch = chr(ord('a') + c)
                q = state

                while q > 0 and str2[q] != ch:
                    q = pi[q - 1]

                if str2[q] == ch:
                    q += 1

                if q == m:
                    completes[state][c] = True
                    q = pi[m - 1]

                next_state[state][c] = q

        # Reverse transition masks, indexed by character then destination state.
        rev_any = [[0] * m for _ in range(26)]
        rev_nonmatch = [[0] * m for _ in range(26)]
        rev_match = [[0] * m for _ in range(26)]

        # Reverse masks when any character is available.
        rev_any_free = [0] * m
        rev_nonmatch_free = [0] * m

        for state in range(m):
            bit = 1 << state
            for c in range(26):
                target = next_state[state][c]
                rev_any[c][target] |= bit
                rev_any_free[target] |= bit

                if completes[state][c]:
                    rev_match[c][target] |= bit
                else:
                    rev_nonmatch[c][target] |= bit
                    rev_nonmatch_free[target] |= bit

        def preimage(target_mask, reverse_masks):
            result = 0
            while target_mask:
                low = target_mask & -target_mask
                target = low.bit_length() - 1
                result |= reverse_masks[target]
                target_mask -= low
            return result

        # feasible[pos] contains KMP states from which suffix pos..end works.
        feasible = [0] * (total + 1)
        feasible[total] = (1 << m) - 1

        for pos in range(total - 1, -1, -1):
            target_mask = feasible[pos + 1]
            requirement = str1[pos - m + 1] if pos >= m - 1 else None

            if forced[pos]:
                c = ord(word[pos]) - ord('a')
                if requirement == 'T':
                    feasible[pos] = preimage(target_mask, rev_match[c])
                elif requirement == 'F':
                    feasible[pos] = preimage(target_mask, rev_nonmatch[c])
                else:
                    feasible[pos] = preimage(target_mask, rev_any[c])
            else:
                if requirement == 'T':
                    # Every character of a T window was stamped above.
                    feasible[pos] = 0
                elif requirement == 'F':
                    feasible[pos] = preimage(target_mask, rev_nonmatch_free)
                else:
                    feasible[pos] = preimage(target_mask, rev_any_free)

        if (feasible[0] & 1) == 0:
            return ""

        # Greedily select the smallest character preserving feasibility.
        state = 0
        result = []

        for pos in range(total):
            requirement = str1[pos - m + 1] if pos >= m - 1 else None
            candidates = [ord(word[pos]) - ord('a')] if forced[pos] else range(26)
            target_mask = feasible[pos + 1]

            for c in candidates:
                is_match = completes[state][c]

                if requirement == 'T' and not is_match:
                    continue
                if requirement == 'F' and is_match:
                    continue

                nxt = next_state[state][c]
                if (target_mask >> nxt) & 1:
                    result.append(chr(ord('a') + c))
                    state = nxt
                    break
            else:
                return ""

        return ''.join(result)