class Solution:
    def generateString(self, str1: str, str2: str) -> str:
        n = len(str1)
        m = len(str2)
        L = n + m - 1

        pi = [0] * m
        for i in range(1, m):
            j = pi[i - 1]
            while j > 0 and str2[i] != str2[j]:
                j = pi[j - 1]
            if str2[i] == str2[j]:
                j += 1
            pi[i] = j

        pat = [ord(c) - 97 for c in str2]
        states = m + 1
        trans = [[0] * 26 for _ in range(states)]

        for q in range(states):
            if q < m:
                target = pat[q]
                if q == 0:
                    for ci in range(26):
                        trans[q][ci] = 1 if ci == target else 0
                else:
                    fallback = trans[pi[q - 1]]
                    row = trans[q]
                    for ci in range(26):
                        if ci == target:
                            row[ci] = q + 1
                        else:
                            row[ci] = fallback[ci]
            else:
                fallback = trans[pi[m - 1]]
                row = trans[q]
                for ci in range(26):
                    row[ci] = fallback[ci]

        single = [0] * states
        for q in range(states):
            bit = 1 << q
            row = trans[q]
            for ci in range(26):
                single[row[ci]] |= bit

        all_mask = (1 << states) - 1
        bit_m = 1 << m
        not_m_mask = all_mask ^ bit_m
        canT_mask = single[m]

        B = 8
        SIZE = 1 << B
        CHUNK_MASK = SIZE - 1
        chunks = (states + B - 1) // B
        table = []
        for k in range(chunks):
            shift = k * B
            tbl = [0] * SIZE
            for v in range(1, SIZE):
                lb = v & -v
                idx = lb.bit_length() - 1
                t = shift + idx
                prev = v ^ lb
                if t < states:
                    tbl[v] = tbl[prev] | single[t]
                else:
                    tbl[v] = tbl[prev]
            table.append(tbl)

        def preimage(mask: int, table=table, chunk_mask=CHUNK_MASK, B=B) -> int:
            res = 0
            for tbl in table:
                if not mask:
                    break
                v = mask & chunk_mask
                if v:
                    res |= tbl[v]
                mask >>= B
            return res

        feas = [0] * (L + 1)
        feas[L] = all_mask
        m_minus_1 = m - 1

        for p in range(L - 1, -1, -1):
            nxt = feas[p + 1]
            if p < m_minus_1:
                feas[p] = preimage(nxt)
            else:
                if str1[p - m_minus_1] == 'T':
                    feas[p] = canT_mask if (nxt & bit_m) else 0
                else:
                    feas[p] = preimage(nxt & not_m_mask)

        if not (feas[0] & 1):
            return ""

        bits = [1 << i for i in range(states)]
        ans = []
        state = 0

        for p in range(L):
            nxt = feas[p + 1]
            if p < m_minus_1:
                allowed = nxt
            elif str1[p - m_minus_1] == 'T':
                allowed = bit_m if (nxt & bit_m) else 0
            else:
                allowed = nxt & not_m_mask

            row = trans[state]
            chosen = -1
            for ci in range(26):
                ns = row[ci]
                if allowed & bits[ns]:
                    chosen = ci
                    break

            if chosen == -1:
                return ""

            ans.append(chr(97 + chosen))
            state = row[chosen]

        return "".join(ans)