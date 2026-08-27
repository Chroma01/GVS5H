from functools import lru_cache
from typing import List


class Solution:
    def permute(self, n: int, k: int) -> List[int]:
        CAP = k  # clamp all counts at k; enough for correct comparisons/subtractions

        @lru_cache(maxsize=None)
        def count(odds: int, evens: int, last: int) -> int:
            # last: 0 = no previous element, 1 = previous was odd, 2 = previous was even
            if odds == 0 and evens == 0:
                return 1
            total = 0
            if last != 1 and odds > 0:          # place an odd number next
                total += count(odds - 1, evens, 1)
                if total >= CAP:
                    return CAP
            if last != 2 and evens > 0:         # place an even number next
                total += count(odds, evens - 1, 2)
                if total >= CAP:
                    return CAP
            return total

        total = count((n + 1) // 2, n // 2, 0)
        if total < k:
            return []

        res = []
        used = [False] * (n + 1)
        odds = (n + 1) // 2
        evens = n // 2
        last = 0

        for _ in range(n):
            for x in range(1, n + 1):
                if used[x]:
                    continue
                p = 1 if x % 2 == 1 else 2
                if p == last:                   # same parity as previous -> not allowed
                    continue
                no = odds - (1 if p == 1 else 0)
                ne = evens - (1 if p == 2 else 0)
                block = count(no, ne, p)        # permutations with this prefix choice
                if k > block:
                    k -= block                  # skip this whole lexicographic block
                else:
                    res.append(x)               # k falls inside this block; fix x
                    used[x] = True
                    odds, evens = no, ne
                    last = p
                    break

        return res