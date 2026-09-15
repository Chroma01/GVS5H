from array import array

class Solution:
    def minCostGoodCaption(self, caption: str) -> str:
        n = len(caption)
        if n < 3:
            return ""
        s = [ord(ch) - 97 for ch in caption]
        INF = 10 ** 9
        size = (n + 1) * 26
        A = array('i', [INF]) * size   # f(i, last, 1)
        C = array('i', [0]) * size     # f(i, last, 3)
        B_next = [INF] * 26            # f(i+1, last, 2)

        # backward DP from i = n-1 down to 1
        for i in range(n - 1, 0, -1):
            x = s[i]
            off_next = (i + 1) * 26
            off_cur = i * 26

            # best1, best2 over c of |x-c| + f(i+1, c, 1)
            best1 = INF
            idx1 = -1
            best2 = INF
            for c in range(26):
                val = abs(x - c) + A[off_next + c]
                if val < best1:
                    best2 = best1
                    best1 = val
                    idx1 = c
                elif val < best2:
                    best2 = val

            B_cur = [0] * 26
            for last in range(26):
                d = abs(x - last)
                av = B_next[last]
                A[off_cur + last] = d + av if av < INF else INF
                bv = d + C[off_next + last]
                B_cur[last] = bv
                min_excl = best1 if idx1 != last else best2
                C[off_cur + last] = bv if bv < min_excl else min_excl
            B_next = B_cur

        # choose first character
        off1 = 26
        best_val = INF
        best_c = 0
        for c in range(26):
            val = abs(s[0] - c) + A[off1 + c]
            if val < best_val or (val == best_val and c < best_c):
                best_val = val
                best_c = c

        res = [0] * n
        res[0] = best_c
        last = best_c
        k = 1
        for i in range(1, n):
            x = s[i]
            if k < 3:
                c = last
                res[i] = c
                k += 1
            else:
                target = C[i * 26 + last]
                off_next = (i + 1) * 26
                chosen = -1
                for c in range(26):
                    if c == last:
                        val = abs(x - c) + C[off_next + c]
                    else:
                        val = abs(x - c) + A[off_next + c]
                    if val == target:
                        chosen = c
                        break
                res[i] = chosen
                if chosen == last:
                    k = 3
                else:
                    last = chosen
                    k = 1

        return ''.join(chr(97 + c) for c in res)