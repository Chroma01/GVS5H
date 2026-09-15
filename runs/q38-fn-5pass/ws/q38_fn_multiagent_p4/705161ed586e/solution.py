from array import array

class Solution:
    def minCostGoodCaption(self, caption: str) -> str:
        n = len(caption)
        if n < 3:
            return ""

        INF = 10**9

        # cost_table[source][target] = minimum operations to change source to target
        cost_table = tuple(tuple(abs(i - j) for j in range(26)) for i in range(26))
        rows = [cost_table[ord(ch) - 97] for ch in caption]

        # Flat arrays: index = position * 26 + character
        # dp1: suffix cost when current open run has length exactly 1
        # dp2: suffix cost when current open run has length exactly 2
        # dp3: suffix cost when current open run has length at least 3
        size = (n + 1) * 26
        dp1 = array('i', [INF]) * size
        dp2 = array('i', [INF]) * size
        dp3 = array('i', [INF]) * size

        # Base case at position n: only a valid run (length >= 3) can end here.
        base_n = n * 26
        for c in range(26):
            dp3[base_n + c] = 0

        d1, d2, d3 = dp1, dp2, dp3
        range26 = range(26)
        conts = [INF] * 26

        # Backward DP.
        for i in range(n - 1, -1, -1):
            b = i * 26
            nb = b + 26
            row = rows[i]

            # For dp3 switch transitions, we need:
            # min_{x != c} (cost_i[x] + dp1[i + 1][x])
            # Keep best and second-best to exclude current character in O(1).
            best = INF
            second = INF
            best_c = -1

            for c in range26:
                w = row[c]

                # dp1: forced to continue same character.
                nxt = d2[nb + c]
                if nxt < INF:
                    d1[b + c] = w + nxt

                # dp2: forced to continue same character, becoming length >= 3.
                nxt = d3[nb + c]
                if nxt < INF:
                    val = w + nxt
                    d2[b + c] = val
                    conts[c] = val
                else:
                    conts[c] = INF

                # Candidate value for switching to character c at position i.
                nxt = d1[nb + c]
                if nxt < INF:
                    v = w + nxt
                else:
                    v = INF

                if v < best:
                    second = best
                    best = v
                    best_c = c
                elif v < second:
                    second = v

            for c in range26:
                # dp3: either continue current run, or switch to a different character.
                sw = best if best_c != c else second
                cont = conts[c]
                d3[b + c] = cont if cont <= sw else sw

        # Initial choice: pick the first character, then state is length 1 at position 1.
        row0 = rows[0]
        opt = INF
        first = -1
        base1 = 26

        for c in range26:
            nxt = d1[base1 + c]
            if nxt < INF:
                total = row0[c] + nxt
            else:
                total = INF

            # Strict '<' keeps the smallest character on ties.
            if total < opt:
                opt = total
                first = c

        if opt >= INF or first < 0:
            return ""

        # Greedy reconstruction for lexicographically smallest optimal caption.
        res = bytearray(n)
        res[0] = first + 97

        prev = first
        length = 1
        cur = d1[base1 + first]

        for i in range(1, n):
            b = i * 26
            nb = b + 26
            row = rows[i]

            chosen = -1
            nxt = INF

            for x in range26:
                w = row[x]

                if x == prev:
                    if length == 1:
                        cand = d2[nb + prev]
                    else:
                        cand = d3[nb + prev]
                elif length == 3:
                    cand = d1[nb + x]
                else:
                    continue

                if cand < INF and w + cand == cur:
                    chosen = x
                    nxt = cand
                    break

            if chosen < 0:
                return ""

            res[i] = chosen + 97

            if chosen == prev:
                if length < 3:
                    length += 1
            else:
                prev = chosen
                length = 1

            cur = nxt

        if length != 3 or cur != 0:
            return ""

        return res.decode()