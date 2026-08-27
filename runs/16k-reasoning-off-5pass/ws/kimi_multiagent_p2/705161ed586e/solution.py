from array import array


class Solution:
    def minCostGoodCaption(self, caption: str) -> str:
        n = len(caption)
        INF = 10 ** 9
        v = [ord(ch) - 97 for ch in caption]

        # G1/G2/G3[pos][c] = min cost to transform caption[pos:] into a valid
        # completion, given the previous output character is c and the current
        # open run has length 1 / 2 / >=3 (runs of length 1 or 2 must be
        # extended with the same char; a run of length >=3 may extend or close).
        # F0[pos] = min cost for caption[pos:] with no open run.
        size = (n + 1) * 26
        G1 = array('i', [INF]) * size
        G2 = array('i', [INF]) * size
        G3 = array('i', [INF]) * size
        F0 = array('i', [INF]) * (n + 1)

        base_n = n * 26
        for c in range(26):
            G3[base_n + c] = 0
        F0[n] = 0

        for pos in range(n - 1, -1, -1):
            x = v[pos]
            cur = pos * 26
            nxt = cur + 26
            # M = min over starting char c' of cost(pos, c') + G1[pos+1][c']
            M = INF
            for c in range(26):
                t = G1[nxt + c] + (x - c if x >= c else c - x)
                if t < M:
                    M = t
            F0[pos] = M
            for c in range(26):
                d = x - c if x >= c else c - x
                G1[cur + c] = G2[nxt + c] + d
                g3cont = G3[nxt + c] + d
                G2[cur + c] = g3cont
                G3[cur + c] = g3cont if g3cont < M else M

        total = F0[0]
        if total >= INF:
            return ""

        # Greedy reconstruction of the lexicographically smallest optimal
        # string. Invariant: used + (min cost from current state) == total.
        res = []
        prev = -1
        run = 0  # 0 = no open run, 1/2 = open run of that length, 3 = run >= 3
        used = 0
        for pos in range(n):
            x = v[pos]
            nxt = (pos + 1) * 26
            if run == 1 or run == 2:
                # Forced to extend the open run with prev.
                c = prev
                used += (x - c if x >= c else c - x)
                run += 1
                res.append(chr(97 + c))
                continue
            for c in range(26):
                # run is 0 (fresh start) or 3 (may extend or start new block).
                new_run = 3 if (run == 3 and c == prev) else 1
                nxt_val = G3[nxt + c] if new_run == 3 else G1[nxt + c]
                d = x - c if x >= c else c - x
                if used + d + nxt_val == total:
                    used += d
                    prev = c
                    run = new_run
                    res.append(chr(97 + c))
                    break
        return ''.join(res)