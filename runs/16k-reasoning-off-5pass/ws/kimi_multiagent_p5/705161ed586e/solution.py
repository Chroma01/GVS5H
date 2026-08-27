from array import array


class Solution:
    def minCostGoodCaption(self, caption: str) -> str:
        n = len(caption)
        if n < 3:
            return ""

        INF = 10 ** 9
        orig = [ord(ch) - 97 for ch in caption]

        # g[i] is an array of length 78: index c*3 + l, where l in {0,1,2}
        # represents current open run length 1, 2, or >=3 (3 = closable).
        # g[i][c][l] = min cost to fill positions i..n-1 given the previous
        # character (at i-1) is c and the current run length is l+1.
        rows = [None] * (n + 1)

        # Base row i == n: valid only if run length >= 3.
        base = array('i', [INF]) * 78
        for c in range(26):
            base[c * 3 + 2] = 0
        rows[n] = base

        for i in range(n - 1, -1, -1):
            o = orig[i]
            nxt = rows[i + 1]
            cur = array('i', [0]) * 78

            # closeBest = min over c' of cost_i(c') + g[i+1][c'][run=1]
            close_best = INF
            for c in range(26):
                v = nxt[c * 3] + abs(c - o)
                if v < close_best:
                    close_best = v

            for c in range(26):
                d = abs(c - o)
                b = c * 3
                # run length 1 -> must continue (becomes 2)
                v = nxt[b + 1] + d
                cur[b] = v if v < INF else INF
                # run length 2 -> must continue (becomes >=3)
                v = nxt[b + 2] + d
                cur[b + 1] = v if v < INF else INF
                # run length >=3 -> continue or close and start new run
                v = nxt[b + 2] + d
                if close_best < v:
                    v = close_best
                cur[b + 2] = v if v < INF else INF

            rows[i] = cur

        # Optimum: choose char for position 0, starting a run of length 1.
        row1 = rows[1]
        o0 = orig[0]
        best = INF
        for c in range(26):
            v = row1[c * 3] + abs(c - o0)
            if v < best:
                best = v
        if best >= INF:
            return ""

        # Greedy lexicographically smallest reconstruction.
        res = []
        prev = -1          # previous chosen char (-1 none)
        run = 0            # current run length (capped at 3)
        remaining = best   # optimal remaining cost from position i
        for i in range(n):
            o = orig[i]
            nxt = rows[i + 1]
            chosen = -1
            for c in range(26):
                if i > 0:
                    if c == prev:
                        nl = run + 1
                        if nl > 3:
                            nl = 3
                    else:
                        if run < 3:
                            continue  # cannot close a run shorter than 3
                        nl = 1
                    v = nxt[c * 3 + (nl - 1)] + abs(c - o)
                else:
                    nl = 1
                    v = nxt[c * 3] + abs(c - o)
                if v == remaining:
                    chosen = c
                    new_run = nl
                    break
            res.append(chr(97 + chosen))
            remaining -= abs(chosen - o)
            prev = chosen
            run = new_run

        return "".join(res)