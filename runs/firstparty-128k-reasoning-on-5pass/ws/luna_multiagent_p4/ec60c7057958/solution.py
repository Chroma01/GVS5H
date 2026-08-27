from typing import List
from functools import lru_cache


class Solution:
    def permute(self, n: int, k: int) -> List[int]:
        LIMIT = 10**15

        @lru_cache(maxsize=None)
        def count(odd: int, even: int, previous: int) -> int:
            """
            Number of valid labeled completions.

            previous:
              -1: no previous element
               0: previous element was even
               1: previous element was odd
            """
            if odd + even == 0:
                return 1

            total = 0

            # Choose an odd next element if allowed.
            if odd > 0 and previous != 1:
                total += odd * count(odd - 1, even, 1)
                if total >= LIMIT:
                    return LIMIT

            # Choose an even next element if allowed.
            if even > 0 and previous != 0:
                total += even * count(odd, even - 1, 0)
                if total >= LIMIT:
                    return LIMIT

            return total

        odd_count = (n + 1) // 2
        even_count = n // 2

        if count(odd_count, even_count, -1) < k:
            return []

        used = [False] * (n + 1)
        answer = []
        previous = -1
        odd = odd_count
        even = even_count

        for _ in range(n):
            for value in range(1, n + 1):
                if used[value]:
                    continue

                parity = value & 1
                if parity == 1:
                    if previous == 1 or odd == 0:
                        continue
                    ways = count(odd - 1, even, 1)
                else:
                    if previous == 0 or even == 0:
                        continue
                    ways = count(odd, even - 1, 0)

                if k > ways:
                    k -= ways
                    continue

                used[value] = True
                answer.append(value)
                previous = parity
                if parity == 1:
                    odd -= 1
                else:
                    even -= 1
                break

        return answer