from typing import List


class Solution:
    def permute(self, n: int, k: int) -> List[int]:
        # precompute factorials
        fact = [1] * (n + 2)
        for i in range(1, n + 2):
            fact[i] = fact[i - 1] * i

        o = (n + 1) // 2   # count of odd numbers in 1..n
        e = n // 2         # count of even numbers in 1..n

        total = fact[o] * fact[e] * (2 if n % 2 == 0 else 1)
        if k > total:
            return []

        odds = list(range(1, n + 1, 2))
        evens = list(range(2, n + 1, 2))

        res = []
        prev = None
        for pos in range(n):
            if pos == 0:
                if n % 2 == 0:
                    # both parities are feasible starts; block sizes coincide
                    cands = sorted(odds + evens)      # simply 1..n
                    B = fact[o - 1] * fact[e]
                else:
                    cands = odds                      # must start with an odd
                    B = fact[o - 1] * fact[e]
            else:
                if prev % 2 == 1:
                    cands = evens
                    B = fact[len(odds)] * fact[len(evens) - 1]
                else:
                    cands = odds
                    B = fact[len(odds) - 1] * fact[len(evens)]

            idx = (k - 1) // B
            k -= idx * B
            v = cands[idx]
            res.append(v)
            prev = v
            if v % 2 == 1:
                odds.remove(v)
            else:
                evens.remove(v)

        return res