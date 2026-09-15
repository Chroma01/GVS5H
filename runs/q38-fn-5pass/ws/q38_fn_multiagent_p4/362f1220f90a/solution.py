class Solution:
    def generateString(self, str1: str, str2: str) -> str:
        n = len(str1)
        m = len(str2)
        L = n + m - 1

        # Apply all 'T' constraints first.
        p = [ord(c) - 97 for c in str2]
        fixed = [-1] * L

        for i, ch in enumerate(str1):
            if ch == 'T':
                for j, val in enumerate(p):
                    pos = i + j
                    old = fixed[pos]
                    if old == -1:
                        fixed[pos] = val
                    elif old != val:
                        return ""

        # If there are no 'F' constraints, the T constraints determine everything.
        if 'F' not in str1:
            for v in fixed:
                if v < 0:
                    return ""
            return ''.join(chr(97 + v) for v in fixed)

        # KMP prefix function for str2.
        pi = [0] * m
        for i in range(1, m):
            j = pi[i - 1]
            while j and p[i] != p[j]:
                j = pi[j - 1]
            if p[i] == p[j]:
                j += 1
            pi[i] = j

        # KMP automaton for states 0..m-1.
        # A full match is normalized immediately to pi[m-1].
        go = [[0] * 26 for _ in range(m)]
        first = p[0]
        row0 = go[0]
        for c in range(26):
            row0[c] = 1 if c == first else 0

        for state in range(1, m):
            pc = p[state]
            fallback = go[pi[state - 1]]
            row = go[state]
            for c in range(26):
                if c == pc:
                    row[c] = state + 1
                else:
                    row[c] = fallback[c]

        q_bits = [1 << q for q in range(m)]
        full_mask = (1 << m) - 1
        m1 = m - 1
        last_c = p[-1]
        last_bit = q_bits[m1]

        # nxt[c][q] = normalized next KMP state.
        # next_bit[c][q] = 1 << nxt[c][q].
        # preimage_char[c][t] = states q with nxt[c][q] == t.
        nxt = [[0] * m for _ in range(26)]
        next_bit = [[0] * m for _ in range(26)]
        preimage_char = [[0] * m for _ in range(26)]

        for c in range(26):
            nc = nxt[c]
            nb = next_bit[c]
            pre = preimage_char[c]
            for q in range(m):
                raw = go[q][c]
                q2 = pi[m1] if raw == m else raw
                nc[q] = q2
                bit = q_bits[q2]
                nb[q] = bit
                pre[q2] |= q_bits[q]

        del go

        # For free positions:
        # all_next[q] = next states reachable by some character.
        # nonmatch_next[q] = next states reachable by a character that does
        #                    NOT complete str2 (needed at F-window ends).
        # preimage_all/nonmatch are inverse masks for sparse feasible sets.
        all_next = [0] * m
        nonmatch_next = [0] * m
        preimage_all = [0] * m
        preimage_nonmatch = [0] * m

        for q in range(m):
            qb = q_bits[q]
            a = 0
            nm = 0
            for c in range(26):
                t = nxt[c][q]
                bit = q_bits[t]
                a |= bit
                preimage_all[t] |= qb
                # A full match can only happen from state m-1 with last_c.
                if not (q == m1 and c == last_c):
                    nm |= bit
                    preimage_nonmatch[t] |= qb
            all_next[q] = a
            nonmatch_next[q] = nm

        # f_end[pos] is True iff an F-window ends at pos.
        f_end = [False] * L
        for i, ch in enumerate(str1):
            if ch == 'F':
                f_end[i + m - 1] = True

        # Suffix feasibility DP.
        # feas[pos] is an m-bit mask: bit q is set iff suffix pos..L-1 can be
        # completed when the current normalized KMP state before pos is q.
        feas = [0] * (L + 1)
        feas[L] = full_mask
        SPARSE = 128

        for pos in range(L - 1, -1, -1):
            B = feas[pos + 1]
            if B == 0:
                return ""

            cfix = fixed[pos]
            fe = f_end[pos]

            # Very common dense case.
            if B == full_mask:
                if cfix == -1:
                    feas[pos] = full_mask
                elif fe and cfix == last_c:
                    cur = full_mask & ~last_bit
                    if cur == 0:
                        return ""
                    feas[pos] = cur
                else:
                    feas[pos] = full_mask
                continue

            cur = 0
            bc = B.bit_count()

            if cfix != -1:
                # Fixed character: deterministic transition.
                if bc <= SPARSE:
                    pre = preimage_char[cfix]
                    x = B
                    while x:
                        lsb = x & -x
                        t = lsb.bit_length() - 1
                        cur |= pre[t]
                        x ^= lsb
                        if cur == full_mask:
                            break
                    if fe and cfix == last_c:
                        cur &= ~last_bit
                else:
                    bits = next_bit[cfix]
                    if fe and cfix == last_c:
                        # State m-1 would complete str2.
                        for q in range(m1):
                            if bits[q] & B:
                                cur |= q_bits[q]
                    else:
                        for q in range(m):
                            if bits[q] & B:
                                cur |= q_bits[q]
            else:
                # Free character: exists a valid character leading into B.
                if bc <= SPARSE:
                    pre = preimage_nonmatch if fe else preimage_all
                    x = B
                    while x:
                        lsb = x & -x
                        t = lsb.bit_length() - 1
                        cur |= pre[t]
                        x ^= lsb
                        if cur == full_mask:
                            break
                else:
                    masks = nonmatch_next if fe else all_next
                    for q in range(m):
                        if masks[q] & B:
                            cur |= q_bits[q]

            if cur == 0:
                return ""
            feas[pos] = cur

        if (feas[0] & 1) == 0:
            return ""

        # Greedy lexicographic reconstruction using the feasibility table.
        chars = [chr(97 + i) for i in range(26)]
        res = []
        q = 0

        for pos in range(L):
            if (feas[pos] & q_bits[q]) == 0:
                return ""

            B = feas[pos + 1]
            fe = f_end[pos]
            cfix = fixed[pos]

            if cfix != -1:
                if fe and q == m1 and cfix == last_c:
                    return ""
                q2 = nxt[cfix][q]
                if (B & q_bits[q2]) == 0:
                    return ""
                res.append(chars[cfix])
                q = q2
            else:
                chosen = -1
                for cidx in range(26):
                    if fe and q == m1 and cidx == last_c:
                        continue
                    q2 = nxt[cidx][q]
                    if B & q_bits[q2]:
                        chosen = cidx
                        q = q2
                        break
                if chosen == -1:
                    return ""
                res.append(chars[chosen])

        return ''.join(res)