class Solution:
    def generateString(self, str1: str, str2: str) -> str:
        n, m = len(str1), len(str2)
        L = n + m - 1

        # KMP prefix function for str2.
        s2 = [ord(ch) - 97 for ch in str2]
        pi = [0] * m
        for i in range(1, m):
            j = pi[i - 1]
            while j and s2[i] != s2[j]:
                j = pi[j - 1]
            if s2[i] == s2[j]:
                j += 1
            pi[i] = j

        # Build KMP automaton states 0..m.
        # State m means the last m characters are exactly str2.
        trans = []
        row0 = [0] * 26
        row0[s2[0]] = 1
        trans.append(row0)

        for state in range(1, m):
            row = trans[pi[state - 1]].copy()
            row[s2[state]] = state + 1
            trans.append(row)

        # From accepting state m, fallback before consuming the next character.
        trans.append(trans[pi[m - 1]].copy())

        # Bit masks for automaton states.
        bits = [1 << i for i in range(m + 1)]
        m_bit = bits[m]
        full_mask = (1 << (m + 1)) - 1
        non_m_mask = full_mask ^ m_bit

        trans_bits = []
        tm_pairs = []       # (all next-state mask, current-state bit)
        tmn_pairs = []      # (non-m next-state mask, current-state bit)
        reach_m_mask = 0
        full_no_mask = 0
        full_F_mask = 0

        for s, row in enumerate(trans):
            rb = [bits[ns] for ns in row]
            trans_bits.append(rb)

            mask = 0
            for b in rb:
                mask |= b

            if mask:
                tm_pairs.append((mask, bits[s]))
                full_no_mask |= bits[s]

            no_m = mask & non_m_mask
            if no_m:
                tmn_pairs.append((no_m, bits[s]))
                full_F_mask |= bits[s]

            if mask & m_bit:
                reach_m_mask |= bits[s]

        is_t = [ch == 'T' for ch in str1]

        # masks[p] = bitmask of automaton states before position p
        # from which suffix p..L-1 can be completed.
        masks = [0] * (L + 1)
        masks[L] = full_mask
        m1 = m - 1

        # Cache repeated feasibility transitions.
        cache_no = {full_mask: full_no_mask, 0: 0}
        cache_f = {full_mask: full_F_mask, 0: 0}

        # Positions that end a length-m window.
        for p in range(L - 1, m1 - 1, -1):
            next_mask = masks[p + 1]

            if is_t[p - m1]:
                if not (next_mask & m_bit):
                    return ""
                if reach_m_mask == 0:
                    return ""
                masks[p] = reach_m_mask
            else:
                res = cache_f.get(next_mask)
                if res is None:
                    cur = 0
                    for mask, bit in tmn_pairs:
                        if mask & next_mask:
                            cur |= bit
                    res = cur
                    cache_f[next_mask] = res

                if res == 0:
                    return ""
                masks[p] = res

        # Prefix positions before the first full window.
        for p in range(m1 - 1, -1, -1):
            next_mask = masks[p + 1]

            res = cache_no.get(next_mask)
            if res is None:
                cur = 0
                for mask, bit in tm_pairs:
                    if mask & next_mask:
                        cur |= bit
                res = cur
                cache_no[next_mask] = res

            if res == 0:
                return ""
            masks[p] = res

        if not (masks[0] & 1):
            return ""

        # Greedily construct the lexicographically smallest feasible string.
        ans = []
        state = 0
        letters = [chr(97 + i) for i in range(26)]

        for p in range(L):
            next_mask = masks[p + 1]
            rb = trans_bits[state]
            row = trans[state]

            if p < m1:
                for c in range(26):
                    if next_mask & rb[c]:
                        ans.append(letters[c])
                        state = row[c]
                        break
                else:
                    return ""

            elif is_t[p - m1]:
                if not (next_mask & m_bit):
                    return ""
                for c in range(26):
                    if rb[c] == m_bit:
                        ans.append(letters[c])
                        state = m
                        break
                else:
                    return ""

            else:
                for c in range(26):
                    if rb[c] != m_bit and (next_mask & rb[c]):
                        ans.append(letters[c])
                        state = row[c]
                        break
                else:
                    return ""

        return ''.join(ans)