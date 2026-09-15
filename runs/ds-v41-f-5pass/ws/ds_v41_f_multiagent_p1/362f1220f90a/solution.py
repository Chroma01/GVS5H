class Solution:
    def generateString(self, str1: str, str2: str) -> str:
        n = len(str1)
        m = len(str2)
        L = n + m - 1

        # prefix function of str2
        pi = [0] * m
        for i in range(1, m):
            j = pi[i - 1]
            while j > 0 and str2[i] != str2[j]:
                j = pi[j - 1]
            if str2[i] == str2[j]:
                j += 1
            pi[i] = j

        # KMP automaton: states 0..m (length of longest prefix of str2
        # that is a suffix of the text read so far)
        nxt = [[0] * 26 for _ in range(m + 1)]
        for s in range(m):
            row = nxt[s]
            for ci in range(26):
                c = chr(97 + ci)
                j = s
                while j > 0 and str2[j] != c:
                    j = pi[j - 1]
                if str2[j] == c:
                    j += 1
                row[ci] = j
        # from state m, the relevant border is the longest proper border
        b = pi[m - 1] if m > 0 else 0
        for ci in range(26):
            nxt[m][ci] = nxt[b][ci]

        # reachability masks (bitmask over states) for all chars / non-m chars
        full = [0] * (m + 1)
        nonm = [0] * (m + 1)
        for s in range(m + 1):
            fm = 0
            nm = 0
            for ci in range(26):
                t = nxt[s][ci]
                fm |= (1 << t)
                if t != m:
                    nm |= (1 << t)
            full[s] = fm
            nonm[s] = nm

        # backward DP: dp[p] = bitmask of states from which positions p..L-1
        # can be completed satisfying all constraints
        dp = [0] * (L + 1)
        dp[L] = (1 << (m + 1)) - 1
        mstart = m - 1
        for p in range(L - 1, -1, -1):
            typ = str1[p - mstart] if p >= mstart else None
            nxtdp = dp[p + 1]
            if typ == 'T':
                if (nxtdp >> m) & 1:
                    cur = 0
                    for s in range(m + 1):
                        if (full[s] >> m) & 1:
                            cur |= (1 << s)
                    dp[p] = cur
                else:
                    dp[p] = 0
            elif typ == 'F':
                cur = 0
                for s in range(m + 1):
                    if nonm[s] & nxtdp:
                        cur |= (1 << s)
                dp[p] = cur
            else:
                cur = 0
                for s in range(m + 1):
                    if full[s] & nxtdp:
                        cur |= (1 << s)
                dp[p] = cur

        if not (dp[0] & 1):
            return ""

        # greedy lexicographically smallest reconstruction
        res = []
        s = 0
        for p in range(L):
            typ = str1[p - mstart] if p >= mstart else None
            nxtdp = dp[p + 1]
            for ci in range(26):
                t = nxt[s][ci]
                if typ == 'T' and t != m:
                    continue
                if typ == 'F' and t == m:
                    continue
                if (nxtdp >> t) & 1:
                    res.append(chr(97 + ci))
                    s = t
                    break
        return ''.join(res)