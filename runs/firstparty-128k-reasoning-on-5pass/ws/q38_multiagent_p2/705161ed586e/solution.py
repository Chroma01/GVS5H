class Solution:
    def minCostGoodCaption(self, caption: str) -> str:
        n = len(caption)
        if n < 3:
            return ""

        A = 26
        INF = 10**12
        BIG = 10**18
        R = range(A)

        cost_table = [[abs(b - c) for c in R] for b in R]
        bases = [ord(ch) - 97 for ch in caption]

        dp1 = [INF] * A
        dp2 = [INF] * A
        dp3 = [0] * A

        choices = bytearray(n * A)
        first = -1
        initial_cost = BIG

        for i in range(n - 1, -1, -1):
            costs = cost_table[bases[i]]

            best_val = BIG
            best_char = -1
            second_best_char = -1
            next_val = BIG
            next_char = -1

            for d in R:
                val = costs[d] + dp1[d]
                if val < best_val:
                    next_val = best_val
                    next_char = best_char
                    best_val = val
                    best_char = d
                    second_best_char = -1
                elif val == best_val:
                    if second_best_char == -1:
                        second_best_char = d
                elif val < next_val:
                    next_val = val
                    next_char = d

            if i == 0:
                first = best_char
                initial_cost = best_val

            new1 = [0] * A
            new2 = [0] * A
            new3 = [0] * A
            idx = i * A

            for c in R:
                cost = costs[c]
                n1 = cost + dp2[c]
                cont = cost + dp3[c]
                n2 = cont

                if c == best_char:
                    if second_best_char != -1:
                        bo_val = best_val
                        bo_char = second_best_char
                    else:
                        bo_val = next_val
                        bo_char = next_char
                else:
                    bo_val = best_val
                    bo_char = best_char

                if cont <= bo_val:
                    n3 = cont
                    ch = c
                    if bo_val == cont and bo_char != -1 and bo_char < c:
                        ch = bo_char
                else:
                    n3 = bo_val
                    ch = bo_char
                    if ch == -1:
                        ch = c

                new1[c] = n1
                new2[c] = n2
                new3[c] = n3
                choices[idx + c] = ch

            dp1, dp2, dp3 = new1, new2, new3

        if first < 0 or initial_cost >= INF:
            return ""

        res = bytearray(n)
        res[0] = 97 + first
        c = first
        length = 1

        for i in range(1, n):
            if length < 3:
                res[i] = 97 + c
                length += 1
            else:
                x = choices[i * A + c]
                res[i] = 97 + x
                if x == c:
                    length = 3
                else:
                    c = x
                    length = 1

        return res.decode()