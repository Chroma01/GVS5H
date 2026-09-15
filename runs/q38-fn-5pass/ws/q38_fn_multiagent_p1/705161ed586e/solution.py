class Solution:
    def minCostGoodCaption(self, caption: str) -> str:
        n = len(caption)
        if n < 3:
            return ""

        from array import array

        A = 26
        S = A * 3
        INF = 10**9

        # dp[i][c][l] flattened:
        # i = next position to fill
        # c = last character of the already-built prefix
        # l = current run length capped at 3 (stored as 0,1,2 for lengths 1,2,3+)
        total = (n + 1) * S
        dp = array('i', [INF]) * total

        # At the end, the last run must already have length at least 3.
        base = n * S
        for c in range(A):
            dp[base + c * 3 + 2] = 0

        # cost_table[ch][x] = operations to change original ch to target x
        cost_table = [bytes(abs(c - x) for x in range(A)) for c in range(A)]
        codes = [b - 97 for b in caption.encode()]
        offs = [c * 3 for c in range(A)]
        R = range(A)
        d = dp

        # Backward DP. dp[0] is not needed because the first character is handled
        # separately during reconstruction.
        for i in range(n - 1, 0, -1):
            w = cost_table[codes[i]]
            next_off = (i + 1) * S
            cur_off = i * S

            # For states with run length 3, switching to a different character x
            # costs w[x] + dp[i+1][x][1]. We need the best and second-best x.
            best1 = INF
            best2 = INF
            idx1 = -1

            for x in R:
                val = w[x] + d[next_off + offs[x]]
                if val < best1:
                    best2 = best1
                    best1 = val
                    idx1 = x
                elif val < best2:
                    best2 = val

            for c in R:
                off = cur_off + offs[c]
                noff = next_off + offs[c]
                wc = w[c]

                # Current run length is 1: must continue with c.
                d[off] = wc + d[noff + 1]

                # Current run length is 2: must continue with c.
                d[off + 1] = wc + d[noff + 2]

                # Current run length is at least 3:
                # either continue with c, or switch to some x != c.
                # switch_cost already includes the cost of the new character x.
                same_cost = wc + d[noff + 2]
                switch_cost = best2 if idx1 == c else best1
                if switch_cost < same_cost:
                    d[off + 2] = switch_cost
                else:
                    d[off + 2] = same_cost

        # Initial choice: pick the first character and enter state (x, length 1).
        ans = INF
        w0 = cost_table[codes[0]]
        off1 = S
        for x in R:
            val = w0[x] + d[off1 + offs[x]]
            if val < ans:
                ans = val

        if ans >= INF:
            return ""

        # Greedy left-to-right reconstruction.
        # At each position, choose the smallest character that can still achieve
        # the optimal remaining cost according to the suffix DP.
        res = bytearray()
        rem = ans
        prev = -1
        run = 0

        for i in range(n):
            w = cost_table[codes[i]]
            next_off = (i + 1) * S
            found = False

            if i == 0:
                for x in R:
                    if w[x] + d[next_off + offs[x]] == rem:
                        res.append(97 + x)
                        prev = x
                        run = 1
                        rem -= w[x]
                        found = True
                        break
            else:
                for x in R:
                    if x == prev:
                        nr = run + 1 if run < 3 else 3
                        idx = next_off + offs[x] + (nr - 1)
                    else:
                        if run != 3:
                            continue
                        nr = 1
                        idx = next_off + offs[x]

                    if w[x] + d[idx] == rem:
                        res.append(97 + x)
                        prev = x
                        run = nr
                        rem -= w[x]
                        found = True
                        break

            if not found:
                return ""

        if rem != 0:
            return ""

        return res.decode()