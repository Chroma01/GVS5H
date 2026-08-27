import sys
from array import array


class Solution:
    def minCostGoodCaption(self, caption: str) -> str:
        n = len(caption)
        if n < 3:
            return ""

        INF = 10 ** 9
        A = 26

        # cost[i][c] = |caption[i] - c|
        base = [ord(ch) - 97 for ch in caption]
        cost = [[abs(b - c) for c in range(A)] for b in base]

        # rdp[i][c][k]: min cost to process positions i..n-1 given position i
        # is character c and the run ending at i has length k (k in {0,1,2}
        # representing run lengths 1, 2, 3+). Valid end only when k == 2.
        # Stored flat: index = (c * 3 + k).
        W = A * 3
        rdp = [array('i', [INF] * W) for _ in range(n + 1)]

        # last row: position n-1, char c, runlen 3+ -> cost only
        last = rdp[n - 1]
        cn1 = cost[n - 1]
        for c in range(A):
            last[c * 3 + 2] = cn1[c]

        for i in range(n - 2, -1, -1):
            nxt = rdp[i + 1]
            cur = rdp[i]
            ci = cost[i]

            # best and second-best over d of nxt[d][runlen=1] for switch moves
            best1 = INF
            best1c = -1
            best2 = INF
            for d in range(A):
                v = nxt[d * 3]  # runlen 1
                if v < best1:
                    best2 = best1
                    best1 = v
                    best1c = d
                elif v < best2:
                    best2 = v

            for c in range(A):
                cc = ci[c]
                o = c * 3
                # runlen 1 -> extend to runlen 2
                v = nxt[o + 1]
                if v < INF:
                    cur[o] = cc + v
                # runlen 2 -> extend to runlen 3
                v = nxt[o + 2]
                if v < INF:
                    cur[o + 1] = cc + v
                # runlen 3 -> extend (stay 3) or switch to d != c with runlen 1
                m = nxt[o + 2]
                sw = best2 if best1c == c else best1
                if sw < m:
                    m = sw
                if m < INF:
                    cur[o + 2] = cc + m

        # pick starting character: position 0 has runlen 1
        row0 = rdp[0]
        total = INF
        start_c = -1
        for c in range(A):
            v = row0[c * 3]
            if v < total:
                total = v
                start_c = c
        if total >= INF:
            return ""

        # greedy reconstruction: at each step choose the smallest next letter
        # that keeps the total cost optimal
        res = [chr(97 + start_c)]
        c = start_c
        k = 0  # run length state: 0 -> len 1
        spent = cost[0][c]
        for i in range(1, n):
            nxt = rdp[i]
            # candidates: extend (d == c), or switch (d != c) if k == 2
            chosen = -1
            chosen_k = -1
            chosen_tot = INF
            # try letters in increasing order; strict improvement keeps
            # the lexicographically smallest letter on ties
            if k == 2:
                lo, hi = 0, A
            else:
                lo, hi = c, c + 1
            for d in range(lo, hi):
                if k == 2:
                    nk = 0 if d != c else 2
                else:
                    nk = k + 1  # d == c here
                v = nxt[d * 3 + nk]
                if v >= INF:
                    continue
                t = spent + cost[i][d] + v
                if t < chosen_tot:
                    chosen_tot = t
                    chosen = d
                    chosen_k = nk
            res.append(chr(97 + chosen))
            spent += cost[i][chosen]
            c = chosen
            k = chosen_k

        return "".join(res)