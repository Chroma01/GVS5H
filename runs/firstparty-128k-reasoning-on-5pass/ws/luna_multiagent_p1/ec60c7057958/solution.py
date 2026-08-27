from functools import lru_cache
from typing import List


class Solution:
    def permute(self, n: int, k: int) -> List[int]:
        CAP = 10**15
        odd_total = (n + 1) // 2
        even_total = n // 2

        @lru_cache(maxsize=None)
        def ways(odd: int, even: int, required_parity: int) -> int:
            """Number of completions using remaining values."""
            if odd + even == 0:
                return 1

            if required_parity == 1:
                if odd == 0:
                    return 0
                result = odd * ways(odd - 1, even, 0)
            else:
                if even == 0:
                    return 0
                result = even * ways(odd, even - 1, 1)

            return min(CAP, result)

        odd_first = (
            odd_total * ways(odd_total - 1, even_total, 0)
            if odd_total
            else 0
        )
        even_first = (
            even_total * ways(odd_total, even_total - 1, 1)
            if even_total
            else 0
        )
        total = min(CAP, odd_first + even_first)

        if k > total:
            return []

        used = [False] * (n + 1)
        answer = []
        odd_remaining = odd_total
        even_remaining = even_total
        previous_parity = None

        for _ in range(n):
            for value in range(1, n + 1):
                if used[value]:
                    continue

                parity = value % 2
                if (
                    previous_parity is not None
                    and parity == previous_parity
                ):
                    continue

                if parity == 1:
                    block = ways(odd_remaining - 1, even_remaining, 0)
                else:
                    block = ways(odd_remaining, even_remaining - 1, 1)

                if k > block:
                    k -= block
                    continue

                answer.append(value)
                used[value] = True
                previous_parity = parity

                if parity == 1:
                    odd_remaining -= 1
                else:
                    even_remaining -= 1
                break
            else:
                return []

        return answer