from array import array


class Solution:
    def minCostGoodCaption(self, caption: str) -> str:
        n = len(caption)
        if n < 3:
            return ""

        INF = 10**18

        # cost[i*26 + c] = |caption[i] - c|, fits in a byte (<= 25)
        cost = bytearray(26 * n)
        for i, ch in enumerate(caption):
            o = ord(ch) - 97
            base = i * 26
            for c in range(26):
                cost[base + c] = o - c if o >= c else c - o

        # B[i]: min cost to transform caption[i:] given position i starts a new block.
        # R3[c][i]: min cost to transform caption[i:] given the block containing
        #           position i-1 has character c and length >= 3 (run may end or continue).
        # Padded to length n+3: B[n] = 0, B[n+1] = B[n+2] = INF;
        # R3[c][n] = 0, R3[c][n+1] = R3[c][n+2] = INF.
        size = n + 3
        B = array('q', [INF]) * size
        R3 = [array('q', [INF]) * size for _ in range(26)]
        B[n] = 0
        for c in range(26):
            R3[c][n] = 0

        # Backward DP.
        # R3[c][i] = cost[i][c] + min(R3[c][i+1], B[i+1])
        # B[i] = min over c of cost[i][c] + cost[i+1][c] + cost[i+2][c] + R3[c][i+3]
        # (cost beyond n-1 treated as 0; the INF sentinels at R3[*][n+1], R3[*][n+2]
        #  and B[n+1], B[n+2] invalidate blocks that would run past the end).
        for i in range(n - 1, -1, -1):
            base = i * 26
            b1 = B[i + 1]
            best = INF
            i1 = base + 26 if i + 1 < n else None
            i2 = base + 52 if i + 2 < n else None
            i3 = i + 3
            for c in range(26):
                r = R3[c]
                v = cost[base + c] + (r[i + 1] if r[i + 1] < b1 else b1)
                r[i] = v
                s = cost[base + c]
                s += cost[i1 + c] if i1 is not None else 0
                s += cost[i2 + c] if i2 is not None else 0
                s += r[i3]
                if s < best:
                    best = s
            B[i] = best

        if B[0] >= INF:
            return ""

        # Greedy lexicographically-smallest reconstruction among optimal captions.
        # States: 0 = B (block boundary), 1 = R1 (run length 1, must continue),
        #         2 = R2 (run length 2, must continue),
        #         3 = R3 (run length >= 3, may continue or end).
        out = []
        i = 0
        state = 0
        cur = -1  # run character for R states
        while i < n:
            base = i * 26
            if state == 0:
                target = B[i]
                i1 = base + 26 if i + 1 < n else None
                i2 = base + 52 if i + 2 < n else None
                i3 = i + 3
                for c in range(26):
                    s = cost[base + c]
                    s += cost[i1 + c] if i1 is not None else 0
                    s += cost[i2 + c] if i2 is not None else 0
                    s += R3[c][i3]
                    if s == target:
                        out.append(chr(97 + c))
                        cur = c
                        state = 1
                        i += 1
                        break
            elif state == 1:
                out.append(chr(97 + cur))
                state = 2
                i += 1
            elif state == 2:
                out.append(chr(97 + cur))
                state = 3
                i += 1
            else:
                r = R3[cur]
                cont = cost[base + cur] + r[i + 1] == r[i]
                end = B[i] == r[i]
                if cont and end:
                    # Continue gives next char cur; end gives B[i]'s best char d.
                    # On tie (d == cur) continuing is always <= ending (proven in
                    # plan), so end only when d is strictly smaller than cur.
                    target = B[i]
                    i1 = base + 26 if i + 1 < n else None
                    i2 = base + 52 if i + 2 < n else None
                    i3 = i + 3
                    d = 26
                    for c in range(26):
                        s = cost[base + c]
                        s += cost[i1 + c] if i1 is not None else 0
                        s += cost[i2 + c] if i2 is not None else 0
                        s += R3[c][i3]
                        if s == target:
                            d = c
                            break
                    if d < cur:
                        state = 0
                    else:
                        out.append(chr(97 + cur))
                        i += 1
                elif cont:
                    out.append(chr(97 + cur))
                    i += 1
                else:
                    state = 0

        return "".join(out)