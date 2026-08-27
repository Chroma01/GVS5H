from typing import List


class Solution:
    def permute(self, n: int, k: int) -> List[int]:
        limit = k

        # Factorials capped at k, since larger values are indistinguishable
        # during rank unranking.
        fact = [1] * (n + 1)
        for i in range(1, n + 1):
            fact[i] = min(limit, fact[i - 1] * i)

        def arrangements(odd_count: int, even_count: int) -> int:
            if odd_count < 0 or even_count < 0:
                return 0
            return min(limit, fact[odd_count] * fact[even_count])

        def count_starting_with(
            parity: int, odd_count: int, even_count: int
        ) -> int:
            """
            Count alternating arrangements of all remaining values whose
            first value has the specified parity.
            """
            if odd_count < 0 or even_count < 0:
                return 0

            length = odd_count + even_count
            required_odd = (
                (length + 1) // 2 if parity == 1 else length // 2
            )
            required_even = length - required_odd

            if odd_count != required_odd or even_count != required_even:
                return 0

            return arrangements(odd_count, even_count)

        odd_total = (n + 1) // 2
        even_total = n // 2

        total = (
            count_starting_with(1, odd_total, even_total)
            + count_starting_with(0, odd_total, even_total)
        )
        total = min(limit, total)

        if k > total:
            return []

        used = [False] * (n + 1)
        odd_left = odd_total
        even_left = even_total
        previous_parity = -1
        result = []

        for _ in range(n):
            for value in range(1, n + 1):
                if used[value]:
                    continue

                parity = value & 1
                if previous_parity != -1 and parity == previous_parity:
                    continue

                next_odd = odd_left - (1 if parity == 1 else 0)
                next_even = even_left - (1 if parity == 0 else 0)

                if next_odd + next_even == 0:
                    block_size = 1
                else:
                    block_size = count_starting_with(
                        1 - parity, next_odd, next_even
                    )

                if k > block_size:
                    k -= block_size
                    continue

                used[value] = True
                result.append(value)
                odd_left = next_odd
                even_left = next_even
                previous_parity = parity
                break
            else:
                return []

        return result