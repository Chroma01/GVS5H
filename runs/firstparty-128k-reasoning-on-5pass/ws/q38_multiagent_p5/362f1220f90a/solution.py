class Solution:
    def generateString(self, str1: str, str2: str) -> str:
        n = len(str1)
        m = len(str2)
        L = n + m - 1

        pats = [ord(c) - 97 for c in str2]
        fixed = [-1] * L
        forbid = [0] * L

        range_m = range(m)
        range26 = range(26)

        for i, ch in enumerate(str1):
            if ch == 'T':
                for j in range_m:
                    pos = i + j
                    val = pats[j]
                    old = fixed[pos]
                    if old == -1:
                        fixed[pos] = val
                    elif old != val:
                        return ""
            else:
                forbid[i + m - 1] = 1

        pi = [0] * m
        for i in range(1, m):
            j = pi[i - 1]
            while j > 0 and pats[i] != pats[j]:
                j = pi[j - 1]
            if pats[i] == pats[j]:
                j += 1
            pi[i] = j
        pi_full = pi[m - 1]

        trans = [[0] * 26 for _ in range(m)]
        for k in range_m:
            row = trans[k]
            pk = pats[k]
            if k == 0:
                for ci in range26:
                    row[ci] = 1 if ci == pk else 0
            else:
                fall = trans[pi[k - 1]]
                for ci in range26:
                    row[ci] = k + 1 if ci == pk else fall[ci]

        all_states = (1 << m) - 1
        bits = [1 << k for k in range_m]
        mode_items = [[None] * m for _ in range(54)]
        mode_all = [0] * 54

        for f in range(-1, 26):
            chars = range26 if f == -1 else (f,)
            for forb in (0, 1):
                mode = (f + 1) * 2 + forb
                items = mode_items[mode]
                for k in range_m:
                    mask = 0
                    trk = trans[k]
                    for ci in chars:
                        raw = trk[ci]
                        if raw == m:
                            if forb:
                                continue
                            mask |= 1 << pi_full
                        else:
                            mask |= 1 << raw
                    items[k] = (mask, bits[k])
                    if mask:
                        mode_all[mode] |= bits[k]

        feasible = [0] * (L + 1)
        feasible[L] = all_states

        for p in range(L - 1, -1, -1):
            mode = (fixed[p] + 1) * 2 + forbid[p]
            nxt = feasible[p + 1]
            if nxt == all_states:
                cur = mode_all[mode]
            else:
                cur = 0
                for mask, bit in mode_items[mode]:
                    if mask & nxt:
                        cur |= bit
            if cur == 0:
                return ""
            feasible[p] = cur

        if (feasible[0] & 1) == 0:
            return ""

        letters = [chr(97 + i) for i in range26]
        all_chars = range26
        single_chars = [(i,) for i in range26]
        res = []
        k = 0

        for p in range(L):
            f = fixed[p]
            forb = forbid[p]
            trk = trans[k]
            chars = all_chars if f == -1 else single_chars[f]
            for ci in chars:
                raw = trk[ci]
                if raw == m:
                    if forb:
                        continue
                    nk = pi_full
                else:
                    nk = raw
                if (feasible[p + 1] >> nk) & 1:
                    res.append(letters[ci])
                    k = nk
                    break
            else:
                return ""

        return ''.join(res)