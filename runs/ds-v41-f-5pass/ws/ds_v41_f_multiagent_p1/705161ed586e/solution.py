class Solution:
    def minCostGoodCaption(self, caption: str) -> str:
        n = len(caption)
        if n < 3:
            return ""
        s = [ord(ch) - 97 for ch in caption]
        INF = 1 << 30
        # Precompute alphabet distances
        dist = [[abs(i - j) for j in range(26)] for i in range(26)]
        
        # State index: c*3 + (L-1), L in {1,2,3}
        # f[i][c][L] = min cost to fill i..n-1 given run of c ending at i-1 has length L (capped at 3)
        prev = [INF] * 78
        for c in range(26):
            prev[c * 3 + 2] = 0  # only a run of length >= 3 may finish the string
        cur = [0] * 78
        parents = bytearray(n * 26)
        rng = range(26)
        
        for i in range(n - 1, 0, -1):
            si = s[i]
            costs = dist[si]
            min1 = INF; arg1 = -1
            min2 = INF; arg2 = -1
            for c in rng:
                cost = costs[c]
                j = c * 3
                cur[j] = cost + prev[j + 1]      # L=1 -> forced place c -> L=2
                cur[j + 1] = cost + prev[j + 2]  # L=2 -> forced place c -> L=3
                v = cost + prev[j]               # switch to c (new run length 1)
                if v < min1:
                    min2 = min1; arg2 = arg1
                    min1 = v; arg1 = c
                elif v < min2:
                    min2 = v; arg2 = c
            pbase = i * 26
            for c in rng:
                cost = costs[c]
                j = c * 3
                cont = cost + prev[j + 2]        # continue current run c (stays L=3)
                if arg1 != c:
                    sw = min1; sw_d = arg1
                else:
                    sw = min2; sw_d = arg2
                if cont < sw:
                    cur[j + 2] = cont
                    parents[pbase + c] = c
                elif sw < cont:
                    cur[j + 2] = sw
                    parents[pbase + c] = sw_d
                else:
                    cur[j + 2] = cont
                    parents[pbase + c] = c if c < sw_d else sw_d
            prev, cur = cur, prev
        
        s0 = s[0]
        total = INF
        first_choice = 0
        for d in rng:
            cost = dist[s0][d]
            v = cost + prev[d * 3]               # prev is now f[1]
            if v < total:
                total = v
                first_choice = d
        
        res = [first_choice]
        c = first_choice
        L = 1
        for i in range(1, n):
            if L < 3:
                d = c
                L += 1
            else:
                d = parents[i * 26 + c]
                L = 3 if d == c else 1
            res.append(d)
            c = d
        return "".join(chr(x + 97) for x in res)