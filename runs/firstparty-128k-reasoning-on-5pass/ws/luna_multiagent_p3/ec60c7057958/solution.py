from typing import List


class Solution:
    def permute(self, n: int, k: int) -> List[int]:
        odd_total = (n + 1) // 2
        even_total = n // 2
        cap = k

        factorial = [1] * (n + 1)
        for i in range(1, n + 1):
            factorial[i] = min(cap, factorial[i - 1] * i)

        def multiply_capped(a: int, b: int) -> int:
            if a == 0 or b == 0:
                return 0
            if a > cap // b:
                return cap
            return a * b

        def count_completions(odd: int, even: int, next_parity: int) -> int:
            remaining = odd + even

            if next_parity == 1:
                required_odd = (remaining + 1) // 2
                required_even = remaining // 2
            else:
                required_even = (remaining + 1) // 2
                required_odd = remaining // 2

            if odd != required_odd or even != required_even:
                return 0

            return multiply_capped(factorial[odd], factorial[even])

        if abs(odd_total - even_total) > 1:
            return []

        base_count = multiply_capped(
            factorial[odd_total],
            factorial[even_total],
        )

        if odd_total == even_total:
            total_count = min(cap, 2 * base_count)
        else:
            total_count = base_count

        if k > total_count:
            return []

        unused = [True] * (n + 1)
        odd = odd_total
        even = even_total
        result = []

        for _ in range(n):
            previous_parity = result[-1] % 2 if result else None

            for value in range(1, n + 1):
                if not unused[value]:
                    continue

                parity = value % 2
                if previous_parity is not None and parity == previous_parity:
                    continue

                remaining_odd = odd - (parity == 1)
                remaining_even = even - (parity == 0)

                ways = count_completions(
                    remaining_odd,
                    remaining_even,
                    1 - parity,
                )

                if k > ways:
                    k -= ways
                    continue

                result.append(value)
                unused[value] = False
                odd = remaining_odd
                even = remaining_even
                break

        return result