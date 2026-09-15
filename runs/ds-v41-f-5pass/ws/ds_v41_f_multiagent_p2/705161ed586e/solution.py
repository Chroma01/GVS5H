from array import array

class Solution:
    def minCostGoodCaption(self, caption: str) -> str:
        n = len(caption)
        if n < 3:
            return ""
        x = [ord(ch) - 97 for ch in caption]
        INF = 1 << 30
        # DIST[v][c] = |v - c|
        DIST = [[abs(v - c) for c in range(26)] for v in range(26)]

        total = (n + 1) * 26
        F1 = array('i', [INF]) * total   # run length so far == 1
        F3 = array('i', [0]) * total     # run length so far >= 3 (row n has 0)

        rng = range(26)
        F1_next = [INF] * 26   # F1[i+1]
        F3_next = [0] * 26     # F3[i+1]  (row n initially)
        F3_next2 = [0] * 26    # F3[i+2]

        for i in range(n - 1, -1, -1):
            dist = DIST[x[i]]
            row = i * 26
            if i <= n - 2:
                dist2 = DIST[x[i + 1]]
                F1cur = [dist[c] + dist2[c] + F3_next2[c] for c in rng]
            else:
                F1cur = [INF] * 26

            g = [dist[d] + F1_next[d] for d in rng]  # start new run with d
            m1 = min(g)
            idx = g.index(m1)
            m2 = INF
            for d in rng:
                if d != idx:
                    v = g[d]
                    if v < m2:
                        m2 = v
            cont = [dist[c] + F3_next[c] for c in rng]
            alt = [m1] * 26
            alt[idx] = m2
            F3cur = [cont[c] if cont[c] <= alt[c] else alt[c] for c in rng]

            F1[row:row + 26] = array('i', F1cur)
            F3[row:row + 26] = array('i', F3cur)
            F3_next2 = F3_next
            F3_next = F3cur
            F1_next = F1cur

        # choose first letter
        dist0 = DIST[x[0]]
        mincost = INF
        d0 = 0
        for d in rng:
            v = dist0[d] + F1[26 + d]
            if v < mincost:
                mincost = v
                d0 = d

        res = [chr(d0 + 97)]
        cur = d0
        runlen = 1
        i = 1
        while i < n:
            if runlen < 3:
                res.append(chr(cur + 97))
                runlen += 1
            else:
                dist = DIST[x[i]]
                target = F3[i * 26 + cur]
                nxt = (i + 1) * 26
                chosen = cur
                for d in rng:
                    if d == cur:
                        cost = dist[d] + F3[nxt + d]
                    else:
                        cost = dist[d] + F1[nxt + d]
                    if cost == target:
                        chosen = d
                        break
                res.append(chr(chosen + 97))
                if chosen == cur:
                    runlen += 1
                else:
                    cur = chosen
                    runlen = 1
            i += 1
        return ''.join(res)