from typing import List

class Solution:
    def permute(self, n: int, k: int) -> List[int]:
        INF = 10**18  # safe upper bound > 10**15

        # Count odds and evens in [1..n]
        odd_total = (n + 1) // 2
        even_total = n // 2

        # Pre‑compute capped factorials
        fact = [1] * (n + 1)
        for i in range(1, n + 1):
            fact[i] = min(fact[i - 1] * i, INF)

        # Total number of alternating permutations
        if odd_total > even_total + 1 or even_total > odd_total + 1:
            return []
        if odd_total == even_total:
            total = min(fact[odd_total] * fact[even_total] * 2, INF)
        else:
            total = min(fact[odd_total] * fact[even_total], INF)
        if k > total:
            return []

        # Helper: count completions of a suffix given remaining odds/evens and required next parity
        def count_completions(odd_rem: int, even_rem: int, next_parity: int) -> int:
            L = odd_rem + even_rem
            if next_parity == 1:          # next must be odd
                odd_needed = (L + 1) // 2
                even_needed = L // 2
            else:                         # next must be even
                odd_needed = L // 2
                even_needed = (L + 1) // 2
            if odd_rem != odd_needed or even_rem != even_needed:
                return 0
            return min(fact[odd_rem] * fact[even_rem], INF)

        used = [False] * (n + 1)
        result: List[int] = []
        odd_rem = odd_total
        even_rem = even_total
        last_parity = None  # None for the first element

        for pos in range(n):
            found = False
            # try numbers in increasing order
            for x in range(1, n + 1):
                if used[x]:
                    continue
                # parity restriction (except for the first position)
                if pos > 0 and (x % 2) == last_parity:
                    continue
                # simulate picking x
                odd_rem2 = odd_rem - (x % 2)
                even_rem2 = even_rem - (1 - (x % 2))
                next_parity = 1 - (x % 2)  # opposite parity for the next slot
                cnt = count_completions(odd_rem2, even_rem2, next_parity)
                if k > cnt:
                    k -= cnt
                else:
                    # choose x
                    result.append(x)
                    used[x] = True
                    odd_rem = odd_rem2
                    even_rem = even_rem2
                    last_parity = x % 2
                    found = True
                    break
            if not found:
                # No admissible candidate – k is out of range
                return []
        return result