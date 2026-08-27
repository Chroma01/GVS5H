from array import array

class Solution:
    def minCostGoodCaption(self, caption: str) -> str:
        n = len(caption)
        if n < 3:
            return ""

        A = 26
        INF = 10**9
        size = (n + 1) * A

        dp1 = array('i', [INF]) * size
        dp2 = array('i', [INF]) * size
        dp3 = array('i', [INF]) * size

        base = n * A
        for c in range(A):
            dp3[base + c] = 0

        s = [ord(ch) - 97 for ch in caption]
        dist = [[abs(a - b) for b in range(A)] for a in range(A)]
        letters = [chr(97 + i) for i in range(A)]
        rangeA = range(A)

        d1, d2, d3 = dp1, dp2, dp3

        for i in range(n - 1, -1, -1):
            si = s[i]
            iA = i * A
            nA = iA + A
            drow = dist[si]

            min1 = INF
            min2 = INF
            cnt = 0
            arg = 0

            for x in rangeA:
                v = d1[nA + x] + drow[x]
                if v > INF:
                    v = INF

                if v < min1:
                    min2 = min1
                    min1 = v
                    cnt = 1
                    arg = x
                elif v == min1:
                    cnt += 1
                elif v < min2:
                    min2 = v

            for c in rangeA:
                cost = drow[c]
                nidx = nA + c

                v1 = d2[nidx] + cost
                if v1 > INF:
                    v1 = INF

                v2 = d3[nidx] + cost
                if v2 > INF:
                    v2 = INF

                idx = iA + c
                d1[idx] = v1
                d2[idx] = v2

                if cnt > 1 or c != arg:
                    sw = min1
                else:
                    sw = min2

                d3[idx] = v2 if v2 < sw else sw

        drow0 = dist[s[0]]
        off = A
        total = INF
        first = -1

        for x in rangeA:
            v = d1[off + x] + drow0[x]
            if v > INF:
                v = INF
            if v < total:
                total = v
                first = x

        if total >= INF or first < 0:
            return ""

        res = [letters[first]]
        state_c = first
        state_k = 1
        rem = d1[off + first]

        for i in range(1, n):
            nA = (i + 1) * A
            drow = dist[s[i]]

            if state_k == 1:
                y = state_c
                rem = d2[nA + y]
                state_k = 2
            elif state_k == 2:
                y = state_c
                rem = d3[nA + y]
                state_k = 3
            else:
                chosen = -1
                for y in rangeA:
                    nidx = nA + y
                    cost = drow[y]

                    if y == state_c:
                        nxt = d3[nidx]
                    else:
                        nxt = d1[nidx]

                    if cost + nxt == rem:
                        chosen = y
                        rem = nxt
                        if y == state_c:
                            state_k = 3
                        else:
                            state_c = y
                            state_k = 1
                        break

                if chosen < 0:
                    return ""
                y = chosen

            res.append(letters[y])

        if state_k != 3:
            return ""

        return ''.join(res)