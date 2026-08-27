class Solution:
    def shortestMatchingSubstring(self, s: str, p: str) -> int:
        parts = p.split('*')
        blocks = [part for part in parts if part != '']
        n = len(s)

        # If all literal parts are empty, the empty substring matches.
        if not blocks:
            return 0

        occ_cache = {}

        def get_occ(block):
            if block not in occ_cache:
                occ_cache[block] = self._kmp_occurrences(s, block)
            return occ_cache[block]

        occs = [get_occ(block) for block in blocks]

        # If any required literal block does not occur, no match is possible.
        for occ in occs:
            if not occ:
                return -1

        k = len(blocks)

        # Only one literal block: the shortest match is the block itself.
        if k == 1:
            return len(blocks[0])

        INF = n + 1

        def build_next(occ):
            """
            nxt[i] = earliest occurrence start >= i, or INF if none.
            occ must be sorted ascending.
            """
            nxt = [INF] * (n + 1)
            j = len(occ) - 1
            cur = INF
            for i in range(n, -1, -1):
                if j >= 0 and occ[j] == i:
                    cur = i
                    j -= 1
                nxt[i] = cur
            return nxt

        next_cache = {}

        def get_next(block, occ):
            if block not in next_cache:
                next_cache[block] = build_next(occ)
            return next_cache[block]

        if k == 2:
            x, y = blocks
            next_y = get_next(y, occs[1])
            best = INF
            lx, ly = len(x), len(y)

            for sx in occs[0]:
                sy = next_y[sx + lx]
                if sy != INF:
                    cand = sy + ly - sx
                    if cand < best:
                        best = cand

            return -1 if best == INF else best

        # k == 3
        x, y, z = blocks
        next_y = get_next(y, occs[1])
        next_z = get_next(z, occs[2])
        best = INF
        lx, ly, lz = len(x), len(y), len(z)

        for sx in occs[0]:
            sy = next_y[sx + lx]
            if sy == INF:
                continue
            sz = next_z[sy + ly]
            if sz == INF:
                continue
            cand = sz + lz - sx
            if cand < best:
                best = cand

        return -1 if best == INF else best

    def _kmp_occurrences(self, s: str, pat: str) -> list:
        n = len(s)
        m = len(pat)

        if m == 0 or m > n:
            return []

        # Prefix function for KMP.
        pi = [0] * m
        j = 0
        for i in range(1, m):
            while j > 0 and pat[i] != pat[j]:
                j = pi[j - 1]
            if pat[i] == pat[j]:
                j += 1
            pi[i] = j

        occ = []
        j = 0
        for i, ch in enumerate(s):
            while j > 0 and ch != pat[j]:
                j = pi[j - 1]
            if ch == pat[j]:
                j += 1
            if j == m:
                occ.append(i - m + 1)
                j = pi[j - 1]

        return occ