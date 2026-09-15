class Solution:
    def minCostGoodCaption(self, caption: str) -> str:
        from array import array

        n = len(caption)
        if n < 3:
            return ""

        S = 78
        INF = 10**9
        rng = range(26)

        arr = [ord(ch) - 97 for ch in caption]
        dist = [[abs(i - j) for j in rng] for i in rng]

        # State index: char * 3 + category
        # category 0: current run length exactly 1
        # category 1: current run length exactly 2
        # category 2: current run length at least 3
        c3 = [c * 3 for c in rng]
        c3_1 = [x + 1 for x in c3]
        c3_2 = [x + 2 for x in c3]

        # dp[pos][state] = minimum cost to finish caption[pos:]
        # given that before pos there is an open run described by state.
        dp = array('i', [INF]) * ((n + 1) * S)

        end_base = n * S
        for c in rng:
            dp[end_base + c3_2[c]] = 0

        next1 = [0] * 26
        next2 = [0] * 26
        next3 = [0] * 26

        for pos in range(n - 1, -1, -1):
            nb = (pos + 1) * S

            for c in rng:
                j = nb + c3[c]
                next1[c] = dp[j]
                next2[c] = dp[j + 1]
                next3[c] = dp[j + 2]

            d = dist[arr[pos]]

            # best1/best2 over x of:
            # d[x] + dp[pos + 1][x, length 1]
            # Used when current run has length >= 3 and we start a new run.
            best1 = INF
            best1_c = -1
            best2 = INF
            best2_c = -1

            for x in rng:
                v = d[x] + next1[x]
                if v < best1:
                    best2 = best1
                    best2_c = best1_c
                    best1 = v
                    best1_c = x
                elif v < best2:
                    best2 = v
                    best2_c = x

            b = pos * S

            for c in rng:
                dc = d[c]
                j = b + c3[c]

                # If current run length is 1, it must be extended to length 2.
                dp[j] = dc + next2[c]

                # If current run length is 2, it must be extended to length >= 3.
                # If current run length is >= 3, continuing the same run has the same cost.
                extend = dc + next3[c]
                dp[j + 1] = extend

                # If current run length is >= 3, we may also start a new run
                # with a different character.
                excl = best1 if best1_c != c else best2
                dp[j + 2] = extend if extend <= excl else excl

        # Choose the first character. There is no open run before position 0.
        d0 = dist[arr[0]]
        total = INF
        first = -1
        base1 = S

        for x in rng:
            v = d0[x] + dp[base1 + c3[x]]
            if v < total:
                total = v
                first = x

        if first < 0 or total >= INF:
            return ""

        # Transition table for greedy reconstruction.
        trans = [[-1] * 26 for _ in range(S)]
        for c in rng:
            s1 = c3[c]
            s2 = c3_1[c]
            s3 = c3_2[c]
            for x in rng:
                if x == c:
                    trans[s1][x] = s2
                    trans[s2][x] = s3
                    trans[s3][x] = s3
                else:
                    trans[s3][x] = c3[x]

        res = bytearray(n)
        res[0] = 97 + first
        state = c3[first]

        # Greedily reconstruct the lexicographically smallest optimal string.
        for pos in range(1, n):
            cur = dp[pos * S + state]
            d = dist[arr[pos]]
            nb = (pos + 1) * S
            row = trans[state]

            chosen = False
            for x in rng:
                ns = row[x]
                if ns != -1 and d[x] + dp[nb + ns] == cur:
                    res[pos] = 97 + x
                    state = ns
                    chosen = True
                    break

            if not chosen:
                return ""

        return res.decode()