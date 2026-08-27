from array import array

COST_TABLE = [[abs(i - j) for j in range(26)] for i in range(26)]
CHARS = [chr(97 + i) for i in range(26)]

STATES = 79
START = 0
OFF = [1 + 3 * c for c in range(26)]

_TYPE = 'i'
if array('i').itemsize < 4:
    _TYPE = 'l'
    if array('l').itemsize < 4:
        _TYPE = 'q'


class Solution:
    def minCostGoodCaption(self, caption: str) -> str:
        n = len(caption)
        if n < 3:
            return ""

        INF = 1_000_000_000
        cost_table = COST_TABLE
        chars = CHARS
        off = OFF
        states = STATES
        range26 = range(26)

        rows = [cost_table[ord(ch) - 97] for ch in caption]

        size = (n + 1) * states
        dp = array(_TYPE, [INF]) * size
        d = dp

        base = n * states
        for c in range26:
            d[base + off[c] + 2] = 0

        cur = (n - 1) * states
        for i in range(n - 1, -1, -1):
            nxt = cur + states
            row = rows[i]

            b1v = INF
            b1c = -1
            b2v = INF
            for x in range26:
                v = row[x] + d[nxt + off[x]]
                if v < b1v:
                    b2v = b1v
                    b1v = v
                    b1c = x
                elif v < b2v:
                    b2v = v

            d[cur] = b1v

            for c in range26:
                o = off[c]
                cost = row[c]
                nb = nxt + o
                cb = cur + o

                v1 = cost + d[nb + 1]
                d[cb] = v1

                v2 = cost + d[nb + 2]
                d[cb + 1] = v2

                sw = b1v if b1c != c else b2v
                d[cb + 2] = v2 if v2 < sw else sw

            cur -= states

        ans = d[START]
        if ans >= INF:
            return ""

        res = [''] * n
        state = START
        cur = 0

        for i in range(n):
            nxt = cur + states
            row = rows[i]
            cur_val = d[cur + state]

            if state == START:
                for x in range26:
                    ns = off[x]
                    if row[x] + d[nxt + ns] == cur_val:
                        state = ns
                        res[i] = chars[x]
                        break
                else:
                    return ""
            else:
                s = state - 1
                c = s // 3
                length = s % 3 + 1

                if length < 3:
                    ns = state + 1
                    if row[c] + d[nxt + ns] == cur_val:
                        state = ns
                        res[i] = chars[c]
                    else:
                        return ""
                else:
                    for x in range26:
                        ns = state if x == c else off[x]
                        if row[x] + d[nxt + ns] == cur_val:
                            state = ns
                            res[i] = chars[x]
                            break
                    else:
                        return ""

            cur += states

        if state == START or (state - 1) % 3 != 2:
            return ""

        return ''.join(res)