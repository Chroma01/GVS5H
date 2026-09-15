from array import array


class Solution:
    def minCostGoodCaption(self, caption: str) -> str:
        n = len(caption)
        if n < 3:
            return ""

        INF = 1 << 30
        vals = [ord(ch) - 97 for ch in caption]
        dist = [[abs(a - b) for b in range(26)] for a in range(26)]
        Dr = [dist[v] for v in vals]

        # C[pos][c] = min cost for suffix pos..n-1 given a run of char c of
        # length >= 3 has just ended at pos-1 (state V(pos, c, 3)).
        # A[p][c] = V(p,c,1) = cost[p][c] + cost[p+1][c] + C[p+2][c]
        # B[p][c] = V(p,c,2) = cost[p][c] + C[p+1][c]
        C = array('i', [0]) * ((n + 3) * 26)

        for pos in range(n - 1, -1, -1):
            cp = pos * 26
            Do = Dr[pos]
            base_next = (pos + 1) * 26

            # min over c' != c of (cost[pos][c'] + A[pos+1][c']) via min1/min2
            if pos <= n - 3:
                D1 = Dr[pos + 1]
                D2 = Dr[pos + 2]
                b3 = (pos + 3) * 26
                min1 = INF
                arg1 = -1
                min2 = INF
                for c in range(26):
                    v = Do[c] + D1[c] + D2[c] + C[b3 + c]
                    if v < min1:
                        min2 = min1
                        min1 = v
                        arg1 = c
                    elif v < min2:
                        min2 = v
            else:
                min1 = INF
                arg1 = -1
                min2 = INF

            for c in range(26):
                cont = Do[c] + C[base_next + c]
                sw = min2 if c == arg1 else min1
                C[cp + c] = cont if cont < sw else sw

        # total = min_c cost[0][c] + A[1][c] = min_c cost[0][c]+cost[1][c]+cost[2][c]+C[3][c]
        D1f = Dr[1]
        D2f = Dr[2]
        b3f = 78
        total = INF
        for c in range(26):
            v = Dr[0][c] + D1f[c] + D2f[c] + C[b3f + c]
            if v < total:
                total = v

        # Greedy lexicographic reconstruction.
        # prev_l in {0,1,2,3} = run length already fixed; cur = exact DP value of state.
        res = []
        i = 0
        prev_c = -1
        prev_l = 0
        cur = total
        while i < n:
            Do = Dr[i]
            if prev_l == 0:
                matched = False
                for x in range(26):
                    a1 = D1f[x] + D2f[x] + C[b3f + x]
                    if Do[x] + a1 == cur:
                        res.append(chr(97 + x))
                        prev_c = x
                        prev_l = 1
                        cur = a1
                        i += 1
                        matched = True
                        break
                if not matched:            # provably unreachable
                    return ""
            elif prev_l == 1:
                x = prev_c
                if i + 1 < n:
                    nxt = Dr[i + 1][x] + C[(i + 2) * 26 + x]
                else:
                    nxt = INF
                res.append(chr(97 + x))
                prev_l = 2
                cur = nxt
                i += 1
            elif prev_l == 2:
                x = prev_c
                nxt = C[(i + 1) * 26 + x] if i + 1 < n else 0
                res.append(chr(97 + x))
                prev_l = 3
                cur = nxt
                i += 1
            else:  # prev_l == 3
                matched = False
                for x in range(26):
                    if x == prev_c:
                        suf = C[(i + 1) * 26 + x] if i + 1 < n else 0
                        nl = 3
                    else:
                        if i + 1 < n - 1:
                            suf = Dr[i + 1][x] + Dr[i + 2][x] + C[(i + 3) * 26 + x]
                        else:
                            suf = INF
                        nl = 1
                    if Do[x] + suf == cur:
                        res.append(chr(97 + x))
                        prev_c = x
                        prev_l = nl
                        cur = suf
                        i += 1
                        matched = True
                        break
                if not matched:            # provably unreachable
                    return ""
        return "".join(res)