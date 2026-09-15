from typing import List

class Solution:
    def permute(self, n: int, k: int) -> List[int]:
        CAP = 10 ** 15  # any true count >= CAP is treated as CAP; safe since k <= 1e15

        # capped factorials
        fact = [1] * (n + 2)
        for i in range(1, n + 2):
            v = fact[i - 1] * i
            fact[i] = CAP if v > CAP else v

        # Number of alternating completions given o remaining odds, e remaining evens,
        # and the next position requiring odd (want_odd True) or even (False).
        def fcount(o: int, e: int, want_odd: bool) -> int:
            m = o + e
            if want_odd:
                os_ = (m + 1) // 2
                es_ = m // 2
            else:
                os_ = m // 2
                es_ = (m + 1) // 2
            if o != os_ or e != es_:
                return 0
            v = fact[o] * fact[e]
            return CAP if v > CAP else v

        total_odd = (n + 1) // 2
        total_even = n // 2

        # Total valid alternating permutations (with capping).
        tot = 0
        for c in range(1, n + 1):
            co = c & 1
            ro = total_odd - co
            re = total_even - (1 - co)
            # after placing c, next must have opposite parity
            tot += fcount(ro, re, co == 0)
            if tot >= CAP:
                tot = CAP
                break
        if tot < k:
            return []

        used = [False] * (n + 1)
        res: List[int] = []
        o, e = total_odd, total_even

        for pos in range(n):
            if pos == 0:
                cands = range(1, n + 1)
            elif res[-1] % 2 == 0:
                cands = range(1, n + 1, 2)  # previous even -> next must be odd
            else:
                cands = range(2, n + 1, 2)  # previous odd -> next must be even

            chosen = -1
            for c in cands:
                if used[c]:
                    continue
                co = c & 1
                block = fcount(o - co, e - (1 - co), co == 0)
                if block == 0:
                    continue
                if k > block:
                    k -= block
                else:
                    chosen = c
                    break

            if chosen == -1:
                return []  # should not happen when tot >= k
            used[chosen] = True
            res.append(chosen)
            if chosen & 1:
                o -= 1
            else:
                e -= 1

        return res