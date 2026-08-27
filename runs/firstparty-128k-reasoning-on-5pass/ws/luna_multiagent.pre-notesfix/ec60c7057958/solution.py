from typing import List


class Solution:
    def permute(self, n: int, k: int) -> List[int]:
        cap = k

        # Capped factorials are sufficient because all comparisons are against k.
        factorial = [1] * (n + 1)
        for i in range(1, n + 1):
            factorial[i] = min(cap, factorial[i - 1] * i)

        odd_total = (n + 1) // 2
        even_total = n // 2

        def completion_count(odd_left: int, even_left: int,
                             last_parity: int) -> int:
            """
            Count valid completions after the prefix has been fixed.
            last_parity: 1 for odd, 0 for even.
            """
            remaining = odd_left + even_left
            next_parity = 1 - last_parity

            if next_parity == 1:
                required_odd = (remaining + 1) // 2
                required_even = remaining // 2
            else:
                required_even = (remaining + 1) // 2
                required_odd = remaining // 2

            if odd_left != required_odd or even_left != required_even:
                return 0

            return min(cap, factorial[odd_left] * factorial[even_left])

        # Count all valid permutations before constructing the requested one.
        total = 0
        for value in range(1, n + 1):
            parity = value & 1
            odd_left = odd_total - (1 if parity else 0)
            even_left = even_total - (0 if parity else 1)

            count = completion_count(odd_left, even_left, parity)
            total = min(cap, total + count)

        if total < k:
            return []

        used = [False] * (n + 1)
        answer = []
        odd_left = odd_total
        even_left = even_total
        last_parity = None

        for _ in range(n):
            for value in range(1, n + 1):
                if used[value]:
                    continue

                parity = value & 1
                if last_parity is not None and parity == last_parity:
                    continue

                next_odd = odd_left - (1 if parity else 0)
                next_even = even_left - (0 if parity else 1)
                if next_odd < 0 or next_even < 0:
                    continue

                count = completion_count(next_odd, next_even, parity)
                if count == 0:
                    continue

                if k > count:
                    k -= count
                    continue

                used[value] = True
                answer.append(value)
                odd_left = next_odd
                even_left = next_even
                last_parity = parity
                break
            else:
                return []

        return answer