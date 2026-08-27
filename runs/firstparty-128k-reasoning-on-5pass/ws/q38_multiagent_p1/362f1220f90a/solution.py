class Solution:
    def generateString(self, str1: str, str2: str) -> str:
        n = len(str1)
        m = len(str2)
        N = n + m - 1

        pat = [ord(ch) - 97 for ch in str2]

        pi = [0] * m
        for i in range(1, m):
            j = pi[i - 1]
            while j > 0 and pat[i] != pat[j]:
                j = pi[j - 1]
            if pat[i] == pat[j]:
                j += 1
            pi[i] = j

        c_range = range(26)
        trans = [[0] * 26 for _ in range(m + 1)]
        for q in range(m + 1):
            match = pat[q] if q < m else -1
            fallback = pi[q - 1] if q > 0 else 0
            for c in c_range:
                if q < m and c == match:
                    trans[q][c] = q + 1
                elif q == 0:
                    trans[q][c] = 0
                else:
                    trans[q][c] = trans[fallback][c]

        bits = [1 << i for i in range(m + 1)]
        mask_none = [0] * (m + 1)
        mask_T = [0] * (m + 1)
        mask_F = [0] * (m + 1)
        for q in range(m + 1):
            mn = mt = mf = 0
            for c in c_range:
                ns = trans[q][c]
                b = bits[ns]
                mn |= b
                if ns == m:
                    mt |= b
                else:
                    mf |= b
            mask_none[q] = mn
            mask_T[q] = mt
            mask_F[q] = mf

        req = [0] * N
        for i, ch in enumerate(str1):
            req[i + m - 1] = 1 if ch == 'T' else 2

        all_states = (1 << (m + 1)) - 1
        dp = [0] * (N + 1)
        dp[N] = all_states
        mp1 = m + 1
        q_range = range(mp1)
        masks_by_req = (mask_none, mask_T, mask_F)

        for p in range(N - 1, -1, -1):
            masks = masks_by_req[req[p]]
            nxt = dp[p + 1]
            cur = 0
            for q in q_range:
                if masks[q] & nxt:
                    cur |= bits[q]
            if cur == 0:
                return ""
            dp[p] = cur

        if not (dp[0] & 1):
            return ""

        letters = [chr(97 + i) for i in c_range]
        ans = [''] * N
        state = 0
        for p in range(N):
            r = req[p]
            nxt = dp[p + 1]
            row = trans[state]
            for c in c_range:
                ns = row[c]
                if r == 1:
                    if ns != m:
                        continue
                elif r == 2:
                    if ns == m:
                        continue
                if nxt & bits[ns]:
                    ans[p] = letters[c]
                    state = ns
                    break
            else:
                return ""
        return ''.join(ans)