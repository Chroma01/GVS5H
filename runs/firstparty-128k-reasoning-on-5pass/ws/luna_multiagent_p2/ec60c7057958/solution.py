from typing import List


class Solution:
    def permute(self, n: int, k: int) -> List[int]:
        CAP = 10**15

        factorial = [1] * (n + 1)
        for i in range(1, n + 1):
            factorial[i] = min(CAP, factorial[i - 1] * i)

        odd_total = (n + 1) // 2
        even_total = n // 2

        def completion_count(odd_count: int, even_count: int,
                             first_parity: int) -> int:
            remaining = odd_count + even_count

            if first_parity == 1:
                required_odd = (remaining + 1) // 2
            else:
                required_odd = remaining // 2

            required_even = remaining - required_odd

            if odd_count != required_odd or even_count != required_even:
                return 0

            return min(CAP, factorial[odd_count] * factorial[even_count])

        total = 0
        for start_parity in (0, 1):
            required_odd = (
                (n + 1) // 2 if start_parity == 1 else n // 2
            )
            required_even = n - required_odd

            if odd_total == required_odd and even_total == required_even:
                total = min(
                    CAP,
                    total + factorial[odd_total] * factorial[even_total]
                )

        if k > total:
            return []

        unused = [True] * (n + 1)
        result = []
        odd_left = odd_total
        even_left = even_total
        expected_parity = None

        for _ in range(n):
            for value in range(1, n + 1):
                if not unused[value]:
                    continue

                parity = value & 1

                if expected_parity is not None and parity != expected_parity:
                    continue

                new_odd = odd_left - parity
                new_even = even_left - (1 - parity)

                completions = completion_count(
                    new_odd,
                    new_even,
                    1 - parity
                )

                if completions == 0:
                    continue

                if k > completions:
                    k -= completions
                    continue

                unused[value] = False
                result.append(value)
                odd_left = new_odd
                even_left = new_even
                expected_parity = 1 - parity
                break

        return result