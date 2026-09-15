class Solution:
    def minCostGoodCaption(self, caption: str) -> str:
        n = len(caption)
        if n < 3:
            return ""

        from array import array

        INF = 10**9
        STATES = 78  # 26 characters * 3 capped run lengths

        # ASCII bytes: a[i] - 97 gives 0..25.
        a = caption.encode()

        # dp[i][c][l] flattened as dp[i * 78 + c * 3 + (l - 1)].
        # l = 1, 2, or 3, where 3 means length at least 3.
        dp = array('i', [INF]) * ((n + 1) * STATES)

        # Base: after the last position, only an already valid run is allowed.
        base = n * STATES
        for c in range(26):
            dp[base + c * 3 + 2] = 0

        # cost[ch][target] = alphabet distance.
        cost = [[abs(i - j) for j in range(26)] for i in range(26)]
        offs = [c * 3 for c in range(26)]
        range26 = range(26)

        # Suffix DP.
        for i in range(n - 1, -1, -1):
            ch = a[i] - 97
            cost_ch = cost[ch]
            cb = i * STATES
            nb = cb + STATES

            # best/second-best switch cost:
            # g[d] = cost to put d at i + dp[i + 1][d][1]
            best1 = INF
            best2 = INF
            best_idx = -1

            for d, off in enumerate(offs):
                val = dp[nb + off] + cost_ch[d]
                if val < best1:
                    best2 = best1
                    best1 = val
                    best_idx = d
                elif val < best2:
                    best2 = val

            for c, off in enumerate(offs):
                dc = cost_ch[c]

                # Current run length 1: must extend to length 2.
                v1 = dp[nb + off + 1] + dc
                if v1 >= INF:
                    v1 = INF
                dp[cb + off] = v1

                # Current run length 2: must extend to length 3.
                # Also used as "extend same character" for length 3.
                v2 = dp[nb + off + 2] + dc
                if v2 >= INF:
                    v2 = INF
                dp[cb + off + 1] = v2

                # Current run length 3: either extend same char, or switch
                # to a different char. Switching to the same char is invalid
                # because adjacent same runs would merge.
                sw = best2 if best_idx == c else best1
                dp[cb + off + 2] = v2 if v2 < sw else sw

        # Choose the first character: smallest character achieving global optimum.
        row1 = STATES
        ch0 = a[0] - 97
        cost0 = cost[ch0]
        ans = INF
        first = -1

        for c, off in enumerate(offs):
            val = cost0[c] + dp[row1 + off]
            if val < ans:
                ans = val
                first = c

        if first < 0 or ans >= INF:
            return ""

        # Greedy lexicographic reconstruction using exact suffix costs.
        res = bytearray()
        res.append(first + 97)

        state_c = first
        state_l = 1
        rem = dp[row1 + offs[first]]

        for i in range(1, n):
            ch = a[i] - 97
            cost_ch = cost[ch]
            nb = (i + 1) * STATES

            chosen = -1
            new_c = -1
            new_l = -1

            for x in range26:
                dc = cost_ch[x]

                if x == state_c:
                    nl = state_l + 1
                    if nl > 3:
                        nl = 3
                    val = dc + dp[nb + offs[state_c] + (nl - 1)]
                    if val == rem:
                        chosen = x
                        new_c = state_c
                        new_l = nl
                        break

                elif state_l == 3:
                    val = dc + dp[nb + offs[x]]
                    if val == rem:
                        chosen = x
                        new_c = x
                        new_l = 1
                        break

            if chosen < 0:
                return ""

            res.append(chosen + 97)
            state_c = new_c
            state_l = new_l
            rem = dp[nb + offs[state_c] + (state_l - 1)]

        return res.decode()