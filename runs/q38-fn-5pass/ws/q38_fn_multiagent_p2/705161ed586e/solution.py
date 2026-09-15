class Solution:
    def minCostGoodCaption(self, caption: str) -> str:
        n = len(caption)
        if n < 3:
            return ""

        A = 26
        INF = 10**9

        b = caption.encode()
        cost_table = [[abs(x - y) for x in range(A)] for y in range(A)]

        # Suffix DP values for the next row:
        # n1[c] = F(i+1, c, 1), n2[c] = F(i+1, c, 2), n3[c] = F(i+1, c, 3)
        # Base at position n: only an already-complete run (length >= 3) is valid.
        n1 = [INF] * A
        n2 = [INF] * A
        n3 = [0] * A

        # Reusable current-row arrays.
        c1 = [INF] * A
        c2 = [INF] * A
        c3 = [INF] * A

        # dec[i * 26 + c] stores the chosen character at position i
        # when the previous run has character c and length at least 3.
        # For lengths 1 or 2, the next character is forced to be c.
        dec = bytearray(n * A)

        for i in range(n - 1, 0, -1):
            costs = cost_table[b[i] - 97]

            # Best and second-best switch costs:
            # g[x] = cost to make position i equal x + F(i+1, x, 1)
            best1_val = INF
            best1_char = -1
            best2_val = INF
            best2_char = -1

            for x, cost_x in enumerate(costs):
                val = n1[x] + cost_x

                if val < best1_val:
                    best2_val = best1_val
                    best2_char = best1_char
                    best1_val = val
                    best1_char = x
                elif val == best1_val:
                    if val < best2_val:
                        best2_val = val
                        best2_char = x
                elif val < best2_val:
                    best2_val = val
                    best2_char = x

            off = i * A

            for c, cost in enumerate(costs):
                # Continue the current run.
                v2 = cost + n3[c]

                c1[c] = cost + n2[c]
                c2[c] = v2

                # Best switch to a different character.
                if best1_char != c:
                    sw_val = best1_val
                    sw_char = best1_char
                else:
                    sw_val = best2_val
                    sw_char = best2_char

                # For state length 3, choose lexicographically smallest
                # character among optimal continue/switch choices.
                if v2 < sw_val:
                    c3[c] = v2
                    dec[off + c] = c
                elif sw_val < v2:
                    c3[c] = sw_val
                    dec[off + c] = c if sw_char < 0 else sw_char
                else:
                    c3[c] = v2
                    if 0 <= sw_char < c:
                        dec[off + c] = sw_char
                    else:
                        dec[off + c] = c

            n1, c1 = c1, n1
            n2, c2 = c2, n2
            n3, c3 = c3, n3

        # Choose the first character: no previous run exists.
        costs0 = cost_table[b[0] - 97]
        ans = INF
        start_char = 0

        for x, cost_x in enumerate(costs0):
            val = cost_x + n1[x]
            if val < ans:
                ans = val
                start_char = x

        if ans >= INF:
            return ""

        # Reconstruct using stored decisions.
        res = bytearray(n)
        res[0] = 97 + start_char

        c = start_char
        length = 1

        for i in range(1, n):
            if length == 3:
                x = dec[i * A + c]
            else:
                x = c

            res[i] = 97 + x

            if x == c:
                if length < 3:
                    length += 1
            else:
                c = x
                length = 1

        if length < 3:
            return ""

        return res.decode()